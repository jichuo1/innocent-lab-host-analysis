# 宿主适配云端分析

[查看长期分析报告](https://github.com/jichuo1/innocent-lab-host-analysis/tree/reports) · [完整证据归档](https://github.com/jichuo1/innocent-lab-host-analysis/releases) · [运行任务](https://github.com/jichuo1/innocent-lab-host-analysis/actions)

开发入口：[宿主适配标准流程](docs/HOST_ADAPTATION_WORKFLOW.md)（从准确样本、功能覆盖台账、R8/DexKit 核查到验证与交付，含快速上手和扩展模板）。

新 APK 自动执行静态、多路径及有界 AI 分析。报告执行成功不等于真机适配通过。

AI 先生成详细逐路径草稿，再以同一模型的独立上下文复核重点页面及全部草稿发现。
评论与动态须重新读取目标包和基线证据；复核未完成不发布成功 Release。报告保留修订决定和证据缺口。

可浏览结论保存在 reports 分支，完整证据保存在本私有仓库 Release。失败记录也保留，只有完整 AI 报告更新 latest.json。

