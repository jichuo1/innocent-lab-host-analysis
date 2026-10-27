"""Terminal failure classes for bounded remote retries. No I/O, no network, no time zone.

The runner is the only authority on why a job stopped. The words below travel in
job.json so a caller can tell a deterministic rejection (the same request cannot
succeed by paying for it again) from a stop that another attempt can still advance,
whether by resuming an admitted page cursor or by retrying unknown transport.
Nothing here reads artifacts, APKs, logs or the network.
"""

from __future__ import annotations

import re
import time

# Same request, same sample, same tooling => the same rejected statement.
DETERMINISTIC = frozenset({
    "invalid_query",        # backend rejected the SQL text or its dialect
    "invalid_input",        # backend rejected the task parameters
    "impl_defined",         # statement shape this engine refuses by design
    "output_too_large",     # the same projection exceeds the same transport budget
    "class_not_found",      # the requested class is absent from this APK
    "decompile_empty",      # the decompiler emits no source for this class
    "not_found",            # decode/reference target is absent from this sample
})
# Another attempt can still make progress: the checkpoint resumes a partial page
# cursors, unknown transport may heal, and exhausted capacity may come back.
PROGRESSABLE = frozenset({
    "page_budget",          # bounded pages per run; the cursor continues next time
    "row_budget",           # bounded rows per run; the cursor continues next time
    "byte_budget",          # bounded bytes per run; the cursor continues next time
    "resume_pending",       # a completed prefix was sealed, the rest still to fetch
    "native_page_budget_retry",
    "backend_request_failed",
    "page_request_failed",
    "analysis_deadline_or_session_failure",
    "backend_session_failed_or_deadline",
    "timeout",
    "disk_capacity",
    "runner_interrupted_before_member",
    "harness_failed",
})
REASON_TEXT = re.compile(r"[A-Za-z0-9_:.-]{1,100}")
# A deterministic rejection inside this window is not replayed without an explicit key.
REPLAY_WINDOW_SECONDS = 6 * 3600
MAX_REASONS = 8
# Exception type names recorded by the validation entry point, mapped to bounded kinds.
EXCEPTION_KINDS = {
    "ValueError": "invalid_input",
    "TypeError": "invalid_input",
    "TimeoutError": "timeout",
    "OSError": "harness_failed",
    "RuntimeError": "harness_failed",
}
_TEXT_LIMIT = 8192
_SQL_REJECTIONS = ("no such table", "no such column", "unknown column", "unknown relation",
                   "sql error", "syntax error", "no such function")
# Relations that exist only in the verified native index.
_NATIVE_RELATIONS = ("class_methods", "method_calls", "class_fields", "method_strings",
                     "method_field_accesses", "method_used_types", "dex_files")


def reason(value):
    """A bounded machine word, or None; free text never leaves the runner."""
    return value if isinstance(value, str) and REASON_TEXT.fullmatch(value) else None


def reasons(values, limit=MAX_REASONS):
    collected = []
    for value in values or ():
        word = reason(value)
        if word is not None and word not in collected:
            collected.append(word)
        if len(collected) == limit:
            break
    return collected


def classify(values):
    """'deterministic', 'progressable' or 'unknown' for one failed job's reasons."""
    words = reasons(values, limit=32)
    if not words:
        return "unknown"
    if any(word in PROGRESSABLE for word in words):
        return "progressable"
    if all(word in DETERMINISTIC for word in words):
        return "deterministic"
    return "unknown"


def command_failure(operation, rc, text, backend=None):
    """Bounded cause for a single-command job that returned non-zero exit status."""
    head = text[:_TEXT_LIMIT].lower() if isinstance(text, str) else ""
    if rc == 124:
        return {"kind": "timeout", "message": operation + " exceeded its bounded timeout"}
    if "classnotfoundexception" in head:
        return {"kind": "class_not_found", "message": "class is not present in this APK"}
    if "outofmemoryerror" in head:
        return {"kind": "harness_failed", "message": "decompiler or scanner ran out of heap"}
    if any(marker in head for marker in _SQL_REJECTIONS):
        failure = {"kind": "invalid_query", "message": "backend rejected the statement"}
        if backend != "dexsql" and any(relation in head for relation in _NATIVE_RELATIONS):
            failure["hint"] = "native table names require backend=dexsql"
        return failure
    if "rejected operation" in head:
        return {"kind": "invalid_input", "message": "backend rejected the operation"}
    if "not found" in head:
        return {"kind": "not_found", "message": "requested target is absent from this sample"}
    return {"kind": "command_failed",
            "message": operation + " exited " + str(rc) + " without a classified cause"}


def exception_kind(name):
    """Bounded kind for a recorded exception type name; unknown names stay a harness problem."""
    word = reason(name) if isinstance(name, str) else None
    return EXCEPTION_KINDS.get(word, "harness_failed")


def blocks_replay(receipt, *, now=None, window=REPLAY_WINDOW_SECONDS):
    """An identical payload already failed for a reason a replay cannot change."""
    if not isinstance(receipt, dict):
        return False
    if receipt.get("status") != "completed" or receipt.get("conclusion") != "failure":
        return False
    if receipt.get("retry_class") != "deterministic":
        return False
    created = receipt.get("created_at")
    if type(created) is not float and type(created) is not int:
        return False
    elapsed = (time.time() if now is None else now) - created
    return 0 <= elapsed <= window


def classification(jobs):
    """Receipt annotation derived from runner job.json values; None when nothing failed."""
    collected = []
    for job in jobs or ():
        if not isinstance(job, dict):
            continue
        for word in job.get("failure_reasons") or ():
            collected.append(word)
        failure = job.get("failure")
        if isinstance(failure, dict):
            collected.append(failure.get("kind"))
    words = reasons(collected, limit=MAX_REASONS)
    if not words:
        return None
    return {"retry_class": classify(words), "failure_reasons": words}
