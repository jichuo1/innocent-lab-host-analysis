## 模块源码快照

- 来源：published
- 捕获时间（UTC）：2026-10-15T14:19:32.431433Z
- 源码 HEAD：5422fad1e3f798252619d610a0504573ff47211b
- 快照 SHA-256：2fa2d3b70f73fa431ed83267a9519c726a41b67de39eb7ee785813de39067120
- 源码树 SHA-256：37745f8f27c41c22eab6e0bc780c6af700d650f49c3f004f862bf9c5f1548a5c
- 含未提交修改：True
- 时效状态：published_unverified_worktree

## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2430 | 283 | 1103 | static_invoke_observed |
| comment_legacy_v2 | 580 | 0 | 743 | static_invoke_observed |
| comment_native_exp3 | 55 | 0 | 56 | static_invoke_observed |
| comment_native_legacy | 192 | 0 | 263 | static_invoke_observed |
| comment_native_next | 49 | 0 | 66 | static_invoke_observed |
| comment_other_ui:(root) | 227 | 2 | 538 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 212 | 0 | 100 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 243 | 30 | 249 | static_invoke_observed |
| danmaku_kotlin | 135 | 3 | 162 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1976 | 25 | 529 | static_invoke_observed |
| detail_theseus_united | 4617 | 98 | 4196 | static_invoke_observed |
| dynamic_compose | 1234 | 151 | 232 | static_invoke_observed |
| dynamic_legacy | 3261 | 103 | 2060 | static_invoke_observed |
| dynamic_opus | 1376 | 94 | 230 | static_invoke_observed |
| dynamic_other:appointment | 32 | 4 | 20 | static_invoke_observed |
| dynamic_other:card | 420 | 88 | 305 | static_invoke_observed |
| dynamic_other:commonCore | 26 | 0 | 62 | static_invoke_observed |
| dynamic_other:commonPerf | 12 | 1 | 3 | static_invoke_observed |
| dynamic_other:commonUi | 23 | 5 | 9 | static_invoke_observed |
| dynamic_other:lightBrowser | 78 | 19 | 34 | static_invoke_observed |
| dynamic_other_legacy | 2098 | 4 | 2185 | static_invoke_observed |
| home_legacy | 744 | 87 | 228 | static_invoke_observed |
| home_new_frame | 198 | 33 | 51 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 327 | 7 | 96 | static_invoke_observed |
| pgc_legacy | 366 | 0 | 455 | static_invoke_observed |
| pgc_theseus | 2262 | 131 | 904 | static_invoke_observed |
| player_java | 954 | 0 | 3308 | static_invoke_observed |
| player_kotlin | 458 | 37 | 836 | static_invoke_observed |
| search_compose | 3136 | 562 | 607 | static_invoke_observed |
| search_native | 1701 | 2 | 2880 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2954 | 44 | 1439 | static_invoke_observed |

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
- comment_kotlin_moss: protocol_signature_or_call_path_changed
- danmaku_kotlin_moss: protocol_signature_or_call_path_changed
- detail_kotlin_moss: protocol_signature_or_call_path_changed
- dynamic_kotlin_moss: protocol_signature_or_call_path_changed
- search_kotlin_moss: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/account/interfaces/v1/KAccountInterfaceV1Moss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/ad/im/v1/KBusinessChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KOpusMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KTribeeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/gopm/widget/v1/KWidgetMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/home/v1/KHomeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KimMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KHistoryMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KMediaMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/listener/v1/KListenerMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/mine/v1/KMineMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/childchannel/v1/KKidsChannelMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/mixture/v1/KMixtureMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/story/v1/KStoryMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KLegacyViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/dynamic/interfaces/feed/v1/KFeedMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/customer/interfaces/KCustomerInterfaceMoss;: protocol_signature_or_call_path_changed

## 原生资源变化

{'added': 0, 'removed': 0, 'changed': 1}

## 未归类的源码多路径候选

- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/agent/host/HostAgentWindow.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/HookEntry.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/RoamingCompatHook.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/VersionAdapter.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/VersionAdapterContract.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/feature/KotlinMossChannel.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/feature/KotlinMossReplyBridge.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/feature/NativeFeedbackPanel.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/hook/feature/ReplyTopologyComposeMenu.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/runtime/HostThreadGuard.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/runtime/replytopology/ReplyTopologyGraphBuilder.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/ui/skin/activity/SkinnedActivity.kt
- Bilibili_Innocent_Lab/app/src/main/java/com/Bilibili_Innocent_Lab/xposedmodule/ui/skin/liquid/LiquidRefractionBackendApi33.kt

## 未归类协议调用者

完整列表见 priority-summary.json；这些调用者不会静默排除。

## 未覆盖边界

- Server-controlled visual variants without structural changes may be invisible
- Invoke edges do not resolve interface dispatch or prove runtime activation
- Obfuscation/DEX relocation can change fingerprints without a new style
- Unknown families are investigation candidates, not confirmed new styles
# AI 适配分析

AI 建议；证据引用已检查，仍须人工及真机验证。

本单元仅覆盖登记页 comment 与 dynamic，样本 9.17.0（9170300）对比基线 9170100，同包同证书，仅 base.apk 体积 +33KB（E000）。两页共 8 条登记路径的 evidence 一律为 static_invoke_observed，runtime_enabled 全部 unknown，module_coverage 全部 requires_installer_review，静态调用存在不等于真机启用，也不等于模块 Hook 生效，本报告不宣称适配通过。可复核的事实变化：全部 8 个家族的 fingerprint 均改变，但 comment_compose 的 compose_methods 在 283→283 不变、dynamic_legacy 的 compose_methods 103→103 不变，说明结构哈希变化本身不能推出新样式，需先排除混淆改名、DEX 重排与重复包装层；在方法数维度上确有实量变化的是 dynamic_compose（compose_methods 141→151、classes 1187→1234）与 comment_native_legacy（classes 181→192、external_invoke_edges 220→263），而 dynamic_legacy 的 external_invoke_edges 反向下降 2075→2060。协议侧 comment_java_moss/dynamic_java_moss 的 definitions 与 invoke_edges 完全未变，Kotlin MOSS 仅 dynamic 少 1 条边（27→26，comment 23 不变），即协议层无结构信号，页面变化主要落在 UI 家族。源码快照 working_tree_dirty=true，全部结论按固定哈希文件追溯（source_tree_sha256 37745f8f…），未读文件不推测其 Hook 覆盖。服务端 A/B 视觉变体在无结构变化时静态不可见，故“样式已穷尽”不可断言。

本单元仅覆盖 9.17.0(9170100→9170300，同一 version_name) 的 home 与 search 四个登记路径。四路径静态证据均为 static_invoke_observed，运行时是否启用、模块安装器是否命中全部为 unknown，故不声明适配通过。结构层面：home_legacy 类数 766→744、外部调用边 198→228，home_new_frame 类数 196→198、边 52→51；search_native 1705→1701、边 2818→2880，search_compose 3146→3136、边 614→607；四条路径的 compose_methods 数值均未变化（87/33/2/562），指纹全部变化。类数小幅增减与同一 version_name 的增量构建、混淆改名、DEX 重排高度兼容，因此指纹变化只能作为“需复核”候选，不能判定为新样式。协议侧 search_java_moss 24 定义/22 实际调用边、search_kotlin_moss 52/18，两侧完全一致，说明协议层定义与调用规模未变；但未注册协议清单含 HomeMoss/KHomeMoss、SearchMoss/KSearchMoss（app/search/v2、app/interfaces/v1、broadcast/message/search 等）多个搜索/首页相关契类，跨家族消费者归属与模块解析点均未读证，覆盖率未知。本概览为草稿阶段结论，尚未复核。

本单元只覆盖 detail（详情页，3 条登记路径）与 pgc（番剧/影视，2 条登记路径）。9.17.0(9170300) 相对 9170100 的冻结静态矩阵显示：detail_legacy 两侧均为 absent（classes=0），不能据此认为旧原生详情已消失，只能说明该家族在本样本中未被静态矩阵命中；detail_theseus_ugc 与 detail_theseus_united 指纹变化，类数分别为 1976→与基线 1975、4617 与基线 4633，外部调用边 529/547、4196/4199 小幅下降，compose 方法数未变（25、98）；两条 detail MOSS 协议定义数与实际调用边（32/35、76/38）与基线完全一致，提示协议层未迁移，家族内差异更可能是混淆改名/DEX 重排或家族内代码搬家，而非新样式。pgc_legacy 类数 352→366、调用边 425→455 上升，pgc_theseus 类数 2276→2262、调用边 1179→904 明显下降、compose 134→131，两条 pgc 协议（12/3、14/7）与基线一致。本单元未读取任何 detail/pgc 定位器与安装器源码正文，module_coverage 仍为 requires_installer_review，runtime_enabled 全部 unknown；全部结论均为静态观察，不构成适配通过。资源仅 1 个 changed、增删为 0，对样式判断无直接支撑。

本单元覆盖 player 与 danmaku 两个登记页面共 4 条路径（9.17.0 build 9170300，sha256 b3950fd3…；基线 9170100，f0f880e8…，同证书、同 repo revision）。player_java 与 player_kotlin 均为 static_invoke_observed：player_java 类数 953→954、外调边 3308 不变；player_kotlin 类数 455→458、Compose 方法 37 不变、外调边 841→836。danmaku_legacy 两侧均 absent（类数 0、边 0、指纹为同一空集哈希）；danmaku_kotlin 类数 137→135、Compose 3 不变、外调边 162 不变；danmaku_java_moss（22 定义/20 实际调用边）与 danmaku_kotlin_moss（46/10）两版完全一致。三条路径被标记 structure_or_call_path_changed。全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，不能宣称适配通过。本轮未获得 player/danmaku 的深挖结果（本轮深挖 E011–E014 属评论区与首页），结论限于 candidate 或 needs_runtime；未读到的安装器/定位器实现细节一律记为未知。

本单元覆盖 story、mine 两页共 4 条登记路径。目标包 9.17.0（9170300）对基线 9170100，证书一致。story_native、mine_native、mine_account_model 被标记结构或调用路径变化，story_kotlin 仍为 absent。四条路径 runtime_enabled 均为 unknown、module_coverage 均为 requires_installer_review；源码快照为未提交工作树（689 文件、dirty），只能按文件哈希作冻结证据，不能当作安装器或运行时覆盖证明。以下区分事实、推断与待真机验证，未宣称任何页面适配通过。

## 各页面评估

### comment

comment 页 5 条路径全部 static_invoke_observed、runtime unknown。与基线相比，5 个家族的 fingerprint 全变，但只有 comment_native_legacy 出现可解释的实量位移：classes 181→192（+11）、external_invoke_edges 220→263（+43），这更像新增调用者或包装层扩容，而不是单纯改名；comment_native_next（48→49，边 67→66）与 comment_native_exp3（54→55，边 52→56）是小幅漂移，属于“不能排除改名/重排”的灰区。comment_compose 的 classes 2428→2430、compose_methods 283→283、edges 1101→1103，Compose 方法数一个不差，仅结构哈希变化，按规则不应判为新样式候选，优先假设 DEX 重排或包装层变化。comment_legacy_v2 的 classes 583→580 略降而边 741→743 略升，方向相反，提示类合并/内联与调用点增加可能同时发生。协议层 comment_java_moss（50 定义/50 边）与 comment_kotlin_moss（130 定义/23 边）与基线完全一致，说明 Reply 相关 gRPC/MOSS 协议接口未变，变化集中在 UI 家族；但 Kotlin MOSS 的 23 条实际边远少于 130 条定义，未落地定义不等于无消费者。模块侧 CommentClassicStyleLocator 以硬编码 owner（com.bilibili.lib.dd.DeviceDecision.getBoolean、kntr.base.dd.IDeviceDecisionKt.getBool）加实验键锚点（comment.next_appearance、comment.kntr.enabled 等）做原生/Kotlin 双家族定位，并以 Class 存在性 kotlinApplicable 决定 Kotlin 家族是否参与；因此 9.17.0 中任一 owner 改名或 Compose 入口 CommentSectionComposeFragment 迁移，都会使定位器静默退化为空集而不抛错。是否命中真机路径、实验键是否下发，均未读到运行条件，记为未知。

证据：E000, E001, E011, E012

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：classes 583→580、external_invoke_edges 741→743、compose_methods 恒 0，fingerprint 由 b8b8915c… 变为 0a6d90ff…；类数与边数反向微变，属哈希变化但无规模化位移。
- 可能影响：经典 V2 评论家族若真实承载 purify/复制桥，则变更可能落在包装层或内联；CommentClassicStyleLocator 的 NATIVE 家族读取依赖该链路的 DeviceDecision.getBoolean，一旦类被内联该方法可能从声明方法列表消失。
- 验证：用 family_evidence 按名重读 comment_legacy_v2 全量类清单，与基线做类级差集；在真机对 DeviceDecision.getBoolean 与 CommentV3Fragment 入口做 Hook 命中日志，确认 direct() 是否返回非空。
- 证据：E000, E001, E011, E012

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：classes 181→192（+11）、external_invoke_edges 220→263（+43）、compose_methods 恒 0，fingerprint 由 86f3175b… 变为 62bf1867…，是本页唯一具有双向实量增长的家族。
- 可能影响：Native legacy 侧新增类与调用边可能带来新的评论条目绑定/复制调用者，CommentNativeBindingCatalog 与 CommentNativeSupplementBridge 的目录与补充绑定可能对新增类未覆盖，导致样式或补充字段缺失而不报错。
- 验证：对新增 11 个类做 JADX 反编译定位其调用者，确认是否属于评论条目的重复包装层；真机验证 NativeSupplementBridge 注入点命中数并与基线对比。
- 证据：E001, E012

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：classes 48→49、external_invoke_edges 67→66、compose_methods 恒 0，fingerprint 由 a418874b… 变为 49f54dff…；边数净减 1。
- 可能影响：属小幅漂移，可能仅为改名/重排，也可能有单个调用点被移除；影响 CommentNativeBindingCatalog 的 next 分支匹配精度。
- 验证：按类名与方法描述比对基线，确认差异是单点改名还是真实移除；真机记录 next 分支 Hook 是否仍有调用。
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：classes 54→55、external_invoke_edges 52→56、compose_methods 恒 0，fingerprint 由 0b5098d4… 变为 51ab749a…。
- 可能影响：实验 3 分支边数小幅增加，可能是实验入口扩写；CommentClassicStyleLocator.matchesKey 显式列有 comment.next_appearance_experiment_3，若键名或读取方法变化，实验分支判定会落到兜底缓存。
- 验证：核对 exp3 家族的读取方法签名是否仍满足 verified() 的 (String, Boolean, …) 约束；真机以实验开关打开/关闭各跑一次，观察读取点是否被调用。
- 证据：E001, E012

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：classes 2428→2430、compose_methods 283→283（完全不变）、external_invoke_edges 1101→1103，fingerprint 由 089904c2… 变为 4d15c77d…；结构哈希变化而 Compose 方法数不变。
- 可能影响：按“哈希变化≠新样式”原则，此路径优先判为 DEX 重排/混淆改名/包装层，而非新增 Compose 样式；CommentComposePurifyBridge、CommentComposeCopyBridge、CommentComposeViewAccess 所依赖的 Compose 访问点可能仅位置变化，但也可能因入口迁移而失配。
- 验证：对 comment_compose 按 compose_signatures 做方法级差集，确认 283 个签名是否逐一对应；真机在 Compose 评论区确认 purify/copy 桥是否生效；另需检查 kotlinApplicable 依赖的 CommentSectionComposeFragment 是否仍存在。
- 证据：E001, E012

### dynamic

dynamic 页 3 条路径全部 static_invoke_observed、runtime unknown。三条路径的 fingerprint 全变，但方法维度信号分两类：dynamic_compose 是本单元最有实量意义的变化，classes 1187→1234（+47）、compose_methods 141→151（+10）、external_invoke_edges 234→232（-2），即新增了 10 个 Compose 方法而外部边反而减少，符合“Compose 内部实现扩张、对外调用收敛”的候选新样式形态，也可能是一次 Compose 重构把若干 @Composable 拆分；在真机与协议层确认前只能记为候选。dynamic_opus 的 classes 1350→1376（+26）但 compose_methods 94→94 不变、edges 226→230，属结构变化而 Compose 层稳定，提示 Opus 侧改动在工具/包装层；dynamic_legacy 则出现 classes 3255→3261（+6）而 edges 2075→2060（-15）的反向组合，最可能的解释是调用点合并或迁移到 Compose/Opus 家族，其次是混淆内联，但都不能排除真实功能点被移除；判定需真实的调用边归属，而静态边不解析接口分发。协议层 3 个 unregistered_protocol 中的 OpusMoss/KOpusMoss、DynamicMoss、FeedMoss 均未登记，dynamic_java_moss 定义与边 134/134 与基线一致、dynamic_kotlin_moss 由 26→27 边（382 定义不变），说明协议面无结构变化，跨家族消费者是否切到 Kotlin 通道静态不可判。模块侧 DynamicPurifyFeatureInstaller/DynamicPurifyPolicy 与 KotlinDynamicMossWatch 的匹配点是否仍覆盖新增类，未读到源码正文，记为未知。

证据：E000, E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：classes 3255→3261（+6）、compose_methods 恒 103、external_invoke_edges 2075→2060（-15），fingerprint 由 494b6f4a… 变为 b7565e6b…；类增边减的反向组合。
- 可能影响：若 15 条边减少来自调用点迁往 Compose/Opus 家族，则 legacy 净化与 tabs 逻辑的实际覆盖面缩小；若来自接口分发或内联，则功能仍在但静态不可见。DynamicPurifyFeatureInstaller 与 DynamicTabsFeatureInstaller 的入口若挂在被合并的方法上，可能整段不生效。
- 验证：对基线与目标做 external_invoke_edges 的调用者差集，确认减少的边来自哪些 owner；真机在动态页分别以 legacy 样式（关闭 Compose 开关）进入，观察 purify 与 tabs Hook 日志是否触发。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：classes 1187→1234（+47）、compose_methods 141→151（+10）、external_invoke_edges 234→232，fingerprint 由 d1bf0fee… 变为 da87e05c…；Compose 方法数实质增加，是本单元唯一 Compose 层实量变化。
- 可能影响：新增 10 个 @Composable 方法可能是动态页 Compose 卡片拆分或新样式分支，DynamicPurify 的 Compose 侧匹配点、以及 Compose 复制/净化桥可能只覆盖旧方法集合，新增分支可能未净化（漏拦而非崩溃）。
- 验证：按 compose_signatures 逐条比对新增 10 个签名并反编译定位其宿主类与调用方；真机开启动态页 Compose 样式，对新增分支构造含屏蔽词/广告卡片的动态条目，检查是否被过滤。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：classes 1350→1376（+26）、compose_methods 恒 94、external_invoke_edges 226→230（+4），fingerprint 由 60096774… 变为 0ea59ce6…；Compose 方法数不变。
- 可能影响：Opus 家族扩张发生在非 Compose 层（模型/工具/包装），dynamic_opus 的净化与卡片绑定若以 Compose 方法为锚则可能仍匹配，但新增非 Compose 类可能引入未登记的协议消费者；OpusMoss/KOpusMoss 均属 unregistered_protocol，跨家族消费者覆盖无从证实。
- 验证：列出新增 26 个类的包归属，判断是否新增 Moss 调用者；核对 dynamic_kotlin_moss 边数 26→27 的那一条边是否落在 Opus 家族；真机在 Opus 详情/列表验证净化生效。
- 证据：E002

### home

首页两条已登记路径并存：home_legacy（Ltv/danmaku/bili/ui/main2/HomeFragmentV2、BasePrimaryMultiPageFragment 等经典框架，744 类/878 Hmm）与 home_new_frame（Ltv/danmaku/bili/khome 家族，含 HomeFrameViewModel$dispatchAction、bubble 组件，198 类）。目标侧 home_legacy 类数由基线 766 降至 744，compose_methods 保持 87 不变，external_invoke_edges 由 198 升至 228；home_new_frame 类数 196→198，compose_methods 33 不变，边数 52→51。两类变化幅度均在个位数到二十余类，且同一 version_name 下只递增 version_code，符合增量构建、混淆改名与 DEX 重排的解释，因此 fingerprint 变化（E003、E013、E014）不构成“新首页样式”的证据；也不能因边数增加推断 Hook 面扩大，定义数与调用边数是不同单位，禁止相除推覆盖率。模块侧本轮未读取任何源码：catalog 中提到 HomeFrameListHook.kt、HomeFrameTabLocator.kt、HomeRecommendPurifyFeatureInstaller.kt、HomeBannerFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt、HomeComponentFilterFeatureInstaller.kt、HostHomeCardSpacingHooks.kt、HomeVerticalDetailRouting.kt 等候选，但未读内容，因此对两条路径各自的安装器/定位器命中情况、兜底分支与宽屏/平板差异均记为未知。首页协议 HomeMoss、KHomeMoss 未登记为协议项，可能存在结构化解析消费者之外的调用者，属未归类候选而非确认新家族。旧/新原生并存时的切换条件（服务端开关、二次确认、组件下发）在静态证据中不可见，未读到运行条件即写未知。结论：两条路径均为待复核的静态调用存在，不宣称通过。

证据：E003, E013, E014

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类数 766→744，compose_methods 保持 87，external_invoke_edges 198→228，fingerprint 由 a56da1e1… 变为 1ae88d27…；样例仍为 Ltv/danmaku/bili/ui/main2/HomeFragmentV2 相关匿名类与 AccountMineRequestResource 枚举，未见新命名家族。
- 可能影响：若差异源于 DEX 重排/混淆，模块既有定位器仍可能命中；若源于真实代码迁移，则依赖 HomeFragmentV2 具体方法描述符的 Hook 点可能失配，影响首页推荐净化、Tab 过滤、顶部栏/横幅处理的安装成功率。当前为推断，未读源码验证。
- 验证：1) 用同一签名分别重读基线与目标的 HomeFragmentV2 及 HomeFrameTabLocator 候选方法描述符，比对方法名/参数是否仅为重命名；2) 逐文件哈希比对 HomeFrameListHook.kt 侧引用的类名清单，确认无消失项；3) 真机抓取 HookEntry 安装日志中各 home 定位器的 DEX 辅助查询成功/失败条目。
- 证据：E003, E014

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 196→198，compose_methods 保持 33，external_invoke_edges 52→51，fingerprint 由 34c59fa3… 变为 d9422517…；样例为 Ltv/danmaku/bili/khome/widget/bubble 系列与 HomeFrameViewModel$dispatchAction$1，属 khome 新框架内部小改动。
- 可能影响：新框架路径的类数净增 2、边数净减 1，属构建级波动量级；对模块的影响取决于 HomeFrameListHook/HomeFrameTabLocator 是否绑定 HomeFrameViewModel.dispatchAction 或 bubble 类型，未读源码前无法判定，标为未知。
- 验证：1) 在 module_source 中读取 HomeFrameListHook.kt 与 HomeFrameTabLocator.kt，列出其实际引用的类名与方法签名，与 E013 样例比对是否仍在；2) 检查是否存在 Compose 与 khome 双栈同时安装的路径，验证 tab 槽位只在一条路径生效；3) 真机在首页切换 Tab 并观察净化是否生效。
- 证据：E003, E013

### search

搜索页两条路径均为 static_invoke_observed：search_native（1701 类，compose_methods 仅 2，外部调用边 2880）与 search_compose（3136 类，compose_methods 562，边 607）。相对基线：search_native 类数 1705→1701、边 2818→2880（+62 边）、compose_methods 不变；search_compose 类数 3146→3136（-10）、边 614→607、compose_methods 不变。两边 compose_methods 完全不变这一点支持“非新样式、仅构建/混淆波动”的替代解释；但 search_native 边数增加 62 属于本单元最大幅度变动，仍需排除真实调用点新增（如新增服务端开关分支或新消费者）后再判定无害。协议侧 search_java_moss 定义 24、实际调用边 22；search_kotlin_moss 定义 52、实际调用边 18，目标与基线两组数字完全相同，说明搜索 MOSS 契约的方法集合与静态调用规模未变，这类“结构未变”无法排除服务端 A/B 视觉变体，静态不可见。同时未注册协议清单含 app/search/v2/SearchMoss、app/search/v2/KSearchMoss、app/interfaces/v1/SearchMoss、KSearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/KSearchMoss 等，说明搜索相关契类存在未归类协议项；它们是否为跨家族消费者、是否被模块解析点覆盖，本轮未读源码，记未知。搜索页模块候选包括 SearchHomeRecommendLocator.kt、SearchHomeRecommendFeatureInstaller.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt、SettingsSearchMatcher.kt，均未读内容，因此安装器覆盖、定位器兜底、窄/宽屏差异一律为未知，不声明适配通过。

证据：E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数 1705→1701，compose_methods 保持 2，external_invoke_edges 2818→2880（本单元最大变动），fingerprint 由 28e67919… 变为 71eaa45e…；无新增 Compose 签名。
- 可能影响：边数 +62 可能是新增分支、新增内部调用点或仅台账口径变化；若确为真实新增调用点，依赖旧调用点签名的净化/推荐隐藏 Hook 可能漏掉新路径，导致搜索首页推荐或默认词清理部分失效。属推断，未读源码。
- 验证：1) 重取该家族边列表做差集，定位新增边的来源类，判断是否落在已知搜索推荐/默认词相关类；2) 读取 SearchHomeRecommendLocator.kt 与 SearchPurifyFeatureInstaller.kt，比对其引用签名是否在新边集合中；3) 真机进入搜索首页，确认推荐模块与默认词清理是否仍生效并记录日志中的定位器命中项。
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数 3146→3136，compose_methods 保持 562，external_invoke_edges 614→607，fingerprint 由 4e4c7892… 变为 b64bbcfd…；Compose 方法总数不变，未见新 Compose 家族。
- 可能影响：类数减 10、边减 7 与 Compose 方法数稳定并存，最可能是重排或删减非 Compose 辅助类；若模块通过 Compose 签名定位搜索页组件，签名集合未变意味着命中概率基本不变，但 runtime 与安装器覆盖未知，不能据此宣称可用。
- 验证：1) 比对两侧 Compose 签名集合的差集，确认 562 个签名逐项一致而非数量巧合；2) 读取 SearchHomeRecommendFeatureInstaller.kt 确认其 Compose 分支与原生分支的互斥条件；3) 真机分别在搜索结果页与搜索首页观察是否有重复净化/双份隐藏。
- 证据：E004

### detail

详情页三条登记路径中，detail_legacy 在目标与基线两侧的静态矩阵均为 absent（classes=0、compose=0、外部调用边=0、指纹为 sha256("[]") 的空集合值），因此“旧原生详情路径消失”这一结论没有证据支撑：absence 只表示本矩阵未命中，可能是路径确实不再被静态识别，也可能是矩阵选择器/规则变化或该类代码被并入其他家族。detail_theseus_ugc 目标 1976 类、25 个 compose 方法、529 条外部调用边，基线 1975/25/547，类数等同、边数少 18、指纹变化；detail_theseus_united 目标 4617/98/4196，基线 4633/98/4199，类数少 16、边数少 3、指纹变化。两条 theseus 路径的 compose 方法数完全不变，这一点削弱“新样式（新增 Compose 实现）”的解释，更符合混淆改名、内联/合并、DEX 重排或家族边界调整。协议侧 detail_java_moss（32 定义/35 实际调用边）与 detail_kotlin_moss（76/38）在两侧完全一致，说明共享协议没有发生跨版本迁移，也就不能把家族内边数变化解释为协议消费者切换家族。模块侧登记的 DetailViewPurify / DetailModulePurify / DetailUnitedModulePurify / DetailUnitedPresentationPurify / DetailAppPromotion / HomeVerticalDetail 等安装器与策略文件只提供了路径清单，本单元未读取其正文，故“定位器命中 detail_theseus_ugc/united 的具体类与方法、是否有兜底”均未知。complete_coverage=false，runtime_enabled=unknown。

证据：E000, E005, E012

#### 路径：detail_legacy

- 状态：absent
- 变化：目标与基线两侧完全一致：classes=0、compose_methods=0、external_invoke_edges=0，指纹同为 4f53cda1…2b945（空集合）；无结构新增或减少。
- 可能影响：对该路径的旧原生理化 Hook 在本版本既无静态命中证据，也无“功能消失”证据；若模块仍有指向该家族的选择器，可能直接落入未命中分支，影响与兜底逻辑未知。
- 验证：用 family_evidence 分别对 detail_legacy 在 target/baseline 两侧按类名重读，确认是否为选择器规则变化；再在真机抓取详情页 Activity/Fragment 栈与类加载日志，比对是否存在旧原生实现；同时读 DetailViewPurifyFeatureInstaller.kt 的定位器与 fallback 分支。
- 证据：E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：指纹由 aba2dbf1…c0d8 变为 729a51a7…b4ea；classes 1975→1976（+1）、compose_methods 25→25（不变）、external_invoke_edges 547→529（-18）；detail 两条 MOSS 协议定义/调用边两侧相同。
- 可能影响：指纹变化但 compose 数量不变，更像混淆改名/家族内合并而非新 Compose 样式；模块若按具体类名或方法签名锚定 UGC 详情模块，-18 条调用边可能意味着部分被锚点消失或其调用方被移到别的家族，导致净化点漏挂或空转，具体影响未知。
- 验证：用 family_evidence(detail_theseus_ugc, target/baseline) 拉取完整类清单按类名与方法体哈希做差，确认是改名还是真删；在 module_source 读 DetailModulePurifyFeatureInstaller.kt 与 DetailUnitedPresentationPurifyFeatureInstaller.kt，核对锚点类名/签名是否仍存在于目标 APK；真机验证时打开 UGC 视频详情页并记录每个净化点是否实际回调。
- 证据：E005, E012

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：指纹由 56c25b77…e4ccf 变为 cafecc5c…df274；classes 4633→4617（-16）、compose_methods 98→98（不变）、external_invoke_edges 4199→4196（-3）；相关 MOSS 协议计数未变。
- 可能影响：类数减少 16 而调用边基本持平，可能是重复包装层被合并或少量类被移出家族边界；对以类为单位的模块净化/展示策略可能少覆盖若干候选，是否影响实际渲染未知。
- 验证：用 family_evidence(detail_theseus_united, target/baseline) 对比类集合差集与 98 个 compose 签名是否一一对应；读 DetailUnitedModulePurifyPolicy.kt / DetailUnitedPresentationPurifyPolicy.kt 确认策略是否按类名白名单匹配；在宽屏/平板与横屏详情页各做一次真机走查。
- 证据：E005, E012

### pgc

PGV/番剧两条登记路径的静态变化方向相反，值得分别对待。pgc_legacy：classes 352→366（+14）、external_invoke_edges 425→455（+30）、compose_methods 两侧均为 0、指纹 a7bb4411…75aae（基线 60c8869e…00358，已变），说明旧原生 PGС 家族内部确实增加了类与调用边，但仍无 Compose 方法，不构成“旧原生被新样式替换”的证据。pgc_theseus：classes 2276→2262（-14）、external_invoke_edges 1179→904（-275）、compose_methods 134→131（-3）、指纹 1b944d7c…37839（基线 44b6f779…6cf14f，已变）；调用边下降幅度远超类数下降，是本次最大结构变化，既可能是真实裁剪/门面合并，也可能是调用边统计口径或家族边界划分变化，静态无法区分。协议侧 pgc_player_moss（12 定义/3 调用边）与 pgc_view_moss（14/7）在目标与基线完全一致，说明 PGC 协议定义与消费者数量未变，跨家族协议迁移假设缺乏支撑。模块侧 PgcAutoActivityPopupFeatureInstaller.kt / PgcAutoActivityPopupPolicy.kt / PgcAutoActivityPopupLocator.kt 仅有文件名证据，正文未读，因此“活动弹窗定位器是否仍命中 pgc_theseus 的入口类、是否有兜底”属未知；complete_coverage=false、runtime_enabled=unknown，不得宣称适配通过。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：指纹由 60c8869e…00358 变为 a7bb4411…75aae；classes 352→366（+14）、external_invoke_edges 425→455（+30）、compose_methods 两侧均为 0。
- 可能影响：旧原生 PGC 家族类与调用边同时增加，可能是新增原生页面/弹窗实现或家族边界扩张；模块若只对固定类名 Hook，新增长尾类不会被覆盖，活动弹窗等位置可能漏净化，实际是否触发未知。
- 验证：用 family_evidence(pgc_legacy, target/baseline) 拉完整类清单取差集，逐个确认新增 14 类的职责（是否属于活动弹窗/推荐卡）；读 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupPolicy.kt，核对其锚点是类名、资源 id 还是接口；真机在番剧详情与播放页分别验证弹窗是否被抑制。
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：指纹由 44b6f779…cf14f 变为 1b944d7c…37839；classes 2276→2262（-14）、external_invoke_edges 1179→904（-275）、compose_methods 134→131（-3）；pgc_player_moss 与 pgc_view_moss 计数未变。
- 可能影响：调用边大幅下降而类数与 Compose 方法仅小幅下降，说明保留下来的类对外调用显著减少，可能意味着公共服务调用被上移/合并为门面，或以接口/反射方式分发使静态边不可见；模块基于具体调用边或方法签名的 Hook 点可能因此断链，是否影响净化/弹窗抑制未知。
- 验证：用 family_evidence(pgc_theseus, target/baseline) 对比调用边端点集合，确认 -275 条边集中在哪些调用方；用 decompile_class 或 module_source 检查 PgcAutoActivityPopupFeatureInstaller.kt 的锚点方法在目标 APK 中是否存在同名同签名；真机在番剧页与播放器页开启模块日志，观察定位器命中/兜底分支并记录实际生效情况。
- 证据：E006, E012

### player

两条路径并存且都被静态证实有调用边：player_java 954 类/3308 外调边（基线 953/3308，指纹 f355088b→ac88f659），player_kotlin 458 类/836 外调边/37 个 Compose 方法（基线 455/841/37）。变化特征不对称：Java 侧类数 +1 而边数持平、Kotlin 侧类数 +3 而边数 -5，说明不是整族重构而是局部类增删与调用关系变动；Compose 方法数完全未变，倾向样式层未新增 Composable 入口，但不能排除服务端 A/B 无结构变化的情形。协议层 player_java_moss（18 定义/2 实际调用边）与 player_kotlin_moss（34/3）两版数值一致，协议面未变，风险集中在定位器命中的类/方法签名。仓库源码侧存在 PlayerSpeedLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller、PlayerCodecForceFeatureInstaller、SponsorPlayerLocator 等适配文件（E000 清单），但其定位实现与宿主方法名映射本轮未读到，安装器覆盖仍为未知，不得据此推断 Hook 生效。

证据：E007, E000

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类数 953→954（+1），外调边 3308→3308（持平），指纹 f355088b…→ac88f659…；changes 标记 player_java 为 structure_or_call_path_changed。
- 可能影响：player_java_moss 定义（18）与实际调用边（2）两版未变，协议层风险低；但若新增类替换了 PlayerSpeedLocator/PlayerBufferLocator 等适配件的目标方法所在类，反射定位可能验真失败并静默跳过，表现为倍速、缓冲、画质等开关无效。定位器实现本轮未读，影响范围未知。
- 验证：先对两版 player_java 做全量类清单与方法签名 diff，确认新增类名与是否被已有调用者引用；再用 module_source 读 PlayerSpeedLocator/PlayerBufferLocator/PlayerQualityFeatureInstaller 验证命中签名在 9170300 仍存在；最后真机核对对应开关是否生效。
- 证据：E007, E000

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数 455→458（+3），外调边 841→836（-5），Compose 方法 37→37（不变），指纹 b9a6ea0f…→c539764c…；changes 标记 player_kotlin 为 structure_or_call_path_changed。
- 可能影响：类增边减的组合提示控制面入口迁移或调用内联，若 5 条消失边属播放页控制链，依赖这些调用点的倍速/缓冲/画质/赞助商跳过 Hook 可能不再触发；Compose 方法数不变不支持“新增 Compose 播放样式”的结论。真实命中与兜底未知。
- 验证：用 family_evidence 取两版全量边清单，列出 5 条消失边的 caller→callee 签名并用 decompile_class 读调用者确认是否在播放页；真机上分别在竖屏、全屏、宽屏/平板入口触发对应功能，对照 LSPosed 安装与命中日志及 9170100 行为。
- 证据：E007, E000

### danmaku

danmaku_legacy 在目标与基线两侧均 absent（类数/边数 0，指纹同为 4f53cda1… 空集哈希），按登记语义该家族在本版静态不可见，不据此推断弹幕功能消失。danmaku_kotlin 仍为 static_invoke_observed：135 类/162 外调边/3 个 Compose 方法，基线 137/162/3，即类数 -2、边数与 Compose 方法数不变，指纹 38fdecc8→97597a31。该组合最可能是少量类删除、合并或迁移，也可能是混淆改名后类被重新聚合，尚不能判定为新样式；需用全量类清单 diff 判定丢失的 2 类是否属于弹幕渲染/净化路径。协议侧 danmaku_java_moss（22 定义/20 实际调用边）与 danmaku_kotlin_moss（46/10）两版一致，而 legacy 家族 absent 却有 20 条实际调用边，提示存在未归入登记家族的协议消费者，属具体待查线索而非新样式确认。仓库源码中有 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy（E000 清单），其定位目标与兜底逻辑本轮未读到，安装器覆盖记为未知。

证据：E008, E000

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线均 absent：类数 0、Compose 方法 0、外调边 0，指纹两侧同为 4f53cda1c8…（空集哈希），即无结构差异；changes 未在本单元声明该路径变化。
- 可能影响：该登记家族在当前版本无可观察类，legacy 侧的弹幕 Hook 无静态落点；但 absent 只表示本家族视图为空，不等于弹幕功能或旧实现消失，也不代表存在替代家族。对模块的可能影响为未知，需依赖运行时验证。
- 验证：用 family_evidence 复核两侧空集；再以 JADX 按已知旧弹幕类名（如 danmaku 渲染/DanmakuView 相关包）在 9170300 全文搜索，确认是否已迁入 danmaku_kotlin 或其他家族；真机播放视频观察弹幕是否正常渲染。
- 证据：E008, E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类数 137→135（-2），外调边 162→162（持平），Compose 方法 3→3（不变），指纹 38fdecc8…→97597a31…；changes 标记 danmaku_kotlin 为 structure_or_call_path_changed。
- 可能影响：边数与 Compose 方法数不变而类数减少，倾向类合并/迁移或混淆改名，而非新增样式；但若消失的 2 类承载散列净化锚点，DanmakuPurify 的 Hook 可能静默不生效；danmaku_java_moss 的 20 条实际调用边在 legacy absent 下无归属，提示未归类消费者，其是否被模块覆盖未知。
- 验证：用 family_evidence 取两版全量类清单 diff 点名消失的 2 类，用 decompile_class 检查其方法体哈希与原调用者；用 protocol_evidence 列出 danmaku_java_moss 20 条调用边 caller 并映射到登记家族；真机触发普通/全屏/宽屏弹幕，核对 DanmakuPurify 安装与命中日志。
- 证据：E008, E000

### story

story 两条登记路径处于两种状态：story_native 为 static_invoke_observed，story_kotlin 为 absent。目标包 story_native 有 2954 类、44 个 Compose 方法、1439 条外部调用边；基线为 2956 类、44 个 Compose 方法、1328 条边，指纹由 dafc… 变为 f410…。类数略降而调用边增加 111 条，属于需要解释的结构/调用路径变化，但不能据此认定出现新样式：DEX 重排、内联、编译器变化或代码迁移都能改变指纹与边数。story_kotlin 两侧均为 0 类、0 边且空集哈希相同，absent 不代表页面功能消失，Compose 实现可能被并入 story_native（该家族确有 44 个 Compose 方法），也可能落在未归类 DEX。StoryMoss/KStoryMoss 未登记为协议，跨家族消费者无法从现有协议视图判断。StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller 的安装条件本单元未读取，runtime_enabled 仍为 unknown。

证据：E000, E009, E012, E013

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类数 2956→2954（−2），Compose 方法 44→44，外部调用边 1328→1439（+111），指纹 dafc7376…→f410eec8…；变化登记为 structure_or_call_path_changed。
- 可能影响：若新增调用边来自 story 页新入口或路由，StoryPurifyFeatureInstaller/StoryActionIconsFeatureInstaller 的定位点可能只覆盖旧调用者；若为 DEX 重排或内联，则可能无实际语义变化，当前无法区分。
- 验证：对 9170100/9170300 的 story_native 类名与方法描述符集合做规范化差集，定位 +111 条边的具体调用者；真机安装后在两个 Installer 的 hook 点打点，记录安装成功数与命中数；对 44 个 Compose 方法所在类回溯调用链，确认是否属于 story 页渲染入口。
- 证据：E000, E009, E012, E013

#### 路径：story_kotlin

- 状态：absent
- 变化：基线与目标均为 0 类、0 个 Compose 方法、0 条外部调用边，空集指纹 4f53cda1… 两侧相同，未登记结构变化。
- 可能影响：absent 仅说明该命名家族未采集到类，不等同于页面 Kotlin/Compose 实现消失；若模块按 native/kotlin 双定位器分流，kotlin 侧候选可能为空，只能依赖 native 分支，存在覆盖缺口。
- 验证：读取 VersionAdapter 及 story 相关定位器的诊断输出，确认 kotlin 侧 HookPoint 列表长度与来源；真机抓取 story 页 Compose 语义树和类加载栈，核对实现是否归入 story_native 或未归类 DEX；检查 StoryMoss/KStoryMoss 的实际消费者。
- 证据：E009, E012

### mine

mine 两条路径均为 static_invoke_observed。mine_native 由基线 326 类、7 个 Compose 方法、94 条外部调用边变为 327 类、7 个、96 条，指纹 f6b18de5…→ae6321bd…，存在 +1 类/+2 边的小幅结构变化；mine_account_model 则由 132 类、0 个 Compose 方法、43 条边保持完全相同的计数，仅指纹 db7f2792…→ebf9deed… 变化。后者更符合混淆改名、DEX 重排或编译器产物差异，不宜当作新样式证据。需要关注的是组件过滤、阅读卡与 VIP 安装器的定位点是否仍命中新增类；本单元未读取 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller 及 MineComponentSnapshot 相关实现，也未见运行时安装日志。MineMoss/KMineMoss 未登记协议，服务端下发字段变化静态不可见，因此账号/VIP 解析影响保持 unknown。

证据：E000, E010

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类数 326→327（+1），Compose 方法 7→7，外部调用边 94→96（+2），指纹 f6b18de5…→ae6321bd…；变化登记为 structure_or_call_path_changed。
- 可能影响：新增类与两条调用边可能是新卡片、过滤入口或组件容器；MineComponentFilterFeatureInstaller 的过滤规则与 HostMineReadingCard 的组件识别可能因类名或结构变化漏匹配。
- 验证：对 mine_native 做类集合差集定位新增类，并核对其方法描述符；真机在“我的”页比对 MineComponentSnapshotStore 过滤前后组件列表；检查 MineVipFeatureInstaller 与组件过滤安装器的 hook 解析日志；确认 7 个 Compose 方法是否属于阅读卡或组件容器。
- 证据：E000, E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数 132→132、Compose 方法 0→0、外部调用边 43→43 均不变，仅指纹 db7f2792…→ebf9deed… 变化；资源变更计数 1 项，未显示该类模型的结构增删。
- 可能影响：计数与边数一致时，指纹变化更可能来自混淆改名、DEX 重排或编译器产物差异；若实际字段名或序列化布局变化，账号信息与 VIP 状态解析仍可能受影响，目前无结构证据。
- 验证：对两版本类名、字段与方法描述符做规范化差集，判断是否仅有改名/重排；真机登录态下核对“我的”页账号信息与 VIP 标识；追踪 AccountInterfaceV1Moss/KAccountInterfaceV1Moss 的消费者是否变化（当前协议未登记，需补登记后复核）。
- 证据：E000, E010

### F001：dynamic_compose 新增 10 个 Compose 方法是本批唯一 Compose 层实量变化，构成新样式候选而非已确认样式
事实：dynamic_compose 由 classes 1187→1234、compose_methods 141→151、external_invoke_edges 234→232，fingerprint 由 d1bf0fee… 变为 da87e05c…（E002）。与之对照，comment_compose 的 compose_methods 283→283 完全不变，仅结构哈希改变（E001），说明哈希变化本身不构成新样式证据。推断：dynamic_compose 增加的 10 个 @Composable 更可能是 Compose 卡片拆分/重构，其次是新增样式分支；因为对外调用边反而减少 2 条，符合内部实现扩张、入口收敛的形态。反例：若这 10 个签名来自重复包装层或混淆后同名拆分，则实际 UI 路径未变，当前计数无适配含义。无法判定的是新增方法的宿主类、调用者与激活条件，静态边也不解析接口分发。
反例与替代解释：可推翻本候选的证据：(1) 按 compose_signatures 做方法级比对后，若新增 10 个签名实为同一逻辑的重复包装或合成 lambda，则不是新样式；(2) 若 Dynam icPurify 现有锚点已包含这些新方法所在类，则不存在覆盖缺口；(3) 若真机开启 Compose 动态页后新增分支从未被调用（服务端未下发），则变化不进入运行路径。
建议：先用 compose_signatures 差集拿到 10 个新增方法名并反编译其宿主与调用方，判断是重构还是新样式；再在真机对新增分支构造含广告/屏蔽词的动态条目验证净化是否漏拦；模块侧核对 DynamicPurifyFeatureInstaller 的匹配集合是否需扩展。在获得运行证据前不得把此路径写成已适配。
证据：E002

### F002：comment_native_legacy 类数净增 11、调用边净增 43，原生补充绑定的目录可能对新增类未覆盖
事实：comment_native_legacy 由 classes 181→192（净增 11）、external_invoke_edges 220→263（净增 43）、compose_methods 恒 0，fingerprint 由 86f3175b… 变为 62bf1867…（E001/E015）；同页 comment_native_next（类 48→49、边 67→66）与 comment_native_exp3（类 54→55、边 52→56）仅为小幅漂移，说明 +43 条边不是全页统一重排带来的噪声，但净增类数不等于实际新增类数，须按类名集合差集区分「新增类」「删除类」与「改名类」。推断：若差集显示净增类与新调用者集中在原生补充绑定/包装层，则 CommentNativeBindingCatalog/CommentNativeSupplementBridge 的匹配点可能未覆盖，表现为样式或补充字段缺失而不抛错。反例：DEX 重排、编译器版本变化或内联体拆分会同时抬高类数与边数而不新增功能，此时目录无需扩展；若新增类全部为既有锚点类的内部 lambda/合成类并由锚点类直接派生，覆盖缺口亦不成立。模块侧两个 Catalog/Bridge 的源码本轮未读到正文，属未知，不能据此断言 Hook 失效。
反例与替代解释：可推翻本发现：若新增 11 个类全部为同一 owner 的内部 lambda/合成类且由既有锚点类直接派生，则目录无需扩展；若基线 9170100 与目标 9170300 之间仅有一次 dex 重排提交（可通过类名集合差集验证为空），则 +43 边同样不成立。
建议：先对 comment_native_legacy 做基线/目标类名集合差集，把「净增 11」拆成实际新增类、删除类与改名类三组，并对新增类反编译定位调用者，判断是否属评论条目的包装层；随后在真机对 comment.next_appearance 读取点与原生评论条目绑定点打命中日志，比较 9170100 与 9170300 的命中数差异；据此决定 CommentNativeBindingCatalog 是否需要新增条目。取得运行时命中证据前不更新该路径的 static_invoke_observed 状态。
证据：E001, E015

### F003：CommentClassicStyleLocator 以硬编码 owner 与实验键锚点做双家族定位，任何改名都会静默退化为空集
事实（源码 E012）：定位器把 NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision、KOTLIN_OWNER=kntr.base.dd.IDeviceDecisionKt、COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment 写成常量，并用 direct() 反射 getBoolean/getBool（首选）加缓存 HookPoint resolve() 兜底；kotlinApplicable() 以类存在性决定 Kotlin 家族是否参与，不存在的路径返回 emptyList() 而不报错；verified() 对 Kotlin 家族要求静态方法、参数 4 或 6 且 p[0] 为接口、p[2] 为 boolean，任一签名偏移即判不合格。锚点键集合包含 comment.next_appearance、comment.next_appearance_experiment_3、comment.kntr.enabled、comment.kntr.route.enabled、comment.kntr.landscape.enabled、comment.kntr.story.enabled。结合 E001：comment 页 5 家族 fingerprint 全变而 comment_compose 的 compose_methods 不变、comment_legacy_v2 类数下降 3，宿主侧存在改名/内联信号；若 Compose 入口 Fragment 或两个 owner 之一在 9.17.0 改名，ClassicStyle 判定将整体退化到缓存或空集，而日志层面不会抛异常。此为静态推断，未读到运行条件与服务端下发。
反例与替代解释：可推翻本推断：若真机上 direct() 对两个 owner 均返回非空且 verified 通过，则定位器未受影响，fingerprint 变化纯属重排；若 kotlinApplicable 为 false 而 NATIVE 家族仍工作，则退化范围仅限 Compose 侧，不构成整体失效；若缓存 HookPoint 命中（resolve 成功）则说明兜底有效，但缓存来自上一版本，需用当前 ClassLoader 验真后才可信。
建议：真机抓取 dex.assist.comment_classic 诊断日志，确认 locate() 中 NATIVE/KOTLIN 两侧是否为空、是否走了缓存兜底；逐项核对四个硬编码 owner 与六个锚点键是否仍存在于 9.17.0 的 dex 常量池；若 Kotlin 侧为空但 Compose 入口仍存在，则按新的 getBool 签名更新 verified() 与 owner 常量。
证据：E012, E001, E011

### F004：首页双路径类数与边数波动、compose 方法数不变——结构哈希变化不能当作新样式
事实：home_legacy 目标 744 类/228 外部边/compose 87，基线 766 类/198 边/compose 87；home_new_frame 目标 198 类/51 边/compose 33，基线 196 类/52 边/compose 33（E003）。两侧 fingerprint 均改变（home_legacy a56da1e1…→1ae88d27…，home_new_frame 34c59fa3…→d9422517…）。抽样：E014 仍见持有 Ltv/danmaku/bili/ui/main2/HomeFragmentV2 与 BasePrimaryMultiPageFragment$b 字段的匿名类及 AccountMineRequestResource 枚举；E013 仍见 Ltv/danmaku/bili/khome/widget/bubble 系列与 HomeFrameViewModel$dispatchAction$1。两者均为有界抽样（每家族只列少量类且正文截断），只能证明这些名字两侧都在，不能推出整套实现无新家族、无新 Compose 签名。推断：首页两条路径 compose_methods 两侧均为 87/33 不变，而类数 -22/+2、边数 +30/-1 波动，最符合 9170100→9170300 增量构建、混淆改名与 DEX 重排；结构哈希变化本身不等于新样式。影响：若属构建波动，既有定位器命中率不变；若 legacy 侧真实迁移了 HomeFragmentV2 相关方法签名，则依赖精确描述符的推荐净化、Tab 过滤、顶部栏/横幅 Hook 点可能失配。本轮可用证据中没有首页模块源码读取，安装器覆盖与兜底仍为未知。
反例与替代解释：可推翻当前推断的证据：(a) 差集中出现 catalog 内定位器实际引用的类或方法描述符消失，说明是真实代码迁移而非重排；(b) 对目标侧补更完整类清单后出现新的 Compose 签名或新 Home* 命名家族，说明新样式候选成立；(c) 真机日志显示 legacy 路径定位器全部未命中而 khome 路径命中，说明发生了实际样式切换而非构建波动。
建议：先做差集定位再谈适配：对两侧 home_legacy/home_new_frame 的方法描述符取差集，把消失项与 catalog 中 HomeFrameListHook.kt、HomeFrameTabLocator.kt 实际引用类名逐条比对；若引用项仍全部存在，则把本条降级为构建波动，并在真机只验证 HookEntry 安装日志中的定位器命中条目。
证据：E003, E013, E014

### F005：搜索两条路径 MOSS 契约规模完全未变，但多处搜索相关 Moss 未登记为协议项，跨家族消费者归属未知
事实：search_java_moss 定义 24、实际调用边 22，search_kotlin_moss 定义 52、实际调用边 18，目标与基线四个数字逐项相同（E004）。同时未注册协议清单中出现 app/search/v2/SearchMoss、app/search/v2/KSearchMoss、app/interfaces/v1/SearchMoss 与 KSearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/KSearchMoss、broadcast/message/main/NativePageMoss 等搜索相关项。推断：搜索契类的方法集合与静态调用规模未变，最可能是服务端契约稳定或静态台账口径一致；但这些契类尚未被登记为协议项，意味着可能存在未被归类的跨家族消费者。影响：若模块的搜索清理（推荐模块隐藏、默认词清理）绑定在已登记的 java/kotlin moss 方法上而真实消费走未登记契类，则静态可见的 Hook 覆盖会高估实际效果。定义数与调用边数单位不同，禁止相除推覆盖率；runtime_enabled 全部 unknown。
反例与替代解释：可推翻当前推断的证据：(a) 未登记 Moss 的调用方全部落在已登记的 search_native/search_compose 家族内，说明只是登记遗漏而非跨家族消费者；(b) 模块源码显示其绑定的是 View/Compose 层而非协议层，则协议未覆盖不影响该功能；(c) 真机日志显示 protobuf 拦截点确实被调用，说明协议层路径在实际运行中启用。
建议：把未登记搜索 Moss 逐个生成登记候选并抽查其调用方，判断是否存在非 search 家族消费者；同时读取 SearchHomeRecommendLocator.kt 与 SearchHomeRecommendPolicy.kt，列出实际绑定的类/方法/协议名，与 22 条 java 边、18 条 kotlin 边做映射，映射不上的键单列为未覆盖项，再交真机验证。
证据：E004

### F006：search_native 外部调用边 2818→2880 是本单元最大单项变化，需先排除真实新增调用点
事实：search_native 目标 2880 条外部调用边，基线 2818 条，净增 62，同时类数由 1705 降至 1701、compose_methods 恒为 2、fingerprint 变化（E004）。推断：边数增加与类数减少并存，可能是把原有调用集中到更少的类里（如内联/去包装层），也可能是新增服务端开关分支引入的新消费者；两种解释在汇总计数层面无法区分。影响：若为真实新增调用点且落在搜索推荐/默认词相关类，则旧签名 Hook 会漏掉新路径，表现为部分场景净化失效；若仅为调用边重新解析，则无功能影响。副作用风险：若新增调用来自分支并存（新旧两栈同时存活），可能出现重复净化或双份隐藏。未知项：未读搜索模块源码，也未取得差集明细。
反例与替代解释：可推翻当前推断的证据：(a) 差集显示新增边全部落在 catalog 已引用的类中，则属调用重新绑定，风险可降级；(b) 新增边来自测试或埋点类，与搜索净化无关；(c) 目标侧类数减少 4 且无新增 Compose 签名，若差集同时显示被吸收的旧边，可判定为内联/去包装而非新功能路径。
建议：对 search_native 两侧边集合做差集，定位新增 62 条边的来源类与方法，按类名归入“已有定位器引用/未引用”两组；对未引用组抽取 3~5 条读方法语义，确认是否为搜索页面的推荐或默认词通道；先做静态收敛，再决定是否需要真机复现。
证据：E004

### F007：detail_theseus 两路径指纹变化但 Compose 与 MOSS 协议计数不变，更像混淆改名/家族内搬运，模块锚点命中仍为未知
事实（E005，target 9170300 对 baseline 9170100）：detail_theseus_ugc 目标 1976 类/25 compose/529 边，基线 1975/25/547，指纹 aba2dbf1…→729a51a7…；detail_theseus_united 目标 4617/98/4196，基线 4633/98/4199，指纹 56c25b77…→cafecc5c…；detail_java_moss（32 定义/35 实际调用边）与 detail_kotlin_moss（76/38）两侧完全一致；detail_legacy 两侧同为 absent（classes=0、空集合指纹）。推断：两条路径 compose_methods 完全不变，协议定义与消费者数量不变，说明本次没有新增 Compose 样式实现、也没有协议层跨家族迁移；-18、-3 条外部调用边与类数微调（-0、+1、-16）同阶，更符合混淆改名、内联/合并、重复包装层消除或 DEX 重排，属候选解释而非结论。未知且本轮无法从证据判定：这些变化是否落在模块刻画的锚点上——本单元未读取 DetailViewPurify / DetailModulePurify / DetailUnitedModulePurify / DetailUnitedPresentationPurify / DetailAppPromotion / HomeVerticalDetail 任一安装器或策略正文，也未做类名/签名级差集，定位器命中率与兜底分支均未知。E012（CommentClassicStyleLocator.kt，NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision、NATIVE_ENTRY=com.bilibili.app.comment3.CommentV3Fragment、COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment，并依赖语义 DEX 查询后台调度）只能作为"模块定位器倾向以宿主精确类名/方法签名为锚点"的跨页面类比，不构成 detail 家族的直接证据。runtime_enabled 全为 unknown，不得据此宣称已适配。
反例与替代解释：若差集显示 529/4196 条边所涉类名全部保留、仅方法体哈希漂移，则本次指纹变化可判为混淆/重排噪声，应下调为无样式变化；若出现新的 Compose 入口签名或 detail MOSS 新增消费者，则"无新样式"推断被推翻；若真机日志显示定位器命中率与基线一致，则锚点断链风险被推翻；反之若安装器锚点在目标 APK 中缺失或签名变化且无兜底，则风险升级为待修复项。
建议：先对 detail_theseus_ugc 与 detail_theseus_united 分别拉取 target/baseline 完整类清单与方法体哈希，做类名+签名级差集，判定变化是改名/重排还是真实删减，再决定是否下调本发现；然后用 module_source 逐个读取 DetailViewPurifyFeatureInstaller.kt、DetailModulePurifyFeatureInstaller.kt、DetailUnitedModulePurifyFeatureInstaller.kt、DetailUnitedPresentationPurifyFeatureInstaller.kt（含对应 Policy），登记锚点类型（类名/方法签名/资源 id/接口）与未命中时的兜底分支，并核对其引用的类与方法在 9170300 类表中是否存在；最后在 UGC 详情、普通视频详情、横屏/平板宽屏三种形态各采集一次净化点命中日志。
证据：E005, E012

### F008：pgc_theseus 外部调用边 1179→904 大幅下降而同版本 pgc_legacy 反向 +30，并存栈迁移与模块锚点命中均待验证
事实（E006）：pgc_theseus classes 2276→2262（-14）、compose_methods 134→131（-3）、external_invoke_edges 1179→904（-275），指纹 44b6f779…→1b944d7c…；pgc_legacy classes 352→366（+14）、external_invoke_edges 425→455（+30）、compose 两侧为 0，指纹 60c8869e…→a7bb4411…；pgc_player_moss（12 定义/3 调用边）与 pgc_view_moss（14/7）两侧完全一致。推断：协议层无变化，两条 PGC 路径的变化都发生在家族内部；theseus 边数降幅约 23% 远大于类数降幅约 0.6% 与 compose 降幅约 2%，既可能是公共服务调用上移/门面化、或被替换为接口与反射分发使静态边不可见，也可能是家族边界划分或调用边统计口径变化，静态证据无法区分；legacy 反向增加提示 PGC 存在并存栈与家族边界移动，不能只以 theseus 单侧下结论。未知：PgcAutoActivityPopupLocator.kt / PgcAutoActivityPopupFeatureInstaller.kt / PgcAutoActivityPopupPolicy.kt 的锚点类型（类名、方法签名、资源 id 或接口）、无命中时的兜底路径与日志入口本轮均未读取；真机上 activity 实际走向 pgc_theseus 还是 pgc_legacy、服务端开关是否控制切换，均无证据。E012（CommentClassicStyleLocator.kt）是评论页定位器，只能作为"模块以宿主精确类名为锚点、并可能依赖后台语义 DEX 查询"的跨页面类比，不能作为 PGC 家族锚点或命中情况的证据。runtime_enabled=unknown、complete_coverage=false，不宣称适配通过。
反例与替代解释：若差集显示减少的边全部来自被删除或改为内部实现的类，而模块锚点类与方法完好、真机命中正常，则锚点断链推断被推翻，降级为重构噪声；若锚点方法在目标 APK 中缺失或签名变化且无兜底，则风险成立并需给出替代锚点；若 pgc_legacy 新增的 14 类正是 theseus 失去调用边的对端，则说明是并存栈切换而非样式新增，两条路径必须分别评估，不能合并结论；服务端 A/B 在无结构变化时静态不可见，不能据此认定样式已穷尽。
建议：先对 pgc_theseus 与 pgc_legacy 分别做端点级调用边差集：确认 -275 条边集中在哪些调用方、+30 条边是否与 legacy 新增 14 类同源（即并存栈/家族边界迁移而非新样式）；再读 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt、PgcAutoActivityPopupPolicy.kt，登记锚点类型、无命中兜底与日志入口，并核对锚点类/方法在 9170300 类表中是否存在同名同签名；最后在番剧详情页与播放页分别采集定位器命中/兜底日志，宽屏与平板形态各一次，并记录对应服务端实验分组。
证据：E006, E012

### F009：player_kotlin 类数 455→458 而外调边 841→836 下降，变化归属与播放器定位点影响均未定位
事实：目标 player_kotlin 458 类/836 外调边/37 Compose 方法，基线 455/841/37，指纹 b9a6ea0f→c539764c；同页 player_java 954/3308 对 953/3308，指纹亦变；两族 player_java_moss（18 定义/2 边）与 player_kotlin_moss（34/3）两版数值不变（E007）。推断：类数与外调边属不同单位、方向相反，只说明类集合与调用关系均有局部变动，尚不能定位到播放控制面；候选解释包括调用内联、入口迁移、少量工具/合成类增删、或经接口/服务端分支分发而静态不可见。Compose 方法数两版均 37，不支持“新增 Compose 播放样式”，也不支持“播放功能消失”。影响：仓库中存在 PlayerSpeedLocator/PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller、PlayerCodecForceFeatureInstaller、SponsorPlayerLocator 等候选适配件（E000 清单），若消失边恰为其命中方法所在调用点，反射定位可能验真失败并静默跳过；但这些文件正文本轮未读，命中签名与兜底未知，因此对倍速/缓冲/画质/赞助商的可能影响只能记为未知而非确定风险。边界：外调边不解析接口分发、不证明真机启用；工作树 dirty（source_tree_sha256 37745f8f…）需按文件哈希追溯。
反例与替代解释：若全量差集显示 5 条消失边仅属混淆改名后的同类调用（callee 方法体哈希不变），结构未实质变化；若变化集中在与播放无关的工具类，则对上述 installer 无影响；若真机日志显示各 Player* installer 均安装成功且功能生效，本推断被推翻。反向解释还包括服务端开关/接口分发导致的静态不可见，以及 Compose 方法数虽不变但既有 Composable 内部被改写的情形。
建议：①按类名与方法描述符对两版 player_kotlin 做规范化差集（family_evidence 为有界样本，需按名重读并用 decompile_class 补齐），点名新增 3 类与消失 5 条边的 caller→callee 精确签名，先排除混淆改名/DEX 重排；②用 module_source 读 PlayerSpeedLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller、PlayerCodecForceFeatureInstaller、SponsorPlayerLocator，登记各自锚点、验真方式与无命中兜底；③真机在 9170300 分别于竖屏、全屏、宽屏/平板入口触发倍速、缓冲、画质、赞助商跳过，记录 LSPosed 安装/命中/跳过日志并与 9170100 对照。
证据：E007, E000

### F010：danmaku_kotlin 类数 137→135 而边数与协议面无变化；danmaku_java_moss 的 20 条实际调用边 caller 尚未映射到登记家族
事实：danmaku_legacy 在目标与基线两侧均 absent（0 类/0 边/0 Compose，指纹同为 4f53cda1… 空集哈希）；danmaku_kotlin 135 类/162 边/3 Compose，基线 137/162/3，指纹 38fdecc8→97597a31；danmaku_java_moss（22 定义/20 条实际调用边）与 danmaku_kotlin_moss（46/10）两版完全一致（E008）。推断：协议层两版零变化，Kotlin 家族类数减少而边数、Compose 数不变，倾向少量类删除/合并/混淆改名而非新增样式；但需注意 java_moss/kotlin_moss 是协议消费者的语言分组，与 legacy/kotlin 的 UI 家族划分不同维度，因此 legacy absent 与 20 条 java_moss 边并存不构成“未登记消费者”的结论，其 caller 可能位于 danmaku_kotlin 或共享模块——在逐条映射前该点属待验证线索。影响：若消失的 2 类承载散列净化锚点，DanmakuPurify 可能静默不生效；若锚点落在稳定的 162 条调用面上则影响有限。边界：DanmakuPurifyFeatureInstaller/Policy 正文本轮未读，锚点、兜底与失败降级未知；定义数与调用边数不是同一单位，不能推导覆盖率；absent 不等于弹幕功能消失；服务端 A/B 若仅改视觉而无结构变化，静态不可见。
反例与替代解释：若差集显示消失的 2 类仅为混淆后合并的合成/匿名类且不承载净化逻辑，本发现可降为噪声；若 20 条 java_moss 调用边 caller 全部落在 danmaku_kotlin 家族内，则“未归类消费者”不成立，只剩协议分组与 UI 家族划分不同维度的说明价值；若真机日志显示净化规则在 9.17.0 正常命中，风险推断被推翻。
建议：①用 family_evidence 按名重读两版 danmaku_kotlin，点名消失的 2 类并用 decompile_class 检查其方法体哈希与原调用者，先排除混淆改名/DEX 重排；②用 protocol_evidence 列出 danmaku_java_moss 20 条调用边的 caller 类名，逐条映射到 danmaku_kotlin 或其他登记/未登记家族，再判断是否存在未归类消费者；③用 module_source 读 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy，登记锚点、兜底与失败降级；④真机分别以普通、全屏、宽屏/平板播放触发弹幕，核对净化规则安装与命中日志，并按服务端开关分组复测。
证据：E008, E000

### F011：story_native 外调边 +111 而 Compose 方法数不变，需先排除 DEX 重排/内联再谈新路由（候选）
事实（E009）：story_native 目标 2954 类、44 个 Compose 方法、1439 条外调边，基线 2956 类、44 个、1328 条，指纹 dafc7376…→f410eec8…；story_kotlin 两侧均为 0 类/0 边、空集哈希 4f53cda1… 相同，状态 absent。推断：类数略降而外调边增加 111 条属于需要解释的结构/调用路径变化，但 DEX 重排、内联、编译器变化、代码迁移或重复包装层都能同时改变指纹与边数，单凭边数不能判定出现新样式或新路由；Compose 方法数不变则说明没有新增 @Composable 入口的可见信号。旁证（不可外推）：E012 显示 comment 页 CommentClassicStyleLocator 以 com.bilibili.lib.dd.DeviceDecision 与 kntr.base.dd.IDeviceDecisionKt 为 native/kotlin 双锚点，并在复用缓存前用当前宿主 ClassLoader 验真；E013 的 home_new_frame 在 198 类中包含 33 个 Compose 方法，说明 Compose 方法并不必然单独形成 kotlin 家族。这两条都是其他页面的证据，只能支持“Compose 实现可能内嵌于 native 家族、模块存在双列表定位模式”的一般假设，不能推出 story 安装器的分流与兜底行为——StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller 源码本轮未读，其锚点来源、双列表结构与 kotlin 列表为空时的回退均记为未知。影响（待验证）：若 +111 条边对应 story 页新增渲染或操作入口，而安装器只命中旧调用者，则相关净化/图标 Hook 可能存在未覆盖入口；若为内联或重排，则无实际语义变化。StoryMoss/KStoryMoss 未登记，跨家族消费者同样未知。
反例与替代解释：若规范化差集显示 caller 集合与方法描述符基本一致，则 +111 条边更可能来自 DEX 重排、内联或编译器产物差异，新入口假设不成立；若 44 个 Compose 方法均为通用 UI 组件且与 story 页渲染无关，则 Compose 覆盖缺口推断不成立；若 story 安装器实际以方法签名而非类名为锚点，类数/边数变化对其命中率影响有限；若服务端 A/B 只切换样式而不改结构，静态证据无法看到，需真机按实验分组抓语义树才能排除。
建议：1) 对 9170100/9170300 的 story_native 做规范化类名与方法描述符差集，列出 +111 条边的 caller→callee，判定是否为同一批调用者的重排或新增入口；2) 读取 StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller 源码（按文件哈希记录），登记各自 HookPoint 来源与兜底分支，确认 story_kotlin 为空时是否只有 native 分支可用；3) 真机安装 9170300 对两个 Installer 的安装成功数与运行时命中数分别打点，并抓取 story 页 Compose 语义树核对渲染入口是否落在 story_native 的 44 个 Compose 方法所在类。
证据：E000, E009, E012, E013

### F012：mine_account_model 计数完全一致而指纹改变：先按改名/重排或方法体变更解释（候选）
事实（E010）：mine_account_model 目标与基线均为 132 类、0 个 Compose 方法、43 条外调边，指纹 db7f2792…→ebf9deed… 改变；同页 mine_native 为 326→327 类、7→7 个 Compose 方法、94→96 条边，指纹 f6b18de5…→ae6321bd… 改变。E000 另显示 base.apk 体积 +33KB、资源变更计数 1 项（added 0/removed 0/changed 1），该资源项的归属页面未确认，不能单独推断 mine 功能变化。推断：类数、Compose 方法数与外调边数三项完全一致时，指纹变化最可能来自混淆改名、DEX 顺序调整或编译器产物差异，但同样可能来自方法体字节码替换、字段类型/描述符调整或注解与序列化布局变化（结构指纹通常包含方法体摘要）；因此现有证据既不足以判定新样式，也不足以判定模型结构未变，只能判定“计数维度无变化”。影响（待验证）：若 mine_account_model 的字段名、类型或序列化布局确有改变，Mine 页账号信息、VIP 标识及依赖组件快照的过滤逻辑可能受影响；若仅是改名或重排，则模块按类名/方法签名定位的 Hook 可能因名称漂移而失配，风险落在定位而非功能。MineComponentFilterFeatureInstaller、MineVipFeatureInstaller 与 MineComponentSnapshot 相关实现本轮未读，解析点与 hook 条件仍为未知；MineMoss/KMineMoss 未登记协议，服务端下发字段变化静态不可见。
反例与替代解释：若描述符与方法体哈希差集显示仅有名称或顺序变化，则“未变”推断可维持，风险主要在锚点名称匹配；若差集出现方法体或字段类型变化，则应升级为结构变化并优先核查序列化与组件过滤规则；若资源变更 1 项经核实不属于 mine 页，则当前把它列为背景的理由不成立，应删除该引用；若 +1 新增类只是无关工具类，则组件过滤漏匹配风险应下调。
建议：1) 对 mine_account_model 做类名、字段描述符、方法描述符与方法体哈希的规范化差集，区分“仅改名/重排”与“方法体或类型真实变化”；2) 对 mine_native 做类集合差集，定位 +1 新增类并核对两条新增边的 caller→callee，判断是否落在组件过滤或阅读卡入口；3) 按文件哈希读取 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller 与 MineComponentSnapshot 相关实现，登记解析点、过滤条件与无命中兜底；4) 真机登录态比对“我的”页账号信息与 VIP 标识，并抓取 MineComponentSnapshotStore 过滤前后的组件列表。
证据：E000, E010

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
已逐条核对 comment 页登记 5 条路径（comment_legacy_v2、comment_native_legacy、comment_native_next、comment_native_exp3、comment_compose），path_reviews 均给出，status 逐字等于静态矩阵 evidence 值 static_invoke_observed，runtime_enabled 全部 unknown、module_coverage 全部 requires_installer_review，草案与本复核均未出现「适配通过」表述。计数事实（E001/E015）：legacy_v2 classes 583→580、edges 741→743、compose_methods 恒 0；native_legacy 181→192、220→263；next 48→49、67→66；exp3 54→55、52→56；compose 2428→2430、compose_methods 283→283、edges 1101→1103，5 个家族 fingerprint 全变。协议侧 comment_java_moss 50 定义/50 边、comment_kotlin_moss 130 定义/23 边与基线一致，Kotlin 23 条实际边远少于 130 定义，未落地定义不等于无消费者。需纠正草案一处表述：草案称 comment_native_legacy 是「本页唯一具有双向实量增长的家族」，但 exp3 亦为类 54→55、边 52→56 的双向增长，两处均须类级/签名级差集后才能定性，不能只对 native_legacy 做方向性解读。comment_compose 的 compose_methods 完全不变而哈希全变，按规则优先假设 DEX 重排、混淆改名或包装层，不列新样式候选。E011 仅为 comment_legacy_v2 target 侧 5 个类样本的有界摘录（total_classes=580），不能代表 580 类整体实现，也不能用于 native_legacy 判断。F003 所依赖的 E012 为截断摘录，仅含 owner/entry/anchor 常量定义，verified()/kotlinApplicable()/matchesKey 未出现在可见证据中，相关机制仍为待补证。
证据：E001, E015, E011, E012

### 复核页面：dynamic
已逐条核对 dynamic 页登记 3 条路径（dynamic_legacy、dynamic_compose、dynamic_opus），path_reviews 均给出，status 逐字等于静态矩阵 evidence 值 static_invoke_observed，runtime_enabled 全部 unknown、module_coverage 全部 requires_installer_review，草案未使用「稳定/完整/无影响」类措辞，本复核不声明适配通过。计数事实（E002/E016）：legacy classes 3255→3261、compose_methods 恒 103、edges 2075→2060（类增边减的反向组合）；compose classes 1187→1234、compose_methods 141→151、edges 234→232；opus classes 1350→1376、compose_methods 恒 94、edges 226→230；三条 fingerprint 均改变。协议侧 dynamic_java_moss 134 定义/134 边与基线一致，dynamic_kotlin_moss 定义为 382 不变、实际边 26→27，另有 OpusMoss/KOpusMoss、DynamicMoss、FeedMoss 等未登记协议，跨家族消费者静态不可判，新增那 1 条边归属家族未知。方法维度上 dynamic_compose 是本单元唯一 compose_methods 增加的家族（+10），但净 +47 类且对外边 -2，尚不能区分「Compose 重构拆分/合成 lambda」与「新增样式分支」，只能作候选；同页 legacy 与 opus 的 compose_methods 均不变，其哈希变化同样不能直接换算为新样式。dynamic_opus 的扩张落在非 Compose 层，是否引入未登记协议消费者无证据。模块侧 DynamicPurifyFeatureInstaller/DynamicPurifyPolicy/KotlinDynamicMossWatch 源码本轮未读到正文，草案已如实记为未知，本复核维持该未知，不做 Hook 覆盖推测。服务端 A/B 视觉变体在无结构变化时静态不可见，不能宣称样式已穷尽。
证据：E002, E016

### 复核页面：home
两条登记路径并存，evidence 均为 static_invoke_observed，runtime_enabled unknown，module_coverage requires_installer_review，故不宣称适配通过。计数与预取证据一致：home_legacy 目标 744 类/87 compose/228 外部边，基线 766/87/198；home_new_frame 目标 198 类/33/51，基线 196/33/52，两侧 fingerprint 均改变（E003，home_legacy a56da1e1…→1ae88d27…，home_new_frame 34c59fa3…→d9422517…）。E014 抽样仍见持有 Ltv/danmaku/bili/ui/main2/HomeFragmentV2 与 BasePrimaryMultiPageFragment$b 字段的匿名类及 AccountMineRequestResource 枚举；E013 抽样仍见 khome 的 widget/bubble 系列与 HomeFrameViewModel$dispatchAction$1；但两者都是有界抽样且正文截断，只能说明这些名字两侧都在，不能外推整套实现无新家族。home_legacy 类数 -22、边 +30 的幅度大于 home_new_frame 的 +2/-1，仍需方法描述符差集才能区分重排与迁移，因此 fingerprint 变化不构成新样式证据。本会话可用证据无首页模块源码读取（E012 属评论页），HomeFrameListHook/HomeFrameTabLocator/HomeBanner/HomeTopBar 等安装器命中、兜底与平板/宽屏分支记未知；E000 中 HomeMoss、KHomeMoss 在未注册协议清单内，E003 protocols 为空，跨家族消费者未知。服务端 A/B 视觉变体无结构变化时静态不可见。
证据：E003, E013, E014, E000

### 复核页面：search
两条登记路径 evidence 均为 static_invoke_observed，runtime_enabled unknown，module_coverage requires_installer_review。计数核对一致：search_native 目标 1701 类/2 compose/2880 外部边，基线 1705/2/2818；search_compose 目标 3136 类/562/607，基线 3146/562/614，fingerprint 两侧均改变（E004）。两侧 compose_methods 恒定（2/562）支持“非新 Compose 样式”的替代解释，但 search_native 外部边 +62 是本单元最大单项变动，端点半差集未做，不能判为无害或无覆盖影响。协议侧 search_java_moss 24 定义/22 边、search_kotlin_moss 52/18 在目标与基线逐项相同（E004），仅说明已登记契约层的静态规模未变；定义数与调用边数单位不同，不相除推覆盖率。E000 未注册协议清单含 app/search/v2/SearchMoss 与 KSearchMoss、app/interfaces/v1/SearchMoss 与 KSearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/KSearchMoss，是否存在跨家族消费者未抽查。搜索模块源码（SearchHomeRecommendLocator/Policy、SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller）本会话可用证据未读到，安装器互斥条件与兜底记未知。fresh_refresh 为空，本单元仅依赖 E003/E004 预取摘录（有界抽样、正文截断）。
证据：E004, E000

### 复核页面：detail
复核认为页级事实与 E005 重新取证逐项吻合：detail_legacy 在 target/baseline 两侧均为 classes=0、compose_methods=0、external_invoke_edges=0、指纹 4f53cda1…2b945（空集合），草稿判为 absent 并明确指出缺席不等于页面功能消失符合要求；detail_theseus_ugc 目标 1976/25/529、基线 1975/25/547（aba2dbf1…→729a51a7…），detail_theseus_united 目标 4617/98/4196、基线 4633/98/4199（56c25b77…→cafecc5c…），detail_java_moss 32/35 与 detail_kotlin_moss 76/38 两侧一致。三条 path_reviews 的 status 逐字使用矩阵 evidence 值（absent / static_invoke_observed），runtime_enabled=unknown、module_coverage=requires_installer_review、complete_coverage=false 均保留，未出现“适配通过”。以 compose_methods 两侧不变削弱“新增 Compose 样式”解释属合理候选推断。缺陷：草稿未读任何 detail 定位器正文，但 F007 引用的 E012 是评论页 CommentClassicStyleLocator.kt，只能作跨页面类比，不构成 detail 家族锚点证据，已在 F007 修订中显式降级；detail_legacy 两侧同时 absent 的成因（选择器规则变化、家族边界调整还是旧原生确已移除）仍未判定，保留了最小补证任务与真机类加载栈验证方法。
证据：E000, E005, E012

### 复核页面：pgc
复核认为页级数值全部与 E006 重新取证吻合：pgc_legacy 目标 366/0/455、基线 352/0/425（60c8869e…→a7bb4411…），pgc_theseus 目标 2262/131/904、基线 2276/134/1179（44b6f779…→1b944d7c…），pgc_player_moss 12/3 与 pgc_view_moss 14/7 两侧一致。两条 path_reviews 的 status 逐字使用 static_invoke_observed，未改写为通过；runtime_enabled=unknown、complete_coverage=false 保留。对 pgc_theseus 边数降幅（-275）远大于类数（-14）与 compose（-3）降幅的观察准确，并同时给出门面化/调用上移与家族边界或统计口径变化两种解释，符合不得据计数差异推断新样式的要求；pgc_legacy 反向 +14 类/+30 边被用于提示并存栈与家族边界移动，避免单侧结论。需修正：页级评估中“本次最大结构变化”应限定为本单元内（其他登记页未在本单元取证），“PGС”为字符笔误，不影响事实。缺陷同 detail：F008 引用 E012（评论页定位器）不成立，PgcAutoActivityPopupLocator/FeatureInstaller/Policy 正文未读，弹窗抑制的锚点与兜底须记为未知并在 F008 修订中保留为补证任务。
证据：E000, E006, E012

### 复核页面：player
两条登记路径 status 与静态矩阵逐字一致（player_java / player_kotlin 均为 static_invoke_observed），runtime_enabled=unknown、module_coverage=requires_installer_review，草稿未出现“适配通过”类表述，符合本轮要求。数值经 E007 复核无误：player_java 类 953→954、外调边 3308→3308、Compose 0；player_kotlin 类 455→458、外调边 841→836、Compose 37→37；两族指纹均变化但协议层 player_java_moss（18 定义/2 边）与 player_kotlin_moss（34/3）两版完全相同。类数与调用边是不同单位，+3 类与 -5 边不能相除或互推覆盖率；指纹变化也不等于新样式，混淆改名、DEX 重排、重复包装层均可产生同向差异，需全量类/签名 diff 才能判定。并存栈方面：本单元仅两族，未见第三条播放器登记路径，Compose 方法数未变不支持“新增 Compose 播放样式”，也不支持“播放功能消失”。源码侧：E000 仅提供 PlayerSpeedLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller 等候选文件清单（工作树 dirty，按 source_tree_sha256 37745f8f… 追溯），其正文本轮未读，因此这些安装器的命中签名、兜底分支与安装条件全部记为未知，不得据文件名推断 Hook 覆盖。宽屏/平板、服务端 A/B 与实验开关条件亦未读到，属未解路径。
证据：E007, E000

### 复核页面：danmaku
两条路径 status 与矩阵一致：danmaku_legacy=absent、danmaku_kotlin=static_invoke_observed，runtime 与 installer 覆盖均未知，草稿明确声明 absent 不等于弹幕功能消失，处理正确。数值经 E008 复核：legacy 两侧类/边/Compose 全为 0 且指纹同为 4f53cda1…（空集哈希），即两版无差异；danmaku_kotlin 类 137→135、外调边 162→162、Compose 3→3、指纹 38fdecc8…→97597a31…。danmaku_java_moss（22 定义/20 实际调用边）与 danmaku_kotlin_moss（46/10）两版完全一致，协议面无结构信号；定义数与调用边数不是同一单位，不能据此推导净化覆盖率。需修正一处推断：java_moss / kotlin_moss 是协议消费者的语言分组，与 danmaku_legacy / danmaku_kotlin 这两个 UI 家族不是同一划分维度，故 legacy 家族 absent 不能直接推出“存在未归入登记家族的消费者”，20 条边的 caller 完全可能落在 danmaku_kotlin 或共享模块内，必须逐条映射后才能定性；该点已在对 F010 的修订中落实。源码侧 DanmakuPurifyFeatureInstaller / DanmakuPurifyPolicy 正文（含锚点、失败降级、服务端开关分支、全屏/宽屏与平板入口）本轮未读，记为未知。
证据：E008, E000

### 复核页面：story
复核通过（静态证据层面）。草稿 story 页结论与预取证据一致：story_native 目标 2954 类/44 个 Compose 方法/1439 条外调边，基线 2956/44/1328，指纹 dafc7376…→f410eec8…，路径状态 static_invoke_observed 与静态矩阵 evidence 值逐字一致；story_kotlin 两侧均 0 类/0 边且空集哈希 4f53cda1… 相同，状态 absent 也逐字一致。评估正确地说明 absent 不等于页面功能消失，并把 Compose 实现可能并入 story_native 或落入未归类 DEX 作为待验证替代解释，没有把 +111 条边直接判定为新样式，符合“结构哈希变化不等于新样式”。两条 path_reviews 给出了具体到可执行的补证动作（规范化描述符差集定位 +111 边调用者、Installer 打点、Compose 语义树抓取），并明确 Runtime/安装器覆盖为 unknown。需注意的唯一薄弱处：草稿 F011 借用 E012（comment 页 CommentClassicStyleLocator）与 E013（home_new_frame）推断 story 安装器的 native/kotlin 双列表行为，属跨页类比，story 两个安装器源码本轮未读，不能作为 story 覆盖结论；已在 F011 修订中降级表述。StoryMoss/KStoryMoss 未登记为协议，跨家族消费者与运行条件均记为未知，未出现“稳定/无影响/适配通过”类表述。
证据：E000, E009, E012, E013

### 复核页面：mine
复核通过（静态证据层面）。mine 页计数与 E010 完全对应：mine_native 326→327 类、Compose 方法 7→7、外调边 94→96，指纹 f6b18de5…→ae6321bd…；mine_account_model 132→132、0→0、43→43 不变而指纹 db7f2792…→ebf9deed… 改变；两条路径状态 static_invoke_observed 与静态矩阵 evidence 值一致，runtime_enabled 与 module_coverage 保持 unknown/requires_installer_review，未宣称适配通过。评估对 mine_account_model 把指纹变化优先解释为混淆改名/DEX 重排/编译产物差异，方向正确且未当作新样式证据；不过“类数与边数一致”并不能排除方法体字节码或字段类型变化（指纹通常包含方法体哈希），草稿原文只列了改名与重排两种解释，已在 F012 修订中补入该替代解释并要求描述符+方法体哈希差集。资源变更 1 项在草稿中仅作背景引用，未据此推断功能变化，可接受但其归属仍为未知。MineMoss/KMineMoss 未登记，服务端下发字段变化静态不可见这一点被明确保留为未知；+1 类/+2 边与组件过滤、阅读卡入口的关系仍待定位，草稿给出的验证动作（类集合差集、MineComponentSnapshotStore 过滤前后比对、Installer hook 日志）具体可执行。
证据：E000, E010

- F001 / retained：计数断言与 E002/E016 完全一致：dynamic_compose classes 1187→1234、compose_methods 141→151、external_invoke_edges 234→232、fingerprint d1bf0fee…→da87e05c…；对照项 comment_compose compose_methods 283→283、dynamic_legacy 103→103、dynamic_opus 94→94 亦可由 E001/E002 支持，「本单元唯一 Compose 方法数增加的家族」成立。level=candidate 恰当：静态计数只证明结构位移，未读到新增 10 个 @Composable 的宿主类、调用方或激活条件；草案已明确不得写成已适配，并列出重构拆分/合成 lambda、锚点已覆盖、服务端未下发三条可推翻路径。结论范围限于本单元 comment+dynamic 两页，不扩及其他已登记页。（E002, E016, E001）
- F002 / revised：核心方向被 E001/E015 支持：comment_native_legacy classes 181→192、external_invoke_edges 220→263、compose_methods 恒 0、fingerprint 86f3175b…→62bf1867…，与同页 next（边 67→66）、exp3（边 52→56）的小幅漂移确有量级差异。但有两处须修正：(1) 类数 181→192 是净增 11，不等于「新增 11 个类」，可能同时存在删类与增类；(2) 原 evidence_ids 误引 E011，该证据是 comment_legacy_v2 target 侧 5 个类样本（total_classes=580），与 native_legacy 无关，改以 E001/E015 的家族 summary 为依据。另保留：CommentNativeBindingCatalog/CommentNativeSupplementBridge 源码本轮未读，目录是否覆盖新增类仍为未知，不得写作已失效。（E001, E015）
- F003 / needs_more_evidence：方向可保留但细节超出可见证据：E012 为被截断的 module_source 摘录，可见部分仅到 NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision、NATIVE_ENTRY、KOTLIN_OWNER=kntr.base.dd.IDeviceDecisionKt、COMPOSE_ENTRY 与 NATIVE_ANCHOR=comment.next_appearance 等常量声明，未出现 verified() 的静态方法/参数位约束、kotlinApplicable() 的类存在性判定、matchesKey 的锚点键集合，也未出现「返回空列表不报错」「缓存 HookPoint 兜底」与诊断日志 dex.assist.comment_classic 的调用位置，故这些机制不能按已读事实陈述。另一半依据也偏弱：5 个家族 fingerprint 全变而 comment_compose 的 compose_methods 283→283 不变（E001/E015），只能说明结构位移，不能证明四个硬编码 owner 之一被改名。宿主运行条件与服务端下发均未读到，缺口明确。（E012, E001, E015）
- F004 / revised：计数部分与 E003 逐项吻合（home_legacy 744/87/228 vs 766/87/198；home_new_frame 198/33/51 vs 196/33/52），E013/E014 抽样确实显示 HomeFragmentV2 字段匿名类、AccountMineRequestResource 与 khome bubble/HomeFrameViewModel$dispatchAction$1，未见命名家族更替。但原文“compose_methods 四条路径全部保持不变（87/33）”把 search 误并入 home；“±2~24 区间波动”漏掉 home_legacy 边数 +30；“未见新命名家族或新 Compose 签名集合”超出 E013/E014 每家族仅少量类的有界抽样（正文截断），不能外推为整套实现结论。故修订措辞与证据边界，保留 candidate 级别与差集优先的下一步。（E003, E013, E014）
- F005 / retained：已用 E004 重新核对：search_java_moss 24 定义/22 边、search_kotlin_moss 52/18 边在目标与基线逐项相同；未注册协议清单中 app/search/v2/SearchMoss、app/search/v2/KSearchMoss、app/interfaces/v1/SearchMoss 与 KSearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/KSearchMoss、broadcast/message/main/NativePageMoss 均在 E000 中可查。原文已把跨家族消费者写成推断/未知而非结论，且明确禁止以定义数除边数推覆盖率、runtime 全部 unknown，未出现“已适配/已覆盖”表述。MOSS 拦截点的实际触发静态不可判定，needs_runtime 级别成立。（E004, E000）
- F006 / retained：E004 复核：search_native 外部边 2818→2880（+62）、类数 1705→1701、compose_methods 恒为 2、fingerprint 变化，数字与原文一致；该 +62 确为 home/search 四路径中最大的正变动（home_legacy +30）。原文明确“汇总计数层面无法区分”内联/去包装与新增分支/新消费者两种解释，仅给出条件性影响，并把差集未做列为未知，未把边数增量当作 Hook 面扩大或覆盖率提升，符合不得用边数推覆盖的要求，candidate 级别合适。（E004）
- F007 / revised：数值与 E005 完全一致（ugc 1976/25/529 vs 1975/25/547；united 4617/98/4196 vs 4633/98/4199；两条 MOSS 32/35、76/38 两侧相同）；"compose 未变且 MOSS 未变，因此指纹漂移不足以推出新样式"成立，替代解释与反例条件也已给出。缺陷：E012 是评论页 CommentClassicStyleLocator.kt，与 detail 家族无直接关系，不能支撑"detail 定位器锚点可能断链"；本轮未读任何 detail 安装器正文，该风险应显式记为未知。据此修订措辞，证据编号不变。（E005, E012）
- F008 / revised：pgc 计数与 E006 完全一致（theseus 2262/131/904 vs 2276/134/1179；legacy 366/0/455 vs 352/0/425；两份 MOSS 两侧不变），"调用边降幅远大于类数与 compose 降幅、legacy 方向相反"的观察成立，且已给出门面化/统计口径两类替代解释，判断可保留。缺陷同 F007：E012 是评论页定位器，不能支撑 PGC 活动弹窗定位器的锚点风险；本轮未读 PgcAutoActivityPopupLocator/FeatureInstaller/Policy 正文，须把该风险明确记为未知并保留补证任务。据此修订措辞。（E006, E012）
- F009 / revised：事实部分经 E007 核对全部成立（player_kotlin 455→458 类、841→836 边、37 Compose 不变；player_java 953→954、3308→3308；两族指纹变化；两族 MOSS 定义与边不变），且已限定为 candidate、未宣称适配通过。但标题与论证把“控制面定位点位移”写得比证据更确定：类数与外调边是不同单位，-5 条边既可能是调用内联/迁移，也可能是与播放控制链无关的工具类或混淆重排，本轮未读到任何 Player* 定位器/安装器正文，无法把变化归入倍速/缓冲/画质/赞助商任一功能链；另需说明 family_evidence 仅返回有界样本，所谓“全量类清单 diff”需按名重读与反编译配合。故修订措辞与验证步骤，等级保持 candidate。（E007, E000）
- F010 / revised：事实经 E008 核对全部成立（legacy 两侧 absent 且空集哈希相同；danmaku_kotlin 137→135、162 边与 3 Compose 不变；两族 MOSS 定义与调用边两版一致），needs_runtime 等级与“未读到 installer 源码”的边界声明也恰当。但标题把“存在未归类弹幕协议消费者”当作结论，而 danmaku_java_moss / danmaku_kotlin_moss 是协议消费者的语言分组，与 danmaku_legacy / danmaku_kotlin 这两个 UI 家族不是同一划分维度，20 条边的 caller 完全可能落在 danmaku_kotlin 或共享模块内；在逐条映射 caller 之前不能断言存在未登记消费者。故修订标题与分析，把该项降为待验证的映射任务，等级仍为 needs_runtime。（E008, E000）
- F011 / revised：事实部分与预取证据一致：E009 显示 story_native 2956→2954 类、Compose 方法 44→44、外调边 1328→1439、指纹改变；story_kotlin 两侧 0/0/0 且空集哈希相同。E012 的 DeviceDecision/IDeviceDecisionKt 双锚点与“复用前用宿主 ClassLoader 验真”均有原文支撑，E013 的 home_new_frame 198 类含 33 个 Compose 方法亦有支撑。问题在于草稿把 comment 页定位器（E012）与 home 家族（E013）当作 story 安装器行为的依据，属跨页类比；story 两个 Installer 源码本轮未读，不能写成对 story 分流/兜底的推断性描述。因此保留候选级结论与 +111 边需复核的判断，修订为显式标注跨页旁证与未知项，并把读取 story 安装器源码列为前置验证，不改变 page 与 evidence_ids。（E000, E009, E012, E013）
- F012 / revised：计数事实与 E010 完全一致（mine_account_model 132/0/43 两侧相同、指纹改变；mine_native 326→327、94→96），把指纹变化优先按混淆改名/DEX 重排解释的方向可保留。但草稿原文只列了改名与重排两种解释，未覆盖“类数与边数不变而方法体字节码、字段类型或序列化布局发生变化”这一可能，而结构哈希通常包含方法体摘要，恰是唯一有变化的维度；此外 E010 的摘要不含资源改动信息，资源变更 1 项来自 E000，其归属页面未确认。因此保留候选级结论，补齐替代解释并把“描述符 + 方法体哈希差集”加入最小补证，不改变 page 与 evidence_ids。（E000, E010）

### 尚未解决的证据缺口

- [1] 完整重读 CommentClassicStyleLocator.kt（当前 E012 摘录截断），确认 verified()、kotlinApplicable()、matchesKey 与全部锚点键的真实实现后再定级 F003。
[2] 对 comment_native_legacy 做基线/目标类名集合差集，把 classes 181→192 的净增拆成实际新增、删除与改名三组，并定位 +43 条外部调用边的调用者。
[3] 对 dynamic_compose 按 compose_signatures 做方法级差集，取得新增 10 个 @Composable 的宿主类与调用方，判定是 Compose 重构拆分还是新增样式分支。
- [4] 对 comment_native_exp3（类 54→55、边 52→56）与 comment_native_next（类 48→49、边 67→66）做类级/签名级差集，区分混淆改名、DEX 重排与真实调用点变化；E011 仅 5 个类样本，不能代表 comment_legacy_v2 的 580 类。
[5] 对 comment_legacy_v2 类数 583→580 与边 741→743 方向相反的组合做类级差集，确认是类合并/内联还是新增调用点。
[6] 对 dynamic_legacy 减少的 15 条 external_invoke_edges 做调用者端点差集，确认是否迁往 Compose/Opus 家族，或仅是接口分发/内联导致静态不可见。
- [7] dynamic_kotlin_moss 由 26→27 的那 1 条新增边归属哪个家族、是否存在跨家族消费者，尚无证据。
[8] OpusMoss/KOpusMoss、DynamicMoss、FeedMoss、ReplyMoss/KReplyMoss 等 unregistered_protocol 未登记，跨家族消费者与安装器覆盖无从判断。
[9] CommentNativeBindingCatalog、CommentNativeSupplementBridge、CommentComposePurifyBridge、CommentComposeViewAccess、DynamicPurifyFeatureInstaller、DynamicPurifyPolicy、KotlinDynamicMossWatch 源码本轮未读到正文，不得推测其 Hook 覆盖与兜底行为。
- [10] 全部 8 条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本轮无安装器命中日志与真机运行时证据，需在 9170300 上抓取各 installer 安装/跳过与命中数并与 9170100 对照。
[11] 评论区与动态页的平板/宽屏分支、服务端 A/B 与实验开关（如 comment.next_appearance 系列键、kntr 各开关）是否控制样式切换，静态不可见，需真机按分组采样。
[12] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），本轮未逐文件核对 dirty 改动，后续须按文件哈希追溯而非依赖目录推断。
- [13] 首页模块源码未读：HomeFrameListHook.kt、HomeFrameTabLocator.kt、HomeBannerFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt、HomeComponentFilterFeatureInstaller.kt、HostHomeCardSpacingHooks.kt 的实际 Hook 点、legacy/khome 绑定与无命中兜底仍为未知，需按固定文件哈希读取（source_tree_sha256 37745f8f…，working_tree_dirty=true）。
[14] home_legacy 未做方法描述符差集：类数 -22、外部边 +30 的具体消失/新增项未定位，无法区分混淆重排、去包装与真实迁移。
[15] home_new_frame 类数 +2、外部边 -1 的来源类未定位，HomeFrameViewModel.dispatchAction 与 bubble 类型是否被模块引用未核对。
- [16] home 页 E003 protocols 为空，HomeMoss/KHomeMoss 仅在未注册协议清单（E000）中出现，是否存在跨家族消费者、是否被模块解析点覆盖未知。
[17] search_native 新增 62 条外部调用边未做端点半差集，无法判断是新增服务端开关分支、内联重绑还是台账口径变化，也无法判断是否落在搜索推荐/默认词通道。
[18] search_compose 类数 -10、边 -7 未定位；562 个 compose 签名仅知总数相同，未逐项比对签名集合是否一致。
- [19] 搜索模块源码未读：SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchHomeRecommendFeatureInstaller.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt 的绑定签名、Compose/原生互斥条件与兜底仍未核实。
[20] 未登记搜索 Moss（app/search/v2、app/interfaces/v1、broadcast/message/search、broadcast/message/main）的调用方归属未抽查，跨家族消费者问题待补证。
[21] 全部四条路径 runtime_enabled 仍为 unknown、module_coverage 为 requires_installer_review，尚未取得 9170300 真机 HookEntry 与定位器安装/命中日志。
- [22] 首页新旧双栈与搜索 Compose/原生双栈的切换条件（服务端开关、实验分组、平板/宽屏分支）静态不可见，是否存在重复净化/双份隐藏未验证。
[23] 服务端 A/B 视觉变体在无结构变化时静态不可见，本轮不能宣称首页/搜索样式已穷尽。
[24] 本单元 fresh_refresh 为空，仅依赖 E003/E004 预取摘录（每家族有界样本、正文截断），缺少更细粒度的类清单与边列表证据。
- [25] detail 与 pgc 均未做类名/签名级 target↔baseline 差集：detail_theseus_ugc（-18 边）、detail_theseus_united（-16 类/-3 边）、pgc_theseus（-275 边）、pgc_legacy（+14 类/+30 边）的具体变化集合未知，混淆改名与真实删减无法区分。
[26] 本单元未读取任何 detail 安装器/策略正文（DetailViewPurify、DetailModulePurify、DetailUnitedModulePurify、DetailUnitedPresentationPurify、DetailAppPromotion、HomeVerticalDetail），各家族锚点类型、命中条件与未命中兜底均未知。
[27] 本单元未读取 PgcAutoActivityPopupLocator.kt / PgcAutoActivityPopupFeatureInstaller.kt / PgcAutoActivityPopupPolicy.kt 正文，PGC 活动弹窗抑制的锚点与兜底路径未知。
- [28] detail_legacy 在 target 与 baseline 两侧同时为 absent 的成因未判定：需确认是家族选择器规则变化、代码并入其他家族，还是旧原生详情实现确已移除；真机 Activity/Fragment 栈与类加载日志采样尚未进行。
[29] 服务端 A/B 与实验开关是否控制 detail/pgc 样式切换无静态证据，真机分账号对照未做，不能宣称样式已穷尽。
[30] 全部 detail/pgc 路径 runtime_enabled=unknown、module_coverage=requires_installer_review、complete_coverage=false，安装器级别覆盖检查在基线与目标上均未执行。
- [31] detail_java_moss(32/35)、detail_kotlin_moss(76/38)、pgc_player_moss(12/3)、pgc_view_moss(14/7) 是否存在跨家族消费者未核对；未登记协议中 view/pgc gateway 等消费者的家族映射亦未完成。
[32] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，head 5422fad1…），需按文件哈希追溯；本单元未取得 detail/pgc 相关源码文件的逐文件哈希记录。
[33] 未验证真机安装后 detail 与 pgc 各 Hook 点是否安装成功、是否被版本适配层跳过，也无 9170100 与 9170300 的安装日志对照。
- [34] player_kotlin 新增 3 类与消失 5 条外调边的精确 caller→callee 签名未取得，无法判定是混淆改名/重排还是真实迁移，也未定位到播放控制链。
[35] PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller、PlayerCodecForceFeatureInstaller、SponsorPlayerLocator 的源码正文本轮未读（仅见 E000 文件清单），锚点、验真方式、无命中兜底与安装条件均为未知。
[36] player 页是否存在第三条并存栈（如宽屏/平板专用播放器、服务端开关或实验分组分支）未取证；两条登记路径的 runtime_enabled 与 module_coverage 仍为 unknown/requires_installer_review。
- [37] danmaku_kotlin 137→135 消失的 2 个类名、方法体哈希与原调用者未取得，无法判断是否承载散列净化锚点。
[38] danmaku_java_moss 20 条实际调用边的 caller 未逐条映射到登记家族；java_moss/kotlin_moss（语言分组）与 legacy/kotlin（UI 家族）划分维度不同，需协议侧 caller 清单才能定性。
[39] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 正文未读，净化锚点、失败降级路径与普通/全屏/宽屏入口覆盖未知。
- [40] 两页均无真机证据：LSPosed 安装成功数、运行时命中数与 9170100 对照缺失，所有 runtime_enabled 与 module_coverage 结论无法前进。
[41] 服务端 A/B 与实验开关对播放器/弹幕样式的影响未取证，无结构变化时静态不可见，不能宣称已穷尽所有样式。
[42] 源码快照 working_tree_dirty=true，本轮结论只能按 source_tree_sha256 37745f8f… 与各文件 sha256 追溯，未读文件的 Hook 覆盖不得推测。
- [43] 本单元草稿 overview 混入了 comment/dynamic/home/search/detail 等其他单元的文字与编号，交付前需由服务端按单元重组，避免跨页结论串用。
[44] story：StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller 源码本轮未读（工作树 dirty，需按文件哈希追溯），锚点来源、native/kotlin 双列表分流与 kotlin 列表为空时的兜底均未知；E012 仅为 comment 页定位器，不能替代。
[45] story：story_native +111 条外调边的规范化类名/方法描述符差集未执行，无法区分新渲染入口、内联与 DEX 重排；44 个 Compose 方法所在类与 story 页渲染入口的调用链未回溯。
- [46] story：story_kotlin 两侧 absent 的原因未确认——是否为 Compose 实现并入 story_native、落入未归类 DEX，或采集选择器规则差异；StoryMoss/KStoryMoss 未登记为协议，跨家族消费者无法判断。
[47] story：无安装器级与真机证据，runtime_enabled 仍为 unknown、module_coverage 仍为 requires_installer_review；宽屏/平板与服务端开关下的 story 形态未采样。
[48] mine：mine_native +1 类/+2 条的类集合差集未执行，新增类与两条新增边的 caller→callee 未定位，无法判断是否对应组件过滤或阅读卡入口。
- [49] mine：MineComponentFilterFeatureInstaller、MineVipFeatureInstaller 及 MineComponentSnapshot/MineComponentSnapshotStore 相关实现本轮未读，解析点、过滤条件与无命中兜底未知。
[50] mine：mine_account_model 的方法体哈希与字段/方法描述符差集未做，无法区分改名重排与方法体或类型真实变化；E000 的资源变更 1 项归属页面未确认。
[51] mine：MineMoss/KMineMoss 未登记协议，服务端下发字段变化静态不可见；账号信息与 VIP 状态的真机比对未执行。
- [52] 两页均缺安装器与真机日志：runtime_enabled、module_coverage 保持 unknown / requires_installer_review，本轮不宣称任何路径适配通过。
[53] 源码快照 working_tree_dirty=true，本轮引用的源码文件未逐一按文件哈希登记，后续复核需以文件哈希而非目录状态追溯。
[54] 草稿 overview 与 next_steps 混入 comment/dynamic、home/search、detail/pgc、player/danmaku 等其他单元的内容，需在服务端合并阶段按单元裁剪，避免被误读为本单元（story/mine）的覆盖结论。

## 下一步

- [1] 按 compose_signatures 对 dynamic_compose 做基线/目标方法级差集，定位新增 10 个 @Composable 的宿主类与调用方，判断重构还是新样式。
[2] 对 comment_native_legacy 新增 11 个类做反编译并标注调用者，核对 CommentNativeBindingCatalog 是否需要扩展条目。
[3] 真机抓取 dex.assist.comment_classic 诊断，确认 CommentClassicStyleLocator 的 NATIVE/KOTLIN 两侧 locate 结果是否为空、是否命中缓存兜底。
[4] 核对四个硬编码 owner（DeviceDecision、IDeviceDecisionKt、CommentV3Fragment、CommentSectionComposeFragment）与六个实验键锚点在 9.17.0 dex 中是否存在。
[5] 对 dynamic_legacy 减少的 15 条 external_invoke_edges 做调用者差集，确认是否为迁移到 Compose/Opus 家族或接口分发不可见。
- [6] 以关闭 Compose 开关进入动态页与评论区，分别验证 legacy 家族 purify/tabs Hook 是否触发，取得运行时启用证据。
[7] 在真机对 DynamicPurify 的 Compose 分支与 Opus 分支构造含屏蔽词/广告卡片条目，验证净化是否漏拦。
[8] 为 OpusMoss/KOpusMoss、DynamicMoss、ReplyMoss/KReplyMoss 等 unregistered_protocol 登记跨家族消费者，确认 dynamic_kotlin_moss 新增的 1 条边落在哪个家族。
[9] 补充 CommentComposePurifyBridge/CommentComposeViewAccess 与 DynamicPurifyFeatureInstaller 的源码正文核对，确认当前锚点集合对新增类是否覆盖（本轮未读，记为未知）。
[10] 在基线与目标各跑一次安装器级别覆盖检查，把 module_coverage 从 requires_installer_review 降到可复核状态。
- [11] 记录工作树未提交改动（working_tree_dirty=true）涉及的源码文件哈希，确保后续复核按文件哈希追溯而非清理工作树。
[12] 对平板/宽屏与 comment.kntr.landscape.enabled、story.enabled 分支各做一次真机路径采样，确认宽屏家族是否有独立实现。
[13] 对 home_legacy、home_new_frame 两侧方法描述符取差集，与 HomeFrameListHook.kt、HomeFrameTabLocator.kt 实际引用的类/方法逐条比对，判定是重排还是在迁移
[14] 读取 HomeRecommendPurifyFeatureInstaller.kt、HomeTabFilterFeatureInstaller.kt、HomeBannerFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt，登记各自 Hook 点与兜底分支，标注 legacy/khome 两条路径的绑定关系
[15] 读取 SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt，列出实际绑定签名并与搜索 java/kotlin moss 调用边做映射，输出未覆盖键清单
- [16] 对 search_native 边集合做差集，定位新增 62 条边的来源类，判断是否落在搜索推荐/默认词通道
[17] 将 app/search/v2、app/interfaces/v1、broadcast/message/search 等未登记搜索 Moss 生成协议候选，抽查其调用方是否跨家族
[18] 检查首页/搜索是否存在新旧双栈同时安装的路径与互斥条件（服务端开关、宽屏分支），确认无重复净化
[19] 真机按版本 9170300 抓取 HookEntry 与各定位器安装日志，记录命中/未命中项，与本报告的静态清单对齐
[20] 服务端 A/B 视觉变体在静态证据中不可见，需在真机分账号对比首页与搜索首页样式差异后再补充结论
- [21] 对 detail_theseus_ugc、detail_theseus_united、pgc_legacy、pgc_theseus 四条路径分别用 family_evidence 拉取 target/baseline 完整类清单与方法体哈希，做类名+签名级差集，区分改名/重排与真实删减。
[22] 对 detail_theseus_ugc 的 -18 条与 pgc_theseus 的 -275 条外部调用边做端点级比对，定位集中变化的调用方类，判断是否为门面化/家族边界迁移。
[23] 读取 DetailModulePurifyFeatureInstaller.kt、DetailViewPurifyFeatureInstaller.kt、DetailUnitedModulePurifyFeatureInstaller.kt、DetailUnitedPresentationPurifyFeatureInstaller.kt 的定位器与 fallback 分支，确认锚点是类名、方法签名还是接口/注解。
[24] 读取 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt、PgcAutoActivityPopupPolicy.kt，确认无命中时的兜底路径与日志入口。
[25] 核实 detail_legacy 在两侧均为 absent 的原因：是选择器规则变化、代码并入其他家族，还是旧原生详情确已移除；补充最小复现（真机类加载栈）。
- [26] 核对 detail_java_moss / detail_kotlin_moss / pgc_player_moss / pgc_view_moss 的 32、76、12、14 个定义是否存在跨家族消费者，避免以边数推断覆盖。
[27] 真机验证 detail：UGC 详情、普通视频详情、横屏/平板宽屏三种形态，开启模块诊断日志记录每个净化点命中/未命中。
[28] 真机验证 pgc：番剧详情页与播放页的活动弹窗抑制、宽屏/平板布局，记录定位器命中与兜底分支。
[29] 确认服务端开关（灰度和 A/B）是否控制 detail/pgc 样式切换；无结构变化时静态不可见，需在真机侧按实验分组对照。
[30] 补证模块源码工作树未提交修改（working_tree_dirty=true）对应文件哈希，按文件哈希而非目录推断本轮 Hook 实现。
- [31] 复核阶段（finish_review）逐条核对本次 5 条 path_reviews 的 status 是否与静态矩阵 evidence 值逐字一致，并核对是否出现“适配通过”类表述。
[32] 对 player_java/player_kotlin 两版分别拉取全量类清单与方法签名 diff，确认类数 +1/+3 与边数 -5 是真实变化还是混淆改名/DEX 重排。
[33] 定位 player_kotlin 消失的 5 条外调边的 caller→callee 签名，用 JADX 判定是否位于播放页控制链（倍速/缓冲/画质/赞助商）。
[34] 核对 PlayerSpeedLocator、PlayerBufferLocator、PlayerQualityFeatureInstaller、PlayerCodecForceFeatureInstaller、SponsorPlayerLocator 的命中签名是否仍存在于 9170300（本轮源码未读到，需补 module_source）。
[35] 列出 danmaku_kotlin 137→135 消失的 2 个类的类名、方法体哈希与原调用者，判断是否承载散列净化锚点。
- [36] 列出 danmaku_java_moss 20 条实际调用边的 caller 类名，映射到登记家族，确认未归类消费者归属。
[37] 读取 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 源码，确认定位点、兜底与失败降级路径（当前记为未知）。
[38] 真机（9.17.0）抓取 LSPosed 安装日志，确认各 Player*/Danmaku* installer 是否安装成功、是否被跳过，与 9170100 对照。
[39] 真机播放页分普通/宽屏/平板分栏三套入口，逐一验证倍速、缓冲、画质、弹幕净化是否生效，记录 UI 与日志双证据。
[40] 记录服务端开关分组（A/B）信息，区分“结构未变但样式不同”与“结构变化”，避免把静态不可见当作无变化。
- [41] 本单元所有路径 runtime_enabled 与 module_coverage 保持 unknown/requires_installer_review，复核阶段补安装器证据后再更新。
[42] 对 9170100 与 9170300 的 story_native 做规范化类名/方法描述符差集，定位 +111 条外部调用边的具体调用者。
[43] 读取 StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller，确认锚点来源、native/kotlin 双列表分流和 kotlin 列表为空时的兜底。
[44] 真机安装 9170300，对 story 两个 Installer 分别记录 hook 安装成功数与运行时命中数，并抓取 story 页 Compose 语义树。
[45] 核对 story_kotlin 为空是否意味着 Kotlin/Compose 实现被并入 story_native 或落入未归类 DEX，检查 StoryMoss/KStoryMoss 的实际消费者。
- [46] 对 mine_native 做类集合差集，定位 +1 新增类并核对其方法描述符与组件过滤规则的关系。
[47] 读取 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller 及 MineComponentSnapshot 相关实现，确认解析点与过滤条件。
[48] 真机在“我的”页比对 MineComponentSnapshotStore 过滤前后组件列表，并核对账号信息与 VIP 标识展示。
[49] 对 mine_account_model 做规范化描述符差集，判定指纹变化是否仅由混淆改名或 DEX 重排造成。
[50] 补登记 MineMoss/KMineMoss、StoryMoss/KStoryMoss 等协议后复核是否存在跨家族消费者；当前协议视图无法判断。
- [51] 按源码文件哈希记录 dirty 工作树中的相关文件版本，确保后续复核可追溯到同一快照。