"""Offline audit of the new home frame (khome) tab data structures across host APKs.

Verifies, per APK, the assumptions the runtime locator relies on:
  1. serializer serialName strings `tv.danmaku.bili.khomeapi.frame.HomeTabData` /
     `...HomeTabItemData` exist and belong to a `$serializer`-like nested class;
  2. element names (addElement order) of both descriptors;
  3. element i -> field mapping proven from the deserialization constructor's iput
     sources (register-level), compared with the dex declared instance field order;
  4. HomeFrameViewModel field Signature annotations reach HomeTabData within 2 hops;
  5. kotlinx SerialDescriptor accessor names are present (not obfuscated).
Usage: python home_frame_audit.py <apk>...
"""
import struct, sys, zipfile, os

TAB_DATA = "tv.danmaku.bili.khomeapi.frame.HomeTabData"
TAB_ITEM = "tv.danmaku.bili.khomeapi.frame.HomeTabItemData"
VM = "Ltv/danmaku/bili/khome/vm/HomeFrameViewModel;"


def uleb(d, o):
    r = s = 0
    while True:
        b = d[o]; o += 1
        r |= (b & 0x7f) << s
        if not b & 0x80:
            return r, o
        s += 7


WIDTH = [1] * 256
def _set(rng, w):
    for i in rng:
        WIDTH[i] = w
_set([0x02, 0x05, 0x08], 2); _set([0x03, 0x06, 0x09], 3)
_set([0x13, 0x15, 0x16, 0x19, 0x1a, 0x1c, 0x1f, 0x20, 0x22, 0x23, 0x29], 2)
_set([0x14, 0x17, 0x1b, 0x24, 0x25, 0x26, 0x2a, 0x2b, 0x2c], 3); WIDTH[0x18] = 5
_set(range(0x2d, 0x3e), 2); _set(range(0x44, 0x6e), 2); _set(range(0x6e, 0x73), 3)
_set(range(0x74, 0x79), 3); _set(range(0x90, 0xb0), 2); _set(range(0xd0, 0xe3), 2)
_set([0xfa, 0xfb], 4); _set([0xfc, 0xfd], 3); _set([0xfe, 0xff], 2)


class Dex:
    def __init__(self, data):
        self.d = d = data
        (self.sids_n, self.sids, self.tids_n, self.tids, self.pids_n, self.pids,
         self.fids_n, self.fids, self.mids_n, self.mids, self.cdefs_n, self.cdefs) = struct.unpack_from('<12I', d, 56)
        self._s = {}
        self._str_index = None

    def s(self, i):
        if i not in self._s:
            o = struct.unpack_from('<I', self.d, self.sids + i * 4)[0]
            _, o = uleb(self.d, o)
            self._s[i] = self.d[o:self.d.index(b'\0', o)].decode('utf-8', 'replace')
        return self._s[i]

    def find_string(self, text):
        lo, hi = 0, self.sids_n - 1
        while lo <= hi:  # string ids are sorted (MUTF-8 order == code point order for ASCII)
            mid = (lo + hi) // 2
            v = self.s(mid)
            if v == text: return mid
            if v < text: lo = mid + 1
            else: hi = mid - 1
        return None

    def t(self, i):
        return self.s(struct.unpack_from('<I', self.d, self.tids + i * 4)[0])

    def field(self, i):
        c, ty, n = struct.unpack_from('<HHI', self.d, self.fids + i * 8)
        return self.t(c), self.s(n), self.t(ty)

    def proto_params(self, i):
        _, _, po = struct.unpack_from('<3I', self.d, self.pids + i * 12)
        if not po: return []
        n = struct.unpack_from('<I', self.d, po)[0]
        return [self.t(struct.unpack_from('<H', self.d, po + 4 + k * 2)[0]) for k in range(n)]

    def method(self, i):
        c, p, n = struct.unpack_from('<HHI', self.d, self.mids + i * 8)
        return self.t(c), self.s(n), self.proto_params(p)

    def classes(self):
        for k in range(self.cdefs_n):
            yield struct.unpack_from('<8I', self.d, self.cdefs + k * 32)

    def class_data(self, off):
        d = self.d
        sf, o = uleb(d, off); inf, o = uleb(d, o); dm, o = uleb(d, o); vm, o = uleb(d, o)
        fields = []; idx = 0
        for k in range(sf + inf):
            if k == sf: idx = 0
            diff, o = uleb(d, o); acc, o = uleb(d, o); idx += diff
            fields.append((idx, acc, k < sf))
        methods = []; idx = 0
        for k in range(dm + vm):
            if k == dm: idx = 0
            diff, o = uleb(d, o); acc, o = uleb(d, o); code, o = uleb(d, o); idx += diff
            methods.append((idx, acc, code))
        return fields, methods

    def insns(self, code_off):
        regs, ins, outs, tries, dbg, n = struct.unpack_from('<HHHHII', self.d, code_off)
        base = code_off + 16; pc = 0
        while pc < n:
            u = struct.unpack_from('<H', self.d, base + pc * 2)[0]
            op = u & 0xff
            if op == 0 and u == 0x0100:
                size = struct.unpack_from('<H', self.d, base + pc * 2 + 2)[0]; w = size * 2 + 4
            elif op == 0 and u == 0x0200:
                size = struct.unpack_from('<H', self.d, base + pc * 2 + 2)[0]; w = size * 4 + 2
            elif op == 0 and u == 0x0300:
                ew = struct.unpack_from('<H', self.d, base + pc * 2 + 2)[0]
                size = struct.unpack_from('<I', self.d, base + pc * 2 + 4)[0]; w = (size * ew + 1) // 2 + 4
            else:
                w = WIDTH[op]
            yield pc, op, base + pc * 2
            pc += w
        return

    def code_header(self, code_off):
        return struct.unpack_from('<HH', self.d, code_off)

    def field_signatures(self, ann_off):
        """field_idx -> joined Signature annotation string."""
        out = {}
        if not ann_off: return out
        d = self.d
        _, fsz, _, _ = struct.unpack_from('<4I', d, ann_off)
        for k in range(fsz):
            fidx, aoff = struct.unpack_from('<II', d, ann_off + 16 + k * 8)
            n = struct.unpack_from('<I', d, aoff)[0]
            for j in range(n):
                item = struct.unpack_from('<I', d, aoff + 4 + j * 4)[0]
                o = item + 1
                tidx, o = uleb(d, o)
                if self.t(tidx) != 'Ldalvik/annotation/Signature;': continue
                cnt, o = uleb(d, o)
                for _ in range(cnt):
                    _, o = uleb(d, o)
                    vt = d[o]; o += 1
                    if vt & 0x1f != 0x1c: break
                    size, o = uleb(d, o); parts = []
                    for _ in range(size):
                        b = d[o]; o += 1; arg = b >> 5
                        v = int.from_bytes(d[o:o + arg + 1], 'little'); o += arg + 1
                        parts.append(self.s(v))
                    out[fidx] = ''.join(parts)
        return out


def load(apk):
    with zipfile.ZipFile(apk) as z:
        return [Dex(z.read(n)) for n in sorted(z.namelist()) if n.startswith('classes') and n.endswith('.dex')]


def find_defs(dexes):
    defs = {}
    for dx in dexes:
        for cd in dx.classes():
            defs[dx.t(cd[0])] = (dx, cd)
    return defs


def serializer_info(dexes, defs, serial):
    """Find the class whose <clinit> const-strings `serial`; return owner + element names."""
    for dx in dexes:
        sidx = dx.find_string(serial)
        if sidx is None: continue
        for cd in dx.classes():
            if not cd[6]: continue
            _, methods = dx.class_data(cd[6])
            for midx, acc, code in methods:
                if not code: continue
                strings = []; hit = False
                for pc, op, at in dx.insns(code):
                    if op == 0x1a: v = struct.unpack_from('<H', dx.d, at + 2)[0]
                    elif op == 0x1b: v = struct.unpack_from('<I', dx.d, at + 2)[0]
                    else: continue
                    if v == sidx: hit = True
                    elif hit: strings.append(dx.s(v))
                if hit:
                    ser = dx.t(cd[0])
                    owner = ser[:ser.rindex('$')] + ';' if '$' in ser else None
                    return ser, owner, strings
    return None, None, []


def fields_and_ctors(defs, cls):
    dx, cd = defs[cls]
    fields, methods = dx.class_data(cd[6])
    inst = [(dx.field(i)[1], dx.field(i)[2]) for i, acc, st in fields if not st]
    ctors = []
    for midx, acc, code in methods:
        c, n, params = dx.method(midx)
        if n == '<init>': ctors.append((params, code))
    return dx, inst, ctors


def iput_mapping(dx, cls, params, code):
    """Return list: element index (param index after leading int) -> field name via iput source regs."""
    regs, ins = dx.code_header(code)
    first = regs - ins + 1  # skip `this`
    reg_of = []; r = first
    for p in params:
        reg_of.append(r); r += 2 if p in ('J', 'D') else 1
    src_to_param = {reg: k for k, reg in enumerate(reg_of)}
    alias = {}
    mapping = {}
    for pc, op, at in dx.insns(code):
        u = struct.unpack_from('<H', dx.d, at)[0]
        if op == 0x07 or op == 0x01 or op == 0x04:  # move-object/move/move-wide vA, vB
            a = (u >> 8) & 0xf; b = (u >> 12) & 0xf
            alias[a] = alias.get(b, b)
        elif op in (0x08, 0x02, 0x05):
            a = (u >> 8) & 0xff; b = struct.unpack_from('<H', dx.d, at + 2)[0]
            alias[a] = alias.get(b, b)
        elif 0x59 <= op <= 0x5f:
            a = (u >> 8) & 0xf; fidx = struct.unpack_from('<H', dx.d, at + 2)[0]
            fc, fn, ft = dx.field(fidx)
            src = alias.get(a, a)
            if fc == cls and src in src_to_param and src_to_param[src] not in mapping:
                mapping[src_to_param[src]] = fn
    return mapping


def audit(apk):
    dexes = load(apk); defs = find_defs(dexes)
    out = {"apk": os.path.basename(apk)}
    for label, serial in (("data", TAB_DATA), ("item", TAB_ITEM)):
        ser, owner, names = serializer_info(dexes, defs, serial)
        out[label + ".owner"] = owner
        out[label + ".elements"] = names
        if not owner or owner not in defs:
            continue
        dx, inst, ctors = fields_and_ctors(defs, owner)
        out[label + ".fields"] = [f"{n}:{t}" for n, t in inst]
        n = len(names)
        out[label + ".ctors"] = [" ".join(p) for p, _ in ctors]
        types = [t for _, t in inst]
        deser = [(p, c) for p, c in ctors if len(p) >= n + 1 and p[0] == 'I' and p[1:n + 1] == types]
        verdict = "no-deser-ctor"
        if deser:
            p, c = deser[0]
            m = iput_mapping(dx, owner, p, c)
            bad = [i for i in range(n) if (i + 1) in m and m[i + 1] != inst[i][0]]
            missing = [i for i in range(n) if (i + 1) not in m]
            verdict = ("order-ok" if not bad else "ORDER-MISMATCH " + str(m)) +                 f" fields={len(inst)} elements={n} unproven={missing}"
        out[label + ".order"] = verdict
        # Companion factory: static field whose type declares a no-arg method returning KSerializer.
        dxo, cdo = defs[owner]
        sfields = [dxo.field(i) for i, acc, st in dxo.class_data(cdo[6])[0] if st]
        factory = []
        for _, fname, ftype in sfields:
            if ftype not in defs: continue
            d2, cd2 = defs[ftype]
            if not cd2[6]: continue
            for midx, acc, code in d2.class_data(cd2[6])[1]:
                c, mn, params = d2.method(midx)
                proto_ret = struct.unpack_from('<HHI', d2.d, d2.mids + midx * 8)[1]
                ret = d2.t(struct.unpack_from('<3I', d2.d, d2.pids + proto_ret * 12)[1])
                if not params and ret == 'Lkotlinx/serialization/KSerializer;' and not (acc & 0x8):
                    factory.append(f"{fname}:{ftype}#{mn}")
        out[label + ".companion"] = factory or "MISSING"
    # VM signature reachability
    reach = "vm-missing"
    if VM in defs:
        dx, cd = defs[VM]
        sigs = dx.field_signatures(cd[5])
        found = set()
        for s in sigs.values():
            for part in s.replace('<', ' ').replace('>', ' ').replace(';', '; ').split():
                if part.startswith('L') and part.endswith(';'): found.add(part)
        target = out.get("data.owner")
        hop1 = target in found
        hop2 = False
        for c in found:
            if c in defs and target:
                d2, cd2 = defs[c]
                if cd2[6]:
                    fl, _ = d2.class_data(cd2[6])
                    if any(d2.field(i)[2] == target for i, a, st in fl if not st): hop2 = True
        reach = f"sigs={len(sigs)} direct={hop1} via_state={hop2}"
    out["vm.reach"] = reach
    names = set()
    for dx in dexes:
        for k in range(dx.mids_n):
            c, n, _ = dx.method(k) if False else (None, None, None)
        break
    # kotlinx accessor names (string pool presence is enough: method names are pooled strings)
    for nm in ("getSerialName", "getElementName", "getElementsCount", "getDescriptor"):
        out["kx." + nm] = any(dx.find_string(nm) is not None for dx in dexes)
    for marker in ("Ltv/danmaku/bili/home/tab/page/HomeFragment;", "Ltv/danmaku/bili/home/tab/page/BaseHomeFragment;",
                   "Lcom/bilibili/bplus/followinglist/home/mediator/WideMediatorFragment;"):
        out["cls." + marker.split('/')[-1][:-1]] = marker in defs
    return out


if __name__ == '__main__':
    for apk in sys.argv[1:]:
        r = audit(apk)
        print("=" * 8, r.pop("apk"))
        for k, v in r.items():
            print(f"  {k}: {v}")
        sys.stdout.flush()
