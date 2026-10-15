"""Public, bounded AI receipts. Private messages and evidence bodies never enter this file."""
from __future__ import annotations

import hashlib
import copy
import json
import math
import os
from pathlib import Path
import re
import stat
import time
import uuid

import remote_schedule

MAX_BYTES = 8 * 1024 * 1024
MAX_REQUESTS = 16
MAX_TRANSPORT_RETRIES = 2
COOLDOWN_SECONDS = 60
HEX = re.compile(r"[0-9a-f]{64}")


class CheckpointError(RuntimeError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def regular(path, *, missing=False):
    try:
        info = path.lstat()
    except FileNotFoundError:
        if missing:
            return
        raise CheckpointError("checkpoint file is missing") from None
    if (not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode)
            or getattr(info, "st_file_attributes", 0) & 0x400 or info.st_nlink != 1):
        raise CheckpointError("checkpoint must be a regular unlinked file")
    if info.st_size > MAX_BYTES:
        raise CheckpointError("checkpoint exceeds its byte budget")


def validate(value):
    if (not isinstance(value, dict) or value.get("schema") != 1 or type(value.get("schema")) is not int
            or not isinstance(value.get("binding"), dict) or not isinstance(value.get("attempts"), list)
            or len(value["attempts"]) > MAX_REQUESTS or not isinstance(value.get("units"), dict)
            or not isinstance(value.get("responses"), dict) or not isinstance(value.get("providers"), dict)
            or value.get("binding_sha256") != digest(value["binding"])):
        raise CheckpointError("invalid AI checkpoint schema or binding")
    if len(value["units"]) > 24 or len(value["responses"]) > MAX_REQUESTS:
        raise CheckpointError("AI checkpoint collection exceeds its budget")
    if (type(value.get("transport_retries")) is not int or not 0 <= value["transport_retries"] <= MAX_TRANSPORT_RETRIES
            or type(value.get("elapsed_seconds", 0)) not in {int, float}
            or not math.isfinite(value.get("elapsed_seconds", 0)) or value.get("elapsed_seconds", 0) < 0):
        raise CheckpointError("invalid checkpoint accounting")
    for unit, saved in value["units"].items():
        if (not re.fullmatch(r"[dr][0-9]{1,2}", unit) or not isinstance(saved, dict)
                or not isinstance(saved.get("result"), dict) or saved.get("result_sha256") != digest(saved["result"])):
            raise CheckpointError("checkpoint unit result digest changed")
    for request_hash, saved in value["responses"].items():
        if (not HEX.fullmatch(request_hash) or not isinstance(saved, dict) or not isinstance(saved.get("usage"), dict)
                or not isinstance(saved.get("model"), str) or len(saved["model"]) > 256):
            raise CheckpointError("invalid checkpoint response metadata")
        response = {key: saved[key] for key in ("clean", "usage", "model") if key in saved}
        if saved.get("response_sha256") != digest(response):
            raise CheckpointError("checkpoint response content digest changed")
        clean = saved.get("clean")
        if (not isinstance(clean, dict) or set(clean)-{"role", "content", "tool_calls"}
                or clean.get("role") != "assistant" or clean.get("content") is not None
                or not isinstance(clean.get("tool_calls", []), list) or len(clean.get("tool_calls", [])) > 8
                or len(json.dumps(clean, ensure_ascii=False).encode()) > 128*1024):
            raise CheckpointError("invalid public checkpoint response")
        for call in clean.get("tool_calls", []):
            function = call.get("function") if isinstance(call, dict) else None
            if (not isinstance(function, dict) or not isinstance(function.get("arguments"), str)
                    or not re.fullmatch(r"[a-z_]{1,48}", str(function.get("name", "")))
                    or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", str(call.get("id", "")))):
                raise CheckpointError("invalid checkpoint tool receipt")
    for attempt in value["attempts"]:
        if (not isinstance(attempt, dict) or not re.fullmatch(r"[0-9a-f]{32}", str(attempt.get("id", "")))
                or not HEX.fullmatch(str(attempt.get("request_sha256", "")))
                or attempt.get("profile") not in {"primary", "backup"}
                or attempt.get("status") not in {"attempt_unknown", "response_received", "failed", "authorized_replay"}
                or attempt.get("stage") not in {"draft", "review"}):
            raise CheckpointError("invalid AI checkpoint attempt")
    return value


def atomic(path, value):
    raw = json.dumps(value, ensure_ascii=False, indent=2).encode()
    if len(raw) > MAX_BYTES:
        raise CheckpointError("AI checkpoint exceeds its byte budget")
    regular(path, missing=True)
    stage = path.with_name(".ai-checkpoint-"+uuid.uuid4().hex+".tmp")
    try:
        with stage.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(stage, path)
    finally:
        stage.unlink(missing_ok=True)


def restore_checkpoint(root, verifiedfiles):
    """Copy one verified public ledger; the pipeline checks its complete binding later."""
    selected = [Path(name) for name in verifiedfiles if Path(name).name == "ai-checkpoint.json"]
    if len(selected) != 1:
        raise CheckpointError("missing or ambiguous AI checkpoint")
    source = selected[0]
    regular(source)
    raw = source.read_bytes()
    value = validate(json.loads(raw))
    root = Path(root); root.mkdir(parents=True, exist_ok=True)
    target = root / "ai-checkpoint.json"
    regular(target, missing=True)
    if target.exists() and target.read_bytes() != raw:
        raise CheckpointError("refusing to replace a different AI checkpoint")
    atomic(target, value)
    return {"restored": True, "sha256": hashlib.sha256(raw).hexdigest(),
            "attempts": len(value["attempts"]), "completed_units": len(value["units"])}


class Checkpoint:
    def __init__(self, root, binding, *, resume_unknown=False):
        if type(resume_unknown) is not bool:
            raise CheckpointError("resume_unknown must be boolean")
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "ai-checkpoint.json"
        self.resume_unknown = resume_unknown
        regular(self.root / "ai-checkpoint.lock", missing=True)
        self.lock = remote_schedule.admission_lock(self.root / "ai-checkpoint.lock")
        if self.lock is None:
            raise CheckpointError("AI checkpoint is already in use")
        try:
            regular(self.path, missing=True)
            if self.path.exists():
                self.value = validate(json.loads(self.path.read_text(encoding="utf-8")))
                if self.value["binding"] != binding:
                    raise CheckpointError("AI checkpoint input/source/prompt/provider binding changed")
            else:
                self.value = {"schema": 1, "binding": binding, "binding_sha256": digest(binding),
                    "attempts": [], "units": {}, "responses": {}, "providers": {},
                    "transport_retries": 0, "elapsed_seconds": 0.0, "created_at": time.time()}
                self.save()
            pending = [row for row in self.value["attempts"] if row["status"] == "attempt_unknown"]
            if pending and not resume_unknown:
                raise CheckpointError("AI request outcome is unknown; explicit resume_unknown authorization is required")
            if pending:
                # A killed caller may have spent its entire per-request deadline.
                # Never reset that active budget merely because finally did not run.
                allowance = self.value["binding"].get("policy", {}).get("total_timeout", 240)
                self.value["elapsed_seconds"] = self.value.get("elapsed_seconds", 0)+sum(
                    min(allowance, max(0.0, time.time()-row["started_at"])) for row in pending)
                for row in pending:
                    row.update(status="authorized_replay", billing_unknown=True, replay_authorized=True)
            self.elapsed_base = self.value.get("elapsed_seconds", 0.0)
            self.started_monotonic = time.monotonic()
            if pending:
                self.save()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.lock is not None:
            self.lock.close(); self.lock = None

    def save(self):
        if hasattr(self, "elapsed_base"):
            self.value["elapsed_seconds"] = max(self.value.get("elapsed_seconds", 0.0),
                self.elapsed_base+time.monotonic()-self.started_monotonic)
        validate(self.value)
        atomic(self.path, self.value)

    def cached(self, request_hash):
        return self.value["responses"].get(request_hash)

    def claim(self, stage, unit, request_hash, profile, session_id, *, transport_retry=False):
        if any(row["status"] == "attempt_unknown" for row in self.value["attempts"]):
            raise CheckpointError("an earlier AI request still has an unknown process outcome")
        if len(self.value["attempts"]) >= MAX_REQUESTS:
            raise CheckpointError("global model request budget exhausted")
        provider = self.value["providers"].get(profile, {})
        if provider.get("failures", 0) >= 2 and time.time() < provider.get("open_until", 0):
            raise CheckpointError("provider circuit is open")
        if transport_retry:
            if self.value["transport_retries"] >= MAX_TRANSPORT_RETRIES:
                raise CheckpointError("global transport compensation budget exhausted")
            self.value["transport_retries"] += 1
        row = {"id": uuid.uuid4().hex, "stage": stage, "unit": unit, "profile": profile,
            "request_sha256": request_hash, "session_id": session_id,
            "status": "attempt_unknown", "billing_unknown": True, "transport_retry": transport_retry,
            "started_at": time.time()}
        self.value["attempts"].append(row)
        self.save()  # Receipt always precedes the POST, even if the process dies immediately.
        return row["id"]

    def received(self, attempt_id, request_hash, clean, usage, model):
        if len(json.dumps(clean, ensure_ascii=False).encode()) > 128 * 1024:
            raise CheckpointError("public model response receipt exceeds its bound")
        row = next(row for row in self.value["attempts"] if row["id"] == attempt_id)
        unknown = bool(usage.get("_usage_unknown", not bool(usage)))
        row.update(status="response_received", billing_unknown=unknown, usage_unknown=unknown, usage=usage, model=model)
        response = {"clean": clean, "usage": usage, "model": model}
        self.value["responses"][request_hash] = {**response, "response_sha256": digest(response)}
        self.value["providers"][row["profile"]] = {"failures": 0, "open_until": 0}
        self.save()

    def failed(self, attempt_id, error):
        row = next(row for row in self.value["attempts"] if row["id"] == attempt_id)
        row.update(status="failed", reason=str(error.reason)[:160], kind=error.kind,
            retryable=bool(error.retryable), billing_unknown=bool(error.billing_unknown),
            http_status=error.http_status)
        delay = getattr(error, "retry_after", None)
        row["retry_after"] = delay if type(delay) in {int, float} and math.isfinite(delay) and delay >= 0 else None
        metrics = getattr(error, "metrics", {}) or {}
        row["metrics"] = {key: value for key, value in metrics.items()
            if key in {"total_ms", "headers_ms", "first_event_ms", "first_visible_delta_ms", "response_bytes",
                       "events", "request_bytes", "http_status"}
            and type(value) in {int, float}}
        provider = self.value["providers"].setdefault(row["profile"], {"failures": 0, "open_until": 0})
        provider["failures"] += 1
        if provider["failures"] >= 2:
            provider["open_until"] = time.time()+COOLDOWN_SECONDS
        self.save()

    def save_unit(self, unit, result):
        if unit in self.value["units"] and self.value["units"][unit]["result_sha256"] != digest(result):
            raise CheckpointError("accepted checkpoint unit changed during replay")
        self.value["units"][unit] = {"result_sha256": digest(result), "result": copy.deepcopy(result)}
        self.save()

    def record_elapsed(self, seconds):
        self.value["elapsed_seconds"] = max(self.value.get("elapsed_seconds", 0.0), self.elapsed_base+max(0.0, seconds))
        self.save()

    def reserve_wait(self, seconds):
        self.value["elapsed_seconds"] = max(self.value.get("elapsed_seconds", 0.0),
            self.elapsed_base+time.monotonic()-self.started_monotonic+seconds)
        self.save()
