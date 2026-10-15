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

更新远程客户端并重新加载 MCP 后，旧四个工具继续存在，并提供单样本和版本矩阵工具：

- `plan_analysis(request)`：只规划，不分发作业。计划中的 native 可用性在 runner 执行前验证。
- `submit_analysis(version_code, request, apk_sha256="", sample_revision="", idempotency_key="")`：一批共用一次样本下载和每后端一次准备。

先把示例对象传给 plan，再传给 submit；后续仍用返回的 request_id 调用 `job_status` 和分页 `job_result`。
强制纯 DexSQL 批次只安装既有依赖的 MCP/Hugging Face 子集，省去 Androguard。安装失败或后端错误不伪装成成功。

Actions 将已安装依赖保存在独立的 `runtime/hostlab-prepared` 隔离环境，使用精确 Python/ABI、OS/架构、runner image、工作区路径、requirements 与准备器源码摘要定位缓存。
恢复后先校验完整文件/目录/链接清单和 SHA-256，再启动解释器验证环境绑定、顶层固定版本及完整已安装版本清单；损坏或失配时重建。
冷安装使用既有 pip 管理无 pip 的 venv，完成依赖检查才发布回执；缓存只保存依赖，在样本步骤之前完成保存，不包含 HF_HOME、APK/DEX、报告或认证文件。
未设置宽泛 restore key；缓存服务不可用时本次冷建，缓存本身不提供成功凭据。失配缓存保留在缓存根以外的受控隔离目录，未自动删除证据。
传递依赖的解析结果记录并校验在缓存回执中；冷重建仍由既有 requirements 解析，不声称不同日期的冷解析已由完整 lock 文件锁定。
纯 native 和普通结构查询不准备 Java；JADX/审计/后端验证仍保留 Java。DexSQL 二进制仍由固定 SHA 安装器校验，未跳过输入校验提速。

暂存 APK 命中仍核对完整大小和 SHA；Linux 冷暂存将复制与哈希合并到一个流，校验后才原子发布。分析结束的源 hash 不变门禁继续执行。
`job.json` 新增 preparation 和 phases：环境准备命中/重建、repo_info、manifest、SDK下载调用、校验、暂存、导入和分析耗时。
SDK下载调用也可能命中 Hub 本地缓存；entry_to_batch_ms 是覆盖层耗时，与其中 repo_info/manifest 不应重复相加。旧 fetch_ms/total_ms 字段保持原口径。

相同运行中请求会返回 `reused:true`。提供成对的准确 APK SHA-256 和不可变 sample_revision，可复用 24 小时内同一工具版本的结构化任务成功结果。
任意原始 SQL 可能包含时间、随机数等表达式，完成后不做自动结果缓存；显式幂等 key 仍可绑定调用者选择的同一执行。
显式 idempotency_key 绑定该请求（包含工具版本与样本选择）；同 key 改参数会拒绝，失败也不会偷偷重跑。
提交期间网络结果不明会返回 dispatch_unknown 和已有请求 ID，此时只查状态，不重新提交。
调度使用崩溃自动释放的 OS 锁；最多接纳 4 个可观察运行中或未确认提交。capacity_full/scheduler_busy 不分发新作业。
这是当前客户端与可观察 GitHub 队列的预算；多台客户端的竞争仍受 GitHub 实际调度约束。同一准确样本的批次在工作流中串行。
工作流显式使用 `queue: max`，避免 GitHub 默认单个 pending 槽将先前已接纳的请求替换取消；GitHub 同组最多保留 100 个 pending，客户端预算仍是 4。

工作流绑定 scheduler 选择的准确工具提交，并在 sample_revision/APK SHA 下取样。`job.json` 保存输入、工具哈希、请求摘要、后端版本和耗时。
结果附件仅包含有界结果和元数据；APK、DEX、SQLite 及原生缓存保留在 runner。仓库与附件可见性以 GitHub 当前权限为准。
旧 decompile/audit 路径和发布规则不变。

## 兼容性边界与验收

DexSQL 的 methods/fields 是引用表，class_methods/class_fields 才是定义。file_id 顺序、LIKE 下划线、MUTF-8/文本排序与 SQLite 存在差异，不能直接替换任意旧 SQL。
旧 code_size 是 16 位 code units，对应 code_items.insns_size，不能映射到 opcode_count。
method_calls 只表示静态调用引用，不自动证明接口最终分派；引用方法身份与完整 offset/op 调用点格式分开。
MCP 复用内存数据集，`.dxc2` 磁盘缓存属于原生 CLI，当前批量执行不伪称重开命中磁盘缓存。

## 多版本 Hook 候选与结构发现

使用 `plan_version_matrix` / `submit_version_matrix` 规划或启动同一功能跨版本的调查；
`advance_version_matrix` 刷新状态并补充待运行样本，`version_matrix_status` 只刷新而不启动新任务，
`version_matrix_result` 收集并比较候选。远程客户端共提供 11 项工具。

每个 selector 必须来自 inventory.json：

```python
samples = [{"version_code": row["version_code"], "apk_sha256": row["sha256"],
            "sample_revision": inventory["sample_revision"]} for row in selected_samples]
```

最多 40 个准确样本、并发 1–4。矩阵只捕获一次不可变工具提交，之后即使 main 更新也不会混用不同分析代码。
本地待运行状态 queued_local 与 GitHub pending 分开计数；每次 advance 最多接纳两个，容量不足仍保留队列。
条目在分发前保存稳定重试键，客户端崩溃后即使作业已经快速完成也不会重复付费执行。失败和未知结果不自动重跑。
显式 idempotency_key 绑定同一矩阵；定义、样本或工具绑定异常时拒绝推进。

默认可以复用同日同一工具/准确样本/结构化任务的结果；原始 SQL 不做隐式完成缓存。
`reuse_completed=false` 用于冷负载比较：新矩阵会真实创建新作业，仍保持同一矩阵内重试的幂等性。
这不是后台定时器；调用方停止 advance 就不会继续提交。deadline_seconds 只停止尚未接纳的条目，已接纳作业继续结算，不自动取消。

结果每次最多收集 8 个版本；跟随 next_offset 读取下一页。比较完整 descriptor 和重复次数，保留每版精确 APK、工具提交和原始 DEX provenance，
不把数字 file_id 或 DEX 重排当成 Hook 变化。SQL 显式输出 descriptor 列时也可进入候选对比；长预览标记截断并指向完整本地文件。

[examples/comment-search-links.json](examples/comment-search-links.json) 是与实际评论搜索链接适配契约对应的 15 项工作负载：
Map getter/URL schema getter 候选、调用/字段/类型消费者、Smali、Manifest，以及结构发现和布局展开查询。
其中 protobuf 形状查询不预设类名，返回类型查询从真实消费者推导数据结构并展开字段布局；KMP 模型查询发现已知命名空间内的新增顶层 RichText 结构。
结构属性与布局会单独计算语义哈希，排除 file_id 重排；长布局保留哈希和显式截断预览，完整数据仍在原始结果文件。
它们产出静态候选及版本差异，不能直接升级为唯一可用 Hook 或设备验收。

### 有界附件收集与恢复

`version_matrix_result(..., download_parallel=4)` 默认最多四路收集，可调 1–4，分析作业并发与附件下载并发分别约束。
同一进程最多四个收集调用、合计最多四个实际附件下载；容量等待有 60 秒期限，不无限创建工作线程。
矩阵保存成功运行的 attempt/commit 快照，收集无需逐版查询长期报告和运行状态；旧矩阵仍兼容，缺失快照时查询原 run。

首次下载按 GitHub artifact 元数据核对 ZIP 的 SHA-256、大小、运行 ID/commit，再校验 ZIP CRC、成员路径和展开预算。
缓存绑定 repository/request/run/attempt/head SHA，每次复用重新核对完整文件清单、大小和 SHA-256，不信任旧 `.downloaded` 标记。
同一附件的并发请求由 OS 锁合并，进程崩溃后锁自动释放；热缓存的完整性校验不需要网络或独占锁。
单归档至多 64 MiB、展开至多 128 MiB/4096 项、单文件至多 32 MiB，拒绝 APK/DEX/程序/数据库及越界、链接和重复路径。

下载和解包在独立临时目录完成，全部校验成功才原子发布新代次和回执；中断及损坏不会被标记完成，也不覆盖旧证据。
每个调用返回独立的比较快照；局部下载失败保留成功附件，`all_analysis_complete=false` 和 `collection_errors` 明确报告，重试同一页只恢复缺失/损坏内容。
基准附件收集失败时不临时换另一个版本当基准。原 `job_result` 的 Unicode 分页与长期报告优先规则保持兼容。

较大矩阵可在补满分析槽后调用 `version_matrix_result(..., prefetch_only=true)`，按 offset/next_offset 分页预取已完成条目的附件。
它只下载和校验，不提交作业、不等待未完成条目、不输出候选比较；调用方可与后续 advance 重叠执行，最多保留一个预取调用即可。
记录已预取 sample_id，只有新的完成条目或需要恢复失败时再预取对应页，避免高频轮询。
最终仍需所有版本结束后用默认 prefetch_only=false 收齐每页和完整性结论，不能把预取成功当成矩阵完成。

开发验收：

```powershell
tools/hostlab/.venv/Scripts/python.exe -m unittest discover -s tools/hostlab -p "test_*.py" -v
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/verify_backends.py --version-code 9150200 --output runtime/hostlab/verification --rounds 2 --jadx
```

Actions 的 backend_validation 操作用准确 runner_revision、样本 revision/SHA，对比类/方法/字段/四类引用集合、Manifest、Smali 和保留的 JADX CLI。
验证缓存位于附件目录之外，附件仅保存计时、计数、结果身份哈希和结论。静态验证不能替代 Android Hook／设备验收。
