"""Select existing dependency subsets before an Actions analysis; stdlib only."""
import json
import os
import analysis_plan


def requirements(operation, argument):
    native = optional = native_only = False
    if operation == "batch":
        request = analysis_plan.validate(json.loads(argument))
        plan = analysis_plan.plan(request)
        native = any(g["backend"] == "dexsql" for g in plan["groups"])
        optional = request["backend"] == "auto" and not any(
            t["operation"] == "query" and t["dialect"] == "dexsql" or "file_id" in t for t in request["tasks"])
        native_only = native and not optional and len(plan["groups"]) == 1
    elif operation == "backend_validation":
        native = True
    return {"needs_dexsql": str(native).lower(), "dexsql_optional": str(optional).lower(),
            "requirements": "requirements-query.txt" if native_only else "requirements.txt"}


if __name__ == "__main__":
    result = requirements(os.environ["HOSTLAB_OPERATION"], os.environ.get("HOSTLAB_ARGUMENT", ""))
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
        for name,value in result.items():
            stream.write(name + "=" + value + "\n")
