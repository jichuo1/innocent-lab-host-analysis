"""Shared-fact gate execution (intake drift & home frame audit) reusing B1Session.

Replaces redundant pure-Python DEX full-archive parsing in `run_intake.py` and
`home_frame_audit.py` during native `meguvizdexdash` full audits while
producing identical verdicts, exit codes, and byte-for-byte `home-frame.log`.
"""
from __future__ import annotations

import contextlib
import hashlib
from pathlib import Path
import struct
import sys
import zipfile
from typing import Any

HERE = Path(__file__).resolve().parent
ANALYSIS_DIR = HERE / "analysis"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from analysis import home_frame_audit as _home_mod  # noqa: E402
from analysis import obfuscated_owner_drift as _drift_mod  # noqa: E402
from analysis import run_intake as _intake_mod  # noqa: E402
from mdd_session import EngineError  # noqa: E402
from native_session import in_list, literal  # noqa: E402

ALPHABET = tuple(_drift_mod.ALPHABET)
KX_ACCESSORS = ("getSerialName", "getElementName", "getElementsCount", "getDescriptor")
MARKERS = (
    "Ltv/danmaku/bili/home/tab/page/HomeFragment;",
    "Ltv/danmaku/bili/home/tab/page/BaseHomeFragment;",
    "Lcom/bilibili/bplus/followinglist/home/mediator/WideMediatorFragment;",
)
VIEW_BINDING_TYPE = "androidx.viewbinding.ViewBinding"
CREATE_METHOD_PARAMS = [
    "android.content.Context",
    "android.view.LayoutInflater",
    "android.view.ViewGroup",
]
CONTINUATION_TYPE = "kotlin.coroutines.Continuation"
KOTLINX_SERIALIZER_DESC = "Lkotlinx/serialization/KSerializer;"
SIGNATURE_ANN_DESC = "Ldalvik/annotation/Signature;"
MAX_ROWS = 1_000_000
MAX_BYTES = 256 * 1024 * 1024

_WIDTH = list(_home_mod.WIDTH)


class GateError(RuntimeError):
    """Raised when shared-fact gate verification fails or facts are incomplete."""


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _desc_to_java(desc: str) -> str:
    arr = 0
    cur = desc
    while cur.startswith("["):
        arr += 1
        cur = cur[1:]
    prim = {
        "V": "void",
        "Z": "boolean",
        "B": "byte",
        "S": "short",
        "C": "char",
        "I": "int",
        "J": "long",
        "F": "float",
        "D": "double",
    }
    if cur in prim:
        base = prim[cur]
    elif cur.startswith("L") and cur.endswith(";"):
        base = cur[1:-1].replace("/", ".")
    else:
        base = cur
    return base + ("[]" * arr)


def _java_to_desc(java_name: str) -> str:
    return "L" + java_name.replace(".", "/") + ";"


def _split_type_list(raw: str) -> list[str]:
    types: list[str] = []
    i = 0
    n = len(raw)
    while i < n:
        start = i
        while i < n and raw[i] == "[":
            i += 1
        if i >= n:
            raise GateError(f"malformed type descriptor list: {raw!r}")
        if raw[i] == "L":
            end = raw.find(";", i)
            if end < 0:
                raise GateError(f"unterminated class descriptor: {raw!r}")
            i = end + 1
        else:
            i += 1
        types.append(raw[start:i])
    return types


def _parse_method_descriptor(method_desc: str) -> tuple[list[str], str]:
    raw = method_desc
    if not raw.startswith("(") and "->" in raw:
        owner, member = raw.split("->", 1)
        if not owner or "(" not in member:
            raise GateError(f"malformed Dalvik method descriptor: {method_desc!r}")
        raw = member[member.index("(") :]
    if not raw.startswith("(") or ")" not in raw:
        raise GateError(f"malformed Dalvik method descriptor: {method_desc!r}")
    close = raw.index(")")
    ret = raw[close + 1 :]
    if not ret:
        raise GateError(f"malformed Dalvik method descriptor: {method_desc!r}")
    return _split_type_list(raw[1:close]), ret


def _extract_field_type_descriptor(field_desc: str) -> str:
    if "->" in field_desc:
        owner, member = field_desc.split("->", 1)
        if not owner or ":" not in member:
            raise GateError(f"malformed Dalvik field descriptor: {field_desc!r}")
        name, ftype = member.split(":", 1)
        if not name or not ftype:
            raise GateError(f"malformed Dalvik field descriptor: {field_desc!r}")
        return ftype
    if not field_desc:
        raise GateError(f"malformed Dalvik field descriptor: {field_desc!r}")
    return field_desc


def _covered(class_name: str, package: str) -> bool:
    if not class_name.startswith(package + "."):
        return False
    return class_name[len(package) + 1 :] in ALPHABET


def _query_checked(session: Any, sql: str) -> list[dict[str, Any]]:
    try:
        rows = session.all(sql, max_rows=MAX_ROWS, max_bytes=MAX_BYTES)
    except EngineError as exc:
        raise GateError(f"shared session query failed ({exc.code}): {exc}") from exc
    cov = session.coverage
    if cov.get("abandoned", 0) != 0:
        raise GateError("query abandoned without complete terminal")
    return rows


def _verify_session_completeness(session: Any, apk_path: Path, pre_sha: str) -> None:
    if _sha256_file(apk_path) != pre_sha:
        raise GateError("APK modified during gate reuse execution")
    cov = session.coverage
    if not isinstance(cov, dict) or cov.get("abandoned", 0) != 0:
        raise GateError("session contains abandoned/incomplete statements")
    for issue in session.layer_issues:
        if isinstance(issue, dict) and issue.get("blocking"):
            raise GateError(f"blocking coverage issue in snapshot: {issue}")
    if not isinstance(session.files, dict) or not session.files:
        raise GateError("verified snapshot contains no DEX files")


def _verify_required_layers(session: Any) -> None:
    probes = (
        "SELECT file_id,string_pool_id,entry_name FROM dex_files ORDER BY file_id LIMIT 1",
        "SELECT string_pool_id,string_idx FROM strings ORDER BY string_pool_id,string_idx LIMIT 1",
        "SELECT file_id,class_idx FROM classes ORDER BY file_id,class_idx LIMIT 1",
        "SELECT file_id,method_idx FROM code_items ORDER BY file_id,method_idx LIMIT 1",
        "SELECT file_id,annotation_off FROM annotations ORDER BY file_id,annotation_off LIMIT 1",
        "SELECT file_id,method_idx FROM method_strings ORDER BY file_id,method_idx LIMIT 1",
    )
    for sql in probes:
        _query_checked(session, sql)


def _decode_insns_slice(insns_bytes: bytes, insns_size_units: int) -> list[tuple[int, int, int]]:
    out: list[tuple[int, int, int]] = []
    pc = 0
    while pc < insns_size_units:
        at = pc * 2
        if at + 2 > len(insns_bytes):
            raise GateError("truncated Dalvik instruction slice in verified DEX")
        u = struct.unpack_from("<H", insns_bytes, at)[0]
        op = u & 0xFF
        if op == 0 and u == 0x0100:
            size = struct.unpack_from("<H", insns_bytes, at + 2)[0]
            w = size * 2 + 4
        elif op == 0 and u == 0x0200:
            size = struct.unpack_from("<H", insns_bytes, at + 2)[0]
            w = size * 4 + 2
        elif op == 0 and u == 0x0300:
            ew = struct.unpack_from("<H", insns_bytes, at + 2)[0]
            size = struct.unpack_from("<I", insns_bytes, at + 4)[0]
            w = (size * ew + 1) // 2 + 4
        else:
            w = _WIDTH[op]
        out.append((pc, op, at))
        pc += w
    return out


class ZipArchiveSliceReader:
    """Reads targeted `insns` slices on demand from verified DEX entries."""

    def __init__(self, apk_path: Path, files: dict[int, str], expected_sha256: str) -> None:
        self.apk_path = apk_path
        self.files = dict(files)
        self.expected_sha256 = expected_sha256
        self._dex_bytes: dict[int, bytes] = {}
        self._zip: zipfile.ZipFile | None = None
        if apk_path.suffix.lower() != ".dex" and zipfile.is_zipfile(apk_path):
            self._zip = zipfile.ZipFile(apk_path, "r")

    def read_insns(self, file_id: int, insns_off: int, insns_size_units: int) -> bytes:
        if file_id not in self._dex_bytes:
            if _sha256_file(self.apk_path) != self.expected_sha256:
                raise GateError("APK changed before reading code slice")
            if self._zip is None:
                self._dex_bytes[file_id] = self.apk_path.read_bytes()
            else:
                entry_name = self.files.get(file_id)
                if not entry_name:
                    raise GateError(f"missing file_id {file_id} in inventory")
                self._dex_bytes[file_id] = self._zip.read(entry_name)
        blob = self._dex_bytes[file_id]
        byte_len = insns_size_units * 2
        if insns_off < 0 or insns_off + byte_len > len(blob):
            raise GateError("code_items insns range exceeds verified member length")
        return blob[insns_off : insns_off + byte_len]

    def close(self) -> None:
        if self._zip is not None:
            self._zip.close()
            self._zip = None


def run_drift_from_session(session: Any) -> tuple[list[tuple[str, str]], list[tuple[str, str | None]], list[str]]:
    reply_desc = _java_to_desc(_drift_mod.REPLY_INFO)
    comment_desc = _java_to_desc(_drift_mod.COMMENT_ITEM)
    mapper_prefix_like = "%(" + reply_desc + "%)" + comment_desc
    mapper_rows = _query_checked(
        session,
        f"SELECT file_id, class_idx, class_descriptor, method_name, method_descriptor, access_flags "
        f"FROM class_methods WHERE method_descriptor LIKE {literal(mapper_prefix_like)} "
        f"ORDER BY file_id, class_idx, method_idx",
    )
    mappers: list[tuple[str, str]] = []
    for row in mapper_rows:
        flags = int(row["access_flags"])
        if not (flags & 0x8) or (flags & 0x1000) or (flags & 0x400):
            continue
        params_desc, ret_desc = _parse_method_descriptor(row["method_descriptor"])
        params_java = [_desc_to_java(p) for p in params_desc]
        ret_java = _desc_to_java(ret_desc)
        if ret_java == _drift_mod.COMMENT_ITEM and params_java and params_java[0] == _drift_mod.REPLY_INFO:
            mappers.append((_desc_to_java(row["class_descriptor"]), row["method_name"]))

    relate_prefix = "L" + _drift_mod.RELATE_GAME_PACKAGE.replace(".", "/") + "/%"
    relate_cls_rows = _query_checked(
        session,
        f"SELECT file_id, class_idx, descriptor, access_flags, superclass_descriptor "
        f"FROM classes WHERE descriptor LIKE {literal(relate_prefix)} ORDER BY file_id, class_idx",
    )
    relate_candidates = [
        row
        for row in relate_cls_rows
        if not (int(row["access_flags"]) & 0x400) and not (int(row["access_flags"]) & 0x200)
    ]
    relate_components: list[tuple[str, str | None]] = []
    if relate_candidates:
        descs = sorted({r["descriptor"] for r in relate_candidates})
        cm_rows = _query_checked(
            session,
            f"SELECT file_id, class_idx, class_descriptor, method_name, method_descriptor "
            f"FROM class_methods WHERE class_descriptor IN ({in_list(descs)}) "
            f"ORDER BY file_id, class_idx, method_idx",
        )
        by_key: dict[tuple[int, int], list[dict[str, Any]]] = {}
        for mrow in cm_rows:
            by_key.setdefault((int(mrow["file_id"]), int(mrow["class_idx"])), []).append(mrow)
        for crow in relate_candidates:
            creates = False
            binds = False
            for mrow in by_key.get((int(crow["file_id"]), int(crow["class_idx"])), []):
                p_desc, r_desc = _parse_method_descriptor(mrow["method_descriptor"])
                p_java = [_desc_to_java(p) for p in p_desc]
                r_java = _desc_to_java(r_desc)
                if r_java == VIEW_BINDING_TYPE and p_java == CREATE_METHOD_PARAMS:
                    creates = True
                if len(p_java) == 2 and p_java[0] == VIEW_BINDING_TYPE and p_java[1] == CONTINUATION_TYPE:
                    binds = True
            if creates and binds:
                sup = crow.get("superclass_descriptor")
                relate_components.append(
                    (_desc_to_java(crow["descriptor"]), _desc_to_java(sup) if sup else None)
                )

    gemini_prefix = "L" + _drift_mod.GEMINI_UI_PACKAGE.replace(".", "/") + "/%"
    gemini_cls_rows = _query_checked(
        session,
        f"SELECT file_id, class_idx, descriptor, access_flags "
        f"FROM classes WHERE descriptor LIKE {literal(gemini_prefix)} ORDER BY file_id, class_idx",
    )
    gemini_candidates = []
    for row in gemini_cls_rows:
        java_name = _desc_to_java(row["descriptor"])
        acc = int(row["access_flags"])
        if "$" in java_name or not (acc & 0x400) or (acc & 0x200):
            continue
        gemini_candidates.append(row)

    gemini_bases: list[str] = []
    if gemini_candidates:
        descs = sorted({r["descriptor"] for r in gemini_candidates})
        cm_rows = _query_checked(
            session,
            f"SELECT file_id, class_idx, class_descriptor, method_name, method_descriptor "
            f"FROM class_methods WHERE class_descriptor IN ({in_list(descs)}) "
            f"ORDER BY file_id, class_idx, method_idx",
        )
        by_key = {}
        for mrow in cm_rows:
            by_key.setdefault((int(mrow["file_id"]), int(mrow["class_idx"])), []).append(mrow)
        for crow in gemini_candidates:
            names: dict[str, list[str]] = {}
            for mrow in by_key.get((int(crow["file_id"]), int(crow["class_idx"])), []):
                p_desc, _ = _parse_method_descriptor(mrow["method_descriptor"])
                names[mrow["method_name"]] = [_desc_to_java(p) for p in p_desc]
            if len(names.get("createViewEntry", [])) == 2 and len(names.get("bindToView", [])) == 2:
                gemini_bases.append(_desc_to_java(crow["descriptor"]))

    return mappers, relate_components, gemini_bases


def _iput_mapping_from_slice(
    insns_bytes: bytes,
    insns_size_units: int,
    regs: int,
    ins: int,
    owner_desc: str,
    params_desc: list[str],
    field_lookup: dict[int, tuple[str, str]],
) -> dict[int, str]:
    first = regs - ins + 1
    reg_of: list[int] = []
    r = first
    for p in params_desc:
        reg_of.append(r)
        r += 2 if p in ("J", "D") else 1
    src_to_param = {reg: k for k, reg in enumerate(reg_of)}
    alias: dict[int, int] = {}
    mapping: dict[int, str] = {}
    for _pc, op, at in _decode_insns_slice(insns_bytes, insns_size_units):
        u = struct.unpack_from("<H", insns_bytes, at)[0]
        if op in (0x07, 0x01, 0x04):
            a = (u >> 8) & 0xF
            b = (u >> 12) & 0xF
            alias[a] = alias.get(b, b)
        elif op in (0x08, 0x02, 0x05):
            a = (u >> 8) & 0xFF
            b = struct.unpack_from("<H", insns_bytes, at + 2)[0]
            alias[a] = alias.get(b, b)
        elif 0x59 <= op <= 0x5F:
            a = (u >> 8) & 0xF
            fidx = struct.unpack_from("<H", insns_bytes, at + 2)[0]
            resolved = field_lookup.get(fidx)
            src = alias.get(a, a)
            if resolved is not None and resolved[0] == owner_desc and src in src_to_param and src_to_param[src] not in mapping:
                mapping[src_to_param[src]] = resolved[1]
    return mapping


def _serializer_info_from_session(
    session: Any,
    slice_reader: ZipArchiveSliceReader,
    serial: str,
    file_to_spid: dict[int, int],
) -> tuple[str | None, str | None, list[str]]:
    hits = _query_checked(
        session,
        f"SELECT DISTINCT ms.file_id, c.class_def_idx, ms.method_class, ms.method_idx "
        f"FROM method_strings ms "
        f"JOIN classes c ON c.file_id = ms.file_id AND c.descriptor = ms.method_class "
        f"WHERE ms.value = {literal(serial)} "
        f"ORDER BY ms.file_id, c.class_def_idx, ms.method_idx",
    )
    if not hits:
        return None, None, []

    hits = sorted(
        hits,
        key=lambda r: (
            session.files.get(int(r["file_id"]), ""),
            int(r["class_def_idx"]),
            int(r["method_idx"]),
        ),
    )
    first_hit = hits[0]
    fid = int(first_hit["file_id"])
    midx = int(first_hit["method_idx"])
    ser = str(first_hit["method_class"])
    spid = file_to_spid.get(fid, fid)

    serial_str_rows = _query_checked(
        session,
        f"SELECT string_idx, value FROM strings WHERE string_pool_id = {spid} AND value = {literal(serial)} ORDER BY string_idx",
    )
    if not serial_str_rows:
        return None, None, []
    serial_sidx = int(serial_str_rows[0]["string_idx"])

    ci_rows = _query_checked(
        session,
        f"SELECT insns_off, insns_size FROM code_items WHERE file_id = {fid} AND method_idx = {midx} ORDER BY method_idx",
    )
    if not ci_rows:
        return None, None, []
    insns_off = int(ci_rows[0]["insns_off"])
    insns_size = int(ci_rows[0]["insns_size"])
    insns_bytes = slice_reader.read_insns(fid, insns_off, insns_size)

    hit = False
    collected_sidxs: list[int] = []
    for _pc, op, at in _decode_insns_slice(insns_bytes, insns_size):
        if op == 0x1A:
            v = struct.unpack_from("<H", insns_bytes, at + 2)[0]
        elif op == 0x1B:
            v = struct.unpack_from("<I", insns_bytes, at + 2)[0]
        else:
            continue
        if v == serial_sidx:
            hit = True
        elif hit:
            collected_sidxs.append(v)

    if not hit:
        return None, None, []

    strings_out: list[str] = []
    if collected_sidxs:
        uniq_sidxs = sorted(set(collected_sidxs))
        s_in = ",".join(str(v) for v in uniq_sidxs)
        s_rows = _query_checked(
            session,
            f"SELECT string_idx, value FROM strings WHERE string_pool_id = {spid} AND string_idx IN ({s_in}) ORDER BY string_idx",
        )
        s_map = {int(r["string_idx"]): r["value"] for r in s_rows}
        strings_out = [s_map[idx] for idx in collected_sidxs]

    owner = (ser[: ser.rindex("$")] + ";") if "$" in ser else None
    return ser, owner, strings_out


def _extract_signature_field_targets(session: Any, fid: int, cidx: int, spid: int) -> tuple[int, set[str]]:
    sig_types = _query_checked(
        session,
        f"SELECT type_idx FROM types WHERE file_id = {fid} AND descriptor = {literal(SIGNATURE_ANN_DESC)} ORDER BY type_idx",
    )
    if not sig_types:
        return 0, set()
    sig_tidx = int(sig_types[0]["type_idx"])

    dir_rows = _query_checked(
        session,
        f"SELECT entry_idx, annotation_set_off FROM annotation_directory_entries "
        f"WHERE file_id = {fid} AND class_idx = {cidx} AND entry_kind = 'field' AND annotation_set_off IS NOT NULL "
        f"ORDER BY entry_idx",
    )
    if not dir_rows:
        return 0, set()

    set_offs = sorted({int(r["annotation_set_off"]) for r in dir_rows})
    set_entries = _query_checked(
        session,
        f"SELECT annotation_set_off, annotation_off, ordinal FROM annotation_set_entries "
        f"WHERE file_id = {fid} AND annotation_set_off IN ({','.join(map(str, set_offs))}) "
        f"ORDER BY annotation_set_off, ordinal",
    )
    if not set_entries:
        return 0, set()

    ann_offs = sorted({int(r["annotation_off"]) for r in set_entries})
    anns = _query_checked(
        session,
        f"SELECT annotation_off, type_idx FROM annotations "
        f"WHERE file_id = {fid} AND annotation_off IN ({','.join(map(str, ann_offs))}) AND type_idx = {sig_tidx} "
        f"ORDER BY annotation_off",
    )
    if not anns:
        return 0, set()

    sig_ann_offs = sorted({int(r["annotation_off"]) for r in anns})
    elems = _query_checked(
        session,
        f"SELECT annotation_off, depth, ordinal, value_kind, value_index FROM annotation_elements "
        f"WHERE file_id = {fid} AND annotation_off IN ({','.join(map(str, sig_ann_offs))}) "
        f"ORDER BY annotation_off, ordinal",
    )
    sidxs = sorted(
        {
            int(e["value_index"])
            for e in elems
            if int(e["depth"]) == 1 and e.get("value_kind") == "string" and e.get("value_index") is not None
        }
    )
    s_map: dict[int, str] = {}
    if sidxs:
        s_rows = _query_checked(
            session,
            f"SELECT string_idx, value FROM strings WHERE string_pool_id = {spid} AND string_idx IN ({','.join(map(str, sidxs))}) ORDER BY string_idx",
        )
        s_map = {int(r["string_idx"]): r["value"] for r in s_rows}

    by_ann: dict[int, list[str]] = {}
    for e in elems:
        if int(e["depth"]) == 1 and e.get("value_kind") == "string" and e.get("value_index") is not None:
            by_ann.setdefault(int(e["annotation_off"]), []).append(s_map[int(e["value_index"])])

    set_to_anns: dict[int, list[int]] = {}
    sig_ann_set = set(sig_ann_offs)
    for se in set_entries:
        aoff = int(se["annotation_off"])
        if aoff in sig_ann_set:
            set_to_anns.setdefault(int(se["annotation_set_off"]), []).append(aoff)

    field_sigs: dict[int, str] = {}
    for drow in dir_rows:
        fidx = int(drow["entry_idx"])
        soff = int(drow["annotation_set_off"])
        for aoff in set_to_anns.get(soff, []):
            parts = by_ann.get(aoff, [])
            if parts:
                field_sigs[fidx] = "".join(parts)

    found: set[str] = set()
    for sig in field_sigs.values():
        for part in sig.replace("<", " ").replace(">", " ").replace(";", "; ").split():
            if part.startswith("L") and part.endswith(";"):
                found.add(part)
    return len(field_sigs), found


def _pick_lex_last(session: Any, rows: list[dict[str, Any]]) -> dict[str, Any]:
    return max(rows, key=lambda r: (session.files.get(int(r["file_id"]), ""), int(r["file_id"])))


def run_home_frame_from_session(
    session: Any,
    slice_reader: ZipArchiveSliceReader,
    apk_path: Path,
) -> dict[str, Any]:
    dex_rows = _query_checked(session, "SELECT file_id, string_pool_id FROM dex_files ORDER BY file_id")
    file_to_spid = {int(r["file_id"]): int(r["string_pool_id"]) for r in dex_rows}

    out: dict[str, Any] = {"apk": apk_path.name}
    for label, serial in (("data", _home_mod.TAB_DATA), ("item", _home_mod.TAB_ITEM)):
        _ser, owner, names = _serializer_info_from_session(session, slice_reader, serial, file_to_spid)
        out[label + ".owner"] = owner
        out[label + ".elements"] = names
        if not owner:
            continue
        owner_rows = _query_checked(
            session,
            f"SELECT file_id, class_idx FROM classes WHERE descriptor = {literal(owner)} ORDER BY file_id, class_idx",
        )
        if not owner_rows:
            continue
        chosen_owner = _pick_lex_last(session, owner_rows)
        owner_fid = int(chosen_owner["file_id"])
        owner_cidx = int(chosen_owner["class_idx"])

        owner_fields = _query_checked(
            session,
            f"SELECT field_idx, class_descriptor, field_name, field_descriptor, kind "
            f"FROM class_fields WHERE file_id = {owner_fid} AND class_idx = {owner_cidx} ORDER BY field_idx",
        )
        inst = [
            (r["field_name"], _extract_field_type_descriptor(r["field_descriptor"]))
            for r in owner_fields
            if r["kind"] == "instance"
        ]
        sfields = [
            (r["field_name"], _extract_field_type_descriptor(r["field_descriptor"]))
            for r in owner_fields
            if r["kind"] == "static"
        ]
        field_lookup = {int(r["field_idx"]): (r["class_descriptor"], r["field_name"]) for r in owner_fields}
        out[label + ".fields"] = [f"{n}:{t}" for n, t in inst]

        ctor_rows = _query_checked(
            session,
            f"SELECT cm.method_idx, cm.method_descriptor AS descriptor, cm.kind AS method_kind, "
            f"ci.registers_size, ci.ins_size, ci.insns_off, ci.insns_size "
            f"FROM class_methods cm "
            f"LEFT JOIN code_items ci ON ci.file_id = cm.file_id AND ci.method_idx = cm.method_idx "
            f"WHERE cm.file_id = {owner_fid} AND cm.class_idx = {owner_cidx} AND cm.method_name = '<init>' "
            f"ORDER BY cm.kind, cm.method_idx",
        )
        ctors = []
        for crow in ctor_rows:
            params_desc, _ = _parse_method_descriptor(crow["descriptor"])
            ctors.append(
                (
                    params_desc,
                    int(crow["registers_size"]) if crow["registers_size"] is not None else None,
                    int(crow["ins_size"]) if crow["ins_size"] is not None else None,
                    int(crow["insns_off"]) if crow["insns_off"] is not None else None,
                    int(crow["insns_size"]) if crow["insns_size"] is not None else None,
                )
            )
        out[label + ".ctors"] = [" ".join(p) for p, *_ in ctors]

        n = len(names)
        types = [t for _, t in inst]
        deser = [c for c in ctors if len(c[0]) >= n + 1 and c[0][0] == "I" and c[0][1 : n + 1] == types]
        verdict = "no-deser-ctor"
        if deser:
            p, regs, ins, insns_off, insns_size = deser[0]
            if insns_off is None or insns_size is None or regs is None or ins is None:
                raise GateError(f"deserializer constructor of {owner} has missing code_item facts")
            insns_bytes = slice_reader.read_insns(owner_fid, insns_off, insns_size)
            m = _iput_mapping_from_slice(insns_bytes, insns_size, regs, ins, owner, p, field_lookup)
            bad = [i for i in range(n) if (i + 1) in m and m[i + 1] != inst[i][0]]
            missing = [i for i in range(n) if (i + 1) not in m]
            verdict = (
                ("order-ok" if not bad else "ORDER-MISMATCH " + str(m))
                + f" fields={len(inst)} elements={n} unproven={missing}"
            )
        out[label + ".order"] = verdict

        factory: list[str] = []
        static_ftypes = sorted({ftype for _, ftype in sfields})
        if static_ftypes:
            comp_cls_rows = _query_checked(
                session,
                f"SELECT file_id, class_idx, descriptor FROM classes WHERE descriptor IN ({in_list(static_ftypes)}) ORDER BY file_id, class_idx",
            )
            chosen_fids: dict[str, int] = {}
            by_desc: dict[str, list[dict[str, Any]]] = {}
            for cr in comp_cls_rows:
                by_desc.setdefault(cr["descriptor"], []).append(cr)
            for desc, cand in by_desc.items():
                chosen_fids[desc] = int(_pick_lex_last(session, cand)["file_id"])
            comp_rows = _query_checked(
                session,
                f"SELECT file_id, class_descriptor, method_name, method_descriptor, access_flags "
                f"FROM class_methods WHERE class_descriptor IN ({in_list(static_ftypes)}) "
                f"ORDER BY file_id, class_idx, kind, method_idx",
            )
            comp_by_type: dict[str, list[dict[str, Any]]] = {}
            for mr in comp_rows:
                cdesc = mr["class_descriptor"]
                if int(mr["file_id"]) == chosen_fids.get(cdesc):
                    comp_by_type.setdefault(cdesc, []).append(mr)
            for fname, ftype in sfields:
                for mr in comp_by_type.get(ftype, []):
                    if int(mr["access_flags"]) & 0x8:
                        continue
                    p_desc, r_desc = _parse_method_descriptor(mr["method_descriptor"])
                    if not p_desc and r_desc == KOTLINX_SERIALIZER_DESC:
                        factory.append(f"{fname}:{ftype}#{mr['method_name']}")
        out[label + ".companion"] = factory or "MISSING"

    reach = "vm-missing"
    vm_rows = _query_checked(
        session,
        f"SELECT file_id, class_idx FROM classes WHERE descriptor = {literal(_home_mod.VM)} ORDER BY file_id, class_idx",
    )
    if vm_rows:
        chosen_vm = _pick_lex_last(session, vm_rows)
        vm_fid = int(chosen_vm["file_id"])
        vm_cidx = int(chosen_vm["class_idx"])
        vm_spid = file_to_spid.get(vm_fid, vm_fid)
        sig_count, found_descs = _extract_signature_field_targets(session, vm_fid, vm_cidx, vm_spid)
        target_owner = out.get("data.owner")
        hop1 = bool(target_owner and target_owner in found_descs)
        hop2 = False
        if target_owner and found_descs:
            found_list = sorted(found_descs)
            hop2_cls_rows = _query_checked(
                session,
                f"SELECT file_id, descriptor FROM classes WHERE descriptor IN ({in_list(found_list)}) ORDER BY file_id, class_idx",
            )
            hop2_fids: dict[str, int] = {}
            hop2_by_desc: dict[str, list[dict[str, Any]]] = {}
            for cr in hop2_cls_rows:
                hop2_by_desc.setdefault(cr["descriptor"], []).append(cr)
            for desc, cand in hop2_by_desc.items():
                hop2_fids[desc] = int(_pick_lex_last(session, cand)["file_id"])
            hop2_rows = _query_checked(
                session,
                f"SELECT file_id, class_descriptor, field_descriptor FROM class_fields "
                f"WHERE class_descriptor IN ({in_list(found_list)}) AND kind = 'instance' "
                f"AND (field_descriptor = {literal(target_owner)} OR field_descriptor LIKE {literal('%:' + target_owner)}) "
                f"ORDER BY file_id, class_idx, field_idx",
            )
            hop2 = any(
                int(r["file_id"]) == hop2_fids.get(r["class_descriptor"])
                and _extract_field_type_descriptor(r["field_descriptor"]) == target_owner
                for r in hop2_rows
            )
        reach = f"sigs={sig_count} direct={hop1} via_state={hop2}"
    out["vm.reach"] = reach

    kx_rows = _query_checked(
        session,
        f"SELECT DISTINCT value FROM strings WHERE value IN ({in_list(KX_ACCESSORS)}) ORDER BY value",
    )
    kx_found = {r["value"] for r in kx_rows}
    for nm in KX_ACCESSORS:
        out["kx." + nm] = nm in kx_found

    m_rows = _query_checked(
        session,
        f"SELECT DISTINCT descriptor FROM classes WHERE descriptor IN ({in_list(MARKERS)}) ORDER BY descriptor",
    )
    marker_found = {r["descriptor"] for r in m_rows}
    for marker in MARKERS:
        out["cls." + marker.split("/")[-1][:-1]] = marker in marker_found

    return out


def render_home_frame_log(apk_path: Path, result: dict[str, Any]) -> str:
    lines = ["=" * 8 + " " + apk_path.name]
    for k, v in result.items():
        if k != "apk":
            lines.append(f"  {k}: {v}")
    return "\n".join(lines) + "\n"


def render_intake_log(
    apk_path: Path,
    tsv_path: Path,
    drift_tuple: tuple[list[tuple[str, str]], list[tuple[str, str | None]], list[str]],
    *,
    mode: str = "full",
) -> tuple[int, str]:
    import io

    mappers, relate, gemini = drift_tuple
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        info = _intake_mod.dump_identity(str(apk_path))
        _intake_mod.print_identity(info)
        print("== alphabet drift ==")
        owners = sorted({owner for owner, _ in mappers})
        mapper_ok = bool(owners) and all(_covered(owner, _drift_mod.MAPPER_PACKAGE) for owner in owners)
        relate_owners = sorted({owner for owner, _ in relate})
        relate_ok = len(relate_owners) == 1 and (
            _covered(relate_owners[0], _drift_mod.RELATE_GAME_PACKAGE)
            or relate_owners[0] == _drift_mod.RELATE_GAME_PACKAGE + ".RelateGameComponent"
        )
        gemini_ok = not gemini or any(_covered(name, _drift_mod.GEMINI_UI_PACKAGE) for name in gemini)
        gemini_letters = [name for name in gemini if _covered(name, _drift_mod.GEMINI_UI_PACKAGE)]
        print(f"    mapper owners      : {owners or '-'}  covered={mapper_ok}")
        print(f"    relate game owners : {relate_owners or '-'}  covered={relate_ok}")
        print(
            f"    gemini bases       : {gemini_letters or '-'}  covered="
            f"{'n/a' if not gemini else gemini_ok}"
        )
        if len(owners) > 1:
            print("    WARNING: mapper has multiple owners — treat as MISSING (fail-closed)")
        failures = 0 if (mapper_ok and relate_ok and gemini_ok) else 1
        if failures:
            print("    RESULT: outside bounded alphabet")
        else:
            print("    RESULT: alphabet still covers mapper / relate / gemini")
        _intake_mod.print_gaps()
        _intake_mod.print_version_hints()
        if mode == "full":
            problems = _intake_mod.print_feature_report(str(tsv_path), None)
            rc = 1 if failures or problems else 0
        else:
            rc = 1 if failures else 0
    return rc, buf.getvalue()


def run_gates(session: Any, apk_path: str | Path, *, expected_sha256: str) -> dict[str, Any]:
    """Compute reused drift and home-frame gate evidence on an already-open verified session."""
    apk = Path(apk_path).resolve(strict=True)
    _verify_session_completeness(session, apk, expected_sha256)
    _verify_required_layers(session)
    drift_tuple = run_drift_from_session(session)
    slice_reader = ZipArchiveSliceReader(apk, session.files, expected_sha256)
    try:
        home_dict = run_home_frame_from_session(session, slice_reader, apk)
    finally:
        slice_reader.close()
    _verify_session_completeness(session, apk, expected_sha256)
    return {
        "gate_mode": "mdd_fact_reuse",
        "drift": drift_tuple,
        "home": home_dict,
        "home_log": render_home_frame_log(apk, home_dict),
    }
