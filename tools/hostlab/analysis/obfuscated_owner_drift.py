"""跨版本核对"按混淆类名写死的候选名单"是否还命中。

背景：`comment_topology` 的 ReplyInfo -> CommentItem mapper facade 与相关游戏推广组件都放在
稳定包内，但类名随每次 R8 混淆在单字母之间漂移。写死名单会静默落空（9.6.0、9.10.0 各发生过
一次），HostCompatibilityAudit 当时又没有覆盖这两个域，因此单独留一份可直接运行的核对脚本。

只读 APK 的 DEX，不解压到磁盘、不反编译、不联网。

用法：
    python tools/hostlab/analysis/obfuscated_owner_drift.py Bilibili_Innocent_Lab/*.apk
"""

import glob
import os
import struct
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dex_reader import Dex, accstr  # noqa: E402

REPLY_INFO = "com.bapis.bilibili.main.community.reply.v1.ReplyInfo"
COMMENT_ITEM = "com.bilibili.app.comment3.data.model.CommentItem"
MAPPER_PACKAGE = "com.bilibili.app.comment3.data.source.v1"
RELATE_GAME_PACKAGE = "com.bilibili.ship.theseus.united.page.intro.module.relate.game"
GEMINI_UI_PACKAGE = "com.bilibili.app.gemini.ui"

# 与 VersionAdapter / DetailAppPromotionFeatureInstaller 保持一致的有界字母表。
ALPHABET = [chr(c) for c in range(ord("a"), ord("z") + 1)]


class _MemDex(Dex):
    def __init__(self, data):
        self.path = "<memory>"
        self.d = data
        (self.string_ids_size, self.string_ids_off, self.type_ids_size, self.type_ids_off,
         self.proto_ids_size, self.proto_ids_off, self.field_ids_size, self.field_ids_off,
         self.method_ids_size, self.method_ids_off, self.class_defs_size,
         self.class_defs_off) = struct.unpack_from("<12I", data, 56)
        self._strings = {}


def iter_dex(apk):
    with zipfile.ZipFile(apk) as archive:
        for name in archive.namelist():
            if name.startswith("classes") and name.endswith(".dex"):
                yield _MemDex(archive.read(name))


def inspect(apk):
    mappers = []
    relate_components = []
    gemini_bases = []
    for dex in iter_dex(apk):
        for cname, acc, sup, data_off, _ in dex.classes():
            try:
                _, methods = dex.class_members(data_off)
            except Exception:
                continue
            names = {mn: params for (_, mn, _, params), _ in methods}
            for (_, mn, ret, params), flags in methods:
                if (ret == COMMENT_ITEM and params and params[0] == REPLY_INFO
                        and flags & 0x8 and not flags & 0x1000 and not flags & 0x400):
                    mappers.append((cname, mn))
            if cname.startswith(RELATE_GAME_PACKAGE + "."):
                # 与 installRelateGameComponentBlock 的结构过滤一致：非接口、非抽象、
                # 继承 gemini 基类，且同时声明 (Context, LayoutInflater, ViewGroup) -> ViewBinding
                # 与 (ViewBinding, Continuation) 两个方法。
                creates = any(
                    ret == "androidx.viewbinding.ViewBinding" and p == [
                        "android.content.Context",
                        "android.view.LayoutInflater",
                        "android.view.ViewGroup",
                    ]
                    for (_, _, ret, p), _ in methods
                )
                binds = any(
                    len(p) == 2 and p[0] == "androidx.viewbinding.ViewBinding"
                    and p[1] == "kotlin.coroutines.Continuation"
                    for (_, _, _, p), _ in methods
                )
                if creates and binds and not acc & 0x400 and not acc & 0x200:
                    relate_components.append((cname, sup))
            if cname.startswith(GEMINI_UI_PACKAGE + ".") and "$" not in cname:
                if (len(names.get("createViewEntry", [])) == 2
                        and len(names.get("bindToView", [])) == 2
                        and acc & 0x400 and not acc & 0x200):
                    gemini_bases.append(cname)
    return mappers, relate_components, gemini_bases


def covered(class_name, package):
    if not class_name.startswith(package + "."):
        return False
    return class_name[len(package) + 1:] in ALPHABET


def main(patterns):
    apks = sorted({path for pattern in patterns for path in glob.glob(pattern)})
    if not apks:
        print("no apk matched", file=sys.stderr)
        return 1
    failures = 0
    for apk in apks:
        mappers, relate, gemini = inspect(apk)
        owners = sorted({owner for owner, _ in mappers})
        mapper_ok = bool(owners) and all(covered(o, MAPPER_PACKAGE) for o in owners)
        relate_owners = sorted({owner for owner, _ in relate})
        # 候选表除字母表外还保留未混淆的 RelateGameComponent（8.84.0–8.96.0 使用）。
        relate_ok = len(relate_owners) == 1 and (
            covered(relate_owners[0], RELATE_GAME_PACKAGE)
            or relate_owners[0] == RELATE_GAME_PACKAGE + ".RelateGameComponent"
        )
        # 运行期按显式优先顺序取第一个命中的候选，同包内的 DataBindingComponent 等长名类
        # 不在字母表候选里，因此只要求"至少有一个单字母基类可命中"。
        # 8.63.0–8.88.0 尚无 gemini 组件框架，整个域不适用，不计为漂移。
        gemini_ok = not gemini or any(covered(name, GEMINI_UI_PACKAGE) for name in gemini)
        if not (mapper_ok and relate_ok and gemini_ok):
            failures += 1
        print(f"{os.path.basename(apk)}")
        print(f"    mapper owners      : {owners or '-'}  covered={mapper_ok}")
        print(f"    relate game owners : {relate_owners or '-'}  covered={relate_ok}")
        gemini_letters = [name for name in gemini if covered(name, GEMINI_UI_PACKAGE)]
        gemini_state = "n/a" if not gemini else str(gemini_ok)
        print(f"    gemini bases       : {gemini_letters or '-'}  covered={gemini_state}")
    print(f"\n{len(apks)} apk checked, {failures} outside the bounded alphabet")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["Bilibili_Innocent_Lab/*.apk"]))
