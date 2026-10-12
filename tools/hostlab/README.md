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

分析仓库：`jichuo1/innocent-lab-host-analysis`，必须有该私有仓库访问权限。
朋友使用远程分析时不需要 HF Token，也不用下载 APK；需要 GitHub CLI（gh）并完成自己的 `gh auth login`。
在 MCP 客户端配置中将 command 设为独立环境 python 的绝对路径，args 设为 remote_mcp.py 的绝对路径。
MCP 名称建议 `hostlab-remote`；不要与本地 dexq 服务混淆。

工具：submit_job(version_code, operation, argument)、job_status(request_id)、list_jobs()、job_result(request_id)。
operation 可选 info、query、decode、string_refs、decompile、audit；argument 分别为 SQL/方法签名/字符串/类名等。
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
新 APK 自动多路径报告已启用 AI 证据分析。默认主通道 opencode.ai/zen/go/v1 的 glm-5.3-flash；该网关要求 `x-opencode-session` 会话头（缺头报 MissingSessionID），ai_review 每次请求都会带上稳定会话 ID。主通道失败自动降级到备用 glm-5.3-flash。
两阶段预算：草案最多 6 次、复核最多 8 次 API 请求（连接中断类失败另可重试至多 2 次，全流程硬上限 16 次）；模型只读工具合计 6 次，另有服务端免费预取；每次最多 65536 输出 token；上下文上限 64 万字符；AI 步骤内部限时 30 分钟（workflow 步骤级硬超时 35 分钟、job 60 分钟）。这是请求/token/时长限制，不是美元扣费硬上限。
全部登记页面的证据在草案开始前由服务端确定性预取（当前 10 页约 3.1 万字符，零 API 成本，不计入模型工具预算），模型只能用深挖工具（family/protocol/module_source/decompile_class）验证关键假设，避免把预算烧在逐页取证上。草案剩 3 次时收到提交提醒，剩 2 次起强制提交；被拒的提交仍有修正额度。复核会话附带服务端刷新的评论/动态证据，复核只提交复核记录（含 revised 修订补丁），最终报告由服务端确定性组装并再次通过完整校验。
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
