# 仅远程分析客户端

解压到项目根，使文件位于 tools/hostlab。需要 Python 3.13 和 GitHub CLI。
管理员先把你的 GitHub 账号加入私有分析仓库：jichuo1/innocent-lab-host-analysis。
触发任务需要 Actions write 权限；使用你自己的 gh auth login，不共享管理员凭据。
Windows 双击 setup-remote.cmd；若装有 Codex CLI，会注册 hostlab-remote。
其它 AI 客户端：command 填独立环境 python 的绝对路径，args 只填 remote_mcp.py 的绝对路径。
重新加载客户端或开启新会话后使用四个 MCP 工具。

- submit_job(9140200, "query", "SELECT file_id,class,name,proto FROM methods WHERE name='getUrlsMap'")
- job_status(返回的 request_id)
- job_result(同一 request_id)
- list_jobs()

operation: info / query / decode / string_refs / decompile / audit。
不需要 HF Token、APK、JDK、JADX 或 Android SDK。只会下载报告和有界分析结果。
计算在 GitHub Actions Runner；每次任务最多 35 分钟，同版本任务串行，结果保留 14 天。
静态证据不能替代真机验收。Actions 消耗仓库拥有者的分钟及产物额度。
本地 stdio 网关不是公开 HTTP 服务；ChatGPT 网页的远程 HTTP 接入未配置。
