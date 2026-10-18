# 仅远程分析客户端

解压到项目根，使文件位于 tools/hostlab。需要 Python 3.13 和 GitHub CLI。
运行环境在 tools/hostlab/.venv-remote，结果与配置在 runtime/hostlab；不使用项目临时目录。
分析服务仓库为 jichuo1/innocent-lab-host-analysis；触发权限由管理员配置。
触发任务需要 Actions write 权限；使用你自己的 gh auth login，不共享管理员凭据。
Windows 双击 setup-remote.cmd；若装有 Codex CLI，会注册 hostlab-remote。
其它 AI 客户端：command 填独立环境 python 的绝对路径，args 只填 remote_mcp.py 的绝对路径。
重新加载客户端或开启新会话后查看可用 MCP 工具，旧四个入口保持兼容。

- submit_job(9140200, "query", "SELECT file_id,class,name,proto FROM methods WHERE name='getUrlsMap'")
- job_status(返回的 request_id)
- job_result(同一 request_id)
- list_jobs()

长单元格查询可以调用 `submit_job(version_code=9140200, operation="query", argument="SELECT file_id,class,name,proto FROM methods WHERE name='getUrlsMap'", max_cell_chars=3000)`。
默认仍为 300；可调范围 1–16000，仅适用于 query。截断提示区分单元格、行数和总输出上限，索引中的完整值不受影响。
更长的值用同一宿主样本及稳定键读取 `length(value)`、`substr(value,1,8000)`、`substr(value,8001,8000)` 等，并设置 `max_cell_chars=16000`，避免控制字符转义挤掉尾部。
SQLite `substr` 的起点从 1 开始；按返回的实际 sample_revision/apk_sha256 检查各段来自同一份样本。

远程 `result.txt` 每次返回 8000 个 Unicode 字符，`job_result` 新增 `result_page` 元数据：
首次用 `job_result(request_id)`；若 `result_page.next_offset` 非空，将该值作为 `job_result(request_id, result_offset=该值)` 继续读取，直到游标为空。
结果页位于 `text` 开头，在 `result_page.file + 换行` 之后，长度为 `result_page.chars`；其余内容是相关文件的摘要。
`result_offset` 从 0 开始，按字符计数，不按 UTF-8 字节计数；读取后续页复用已下载的结果，不再启动 Actions 分析。
`text_truncated` 明确标记是否仍有未显示的结果或其它文件内容；返回的本地文件路径可读取完整结果。
长期多路径报告继续返回 reports 分支和文件入口，`result_offset` 只用于结果附件中的 `result.txt`。

## 模块源码快照

完整分析与普通 DEX 查询分别处理。`multipath_audit` 提交前会在有生产目录的本地项目中捕获工作树，
包含范围内未提交和新增源码；没有生产目录的远程客户端会读取最近发布快照的元数据。
两者都把不可变私有存储 revision、payload SHA-256、源码树 SHA-256 和捕获时间绑定进任务。
APK 的 `source_revision` 仍指 APK 数据集，不是模块源码 revision。

源码全文保存于已验证可访问的私有 `innocent-lab-dev/bilibili-host-apks` 数据集的 `source-snapshots/` 独立目录。
源码写入不会改动 APK manifest 或已有样本字节；模块源码 revision 与 APK revision 分别记录。公开状态、报告和索引只包含
来源元数据与文件哈希，缺失、损坏或未校验的快照不会回退到旧 `production-context.json`。
普通 `query/info/decode/string_refs` 不捕获或上传源码。远程客户端使用 published 模式不需要 HF 凭据；
本地 worktree 模式使用已登录的完整工具环境（既有 `huggingface_hub`），上传前执行明确的令牌/私钥门禁。
相同源码 HEAD、选择规则、完整文件树和工作树状态可复用已验真的不可变源码快照；保留原捕获时间，每次仍重新捕获、执行秘密门禁、核 payload SHA 并再次核对源码。受限本地索引仅含元数据，OS 锁将同工作区并发准备合为一次，等待最多 120 秒；失配/损坏恢复到正常发布，锁忙不会绕过保护重复上传。

可通过 `source_mode="worktree"` 要求存在本地源码，通过 `source_mode="published"` 指定最近发布的来源；
默认 `auto` 自动选择。`regenerate_ai` 默认重用原报告历史源码，显式 source_mode 才使用新源码审查，
并保留原始静态证据 run；它不表示重新扫描 APK。

`job_result` 返回独立 `source_freshness`：`current`、`drift`、`unavailable` 或 `legacy`，以及变化文件列表。
这是与调用方当前项目的比较，不改写历史报告。只有本地完整生产树能确认 current；远端 recently published
来源仍明确标注 published，不能声称观察到了桌面的最新工作树。

客户端更新后需重载 MCP 服务或开启新会话，才能使用提交前的自动捕获；服务端默认发布源读取仍独立生效。

operation: info / query / decode / string_refs / decompile / audit / multipath_audit / regenerate_ai。
新 APK 自动报告与 multipath_audit 包含有界 AI 分析；AI 建议不能替代真机验收。
全部登记页面证据由服务端预取（零 API 成本）；AI 先出详细逐路径草稿，再在同一模型的独立上下文中复核重点页面和全部草稿发现；评论与动态由服务端重新读取、复核记录引用其编号。
草稿按最多两个页面分片、最多六个单元，再用独立上下文逐片复核重点页面与全部发现。全流程最多 16 次 API 请求（含探索、修正、失败和最多两次传输补偿），跨恢复任务累计；每次最多 8192 输出 token、240 秒墙钟时限、45 秒读空闲时限，AI 累计限时 30 分钟。逐页面/路径校验与评论、动态新读取证据要求保持生效，复核未完成不发布成功 Release。

SSE 传输封装与实际内容分开限额：默认原始流最多 8 MiB，按输出档位增加且硬限 32 MiB；拼接文本/工具字段合计仍限 2 MiB，最多 65536 个数据事件。单行/事件、工具参数、JSON 回退与传输子进程输出继续独立校验。曾被旧 2 MiB SSE 封装上限中断的默认任务，可在修复传输实现后显式使用 `extended-v1`；仅精确匹配该历史错误及其边界指标才允许迁移，原失败、未知计费和时间完整保留，补偿照常计数。其他格式/大小错误不会获得自动重试许可。

正式调用和探测统一接受 Chat Completions 根地址或完整 `/chat/completions` 地址，`/messages`、`/responses` 不能冒充该协议。官方 OpenAI 使用 `max_completion_tokens`，其他兼容端默认 `max_tokens`；需要显式字段时设置仓库变量 `AI_PRIMARY_OUTPUT_TOKEN_PARAMETER` / `AI_BACKUP_OUTPUT_TOKEN_PARAMETER`，仅允许这两个值，并计入恢复绑定。每条回复最多八个工具调用，公开回复账本最多128 KiB；超额明确停止，不静默丢弃工具。完整 usage 即使在后处理失败时也保留，已收到但不能入账本的回复记录摘要与已知用量，不伪装成未知 POST。
`regenerate_ai` 支持旧数字 run ID，也支持 JSON `{"static_run":原始静态runID,"checkpoint_run":检查点runID,"resume_unknown":false}`。恢复保留目标、基线、规则、矩阵和原 run 身份；仅重新绑定明确指定的源码快照并执行 AI。它不准备 Java/JADX、不下载或扫描 APK，模型不提供 decompile_class。检查点中的成功响应复用，静态/源码/提示/工具/提供商配置漂移则拒绝复用；请求结果不明时默认禁止重放，显式授权仍保留未知计费和已用预算。
每次请求先持久化账本，连续两次提供商失败熔断 60 秒。公开检查点只保存请求哈希、调用状态、用量和结构化结果，不包含源码正文或请求消息。未知用量不计作零。
启用 fallback 时，主通道 401/403 仅尝试一次已配置的独立备用凭据；不会重复原认证失败请求，备用拒绝时停止。该切换也消耗两次全局补偿额度，初始通道与 fallback 策略绑定进检查点。
`checkpoint_run` 恢复在未显式指定源码时固定采用该检查点源码，不再依赖原静态报告的旧源码或移动的最新指针。遇到经过验证的草稿分片而默认预算不足，可显式加入 `"recovery_policy":"extended-v1"`：在旧账务基础上将恢复链总限设为 24 次请求、4 次补偿、每次 16384 输出，累计期限仍为 30 分钟；默认任务上限不变。导入草稿必须重新通过完整校验，历史调用不删除，独立复核全部保留。

已完成全部草稿及至少一组独立复核的 `extended-v1` 检查点，可显式选择 `"recovery_policy":"completion-v2"` 继续剩余复核。新累计上限固定为 32 次请求、4 次补偿和 60 分钟，原有时间、补偿、调用和未知计费全部保留；导入的复核仍按原始新鲜读取边界重验。同策略重启验证完整父历史与新增证据，不重跑已完成单元或 APK。此策略需要明确的 checkpoint_run，不能从旧报告隐式继承。

已完成更多复核、但长推理超过原 240 秒请求期限的 v2 检查点，可显式进入 `completion-v3`。它从已知成功输出吞吐估算 360–600 秒有界时限，累计硬限 40 请求/6 补偿/80 分钟，并保留全部旧账和 `ai-final-*` 父证据。默认/v1/v2 不变，不降低输出或复核要求；零/缺失/未知 usage 不会被当作速度样本。
reports 分支保存可浏览结论，私有 Release 只保存完整成功分析的证据；失败只保留报告记录。MCP 取结果优先访问长期报告。
不需要 HF Token、APK、JDK、JADX 或 Android SDK。只会下载报告和有界分析结果。
计算在 GitHub Actions Runner；分析 job 最多 45 分钟，发布 job 最多 15 分钟。Actions 附件保留 14 天，仓库报告和 Release 不按这个期限清理。
静态证据不能替代真机验收。Actions 消耗仓库拥有者的分钟及产物额度。
本地 stdio 网关不是公开 HTTP 服务；ChatGPT 网页的远程 HTTP 接入未配置。
# Read-only sample inventory

Call `submit_job(version_code=1, operation="inventory")`, then use `job_status` and `job_result` as usual. The version code is a required placeholder and does not select an APK. The `inventory.json` artifact lists every registered sample at one immutable sample revision, exposing only version, SHA-256, size, and certificate metadata. No APK or DEX is downloaded for this operation.

## 批量计划与可选 DexSQL

更新并重新加载 MCP 后有十二项工具，包括单样本 plan/submit、多版本 plan/submit/advance/status/result 和显式恢复。
相关查询一批共用一次下载与后端会话，保留 SQLite 方言和 JADX 路径。完整请求示例、去重/未知提交行为与限额见 [DEXSQL.md](DEXSQL.md)。

DexSQL query会在页数、行数、字节及原总时限内自动续页。显式恢复可在原request添加
`resume={"run_id":原run,"attempt":原attempt,"request_id":"原32位request_id"}`，再向
`submit_analysis`提供原APK SHA及sample revision。已验真的完成任务不重跑，部分查询只取剩余页面；
恢复默认绑定稳定幂等键，确认失败后再次执行需要新键。旧客户端普通请求继续兼容；显式恢复参数和分页预算需要更新客户端并重新加载MCP。契约、排序要求及封存规则见 [DEXSQL.md](DEXSQL.md#查询续页与断点恢复)。

`version_matrix_result` 默认四路附件收集，`download_parallel` 可设 1–4；多个调用也共享下载预算。
已验证的附件复用本地文件，分页不重复下载；首次校验 GitHub ZIP SHA-256，复用前重新校验文件 SHA-256。
`collection_errors` 表示局部收集未完成，可重试相同 matrix_id/offset；已成功文件保留，不创建新的 Actions 作业。
较大矩阵可在分析槽补满后用 `prefetch_only=true` 分页预取已完成条目，与后续分析重叠；最终用默认参数收齐每页完整比较。

多版本任务可选 `runner_batch_size=4`，让同一 runner 复用环境处理最多四版；默认 1 保持原调度路径。
`max_parallel=4` 约束物理 runner；一个 runner 内最多两路取样预取、逐版串行分析，输出按固定输入索引隔离。
每版完整 SHA 与分析后源校验保留，部分失败仍收回其它成员。组附件只下载一次并逐次复验。
`recover_version_matrix(matrix_id)` 显式重试已确认失败/未开始成员，保留原工具提交且不重跑成功成员；未知派发不自动重试。
详细状态与恢复键规则见 [DEXSQL.md](DEXSQL.md)。

可选 `execution_policy="adaptive"` 会按验证过的成本记录平衡分组，并让runner在1–2路间有界调整预取。
原生组最多12版、SQLite/auto最多4版，物理runner总预算仍为4；不要同时指定固定runner_batch_size。
默认fixed保留原路径。纯规划不读网络或性能缓存；提交时才固定工具提交、成本快照和分组，之后不改写已派发组。
两种模式都记录相同的有界资源观测；`job_result(sample_index=0..11)` 可读取自适应组中的独立成员。
