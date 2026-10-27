# 私有宿主 APK 共享与离线分析工具

固定目录：源码及环境 `tools/hostlab/`（`.venv` / `.venv-remote`），配置、缓存及报告 `runtime/hostlab/`，分享压缩包 `artifacts/hostlab/`。

工具支持按需取包、混淆漂移检查、27 项 FEATURE 结构审计、新首页框架探针、报告对比及指定类反编译。静态审计通过不能代替设备验收。审计规则复用现有本地脚本，并非全部运行期功能覆盖。

## 首次配置

在仓库根运行：

```powershell
python -m venv tools/hostlab/.venv
tools/hostlab/.venv/Scripts/python.exe -m pip install -r tools/hostlab/requirements.txt
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py login
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py configure 组织名/仓库名
```

登录时 Token 在终端隐藏输入，不发到聊天，不放入源码。朋友使用自己的只读 Token。
账号须已经有私有仓库访问权。配置命令拒绝公开仓库。
SDK 凭据保存在用户级标准 Hugging Face 缓存；项目配置只保存仓库 ID。

## 使用

本机快捷上传：将一个或多个 APK 拖到 `tools/hostlab/upload-apk.cmd`。
也可以使用 `artifacts/hostlab/上传新APK.lnk`（本机快捷方式，绝对路径，不用于跨电脑分享）。
逐个校验并上传，失败最多重试三次；已发布哈希自动跳过，不要求更改 APK 文件名。
本机配置的代理可用时会使用它，端口关闭则回退默认线路；Xet 高性能模式保持启用。

```powershell
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py inventory Bilibili_Innocent_Lab
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py upload "APK的绝对路径"
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py list
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py fetch --version-code 9140200
```

同 versionCode 多样本时必须加 `--sha256 完整哈希`。复现时加 `--revision 完整仓库提交`。
清单不含原始本地路径；本机盘点结果存在被忽略的 `runtime/hostlab/`。
上传需 Android SDK 的 aapt/apksigner 及 Java，目前收包端面向 Windows；下载端无需 SDK。
下载得到的 APK 路径可交给原来的 `run_intake.py` / JADX CLI。
工具没有自动删除缓存、改仓库可见性、添加成员、启动付费 Jobs 的行为。

当前 `/tools` 被项目本地忽略；本工具尚未提交。跨电脑可只复制本目录。

## 朋友电脑

将 `hostlab-client.zip` 解压到朋友的仓库根，使工具位于 `tools/hostlab/`。
先由组织管理员把朋友的 Hugging Face 账号设为 read 成员。
朋友创建只读 Token，只勾选本样本库的读取权限，双击 `setup-client.cmd`。
之后 AI 可运行上述 `list` / `fetch` 命令，无需保存全部 APK。

工具包包含 JADX 1.5.6 JAR 及其许可证；完整审计需要 JDK 17+ 的 java/javac。
下载、列版本不需要 JDK。云端样本的分析不要求 Android SDK；本地 APK 身份核验及上传需要 SDK。

## AI 分析入口

```powershell
# 检查 Java、JADX、SDK；不自动安装系统软件
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py doctor
# 云端指定版本：下载校验后执行完整审计
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py audit --version-code 9140200
# 轻量检查：漂移和新首页探针，不要求 Java/JADX
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py audit --version-code 9140200 --mode basic
# 指定类反编译，只接受真实 DEX 类名，不使用 GUI
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py decompile --version-code 9140200 --class com.bapis.bilibili.main.community.reply.v1.Content
# 对比两份完整报告
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py compare --base "旧版summary.json路径" --target "新版summary.json路径"
# 离线使用本地 APK，无需 Hugging Face 登录
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/hostlab.py audit --apk "APK绝对路径"
```

输出位于 `runtime/hostlab/reports/<versionCode>/<hash>/<时间>/`。
包括 summary.json、features.tsv、intake.log、home-frame.log；反编译有 class.java 和 decompile.log。
报告记录样本身份、云端提交（若适用）、工具源码哈希和 JADX JAR 哈希。
审计源码是现有离线工具的快照，未自动同步生产 VersionAdapter；例如旧候选表 MISSING 不能单独证明当前 DexKit 兜底失效。发现问题后仍需核对生产定位器与实际语义。
intake 返回 1 可表示发现 MISSING/PARTIAL 等兼容性问题，查看日志，不应直接当作工具崩溃。
探针返回 0 仅表示执行成功，其结构观测见日志，不能直接当作兼容通过。
规则或 JADX 哈希不同时 compare 返回 2，仍输出差异，但不能把差异全归因于宿主。
超时默认 900 秒，可用 `--timeout` 设置 1–3600 秒。
历史接入清单在 analysis/HOST_INTAKE.md，旧版本数字只作历史参考。
未配置远程 Jobs/MCP，不产生付费计算；分析在调用方电脑执行。

Windows 也可以直接使用短命令 `tools\hostlab\hostlab.cmd audit --version-code 9140200`。

## dexq 结构快查

包含原有自建 dexq 的 server.py 和 dexq_workers.py；独立环境固定安装 androguard 4.1.4、mcp 2.2.0。
不要安装互联网上的同名 dexq 包。原始 `D:/Tools/dexq-mcp` 不受修改。
优先 dexq 查类/方法/字段/字符串和引用，再用 decompile 看 Java。

```powershell
tools\hostlab\hostlab.cmd dexq index --version-code 9140200
tools\hostlab\hostlab.cmd dexq query --version-code 9140200 --sql "SELECT file_id,class,name,proto FROM methods WHERE name='getUrlsMap'" --limit 20
tools\hostlab\hostlab.cmd dexq refs --version-code 9140200 --kind string --target disable_underline --limit 20
tools\hostlab\hostlab.cmd dexq decode --version-code 9140200 --method "Lcom/bapis/bilibili/main/community/reply/v1/Content;->getUrlsMap()Ljava/util/Map;"
tools\hostlab\hostlab.cmd dexq info --version-code 9140200
tools\hostlab\hostlab.cmd dexq tables --version-code 9140200
```

支持 `--apk` 本地输入或 `--revision` 固定云端提交。CLI 每次打开数据集，但会复用磁盘索引。
缓存放 `runtime/hostlab/dexq-cache`，不进压缩包；每个大宿主索引可能超过 1 GB。
同一 APK 的首次索引不要并发执行。SQL 只读、单条、60 秒限时，输出最多 1000 行。
查询默认每个单元格预览 300 个转义后的字符；截断只影响显示，索引保留原文，不需要重建。
需要长签名或字符串时加 `--max-cell-chars 3000`（范围 1–16000）；出现 `cell(s) truncated` 时不能把未显示的尾部当成不存在。
单次表格最多 64000 字符，只返回完整行；触及总上限时缩小 SELECT 列或用稳定排序分页。
超过 16000 字符的值按 `(file_id, string_idx)` 等稳定键分段读取：

```sql
SELECT file_id, string_idx, length(value) FROM strings WHERE file_id=0 AND string_idx=7;
SELECT substr(value,1,8000) FROM strings WHERE file_id=0 AND string_idx=7;
SELECT substr(value,8001,8000) FROM strings WHERE file_id=0 AND string_idx=7;
```

示例键需替换为实际查询所得。分段查询设 `--max-cell-chars 16000`；8000 原始字符可容纳制表符/换行转义后的扩展。
SQLite 的 `substr` 从 1 开始，分段后检查累计原始长度与 `length(value)` 一致。
refs 不解析接口分派/子类重写；decode 输出 smali 类文本，不是 Java。

可选 MCP 启动命令：

```powershell
tools\hostlab\hostlab.cmd dexq mcp
```

这是 stdio 服务，会等待 AI 客户端连接，不是网页。工具包不会自动修改任何 AI 客户端配置。
配置客户端时使用项目环境 python 的绝对路径作 command、hostlab.py 的绝对路径及 `dexq mcp` 作 args。
默认路径白名单仅项目根及 Hugging Face 缓存，原服务的只读 SQL/输出上限仍保留。

## 后续 GitHub Actions

推荐独立私有分析仓库，workflow_dispatch 接收版本、分析动作和有界参数。
Runner 使用只读 HF_TOKEN 从私有库取包，在 runner 上运行 dexq/audit/decompile，只上传报告、查询结果和指定代码。
不要将 APK/DEX/完整索引自动上传到公开仓库 artifact。
使用 env 传入 SQL/方法签名，再由 Python 构造参数列表，不能把用户输入直接插进 shell 命令。
每个任务只处理一个样本、限制 workers=2、设置 timeout；首次建索引按样本串行。
跨任务缓存要同时核对 APK SHA256、dexq schema 和工具源码哈希，不能只依赖版本名。
当前 dexq 索引使用路径/大小/mtime 做本机缓存键，尚未实现 Actions 跨机器缓存复用。
SQLite 索引可供只读 SQL 查询，但 decode/find_refs 仍需原 APK/DEX；不能把索引打包给朋友后声称完整离线查询不需要原包。
要让朋友完全不取 APK，应让这些操作也在 Actions 上执行，由客户端触发任务并取回结果。
远程实现见 remote_job.py / host-analysis.yml，MCP 网关见 remote_mcp.py。

## 远程 MCP 使用

分析仓库：`jichuo1/innocent-lab-host-analysis`，提交任务需要相应 Actions 权限；仓库与报告的实际可见性以 GitHub 设置为准，APK 保留在私有 Dataset 与 runner。
朋友使用远程分析时不需要 HF Token，也不用下载 APK；需要 GitHub CLI（gh）并完成自己的 `gh auth login`。
在 MCP 客户端配置中将 command 设为独立环境 python 的绝对路径，args 设为 remote_mcp.py 的绝对路径。
MCP 名称建议 `hostlab-remote`；不要与本地 dexq 服务混淆。

工具：submit_job(version_code, operation, argument)、job_status(request_id)、list_jobs()、job_result(request_id)。
operation 可选 info、query、decode、string_refs、decompile、audit；argument 分别为 SQL/方法签名/字符串/类名等。
query/decode/string_refs/info 可用 backend="sqlite"（默认，旧 schema）或 backend="dexsql"（原生关系）；单条命令不猜测 schema。
同一 payload 的确定性失败（SQL/参数被拒、行数/字节预算、类不存在）在 6 小时内不自动重派：submit 返回 replay_blocked，
修正后可显式 force=true / allow_replay=true 授权一次付费重跑。失败原因见 job.json 的 failure/retry_class/failure_reasons。
提交后返回 request_id，稍后查状态，完成后取结果。AI 不应把 submit 成功当成分析完成。
job_result 只下载结果附件，不下载 APK/DEX/完整索引；附件保留 14 天，过期需重跑。
当前没有跨任务索引缓存，每次任务重新取包并按需索引；先保证证据一致，再优化缓存。

## 自动收样与页面多路径机制

已部署 Automatic new APK intake，每半小时补查私有样本清单；GitHub 调度可能延迟，不保证实时。
上传工具成功发布新哈希后也会请求补查；没有 gh 或触发失败时，由云端补查兜底。
初始 28 个样本列在 bootstrap-samples.json，仅登记为基线，历史续传不会批量触发分析。
此后任何新增哈希都会检查，包含旧版本的新发行样本；同 versionCode 多样本由哈希区分。
任务固定 source_revision、apk_sha256、baseline_sha256，同签名谱系选择相邻低版本基线。
状态在私有分析仓库 intake-state 分支 .hostlab/intake-state.json；重复事件通过确定性 request_id 去重。

操作 multipath_audit：先跑现有 FEATURE 审计，再对目标和基线分别扫描全部 DEX。
矩阵登记评论、动态、首页、搜索、详情、影视、播放器、弹幕、Story、我的页。
各路径独立记录定义、Compose 形状、真实 invoke 边和 Java/Kotlin 协议，不能以一个路径通过覆盖另一个。
未知子模块、未归类协议调用者及源码中的未映射多路径候选都输出待复核，不静默排除。
并扫描未登记的 com.bapis *Moss 协议，自动识别 Java/Kotlin 双通道，不仅依赖已知 14 条入口。
相关家族的方法体指纹与 APK XML/资源表指纹也参与变化发现；DEX 重排和资源 ID 变化可能造成候选差异。
原生资源差异目前是全局范围，不能自动归因到某个页面，更不能把资源条目数当成新样式数量。
源码证据来自 production-context.json 的固定文件哈希快照；当前快照含未提交源码，不能当作已发布生产版本。
输出 priority-report.md / priority-summary.json / priority-target.json / priority-baseline.json 和普通审计报告。
新家族、消失家族、签名/调用路径变化是调查候选，不自动宣称新视觉样式或 Hook 已覆盖。
服务端灰度、样式数据变化、反射和接口分派仍需运行期证据；complete_coverage 不会因此自动变为 true。
新 APK 自动多路径报告已启用 AI 证据分析。通道和模型取自仓库的 `AI_DEFAULT_PROFILE`、`AI_PRIMARY_*`、`AI_BACKUP_*` 配置，实际响应模型与用量写入尝试账本；客户端不写死端点或模型。每个单元携带稳定 `x-opencode-session`，兼容需要该路由头的 OpenCode 网关。启用 fallback 时，主通道可恢复故障在有界补偿额度内转至独立备用配置。
草稿按页面与路径分片，每片最多两个页面，最多六个草稿单元；首片要求至少两次深挖，模型只读工具总上限仍为六次，并给独立复核预留额度。后续单元根据剩余请求预算按需取证，调度始终为剩余单元预留结构化提交。重点页面和所有草稿发现再分片进入独立上下文复核。探索、提交、格式修正和失败调用全部计入全流程 16 次请求硬限；传输补偿最多两次，跨恢复任务共用预算，每次最多 65536 输出 token。上下文上限仍为 64 万字符，AI 内部累计限时 30 分钟（workflow 步骤硬超时 35 分钟、job 60 分钟）。这是请求/token/时长限制，不是美元扣费硬上限。
全部登记页面的证据由服务端确定性预取，不消耗模型调用；各单元只发送相关页面与源码候选。SSE 传输增量接收工具参数，响应必须完整结束并通过结构校验；读空闲限时 45 秒，单次请求墙钟限时 240 秒，超时终止并回收独立传输进程。网关会话 ID 在同一单元内保持稳定，它用于路由和提示缓存，不能作为服务端幂等保证。复核会话附带服务端重新读取的评论/动态证据，复核只提交记录（含 revised 修订补丁），最终报告由服务端组装后再做完整覆盖校验。

细粒度 SSE 会重复大量封装元数据，不能用相同字节上限代表实际正文。新任务流传输限 32 MiB；历史档位仍按输出预算在 8–32 MiB 内验真；累计拼接 UTF-8 文本/工具字段仍限 2 MiB，数据事件最多 262144 个。JSON 回退保留原随输出档位变化的 2–8 MiB 传输限额，实际内容与 worker 输出仍限 2 MiB。单行/事件限 1 MiB，工具参数限 1048576 字符，私有请求限 8 MiB。精确匹配旧默认 2 MiB 流封装截断及边界指标的历史任务，在修复传输后可显式迁移到既有 `extended-v1`，保留原非重试错误和未知计费并消耗一次恢复补偿；不会自动放过其他格式或大小错误。
AI 流程为预取 → 详细草稿 → 同一模型独立上下文复核（记录制）→ 服务端组装修订后的最终报告；复核不代表人工或真机验收。
所有登记路径分别填写状态、基线变化、可能影响、具体验证方法和证据引用，缺失或擅改静态状态会被拒绝。
评论、动态、所有多路径页面及变化页面进入重点复核；复核阶段必须重新读取评论与动态的目标/基线证据。
草稿发现逐项记录保留、修订、否决或待补证；最终报告必须删除否决项，待补证项不得升级为确定事实。
ai-draft.json / ai-review.json 保留草稿与复核记录；ai-analysis.json 记录提示词版本、哈希及分阶段请求。
复核未完成按 AI 失败处理，不创建 Release，也不更新最新完整报告。
模型只读证据、源码片段及受限类反编译；没有 shell、任意路径、密钥读取或仓库写工具。
报告包含 AI 建议和 E000/E001… 证据引用；引用存在不代表建议已正确或真机已适配。
AI 失败会在 reports 分支保留失败记录，不创建 Release，不更新 latest.json，也不会标为完整 AI 分析。
MCP 示例：submit_job(9140200, "multipath_audit", "")。
重生成已有静态结果：submit_job(9140400, "regenerate_ai", "原分析run ID")，无需重新扫描同一份 APK。
恢复未完成的 AI 单元：`submit_job(9150300, "regenerate_ai", '{"static_run":38716769106,"checkpoint_run":检查点runID}', source_mode="published")`。必须绑定同一份静态证据、源码快照、提示词、工具实现和提供商配置；任一漂移都拒绝复用。已验收响应不再调用模型，剩余单元继续处理。`ai-checkpoint.json` 仅保存公开请求摘要、状态、用量、结构化响应和验收分片，不保存请求消息、源码正文或密钥。
每次 POST 前先落请求账本；连续两次提供商失败会打开 60 秒熔断。处理过的暂时失败可在两次补偿额度内切换备用通道；主通道认证被拒（401/403）时也仅切换一次独立备用凭据，原凭据不重试，备用仍被拒就停止，显式关闭 fallback 则不切换。进程中断后结果不明的请求默认阻止重放，确认后才能显式传 `"resume_unknown":true`，原未知计费记录和总请求次数仍保留。恢复只读取已验真附件，逐文件校验静态目标和基线原字节；不准备 Java/JADX，不下载或重新分析 APK，模型也没有类反编译工具。
连续从同一工作区提交多版本时，源码准备按完整 HEAD、选择规则、文件树和工作树状态复用已验真快照，原捕获时间保持不变。每次仍重新捕获并过秘密门禁，校验私有 payload 的完整 SHA，再核对源码；元数据索引受限于专用目录，OS 锁使并发未命中只发布一次，最多等待 120 秒。源码变化或缓存损坏不会冒用旧身份。

已有可验真草稿分片、但默认预算不足时，可明确指定 `"recovery_policy":"extended-v1"` 并提供 `checkpoint_run`。该恢复链总上限为 24 次请求、4 次补偿、单次 65536 输出，累计期限仍为 1800 秒；旧调用、用量、未知计费与已用时间全部保留。普通新生成和普通恢复为 16/2/65536。迁移仅允许预定传输/调度实现变化，静态事实、源码、提示和验收代码必须匹配；草稿重新完整校验后复用，剩余草稿及所有独立复核继续执行。未显式指定源码的检查点恢复使用该检查点固定源码；显式选择不同源码会被拒绝。

若 `extended-v1` 已完成全部草稿和至少一组独立复核，剩余复核耗尽累计期限，可显式使用 `"recovery_policy":"completion-v2"`。它仅从验真的完整父检查点导入连续已完成单元，重新校验草稿、复核及原始独立读取边界；其总上限为 32 次请求、4 次补偿、累计 3600 秒，单次输出为 65536。此前请求、未知计费、已用补偿与时间都继续计入，不重新分析 APK。原始父检查点和证据保存在独立 `ai-completion-*` 文件；同策略重启还核对新增证据与原父前缀，不能覆盖不同恢复链。

强制提交单元时只向提供商发送对应的 finish 工具，避免兼容网关忽略 tool_choice 后继续选择已耗尽预算的读工具；遗漏 finding_id 等结构错误会返回准确字段与允许值，完整语义校验保持不变。

若 `completion-v2` 已接受更多复核，但实际长推理超过原 240 秒单请求期限，可明确从其检查点进入 `"recovery_policy":"completion-v3"`。它按同提供商最近八次已知成功输出的保守吞吐估算 360–600 秒请求期限，并始终服从剩余累计期限；缺失、零值或未知计费不作为快速样本。固定累计硬限为 40 请求、6 补偿、4800 秒，输出与原验收规则不变；`ai-final-*` 保存完整 v2 父记录，历史时间与计费不清零。只允许预定的逐代迁移及同策略精确恢复，不允许任意改限或未知下一代策略。

提供商诊断读取实际配置：`check_ai_connectivity.py` 只访问目录、输出凭据形状布尔值和固定错误分类；目录公开时不能据此证明 key 可用。`probe_ai_generation.py` 默认只测 primary，按最小生成→流式→合成工具三个依赖阶段串行测试，每阶段最多一次 POST，共享 180 秒期限；失败即停止，账本阻止自动重放。报告不包含密钥、生成正文、隐藏思考或错误正文，合成工具不执行。HTTP 401/403 要检查 key 与账户/模型访问权限，不能用参数降级掩盖认证失败。

AI 分析与生成诊断共用 `hostlab-ai-provider-slot` 串行队列，不取消已运行任务；其他静态查询保留原有并发分组。同一任务内 primary 相邻 POST 至少间隔 35 秒，backup 至少 15 秒；这是客户端保护间隔，不代表服务方配额保证。诊断每阶段仍只调用一次，默认只测 primary，可显式选 backup/all。429 保留至少 60 秒冷却，503 至少 15 秒；完整保留更长的 Retry-After，剩余期限不足则停止，不提前请求。冷却只约束失败提供商，不阻塞独立备用凭据；每次切换或传输重试仍计入既有补偿和请求硬限。

完整结束但返回未提供工具的响应可进入原有逻辑请求预算内的纠正流程，不作为传输重试；未知工具名统一记为 invalid_tool，参数丢弃，只返回当前允许工具的提示，绝不派发执行。工具结构损坏、流中断、输出未完成和认证失败仍按各自边界处理；已知用量和未知计费不清零。

提供商不接受具名 tool_choice 时，可显式配置 AI_PRIMARY_TOOL_CHOICE_MODE=auto（备用对应 AI_BACKUP_TOOL_CHOICE_MODE）；默认 named 不变。auto 模式的强制提交请求仍只提供唯一的目标工具，服务端完整校验返回结果，不将普通文本或其他工具视作提交成功。诊断读取同一配置；配置参与提供商检查点摘要，不能静默复用不同模式的旧检查点。HTTP 400 不自动降级或重试。

输出以 length 截断时，自动流程立即停止，不以相同输出上限重试或切换提供商。显式较大预算恢复保留该单元所有失败和用量；若此前仅发生长度截断，则回到该单元最初使用的提供商继续。extended-v1 也支持全部草稿已验收、尚无已验收复核时的 r0 恢复：先完整校验并复用草稿与证据，补偿仍保留给原失败单元，不重新运行草稿或静态分析。强制提交请求附带明确的仅提交指令，与唯一允许工具共同约束兼容模式。

## 仓库内长期报告

reports 分支 README.md 是报告首页，index.json 是机器索引；每次结果存 samples/<code>/<完整sha>/runs/<run>-a<attempt>/。
仅完整 AI 结果更新样本 latest.json，历史报告不覆盖；失败记录保留独立目录。
中文 report.md 和精简 summary.json 可直接浏览，完整证据在同一私有仓库 Release。
Release 包含 evidence.zip 和 evidence-manifest.json，记录文件哈希，不包含 APK/DEX/SQLite/凭据。
AI 和分析 job 无仓库写权限；独立 publish job 才使用 contents:write，并通过非强制 Git 引用更新处理并发。
MCP job_result 优先读取 reports 分支，Actions 附件过期后仍可取得结论和 Release 入口。
Actions 使用账户分钟和产物额度，超出额度可能收费；每任务最多 35 分钟，没有启用 HF 付费 Jobs。
本地 MCP 网关不是公开 HTTP 服务；当前 Codex 注册后通常需要新会话/重新加载才能发现工具。

## 批量续传

管理员完成 inventory 后运行：

```powershell
tools/hostlab/.venv/Scripts/python.exe tools/hostlab/upload_inventory.py
```

每个样本和清单同次提交；中断后重跑跳过已登记哈希。
三次失败后停止，状态写入 `runtime/hostlab/upload-state.json`。
状态中的 completed 代表成功发布及清单回读，不代表重新下载全部文件。

## 可选原生后端与调度

完整审计只使用原始 DEX 名称，关闭 JADX 的全局 Java 名称改写和 UsageInfo 索引，保留全部 FEATURE 检查。
Java 堆按实测可用内存预算，保留至少 2 GiB 及 30% 余量，上限 8 GiB；遥测缺失回退到 4 GiB，
不足 1 GiB 审计堆时在启动前明确失败。JVM 内存溢出直接退出，不自动重试或跳过审计。
多路径扫描在内存不足 4 GiB 或内存未知时使用一个 worker，其余最多两个；所有 DEX 仍逐一处理。
超时清理 Python/Java/worker 后代，结果只有完整结束才原子发布；残缺、旧报告、样本错配不能进入 AI 审查。
资源采样及总耗时保存在结果产物中；采样 RSS 峰值不等于操作系统精确峰值。

DexSQL 可选后端、批量执行、计划原因、远端去重和兼容边界见 [DEXSQL.md](DEXSQL.md)。
旧 SQLite/JADX 命令保持原有默认值；相关查询优先打包成一次 `plan_analysis` / `submit_analysis`，共用样本与准备成本。


### 模型输出预算与历史恢复

新任务以 `output_budget=generous-v1` 固定声明 65536 token 单次输出预算，覆盖普通草稿、独立复核、
旧单体审查及三个显式恢复档位；只提高 token/载荷容量，不增加各档位请求、补偿、单次和累计时限。
历史 8192/16384 账本仍以其原有预算、摘要、费用及时间验真，不按新默认值改写。
最小回复、流式和强制工具生成探测均为 8192 token；它们只有固定合成任务，目录连通性检查无生成预算。
SSE 事件最多 262144 个，单事件 1 MiB，累计解码内容/worker 输出 2 MiB，JSON 传输最多 8 MiB；
账本容量提高后仍逐个校验响应和单元摘要，附件只对具名检查点允许 64 MiB，其他文件沿用原限额。
模型、提供商及上下文窗口可能限制实际输出；token 预算不替代报告完整性门禁或取消超时。

首次多路径分析的检查点可直接恢复：仅当 `checkpoint_run` 与 `static_run` 是同一已验真原运行，
才从其原始附件推导缺失的静态 manifest。目标/基线原字节、源码、矩阵、提示、验收规则和已完成单元
继续校验；恢复禁用 APK 与反编译访问。唯一受控的 reviewer 实现迁移为进程清理修复的准确哈希对，
它不更改验收代码；任意其他 reviewer 或提示漂移仍拒绝复用。
