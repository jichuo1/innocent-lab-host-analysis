"""Select existing dependency subsets before an Actions analysis; stdlib only."""
import json
import os
import analysis_plan


def requirements(operation, argument, backend=None):
    backend = os.environ.get("HOSTLAB_BACKEND", "sqlite") if backend is None else backend
    if backend not in {"sqlite", "dexsql"}:
        raise ValueError("backend must be sqlite or dexsql")
    native = optional = False
    native_only = operation == "regenerate_ai"
    if operation in {"batch", "batch_group"}:
        if operation == "batch_group":
            import runner_group
            request = runner_group.validate(json.loads(argument))["request"]
        else:
            request = analysis_plan.validate(json.loads(argument))
        plan = analysis_plan.plan(request)
        native = any(g["backend"] == "dexsql" for g in plan["groups"])
        optional = request["backend"] == "auto" and not any(
            t["operation"] == "query" and t["dialect"] == "dexsql" or "file_id" in t for t in request["tasks"])
        native_only = native and not optional and len(plan["groups"]) == 1
    elif operation == "backend_validation":
        native = True
    elif operation in {"audit", "multipath_audit"}:
        native = optional = True
    elif operation in analysis_plan.REMOTE_COMMANDS:
        # A single command declares one backend; the native one needs its verified
        # binary before the APK is opened, the legacy one keeps androguard only.
        native = backend == "dexsql"
        native_only = native
    return {"needs_dexsql": str(native).lower(), "dexsql_optional": str(optional).lower(),
            "needs_java":str(operation in {"audit","decompile","multipath_audit","backend_validation"}).lower(),
            "requirements": "requirements-query.txt" if native_only else "requirements.txt"}


if __name__ == "__main__":
    result = requirements(os.environ["HOSTLAB_OPERATION"], os.environ.get("HOSTLAB_ARGUMENT", ""))
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        for name,value in result.items():
            stream.write(name + "=" + value + "\n")
