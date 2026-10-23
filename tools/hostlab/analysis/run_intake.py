"""宿主升版接入：身份、字母表漂移、可选 jadx 结构审计、与上一版 FEATURE 对照。

用法（仓库根）：
    python tools/hostlab/analysis/run_intake.py path/to/bili.apk
    python tools/hostlab/analysis/run_intake.py path/to/bili.apk --prev tools/hostlab/analysis/fixed-audits/9.10.0.tsv
    python tools/hostlab/analysis/run_intake.py path/to/bili.apk --audit --prev ...

不联网、不写 APK。--audit 需要本机 jadx-*-all.jar，9.10 量级要数分钟。
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from obfuscated_owner_drift import inspect, covered, MAPPER_PACKAGE, RELATE_GAME_PACKAGE, GEMINI_UI_PACKAGE  # noqa: E402

# HostCompatibilityAudit.run() 当前写出的 FEATURE id。增域后同步这里。
EXPECTED_FEATURES = [
    "block_update",
    "player_default_quality",
    "comment_free_copy",
    "description_free_copy",
    "home_top_bar",
    "mine_entry",
    "mine_vip",
    "dynamic_tabs",
    "full_number",
    "player_portrait",
    "player_status_bar",
    "home_recommend",
    "video_relate",
    "home_tabs",
    "mine_components",
    "story_purify",
    "splash_ads",
    "bottom_bar",
    "teenagers_mode",
    "comment_filter",
    "comment_purify",
    "comment_topology",
    "comment_section",
    "paused_ad",
    "home_banner",
    "merchandise",
    "game_promotion",
]

# 安装器存在、审计 FEATURE 集合覆盖不到（或只覆盖一部分）的点。
COVERAGE_GAPS = [
    (
        "home_vertical_detail",
        "竖屏进普通详情的启动边界。审计没有对应 FEATURE；改 cid 前必须有设备抓包。",
    ),
    (
        "home_component_filter",
        "首页子 Fragment 隐藏。locateHomeComponents，审计未覆盖。",
    ),
    (
        "mine_account_mine",
        "AccountMine.sectionListV2 数据层。mine_components FOUND 只证明 MenuGroup getter/legacy。",
    ),
    (
        "detail_app_promotion / RelateGameComponent",
        "只认 obfuscated_owner_drift 的 relate game 行，不认 game_promotion FEATURE（那是 mention 协议）。",
    ),
    (
        "player_interactive_overlay",
        "播放器互动层的 Moss/VideoGuide/DmResource 和 DmViewReply.activityMeta。须补查全部载体、默认实例保护及保留名单。",
    ),
    (
        "pgc_auto_activity_popup",
        "OgvActivityVo 自动弹出描述符。paused_ad FOUND 不能证明该层；须补查 constructWith 参数槽位和可空重建契约。",
    ),
]

AAPT_CANDIDATES = [
    os.environ.get("HOSTLAB_AAPT", ""),
    os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Android",
        "Sdk",
        "build-tools",
        "36.0.0",
        "aapt.exe",
    ),
    os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Android",
        "Sdk",
        "build-tools",
        "35.0.0",
        "aapt.exe",
    ),
    os.path.join(
        os.environ.get("ANDROID_HOME", ""),
        "build-tools",
        "36.0.0",
        "aapt.exe",
    ),
]

JADX_CANDIDATES = [
    os.environ.get("HOSTLAB_JADX_JAR", ""),
    os.path.join(os.path.expanduser("~"), "jadx", "lib", "jadx-1.5.6-all.jar"),
    *glob.glob(os.path.join(os.path.expanduser("~"), "jadx", "lib", "jadx-*-all.jar")),
]


def first_existing(paths):
    seen = set()
    for path in paths:
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            return path
    return None


def dump_identity(apk: str) -> dict:
    info = {
        "file": os.path.basename(apk),
        "size": os.path.getsize(apk),
        "package": None,
        "versionName": None,
        "versionCode": None,
    }
    aapt = first_existing(AAPT_CANDIDATES)
    if not aapt:
        print("aapt not found; identity is filename-only", file=sys.stderr)
        return info
    # Windows aapt/ziparchive 打不开含非 ASCII 的路径；拷到短英文名再 dump。
    tmp_dir = None
    target = apk
    try:
        try:
            apk.encode("ascii")
        except UnicodeEncodeError:
            tmp_dir = tempfile.mkdtemp(prefix="host-intake-")
            target = os.path.join(tmp_dir, "host.apk")
            shutil.copy2(apk, target)
        out = subprocess.check_output(
            [aapt, "dump", "badging", target],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.CalledProcessError as exc:
        snippet = (exc.output or str(exc))[:400]
        print(f"aapt failed: {snippet}", file=sys.stderr)
        return info
    finally:
        if tmp_dir:
            shutil.rmtree(tmp_dir, ignore_errors=True)
    match = re.search(
        r"package: name='([^']+)' versionCode='([^']+)' versionName='([^']+)'",
        out,
    )
    if match:
        info["package"] = match.group(1)
        info["versionCode"] = match.group(2)
        info["versionName"] = match.group(3)
    return info


def print_identity(info: dict) -> None:
    print("== identity ==")
    print(f"    file         : {info['file']}  ({info['size']} bytes)")
    print(f"    package      : {info['package'] or '-'}")
    print(f"    versionName  : {info['versionName'] or '-'}")
    print(f"    versionCode  : {info['versionCode'] or '-'}")
    if info["package"] and info["package"] != "tv.danmaku.bili":
        print("    WARNING: package is not tv.danmaku.bili — HD / 渠道包不在本清单范围")


def print_drift(apk: str) -> int:
    print("== alphabet drift ==")
    mappers, relate, gemini = inspect(apk)
    owners = sorted({owner for owner, _ in mappers})
    mapper_ok = bool(owners) and all(covered(owner, MAPPER_PACKAGE) for owner in owners)
    relate_owners = sorted({owner for owner, _ in relate})
    relate_ok = len(relate_owners) == 1 and (
        covered(relate_owners[0], RELATE_GAME_PACKAGE)
        or relate_owners[0] == RELATE_GAME_PACKAGE + ".RelateGameComponent"
    )
    gemini_ok = not gemini or any(covered(name, GEMINI_UI_PACKAGE) for name in gemini)
    gemini_letters = [name for name in gemini if covered(name, GEMINI_UI_PACKAGE)]
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
    return failures


def parse_features(tsv_path: str) -> dict[str, tuple[str, str]]:
    rows = {}
    with open(tsv_path, encoding="utf-8") as handle:
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3 and parts[0] == "FEATURE":
                detail = parts[3] if len(parts) > 3 else ""
                rows[parts[1]] = (parts[2], detail)
    return rows


def print_feature_report(tsv_path: str, prev_path: str | None) -> int:
    print(f"== audit features ({os.path.basename(tsv_path)}) ==")
    rows = parse_features(tsv_path)
    prev = parse_features(prev_path) if prev_path else {}
    problems = 0
    for feature_id in EXPECTED_FEATURES:
        if feature_id not in rows:
            print(f"    {feature_id:24} ABSENT from TSV (auditor older than checklist?)")
            problems += 1
            continue
        state, detail = rows[feature_id]
        mark = ""
        if prev and feature_id in prev and prev[feature_id][0] != state:
            mark = f"  (was {prev[feature_id][0]})"
        if state != "FOUND":
            problems += 1
        snippet = detail if len(detail) <= 120 else detail[:117] + "..."
        print(f"    {feature_id:24} {state}{mark}")
        if state != "FOUND" and snippet:
            print(f"        {snippet}")
    extra = sorted(set(rows) - set(EXPECTED_FEATURES))
    if extra:
        print(f"    extra FEATURE ids: {extra}")
    if prev:
        print("== vs previous ==")
        for feature_id in EXPECTED_FEATURES:
            old = prev.get(feature_id)
            new = rows.get(feature_id)
            if not old or not new:
                continue
            if old[0] != new[0]:
                print(f"    {feature_id}: {old[0]} -> {new[0]}")
        if not any(
            prev.get(fid) and rows.get(fid) and prev[fid][0] != rows[fid][0]
            for fid in EXPECTED_FEATURES
        ):
            print("    no FEATURE state changes among expected ids")
    return problems


def print_gaps() -> None:
    print("== coverage gaps (not in FEATURE set; still must check) ==")
    for name, reason in COVERAGE_GAPS:
        print(f"    {name}")
        print(f"        {reason}")


def print_version_hints() -> None:
    print("== sv / rule decision ==")
    print("    JSON 字段增删改            -> SCHEMA_VERSION 和 ADAPTER_RULE_VERSION 都加")
    print("    只改候选表 / 结构过滤      -> 只加 ADAPTER_RULE_VERSION")
    print("    字母表仍覆盖 mapper/relate -> 不写死短名，不 bump")
    print("    topology 规则变了          -> 必须加 rule（快路径不检查 commentTopology）")
    print("    阻止更新/画质新 owner      -> 前置进候选表，保留旧项，加 rule")


def compile_and_run_audit(apk: str, tsv_path: str) -> int:
    jadx = first_existing(JADX_CANDIDATES)
    if not jadx:
        print("jadx-*-all.jar not found; skip --audit", file=sys.stderr)
        print("expected: %USERPROFILE%\\jadx\\lib\\jadx-1.5.6-all.jar", file=sys.stderr)
        return 1
    javac = "javac"
    java = "java"
    classes_dir = os.path.join(HERE, "audit-classes")
    os.makedirs(classes_dir, exist_ok=True)
    src = os.path.join(HERE, "HostCompatibilityAudit.java")
    print(f"== compile audit (jadx={jadx}) ==")
    compile_cmd = [
        javac,
        "-J-Xmx512m",
        "-encoding",
        "UTF-8",
        "-cp",
        jadx,
        "-d",
        classes_dir,
        src,
    ]
    try:
        subprocess.check_call(compile_cmd, timeout=180)
    except subprocess.TimeoutExpired:
        print("javac timed out", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError:
        print("javac failed", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("javac not on PATH", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(tsv_path)), exist_ok=True)
    sep = ";" if os.name == "nt" else ":"
    run_cmd = [
        java,
        "-Xmx" + str(int(os.environ.get("HOSTLAB_AUDIT_HEAP_MIB", "4096"))) + "m",
        "-XX:+ExitOnOutOfMemoryError",
        "-cp",
        classes_dir + sep + jadx,
        "HostCompatibilityAudit",
        os.path.abspath(apk),
        os.path.abspath(tsv_path),
    ]
    print(f"== run audit -> {tsv_path} ==")
    print("    heap MiB=" + os.environ.get("HOSTLAB_AUDIT_HEAP_MIB", "4096"), flush=True)
    try:
        subprocess.check_call(run_cmd)
    except subprocess.CalledProcessError:
        print("HostCompatibilityAudit failed", file=sys.stderr)
        return 1
    return 0


def default_tsv_path(apk: str, info: dict) -> str:
    version = info.get("versionName") or "unknown"
    return os.path.join(HERE, "fixed-audits", f"{version}.tsv")


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass
    parser = argparse.ArgumentParser(description="Host APK intake checklist runner")
    parser.add_argument("apk", help="official tv.danmaku.bili APK")
    parser.add_argument("--prev", help="previous fixed-audits TSV for FEATURE diff")
    parser.add_argument(
        "--audit",
        action="store_true",
        help="compile and run HostCompatibilityAudit (needs jadx, slow)",
    )
    parser.add_argument(
        "--tsv",
        help="audit output TSV; default tools/hostlab/analysis/fixed-audits/<versionName>.tsv",
    )
    args = parser.parse_args(argv)
    apk = os.path.abspath(args.apk)
    if not os.path.isfile(apk):
        print(f"apk not found: {apk}", file=sys.stderr)
        return 1
    if zipfile.is_zipfile(apk) is False:
        print(f"not a zip/apk: {apk}", file=sys.stderr)
        return 1

    info = dump_identity(apk)
    print_identity(info)
    failures = print_drift(apk)
    print_gaps()
    print_version_hints()

    tsv_path = os.path.abspath(args.tsv) if args.tsv else default_tsv_path(apk, info)
    if args.audit:
        audit_rc = compile_and_run_audit(apk, tsv_path)
        if audit_rc != 0:
            return audit_rc
        failures += print_feature_report(tsv_path, args.prev)
    elif args.prev and os.path.isfile(args.prev):
        print("== note ==")
        print("    --audit not set; FEATURE diff skipped. Pass --audit to produce a current TSV.")
        print(f"    previous TSV kept for later: {args.prev}")
    elif args.prev:
        print(f"previous TSV not found: {args.prev}", file=sys.stderr)

    print("== next ==")
    print("    1. MISSING/PARTIAL -> 打开 TSV 的 DISCOVERY / mapperOwners，按 HOST_INTAKE.md §6 改候选表")
    print("    2. 字母表仍覆盖 -> 不要写死这次的短名")
    print("    3. 改规则后加 ADAPTER_RULE_VERSION；改 JSON 形状再加 SCHEMA_VERSION")
    print("    4. 真机最低集见 HOST_INTAKE.md §8；静态 FOUND 不能写进 README 已验证列")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
