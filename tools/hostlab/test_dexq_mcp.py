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
        long_value = "开头" + "黑神话悟空🔍" * 180 + "完整末尾"
        sql = "SELECT '" + long_value + "' AS long_value"
        preview = await call("query", dataset_id=ds, sql=sql)
        assert "cell(s) truncated at 300" in preview and "完整末尾" not in preview
        full = await call("query", dataset_id=ds, sql=sql, max_cell_chars=3000)
        assert full.splitlines()[1] == long_value and "truncated" not in full
        await call("query", expected_error=True, dataset_id=ds, sql=sql, max_cell_chars=0)
        # A real indexed host signature just above the legacy 300-character boundary.
        signature_sql = ("SELECT length(proto),substr(proto,-24),proto FROM methods "
                         "WHERE length(proto)>300 ORDER BY length(proto),file_id,method_idx LIMIT 1")
        signature = await call("query", dataset_id=ds, sql=signature_sql, max_cell_chars=16000)
        length, tail, proto = signature.splitlines()[1].split("\t")
        assert len(proto) == int(length) and proto.endswith(tail) and "truncated" not in signature
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
                          "long_cell_retrieved_via_mcp": True,
                          "host_long_signature_chars": int(length),
                          "multiple_statements_rejected": True, "index": opened["cache"],
                          "classes": opened["totals"]["classes"],
                          "seconds": round(time.monotonic() - start, 2)}, indent=2))


if __name__ == "__main__":
    asyncio.run(main(Path(sys.argv[1]).resolve()))
