"""Real MCP transport smoke test; --submit launches exactly one remote info job."""
import argparse
import asyncio
import json
from pathlib import Path
import sys
from mcp import Client
from mcp.client.stdio import StdioServerParameters
import hostlab


async def main(args):
    params = StdioServerParameters(command=sys.executable,
        args=[str(Path(__file__).with_name("remote_mcp.py"))])
    async with Client(params) as client:
        tools = await client.list_tools()
        assert {t.name for t in tools.tools} == {"submit_job", "job_status", "job_result", "list_jobs", "plan_analysis", "submit_analysis"}
        async def call(name, arguments):
            r = await client.call_tool(name, arguments)
            assert not r.is_error, name
            return json.loads("\n".join(getattr(c, "text", "") for c in r.content))
        if args.submit:
            result = await call("submit_job", {"version_code": 9140200, "operation": args.operation,
                                              "argument": args.argument})
            hostlab.write_json(hostlab.STATE / "remote-smoke.json", result)
            print(json.dumps(result))
        elif args.request:
            status = await call("job_status", {"request_id": args.request})
            print(json.dumps(status))
            if status.get("status") == "completed":
                result = await call("job_result", {"request_id": args.request})
                assert status["conclusion"] == "success", result["text"][:500]
                assert args.expected in result["text"]
                print(json.dumps({"remote_round_trip": "passed", "files": result["files"]}))
        else:
            result = await client.call_tool("submit_job", {"version_code": -1, "operation": "info"})
            assert result.is_error
            print("Remote MCP: six tools discovered; invalid input rejected")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--request")
    parser.add_argument("--operation", choices=("info", "decompile", "query"), default="info")
    parser.add_argument("--argument", default="")
    parser.add_argument("--expected", default="tv.danmaku.bili")
    asyncio.run(main(parser.parse_args()))
