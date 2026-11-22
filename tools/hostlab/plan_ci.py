"""Select existing dependency subsets before an Actions analysis; stdlib only."""
import json
import os
import analysis_plan


def requirements(operation, argument, backend=None):
    backend = os.environ.get("HOSTLAB_BACKEND", "meguvizdexdash") if backend is None else backend
    if backend not in {"sqlite", "dexsql", "meguvizdexdash"}:
        raise ValueError("backend must be sqlite, dexsql, or meguvizdexdash")
    native = optional = False
    needs_java = operation == "decompile"
    native_only = operation == "regenerate_ai"
    if operation in {"batch", "batch_group"}:
        if operation == "batch_group":
            import runner_group
            request = runner_group.validate(json.loads(argument))["request"]
        else:
            request = analysis_plan.validate(json.loads(argument))
        plan = analysis_plan.plan(request)
        native = any(g["backend"] in analysis_plan.NATIVE_BACKENDS for g in plan["groups"])
        optional = request["backend"] == "auto" and not any(
            (t["operation"] == "query" and t["dialect"] in analysis_plan.NATIVE_BACKENDS) or "file_id" in t
            for t in request["tasks"])
        native_only = native and not optional and len(plan["groups"]) == 1
    elif operation == "backend_validation":
        options = json.loads(argument or "{}")
        if not isinstance(options, dict):
            raise ValueError("backend_validation options must be a JSON object")
        is_audit = bool(options.get("audit", False))
        has_ref = bool(options.get("native_reference"))
        native = True
        needs_java = (is_audit and not has_ref) or (not is_audit and bool(options.get("jadx", True)))
        native_only = is_audit and has_ref
    elif operation in {"audit", "multipath_audit"}:
        native = optional = True
        needs_java = False
    elif operation in analysis_plan.REMOTE_COMMANDS:
        # A single command declares one backend; the native one needs its verified
        # binary before the APK is opened, the legacy one keeps androguard only.
        native = backend in analysis_plan.NATIVE_BACKENDS
        native_only = native
    return {"needs_mdd": str(native).lower(), "mdd_optional": str(optional).lower(),
            "needs_dexsql": "false", "dexsql_optional": "false",
            "needs_java": str(needs_java).lower(),
            "requirements": "requirements-query.txt" if native_only else "requirements.txt"}


if __name__ == "__main__":
    result = requirements(os.environ["HOSTLAB_OPERATION"], os.environ.get("HOSTLAB_ARGUMENT", ""))
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        for name,value in result.items():
            stream.write(name + "=" + value + "\n")
