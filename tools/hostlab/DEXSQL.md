# 可选 DexSQL 后端与批量调度

旧 `dexq query/refs/decode/info` 默认仍走 SQLite/Androguard；Java 伪源码仍走现有 JADX CLI。
DexSQL 固定为 0.1.0，各平台资产在 `install_dexsql.py` 校验 SHA-256。安装不改变全局 PATH 或 MCP。

```powershell
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/install_dexsql.py
tools/hostlab/hostlab.cmd dexq capabilities
tools/hostlab/hostlab.cmd dexq query --version-code 9150200 --backend dexsql --sql "SELECT file_id,method_descriptor FROM class_methods WHERE method_name='getUrlsMap' ORDER BY file_id,method_idx"
tools/hostlab/hostlab.cmd dexq refs --version-code 9150200 --backend dexsql --detail methods --kind string --target disable_underline
```

Linux/macOS 直接使用当前 Python 调用 `tools/hostlab/hostlab.py`。`HOSTLAB_DEXSQL` 可指定已有程序，仍必须通过本平台固定哈希校验；不会向该覆盖路径下载或写入。
LICENSE、LICENSE-AUXILIARY 和导出的第三方声明保留在程序目录；客户端包分发安装器与许可，不夹带缓存或本地程序。

## 请求与计划

相关问题放在一个 JSON 请求文件中。示例：

```json
{
  "backend": "auto",
  "threads": 2,
  "timeout_seconds": 180,
  "tasks": [
    {"id":"urls","operation":"locate","kind":"method","name":"getUrlsMap"},
    {"id":"anchor","operation":"refs","kind":"string","target":"disable_underline"},
    {"id":"manifest","operation":"info"}
  ]
}
```

```powershell
tools/hostlab/hostlab.cmd dexq plan --request request.json
tools/hostlab/hostlab.cmd dexq batch --version-code 9150200 --request request.json --output result.json
```

至多 16 项、30000 UTF-8 字节，线程 1–6、总执行期限 1–600 秒。每个后端只开一个数据集，任务为独立只读操作，按后端分组顺序执行。
实际线程还受可用 CPU 数限制。完全相同的结构化任务会复用批内结果并返回 `reused_from`，原始 SQL 每次照常执行。

| operation | 参数 | 契约 |
| --- | --- | --- |
| query | sql, dialect, limit, offset | dialect 默认 sqlite；DexSQL SQL 显式声明 dexsql；不改写 SQL |
| locate | kind=class/method/field, name, 可选 owner | 查定义；类的 name 是完整类型描述符 |
| refs | kind=string/method/field/type, target, detail | 默认 methods，保留引用重复次数；sites 保留旧 offset/op 并走 SQLite |
| decode | method, 可选 file_id | 完整方法描述符；file_id 只对本次 DexSQL 数据集有效 |
| info | 无 | Manifest；部分权限页仍标 partial |

`auto` 对结构化引用优先 DexSQL，对已有热索引的纯结构查询复用 SQLite；若本批已需原生后端且无强制旧任务，结构查询共享原生会话，避免多开。
原生不可用时只对等价的结构化操作回退。强制 dexsql 或 DexSQL SQL 不会被送入 SQLite。

批次返回逐项 `complete/partial/error/skipped`、会话准备成本、版本和计划原因。任何截断或错误都不会标成完整成功，CLI 返回 2。
失效数据集和未知结果不会自动重放；MCP SDK 负责 EOF、Windows Job Object／POSIX 进程组的关闭和终止升级。
结果总预算 1 MiB，按完整任务结果记账；原始 SQL/native typed result 保留整数精度及分页字段。

## 远端工具

更新远程客户端并重新加载 MCP 后，旧四个工具继续存在，新增：

- `plan_analysis(request)`：只规划，不分发作业。计划中的 native 可用性在 runner 执行前验证。
- `submit_analysis(version_code, request, apk_sha256="", sample_revision="", idempotency_key="")`：一批共用一次样本下载和每后端一次准备。

先把示例对象传给 plan，再传给 submit；后续仍用返回的 request_id 调用 `job_status` 和分页 `job_result`。
强制纯 DexSQL 批次只安装既有依赖的 MCP/Hugging Face 子集，省去 Androguard。安装失败或后端错误不伪装成成功。

相同运行中请求会返回 `reused:true`。提供成对的准确 APK SHA-256 和不可变 sample_revision，可复用 24 小时内同一工具版本的成功结果。
显式 idempotency_key 绑定该请求（包含工具版本与样本选择）；同 key 改参数会拒绝，失败也不会偷偷重跑。
提交期间网络结果不明会返回 dispatch_unknown 和已有请求 ID，此时只查状态，不重新提交。
调度使用崩溃自动释放的 OS 锁；最多接纳 4 个可观察运行中或未确认提交。capacity_full/scheduler_busy 不分发新作业。
这是当前客户端与可观察 GitHub 队列的预算；多台客户端的竞争仍受 GitHub 实际调度约束。同一准确样本的批次在工作流中串行。

工作流绑定 scheduler 选择的准确工具提交，并在 sample_revision/APK SHA 下取样。`job.json` 保存输入、工具哈希、请求摘要、后端版本和耗时。
结果附件仅包含有界结果和元数据；APK、DEX、SQLite 及原生缓存保留在 runner。仓库与附件可见性以 GitHub 当前权限为准。
旧 decompile/audit 路径和发布规则不变。

## 兼容性边界与验收

DexSQL 的 methods/fields 是引用表，class_methods/class_fields 才是定义。file_id 顺序、LIKE 下划线、MUTF-8/文本排序与 SQLite 存在差异，不能直接替换任意旧 SQL。
旧 code_size 是 16 位 code units，对应 code_items.insns_size，不能映射到 opcode_count。
method_calls 只表示静态调用引用，不自动证明接口最终分派；引用方法身份与完整 offset/op 调用点格式分开。
MCP 复用内存数据集，`.dxc2` 磁盘缓存属于原生 CLI，当前批量执行不伪称重开命中磁盘缓存。

开发验收：

```powershell
tools/hostlab/.venv/Scripts/python.exe -m unittest discover -s tools/hostlab -p "test_*.py" -v
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/verify_backends.py --version-code 9150200 --output runtime/hostlab/verification --rounds 2 --jadx
```

Actions 的 backend_validation 操作用准确 runner_revision、样本 revision/SHA，对比类/方法/字段/四类引用集合、Manifest、Smali 和保留的 JADX CLI。
验证缓存位于附件目录之外，附件仅保存计时、计数、结果身份哈希和结论。静态验证不能替代 Android Hook／设备验收。
