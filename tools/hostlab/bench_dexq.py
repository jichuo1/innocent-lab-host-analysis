"""Benchmark packaged dexq using the real stdio MCP transport."""
import asyncio
import json
from pathlib import Path
import sys
import time
from mcp import Client
from mcp.client.stdio import StdioServerParameters
import dexq_cli


async def main(apk):
    params = StdioServerParameters(command=sys.executable, args=[str(dexq_cli.SERVER)],
                                   env=dexq_cli.environment(apk), cwd=str(dexq_cli.SERVER.parent))
    async with Client(params) as client:
        async def timed(name, arguments):
            started = time.monotonic()
            result = await client.call_tool(name, arguments)
            assert not result.is_error, name
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            return text, round(time.monotonic() - started, 3)
        text, opened_s = await timed("open_dataset", {"inputs": [str(apk)]})
        opened = json.loads(text)
        _, query_s = await timed("query", {"dataset_id": opened["dataset_id"],
            "sql": "SELECT file_id,class,name,proto FROM methods WHERE name='getUrlsMap'", "limit": 10})
        _, refs_s = await timed("find_refs", {"dataset_id": opened["dataset_id"], "kind": "string",
                                               "target": "disable_underline", "limit": 2})
        print(json.dumps({"cache": opened["cache"], "open_seconds": opened_s,
                          "query_seconds": query_s, "string_refs_seconds": refs_s}, indent=2))


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]).resolve()))
