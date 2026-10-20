## 模块源码快照

- 来源：published
- 捕获时间（UTC）：2026-10-15T14:19:32.431433Z
- 源码 HEAD：5422fad1e3f798252619d610a0504573ff47211b
- 快照 SHA-256：2fa2d3b70f73fa431ed83267a9519c726a41b67de39eb7ee785813de39067120
- 源码树 SHA-256：37745f8f27c41c22eab6e0bc780c6af700d650f49c3f004f862bf9c5f1548a5c
- 含未提交修改：True
- 时效状态：historical

复用历史静态证据 run 39424178585；本轮只重新执行 AI 审查。模块源码重新绑定到上述快照。

## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2446 | 278 | 932 | static_invoke_observed |
| comment_legacy_v2 | 579 | 0 | 743 | static_invoke_observed |
| comment_native_exp3 | 58 | 0 | 61 | static_invoke_observed |
| comment_native_legacy | 172 | 0 | 209 | static_invoke_observed |
| comment_native_next | 45 | 0 | 49 | static_invoke_observed |
| comment_other_ui:(root) | 221 | 2 | 511 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 23 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 216 | 0 | 101 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 236 | 32 | 247 | static_invoke_observed |
| danmaku_kotlin | 57 | 1 | 8 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1947 | 25 | 509 | static_invoke_observed |
| detail_theseus_united | 4579 | 99 | 4312 | static_invoke_observed |
| dynamic_compose | 1136 | 127 | 220 | static_invoke_observed |
| dynamic_legacy | 3252 | 105 | 2152 | static_invoke_observed |
| dynamic_opus | 1354 | 92 | 191 | static_invoke_observed |
| dynamic_other:appointment | 25 | 3 | 18 | static_invoke_observed |
| dynamic_other:card | 422 | 87 | 305 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 60 | static_invoke_observed |
| dynamic_other:commonPerf | 11 | 1 | 4 | static_invoke_observed |
| dynamic_other:commonUi | 21 | 5 | 8 | static_invoke_observed |
| dynamic_other:lightBrowser | 80 | 19 | 29 | static_invoke_observed |
| dynamic_other_legacy | 2108 | 4 | 2144 | static_invoke_observed |
| home_legacy | 769 | 87 | 211 | static_invoke_observed |
| home_new_frame | 196 | 33 | 48 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 328 | 7 | 91 | static_invoke_observed |
| pgc_legacy | 354 | 0 | 386 | static_invoke_observed |
| pgc_theseus | 2264 | 131 | 1328 | static_invoke_observed |
| player_java | 957 | 0 | 3229 | static_invoke_observed |
| player_kotlin | 7 | 0 | 100 | static_invoke_observed |
| search_compose | 3145 | 561 | 594 | static_invoke_observed |
| search_native | 1702 | 2 | 2851 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2925 | 44 | 1318 | static_invoke_observed |

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
- player_kotlin_moss: protocol_signature_or_call_path_changed
- search_kotlin_moss: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/account/interfaces/v1/KAccountInterfaceV1Moss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/ad/im/v1/KBusinessChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/coldstart/v1/KColdStartMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/distribution/KDistributionMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KOpusMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KTribeeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/feed/v1/KFeedMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/gopm/widget/v1/KWidgetMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/home/v1/KHomeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KimMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KHistoryMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KMediaMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/mine/v1/KMineMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/overseas/app/v1/KSplashMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/overseas/ogv/v1/KBangumiMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/playerunite/v1/KPlayerMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/resource/v1/KLegacyResourceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/resource/v1/KModuleMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/search/v2/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/childchannel/v1/KKidsChannelMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/mixture/v1/KMixtureMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/popular/v1/KPopularMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/rank/v1/KRankMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/topic/v1/KTopicMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/translation/v1/KTranslationMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KLegacyViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/wall/v1/KWallMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/message/main/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v1/KBroadcastRoomMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v1/KLaserMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v2/KLaserMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/interfacess/cosmoconn/v1/CosmoInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/interfacess/cosmoconn/v1/KCosmoInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/interfacess/watch/v1/KWatchInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/service/favorite/v1/KFavoriteMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/service/govern/v1/KQoeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/dynamic/interfaces/feed/v1/KFeedMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/dynamic/interfaces/vote/v1/KVoteMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/entitle/hub/interfaces/KEntitleHubMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/customer/interfaces/KCustomerInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/gateway/interfaces/v1/KImGatewayApiMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/interfaces/v1/KImInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/app/interfaces/api/grpc/v1/KMoreLiveMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/app/room/v1/KUniversalInteractMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/approom/api/grpc/v1/KDanmuMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/play_gateway/KPlayGatewayMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/xroom_extend/api/v1/KReportMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/main/community/reply/v2/KReplyMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/polymer/chronos/v1/KChronosServiceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/relation/interfaces/KRelationInterfaceMoss;: protocol_signature_or_call_path_changed

## 原生资源变化

{'added': 24, 'removed': 12, 'changed': 8604}

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

本单元审计评论页与动态页在 9.15.0→9.16.0 的宿主适配变化。两侧同签名证书、同仓库冻结 APK，静态矩阵显示评论 5 个家族（legacy_v2、native_legacy、native_next、native_exp3、compose）与动态 3 个家族（legacy、compose、opus）全部仅达 static_invoke_observed，runtime_enabled 一律 unknown，module_coverage 全部 requires_installer_review，因此任何路径都不能声称适配通过。变化点集中在家族规模与调用边数量：评论 compose 278 compose 方法、932 外调边为最大一族；动态 compose 类数 956→1136、compose 方法 112→127，opus 几乎持平。结构化指纹全部改变，但 APK 访问关闭，只能按冻结视图取证，训练有界的类样本不足以代表整套实现；混淆短名（如 kntr.app.following.followinglist.A）提示指纹变化更可能是重排/改名而非新样式。以下推断未经真机验证。

本单元覆盖 home（home_legacy、home_new_frame）与 search（search_native、search_compose）四条登记路径，对比基线 9.15.0 与目标 9.16.0（同一签名证书，包体 +6.2MB）。四条路径的静态证据值均为 static_invoke_observed，runtime_enabled 与 module_coverage 均为 unknown/requires_installer_review，因此本报告不判定适配结果。变化集中在：home_legacy 类数 1004→769、Compose 方法 128→87、外部调用边 236→211 且指纹改变；home_new_frame 类数（196）、Compose 方法（33）不变、边数 46→48 但指纹改变；search_native 类数 1674→1702、边数 2789→2851；search_compose 类数 3149→3145、Compose 方法 556→561、边数 616→594，二者 search_java_moss（24 定义/22 边）与 search_kotlin_moss（52 定义/18 边）两侧完全一致。已用深挖工具核实 home 两个家族的类样本（E013/E014），但本轮 module_source 与 search_compose 深挖调用被额度拒绝，模块侧解析点、安装器/定位器覆盖均未读到，相关结论保持 candidate/needs_runtime，不得视为适配通过。源码快照工作树为 dirty（source_tree_sha256 37745f8f…），按文件哈希追溯，未做清理。

9.16.0(9160200) 对 9.15.0(9150300) 同包同证书，本单元只覆盖 detail 与 pgc 两页共 5 条登记路径。事实：detail_legacy 两版均为 absent（类数 0、指纹为全零哈希值 4f53cda1…，即空集合），detail_theseus_ugc 类数 1953→1947、外部调用边 515→509、Compose 方法 25 不变、指纹变化；detail_theseus_united 类数 4602→4579、Compose 98→99、调用边 4163→4312（+149）、指纹变化。pgc_legacy 类数 353→354、调用边 401→386、Compose 0 不变、指纹变化；pgc_theseus 类数 2249→2264（+15）、Compose 131 不变、调用边 742→1328（+586，约 +79%）、指纹变化。四个 Moss 协议定义的与调用边数两版完全不变（detail_java_moss 32/35、detail_kotlin_moss 76/10、pgc_player_moss 12/3、pgc_view_moss 14/7）。所有路径 module_coverage=requires_installer_review、runtime_enabled=unknown，未核实安装器与真机启用，不能宣称适配通过。本单元深挖工具被禁用，仅使用 E000/E005/E006 预取证据，缺失项记为未知。

本单元只覆盖 player 与 danmaku 两页（9.16.0 对 9.15.0）。预取证据显示：player 两家族均为 static_invoke_observed，player_java 类数 953→957、外部调用边 3225→3229 且指纹变化；player_kotlin 类数 7、边数 100 均未变但指纹变化，更像混淆改名/DEX 重排而非新样式。danmaku_legacy 两侧都 absent，danmaku_kotlin 类数 56→57、边数 9→8 且指纹变化，属结构候选变化。四组 MOSS 协议定义数与实调边两侧完全一致（18/2、34/3、22/20、46/4），说明协议层未随家族指纹漂移，需注意协议不变不代表样式不变。所有 path 的 runtime_enabled 均为 unknown，module_coverage 均 requires_installer_review；本单元深挖工具被拒绝（仅允许 finish_report），未获得新增 E 证据，因此全部结论限于预取摘录，不得表述为适配通过。源码快照 working_tree_dirty=true，未读源码，不对 Hook 覆盖作推测。

本单元只提交 story 与 mine 两页、共四条登记路径。静态矩阵显示：story_native 目标版 2925 类/44 Compose 方法/1318 条外部调用边（基线 2958/44/1380），story_kotlin 两侧均为 0 类且 evidence=absent；mine_native 328/7/91（基线 324/7/95），mine_account_model 132/0/43（基线 132/0/54）。三条 static_invoke_observed 路径指纹全部变化，仅 story_kotlin 维持 absent，四条路径均为 runtime_enabled=unknown、module_coverage=requires_installer_review。两页声明内 protocol 映射为空，但样本未登记协议列表中同时出现 StoryMoss、MineMoss/KMineMoss 与 account interfaces，说明协议消费者存在而登记缺失，不能据此判断样式已被穷尽。本轮深挖工具不可用（仅允许 finish_report），模块源码正文未读；冻结快照 source_dirty=true、working_tree_dirty=true，只能定位候选 Installer，不能证明 Hook 生效。故全部结论停留在候选/待真机级别，不宣称适配通过。

## 各页面评估

### comment

评论页同时登记 5 条路径，均静态观测到外调边：comment_legacy_v2（579 类/743 边）、comment_native_legacy（172/209）、comment_native_next（45/49）、comment_native_exp3（58/61）、comment_compose（2446 类、278 compose 方法、932 边）。与基线相比：legacy_v2 类 581→579、边 734→743，属微幅波动；native_legacy 类 156→172、边 177→209（约 +18%），是本页变化最大的非 Compose 家族；native_next 类持平 45、边 46→49；native_exp3 类 60→58、边 59→61；compose 类 2417→2446、compose 方法 274→278、边 918→932。全部指纹改变，但仅凭指纹不能判定新样式，混淆改名与 DEX 重排同样会改写指纹。协议层：comment_java_moss 定义 50/实际边 50（两侧相同），comment_kotlin_moss 定义 130/边 26（两侧相同），Kotlin MOSS 的定义-边落差说明多数声明未观测到静态消费者，可能由接口分发或协程边界吞掉。深挖家族样本（E011）仅取 5 个类且均为空 compose_signatures 的 service/data 类，无法据此判断 278 个 compose 方法的实际入口，也无法确认模块安装器在 9.16.0 是否命中，故路径级影响与兜底均记为未知，需真机与安装器日志补证。

证据：E000, E001, E011

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 581→579、外调边 734→743，指纹由 dc1ce6f2… 变为 33676515…，规模小幅波动但边数上升。
- 可能影响：若模块的经典样式定位器按类/字段签名绑定，指纹变化可能使定位失败并回落到未 Hook 状态；实际影响未知。
- 验证：在 9.16.0 真机进入评论区旧样式入口，开启模块日志确认 CommentClassicStyleLocator 命中类名与 Hook 成功条数，再与 9.15.0 对照。
- 证据：E001, E011

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 156→172、边 177→209，为本页非 Compose 家族最大增幅，指纹 5f1a4dd5…→3219e4f0…。
- 可能影响：新增类可能承载新的绑定/装饰层，模块原有 native 绑定规则可能未覆盖新增子类，导致部分卡片未被处理；未读源码前不可断定。
- 验证：抽取新增类的方法语义（CommentNativeBindingCatalog 依赖的绑定方法名），用真机分别打开视频详情页原生评论与二级回复，记录 Hook 日志中未命中类名清单。
- 证据：E001

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类持平 45，边 46→49，compose_methods 仍为 0，指纹 4f7755ff…→07ff5e26…。
- 可能影响：结构基本不变，若模块在该家族已有绑定，回归风险较低，但路径是否启用仍取决于服务端开关。
- 验证：真机灰度账号下确认 next 样式是否出现（可通过宿主内实验开关），并核对模块日志该家族 Hook 计数是否非零。
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 60→58、边 59→61，指纹 d0a1de81…→067a483c…，规模略减而边数微增。
- 可能影响：类数减少不等于功能消失，可能为合并或迁移；若模块按旧内部类名定位会静默失效。
- 验证：以实验组账号触发 exp3 评论样式，比对模块 Hook 命中的类名与 9.15.0 快照差异，并确认是否有兜底反编译器路径生效。
- 证据：E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2417→2446、compose 方法 274→278、外调边 918→932，指纹 b91f8725…→1b4eddf5…；深挖样本仅 5 个类，其中 compose_signatures 全为空。
- 可能影响：Compose 侧复制/净化/回复按钮桥接依赖 ComposeViewAccess 与 NativeBindingCatalog，类增长若集中在新的包装层，可能造成 UI 树访问失败或按钮注入重复；具体影响未验证。
- 验证：在真机 Compose 评论区抓取 CommentComposeViewAccess 的节点查找日志，检查 4 个新增 compose 方法的调用者是否与旧入口并行存在，并观察回复按钮是否只注入一次。
- 证据：E001, E011

### dynamic

动态页登记 3 条路径：dynamic_legacy（3252 类、105 compose 方法、2152 边）、dynamic_compose（1136 类、127 compose 方法、220 边）、dynamic_opus（1354 类、92 compose 方法、191 边）。与基线比较：legacy 类 3227→3252、边 2193→2152（类增而边减），compose 类 956→1136（+约 19%）、compose 方法 112→127、边 170→220，是本页变化最显著的一方；opus 类 1341→1354、compose 方法持平 92、边 190→191。深挖家族样本（E012）给出的 5 个类均为 kntr.app.following.followinglist 下混淆短名 A–E，多为带 ComposeLambda/State 字段的 lambda 包装类，说明该家族含关注列表宽屏（ui/wide）相关实现，但也暴露样本不足以覆盖 1136 个类。协议层 dynamic_java_moss 定义 134/边 134、dynamic_kotlin_moss 定义 382/边 26，两侧相同；Kotlin MOSS 定义多而边少，跨家族消费者是否存在需另行核实。种子未注册协议清单含 DynamicMoss、KOpusMoss、OpusMoss、KTribeeMoss 等，说明动态/Opus 协议族存在模块未登记的接口，无法据此判断净化策略是否仍生效。全部路径 runtime_enabled 为 unknown，module_coverage 需安装器复核，未读源码部分不下结论。

证据：E000, E002, E012

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3227→3252，compose 方法保持 105，外调边 2193→2152（减少 41），指纹 d5217d02…→e3738343…。
- 可能影响：类增加而边减少可能来自调用合并或迁移到新入口；若 DynamicPurify 决策依赖的旧调用点被替换，部分动态卡片可能不再进入过滤逻辑。
- 验证：真机打开动态时间线，抓取 DynamicPurifyPolicy 命中日志与未处理卡片类型清单，并对照 9.15.0 的同一清单。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 956→1136、compose 方法 112→127、边 170→220，指纹 84a035d3…→3c0596bc…；深挖样本显示 kntr.app.following.followinglist 下新增 lambda/宽屏 UI 包装类。
- 可能影响：Compose 动态（含关注列表宽屏布局）新增包装层时，模块基于类名/Composable 签名的安装器可能漏挂，表现为净化或标签控制不生效；也可能是混淆重排导致的同义变化。
- 验证：在真机以平板/宽屏与手机两种形态分别进入关注列表动态流，比对 Compose Hook 命中的 Composable 方法数量与新增包装类的对应关系，并核对 DynamicTabsFeatureInstaller 的安装日志。
- 证据：E002, E012

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1341→1354、compose 方法 92 持平、边 190→191，指纹 5f15905b…→008f9bfd…。
- 可能影响：Opus 结构基本稳定，模块净化若依赖固定类名仍有被混淆改名打断的风险；KOpusMoss/OpusMoss 未在模块登记协议中，跨家族消费者覆盖未知。
- 验证：真机打开动态页 Opus 图文卡片，确认 DynamicPurify 对 Opus 文本与图片节点的处理日志；同时用反编译类核对 Opus 协议 MOSS 调用方是否被模块 Hook 覆盖。
- 证据：E000, E002

### home

主页两条路径均以 static_invoke_observed 记录，运行时启用与安装器覆盖未知。home_legacy 出现明显收缩：类 1004→769、Compose 方法 128→87、外部调用边 236→211（E003），指纹 aa99feb8…→8772cd6d…；深挖样本 E013 显示该家族 class 文件来自 file_id 24，包含 Ltv/danmaku/bili/ui/main2/ 下的 HomeFragmentV2 内部类（A、A0）、WatchLaterFragmentV2 回调（B0）与 AccountMineRequestResource 枚举，说明旧版 Main2 主页承载仍在，但条目明显减少，可能是部分组件迁移到 khome 新框架、混淆改名或重复包装层被裁剪。home_new_frame 类数 196、Compose 方法 33 与基线完全一致，仅外部调用边 46→48 且指纹改变（E003/E014），深挖样本 E014 显示 khome/widget/bubble 的 a/b/getId/getImageUrl/getUrl 等类以及 HomeFrameViewModel$dispatchAction$1（持 ap1/b action、SuspendLambda）结构仍在，属于“哈希变化但量级不变”的典型样本，不能直接判为新样式。对模块的可能影响：HomeFrameListHook/HomeFrameTabLocator/HomeFrameViewModel 相关的字段与 action 类型若被改名，Hook 定位与 tab 过滤可能静默失效；home_legacy 的类收缩也可能让基于旧类名的过滤点落空。本轮 module_source 读取被额度拒绝，无法核对这些定位器的实际匹配签名，因此模块影响未知。验证需要：在目标包上用真机分别进入旧版与新框架主页、切换底部 tab、开关净化与组件过滤功能，结合类加载与安装器日志确认 Hook 是否挂载。

证据：E003, E013, E014

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 1004→769、Compose 方法 128→87、外部调用边 236→211，家族指纹 aa99feb8…→8772cd6d…；深挖样本仍见 Ltv/danmaku/bili/ui/main2/HomeFragmentV2 相关内部类、WatchLaterFragmentV2 回调与 AccountMineRequestResource 枚举。
- 可能影响：旧版主页家族规模收缩，可能意味着组件迁出或重复包装层减少；若 HomeComponentFilter/ TabFilter 依赖的旧类名被改，过滤点可能静默不生效，具体是否命中未知。
- 验证：在 9.16.0 真机进入旧版主页，开启组件过滤与 tab 过滤后抓取类加载与 Hook 安装日志，确认 Ltv/danmaku/bili/ui/main2/* 下被 Hook 的类是否仍加载并被命中；与 9.15.0 同名类做方法签名逐一比对。
- 证据：E003, E013

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 196、Compose 方法 33 与基线一致，外部调用边 46→48，指纹 e3ea6856…→08696567…；深挖样本仍包含 khome/widget/bubble 的 a/b 类与 HomeFrameViewModel$dispatchAction$1（action 类型 ap1/b）。
- 可能影响：量级不变仅调用边 +2，更像改名/DEX 重排而非新样式；HomeFrameListHook 与 HomeFrameTabLocator 若按类名或字段名定位，改指纹后可能匹配失败，运行时是否启用未知。
- 验证：对 HomeFrameViewModel 与 dispatchAction 的 action 类型做目标包字段/方法签名比对（本轮无法反编译，需在允许访问 APK 的环境执行）；真机切换新版主页 tab 并观察列表过滤是否生效，检查安装器日志中的定位器命中记录。
- 证据：E003, E014

### search

搜索两条路径均以 static_invoke_observed 记录，运行时启用与安装器覆盖未知。search_native 类 1674→1702（+28）、外部调用边 2789→2851（+62），Compose 方法恒为 2，指纹改变（E004），说明旧原生搜索栈仍在增长而非被替换。search_compose 类 3149→3145（−4）、Compose 方法 556→561（+5）、外部调用边 616→594（−22）（E004），方向相反：Compose 侧方法数微增而调用边下降，可能是 Lambda/包装类合并或重命名，也可能是部分调用改走协议/内部调用，静态不可判定。协议层 search_java_moss 24 定义/22 实际调用边、search_kotlin_moss 52 定义/18 实际调用边，两侧完全相同，提示 MOSS 协议面在本次升级未发生结构变化；但未登记协议清单中仍存在 app/interfaces/v1 KSearchMoss、SearchMoss，app/search/v2 KSearchMoss、SearchMoss 以及 broadcast/message/search/SearchMoss 等，跨家族消费者无法从本单元证据确认。对模块的可能影响：SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller 依赖的搜索首页推荐与默认词解析点若发生改名或迁移，可能只覆盖其中一条栈（原生或 Compose），产生“净化只对一种布局生效”的部分覆盖。本轮 module_source 与 search_compose 深挖均被额度拒绝，模块解析点与其调用边未被读取，因此覆盖情况明确为未知。验证需要在真机分别触发原生与 Compose 搜索首页，检查默认词与推荐卡是否被清理，并抓取定位器命中日志。

证据：E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类 1674→1702、外部调用边 2789→2851、Compose 方法 2→2，指纹 481dae50…→bc8afdf5…；家族规模净增长，未见被新栈替代的迹象。
- 可能影响：增长可能来自新增业务类或混淆拆分；基于类名/方法签名定位的原生搜索 Hook 若指向已改名条目会静默失效，是否命中未知。
- 验证：在真机 9.16.0 进入原生搜索首页，开启搜索净化与默认词清理，记录 Hook 安装器与定位器日志中的命中类；与 9.15.0 的同名类方法集比对，确认新增 28 个类的归属包。
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类 3149→3145、Compose 方法 556→561、外部调用边 616→594，指纹 6c663f2d…→e0ff4112…；方法数上升但外部调用边下降 22。
- 可能影响：边下降与 Compose 修复/内联或调用迁移一致，也可能来自重复包装层合并；若模块对 Compose 搜索首页的解析点依赖被合并的调用边，推荐卡净化可能只覆盖部分样式，未知。
- 验证：真机在 Compose 搜索首页分别打开与关闭推荐净化，比对渲染结果；对 E004 中 Compose 家族样本类做完全限定名与方法签名差分（需 APK 访问），确认调用边减少是否集中于单个 Composable。
- 证据：E004

### detail

事实：detail_legacy 在 9.15.0 与 9.16.0 均 absent（类数 0、Compose 0、外部调用边 0、指纹为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945，即空集合哈希），因此本页不存在“旧原生样式被删除”的证据，只能记为已登记但静态不可见（E005）。detail_theseus_ugc：类数 1953→1947（-6）、Compose 方法 25→25、外部调用边 515→509（-6）、指纹由 c36f2a42… 变为 5cd2f7c7…，属小幅结构/调用路径变化，量级与“少量类增删、混淆改名或 DEX 重排”相符，尚不足以判定新样式（E005）。detail_theseus_united：类数 4602→4579（-23）、Compose 98→99（+1）、外部调用边 4163→4312（+149）、指纹由 83e1f0b1… 变为 519ae33f…，是 detail 页变化最大的一条，需分开核实“真实新增调用路径”与“解析/编译变化”（E005）。协议侧 detail_java_moss 32 定义/35 实际调用边、detail_kotlin_moss 76 定义/10 实际调用边，两版完全相同；注意定义数与调用边不是同一单位，不能据 76 与 10 相除推导覆盖率，但 Kotlin Moss 仅有 10 条实测调用边说明其协议消费者入口在静态视图中很少，模块侧是否存在兜底未知（E005）。module_coverage 全为 requires_installer_review，runtime_enabled=unknown：静态调用存在不证明真机启用，安装器是否覆盖 DetailModulePurify/DetailUnitedModulePurify/DetailViewPurify 系列未读源码，记为未知（E005）。

证据：E005, E000

#### 路径：detail_legacy

- 状态：absent
- 变化：两版均 absent：类数 0、Compose 0、外部调用边 0、指纹为固定空集合哈希，无新增或删除证据。
- 可能影响：对模块的可能影响未知：不能推断旧原生 detail 样式在该版本被移除，也不能推断模块旧路径失效；只能确认静态矩阵未观察到该类家族。
- 验证：最小补证：对 9.16.0 全量类清单检索 detail 旧家族登记类名/包前缀，确认是缺席还是登记键不匹配；再在真机抓取详情页 Activity 与模块日志，确认实际走的是哪条路径。
- 证据：E005, E000

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类数 1953→1947、外部调用边 515→509（均 -6）、Compose 方法 25 不变、指纹变化；量级小，与少量类增删/混淆改名或 DEX 重排一致。
- 可能影响：若为真实类删改，依赖 UGC Theseus 类名/方法签名的详情页模块净化 Hook 可能部分失配；若仅为重排则影响有限。两种可能均未区分。
- 验证：对两版该家族类样本做类名与 method_bodies_sha256 的逐类 diff，区分删除类、改名类与方法体变化；再用 decompile_class 核对模块解析点所依赖的签名是否仍存在；真机验证 UGC 详情页净化 Hook 是否触发。
- 证据：E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类数 4602→4579（-23）、Compose 98→99（+1）、外部调用边 4163→4312（+149）、指纹变化；类数下降与调用边上升方向相反，指向解析/编译差异而非单纯新增页面。
- 可能影响：united 详情页承载推荐/广告等可净化模块，调用边增加可能意味着新增对外部模块的调用点，模块 DetailUnitedModulePurify/DetailUnitedPresentationPurify 的策略命中面可能变化；是否为真实新增未确认。
- 验证：抽样比对两版 united 家族的高出度类与新增调用边目标类，判断是同一方法体内部调用重组还是新调用者；再读 DetailUnitedModulePurifyPolicy/Installer 解析点核对签名；真机对照净化前后模块列表。
- 证据：E005

### pgc

事实：pgc_legacy 类数 353→354（+1）、Compose 0 不变、外部调用边 401→386（-15）、指纹由 58516e1d… 变为 b77616da…（E006）。类数与调用边反向变化，单凭这三个数与指纹无法判定是否为新样式或新原生实现，需按类名/方法体哈希细化。pgc_theseus 类数 2249→2264（+15）、Compose 方法 131→131 不变、外部调用边 742→1328（+586，约 +79%）、指纹由 e02d9f27… 变为 ede5e8c1…（E006）。这是本单元幅度最大的变化，但类数仅增 15、Compose 方法零增长，故“新增整套新样式页面”与“既有类之间解析出的调用边增多（内联/去虚拟化/DEX 重排/解析器版本变化）”两种解释都成立，静态数据不能区分；不能据此宣称 PGC 存在新样式，也不能宣称旧样式消失。协议侧 pgc_player_moss 12 定义/3 实际调用边、pgc_view_moss 14 定义/7 实际调用边，两版完全一致，说明跨 pgc 播放与视图的 Moss 协议结构在本次升级中未变；但定义数与调用边单位不同，不可相除推导覆盖率，且实际调用边很少，说明模块侧若依赖这些协议消费者，入口面窄，兜底是否存在未读源码即未知（E006）。pgc 页已登记模块源码包含 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt/Policy.kt，其覆盖情况属 module_coverage=requires_installer_review，本单元未读安装器与定位器源码，运行时是否启用为 unknown（E006）。

证据：E006, E000

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类数 353→354（+1）、外部调用边 401→386（-15）、Compose 0 不变、指纹变化；类数与调用边反向变动，变化性质未定。
- 可能影响：若 386 条边中有 15 条属于被模块依赖的入口（例如自动弹窗定位路径），PgcAutoActivityPopupLocator 的定位点可能偏移；是否发生未知。
- 验证：对两版 pgc_legacy 类样本做类名与 method_bodies_sha256 diff，定位那 1 个新增类与 15 条消失边的源/目标类；用 module_source 读 PgcAutoActivityPopupLocator.kt 核对定位签名；真机打开 PGC 详情页观察弹窗与模块日志。
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类数 2249→2264（+15）、Compose 方法 131 不变、外部调用边 742→1328（+586）、指纹变化；调用边增幅远超类数增幅，主因尚未确定。
- 可能影响：pgc_theseus 承载 PGC Theseus 模块渲染与净化面；若调用边增加对应真实新增跨模块调用（如活动弹窗/推荐模块），PgcAutoActivityPopupFeatureInstaller 的策略命中与兜底可能需要扩展；若仅为解析差异则影响有限。两种情况均未区分。
- 验证：以 family_evidence 重读 pgc_theseus 目标侧完整样本，按调用边目标包的分布对比 742 与 1328 两版，判断新增边集中于已存在类还是新类；再核对 pgc_view_moss/pgc_player_moss 的 7/3 条实际调用边是否落在新增边内；真机 A/B（开关模块前后）对照 PGC 详情页模块列表。
- 证据：E006

### player

player 页两条登记路径均为 static_invoke_observed，但性质不同。player_java：类 953→957、外部调用边 3225→3229、指纹 f99b126d…（基线 4102698f…），即规模与结构同时小幅变化，属需要复核的结构/调用路径变化；+4 类 +4 边无法区分是新增解析入口、包装层重复，还是混淆拆分，必须按类级清单比对而不能用计数推断覆盖。player_kotlin：类 7、compose_methods 0、边 100 三者与基线完全相同，仅指纹 544b8dec… 对 b275709b… 变化，最合理解释是常量池/方法体顺序或 DEX 重排导致哈希漂移，尚无证据支持“新播放器 Kotlin 样式”。协议侧 player_java_moss 18 定义/2 实调边、player_kotlin_moss 34 定义/3 实调边两侧一致，说明协议面未扩张，但也提示 18 与 34 个定义中仅 2 与 3 条有实调边，模块若依赖未被实调的协议面则静态不可见。风险点：外部调用边存在不证明真机路径启用，也不证明模块 Hook 命中；安装器定位器（PlayerSpeedLocator、PlayerBufferLocator、SponsorPlayerLocator 等）是否覆盖变化后的类名/签名，预取没有给出结果，module_coverage 仍为 requires_installer_review。结论为 candidate，需按哈希的类级 diff 加真机播放链路验证。

证据：E000, E007

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类 953→957、外部调用边 3225→3229，指纹 f99b126d… 对基线 4102698f…；协议 player_java_moss 仍为 18 定义/2 实调边。
- 可能影响：若 +4 类是新的播放器外壳或包装层，倍速、缓冲、画质、片尾推荐等以类名/签名为锚点的定位器可能落空；协议面未变，网络层插件风险相对低，但 2 条实调边之外的协议消费者静态不可见。
- 验证：1) 拉取两侧 player_java 类级清单按 method_bodies_sha256 做差异，标记新增/消失类；2) 用 JADX 读新增类确认是包装层还是真实新逻辑；3) 真机在 9.16.0 上打开视频页，看模块日志中 PlayerSpeedLocator/PlayerBufferLocator 的解析结果是否仍命中；4) 对未被实调的协议定义列消费者清单，确认是否存在跨家族调用者。
- 证据：E000, E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类 7、compose_methods 0、外部调用边 100 与基线完全一致，仅指纹 544b8dec… 对 b275709b… 变化；protocols player_kotlin_moss 34 定义/3 实调边两侧一致。
- 可能影响：计数完全一致时优先视为混淆改名/方法体顺序或 DEX 重排造成的结构哈希变化，而非新样式；若据此新写适配钩子可能引入无谓重复包装。真实风险在于 3 条实调边是否被模块覆盖仍未知。
- 验证：1) 比对两侧 7 个类的类名与方法体哈希，确认差异是否为常量池级；2) 检查模块中 player_kotlin 相关定位器是否按字符串类名匹配，若是则确认新旧名映射；3) 真机复现播放器 Kotlin 路径（如投屏/小窗或特定播放内核），查看 Hook 是否触发并有可观测行为差异。
- 证据：E007

### danmaku

danmaku 页两条登记路径状态相反。danmaku_legacy 在 9.16.0 与 9.15.0 两侧 classes=0、compose_methods=0、external_invoke_edges=0、指纹同为 4f53cda1…，evidence 为 absent；absent 只说明旧家族未被静态观测到，不等于弹幕功能消失，也不能据此外推旧原生弹幕已被移除，存在家族识别规则未覆盖、类迁移到其他命名空间（例如更通用渲染层）等替代解释。danmaku_kotlin 为 static_invoke_observed：类 56→57、compose_methods 1、外部调用边 9→8、指纹 7f0a50d2… 对 f55e24e0…，属结构或调用路径变化，且是唯一被观测到的弹幕实现候选，需重点复核；但 1 个 compose 方法和 8 条外部边样本极小，无法代表整套弹幕渲染、发送与净化实现。协议侧 danmaku_java_moss 22 定义/20 实调边、danmaku_kotlin_moss 46 定义/4 实调边两侧完全一致，说明共同协议未变；但 20 条实调边分布在哪些家族、是否被 Kotlin 家族消费，预取未给出跨家族消费者明细，属于必须补证的未知。DanmakuPurifyFeatureInstaller/Policy 等净化入口是否仍能定位到变化后的类，本单元未读到源码，module_coverage 仍为 requires_installer_review，不得推测 Hook 覆盖。结论为 candidate/needs_runtime。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：9.16.0 与 9.15.0 两侧均 classes=0、边 0、指纹 4f53cda1…，无结构变化可观察。
- 可能影响：无法判断旧原生弹幕家族是被移除、被识别规则漏掉，还是迁移到其他命名空间；若模块仍有面向该家族的净化钩子，需确认其是否已成为死代码，反之若依赖它做兜底则存在兜底缺失风险。
- 验证：1) 用不同家族识别参数（包名前缀、渲染类继承自 View/SurfaceView、字符串常量如 danmaku 相关 key）重跑识别，判定是识别漏检还是真缺失；2) 在 9.16.0 真机开启弹幕并用净化功能，观察是否有任何 Hook 日志命中；3) 检查模块中指向旧家族的钩子是否仍有存活调用者。
- 证据：E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类 56→57、compose_methods 1、外部调用边 9→8、指纹 7f0a50d2… 对 f55e24e0…；协议 danmaku_java_moss 22/20 与 danmaku_kotlin_moss 46/4 两侧不变。
- 可能影响：唯一被观测到的弹幕实现对，类数增加而外部边减少，可能是类拆分/包装重复或调用收敛，仅凭计数不能判定新样式；净化、发送、屏蔽词等基于类名或方法签名的注入点可能因改名或迁移失配。
- 验证：1) 对两侧 danmaku_kotlin 做类级 diff，定位新增类与被删除的 1 条外部边的调用方；2) 用 JADX 读新增类与那 1 个 compose 方法，确认是否为渲染外壳；3) 查 danmaku_java_moss 20 条实调边的调用者清单，判断是否有跨家族（Kotlin/Compose）消费者；4) 真机对比 9.15.0 与 9.16.0 的弹幕净化、屏蔽、开关行为差异，并记录日志时间戳。
- 证据：E008

### story

story 页登记两条路径。story_native 在 9.16.0 仍为 static_invoke_observed：2925 类、44 个 Compose 方法、1318 条外部调用边，相对 9.15.0 基线（2958/44/1380）分别少 33 类、0 个 Compose 方法、62 条边，指纹由 6b74bce4… 变为 7fffa3be…。变化性质未知：Compose 方法数完全不变而类数与边数同时小幅下降，既可能是混淆改名与 DEX 重排（足以单独改变结构哈希），也可能是真实的分支裁剪或代码迁移；本单元未读到运行条件，不能判定属于哪种。story_kotlin 两侧都是 0 类、0 边、指纹为 4f53cda1…（空集哈希），evidence 恒为 absent，说明该家族在基线与目标版都没有可见的独立 Kotlin 实现，不能解读为页面功能消失，也不排除其实现被归入其他家族。种子内 story.protocols 为空，但未登记协议清单中确实出现 Lcom/bapis/bilibili/app/story/v1/StoryMoss; 与 dynamic/view 系列，说明存在未登记到页面的协议消费者；这对模块的意义是：旧/新原生并存栈、Compose 与 MOSS 通道的切换条件、服务端开关与宽屏变体均无从静态穷尽。模块侧存在 StoryActionIconsFeatureInstaller/StoryActionIconsPolicy/StoryPurifyFeatureInstaller/HomeVerticalDetail* 等候选文件，但本单元未读其正文，安装器命中、定位器兜底与 Hook 生效全部为未知。

证据：E009, E000

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：静态调用边仍存在；类数 2958→2925、外部调用边 1380→1318、Compose 方法 44→44，指纹 6b74bce4…→7fffa3be…。
- 可能影响：第 62 条调用边的减少可能触及模块依赖的具体入口/回调；也可能只是混淆改名或 DEX 重排导致的结构体现，实际 Hook 覆盖面未知。
- 验证：对 9.16.0 逐类比对 9.15.0 的 story_native 类清单，按方法体哈希而非类名匹配，确认 33 个缺失类是改名、合并还是真实删除；再对模块 StoryActionIcons/StoryPurify/HomeVerticalDetail 的候选定位器逐条打印命中结果。
- 证据：E009, E000

#### 路径：story_kotlin

- 状态：absent
- 变化：基线与目标版均为 0 类、0 Compose 方法、0 外部调用边，空集指纹一致，无变化。
- 可能影响：不存在可审计的独立 Kotlin 家族调用面，因此本轮无法给出该家族的模块覆盖率；不代表故事页相关界面不存在。
- 验证：在真机上以模块日志确认 story 相关 Hook 实际进入的类与方法名；若命中 khome/Kotlin 侧类，则说明该实现被计入其他家族，需重新归族而非维持 absent。
- 证据：E009

### mine

mine 页登记两条路径。mine_native 在 9.16.0 为 static_invoke_observed：328 类、7 个 Compose 方法、91 条外部调用边，基线 9.15.0 为 324/7/95，即类数 +4、Compose 方法持平、边数 -4，指纹由 cf69dfa7… 变为 66c1fa8a…。mine_account_model 保持 132 类、0 Compose 方法，但外部调用边由 54 降至 43（-11），指纹 d5370d6e…→ddcfc5ef…。两条路径指纹均变化而规模近乎持平或仅小幅收缩，最典型解释是混淆改名/DEX 重排或重复包装层收敛；但 mine_account_model 去掉 11 条边而类数不变，也可能涉及账号模型的聚合请求或回调入口迁移，这正好是 MineVip/账号卡片类 Hook 的敏感面。种子内 mine.protocols 为空，而未登记协议清单含 Lcom/bapis/bilibili/app/mine/v1/MineMoss;、KMineMoss、account/interfaces/v1/AccountInterfaceV1Moss 与 KAccountInterfaceV1Moss，说明 Mine 页与账号信息存在 MOSS 协议消费者却未登记到页面，跨家族消费者与兜底路径无法静态判定。模块侧候选为 MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineVipFeatureInstaller、MineComponentSnapshotHostBridge/QueryClient/Store、HostMineReadingCard；本单元未读源码正文，且快照 working_tree_dirty=true，因此组件过滤快照的取数点、VIP 替换点与跨进程快照桥是否命中真实类均为未知，安装器与运行验证待补。

证据：E010, E000

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类数 324→328（+4）、Compose 方法 7→7、外部调用边 95→91（-4），指纹 cf69dfa7…→66c1fa8a…。
- 可能影响：新增 4 个类可能是新组件或包装层；减少的 4 条边可能改变 MineComponentFilter 依赖的组件列表/回调入口，导致过滤清单抓取不到或抓到新增块。
- 验证：在 9.16.0 上按方法体哈希比对新出现的 4 个 mine_native 类，确认是否属 Mine 组件容器；真机打印 MineComponentSnapshot 实际采集到的组件标识与数量，与设置页可见项逐一对照。
- 证据：E010, E000

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数 132→132、Compose 方法 0→0，外部调用边 54→43（-11），指纹 d5370d6e…→ddcfc5ef…。
- 可能影响：规模不变而调用边明显减少，可能意味账号模型对外调用被收敛/内联，或 VIP/账号卡片相关入口迁移到其他类；MineVip 与账号卡替换的定位点可能失效，也可能不受影响。
- 验证：对 132 个类做逐类方法体哈希对齐，列出丢失 11 条边的源方法；在真机开启模块后核对 Mine 页账号卡与 VIP 状态替换是否触发，并检查是否有未归类调用者绕过该模型。
- 证据：E010, E000

### F001：评论页 5 家族并存且模块安装器覆盖未验证；Kotlin MOSS 定义数与实调边数不可互推覆盖率
事实：评论页 5 条路径在 9.16.0 均有静态外调边且 status 保持 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E001、E017），其中 comment_compose 规模最大（2446 类、278 compose 方法、932 边），comment_native_legacy 类 156→172、边 177→209 为增幅最大的非 Compose 家族；五族指纹全部改变（E001）。推断边界：指纹变化可由混淆短名轮换、DEX 重排或编译器差异造成，不能据此判定新样式。E011 仅返回 5 个类样本且 compose_signatures 全空，无法代表 278 个 compose 方法或安装器命中形态。协议层 comment_java_moss 为 50 定义/50 实调边、comment_kotlin_moss 为 130/26，两侧一致；定义数包含重载与 $default 桥接（对照静态证据 E020，同一业务方法可展开为 4 个签名变体），因此定义数与实调边数属不同单位，不能相除或直接解读为“多数声明无消费者”；评论侧 caller 抽样本轮未取得，是否存在跨家族消费者仍未知。本轮未读 CommentClassicStyleLocator、CommentComposeViewAccess、CommentNativeBindingCatalog、CommentPurifyFeatureInstaller 等模块源码，故“若按旧类名/签名注册则新增类可能落在 Hook 之外”仅为待验证假设。反例：新增类可能为空实现、数据类或重复包装层，边数上升也可能来自包装层而非新样式；服务端 A/B 无结构变化时静态不可见。
反例与替代解释：若真机日志显示 CommentComposeViewAccess 与 NativeBindingCatalog 在所有已触发样式下命中计数非零，则“新增类落在 Hook 之外”的推断被推翻；若新增类均为空实现/纯数据类，或方法名归并后 Kotlin MOSS 声明多数有消费者，则不构成 Hook 缺口；若同签名方法体哈希一致，则类数/边数变化应记为混淆或重排而非新样式。
建议：1) 真机（灰度账号）逐一触发 legacy_v2/native_legacy/next/exp3/compose 五种样式，记录 Hook 命中类名、失败类名与安装器版本判定日志；2) 按文件哈希重读 CommentClassicStyleLocator、CommentComposeViewAccess、CommentNativeBindingCatalog、CommentPurifyFeatureInstaller，提取实际匹配常量并核对 9.16.0 类清单；3) 对 comment_native_legacy 新增类与 comment_kotlin_moss 的 130 个声明按方法名归并后再统计消费者，避免把 $default 桥接重复计为覆盖率缺口。
证据：E001, E011, E017, E020

### F002：动态 Compose 家族类 956→1136，样本落在关注列表/宽屏 Compose 包装层，但增长来源未定位
事实：dynamic_compose 类 956→1136、compose 方法 112→127、外调边 170→220，fingerprint 由 84a035d3… 变为 3c0596bc…（E002、E018），为本页最大变化；同页 dynamic_legacy 类 3227→3252 而边 2193→2152（类增边减），dynamic_opus 基本持平（92 compose 方法、边 190→191）。E019 的 5 个类样本（占 1136 类的有界抽样）全部位于 kntr/app/following/followinglist，字段含 FollowingListViewModel、ui/wide/i、State/MutableState/ComposableLambda，方法多为 <init>/invoke 的 lambda 包装，compose_signatures 全空——可证该家族承载关注列表（含宽屏）Compose 实现，但不能据此认定新增的约 180 个类集中在该前缀或该包装层，也未观察到可被 @Composable 签名定位的方法。推断：若安装器依赖固定类名或 Composable 签名，新增包装层存在漏挂风险；但该风险目前只有样本级证据。反例：混淆短名序号变化、DEX 重排、编译器版本差异都会同时改写类数、边数与指纹；9.16.0 也可能只是同一实现被拆成更多合成 lambda 类。服务端开关与平板/宽屏分支的实际启用条件未读到运行证据。
反例与替代解释：若两侧前缀对照显示同类包装层在 9.15.0 已存在、仅短名序号变化，则变化应记为混淆重排而非新增层；若真机日志显示新旧包装均被命中且注入一次，则功能层不受影响；若增量为内联合成 lambda（编译器产物），不构成可 Hook 的独立入口。
建议：1) 两侧按 kntr.app.following 前缀做去混淆式类清单对照（比较字段类型集合、ComposableLambda/State 数量与 ui/wide 分支，而非短名序号），判定 +180 类的归属；2) 平板/宽屏与手机两种形态分别录制跟随列表动态流的 Hook 命中日志，核对 DynamicTabsFeatureInstaller/DynamicPurifyFeatureInstaller 的安装条数；3) 对同签名方法体哈希做基线对照，为“改名/重排而非新样式”提供反证。
证据：E002, E018, E019

### F003：动态页协议消费者跨家族且含未归族调用者；Opus 相关 MOSS 归属与模块入口未验证
事实：模块登记协议为 dynamic_java_moss（134 定义/134 实调边）与 dynamic_kotlin_moss（382/26），两侧一致（E002、E018）。E020 的 26 条 dynamic_kotlin_moss 实调边 caller 抽样显示消费者跨三个族：dynamic_legacy（Lcom/bilibili/bplus/followinglist/service/b1 调 subscriptionClick 等）、dynamic_compose（Lkntr/app/following/followinglist/data/l 调 dynAll、dynTab、dynVideo、dynDetails、dynFriend、feedFilter、dynAllPersonal、dynVideoPersonal）、以及静态矩阵中未登记的候选族 dynamic_other:commonCore（Lkntr/app/following/commonCore/interaction/InteractionServiceImpl）。种子未注册协议清单包含 DynamicMoss、OpusMoss、KOpusMoss、CampusMoss、KTribeeMoss、OpusMoss（E000），但本轮抽样未观测到这些接口的调用者。推断：动态与 Opus 数据可能全部经已登记的 KDynamicMoss 下发，也可能存在未登记接口的并行消费者；在后一种情况下，若模块净化/解析入口只绑定已登记类，Opus 或校园等多来源卡片可能落到兜底逻辑。反例与边界：未登记协议存在不等于页面使用；实调边数 26 只是观测上界，接口分发、协程边界与动态代理均可能隐藏调用；定义数含重载与 $default 桥接（E020 可见同一方法 4 个签名变体），不得与边数相除推出覆盖率。
反例与替代解释：若真机抓包与 KotlinDynamicMossWatch 日志显示动态与 Opus 请求均落在已登记 KDynamicMoss 且模块入口覆盖这些调用点，则覆盖担忧不成立；若 Opus 数据由已登记接口返回但字段层另有解析器，则风险转移到解析层而非协议层。
建议：1) 对 KOpusMoss/OpusMoss/CampusMoss/KTribeeMoss 单独取 caller 证据，确认动态页 Opus 卡片实际请求的服务；2) 把 dynamic_other:commonCore 归族并评估其是否位于动态页净化入口路径；3) 按文件哈希重读 DynamicPurifyFeatureInstaller、DynamicPurifyPolicy、KotlinDynamicMossWatch，核对入口是否只依赖已登记协议类及是否有兜底；4) 真机抓包 + KotlinDynamicMossWatch 日志比对实际服务名与静态消费者集合。
证据：E000, E002, E018, E019, E020

### F004：home_new_frame 指纹改变但类数与 Compose 方法数不变，倾向改名/重排而非新样式（缺基线样本比对）
事实：目标 9.16.0 home_new_frame 为 196 类、33 个 Compose 方法、48 条外部调用边，指纹 08696567…；基线 9.15.0 为 196 类、33 个 Compose 方法、46 条外部调用边，指纹 e3ea6856…（E003）。事实：E014 目标侧样本（file_id 24）包含 Ltv/danmaku/bili/khome/widget/bubble/r（a/b 短名方法，参数类型 bubble/t、Function0）、bubble/d（a()/c() 返回 J）、bubble/e（getId/getImageUrl/getUrl）、bubble/f（a(bubble/g)Z、b(bubble/e)V）以及 Ltv/danmaku/bili/khome/vm/HomeFrameViewModel$dispatchAction$1（字段 $action:Lap1/b;、this$0:HomeFrameViewModel，方法 create/invoke/invokeSuspend）。推断：在类数与 Compose 方法数恒定、仅外部调用边 +2 的情况下，结构指纹变化更可能来自混淆改名、DEX 重排或短名类重新编号，而不是启用新样式框架；但本轮只有目标侧类样本，基线侧类样本未重新读取，“同名类沿用”仅由计数不变推出，未做逐类签名对齐。未知：HomeFrameListHook/HomeFrameTabLocator 实际匹配的类名、字段名以及 ap1/b 的对应关系未读到，定位器在 9.16.0 是否命中未知；静态调用存在不证明运行时启用。
反例与替代解释：可推翻当前推断的证据：①基线侧样本比对显示 bubble/r、bubble/e 等在 9.15.0 存在相同签名，则指纹变化纯属重排，推断成立但需记录为“无结构变化”；②HomeFrameViewModel 或 dispatchAction 的 $action 类型在新版缺失或改签，说明确有迁移；③真机日志显示新框架主页加载了 E014 之外更多 khome 子包的 Composable 并带新布局入口；④定位器命中率与基线一致而过滤行为改变，指向行为层而非结构层变化。
建议：先补基线侧对照再下结论：对 9.15.0 与 9.16.0 分别读取 home_new_frame 家族类样本，逐个对齐 HomeFrameViewModel、dispatchAction 参数类型 ap1/b 及 khome/widget/bubble 各短名类的完全限定名与方法签名；同时重读 HomeFrameTabLocator.kt/HomeFrameListHook.kt 提取匹配常量，核对是否依赖被重编号的短名类。之后在 9.16.0 真机往返切换新版主页 tab，检查安装器日志中定位器是否命中。若签名逐类对齐而指纹仍变，按重排/改名处理；若出现新签名的 Compose 布局入口，则改登记为新样式候选。
证据：E003, E014

### F005：home_legacy 规模显著收缩，旧类名定位 Hook 存在静默失效风险
事实：home_legacy 类 1004→769（−235）、Compose 方法 128→87（−41）、外部调用边 236→211（−25），指纹 aa99feb8…→8772cd6d…（E003）。事实：E013 目标侧样本（file_id 24）仍含 Ltv/danmaku/bili/ui/main2/A（持 HomeFragmentV2、ArgbEvaluator、ImageView，实现 onAnimationUpdate）、main2/A0（WatchLaterFragmentV2 的 DialogInterface.OnClickListener）、main2/userprotocol/n（w5(String)）以及 AccountMineRequestResource 枚举（可见 REFRESH/RESELECTED/RESUME/ACCOUNT_UPDATE 常量），说明旧版 Main2 主页骨架在目标包内仍可观察到；同时 home_new_frame 外部调用边仅 46→48，减少的 235 个类未体现在已登记新框架家族中。推断：收缩可能来自组件迁往未登记家族、混淆合并/匿名类内联，或裁掉重复包装层；但本轮 E013 只有 5 个类样本且摘录被截断，不能代表 769 类整体，也不能据此确认“迁移”。未知：消失类的归属包区间未读取；模块 HomeComponentFilterFeatureInstaller/HomeTopBarFeatureInstaller/HomeBannerFeatureInstaller/HomeFrameListHook 的匹配目标（类名常量、方法签名）本轮未读取或未复核，因此“旧类名定位 Hook 静默失效”只登记为风险而非结论。
反例与替代解释：替代解释：①减少主要来自混淆合并、匿名类内联或短名重编号，功能未消失；②部分类被搬入 khome 但归入未登记家族，因此在已登记矩阵中不可见；③服务端开关在目标版本关闭旧主页，代码保留但路径不启用，静态不可见；④旧主页在 9.16.0 已降级为兜底，实际入口走新框架（需真机确认哪个栈渲染）。若包级差分显示消失类集中于纯工具/匿名类且旧主页关键入口签名不变，应撤回“迁移”推断。
建议：最小补证任务：对 9.15.0 与 9.16.0 的 Ltv/danmaku/bili/ui/main2/* 与 khome/* 做包级类清单差分，标出消失的 235 个类归属包并区分匿名/合成类；重读 HomeComponentFilterFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt、HomeBannerFeatureInstaller.kt、HomeFrameListHook.kt 提取类名与方法签名常量并逐条对照；在 9.16.0 真机进入旧版主页触发顶部栏、Banner 与组件过滤，采集 Hook 安装与命中日志，区分“类未加载”与“加载但未命中”。
证据：E003, E013

### F006：搜索双栈并存且 MOSS 协议面无变化，模块跨栈覆盖未读到需补证
事实：search_native 类 1674→1702、外部调用边 2789→2851（增长），Compose 方法恒为 2；search_compose 类 3149→3145、Compose 方法 556→561、外部调用边 616→594（下降）；两条路径指纹均改变（E004）。协议层 search_java_moss 24 定义/22 实际调用边、search_kotlin_moss 52 定义/18 实际调用边，目标与基线完全一致，说明搜索相关 MOSS 协议定义与消费边在本次升级未改。推断：搜索页仍是原生+Compose 双栈并存，变化属于栈内重排/局部新增，而非某一栈被替换；协议层未变意味着净化若走协议层则不易受本次结构变化影响，但若走 UI 定位器则可能只覆盖单栈。未知：SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller 的解析点与安装器覆盖本轮未能读取（module_source 与 search_compose 深挖均被额度拒绝），未登记协议中的 app/interfaces/v1 与 app/search/v2 SearchMoss 是否有跨家族消费者也未确认。
反例与替代解释：可推翻当前推断的证据：①真机日志显示搜索首页只走其中一栈（另一栈 dead code），则双栈并存不成立；②Compose 侧 +5 方法若全为新推荐卡 Composable，则可能是新样式候选而非重排；③若定位器日志显示两栈均被命中，则跨栈覆盖风险不成立；④若未登记 SearchMoss 的跨家族消费者持有搜索首页数据，则协议层“未变”不能推出净化不受影响。
建议：最小补证任务：重读上述四个模块文件，列出其目标类名/方法签名常量；与 E004 家族样本及 MOSS 定义做交叉核对；真机在原生与 Compose 搜索首页分别触发默认词清理与推荐卡净化并抓命中日志；同时确认搜索首页是否受服务端样式开关控制而静默切换栈。
证据：E004

### F007：pgc_theseus 外部调用边 742→1328（约 +79%）而类数仅 +15、Compose 131 不变，需先区分解析差异与真实新增调用路径
事实：E006 显示 pgc_theseus 在 9.16.0 为 2264 类/131 Compose 方法/1328 外部调用边，基线 9.15.0 为 2249/131/742，指纹由 e02d9f27… 变为 ede5e8c1…；类增 15、Compose 方法零增长而调用边增 586，说明新增边并非来自成批新增的 Compose 页面类。推断（未验证）：新增边可能来自既有类之间新解析出的调用（内联减少、去虚拟化、DEX 重排/解析顺序变化），也可能来自少数既有类新增了对外部家族的密集调用；两种解释对模块影响不同，前者可能无需适配动作，后者可能需要扩展 PgcAutoActivityPopup 相关策略。限制：调用边不解析接口分派，也不证明运行时激活；本轮 family_evidence/decompile_class/module_source 深挖因额度限制未执行，新增边未落到具体源类与目标类，pgc_view_moss（14 定义/7 实调边）与 pgc_player_moss（12/3）的消费者家族也未取证；安装器与定位器源码未读，Hook 覆盖保持未知。
反例与替代解释：可推翻当前 candidate 的证据：(1) 若 586 条新增边的源方法体哈希在基线同签名方法中已存在，只是解析器或文件顺序差异，则判定为非变更；(2) 若新增边目标集中在与净化无关的基础库（日志/协程/序列化），则对模块影响可排除；(3) 若 pgc_view_moss 的 7 条实际调用边与新增边无交集，则协议消费者未受影响。反之若出现新源类且其字段/签名与活动弹窗定位点一致，则升级为 static_evidence 级风险。
建议：用 family_evidence 重读 pgc_theseus 目标侧完整类/方法样本，对两版按“调用边目标包”聚合对比 742 与 1328 的分布差异，把新增边落到具体源类与目标类；对新增边源类用 decompile_class 检查是否只是同一方法的拆分/桥接方法。若确认存在新调用者，再读快照中的 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt、PgcAutoActivityPopupPolicy.kt（source_snapshot 工作树 dirty，需按文件哈希追溯）核对定位签名与兜底扫描是否覆盖；最后在真机开关 PgcAutoActivityPopupFeature 前后对照 PGC 详情页模块与自动弹窗表现。
证据：E006, E000

### F008：detail_theseus_united 类数 4602→4579 而调用边 4163→4312；detail_kotlin_moss 76 定义仅 10 条实际调用边，模块兜底与安装器覆盖未知
事实：E005 显示 detail_theseus_united 类数 -23、Compose 98→99、外部调用边 +149、指纹变化；detail_theseus_ugc 类数 -6、调用边 -6、Compose 25 不变；detail_legacy 两版均 absent（空集合哈希）。detail_java_moss 32 定义/35 边与 detail_kotlin_moss 76 定义/10 边两版完全一致。推断：详情页存在两组并存静态栈（ugc 与 united），未读运行条件，因此无法判断 9.16.0 真机上哪一组实际渲染，也无法判断模块是否两者都装 Hook；Kotlin Moss 定义多而实测调用边仅 10 条，提示其协议消费者入口在静态视图中稀少，若模块仅按少数入口定位，存在漏挂风险；但定义数与调用边单位不同，不能相除推导覆盖率。限制：全部路径 module_coverage=requires_installer_review、runtime_enabled=unknown，且本单元未读任何模块源码与安装器，Hook 覆盖不得推测。
反例与替代解释：可推翻当前 needs_runtime 判断的证据：(1) 若被删除的类与模块解析点无关（纯 DTO/工具类），则影响可降级为无适配动作；(2) 若真机日志显示 only ugc 栈被启用、united 仅为宽屏/实验分支，则 united 的变化可降权；(3) 若 DetailUnitedModulePurifyFeatureInstaller 明确按兜底扫描（如遍历模块列表接口）而非固定类名，则类数变化不构成失配；(4) 若 10 条 Kotlin Moss 调用边覆盖全部实际渲染入口，则漏挂推断不成立。
建议：先做静态最小补证：用 family_evidence 分别重读 detail_theseus_ugc/united 两版类样本，列出被删除的 6/23 个类名与新增的 Compose 方法所属类，确认是否为推荐/广告模块载体；用 family_evidence（或 protocol_evidence）确认 10 条 Kotlin Moss 调用边的具体消费者类，并与 DetailModulePurifyFeatureInstaller/DetailUnitedModulePurifyFeatureInstaller 中的解析类名集合比对。再做真机验证：同一详情页依次走 ugc/united 两种入口，采集模块 Xposed 日志，确认各 installer 是否真的安装并命中；对 absent 的 detail_legacy 需在真机确认已无该路径入口。
证据：E005, E000

### F009：player_kotlin 计数不变仅指纹变化，优先按混淆/DEX 重排解释，不应视为新播放器 Kotlin 样式
事实：player_kotlin 两侧 classes=7、compose_methods=0、external_invoke_edges=100 完全一致，只有 fingerprint 由 b275709b… 变为 544b8dec…；同侧 player_kotlin_moss 仍为 34 定义/3 实调边（E007）。推断：在类数与调用边数均无变化的前提下，指纹变化更可能来自混淆改名、方法体顺序、常量池或 DEX 重排，而非新增样式族。待真机验证：模块中按字符串类名锚定的 Kotlin 播放器定位器是否仍命中，以及 3 条实调边的实际消费者。反例：若类级 diff 显示有类被重命名且同时新增了包装层，或 3 条实调边之外的消费者发生迁移，则“仅哈希漂移”的推断被推翻，需要真实新增适配。
反例与替代解释：可推翻本推断的证据：类级 diff 显示方法体语义变化（非仅顺序/常量池）；模块日志显示定位器在 9.16.0 解析失败；发现原有 3 条实调边的消费者数量或签名改变。
建议：先做两侧 7 个类的类名+method_bodies_sha256 对照表，再决定是否需要为新名补定位器；不要因为指纹变化新增重复包装钩子。真机用播放器 Kotlin 路径触发一次并记录 Hook 命中日志。
证据：E000, E007

### F010：danmaku_legacy 两侧 absent 而 danmaku_kotlin 边数 9→8，旧家族缺失与唯一候选家族并存，跨家族协议消费者未明
事实：danmaku_legacy 在 9.16.0 与 9.15.0 均 classes=0、边 0、指纹相同（E008），即两侧一致地 absent；danmaku_kotlin 56→57 类、外部边 9→8、指纹变化，danmaku_java_moss 22 定义/20 实调边与 danmaku_kotlin_moss 46 定义/4 实调边两侧完全不变。推断：弹幕共同协议未变，家族层发生类级重组；absent 不能证明旧原生弹幕功能消失，更可能是识别规则未覆盖或类迁移。未知：20 条 danmaku_java_moss 实调边由哪些家族/页面消费，是否存在 Kotlin 家族跨家族调用者，以及 DanmakuPurifyFeatureInstaller 在 9.16.0 是否仍解析到目标类——本单元未读到源码，不作推测。待真机验证：净化/屏蔽开关的实际行为差异。
反例与替代解释：可推翻本推断的证据：放宽识别后 danmaku_legacy 出现非零类数（说明是识别漏检）；danmaku_java_moss 实调边调用者全部落在 danmaku_kotlin（说明协议层已被新家族接管）；真机日志显示净化钩子在 9.16.0 上仍正常命中（说明影响有限）。
建议：补证顺序：1) 用放宽的家族识别参数复跑 danmaku_legacy，区分识别漏检与真实缺失；2) 拉取 danmaku_java_moss 20 条实调边的调用者清单，标注所属家族与页面；3) 真机在 9.16.0 上开启弹幕净化与屏蔽词，观察是否有 Hook 命中及可见效果；4) 若两侧均无命中，再考虑新增弹幕家族候选，而不是直接修补旧家族钩子。
证据：E008, E000

### F011：story_native 类数与调用边小幅下降而 Compose 面不变，裁剪与重排仍未区分
事实（E009，两版同签名证书、同仓库冻结 APK，见 E000）：9.16.0 story_native 为 2925 类 / 44 Compose 方法 / 1318 外部调用边，基线 9.15.0 为 2958 / 44 / 1380，指纹 6b74bce4…→7fffa3be…；story_kotlin 两侧均为 0 类 / 0 边 / 空集指纹 4f53cda1…、evidence=absent。推断：类数 -33、边数 -62 同步收缩而 Compose 方法数完全不变，至少两种解释并存——真实分支裁剪或实现迁移，或混淆改名与 DEX 重排；结构哈希变化本身不能作为新样式依据。证据边界（重要）：本轮 E009 仅下发家族摘要（limits 声明 two class samples per family，实际内容无 story 类样本），story 家族没有任何类名/方法体哈希可比；草稿中“混淆敏感”的论证是借 E011（comment_compose 的 kntr/common/comment 短名类）与 E012（dynamic_compose 的 kntr/app/following 短名类）类推，属其他页面证据，不能作为 story 家族结论。未知：消失的 62 条边对应哪些入口、是否包含模块依赖的回调；运行期启用与安装器覆盖均未读（E000 仅列候选文件，快照 working_tree_dirty）。
反例与替代解释：若方法体哈希对齐后 33 个类在目标版均有同哈希配对（仅类名变化），变化应归为混淆改名/DEX 重排，对模块影响的推断可撤销；若交集为空且真机 Hook 命中数与基线一致，则计数下降与适配无关；若缺失方法正落在模块注入点且真机不再命中，则升级为真实调用路径缺失（仍需真机证据，不能凭静态推断定论）；若仍拿不到 story 类样本，应保持“裁剪与重排未知”，不得二选一地下结论。
建议：第一步补证：在可访问 APK/反编译的环境，以 method_bodies_sha256 为键对 9.15.0 与 9.16.0 的 story_native 做集合差，输出仅存在于基线的类与方法签名，并统计“同哈希不同类名”的配对数量，直接区分重排与真实删除。第二步：把仅存在于基线的方法签名与模块 StoryActionIconsFeatureInstaller/StoryActionIconsPolicy/StoryPurifyFeatureInstaller/HomeVerticalDetail* 的定位目标求交（需先读源码正文并记录文件哈希，工作树 dirty），交集非空则列为高风险入口。第三步：真机打印上述安装器的命中类/方法与版本门限判定日志，仅在命中证据齐备后再讨论 module_coverage。
证据：E009, E000, E011, E012

### F012：mine_account_model 类数不变而外部调用边减少 11 条，MineVip/账号卡定位点待核
事实（E010，同签名证书与同仓库冻结 APK 见 E000）：mine_account_model 两侧均为 132 类 / 0 Compose 方法，外部调用边 54→43（-11），指纹 d5370d6e…→ddcfc5ef…；mine_native 324→328 类（+4）、95→91 边（-4）、Compose 方法 7→7，指纹 cf69dfa7…→66c1fa8a…。推断：类数完全不变而出边减少 11，更像方法体内对外调用被内联/收敛，或聚合入口迁移到其他类，而非整体重写。跨家族线索：E013（home_legacy 目标样本）中出现 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource 枚举（ACCOUNT_UPDATE/REFRESH/RESELECTED），说明账号刷新资源在 home 家族亦被使用，mine 侧消费者可能不是单一入口；该枚举是否属 mine_account_model 的同一模型消费者尚未确认。协议面：种子 mine.protocols 为空，而 E000 未登记协议清单含 MineMoss、KMineMoss、AccountInterfaceV1Moss/K 系列，服务端开关或无结构变化的新通道静态不可见。未知（不作推测）：E010 只下发家族摘要、无 mine 类样本，丢失 11 条边的源方法未定位；“是否触及 MineVipFeatureInstaller 与 HostMineReadingCard 依赖的读取路径”需读源码与真机日志才能判断，草稿原表述已撤回为待核。
反例与替代解释：若丢失的 11 条边全部落在与账号/VIP 无关的工具或日志类，对模块影响可判为低；若真机日志显示 VIP 替换与组件快照均正常触发，则边数下降属编译器内联或 DEX 重排产物；若真机显示组件快照采集不到新增块或 VIP 替换不再触发，才确认为真实影响并需补兜底定位器；若 E013 的 AccountMineRequestResource 确认为同一模型消费者，还需评估 home 家族入口是否会绕过 mine 侧 Hook。
建议：先用 method_bodies_sha256 对 132 个类做两版逐类对齐，列出丢失 11 条边的源方法所属类，并标注是否为账号/VIP 字段读取；再读 MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineVipFeatureInstaller、MineComponentSnapshotHostBridge/QueryClient/Store 正文并记录文件哈希（快照 working_tree_dirty，按哈希追溯，不建议清理工作树）；真机在 Mine 页打印 MineComponentSnapshot 实际采集的组件标识/数量与 VIP 替换日志，分别覆盖登录/未登录与手机/宽屏四组条件，并与设置页可见项对照。
证据：E010, E000, E013

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
评论页 5 条路径在 9.16.0 与 9.15.0 两侧均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E001、E017），本单元不改变任何 status。规模：comment_legacy_v2 579 类/743 边。变化：legacy_v2 581→579 类、734→743 边；comment_native_legacy 156→172 类、177→209 边（本页非 Compose 最大增幅）；comment_native_next 类持平 45、边 46→49；comment_native_exp3 60→58 类、59→61 边；comment_compose 2417→2446 类、274→278 compose 方法、918→932 边。五族指纹全部改变，但同证书、包名不变前提下，混淆短名轮换与 DEX 重排即可改写指纹，不能据指纹认定新样式。E011 只取 5 个类样本，compose_signatures 全空、含空方法体类，不能外推到 278 个 compose 方法或 Installer 命中形态。协议侧 comment_java_moss 50 定义/50 实调边、comment_kotlin_moss 130/26 两侧一致；定义数含重载与 $default 桥接（静态证据 E020 显示同一业务方法存在多个签名变体，如 alumniDynamics 4 个），故 130 与 26 不是覆盖率分子分母；本轮 comment_kotlin_moss 的 caller 抽样因工具额度被拒，评论侧是否存在跨家族消费者仍未知。模块源码（CommentClassicStyleLocator、CommentComposeViewAccess、CommentNativeBindingCatalog、CommentPurifyFeatureInstaller 等）本轮未读，因此定位器匹配常量、安装器覆盖率与兜底逻辑一律记为未知；服务端 A/B 无结构变化时静态不可见。
证据：E000, E001, E011, E017, E020

### 复核页面：dynamic
动态页 3 条路径两侧均为 static_invoke_observed（E002、E018）：dynamic_legacy 3252 类/105 compose 方法/2152 边、dynamic_compose 1136/127/220、dynamic_opus 1354/92/191，runtime 与安装器覆盖保持不变，本单元不升级状态。变化：legacy 类 3227→3252 但边 2193→2152（类增边减）；compose 类 956→1136（约 +19%）、compose 方法 112→127、边 170→220，为本页最大变化；opus 类 1341→1354、compose 方法持平 92、边 190→191。三族指纹全变，混淆改名/DEX 重排同样改写指纹，未做类名归并对照前不能判为新样式。E019 深挖仅 5/1136 类，全部位于 kntr/app/following/followinglist（A–E），字段含 FollowingListViewModel、ui/wide/i、State/MutableState/ComposableLambda，属 Compose lambda 包装，compose_signatures 全空：可证该家族绑定关注列表（含宽屏）Compose 实现，但不足以解释 +180 类来源，也无法判断安装器是否漏挂（按 @Composable 签名定位时可能完全不可达）。协议侧 dynamic_java_moss 134/134、dynamic_kotlin_moss 382/26 两侧一致；E020 显示 26 条实调边消费者跨 dynamic_legacy（bplus/followinglist/service/b1）、dynamic_compose（kntr/app/following/followinglist/data/l 调 dynAll/dynTab/dynVideo/dynDetails/dynFriend/feedFilter/dynAllPersonal/dynVideoPersonal）以及未登记候选族 dynamic_other:commonCore（InteractionServiceImpl），即已登记 Kotlin MOSS 确有跨家族消费者；未登记 OpusMoss/KOpusMoss/CampusMoss/KTribeeMoss 在本轮抽样中无调用者，Opus 数据源归属仍未知。所有结论待真机、分组与模块源码补证。
证据：E000, E002, E018, E019, E020

### 复核页面：home
home 页两条登记路径本轮重新取证后的状态：home_legacy 与 home_new_frame 的 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E003），因此两条路径都不判定适配结果，也不得升级为通过。home_legacy：类 1004→769、Compose 方法 128→87、外部调用边 236→211，家族指纹 aa99feb8…→8772cd6d…（E003）。目标侧样本 E013（file_id 24）仍包含 Ltv/danmaku/bili/ui/main2/A（持 HomeFragmentV2、ArgbEvaluator、ImageView，实现 onAnimationUpdate）、A0（WatchLaterFragmentV2 的 DialogInterface.OnClickListener）、userprotocol/n 与 AccountMineRequestResource 枚举，说明旧 Main2 主页骨架在目标包内仍可观察到；但样本只有 5 个类且摘录被截断，不能代表 769 类，也不能据此断言“迁往 khome 新框架”，减少的 235 类归属包未读取。home_new_frame：类数 196、Compose 方法 33 两侧一致，仅外部调用边 46→48，指纹 e3ea6856…→08696567…（E003）；E014 目标侧样本可见 Ltv/danmaku/bili/khome/widget/bubble/{r,d,e,f} 与 HomeFrameViewModel$dispatchAction$1（字段 $action:Lap1/b;），但本轮未重新读取基线侧类样本，“同名类沿用”只来自计数不变而非逐类比对。两条路径的模块侧定位器（HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilterFeatureInstaller 等）签名与安装器覆盖本轮均未读取，Hook 是否实际命中明确未知；静态调用存在不证明路径在真机启用。最小补证：ui/main2/* 与 khome/* 包级类清单差分、两侧同签名方法比对、真机旧/新主页 tab 切换与过滤功能命中日志。
证据：E003, E013, E014

### 复核页面：search
search 页两条登记路径本轮重新取证后的状态：search_native 与 search_compose 的 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E004），不判定适配。search_native：类 1674→1702、外部调用边 2789→2851、Compose 方法恒为 2，指纹 481dae50…→bc8afdf5…，规模净增长，没有静态迹象显示该栈被替换；新增 28 类的归属包未读取，若模块定位常量指向的类被改名则会静默失配，命中与否未知。search_compose：类 3149→3145、Compose 方法 556→561、外部调用边 616→594（−22），指纹 6c663f2d…→e0ff4112…，方法数微增而调用边下降方向相反，可由 Lambda/包装类合并、内联或调用迁移解释，静态无法判定；本轮未对 search_compose 家族类样本做深挖，不能把 −22 边读成整族失效或新样式。协议面：search_java_moss 24 定义/22 实际调用边、search_kotlin_moss 52 定义/18 实际调用边，目标与基线完全一致（E004），说明已登记 MOSS 协议面本次升级未见结构变化；但未登记清单中的 app/interfaces/v1 SearchMoss/KSearchMoss、app/search/v2 SearchMoss/KSearchMoss、broadcast/message/search/SearchMoss 是否存在跨家族消费者未确认，不能据此推出“净化不受影响”。SearchHomeRecommendLocator/SearchHomeRecommendPolicy/SearchDefaultWordsCleaner/SearchPurifyFeatureInstaller 的解析点与安装器覆盖未读取，原生/Compose 两条栈的覆盖差异（是否只覆盖其中一栈）明确未知。最小补证：模块定位常量与两栈类清单交叉核对、双栈真机净化前后对照与定位器命中日志、服务端样式开关分组记录。
证据：E004

### 复核页面：detail
复核 E005：三路径数值与状态字段和静态矩阵一致——detail_legacy 两侧 absent（类数 0、Compose 0、边 0、指纹常量 4f53cda1…）、detail_theseus_ugc 1947 类/25 Compose/509 边（基线 1953/25/515）、detail_theseus_united 4579/99/4312（基线 4602/98/4163）；detail_java_moss 32 定义/35 边、detail_kotlin_moss 76 定义/10 边两版相同。草稿未把指纹变化当成新样式，未提升 status，符合约束。需保留的两处收紧：其一，“空集合哈希”是对常量指纹的推断而非证据直述，应标为推断；其二，prefetch 限每家族 2 个类样本，样本不可外推为整套实现，ugc/united 的类名与 method_bodies_sha256 逐类 diff 未做。协议侧仅知定义数与实调边数相同，10 条 Kotlin Moss 实调边的消费者类未取证，跨 ugc/united 与 Java Moss 的分布未知，不得据此判断模块入口覆盖。安装器/定位器源码（快照中存在、工作树 dirty）本轮未读，故 module_coverage 保持 requires_installer_review、runtime_enabled 保持 unknown，Hookup 覆盖不得推测。
证据：E005, E000

### 复核页面：pgc
复核 E006：pgc_legacy 354 类/0 Compose/386 边（基线 353/0/401）、pgc_theseus 2264/131/1328（基线 2249/131/742），两侧指纹均改变；pgc_player_moss 12 定义/3 边、pgc_view_moss 14 定义/7 边两版一致，与草稿数值吻合。草稿正确拒绝把 +586 条调用边（约 +79%）判为新样式或页面新增，并列出了“解析/编译差异”与“真实新增调用者”两种解释，也未把协议定义数除以调用边数推导覆盖率，方向可保留。缺口在证据层：没有按调用边目标包聚合的分布 diff，也没有类名与 method_bodies_sha256 的逐类比对，586 条新增边未落到源/目标类；pgc_legacy 的 +1 类与 -15 边同样未定位；PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt、PgcAutoActivityPopupPolicy.kt 未读，定位签名与兜底扫描方式未知；运行条件、平板/宽屏分支与服务端开关无任何证据，只能记未知。两路径 status 均应保持 static_invoke_observed。
证据：E006, E000

### 复核页面：player
复核 player 两条登记路径与 E007 逐项对照无误：player_java 类 953→957、外部调用边 3225→3229、指纹 4102698f…→f99b126d…，属规模与结构同时变化；player_kotlin 类 7、compose_methods 0、边 100 与基线完全相同，仅指纹 b275709b…→544b8dec… 变化，符合混淆改名/DEX 重排的解释，尚不构成新样式证据。协议侧 player_java_moss 18 定义/2 实调边、player_kotlin_moss 34 定义/3 实调边两侧一致，协议面未扩张。两条路径 evidence 均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，因此不判定适配结果。关键缺口未被草稿跨过：+4 类未做类级 diff（是解析入口、包装层还是混淆拆分无法区分）；18 与 34 个协议定义中仅 2 与 3 条有实调边，其余消费者静态不可见；PlayerSpeedLocator、PlayerBufferLocator、SponsorPlayerLocator 的匹配方式（字符串类名/签名/结构特征）本轮未读源码，不能推测覆盖。E007 每家族仅两个类样本，属有界摘录，不能代表整套播放器实现。结论保持 candidate/needs_runtime，需类级哈希 diff 与真机播放链路验证。
证据：E000, E007

### 复核页面：danmaku
复核 danmaku 两条登记路径与 E008 对照无误：danmaku_legacy 两侧 classes=0、compose_methods=0、边=0、指纹同为 4f53cda1…，evidence=absent；这是识别结果为空，不能推为旧原生弹幕已被移除，家族识别规则未覆盖或类迁移到更通用渲染层均未被排除。danmaku_kotlin 为唯一被观测到的候选（static_invoke_observed）：类 56→57、compose_methods 1、外部边 9→8、指纹 f55e24e0…→7f0a50d2…，类增边减可能来自类拆分/包装重复或调用收敛，仅凭计数不能判定新样式。协议侧 danmaku_java_moss 22/20、danmaku_kotlin_moss 46/4 两侧完全一致，说明共同协议未变，但 20 条实调边归属哪个家族、是否存在 Kotlin 侧跨家族消费者，预取只给了有界调用者样本，未给全集。DanmakuPurifyFeatureInstaller/Policy 源码本轮未读，module_coverage 仍为 requires_installer_review；runtime_enabled 一律 unknown。结论保持 candidate/needs_runtime，不得声称适配通过。
证据：E000, E008

### 复核页面：story
已用 fresh_refresh 复读 E009 核对：9.16.0 story_native 仍为 static_invoke_observed，2925 类 / 44 Compose 方法 / 1318 外部调用边，基线 9.15.0 为 2958 / 44 / 1380，指纹 6b74bce4…→7fffa3be…，两版同签名证书、同仓库冻结 APK（E000），状态值与草稿一致，未见把计数变化误写成适配结论。story_kotlin 两侧均为 0 类 / 0 边 / 空集指纹 4f53cda1…、evidence=absent，属“未检出”，草稿已明确不等于功能消失，表述可保留，但归族口径仍需真机日志确认。关键缺口：E009 的 limits 虽写 two class samples per family，本次下发内容只含家族摘要，无 story 家族任何类/方法体样本，因此“33 类与 62 条边的下降是裁剪、迁移还是混淆改名/DEX 重排”在 story 家族自身证据上无法定论——草稿用 E011（comment_compose）、E012（dynamic_compose）的短名混淆类做类推，已作为间接证据在 F011 修订中降级标注。protocols 为空而 E000 未登记清单含 Lcom/bapis/bilibili/app/story/v1/StoryMoss; 与 app/view 系列，说明协议消费者未登记到页面，跨家族消费者、共同协议兜底、宽屏与服务端开关分支均静态不可穷尽。模块侧只见 E000 的候选文件名（StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、HomeVerticalDetail*），正文未读、module_source 未执行，且在 working_tree_dirty 快照下需按文件哈希追溯，安装器命中与运行期启用一律 unknown，不得判为适配通过。
证据：E009, E000, E011, E012

### 复核页面：mine
已用 fresh_refresh 复读 E010 核对：9.16.0 mine_native 为 328 类 / 7 Compose 方法 / 91 边，基线 324 / 7 / 95，指纹 cf69dfa7…→66c1fa8a…；mine_account_model 两侧均 132 类 / 0 Compose 方法，外部调用边 54→43，指纹 d5370d6e…→ddcfc5ef…，与草稿数值一致，未把类数持平当作“无影响”。两条路径均保持 static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review，结论层级正确。值得补充的旁证：E013（home_legacy 目标样本）中出现 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource 枚举（ACCOUNT_UPDATE/REFRESH/RESELECTED），说明账号刷新资源在 home 家族亦被使用，mine 侧消费者可能跨家族，需在 mine 单元确认是否为同一模型入口，而不是默认只有单一调用面。种子 mine.protocols 为空，但 E000 未登记清单含 MineMoss、KMineMoss、AccountInterfaceV1Moss/K 系列，Service 端开关或无结构变化的新通道静态不可见。缺口：E010 同样只下发家族摘要，无 mine 类样本，132 类逐类方法体哈希对齐未做，丢失 11 条边的源方法未知；MineComponentFilter/Snapshot、MineVip、HostMineReadingCard、MineComponentSnapshotHostBridge/QueryClient/Store 源码未读，快照 dirty 需按文件哈希追溯，安装器命中、跨进程快照桥连通、VIP 替换与宽屏/登录两态行为均待真机验证。
证据：E010, E000, E013

- F001 / revised：核心事实成立（E001/E017 五路径均为 static_invoke_observed、runtime 与安装器覆盖未知；native_legacy 156→172 类/177→209 边；E011 样本 5 类且 compose_signatures 全空不可外推），但草稿把 comment_kotlin_moss“130 定义/26 实调边”当作覆盖不足的证据，违反定义数与调用边数不同单位、不可互推的规则：定义数含重载与 $default 桥接（E020 显示同一业务方法存在 4 个签名变体），该落差本身不证明消费者缺失；另评论侧 caller 抽样本轮被额度拒绝，跨家族消费者应写为未知而非“落差表明”。补丁删除该推断，保留“模块源码未读、安装器命中未验证”的 needs_runtime 定位。（E001, E011, E017, E020）
- F002 / revised：类数与边数变化、指纹改变均有 E002/E018 支持，E019 确认样本类位于 kntr/app/following/followinglist 且含 ui/wide、State/MutableState/ComposableLambda 字段，可证该家族包含关注列表（含宽屏）Compose 包装；但草稿标题与正文把“类数增长约 19%”与“宽屏包装层”并置，易被读成增长来源已定位，而样本仅 5/1136、compose_signatures 全为空，无法归因 +180 类，也无法判断安装器按 @Composable 签名是否可达。补丁把“同新包装层出现”改为“样本落在该前缀、增长未归因”，并明确混淆重排反例。（E002, E018, E019）
- F003 / revised：草稿把“种子中存在未登记 MOSS 协议”直接推导为动态/Opus 覆盖缺口，属未证明的推断：未登记协议清单（E000）是 APK 级存在性，不含调用者；且本轮新取得的静态证据 E020 显示已登记的 dynamic_kotlin_moss 确有跨家族消费者（dynamic_legacy 的 bplus/followinglist/service/b1、dynamic_compose 的 kntr/app/following/followinglist/data/l 调用 dynAll/dynTab/dynVideo/dynDetails 等、以及未登记候选族 dynamic_other:commonCore 的 InteractionServiceImpl），未登记 OpusMoss/KOpusMoss/CampusMoss/KTribeeMoss 在抽样中无调用者。补丁把结论收窄为“已登记 KDynamicMoss 消费者跨家族且含未归族调用者，Opus 侧协议归属未知”，保留 needs_runtime。（E000, E002, E018, E019, E020）
- F004 / revised：核心事实成立：E003 显示 home_new_frame 类数 196、Compose 方法 33 两侧一致，仅外部调用边 46→48 且指纹 e3ea6856…→08696567…；E014 确实包含 khome/widget/bubble 短名类与 HomeFrameViewModel$dispatchAction$1（$action:Lap1/b;）。但草稿把该样本描述为“同一 file_id 24 下仍存在”“与基线家族属同一职责层”，本轮 E014 只有目标侧样本、基线侧类样本未重新读取，“沿用/同层”来自计数不变而非逐类比对，属外推过度；且 module_source 未读，定位器匹配关系仍未知。据此降为更严格的表述并明确该推断的替代解释，保留 candidate 级别。（E003, E014）
- F005 / revised：计数变化（1004→769 类、128→87 Compose 方法、236→211 边、指纹改变）由 E003 支持，E013 也确证目标包内仍有 ui/main2 的 A/A0、userprotocol/n 与 AccountMineRequestResource 枚举。但草稿引用的 B0（BiliApiDataCallback 子类）与枚举“含 SELECTED…等 6 项与 getShowNextTips”在本会话 E013 摘录中被截断、不可见，属于复核无法确认的细节；“说明净减少部分未全部转入已登记新框架家族”亦把推断写成事实。故移除不可复核样本细节、弱化因果措辞，保留 needs_runtime。（E003, E013）
- F006 / retained：E004 支持全部计数与协议事实：search_native 1674→1702 类、2789→2851 边、Compose 方法 2；search_compose 3149→3145 类、556→561 Compose 方法、616→594 边；两侧指纹均改变；search_java_moss 24 定义/22 边、search_kotlin_moss 52 定义/18 边完全一致。analysis 已明确区分事实（计数与协议面）与推断（双栈并存属登记家族层面、单栈 dead code 为可推翻条件），并把模块解析点、安装器覆盖、未登记 SearchMoss 跨家族消费者都列为未知，未把低计数或未检出当作新样式或失效，故保留原表述与 needs_runtime 级别。（E004）
- F007 / revised：数值断言被 E006 完全支持：pgc_theseus 类数 2249→2264、Compose 131 两侧不变、外部调用边 742→1328（+586，约 +79%）、指纹 e02d9f27… → ede5e8c1…；level=candidate 与“未排除解析差异/重排”的状态相称，alternatives 给出了可推翻条件（同签名方法体哈希一致、新增边落在日志/协程等无关基础库、与 pgc_view_moss 7 条实调边无交集），recommendation 是具体可执行的补证路径（按目标包聚合、decompile_class 查桥接/拆分方法、再读 Locator/Installer、最后真机 A/B）。需修订的是过程性表述“本单元禁止深挖工具”：工具存在但本轮额度受限未执行，应如实记为未取证；同时已把“协议消费者家族未取证”“安装器未读即 Hook 覆盖未知”写入正文，避免读者误以为已核实。（E006, E000）
- F008 / retained：事实部分被 E005 支持：detail_theseus_united 4602→4579 类、Compose 98→99、外部调用边 4163→4312（+149）、detail_theseus_ugc 1953→1947、515→509、Compose 25 不变、detail_legacy 两侧 absent、detail_java_moss 32/35 与 detail_kotlin_moss 76/10 两版一致；正文明确写出“定义数与调用边单位不同，不能相除推导覆盖率”，未用 76/10 推覆盖率。并发栈表述有依据（矩阵中 ugc 与 united 同为 static_invoke_observed），且明确“未读运行条件，无法判断真机渲染哪一组”，未宣称 Hook 生效或适配通过。发现中“若模块仅按少数入口定位，存在漏挂风险”及“安装器/兜底未知”均为条件式表述，并在 alternatives 给出四条推翻条件（被删类为纯 DTO、united 仅宽屏/实验分支、安装器按兜底扫描、10 条实调边覆盖全部渲染入口），未把未知写成故障。level=needs_runtime 合理：既有安装器源码未读的静态缺口，也有真机入口与命中日志未采集的运行时缺口；本轮无需改文，但最终结论仍受“每家族仅 2 个类样本、源码快照 dirty”限制。（E005, E000）
- F009 / retained：E007 两侧数据逐项吻合：player_kotlin 目标与基线均为 classes=7、compose_methods=0、external_invoke_edges=100，只有 fingerprint 由 b275709b… 变为 544b8dec…，同侧 player_kotlin_moss 均为 34 定义/3 实调边。断言“计数不变时优先按混淆/DEX 重排解释、不视为新样式”与证据一致，且已明确标为 candidate 并列出可推翻证据（类级方法体语义变化、定位器解析失败、实调边消费者变化），未把指纹变化等同于适配结论。需注意其适用范围仅限 player_kotlin；同页 player_java 同时存在类 953→957、边 3225→3229 的实质变化，不由本结论覆盖。（E000, E007）
- F010 / retained：E008 支持全部事实陈述：danmaku_legacy 两侧 classes=0/边=0/指纹相同且 evidence=absent；danmaku_kotlin 56→57 类、compose_methods 1、边 9→8、指纹变化；两侧 moss 协议 22/20 与 46/4 不变。分析中明确 absent 不等于功能消失，并把识别漏检、类迁移、跨家族协议消费者、DanmakuPurifyFeatureInstaller 是否仍解析到目标类列为未知，未推测 Hook 覆盖；等级 needs_runtime 与“补证顺序 + 可推翻证据”写法符合证据强度，无过度外推。（E000, E008）
- F011 / revised：核心事实完全由 fresh_refresh 的 E009 支持（2925/44/1318 vs 2958/44/1380、指纹变化、story_kotlin 两侧空集指纹 absent），页面归属 story 正确，未把计数变化误判为新样式或失效，可保留。但草稿用 E011（comment_compose）与 E012（dynamic_compose）的短名混淆类来论证“该类结构计数对改名与重排高度敏感”，属跨页面类推：E009 仅下发家族摘要、无 story 家族自身类样本或方法体哈希，故“裁剪 vs 重排”在 story 证据面内仍是未知，需在正文中显式标注该限制并避免把间接类推当作 story 证据。因此以修订落实，保持 candidate 级别与未知表述。（E009, E000, E011, E012）
- F012 / revised：事实部分与 fresh_refresh 的 E010 一致（mine_account_model 132 类两侧持平、外部调用边 54→43、指纹变化；mine_native 324→328 类、95→91 边、Compose 7→7），页面归属 mine 正确，级别 needs_runtime 与未读源码、未做运行验证的现状相符，故保留。但草稿断言该变化“直接关系到 MineVipFeatureInstaller 与 HostMineReadingCard 所依赖的账号/VIP 信息读取路径”，在模块源码未读（快照 dirty）的情况下属于对 Hook 覆盖的推测，须改为待核；同时应补上 E013 中出现的 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource 这一跨家族线索，说明账号刷新资源并非只由 mine 家族消费，避免把 mine 页当成单一调用面。修订不改页面与证据集，只调整分析、建议与替代解释的确定性表述。（E010, E000, E013）

### 尚未解决的证据缺口

- [1] 模块源码未读：CommentClassicStyleLocator、CommentComposeViewAccess、CommentNativeBindingCatalog、CommentPurifyFeatureInstaller、DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller、KotlinDynamicMossWatch 本轮无 module_source 结果，定位器匹配常量、兜底扫描与 9.16 版本门限仍未知；需按文件哈希补读（source_snapshot 标记 working_tree_dirty）。
[2] comment_kotlin_moss 的 caller 抽样被工具额度拒绝（返回 Read-only tool budget exhausted），评论侧是否存在跨家族消费者仍未取证，不得以 130 定义/26 边推断覆盖缺口。
[3] 类级差分未做：comment_native_legacy +16 类、comment_native_exp3 −2 类、dynamic_compose +180 类、dynamic_legacy +25 类的具体类名与包归属无法取得（APK 访问关闭），指纹变化属混淆改名/DEX 重排/代码迁移的判断未完成。
- [4] dynamic_compose 样本 compose_signatures 全空，说明按 @Composable 签名定位可能整体不可达；需改以字段类型（ComposableLambda/State/MutableState）与调用点定位来判定安装器可达性。
[5] 未登记候选族 dynamic_other:commonCore（E020 中 InteractionServiceImpl 为 dynamic_kotlin_moss 消费者）未纳入静态矩阵，需归族并确认是否影响动态页净化入口。
[6] 未登记协议 OpusMoss/KOpusMoss/CampusMoss/KTribeeMoss/DynamicMoss 的调用者未取证，Opus 卡片数据是否走已登记 KDynamicMoss 之外的服务仍未知。
- [7] 平板/宽屏分支（kntr/app/following/followinglist/ui/wide）的运行时启用条件未验证，宽屏下 Hook 覆盖与布局差异未知。
[8] 服务端 A/B 与实验分组未记录：评论 5 样式与动态 3 路径的实际启用组合静态不可见，不能宣称样式已穷尽。
[9] 全部路径 status 仍为 static_invoke_observed；需真机日志回填 runtime_enabled 与 module_coverage 后才能评估是否适配，本轮不宣称通过。
- [10] 定义数与实调边数单位不同：需按方法名归并 comment/dynamic Kotlin MOSS 签名（含 $default 桥接）后重新统计消费者，避免重复计数。
[11] 复制、净化、回复按钮等具体功能在新增类/包装层下的行为（是否重复注入、是否静默失效）尚无任何运行时证据。
[12] “指纹变化≠新样式”的未变更反证未做：需比对同签名方法体哈希，以排除混淆/重排造成的计数差异。
- [13] home 两家族均缺基线侧类样本对照：本轮 E013/E014 仅目标侧摘录，E013 且在服务端摘录处被截断，无法逐类确认“同名类沿用”，需重读基线 family_evidence 做签名级对齐。
[14] module_source 未读：HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeComponentFilterFeatureInstaller.kt 的匹配常量与兜底路径未提取，home 两条路径的 module_coverage 仍为 requires_installer_review。
[15] ui/main2/* 与 khome/* 的包级类清单差分未做：home_legacy 减少的 235 个类（含匿名/合成类区分）归属未知，无法判定迁移、混淆合并还是裁撤包装层。
- [16] search 模块侧未读：SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt 的解析目标与安装器安装条件未提取，原生/Compose 跨栈覆盖无法判断。
[17] search_compose 家族类样本未深挖，外部调用边 616→594 的下降未定位到具体 Composable，不能排除调用迁移或内联合并。
[18] 未登记协议（app/interfaces/v1 SearchMoss/KSearchMoss、app/search/v2 SearchMoss/KSearchMoss、broadcast/message/search/SearchMoss 等）的跨家族消费者未取证，已登记 MOSS 面“未变”不能推出净化不受影响。
- [19] 两条页面均无真机日志：Hook 安装器命中、定位器命中、失败类名均未采集，runtime_enabled 保持 unknown，本轮不构成适配验收。
[20] 服务端样式开关/A-B 分组未记录：无结构变化的分支静态不可见，不能宣称所有样式已穷尽或已适配。
[21] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），相关模块文件需按文件哈希追溯；本次未核对未提交修改对上述定位器与策略的影响，也未清理工作树。
- [22] pgc_theseus 742→1328 的新增调用边尚无按目标包聚合的分布 diff，也未落到源/目标类，无法区分“解析/重排差异”与“真实新增调用者”（E006）。
[23] pgc_legacy 的 +1 个新增类与 15 条消失边的源/目标未定位，PgcAutoActivityPopupLocator 定位签名是否仍命中未知。
[24] PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupFeatureInstaller.kt、PgcAutoActivityPopupPolicy.kt 未读（快照中存在，工作树 dirty，需按文件哈希追溯），是否存在兜底扫描与版本门限未知。
- [25] DetailModulePurify / DetailUnitedModulePurify / DetailUnitedPresentationPurify / DetailViewPurify 系列 Installer 与 Policy 未读，其解析类名集合未与 detail_theseus_ugc/united 实际类清单比对。
[26] detail_kotlin_moss 10 条实际调用边与 detail_java_moss 35 条实际调用边的消费者类未取证，跨 ugc/united 两个家族的分布与共享数据源未知。
[27] detail_theseus_ugc（1953→1947）与 detail_theseus_united（4602→4579）两侧类名与 method_bodies_sha256 逐类 diff 未做，被删 6/23 个类是否为推荐/广告载体未确认。
- [28] detail_legacy 两侧 absent 未用放宽识别口径（包前缀、基类、字符串常量）复核，属登记键不匹配/漏检还是真实缺失未知；不得据此推断旧原生样式被移除。
[29] 两个页面所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review：真机 ugc/united 与 pgc_legacy/pgc_theseus 入口、安装器安装与命中日志均未采集。
[30] 平板/宽屏分支与服务端 A/B 开关无任何证据，静态不可见不等于该变体未变或已适配。
- [31] prefetch 每家族仅 2 个类样本、每协议 4 个调用者样本，样本不得外推为整套实现；source_snapshot working_tree_dirty=true，模块源码结论须按文件哈希追溯，不清理工作树。
[32] player_java 类 953→957、边 3225→3229 尚未做类级 diff（类名 + method_bodies_sha256），新增 4 类是解析入口、包装/重复层还是混淆拆分仍未知，无法判断倍速/缓冲/画质/片尾推荐等定位器是否失配。
[33] player_java_moss（18 定义/2 实调边）与 player_kotlin_moss（34 定义/3 实调边）未被实调的协议定义消费者清单未取，跨家族消费者是否存在未知。
- [34] 未读 module_source：PlayerSpeedLocator、PlayerBufferLocator、PlayerSpeedSessionLocator、SponsorPlayerLocator/SponsorPlayerAccess、PlayerPopupPromotionLocator 的匹配方式（字符串类名/签名/结构特征）未知，9.16.0 改名后的失配风险无法评估。
[35] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 的定位方式与目标签名本轮未读到源码；source_snapshot 为 working_tree_dirty=true，相关文件未记录文件哈希，无法按哈希追溯。
[36] danmaku_java_moss 20 条实调边与 danmaku_kotlin_moss 4 条实调边的完整调用者清单（所属家族/页面）未取，跨家族协议消费者是否存在未知。
- [37] danmaku_legacy 的 absent 尚未用放宽识别参数（包名前缀、渲染基类如 SurfaceView/View、danmaku 相关字符串常量）复跑，识别漏检与真实缺失不可区分。
[38] player_kotlin 7 个类的类名与 method_bodies_sha256 对照表未产出，仅哈希漂移的推断缺少类级证据。
[39] E007/E008 均限定每家族两个类样本、每协议四调用者样本且 runtime unknown，样本不能代表整套播放器与弹幕实现；本复核会话 fresh_refresh 为空，player/danmaku 的基线-目标重读仍依赖这些有界预取摘录。
- [40] 真机验证未进行：播放器倍速/缓冲/画质/片尾推荐/弹幕净化与屏蔽的 Hook 命中与可见行为差异，以及平板/宽屏与服务端 A/B 变体表现，均保持未知。
[41] 两条路径的 runtime_enabled 与 module_coverage 在安装器层面未给出结论，需在安装器与版本适配契约（VersionAdapterContract/VersionAdapter）中确认 9.16.0 条目。
[42] story_native 与 mine_account_model 的方法体哈希集合差（method_bodies_sha256 对齐）未执行：E009/E010 仅下发家族摘要，无类样本，消失的 62 条 story 边与 11 条 account_model 边对应的源方法全部未知，需在可访问 APK/反编译的环境补齐。
- [43] story 家族类样本未读取：无法判断 33 个类的减少是同哈希改名、合并还是真实删除；草稿的混淆敏感性论证只来自 E011/E012 其他页面样本，属间接类推。
[44] 模块源码正文未读：StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、HomeVerticalDetail*、MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineVipFeatureInstaller、MineComponentSnapshotHostBridge/QueryClient/Store 的定位签名、安装器门限与兜底逻辑均未读到（本轮 module_source 未执行），Hook 覆盖不得推测。
[45] 源码快照 working_tree_dirty=true，需按文件哈希追溯 MineComponentSnapshot 与 StoryActionIconsPolicy 等文件的未提交修改来源，不得清理工作树；当前无法确认模块侧行为是否与 published snapshot 一致。
- [46] 运行期启用未验证：story_native 与 mine 两条路径 runtime_enabled 全为 unknown，需真机（灰度账号）采集安装器安装/命中类名与方法、失败类名与版本判定日志，覆盖登录/未登录两态。
[47] 平板/宽屏分支未验证：story 与 mine 均有宽屏相关候选（如 dynamic/home 家族的 ui/wide、模块 HostMineReadingCard），当前无任何宽屏条件下的 Hook 命中证据。
[48] 服务端开关/A-B 无结构变化时静态不可见：Mine 与 Story 的样式切换条件未取得任何运行条件证据，不得宣称所有样式已穷尽。
- [49] 未登记协议消费者未定位：Lcom/bapis/bilibili/app/story/v1/StoryMoss;、app/mine/v1/MineMoss 与 KMineMoss、account/interfaces/v1/AccountInterfaceV1Moss 与 K 系列在种子中无页面登记，其实际调用方、是否跨家族、是否有共享兜底路径均未知。
[50] story_kotlin 归族口径未定：两侧 absent（0 类、空集指纹）说明静态未检出该家族实现，若真机 Hook 命中 Kotlin 侧类，需修改家族归属而非维持 absent，本轮无法判定。
[51] E013 中 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource 归属 home_legacy 却涉及账号刷新资源，是否为 mine 侧同一模型的跨家族消费者需在 mine 单元单独取证，避免把 mine 页当成单一调用面。
- [52] mine_native 新增的 4 个类未识别：是否属 Mine 组件容器或重复包装层未知，需按方法体哈希比对本轮未做。
[53] 所有路径保持 static_invoke_observed，未取得任何真机日志前不得升级为适配通过；module_coverage 需在安装器与定位器命中证据齐备后重新评估。

## 下一步

- [1] 在 9.16.0 真机（灰度账号）逐一触发 5 种评论样式，采集模块 Hook 命中类名、失败类名与安装器版本判定日志，形成路径级启用证据。
[2] 对 comment_native_legacy 新增类（类数 +16）与 comment_native_next/exp3 类清单做两侧去混淆对照，判断是否为重排还是新绑定层。
[3] 对 dynamic_compose 按 kntr.app.following 前缀比较字段类型与 ComposeLambda 结构，区分混淆改名与新增包装层。
[4] 抓取动态页与 Opus 卡片流量，确认实际服务名是否落在未登记 MOSS 协议（DynamicMoss/KOpusMoss/OpusMoss）内。
- [5] 在平板/宽屏与手机两种形态下分别验证动态 Compose 路径的 Hook 覆盖与宽屏布局分支。
[6] 核对 comment_kotlin_moss（定义 130/边 26）与 dynamic_kotlin_moss（382/26）的未消费声明是否由接口分发吞掉，补最小调用者取证。
[7] 复核模块安装器在 9.16.0 的版本适配契约（VersionAdapterContract）是否有该版本条目，避免仅凭指纹登记判断。
[8] 以上结果回填后统一更新路径 runtime_enabled 与 module_coverage，未验证前保持 static_invoke_observed。
- [9] 重读 module_source：SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt，提取其类名/方法签名常量（本轮被额度拒绝）。
[10] 重读 HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeComponentFilterFeatureInstaller.kt，确认对 khome 与 ui/main2 的定位条件是否依赖被改名的短名类。
[11] 在允许 APK 访问的环境对 9.15.0/9.16.0 做 Ltv/danmaku/bili/ui/main2/* 与 khome/* 包级类清单差分，定位 home_legacy 减少的 235 个类归属。
[12] 提取 HomeFrameViewModel、dispatchAction 参数类型 ap1/b 及 khome/widget/bubble 短名类签名，判断 home_new_frame 变化属改名还是新增。
- [13] 对 search_native 新增 28 个类做归属包标注，确认是否新增可被净化器定位的推荐/默认词组件。
[14] 对 search_compose 减少 22 条外部调用边做定位，确认是否集中于单个 Composable 或内联包装层。
[15] 真机验证：旧版主页、新框架主页、原生搜索页、Compose 搜索页各采集一轮 Hook 安装器与定位器命中日志。
[16] 核对未登记协议 app/interfaces/v1 SearchMoss/KSearchMoss 与 app/search/v2 SearchMoss/KSearchMoss 的跨家族消费者，确认是否存在共享数据源。
- [17] 确认搜索与主页是否存在服务端样式开关（A/B），并记录实验分组，避免把静态不可见误判为未变。
[18] 所有结论保持 static_invoke_observed，不升级为适配通过；补充真机日志后再评估 module_coverage。
[19] 对 pgc_theseus 做两版按调用边目标包的分布 diff，定位 742→1328 的新增边源类与目标类，判定解析差异还是真实新增调用者（E006）。
[20] 对 detail_theseus_ugc/united 两版做逐类名与 method_bodies_sha256 diff，列出被删除类与新增 Compose 方法所属类，确认是否涉及推荐/广告模块载体（E005）。
- [21] 读 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupFeatureInstaller.kt，核对定位签名在 9.16.0 pgc_theseus 中是否仍存在及是否有兜底扫描。
[22] 读 DetailModulePurifyFeatureInstaller.kt / DetailUnitedModulePurifyFeatureInstaller.kt / DetailUnitedPresentationPurifyFeatureInstaller.kt，比对解析类名集合与 detail_theseus_ugc/united 实际类清单。
[23] 确认 detail_kotlin_moss 10 条实际调用边的具体消费者类，判断协议消费者是否跨 ugc/united 两个家族，评估模块入口覆盖面。
[24] 真机验证：同一详情页分别进入 ugc 与 united 入口，采集 Xposed 日志确认 installer 安装与命中，并记录实际渲染家族。
- [25] 真机验证 PGC 详情页：开关 PgcAutoActivityPopupFeature 前后对照自动弹窗与模块列表，记录 pgc_legacy 与 pgc_theseus 实际使用栈。
[26] 检查平板/宽屏与前置服务端开关条件（A/B 无结构变化时静态不可见），记录未覆盖场景为未知而非已适配。
[27] 对两条指纹变化路径补充“未变更”反证：若同签名方法体哈希一致，则结论改记为混淆/重排导致，不登记为新样式。
[28] 两侧 player_java 类级 diff（类名 + method_bodies_sha256），标注 953→957 的新增类并判断是否为包装层或重复层。
- [29] 两侧 player_kotlin 7 个类逐一对照，确认指纹变化是否仅为常量池/方法顺序，排除新样式。
[30] 放宽 danmaku_legacy 识别参数（包名前缀、渲染基类、字符串常量）复跑，判定 absent 是漏检还是真实缺失。
[31] 统计 danmaku_java_moss 20 条实调边与 danmaku_kotlin_moss 4 条实调边的调用者所属家族，确认是否存在跨家族协议消费者。
[32] 核对模块中 PlayerSpeedLocator、PlayerBufferLocator、SponsorPlayerLocator 的匹配方式（字符串类名/签名/结构特征），评估 9.16.0 改名后的失配风险。
- [33] 核对 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 的目标定位方式，并记录其源码文件哈希（source_snapshot 为 working_tree_dirty）。
[34] 真机 9.16.0：打开视频页验证倍速、缓冲、画质、片尾推荐、弹幕净化/屏蔽各功能的 Hook 命中日志与可见行为，并按 9.15.0 做 A/B。
[35] 记录平板/宽屏与服务端开关下的播放器与弹幕表现差异，区分静态不可见的 A/B 变体。
[36] 明确记录每条 path 的 runtime_enabled 与 module_coverage 结果回填，避免以静态观测替代安装器与运行时验证。
- [37] 按方法体哈希对 story_native（2958→2925 类）和 mine_account_model（132 类）做基线-目标集合差，输出丢失方法签名清单，并标注是否与模块候选定位目标相交。
[38] 在 9.16.0 真机以模块调试日志记录 StoryActionIcons、StoryPurify、HomeVerticalDetail 三个 Installer 的实际命中类/方法，判定静态调用是否在运行期启用（当前 runtime_enabled=unknown）。
[39] 真机验证 Mine 页：MineComponentFilter 采集到的组件清单、MineVip 替换结果、HostMineReadingCard 渲染，分别记录已登录/未登录、手机/宽屏两组条件。
[40] 补登记 mine 页与 story 页的协议消费者：MineMoss/KMineMoss/AccountInterfaceV1Moss 与 StoryMoss 的实际调用方，明确是否存在跨家族消费者与兜底路径。
- [41] 定位并记录 story_kotlin 的归族口径：若真机 Hook 命中 Kotlin 侧类，需变更家族归属而非维持 absent。
[42] 在安装器层面确认模块模块清单是否包含 story/mine 候选 Installer，并记录安装成功/失败与版本门限判定。
[43] 复核冻结源码快照的未提交修改（source_dirty=true）对 MineComponentSnapshot 与 StoryActionIconsPolicy 的影响，按文件哈希追溯改动来源，不清理工作树。