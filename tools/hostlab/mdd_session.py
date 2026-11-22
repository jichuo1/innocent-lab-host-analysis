"""Owned, bounded MeguvizDexDash `serve` session using typed B1 batches."""
from __future__ import annotations

from concurrent.futures import Future, TimeoutError as FutureTimeout
from dataclasses import dataclass, field
import os
from pathlib import Path
import queue
import re
import struct
import subprocess
import threading
import time
import json
from typing import Any, Iterator

import analysis_batch as batch
import install_meguvizdexdash
import process_control

STREAM_PROTOCOL = "mdd.cli-stream.v1"
BATCH_SCHEMA = "mdd.sdk-batch.v1"
DIALECT = "dexsql-0.1.0"
NON_SCALAR_TEXT = "lossy-replacement"
DEFAULT_SQL_LIMITS = {
    "steps": 40_000_000_000,
    "scanned_rows": 4_000_000_000,
    "result_rows": 4_000_000,
}
DEFAULT_BATCH_ROWS = 10_000
MAX_SQL_BYTES = 256 * 1024
MAX_LINE_BYTES = 64 * 1024 * 1024
MAX_RESPONSE_BYTES = 512 * 1024 * 1024
QUEUE_SLOTS = 8
INCOMPLETE_CODES = ("INCOMPLETE_FACTS", "PARTIAL_INPUT")
COVERAGE_STATES = ("complete", "partial", "unknown")
OPERATION_STATES = ("ok", "error", "cancelled")
_LEGACY_ENV = ("DEXQ_CACHE_DIR", "DEXQ_ROOTS", "DEXQ_WORKERS")


class EngineError(RuntimeError):
    code = "INTERNAL_FAULT"
    stage = "hostlab.session"

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        stage: str | None = None,
        body: dict[str, Any] | None = None,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        if code is None and body and isinstance(body.get("code"), str):
            code = body["code"]
        if stage is None and body and isinstance(body.get("stage"), str):
            stage = body["stage"]
        if code is not None:
            self.code = code
        if stage is not None:
            self.stage = stage
        error = dict(body) if body else {"code": self.code, "stage": self.stage, "message": message}
        self.detail = dict(detail or {}, error=error)


class EngineRejected(EngineError):
    """The engine refused the statement or the open."""


class EngineIncomplete(EngineError):
    """The engine answered without complete input/fact coverage."""

    code = "INCOMPLETE_FACTS"


class EngineProtocolError(EngineError):
    """Stream frame violated `mdd.cli-stream.v1` or contradicted itself."""

    code = "INTERNAL_FAULT"


class EngineLost(EngineError):
    """The engine process exited before delivering a terminal frame."""

    code = "WORKER_LOST"


class SessionClosed(EngineError):
    code = "SNAPSHOT_CLOSED"


@dataclass(frozen=True)
class DexMutf8:
    raw: bytes
    utf16_units: int

    def text(self) -> str:
        units: list[int] = []
        data, i = self.raw, 0
        while i < len(data):
            b = data[i]
            if b < 0x80:
                units.append(b)
                i += 1
            elif b & 0xE0 == 0xC0 and i + 1 < len(data):
                units.append(((b & 0x1F) << 6) | (data[i + 1] & 0x3F))
                i += 2
            elif b & 0xF0 == 0xE0 and i + 2 < len(data):
                units.append(((b & 0x0F) << 12) | ((data[i + 1] & 0x3F) << 6) | (data[i + 2] & 0x3F))
                i += 3
            else:
                raise EngineProtocolError("a dex_mutf8 cell is not well-formed MUTF-8")
        return b"".join(struct.pack(">H", u) for u in units).decode("utf-16-be", "surrogatepass")


def _issue_summary(issue: Any) -> dict[str, Any]:
    if not isinstance(issue, dict):
        return {"issue": str(issue)[:500]}
    error = issue.get("error") if isinstance(issue.get("error"), dict) else {}
    details = error.get("details")
    return {
        "dex_occurrence_id": issue.get("dex_occurrence_id"),
        "layers": issue.get("layers"),
        "code": error.get("code"),
        "stage": error.get("stage"),
        "message": str(error.get("message", ""))[:300],
        "reason": details.get("reason") if isinstance(details, dict) else None,
    }


def _completeness(operation_status: str, coverage_input: Any, coverage_facts: Any, execution_complete: Any) -> dict[str, Any]:
    if (
        operation_status not in OPERATION_STATES
        or coverage_input not in COVERAGE_STATES
        or coverage_facts not in COVERAGE_STATES
        or type(execution_complete) is not bool
    ):
        raise EngineProtocolError("unrecognised operation status or coverage state")
    reasons: list[str] = []
    if operation_status != "ok":
        reasons.append("operation_" + operation_status)
    for name, state in (("input", coverage_input), ("facts", coverage_facts)):
        if state != "complete":
            reasons.append(f"{name}_{state}")
    if not execution_complete:
        reasons.append("execution_incomplete")
    complete = not reasons
    return {
        "complete": complete,
        "partial": not complete and operation_status == "ok",
        "failed": operation_status != "ok",
        "reasons": reasons,
    }


@dataclass
class Opened:
    dex_count: int
    layer_issues: list[Any]
    profile: str
    sql_dialect: str
    snapshot_id: str
    scope_id: str
    layers: list[str] | None = None

    def describe(self) -> dict[str, Any]:
        return {
            "protocol": STREAM_PROTOCOL,
            "dex_count": self.dex_count,
            "profile": self.profile,
            "sql_dialect": self.sql_dialect,
            "snapshot_id": self.snapshot_id,
            "scope_id": self.scope_id,
            "layer_issues": [_issue_summary(issue) for issue in self.layer_issues],
        }


@dataclass
class Statement:
    id: str
    sql: str
    rows: int = 0
    next_sequence: int = 0
    finished: bool = False


@dataclass
class Coverage:
    statements: int = 0
    abandoned: int = 0
    input: str = "complete"
    facts: str = "complete"
    layers: set[str] = field(default_factory=set)
    issues: list[Any] = field(default_factory=list)

    @staticmethod
    def _worse(a: str, b: str) -> str:
        order = {"complete": 0, "partial": 1, "unknown": 2}
        return a if order.get(a, 3) >= order.get(b, 3) else b

    def add(self, coverage: dict[str, Any]) -> None:
        self.statements += 1
        self.input = self._worse(self.input, str(coverage.get("input", "unknown")))
        self.facts = self._worse(self.facts, str(coverage.get("facts", "unknown")))
        self.layers.update(coverage.get("required_layers") or [])
        self.issues.extend(coverage.get("issues") or [])

    def describe(self) -> dict[str, Any]:
        return {
            "statements": self.statements,
            "abandoned": self.abandoned,
            "input": self.input,
            "facts": self.facts,
            "required_layers": sorted(self.layers),
            "issues": list(self.issues),
        }


def child_environment(apk: Path, threads: int) -> dict[str, str]:
    base = batch.child_environment(apk, threads)
    env = {k: v for k, v in base.items() if k not in _LEGACY_ENV}
    effective = min(threads, os.cpu_count() or 1)
    env["MDD_FACTS_THREADS"] = str(max(1, effective))
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def serve_command(
    binary: str | os.PathLike[str],
    apk: Path,
    *,
    dialect: str = DIALECT,
    timeout_seconds: float = 900,
    sql_limits: dict[str, int] | None = None,
    non_scalar_text: str = NON_SCALAR_TEXT,
) -> list[str]:
    command = [
        str(binary),
        "serve",
        "--dialect",
        dialect,
        "--deadline-ms",
        str(max(1, int(timeout_seconds * 1000))),
    ]
    limits = DEFAULT_SQL_LIMITS if sql_limits is None else sql_limits
    for key in ("steps", "scanned_rows", "result_rows"):
        if key in limits:
            command += ["--sql-max-" + key.replace("_", "-"), str(int(limits[key]))]
    if non_scalar_text != "reject":
        command += ["--non-scalar-text", non_scalar_text]
    command += ["--input", str(apk)]
    return command


class Transport:
    """Drives one `meguvizdexdash serve` subprocess over `mdd.cli-stream.v1` JSONL."""

    CLOSE_WAIT = 5.0

    def __init__(
        self,
        command: list[str],
        env: dict[str, str] | None,
        deadline: float,
        *,
        max_line_bytes: int = MAX_LINE_BYTES,
    ) -> None:
        self.command = list(command)
        self.env = env
        self.deadline = deadline
        self.max_line = max_line_bytes
        self.process: subprocess.Popen[bytes] | None = None
        self.messages: queue.Queue[Any] = queue.Queue(maxsize=QUEUE_SLOTS)
        self.closed = threading.Event()
        self.reader: threading.Thread | None = None
        self.stderr_reader: threading.Thread | None = None
        self.stderr_tail = bytearray()
        self.broken: EngineError | None = None
        self.abandoned: set[str] = set()
        self.statement_count = 0
        self.response_bytes = 0
        self.opened: Opened | None = None
        self.coverage = Coverage()
        self.last_terminal: dict[str, Any] | None = None

    def start(self) -> Opened:
        self.process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self.env,
            close_fds=True,
            start_new_session=os.name != "nt",
        )
        self.reader = threading.Thread(target=self._read_stdout, daemon=True, name="hostlab-mdd-reader")
        self.stderr_reader = threading.Thread(target=self._read_stderr, daemon=True, name="hostlab-mdd-stderr")
        self.reader.start()
        self.stderr_reader.start()
        frame = self._frame(opening=True)
        if frame.get("kind") != "opened" or frame.get("protocol") != STREAM_PROTOCOL:
            raise self._broken(EngineProtocolError("the engine did not open with the expected stream protocol"))
        dataset = frame.get("dataset")
        if not isinstance(dataset, dict):
            raise self._broken(EngineProtocolError("the opened frame does not describe a dataset"))
        try:
            self.opened = Opened(
                int(dataset["dex_count"]),
                list(dataset["layer_issues"]),
                str(dataset["profile"]),
                str(dataset["sql_dialect"]),
                str(dataset["snapshot_id"]),
                str(dataset["scope_id"]),
                list(dataset["layers"]) if isinstance(dataset.get("layers"), list) else None,
            )
        except (KeyError, TypeError, ValueError):
            raise self._broken(EngineProtocolError("the opened frame does not describe a dataset")) from None
        return self.opened

    def _read_stdout(self) -> None:
        stream = self.process.stdout
        while not self.closed.is_set():
            try:
                line = stream.readline(self.max_line + 1)
                item: Any = line
                if line and (len(line) > self.max_line or not line.endswith(b"\n")):
                    item = EngineProtocolError("an engine frame exceeds its byte budget or ends without a newline")
            except (OSError, ValueError):
                item = EngineLost("the engine output could not be read")
            while not self.closed.is_set():
                try:
                    self.messages.put(item, timeout=0.1)
                    break
                except queue.Full:
                    continue
            if not item or isinstance(item, Exception):
                return

    def _read_stderr(self) -> None:
        stream = self.process.stderr
        try:
            while not self.closed.is_set():
                chunk = stream.read1(4096)
                if not chunk:
                    return
                self.stderr_tail.extend(chunk)
                del self.stderr_tail[:-8192]
        except (OSError, ValueError):
            return

    def stderr_text(self) -> str:
        return bytes(self.stderr_tail).decode("utf-8", "replace")

    def _broken(self, error: EngineError) -> EngineError:
        if self.broken is None:
            self.broken = error
        return error

    def _refusal(self) -> EngineError | None:
        for line in reversed(self.stderr_text().strip().splitlines()):
            try:
                body = json.loads(line)
            except ValueError:
                continue
            if isinstance(body, dict) and isinstance(body.get("code"), str):
                return EngineRejected(str(body.get("message", "the engine refused to start")), body=body)
        return None

    def _frame(self, opening: bool = False) -> dict[str, Any]:
        while True:
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise self._broken_timeout("native audit deadline exhausted")
            try:
                item = self.messages.get(timeout=remaining)
            except queue.Empty:
                raise self._broken_timeout("native audit CLI response timed out") from None
            if isinstance(item, Exception):
                raise self._broken(item)
            if not item:
                if self.process is not None:
                    try:
                        self.process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        pass
                if self.stderr_reader is not None:
                    self.stderr_reader.join(timeout=2)
                refusal = self._refusal() if opening or self.opened is None else None
                if refusal is not None:
                    raise self._broken(refusal)
                code = self.process.returncode if self.process is not None else None
                raise self._broken(
                    EngineLost(
                        "native audit CLI exited before a complete result"
                        + (f" (exit status {code})" if code is not None else "")
                        + (": " + self.stderr_text()[-400:] if self.stderr_text() else "")
                    )
                )
            self.response_bytes += len(item)
            if self.response_bytes > MAX_RESPONSE_BYTES:
                raise self._broken(EngineProtocolError("native audit CLI response exceeds byte budget"))
            if not item.strip():
                continue
            try:
                frame = json.loads(item)
            except ValueError:
                raise self._broken(EngineProtocolError("a line of the engine output is not JSON")) from None
            if not isinstance(frame, dict) or not isinstance(frame.get("kind"), str):
                raise self._broken(EngineProtocolError("a frame that is not an object with a kind"))
            return frame

    def _broken_timeout(self, message: str) -> TimeoutError:
        error = TimeoutError(message)
        if self.broken is None:
            self.broken = EngineError(message, code="DEADLINE_EXCEEDED")
        return error

    def send(self, request: dict[str, Any]) -> None:
        data = (json.dumps(request) + "\n").encode("utf-8")
        done: Future[None] = Future()

        def write() -> None:
            try:
                self.process.stdin.write(data)
                self.process.stdin.flush()
                done.set_result(None)
            except BaseException as exc:
                done.set_exception(exc)

        writer = threading.Thread(target=write, daemon=True, name="hostlab-mdd-writer")
        writer.start()
        try:
            done.result(timeout=max(0.001, self.deadline - time.monotonic()))
        except FutureTimeout:
            self.kill()
            raise self._broken_timeout("native audit CLI input timed out") from None
        except (BrokenPipeError, OSError, ValueError):
            raise self._broken(EngineLost("the engine closed its input before the statement was sent")) from None

    def statement(self, sql: str, **options: Any) -> Iterator[tuple[str, dict[str, Any]]]:
        if self.broken is not None:
            raise SessionClosed("the session is broken: " + str(self.broken))
        if self.closed.is_set() or self.process is None:
            raise SessionClosed("the session is closed")
        if time.monotonic() >= self.deadline:
            raise self._broken_timeout("native audit deadline exhausted")
        if len(sql.encode("utf-8")) > MAX_SQL_BYTES:
            raise EngineProtocolError(
                "native audit SQL exceeds its byte budget",
                code="INVALID_ARGUMENT",
                stage="hostlab.session",
            )
        self._skip_abandoned()
        self.statement_count += 1
        state = Statement(f"s{self.statement_count}", sql)
        self.send({"id": state.id, "sql": sql, **options})
        try:
            while True:
                frame = self._frame()
                kind = frame["kind"]
                if frame.get("id") in self.abandoned:
                    if kind in ("terminal", "rejected"):
                        self.abandoned.discard(frame["id"])
                        self.coverage.abandoned += 1
                    continue
                if kind == "rejected":
                    state.finished = True
                    body = frame.get("error") if isinstance(frame.get("error"), dict) else {}
                    raise EngineRejected(
                        str(body.get("message", "the engine rejected the request")),
                        body=body or None,
                    )
                if frame.get("id") != state.id:
                    raise self._broken(EngineProtocolError("a frame for another request arrived"))
                if kind == "batch":
                    yield "batch", self._batch(frame.get("batch"), state)
                elif kind == "terminal":
                    state.finished = True
                    yield "terminal", self._terminal(frame.get("terminal"), state)
                    return
                else:
                    raise self._broken(EngineProtocolError(f"a {kind!r} frame inside a statement"))
        finally:
            if not state.finished:
                self.abandoned.add(state.id)

    def _skip_abandoned(self) -> None:
        while self.abandoned:
            frame = self._frame()
            if frame.get("id") in self.abandoned:
                if frame["kind"] in ("terminal", "rejected"):
                    self.abandoned.discard(frame["id"])
                    self.coverage.abandoned += 1
                continue
            raise self._broken(EngineProtocolError("a frame for no known request arrived"))

    def _batch(self, document: Any, state: Statement) -> dict[str, Any]:
        try:
            ok = (
                document["schema"] == BATCH_SCHEMA
                and int(document["sequence"]) == state.next_sequence
                and int(document["first_row"]) == state.rows
                and int(document["row_count"]) == len(document["rows"])
                and isinstance(document["columns"], list)
                and all(isinstance(row, list) and len(row) == len(document["columns"]) for row in document["rows"])
            )
        except (KeyError, TypeError, ValueError):
            ok = False
        if not ok:
            raise self._broken(EngineProtocolError("a batch that is out of order, mislabelled or ragged"))
        state.next_sequence += 1
        state.rows += len(document["rows"])
        return document

    def _terminal(self, terminal: Any, state: Statement) -> dict[str, Any]:
        if not isinstance(terminal, dict) or terminal.get("operation_status") not in OPERATION_STATES:
            raise self._broken(EngineProtocolError("a terminal that does not state its operation status"))
        self.last_terminal = terminal
        coverage = terminal.get("coverage") if isinstance(terminal.get("coverage"), dict) else {}
        response = terminal.get("response") if isinstance(terminal.get("response"), dict) else {}
        execution = terminal.get("execution") if isinstance(terminal.get("execution"), dict) else {}
        self.coverage.add(coverage)
        if terminal["operation_status"] != "ok":
            error = terminal.get("error") if isinstance(terminal.get("error"), dict) else {}
            code = error.get("code")
            cls = EngineIncomplete if code in INCOMPLETE_CODES else EngineRejected
            raise cls(
                str(error.get("message", "the statement failed")),
                body=error or None,
                detail={"coverage": coverage, "emitted_rows": response.get("emitted_rows")},
            )
        try:
            emitted = int(response["emitted_rows"])
        except (KeyError, TypeError, ValueError):
            raise self._broken(EngineProtocolError("a terminal without a row count")) from None
        if emitted != state.rows:
            raise self._broken(EngineProtocolError("the terminal row count differs from the rows delivered"))
        complete = _completeness(
            "ok",
            coverage.get("input"),
            coverage.get("facts"),
            execution.get("complete"),
        )
        if response.get("truncated") is not False or response.get("more_available") is not False:
            raise EngineIncomplete(
                "the statement was cut short; its result is not complete",
                detail={"coverage": coverage, "response": response},
            )
        if not complete["complete"]:
            raise EngineIncomplete(
                "the statement's coverage is not complete: " + ",".join(complete["reasons"]),
                detail={"coverage": coverage, "reasons": complete["reasons"]},
            )
        return terminal

    def kill(self) -> None:
        process = self.process
        if process is not None and process.poll() is None:
            process_control.terminate_tree(process)

    def close(self, clean: bool) -> None:
        process = self.process
        problem: EngineError | None = None
        self.closed.set()
        try:
            if process is None:
                return
            if clean and process.poll() is None:
                try:
                    process.stdin.write(b'{"op":"close"}\n')
                    process.stdin.flush()
                    process.stdin.close()
                except (BrokenPipeError, OSError, ValueError):
                    pass
                try:
                    process.wait(timeout=self.CLOSE_WAIT)
                except subprocess.TimeoutExpired:
                    self.kill()
                    problem = EngineLost("native audit CLI did not exit after close")
            elif process.poll() is None:
                self.kill()
            if clean and problem is None and process.poll() is not None and process.returncode:
                problem = EngineLost(f"native audit CLI exited unsuccessfully ({process.returncode})")
        finally:
            if process is not None:
                if process.poll() is None:
                    self.kill()
                for stream in (process.stdin, process.stdout, process.stderr):
                    if stream is not None:
                        try:
                            stream.close()
                        except (BrokenPipeError, OSError, ValueError):
                            pass
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pass
            for thread in (self.reader, self.stderr_reader):
                if thread is not None:
                    thread.join(timeout=3)
        if problem is not None:
            raise problem


class B1Session:
    """Drop-in HostLab `NativeSession` over MeguvizDexDash B1 typed batches."""

    wire = "b1"
    transport_name = "typed_batch_v1"

    def __init__(self, apk: str | os.PathLike[str], timeout: float = 900, threads: int = 2) -> None:
        self.apk = Path(apk).resolve(strict=True)
        self.timeout = timeout
        self.threads = threads
        self.deadline = time.monotonic() + timeout
        self.queries = 0
        self.files: dict[int, str] = {}
        self.opened: dict[str, Any] = {}
        self.statements: list[str] = []
        self.transport: Transport | None = None
        self.last_columns: tuple[str, ...] | None = None

    def __enter__(self) -> B1Session:
        started = time.monotonic()
        binary = install_meguvizdexdash.verify()
        expected = batch.archive_inventory(self.apk)
        command = serve_command(binary, self.apk, timeout_seconds=self.timeout)
        env = child_environment(self.apk, self.threads)
        self.transport = Transport(command, env, self.deadline)
        try:
            opened = self.transport.start()
            self.files = {
                int(r["file_id"]): r["entry_name"]
                for r in self.rows("SELECT file_id,entry_name FROM dex_files ORDER BY file_id")
            }
            batch.verify_inventory(expected, self.files)
            self.opened = {
                "backend": "meguvizdexdash",
                "transport": self.transport_name,
                "wire": self.wire,
                "prepare_ms": (time.monotonic() - started) * 1000,
                "files": self.files,
                "cache": "memory_session",
                "source_diagnostics": [_issue_summary(i) for i in opened.layer_issues],
                "dataset": opened.describe(),
                "layers": opened.layers,
            }
            return self
        except BaseException:
            self.__exit__(RuntimeError, None, None)
            raise

    def __exit__(self, error: Any, *_: Any) -> None:
        if self.transport is not None:
            self.transport.close(clean=error is None and self.transport.broken is None)

    @property
    def coverage(self) -> dict[str, Any]:
        if self.transport is None:
            return {"statements": 0, "abandoned": 0, "input": "unknown", "facts": "unknown", "required_layers": [], "issues": []}
        described = self.transport.coverage.describe()
        described["abandoned"] += len(self.transport.abandoned)
        return described

    @property
    def layer_issues(self) -> list[Any]:
        if self.transport is None or self.transport.opened is None:
            return []
        return list(self.transport.opened.layer_issues)

    @staticmethod
    def _need_stable_order(sql: str) -> None:
        if "ORDER BY" not in sql.upper():
            raise ValueError("native audit requires stable ordering")

    @staticmethod
    def _need_unambiguous(columns: list[str]) -> None:
        if not columns or len(columns) != len(set(columns)):
            raise EngineProtocolError("ambiguous native audit columns", code="INVALID_ARGUMENT")

    @staticmethod
    def _decode_dto_cell(cell: Any) -> str | None:
        try:
            tag = cell["t"]
            if tag == "null":
                return None
            if tag == "text":
                if "units" in cell:
                    raw = bytes.fromhex(cell["units"])
                    text = raw.decode("utf-16-be", "surrogatepass")
                    try:
                        text.encode("utf-8")
                    except UnicodeEncodeError:
                        raise EngineProtocolError("a text cell holds an unpaired surrogate; it is not valid Unicode text") from None
                    return text
                text = cell["v"]
                if not isinstance(text, str):
                    raise TypeError
                return text
            if tag in ("i64", "u64"):
                v = cell["v"]
                if type(v) is str and (
                    (v.isascii() and v.isdigit() and (len(v) == 1 or v[0] != "0"))
                    or (v.startswith("-") and len(v) >= 2 and v[1] != "0" and v[1:].isascii() and v[1:].isdigit())
                ):
                    return v
                return str(int(v))
            if tag == "dex_mutf8":
                text = DexMutf8(bytes.fromhex(cell["v"]), int(cell["utf16_units"])).text()
                try:
                    text.encode("utf-8")
                except UnicodeEncodeError:
                    raise EngineProtocolError("a text cell holds an unpaired surrogate; it is not valid Unicode text") from None
                return text
            if tag == "bool":
                _ = bool(cell["v"])
                raise EngineProtocolError("a bool cell cannot be represented in the audit DTO")
            if tag == "f64":
                _ = struct.unpack(">d", bytes.fromhex(cell["bits"]))[0]
                raise EngineProtocolError("a float cell cannot be represented in the audit DTO")
            if tag == "bytes":
                _ = bytes.fromhex(cell["v"])
                raise EngineProtocolError("a bytes cell cannot be represented in the audit DTO")
        except EngineProtocolError:
            raise
        except (KeyError, TypeError, ValueError, struct.error):
            raise EngineProtocolError("a cell that does not decode") from None
        raise EngineProtocolError(f"an unknown cell tag {tag!r}")

    def _decode_direct_batches(
        self,
        sql: str,
        *,
        max_rows: int = 500_000,
        max_bytes: int = 128 * 1024 * 1024,
    ) -> Iterator[list[dict[str, Any]]]:
        if self.transport is None:
            raise SessionClosed("the session is not open")
        decode_dto = self._decode_dto_cell
        col_tuple: tuple[str, ...] | None = None
        last_cols: tuple[str, ...] | None = None
        names: list[str] | None = None
        ncols = 0
        c0 = c1 = c2 = c3 = c4 = ""
        used, count = 0, 0
        for kind, payload in self.transport.statement(sql, batch_rows=DEFAULT_BATCH_ROWS):
            if kind == "batch":
                cur_tuple = tuple(payload["columns"])
                if col_tuple is None:
                    col_tuple = cur_tuple
                    names = list(col_tuple)
                    self._need_unambiguous(names)
                    ncols = len(names)
                    if ncols >= 1:
                        c0 = names[0]
                    if ncols >= 2:
                        c1 = names[1]
                    if ncols >= 3:
                        c2 = names[2]
                    if ncols >= 4:
                        c3 = names[3]
                    if ncols >= 5:
                        c4 = names[4]
                elif cur_tuple != col_tuple:
                    raise EngineProtocolError("the columns changed between batches")
                batch_out: list[dict[str, Any]] = []
                batch_append = batch_out.append
                for raw_row in payload["rows"]:
                    count += 1
                    if count > max_rows:
                        raise EngineProtocolError("native audit exceeded its complete row budget", code="QUOTA_EXCEEDED")
                    if len(raw_row) != ncols:
                        raise EngineProtocolError("a batch row width differs from its columns")
                    vals: list[Any] = []
                    v_append = vals.append
                    for cell in raw_row:
                        if type(cell) is dict:
                            tag = cell.get("t")
                            if tag == "u64":
                                v = cell.get("v")
                                if type(v) is str and v.isascii() and v.isdigit() and (len(v) == 1 or v[0] != "0"):
                                    used += len(v)
                                    v_append(v)
                                    continue
                            elif tag == "text" and "units" not in cell:
                                v = cell.get("v")
                                if type(v) is str:
                                    used += len(v) if v.isascii() else len(v.encode())
                                    v_append(v)
                                    continue
                            elif tag == "null":
                                v_append(None)
                                continue
                        val = decode_dto(cell)
                        if val is not None:
                            used += len(val) if val.isascii() else len(val.encode())
                        v_append(val)
                    if used > max_bytes:
                        raise EngineProtocolError("native audit exceeded its complete byte budget", code="QUOTA_EXCEEDED")
                    if ncols == 2:
                        batch_append({c0: vals[0], c1: vals[1]})
                    elif ncols == 1:
                        batch_append({c0: vals[0]})
                    elif ncols == 3:
                        batch_append({c0: vals[0], c1: vals[1], c2: vals[2]})
                    elif ncols == 5:
                        batch_append({c0: vals[0], c1: vals[1], c2: vals[2], c3: vals[3], c4: vals[4]})
                    elif ncols == 4:
                        batch_append({c0: vals[0], c1: vals[1], c2: vals[2], c3: vals[3]})
                    else:
                        batch_append(dict(zip(names, vals)))
                if batch_out:
                    yield batch_out
            else:
                final = (payload.get("data") or {}).get("columns")
                if col_tuple is not None and final is not None and tuple(final) != col_tuple:
                    raise EngineProtocolError("the terminal names other columns than the batches")
                last_cols = tuple(final) if final is not None else col_tuple
                self.last_columns = last_cols
        if names is None:
            self._need_unambiguous(list(last_cols or ()))
        self.queries += 1

    def rows(
        self,
        sql: str,
        *,
        page_size: int = 1000,
        max_rows: int = 500_000,
        max_bytes: int = 128 * 1024 * 1024,
    ) -> Iterator[dict[str, Any]]:
        _ = page_size
        self._need_stable_order(sql)
        self.statements.append(sql)
        for batch_rows in self._decode_direct_batches(sql, max_rows=max_rows, max_bytes=max_bytes):
            yield from batch_rows

    def all(self, sql: str, **bounds: Any) -> list[dict[str, Any]]:
        return list(self.rows(sql, **bounds))
