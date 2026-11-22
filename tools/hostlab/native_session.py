"""Internal SQL literals and the owned MeguvizDexDash B1 session; external MCP stays compatible."""
from mdd_session import (
    B1Session as NativeSession,
    EngineError,
    EngineIncomplete,
    EngineLost,
    EngineProtocolError,
    EngineRejected,
    SessionClosed,
)

__all__ = [
    "EngineError",
    "EngineIncomplete",
    "EngineLost",
    "EngineProtocolError",
    "EngineRejected",
    "NativeSession",
    "SessionClosed",
    "in_list",
    "literal",
]


def literal(value):
    if any(c in value for c in "\r\n\0"):
        raise ValueError("audit SQL literal contains unsupported control characters")
    return "'" + value.replace("'", "''") + "'"


def in_list(values):
    return ",".join(literal(value) for value in values)
