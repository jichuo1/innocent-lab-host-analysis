## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2378 | 274 | 939 | static_invoke_observed |
| comment_legacy_v2 | 586 | 0 | 761 | static_invoke_observed |
| comment_native_exp3 | 67 | 0 | 84 | static_invoke_observed |
| comment_native_legacy | 181 | 0 | 243 | static_invoke_observed |
| comment_native_next | 47 | 0 | 64 | static_invoke_observed |
| comment_other_ui:(root) | 188 | 2 | 492 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 191 | 0 | 119 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 238 | 32 | 298 | static_invoke_observed |
| danmaku_kotlin | 57 | 1 | 8 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1906 | 25 | 499 | static_invoke_observed |
| detail_theseus_united | 4485 | 98 | 4140 | static_invoke_observed |
| dynamic_compose | 953 | 112 | 143 | static_invoke_observed |
| dynamic_legacy | 3193 | 104 | 2143 | static_invoke_observed |
| dynamic_opus | 1313 | 92 | 195 | static_invoke_observed |
| dynamic_other:appointment | 26 | 3 | 18 | static_invoke_observed |
| dynamic_other:card | 412 | 82 | 287 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 58 | static_invoke_observed |
| dynamic_other:commonPerf | 13 | 1 | 2 | static_invoke_observed |
| dynamic_other:commonUi | 21 | 5 | 9 | static_invoke_observed |
| dynamic_other:lightBrowser | 71 | 18 | 29 | static_invoke_observed |
| dynamic_other_legacy | 2063 | 4 | 2145 | static_invoke_observed |
| home_legacy | 1031 | 128 | 222 | static_invoke_observed |
| home_new_frame | 182 | 33 | 53 | static_invoke_observed |
| mine_account_model | 132 | 0 | 54 | static_invoke_observed |
| mine_native | 318 | 7 | 98 | static_invoke_observed |
| pgc_legacy | 357 | 0 | 397 | static_invoke_observed |
| pgc_theseus | 2194 | 131 | 4407 | static_invoke_observed |
| player_java | 962 | 0 | 3235 | static_invoke_observed |
| player_kotlin | 8 | 0 | 150 | static_invoke_observed |
| search_compose | 3147 | 556 | 594 | static_invoke_observed |
| search_native | 1625 | 2 | 2760 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2884 | 44 | 1389 | static_invoke_observed |

## 需要复核的变化

- comment_compose: structure_or_call_path_changed
- comment_legacy_v2: structure_or_call_path_changed
- comment_native_exp3: structure_or_call_path_changed
- comment_native_legacy: structure_or_call_path_changed
- comment_native_next: structure_or_call_path_changed
- comment_other_ui:(root): structure_or_call_path_changed
- comment_other_ui:adapter: structure_or_call_path_changed
- comment_other_ui:nextwidget: structure_or_call_path_changed
- comment_other_ui:span: structure_or_call_path_changed
- comment_other_ui:view: structure_or_call_path_changed
- comment_other_ui:webview: structure_or_call_path_changed
- comment_other_ui:widget: structure_or_call_path_changed
- danmaku_kotlin: structure_or_call_path_changed
- detail_theseus_ugc: structure_or_call_path_changed
- detail_theseus_united: structure_or_call_path_changed
- dynamic_compose: structure_or_call_path_changed
- dynamic_legacy: structure_or_call_path_changed
- dynamic_opus: structure_or_call_path_changed
- dynamic_other:appointment: structure_or_call_path_changed
- dynamic_other:card: structure_or_call_path_changed
- dynamic_other:commonCore: structure_or_call_path_changed
- dynamic_other:commonPerf: structure_or_call_path_changed
- dynamic_other:commonUi: structure_or_call_path_changed
- dynamic_other:lightBrowser: structure_or_call_path_changed
- dynamic_other_legacy: structure_or_call_path_changed
- home_legacy: structure_or_call_path_changed
- home_new_frame: structure_or_call_path_changed
- mine_account_model: structure_or_call_path_changed
- mine_native: structure_or_call_path_changed
- pgc_legacy: structure_or_call_path_changed
- pgc_theseus: structure_or_call_path_changed
- player_java: structure_or_call_path_changed
- player_kotlin: structure_or_call_path_changed
- search_compose: structure_or_call_path_changed
- search_native: structure_or_call_path_changed
- story_native: structure_or_call_path_changed

## 原生资源变化

{'added': 0, 'removed': 0, 'changed': 1}

## 未归类的源码多路径候选

- KotlinMossChannel.kt
- KotlinMossReplyBridge.kt
- NativeFeedbackPanel.kt
- ReplyTopologyComposeMenu.kt
- HookEntry.kt
- RoamingCompatHook.kt
- VersionAdapter.kt

## 未归类协议调用者

完整列表见 priority-summary.json；这些调用者不会静默排除。

## 未覆盖边界

- Server-controlled visual variants without structural changes may be invisible
- Invoke edges do not resolve interface dispatch or prove runtime activation
- Obfuscation/DEX relocation can change fingerprints without a new style
- Unknown families are investigation candidates, not confirmed new styles
# AI 适配分析

AI 建议；证据引用已检查，仍须人工及真机验证。

样本 9.14.0(9140400) 与基线 9.14.0(9140200) 同证书同源，属同版本增量包。10 个登记页面 29 条路径均为 static_invoke_observed，runtime_enabled 全部 unknown、complete_coverage 全为 false。重点评论/动态已抽查家族结构与 MOSS 协议调用，未发现确凿的新样式或功能失效证据；工作树未提交与 120+ 未注册协议是主要待办。以下结论均为待复核建议。

## 各页面评估

### comment
5 条路径均 static_invoke_observed。comment_compose 2378 类/274 compose 方法，kntr/common/comment 包结构完整（E001）；kotlin_moss 定义 130、实际调用边 26，调用者集中在 comment_compose 数据层（E003）。未发现新样式或失效证据；低调用率待运行时确认。
证据：E000, E001, E003

### dynamic
3 条路径均 static_invoke_observed。dynamic_compose 953 类，followinglist 的 ViewModel/状态机样本齐全（E002）；kotlin_moss 382 定义仅 26 条实际边，调用者横跨 legacy 与 compose 两栈（E004）。未发现新样式或失效证据，运行时启用未知。
证据：E000, E002, E004

### home
home_legacy 1031 类、home_new_frame 182 类，均 static_invoke_observed，无协议注册。两条变更均仅为 structure_or_call_path_changed，符合混淆/重排可致指纹漂移的已知限制，无新样式或失效证据，仅缺运行时确认。
证据：E000

### search
search_native 1625 类、search_compose 3147 类/556 compose 方法，均 static_invoke_observed。java_moss 22/24 覆盖良好，kotlin_moss 18/52 调用率偏低，属待复核候选而非失效证据。
证据：E000

### detail
detail_legacy 显示 absent（空输入指纹），theseus_united 4485 类/4140 边，com/bilibili/ship/theseus/united 下 MenuService、TheseusCommentService、videoquality 等样本结构完整（E005）。legacy 缺失更可能是移除/归属调整而非功能失效，需安装器复核映射。
证据：E000, E005

### pgc
pgc_legacy 357 类、pgc_theseus 2194 类/131 compose 方法，均 static_invoke_observed。协议定义调用率偏低（player_moss 3/12、view_moss 7/14），待运行时确认，未见新样式或失效证据。
证据：E000

### player
player_java 962 类/3235 边为主栈，static_invoke_observed。player_kotlin_moss 34 定义仅 3 条实际边，调用者位于 kntr/common/playconfig 且被标 external_or_unknown（E006），说明跨族引用未被页面归属，不能据此断言失效。
证据：E000, E006

### danmaku
danmaku_legacy 显示 absent（空输入指纹），danmaku_kotlin 仅 57 类/8 边；java_moss 调用充分（20/22）。legacy 缺失与 kotlin 路径体量偏小需安装器与运行时双重复核，不构成失效结论。
证据：E000

### story
story_native 2884 类/1389 边，static_invoke_observed；story_kotlin 显示 absent（空输入指纹），无协议注册。未见新样式或失效证据，absent 需安装器侧核对家族映射。
证据：E000

### mine
mine_native 318 类/98 边、mine_account_model 132 类/54 边，均 static_invoke_observed，无协议注册，变更均为 structure_or_call_path_changed。页面体量小且稳定，未发现新样式或失效证据。
证据：E000, E007

### 评论页面运行时启用状态未知
5 条路径 runtime_enabled=unknown、complete_coverage=false，evidence 停留在 static_invoke_observed。静态调用边不解析接口分发，不能证明真机生效；comment_kotlin_moss 130 定义仅 26 条实际调用边，低调用率需运行时解释。
建议：真机验证评论各路径功能是否生效，并复核 Kotlin MOSS 调用覆盖率，再决定是否接受适配。
证据：E000, E001, E003

### 动态页面运行时启用状态未知且协议调用率偏低
3 条路径均 static_invoke_observed；dynamic_kotlin_moss 382 定义仅 26 条实际边，调用者横跨 dynamic_legacy 与 dynamic_compose 两栈，静态覆盖不完整，不构成失效证据。
建议：运行时观测动态页各路径与协议启用情况，补齐静态无法覆盖的接口分发证据。
证据：E000, E002, E004

### 详情页 theseus_united 结构完整，legacy 缺失待安装器复核
theseus_united 4485 类/4140 边，MenuService、TheseusCommentService、videoquality 等样本结构完整；detail_legacy 指纹为空输入哈希且 evidence=absent，更可能是代码移除或家族归属调整而非功能失效。
建议：在安装器侧核对 detail_legacy 登记映射是否仍有效，确认 absent 是否为预期行为。
证据：E000, E005

### 播放器 Kotlin 协议存在跨族未归属调用
player_kotlin_moss 34 定义仅 3 条实际边，调用者位于 kntr/common/playconfig 且被标 external_or_unknown，说明部分调用未被页面家族归属，静态低调用率不能断言失效。
建议：运行时观测播放配置相关调用，确认 playConf/playConfEdit 实际使用情况。
证据：E000, E006

### 生产源码快照工作树未提交
source_dirty=true；抽查 VersionAdapter.kt（模块内版本适配器，与我的页入口相关）返回 working_tree_dirty 标记，适配逻辑为运行时定位+缓存，快照与构建产物可能不一致。
建议：提交或清理工作树后重建快照，再以发布产物为基准复核适配结论。
证据：E007

### 36 个待复核变更均为结构/调用路径变化，另有 120+ 未注册协议
changes 全部为 structure_or_call_path_changed，资源 added=0/removed=0/changed=1；limitations 明确混淆/DEX 重排可致指纹漂移，未知家族是调查候选而非确认的新样式。unregistered_protocols 覆盖 HomeMoss、ReplyMoss、ViewMoss 等 120+ 协议，指向登记覆盖不全。
建议：将结构变化与未注册协议视为待复核信号，逐条核对是否需纳入登记，不据此判定新样式或失效。
证据：E000

## 下一步

- 在真机（LSPosed）环境按登记页面逐项验证重点功能是否生效，再判定适配接受
- 提交或清理未提交的工作树后重建生产源码快照，重新执行本次比对
- 逐条核对 unregistered_protocols，区分样式相关协议与后台协议并补充登记
- 对 detail_legacy / danmaku_legacy / story_kotlin 三个 absent 家族核对安装器映射与真实归属
- 对定义/调用率偏低的 Kotlin MOSS 协议补充运行时观测数据