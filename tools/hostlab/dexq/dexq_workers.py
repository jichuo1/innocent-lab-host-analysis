"""dexq 的多进程 worker：只依赖 androguard，绝不能 import mcp（spawn 会在每个子进程重新导入本模块）。

约定：
- worker 不许向 stdout 写任何东西（父进程的 stdout 就是 MCP 协议通道）。
- proto 一律去掉空格：androguard 的 get_descriptor() 会在参数间插空格，而 smali 签名没有。
"""
from __future__ import annotations

import os
import re
import sys
import zipfile


def init_worker() -> None:
    from loguru import logger

    logger.remove()  # androguard 默认 DEBUG 刷屏，既慢又污染 stderr
    sys.stdout = open(os.devnull, "w")


def norm_proto(proto: str) -> str:
    return proto.replace(" ", "")


def _clean(text: str) -> str:
    # dex 字符串可能含孤立代理项，直接进 sqlite 会 UnicodeEncodeError
    return text.encode("utf-8", "backslashreplace").decode("utf-8")


def load_dex(src: str, member: str | None):
    """返回 (原始字节长度, DEX)。member 为空表示 src 本身就是 .dex。"""
    from androguard.core.dex import DEX

    if member is None:
        with open(src, "rb") as fh:
            raw = fh.read()
    else:
        with zipfile.ZipFile(src) as zf:
            raw = zf.read(member)
    return len(raw), DEX(raw)


def extract(job):
    """把一个 dex 拆成可批量入库的行。job = (src, member, file_id)。"""
    src, member, file_id = job
    size, d = load_dex(src, member)
    strings = d.get_strings()
    method_ids = d.get_methods()
    field_ids = d.get_fields()
    classes = d.get_classes()

    def source_file(idx: int) -> str:
        return strings[idx] if isinstance(idx, int) and 0 <= idx < len(strings) else ""

    return {
        "dex": (file_id, src, member or "", size, len(classes), len(method_ids),
                len(field_ids), len(strings)),
        "classes": [
            (file_id, c.get_name(), c.get_access_flags_string(), c.get_superclassname(),
             ",".join(c.get_interfaces() or []), _clean(source_file(c.get_source_file_idx())))
            for c in classes
        ],
        "methods": [
            (file_id, e.get_method_idx(), e.get_class_name(), e.get_name(),
             norm_proto(e.get_descriptor()), e.get_access_flags_string(), e.get_length())
            for e in d.get_encoded_methods()
        ],
        "fields": [
            (file_id, g.get_class_name(), g.get_name(), g.get_descriptor(),
             g.get_access_flags_string())
            for g in d.get_encoded_fields()
        ],
        "method_ids": [
            (file_id, i, m.get_class_name(), m.get_name(), norm_proto(m.get_descriptor()))
            for i, m in enumerate(method_ids)
        ],
        "field_ids": [
            (file_id, i, x.get_class_name(), x.get_name(), x.get_type())
            for i, x in enumerate(field_ids)
        ],
        "strings": [(file_id, i, _clean(s)) for i, s in enumerate(strings)],
    }


_FIELD_OPS = ("iget", "iput", "sget", "sput")
_TYPE_OPS = {"const-class", "new-instance", "check-cast", "instance-of", "new-array",
             "filled-new-array", "filled-new-array/range"}
_PER_DEX_CAP = 5000


def scan_refs(job):
    """在一个 dex 里找引用。job = (src, member, file_id, kind, target)。

    kind:
      string  target=字符串原文            → const-string 使用点
      method  target=Lcls;->name(proto)ret → invoke-* 调用点
      field   target=Lcls;->name:type      → iget/iput/sget/sput 使用点
      type    target=Lcls;                 → const-class/new-instance/check-cast 等
    返回 (file_id, hits)；hits 元素 (class, name, proto, offset_units, op)。
    """
    src, member, file_id, kind, target = job
    _, d = load_dex(src, member)
    idxs: set[int] = set()
    if kind == "string":
        try:
            idxs.add(d.get_strings().index(target))
        except ValueError:
            return file_id, []
    elif kind == "method":
        m = re.fullmatch(r"(L[^;]+;)->([^(]+)(\(.*)", target)
        if not m:
            return file_id, []
        cls, name, proto = m.group(1), m.group(2), norm_proto(m.group(3))
        for i, x in enumerate(d.get_methods()):
            if (x.get_class_name() == cls and x.get_name() == name
                    and norm_proto(x.get_descriptor()) == proto):
                idxs.add(i)
    elif kind == "field":
        m = re.fullmatch(r"(L[^;]+;)->([^:]+):(.+)", target)
        if not m:
            return file_id, []
        for i, x in enumerate(d.get_fields()):
            if (x.get_class_name() == m.group(1) and x.get_name() == m.group(2)
                    and x.get_type() == m.group(3)):
                idxs.add(i)
    elif kind != "type":
        return file_id, []
    if kind != "type" and not idxs:
        return file_id, []

    hits = []
    for e in d.get_encoded_methods():
        code = e.get_code()
        if code is None:
            continue
        off = 0
        for ins in code.get_bc().get_instructions():
            nm = ins.get_name()
            hit = False
            if kind == "string":
                hit = nm in ("const-string", "const-string/jumbo") and ins.get_ref_kind() in idxs
            elif kind == "method":
                hit = nm.startswith("invoke") and ins.get_ref_kind() in idxs
            elif kind == "field":
                hit = nm[:4] in _FIELD_OPS and ins.get_ref_kind() in idxs
            elif nm in _TYPE_OPS:
                hit = d.get_cm_type(ins.get_ref_kind()) == target
            if hit:
                hits.append((e.get_class_name(), e.get_name(), norm_proto(e.get_descriptor()),
                             off // 2, nm))
                if len(hits) >= _PER_DEX_CAP:
                    return file_id, hits
            off += ins.get_length()
    return file_id, hits
