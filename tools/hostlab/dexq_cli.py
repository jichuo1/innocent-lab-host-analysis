"""Portable CLI over the existing dexq MCP implementation; no GUI required."""
import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import analyze
import hostlab

SERVER = Path(__file__).resolve().parent / "dexq/server.py"


def environment(apk=None):
    from huggingface_hub.constants import HF_HUB_CACHE
    env = dict(os.environ)
    env["DEXQ_CACHE_DIR"] = str(hostlab.STATE / "dexq-cache")
    env["DEXQ_ROOTS"] = os.pathsep.join([str(apk.parent)] if apk else
                                       [str(hostlab.ROOT), str(Path(HF_HUB_CACHE).resolve())])
    env["PYTHONIOENCODING"] = "utf-8"
    return env


async def run(args, apk, sample):
    from mcp import Client
    from mcp.client.stdio import StdioServerParameters
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)],
                                   env=environment(apk), cwd=str(SERVER.parent))
    async with Client(params) as client:
        async def call(name, **arguments):
            result = await client.call_tool(name, arguments)
            text = "\n".join(getattr(item, "text", "") for item in result.content)
            if result.is_error:
                raise RuntimeError("dexq rejected operation: " + text[:500])
            return text
        opened = json.loads(await call("open_dataset", inputs=[str(apk)]))
        dataset = opened["dataset_id"]
        if args.command == "index":
            output = json.dumps({"sample": sample, "index": opened}, ensure_ascii=False, indent=2)
        elif args.command == "query":
            output = await call("query", dataset_id=dataset, sql=args.sql, limit=args.limit)
        elif args.command == "decode":
            output = await call("decode", dataset_id=dataset, method=args.method, max_chars=args.max_chars)
        elif args.command == "refs":
            output = await call("find_refs", dataset_id=dataset, kind=args.kind, target=args.target, limit=args.limit)
        elif args.command == "info":
            output = await call("apk_info", path=str(apk))
        else:
            output = await call("describe_tables")
        print(output)
        await call("close_dataset", dataset_id=dataset)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("mcp", help="Launch stdio server; configure your AI client explicitly")
    for name in ("index", "query", "decode", "refs", "info", "tables"):
        command = sub.add_parser(name)
        source = command.add_mutually_exclusive_group(required=True)
        source.add_argument("--apk", type=Path)
        source.add_argument("--version-code", type=int)
        command.add_argument("--sha256")
        command.add_argument("--revision")
        if name == "query":
            command.add_argument("--sql", required=True)
        if name in {"query", "refs"}:
            command.add_argument("--limit", type=int, default=100)
        if name == "decode":
            command.add_argument("--method", required=True)
            command.add_argument("--max-chars", type=int, default=12000)
        if name == "refs":
            command.add_argument("--kind", choices=("method", "field", "string", "type"), required=True)
            command.add_argument("--target", required=True)
    args = parser.parse_args(argv)
    if args.command == "mcp":
        os.execve(sys.executable, [sys.executable, str(SERVER)], environment())
    else:
        apk, sample = analyze.inputs(args)
        asyncio.run(run(args, apk, sample))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
