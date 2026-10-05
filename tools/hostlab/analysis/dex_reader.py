import struct, sys, os, glob, json

ACC = {0x1:'public',0x2:'private',0x4:'protected',0x8:'static',0x10:'final',0x400:'abstract',0x1000:'synthetic',0x200:'interface'}

def uleb(data, off):
    result = 0; shift = 0
    while True:
        b = data[off]; off += 1
        result |= (b & 0x7f) << shift
        if not (b & 0x80): break
        shift += 7
    return result, off

def desc2java(d):
    arr = 0
    while d.startswith('['):
        arr += 1; d = d[1:]
    prim = {'V':'void','Z':'boolean','B':'byte','S':'short','C':'char','I':'int','J':'long','F':'float','D':'double'}
    if d in prim: base = prim[d]
    elif d.startswith('L'): base = d[1:-1].replace('/','.')
    else: base = d
    return base + '[]'*arr

class Dex:
    def __init__(self, path):
        self.path = path
        self.d = open(path,'rb').read()
        d = self.d
        (self.string_ids_size, self.string_ids_off, self.type_ids_size, self.type_ids_off,
         self.proto_ids_size, self.proto_ids_off, self.field_ids_size, self.field_ids_off,
         self.method_ids_size, self.method_ids_off, self.class_defs_size, self.class_defs_off,
         ) = struct.unpack_from('<12I', d, 56)
        self._strings = {}
    def string(self, idx):
        if idx in self._strings: return self._strings[idx]
        off = struct.unpack_from('<I', self.d, self.string_ids_off + idx*4)[0]
        n, off = uleb(self.d, off)
        end = self.d.index(b'\x00', off)
        s = self.d[off:end].decode('utf-8','replace')
        self._strings[idx] = s
        return s
    def type_desc(self, idx):
        return self.string(struct.unpack_from('<I', self.d, self.type_ids_off + idx*4)[0])
    def type_name(self, idx):
        return desc2java(self.type_desc(idx))
    def proto(self, idx):
        base = self.proto_ids_off + idx*12
        shorty, ret, params_off = struct.unpack_from('<3I', self.d, base)
        params = []
        if params_off:
            size = struct.unpack_from('<I', self.d, params_off)[0]
            for i in range(size):
                t = struct.unpack_from('<H', self.d, params_off+4+i*2)[0]
                params.append(self.type_name(t))
        return self.type_name(ret), params
    def method(self, idx):
        base = self.method_ids_off + idx*8
        cls, proto, name = struct.unpack_from('<HHI', self.d, base)
        ret, params = self.proto(proto)
        return self.type_name(cls), self.string(name), ret, params
    def field(self, idx):
        base = self.field_ids_off + idx*8
        cls, typ, name = struct.unpack_from('<HHI', self.d, base)
        return self.type_name(cls), self.string(name), self.type_name(typ)
    def classes(self):
        for i in range(self.class_defs_size):
            base = self.class_defs_off + i*32
            cidx, acc, sup, iface_off, src, anno, data_off, static_off = struct.unpack_from('<8I', self.d, base)
            yield self.type_name(cidx), acc, (self.type_name(sup) if sup != 0xffffffff else None), data_off, iface_off
    def class_members(self, data_off):
        if not data_off: return [], []
        d = self.d; off = data_off
        sf, off = uleb(d, off); inf, off = uleb(d, off); dm, off = uleb(d, off); vm, off = uleb(d, off)
        fields = []; methods = []
        idx = 0
        for _ in range(sf):
            diff, off = uleb(d, off); a, off = uleb(d, off); idx += diff
            fields.append((self.field(idx), a))
        idx = 0
        for _ in range(inf):
            diff, off = uleb(d, off); a, off = uleb(d, off); idx += diff
            fields.append((self.field(idx), a))
        idx = 0
        for _ in range(dm):
            diff, off = uleb(d, off); a, off = uleb(d, off); c, off = uleb(d, off); idx += diff
            methods.append((self.method(idx), a))
        idx = 0
        for _ in range(vm):
            diff, off = uleb(d, off); a, off = uleb(d, off); c, off = uleb(d, off); idx += diff
            methods.append((self.method(idx), a))
        return fields, methods

def accstr(a):
    return ' '.join(v for k,v in sorted(ACC.items()) if a & k)

def find_class(dexdir, names, show=True):
    out = {}
    for f in sorted(glob.glob(os.path.join(dexdir,'*.dex'))):
        try: dx = Dex(f)
        except Exception as e: continue
        for cname, acc, sup, data_off, iface_off in dx.classes():
            if cname in names:
                fields, methods = dx.class_members(data_off)
                out.setdefault(cname, []).append({
                    'dex': os.path.basename(f), 'access': accstr(acc), 'super': sup,
                    'fields': [(fn, ft, accstr(a)) for (fc, fn, ft), a in fields],
                    'methods': [(mn, ret, params, accstr(a)) for (mc, mn, ret, params), a in methods],
                })
    return out

if __name__ == '__main__':
    dexdir = sys.argv[1]
    names = set(sys.argv[2:])
    res = find_class(dexdir, names)
    for n in sys.argv[2:]:
        if n not in res:
            print(f'### {n}: NOT FOUND'); continue
        for e in res[n]:
            print(f"### {n}  [{e['dex']}] access={e['access']} super={e['super']}")
            for fn, ft, a in e['fields']:
                print(f"    field {a} {ft} {fn}")
            for mn, ret, params, a in e['methods']:
                print(f"    method {a} {ret} {mn}({', '.join(params)})")
