# 仅远程分析客户端

解压到项目根，使文件位于 tools/hostlab。需要 Python 3.13 和 GitHub CLI。
运行环境在 tools/hostlab/.venv-remote，结果与配置在 runtime/hostlab；不使用项目临时目录。
管理员先把你的 GitHub 账号加入私有分析仓库：jichuo1/innocent-lab-host-analysis。
触发任务需要 Actions write 权限；使用你自己的 gh auth login，不共享管理员凭据。
Windows 双击 setup-remote.cmd；若装有 Codex CLI，会注册 hostlab-remote。
其它 AI 客户端：command 填独立环境 python 的绝对路径，args 只填 remote_mcp.py 的绝对路径。
重新加载客户端或开启新会话后使用四个 MCP 工具。

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

operation: info / query / decode / string_refs / decompile / audit / multipath_audit / regenerate_ai。
新 APK 自动报告与 multipath_audit 包含有界 AI 分析；AI 建议不能替代真机验收。
AI 先出详细逐路径草稿，再在同一模型的独立上下文中复核重点页面和全部草稿发现；评论与动态须重新取两侧证据。
两阶段合计最多 8 次 API 请求（连接中断类传输失败可额外自动重试，合计至多 2 次）、8 次只读取证，每次最多 32768 输出 token。复核未完成不发布成功 Release。
reports 分支保存可浏览结论，私有 Release 只保存完整成功分析的证据；失败只保留报告记录。MCP 取结果优先访问长期报告。
不需要 HF Token、APK、JDK、JADX 或 Android SDK。只会下载报告和有界分析结果。
计算在 GitHub Actions Runner；分析 job 最多 45 分钟，发布 job 最多 15 分钟。Actions 附件保留 14 天，仓库报告和 Release 不按这个期限清理。
静态证据不能替代真机验收。Actions 消耗仓库拥有者的分钟及产物额度。
本地 stdio 网关不是公开 HTTP 服务；ChatGPT 网页的远程 HTTP 接入未配置。
# Read-only sample inventory

Call `submit_job(version_code=1, operation="inventory")`, then use `job_status` and `job_result` as usual. The version code is a required placeholder and does not select an APK. The `inventory.json` artifact lists every registered sample at one immutable sample revision, exposing only version, SHA-256, size, and certificate metadata. No APK or DEX is downloaded for this operation.
