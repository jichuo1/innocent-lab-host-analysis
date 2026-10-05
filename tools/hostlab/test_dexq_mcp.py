"""Exercise every packaged MCP tool and SQL rejection through a real stdio client."""
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
        async def call(name, expected_error=False, **kwargs):
            response = await client.call_tool(name, kwargs)
            assert bool(response.is_error) == expected_error, name
            return "\n".join(getattr(c, "text", "") for c in response.content)
        tools = await client.list_tools()
        assert len(tools.tools) == 8
        start = time.monotonic()
        opened = json.loads(await call("open_dataset", inputs=[str(apk)]))
        ds = opened["dataset_id"]
        assert opened["totals"]["classes"] > 0
        await call("list_datasets")
        await call("describe_tables")
        result = await call("query", dataset_id=ds, limit=5,
                            sql="SELECT class,name,proto FROM methods WHERE class='Lcom/bapis/bilibili/main/community/reply/v1/Content;' AND name='getUrlsMap'")
        assert "getUrlsMap" in result
        await call("query", expected_error=True, dataset_id=ds, sql="DROP TABLE classes")
        await call("query", expected_error=True, dataset_id=ds, sql="SELECT 1; SELECT 2")
        method = "Lcom/bapis/bilibili/main/community/reply/v1/Content;->getUrlsMap()Ljava/util/Map;"
        code = await call("decode", dataset_id=ds, method=method, max_chars=2000)
        assert "getUrlsMap" in code
        await call("find_refs", dataset_id=ds, kind="method", target=method, limit=2)
        info = json.loads(await call("apk_info", path=str(apk)))
        assert info["package"] == "tv.danmaku.bili"
        await call("close_dataset", dataset_id=ds)
        print(json.dumps({"tools_verified": 8, "sql_write_rejected": True,
                          "multiple_statements_rejected": True, "index": opened["cache"],
                          "classes": opened["totals"]["classes"],
                          "seconds": round(time.monotonic() - start, 2)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]).resolve()))
