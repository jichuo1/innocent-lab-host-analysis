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

## 结构审计与多路径扫描

`analyze.py audit --backend dexsql` 使用 runner 内固定哈希的原生 CLI；`--backend legacy`
保留原 JADX 结构审计与 Androguard 多路径扫描，`--backend auto` 优先原生，只在不可用或明确不支持时回退。
默认策略为 auto，优先 DexSQL。`HOSTLAB_AUDIT_BACKEND` 可显式选择策略，报告记录实际后端及回退原因。
云端用户继续提交现有 audit/multipath_audit，不需要在本地安装 CLI，也不需要重载共享 MCP。

原生路径复用同一份家族、页面和协议规则；27 项 FEATURE、DISCOVERY、父类/接口、泛型 Signature、
字符串引用、真实调用边、调用次数、协议双路径、未知调用者、原始方法体和资源指纹都保留。
LIKE 仅作候选预过滤，最终分类保持原来的大小写规则；file_id 映射回旧报告的数字 DEX 顺序。
方法体按旧描述符顺序排序后，对同一份原始 DEX 指令字节计算哈希。
JADX CLI 仍供单类伪源码与后续语义复核，Java 保留用于必要的回退；原生结构路径不启动 JVM。

内部批量提取使用一个 `query --interactive` 进程，SQL 投影用无损 hex 单元格和独立结束标记，
区分 null/空串并保留 Unicode、控制字符与大整数。SQL 256 KiB、单行 4 MiB、单次传输512 MiB、
解码结果默认128 MiB/500000行均为硬上限；特定调用边查询有显式有界额度，超限一律失败，不截断伪装完成。
共享总时限覆盖准备、写入和读取，异常终止自有进程树。外部 MCP 的分页与返回格式不变。
输入 SHA 前后重验、完整物理 DEX 清单、原有 intake 漂移/home-frame/FEATURE 门禁继续执行。
重复定义、未知泛型外部类语义或 DEX041 原始指纹等明确未等价形态走有原因的旧实现回退；
未知运行错误、超时、损坏结果均失败，不以换后端隐藏问题。

云端 `backend_validation` 的 `argument={"audit":true,"rounds":2}` 配合准确的目标 SHA、基线 SHA、
sample_revision 和 runner_revision，串行双跑两个 APK，交替先后顺序，逐字段比较完整证据多重集。
它还比较跨版本变化/资源差异/审计结论，并保存各轮耗时、内存采样及源码哈希。
验证不调用付费 AI，不把 APK、DEX 或反编译目录上传为产物；仅全部证据一致后才能切换默认策略。

2026-10-24 [云端两轮完整双跑](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/40061414146)
在候选 `e4ab3d1af6a13f40695f4be37bfd66f88c5b4c02` 上完成，输入固定于
sample revision `1c744580ec53f13d57339e162246945e5004e577`。
目标 `9170100/f0f880e841d017db335b3919e6d4792961f2e08aa9993da661b626d52cfcb955` 与
基线 `9161100/41efb1c9acb07badab5296953fb3da1def6925e2b34662120ca96df9d17bbfb2`
各轮20类完整证据均一致，跨版本103项变化、资源差异及结论也一致，源码哈希结束重验成立。

| APK | 旧实现耗时中位数 | 原生耗时中位数 | 耗时减少 | 旧进程树 RSS 采样峰值 | 原生采样峰值 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 9170100 | 163.98 s | 105.87 s | 35.4% | 6996–7175 MiB | 1261–1266 MiB |
| 9161100 | 150.67 s | 94.44 s | 37.3% | 6661–6782 MiB | 1187–1196 MiB |

这些是同一 Linux runner、每后端/样本两轮新进程、交替顺序、保留 OS 文件缓存的完整静态门禁与扫描测量；
样本下载在分析计时外，采样 RSS 不是内核记录的真实瞬时峰值。静态结果仍为 REVIEW_REQUIRED，运行期未知。

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
| query | sql, dialect, limit, offset, 可选 pagination | dialect 默认 sqlite；DexSQL SQL 显式声明 dexsql；不改写 SQL |
| locate | kind=class/method/field, name, 可选 owner | 查定义；类的 name 是完整类型描述符 |
| refs | kind=string/method/field/type, target, detail | 默认 methods，保留引用重复次数；sites 保留旧 offset/op 并走 SQLite |
| decode | method, 可选 file_id | 完整方法描述符；file_id 只对本次 DexSQL 数据集有效 |
| info | 无 | Manifest；部分权限页仍标 partial |

`auto` 对结构化引用优先 DexSQL，对已有热索引的纯结构查询复用 SQLite；若本批已需原生后端且无强制旧任务，结构查询共享原生会话，避免多开。
原生不可用时只对等价的结构化操作回退。强制 dexsql 或 DexSQL SQL 不会被送入 SQLite。

批次返回逐项 `complete/partial/error/skipped`、会话准备成本、版本和计划原因。任何截断或错误都不会标成完整成功，CLI 返回 2。
失效数据集和未知结果不会自动重放；MCP SDK 负责 EOF、Windows Job Object／POSIX 进程组的关闭和终止升级。
结果总预算 2 MiB，按完整任务结果记账；原始 SQL/native typed result 保留整数精度及分页字段。

## 查询续页与断点恢复

DexSQL 批量 query 的 `limit` 是每页行数，默认在同一数据集中自动续页。每项默认总行数上限1000、每次执行最多8页、结果字节上限1 MiB，并共享原批次的总时限和2 MiB输出预算。可以显式传入 `pagination={"max_pages":8,"max_rows":1000,"max_bytes":1048576}`；硬范围分别为1–32、1–10000和1024–1048576。`max_pages=1` 保留单页行为；页数按每次恢复计算，行数/字节按累计结果计算。SQLite SQL仍按原请求执行，JADX路径不变。

续页要求调用者给出可复现的外层 `ORDER BY`，并选择唯一的排序键/消歧键；这是原生接口重执行 SQL 的契约，不能依赖未排序结果或随机值。缺少外层排序、游标不前进、模式或总行数变化、达到页数/行数/字节/后端offset预算时，仍返回 partial 和明确 `stop_reason`、`next_offset`，不伪装完整。空结果成功、整数精度、重复行、长SQL元数据缩略与原SQL保持兼容。原生范围仍为offset+limit不超过100000。

每个已接纳页面和完成任务会原子更新 `remote-output/checkpoint.json`。正常结束、受控超时和后端失败后仍执行源校验，只有最终APK SHA-256/DEX清单校验成立才封存检查点；进程被强制杀死而未封存、产物过期或校验失败的检查点不会被信任，也不会回退成全量重跑。

检查点schema 2在签名前将对象键规范化为JSON字符串，避免多DEX数字file_id键在往返序列化后改变排序。旧schema 1只为已审计的写入器哈希复现其数字file_id排序算法，仍核对原GitHub附件摘要和原封存摘要，不改写旧记录。已完成任务的结果内容保持原始哈希；当前执行的新增行数/开集次数单独记账，避免把历史分页统计误算成新工作。

恢复时向原请求添加 `"resume":{"run_id":原run,"attempt":原attempt,"request_id":"原32位request_id"}`，通过 `submit_analysis` 传入准确的 `apk_sha256` 和 `sample_revision`。服务端验证同仓Actions的run/attempt、ZIP摘要与文件摘要、样本/请求身份、固定原生版本和兼容核心工具，再保留完成任务内容并从最后接纳的游标续取。仅支持单样本batch，分组版本仍使用原版本恢复机制。普通SQL完成结果仍不作为新任务缓存；这里是显式恢复同一个不可变工作请求。

恢复提交默认使用稳定幂等键，未知派发和重复调用不重放；确认失败后要再次执行，需显式提供新的 `idempotency_key`。旧schema-1检查点只兼容已审计的工具哈希，后续检查点要求封存摘要及batch契约版本一致。原运行及其11项/其它已完成结果继续保留，不覆盖旧产物。

Actions摘要逐项列出完成状态、返回/总行数、复用/新取行数、下一游标与停止原因；`job.json`保留原工作摘要并增加执行请求摘要和契约版本。恢复的结果包含原run/attempt与附件摘要，可独立复核实际复用了哪些数据。所有受信文件都在上传的有界产物内，仍不包含APK、DEX、数据库或凭据。

已知返回 output_too_large 时，只对尚未接纳的当前页有界减小行数；最小为1行，超时、未知传输错误或已关闭数据集不自动重试。每任务最多10次缩页，沿用同一总时限；接纳页、缩页后的上限和本轮缩页次数写入分页元数据。单行仍超限时保留失败，需调用者显式用 substr() 拆值。

明确属于单条只读SQL的 invalid_query / invalid_input / impl_defined / output_too_large 错误不会使仍有效的会话跳过其他独立任务；原错误仍保留，整批仍不算完整。未知错误与失效会话保持停止。

从分组作业恢复单个成员时，在 resume 中增加 sample_index=0..11；新任务仍是单样本 batch，校验原组、成员索引、准确样本、请求、工具与封存检查点。完成任务和已接纳行复用，仅补剩余游标；原1 MiB任务可在新的2 MiB批量总预算内继续，每项查询自己声明的max_bytes上限保持不变。检查点与结果使用紧凑JSON写入，避免格式化空白挤占附件边界。

DexSQL 0.1.0的 method_calls 调用者列是 method，目标列是 callee；先用 SELECT * FROM method_calls LIMIT 0 读取实际列定义。分组后排序应显式投影排序键，例如 SELECT f,o,n/8 AS bucket,... GROUP BY f,o,n/8 ORDER BY o,bucket,f。VALUES 派生表不接受 chunks(n) 这种列别名列表，可显式 SELECT column1 AS n FROM (VALUES(0),(1))。客户端不会自动改写原始SQL或切换其方言。

## 远端工具

更新远程客户端并重新加载 MCP 后，旧四个工具继续存在，并提供单样本和版本矩阵工具：

- `plan_analysis(request)`：只规划，不分发作业。计划中的 native 可用性在 runner 执行前验证。
- `submit_analysis(version_code, request, apk_sha256="", sample_revision="", idempotency_key="")`：一批共用一次样本下载和每后端一次准备。

先把示例对象传给 plan，再传给 submit；后续仍用返回的 request_id 调用 `job_status` 和分页 `job_result`。
强制纯 DexSQL 批次只安装既有依赖的 MCP/Hugging Face 子集，省去 Androguard。安装失败或后端错误不伪装成成功。

Actions 将已安装依赖保存在独立的 `runtime/hostlab-prepared` 隔离环境，使用精确 Python/ABI、OS/架构、runner image、工作区路径、requirements 与准备器源码摘要定位缓存。
恢复后先校验完整文件/目录/链接清单和 SHA-256，再启动解释器验证环境绑定、顶层固定版本及完整已安装版本清单；损坏或失配时重建。
冷安装使用既有 pip 管理无 pip 的 venv，完成依赖检查才发布回执；缓存只保存依赖，在样本步骤之前完成保存，不包含 HF_HOME、APK/DEX、报告或认证文件。
依赖以当前精确解释器预编译为校验源哈希的字节码，源文件和字节码都进入完整性清单；正常执行不再反复编译依赖。
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
`version_matrix_result` 收集并比较候选。远程客户端共提供 12 项工具，包括显式失败恢复。

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

### 同一 runner 复用多版本环境

`plan_version_matrix` 和 `submit_version_matrix` 可传 `runner_batch_size=1..4`，默认 1，旧客户端与已保存矩阵继续使用原路径。
例如 `submit_version_matrix(samples=samples, request=request, runner_batch_size=4, max_parallel=4)`：每个物理 runner 最多处理四个版本，最多同时接纳四个 runner；34 版最多需要九个新作业。
分组、准确样本、请求、工具提交及重试键在首次派发前固化。更改分组参数需要新矩阵，不可改变旧矩阵的身份。

一个 runner 只准备一次依赖环境、验证一次私有仓库，并按不可变 revision 复用 manifest。
输入准备使用最多两个下载工作线程和滑动窗口，下载完成的版本先分析；分析期间继续预取后续样本，避免输入顺序让已就绪版本等待较慢下载。
每个版本仍独立验证 manifest 路径、size、完整 SHA-256 与分析后源 SHA，使用全新的后端会话，分析本身在一个 runner 内串行执行以控制内存。
HF/Xet 连接池在进程内复用，不将私有 APK、HF_HOME 或令牌保存到公开依赖缓存。下载线程不能安全强杀；最终进程期限仍由 Actions 作业限定。

组结果包含 `group.json` 与 `samples/<组内索引>/job.json,result.txt`；每版保留原 batch 身份及组内索引。
`job_result` 对组请求默认返回组回执与全部文件路径；加 `sample_index` 可独立读取成功或失败成员的输出（固定组0..3、自适应组0..11），继续支持 `result_offset` 的 Unicode 分页。
每完成一版即原子更新检查点，成员失败继续处理其它版本，附件步骤始终运行。
Actions conclusion 只描述物理作业；矩阵先校验组回执与逐版元数据，才接受逐版 complete/failed/skipped。
收集临时失败保留 `awaiting_results` 并重读同一附件，不重复派发；组作业失败也可取回其已完成成员。
同轮完成组最多四路并行收集，只有主线程验证、合并和保存矩阵状态。
`physical_inflight` 表示正在占用的 runner，成员状态数可以大于此值。一个组的多版结果复用同一份已验证附件下载。

`recover_version_matrix(matrix_id, idempotency_key="")` 是显式启动恢复的入口，只重跑原矩阵已确认 failed/skipped 成员，保留原工具提交、请求及分组参数。
已成功成员不会重跑，未知派发和仍在执行的成员不进入恢复队列。默认恢复键重入同一恢复矩阵；如果恢复本身再次失败，有意再次执行时使用新的显式键。
附件缺失或身份不符不能伪装为成功，也不自动变成新的付费作业。deadline 只停止尚未派发的组；已接受作业不自动取消。
若物理作业已明确结束而附件永久丢失，可显式设置 `include_unverified_results=true` 创建恢复队列；原结果继续标记不可验收。
这会有意重新执行已结束但无法验证的成员，可能重复其计算；默认关闭，且从不包含仍运行或派发结果未知的成员。
任意旧 SQLite SQL 方言、自动选择/回退规则及 JADX CLI 继续按既有契约执行。

### 可选自适应分组与资源反馈

`plan_version_matrix(..., execution_policy="adaptive")` 只给无网络、无缓存读取的冷规划；`submit_version_matrix(..., execution_policy="adaptive")` 才捕获不可变工具提交与性能快照。
自适应模式不同时设置固定 `runner_batch_size`，其默认值保持1；普通调用仍为 `execution_policy="fixed"`。
例如原生34版可先规划为四组8–9版，最多同时四个runner；旧固定4版路径仍可用于对照或回退。

分组采用有边界的成本平衡启发式。成本来自相同工具提交、规范化请求指纹、准确APK SHA的已验证结果；记录取样、分析耗时和可信输入大小。
未命中时按样本数稳定平衡，未知大小不冒充准确大小。原生组最多12版，SQLite/auto组最多4版；请求30,000字节、已知输入合计4 GiB及预测期限继续约束，无法容纳时增加后续组，保留全部样本。
模型是性能提示，不能替代manifest、完整性或结果验收。schema3固化规划器版本、成本快照/哈希和拓扑；已接受或未知派发的组不再重新分配。
升级算法应新增planner_version并保留旧版本加载分支。默认fixed的schema1/2、定义哈希和幂等键继续兼容。

自适应一次最多补满四个空物理槽，串行POST仍经过全局接纳锁、派发前回执与稳定键；fixed保留每次两次派发的行为。
并行附件收集、逐版检查点和显式恢复继续生效。恢复固定原工具提交及执行策略，不自动重放未知派发。

runner的自适应预取在1–2路间调整，仅影响尚未开始的准备。按取样/处理耗时EWMA、准备队列等待、CPU、内存和I/O压力收缩，经过冷却与低压采样后再扩展；处理阶段对新预取接纳限为一路，现有下载自然排空。
磁盘接纳保留输入复制与下载空间，并为在途准备留预算。每版仍独立后端会话，原生分析保持串行。
未修改未文档化的Xet内部参数，也不通过取消Future声称已经终止原生传输。

fixed与adaptive均采用相同的stdlib资源采样器，默认0.5秒间隔、最多7200条、1 MiB资源附件；不支持的字段为null。
记录的CPU范围、cgroup范围、系统接口网络计数与采样进程树RSS分别标明；采样RSS峰值不等于连续真实峰值，系统指标也不能冒充该分析独占用量。
`resources.json` 保存有界时间轴，`group.json` 保存摘要与有界决策；纯分析起止另在每版job.phases记录，避免将processing中的导入/报告时间当作纯分析。
遥测不可用或记录失败不改变APK语义结果；压力未知时保守接纳，磁盘不足/期限触及时明确保留未开始成员。

客户端性能缓存位于 `runtime/hostlab/scheduling-profiles`，最多256条/1 MiB，OS锁下原子合并，只是可丢弃的性能提示。
重复矩阵键优先恢复原计划，不因新观察记录或main变化而改写拓扑。基准测试可把校准记录复制为该目录的普通 `frozen-*.json`，通过本地环境变量 `HOSTLAB_SCHEDULING_PROFILE` 固定读取；快照路径只允许该专用目录，哈希写入规划，观察器不会覆盖冻结文件。
多轮对照应固定同一快照和准确样本、请求及工具提交，交错试验顺序，保留失败分母，并分别报告完整交付墙钟、累计作业成本与资源观测。

### 调度状态与运行身份

workflow 派发显式请求 GitHub API `2026-03-10`，可返回运行 ID 时立即保存映射，减少提交后的发现往返；旧服务空响应继续兼容。POST 前先落稳定 request ID，网络异常或无法确认的响应返回 `dispatch_unknown` 与原 ID，不自动重发；后续 `job_status` 可由回执中的 run ID 恢复映射。
同一 run、同一 attempt 的较旧 API 状态不会把已完成任务改回 pending，也不会继续占用空槽；明确增加的 run_attempt 会重新纳入并发预算。无法确认 attempt 或状态的冲突保守占位并返回 `status_unconfirmed`。全局四槽与串行派发边界保持生效。
