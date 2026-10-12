"""Deterministic private report publisher. Model text cannot control paths or Git operations."""
import base64
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
import zipfile

REPO = "jichuo1/innocent-lab-host-analysis"


def api(path, data=None, method=None):
    req=urllib.request.Request("https://api.github.com/repos/"+REPO+("/"+path if path else ""),
        data=json.dumps(data).encode() if data is not None else None,
        headers={"Authorization":"Bearer "+os.environ["GH_TOKEN"],"Accept":"application/vnd.github+json",
                 "Content-Type":"application/json","X-GitHub-Api-Version":"2022-11-28"},
        method=method or ("POST" if data is not None else "GET"))
    with urllib.request.urlopen(req,timeout=60) as response:
        raw=response.read()
        return json.loads(raw) if raw else None


def compact(data):
    value={k:data.get(k) for k in ("sample","baseline","analysis_status","review_reasons","coverage_claim",
        "ai_status","ai_review","runtime_verified","limitations","regenerated_from_run","families","page_path_matrix")}
    value["changes"]=[{k:v for k,v in c.items() if k not in {"before","after"}} for c in data["changes"]]
    value["unregistered_protocol_count"]=len(data.get("unregistered_protocols",[]))
    value["protocol_twin_count"]=len(data.get("protocol_twins",[]))
    value["resource_change_counts"]={k:len(v) for k,v in (data.get("resource_changes") or {}).items() if isinstance(v,list)}
    ctx=data.get("source_snapshot") or {}
    value["source_snapshot"]={"repository_head":ctx.get("repository_head"),"working_tree_dirty":ctx.get("working_tree_dirty"),
        "files":[{"path":r["path"],"sha256":r["sha256"]} for r in ctx.get("source_records",[])]}
    return value


def evidence_note(data):
    matrix=data.get("page_path_matrix") or {}
    paths=[path for page in matrix.values() for path in page.get("paths",{}).values()]
    observed=sum(path.get("evidence")=="static_invoke_observed" for path in paths)
    absent=sum(path.get("evidence")=="absent" for path in paths)
    return ("## 静态事实核对（程序计算）\n\n"
        f"登记页面 {len(matrix)} 个，登记路径 {len(paths)} 条；其中 {observed} 条有静态调用证据，{absent} 条未检出。"
        "路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。\n\n"
        "方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。"
        "证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。"
        "未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。\n\n")


def prepare(root,run_id,attempt):
    data=json.loads((root/"remote-output/priority-summary.json").read_text(encoding="utf-8"))
    sample=data["sample"]
    sha=sample["sha256"]
    code=int(sample["version_code"])
    if code<=0 or not re.fullmatch(r"[0-9a-f]{64}",sha):
        raise RuntimeError("Invalid sample identity")
    complete_ai=data.get("ai_status")=="completed" and data.get("ai_review",{}).get("status")=="completed"
    if data.get("ai_review",{}).get("schema",1)>=2:
        complete_ai=complete_ai and data["ai_review"].get("review_status")=="completed" and (data["ai_review"].get("review") or {}).get("status")=="completed"
    key=f"{run_id}-a{attempt}"
    directory=f"samples/{code}/{sha}/runs/{key}"
    tag=f"analysis-{code}-{sha[:12]}-{key}"
    output=root/"publish-bundle"
    output.mkdir(parents=True,exist_ok=True)
    evidence=output/"evidence.zip"
    manifest=[]
    with zipfile.ZipFile(evidence,"w",zipfile.ZIP_DEFLATED) as archive:
        for base in (root/"remote-output",root/"reports"):
            if not base.exists(): continue
            for p in sorted(base.rglob("*")):
                if not p.is_file() or p.suffix not in {".json",".md",".tsv",".log",".txt",".java"}:
                    continue
                if "classes" in p.parts or "jadx-output" in p.parts:
                    continue
                relative=p.relative_to(root).as_posix()
                raw=p.read_bytes()
                manifest.append({"path":relative,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
                archive.write(p,relative)
    manifest_path=output/"evidence-manifest.json"
    manifest_path.write_text(json.dumps({"schema":1,"files":manifest},indent=2),encoding="utf-8")
    value=compact(data)
    value.update({"report_id":key,"analysis_run_id":int(run_id),"review_commit":os.environ.get("GITHUB_SHA"),
                  "evidence_release":f"https://github.com/{REPO}/releases/tag/{tag}" if complete_ai else None})
    entry={"report_id":key,"version_code":code,"version_name":sample["version_name"],"apk_sha256":sha,
           "status":data["analysis_status"] if complete_ai else "AI_ANALYSIS_FAILED","ai_status":data.get("ai_status","failed"),"complete":complete_ai,"path":directory+"/report.md",
           "created_at":datetime.now(timezone.utc).isoformat(),"run_url":f"https://github.com/{REPO}/actions/runs/{run_id}",
           "release_url":value["evidence_release"]}
    entry["request_id"]=os.environ.get("HOSTLAB_REQUEST_ID")
    files={directory+"/report.md":evidence_note(data)+(root/"remote-output/priority-report.md").read_text(encoding="utf-8"),
           directory+"/summary.json":json.dumps(value,ensure_ascii=False,indent=2),
           directory+"/evidence.json":json.dumps({"release":value["evidence_release"],"files":manifest},indent=2)}
    if complete_ai:
        files[f"samples/{code}/{sha}/latest.json"]=json.dumps(entry,indent=2)
    # Small FEATURE tables stay directly browsable in Git.
    for p in sorted((root/"reports").glob("*/*/*/features.tsv")):
        files[directory+"/features-"+p.parts[-4]+".tsv"]=p.read_text(encoding="utf-8")
    for text in files.values():
        if len(text.encode())>2*1024*1024:
            raise RuntimeError("Browsable report exceeds size budget")
    return entry,files,tag,[evidence,manifest_path]


def release(tag,assets):
    try:
        existing=api("releases/tags/"+tag)
    except urllib.error.HTTPError as exc:
        if exc.code!=404: raise
        existing=api("releases",{"tag_name":tag,"target_commitish":os.environ["GITHUB_SHA"],"name":tag,
            "body":"Complete static evidence and AI review. See reports branch for the readable report.","draft":False,"prerelease":True})
    names={a["name"] for a in api(f"releases/{existing['id']}/assets")}
    for p in assets:
        if p.name in names: continue
        req=urllib.request.Request(f"https://uploads.github.com/repos/{REPO}/releases/{existing['id']}/assets?name={p.name}",
            data=p.read_bytes(),headers={"Authorization":"Bearer "+os.environ["GH_TOKEN"],"Content-Type":"application/octet-stream"},method="POST")
        with urllib.request.urlopen(req,timeout=180) as response:
            response.read()


def publish(entry,files):
    for retry in range(4):
        try:
            head=api("git/ref/heads/reports")["object"]["sha"]
            tree=api("git/commits/"+head)["tree"]["sha"]
            old=api("contents/index.json?ref=reports")
            index=json.loads(base64.b64decode(old["content"]))
        except urllib.error.HTTPError as exc:
            if exc.code!=404: raise
            head,tree,index=None,None,{"schema":1,"reports":[]}
        if any(r["report_id"]==entry["report_id"] for r in index["reports"]):
            return
        index["reports"].append(entry)
        index["reports"].sort(key=lambda r:(r["version_code"],r["created_at"]),reverse=True)
        readme=["# 宿主适配分析报告", "", "任务成功不等于适配通过。AI 建议仍需人工和真机验收。", "",
                "| 样本 | 分析结论 | AI | 报告 | 完整证据 |", "|---|---|---|---|---|"]
        for r in index["reports"]:
            evidence="[下载]("+r["release_url"]+")" if r.get("release_url") else "—"
            readme.append(f"| {r['version_name']} / {r['version_code']} | {r['status']} | {r['ai_status']} | [查看]({r['path']}) | {evidence} |")
        files=dict(files)
        complete=[r for r in index["reports"] if r.get("complete") and r.get("apk_sha256")==entry.get("apk_sha256")]
        if complete and max(complete,key=lambda r:r["created_at"])["report_id"]!=entry["report_id"]:
            files.pop(f"samples/{entry['version_code']}/{entry['apk_sha256']}/latest.json",None)
        content={**files,"index.json":json.dumps(index,ensure_ascii=False,indent=2),"README.md":"\n".join(readme)}
        entries=[]
        for path,text in content.items():
            blob=api("git/blobs",{"content":base64.b64encode(text.encode()).decode(),"encoding":"base64"})
            entries.append({"path":path,"mode":"100644","type":"blob","sha":blob["sha"]})
        payload={"tree":entries}
        if tree: payload["base_tree"]=tree
        newtree=api("git/trees",payload)
        commit=api("git/commits",{"message":f"docs(report): publish {entry['version_code']} {entry['report_id']}",
                                  "tree":newtree["sha"],"parents":[head] if head else []})
        try:
            if head:
                api("git/refs/heads/reports",{"sha":commit["sha"],"force":False},method="PATCH")
            else:
                api("git/refs",{"ref":"refs/heads/reports","sha":commit["sha"]})
            print("Published report: https://github.com/"+REPO+"/blob/reports/"+entry["path"])
            return
        except urllib.error.HTTPError as exc:
            if exc.code not in (409,422) or retry==3: raise
            time.sleep(2)


def publish_result(entry,files,tag,assets):
    if entry["complete"]:
        release(tag,assets)
    publish(entry,files)


if __name__=="__main__":
    if not api("")["private"]:
        print("Warning: report repository is public; reports and Releases will be publicly visible.")
    run_id=os.environ["GITHUB_RUN_ID"]
    attempt=os.environ.get("GITHUB_RUN_ATTEMPT","1")
    if not run_id.isdigit() or not attempt.isdigit(): raise RuntimeError("Invalid run identity")
    root=Path(os.environ.get("HOSTLAB_REPORT_INPUT","runtime/hostlab/publish-input"))
    if not (root/"remote-output/priority-summary.json").exists():
        key=f"{run_id}-a{attempt}"
        path=f"failures/{key}/report.md"
        code=os.environ.get("HOSTLAB_VERSION","")
        entry={"report_id":key,"version_code":int(code) if code.isdigit() else 0,"version_name":"未完成",
               "apk_sha256":None,"status":"ANALYSIS_FAILED","ai_status":"not_completed","complete":False,
               "path":path,"created_at":datetime.now(timezone.utc).isoformat(),
               "run_url":f"https://github.com/{REPO}/actions/runs/{run_id}","release_url":None}
        entry["request_id"]=os.environ.get("HOSTLAB_REQUEST_ID")
        publish(entry,{path:"# 分析未完成\n\n本次未生成完整静态证据或 AI 报告。[查看运行日志]("+entry["run_url"]+")。\n"})
        raise SystemExit(0)
    entry,files,tag,assets=prepare(root,run_id,attempt)
    publish_result(entry,files,tag,assets)
