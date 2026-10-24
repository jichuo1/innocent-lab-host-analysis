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
| comment_compose | 2428 | 283 | 1101 | static_invoke_observed |
| comment_legacy_v2 | 583 | 0 | 741 | static_invoke_observed |
| comment_native_exp3 | 54 | 0 | 52 | static_invoke_observed |
| comment_native_legacy | 181 | 0 | 220 | static_invoke_observed |
| comment_native_next | 48 | 0 | 67 | static_invoke_observed |
| comment_other_ui:(root) | 225 | 2 | 502 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 215 | 0 | 92 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 241 | 30 | 232 | static_invoke_observed |
| danmaku_kotlin | 137 | 3 | 162 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1975 | 25 | 547 | static_invoke_observed |
| detail_theseus_united | 4633 | 98 | 4199 | static_invoke_observed |
| dynamic_compose | 1187 | 141 | 234 | static_invoke_observed |
| dynamic_legacy | 3255 | 103 | 2075 | static_invoke_observed |
| dynamic_opus | 1350 | 94 | 226 | static_invoke_observed |
| dynamic_other:appointment | 32 | 4 | 18 | static_invoke_observed |
| dynamic_other:card | 426 | 88 | 287 | static_invoke_observed |
| dynamic_other:commonCore | 26 | 0 | 62 | static_invoke_observed |
| dynamic_other:commonPerf | 11 | 1 | 4 | static_invoke_observed |
| dynamic_other:commonUi | 22 | 5 | 7 | static_invoke_observed |
| dynamic_other:lightBrowser | 82 | 19 | 37 | static_invoke_observed |
| dynamic_other_legacy | 2103 | 4 | 2198 | static_invoke_observed |
| home_legacy | 766 | 87 | 198 | static_invoke_observed |
| home_new_frame | 196 | 33 | 52 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 326 | 7 | 94 | static_invoke_observed |
| pgc_legacy | 352 | 0 | 425 | static_invoke_observed |
| pgc_theseus | 2276 | 134 | 1179 | static_invoke_observed |
| player_java | 953 | 0 | 3308 | static_invoke_observed |
| player_kotlin | 455 | 37 | 841 | static_invoke_observed |
| search_compose | 3146 | 562 | 614 | static_invoke_observed |
| search_native | 1705 | 2 | 2818 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2956 | 44 | 1328 | static_invoke_observed |

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
- unregistered_protocol:Lcom/bapis/bilibili/app/listener/v1/KListenerMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/mine/v1/KMineMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/overseas/app/v1/KSplashMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/overseas/ogv/v1/KBangumiMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/playeronline/v1/KPlayerOnlineMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/playerunite/v1/KPlayerMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/resource/v1/KLegacyResourceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/resource/v1/KModuleMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/search/v2/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/childchannel/v1/KKidsChannelMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/mixture/v1/KMixtureMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/mixture/v1/MixtureMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/popular/v1/KPopularMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/rank/v1/KRankMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/story/v1/KStoryMoss;: protocol_signature_or_call_path_changed
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
- unregistered_protocol:Lcom/bapis/bilibili/community/service/cert/v1/KFieldCertMoss;: protocol_signature_or_call_path_changed
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
- unregistered_protocol:Lcom/bapis/bilibili/pgc/gateway/view/v1/KViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/polymer/chronos/v1/KChronosServiceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/polymer/contract/KContractMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/relation/interfaces/KRelationInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/subtitle/KSubtitleMoss;: protocol_signature_or_call_path_changed

## 原生资源变化

{'added': 15, 'removed': 0, 'changed': 7121}

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

本单元审计评论页 5 条、动态页 3 条登记路径，基线 9.16.1→目标 9.17.0（E000、E001、E002）。两页全部 8 条路径均被判为 structure_or_call_path_changed，但证据值只有 static_invoke_observed，runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review，因此没有任何路径可宣称适配通过。深挖复核两条关键假设：评论 Compose 家族样本类落在 kntr.common.comment.common.service 与 kntr.common.comment.richtext，与模块 CommentClassicStyleLocator 的 COMPOSE_ENTRY、CommentModel 判据同包前缀，且模块对 DeviceDecision 布尔读取方法有严格签名验真（E011、E013）；动态 Opus 样本类集中在 kntr.app.following.opusDetail.api，是含外链/广告拦截与快照缓存的独立实现栈，与 DynamicPurifyPolicy 依赖的 AdditionalType 常量、逐段正文回调无同包证据（E012、E014）。结构哈希与计数变化不能直接读作新样式或功能消失，需先排除混淆改名、DEX 重排与代码迁移；源码快照为 dirty worktree（source_tree_sha256 37745f8f…），结论按文件哈希追溯，未读源码的 Hook 覆盖不下结论。

9.17.0(9170100) 相对 9.16.1(9161100) 基线，home 与 search 的四个登记路径全部为 static_invoke_observed，四族指纹均变化，但计数变动幅度很小：home_legacy 767→766 类、边 204→198；home_new_frame 类 196、compose 方法 33 均不变、边 49→52；search_native 1702→1705 类、边 2859→2818；search_compose 3141→3146 类、561→562 compose 方法、边 595→614。search_java_moss 定义 24/边 22、search_kotlin_moss 定义 52/边 18 与基线完全一致，未见协议层结构变化。指纹变化本身不等于新样式，需先排除混淆改名、DEX 重排与代码迁移。本单元未取得 home/search 定位器与安装器源码，安装器覆盖、定位兜底与运行时启用均未知；结论只能是需安装器与真机复核，不能宣称适配通过。

本单元覆盖 detail 三路径（legacy/theseus_ugc/theseus_united）与 pgc 两路径（legacy/theseus）。9.17.0 对 9.16.1：detail_legacy 两侧均为 absent；两个 theseus 家族与两个 pgc 家族全部命中 structure_or_call_path_changed，指纹全变。数值上 detail_theseus_ugc 调用边 510→547、detail_theseus_united 4257→4199（类数反而 +52）、pgc_theseus 782→1179 为本单元最大差异，detail_kotlin_moss 实际调用边 10→38 而定义数仍为 76。四组 MOSS 协议定义数均未变（32/76/12/14），差异集中在消费者与样式侧。模块侧 installer/locator 运行条件未读，全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review、complete_coverage=false。指纹变化不等于新样式，需先排除混淆改名、DEX 重排与服务端开关；本报告不宣称适配通过。

样本 tv.danmaku.bili 9.17.0（9170100，base.apk）对比基线 9.16.1（9161100），仅有冻结静态证据，安装器与运行期状态全部未知。player 两族均观察到静态调用：player_java 953 类/3308 边（基线 958/3222），player_kotlin 455 类/37 Compose 方法/841 边（基线 7/0/100），后者数量级跃迁必须先排除族识别口径、Kotlin 元数据或 DEX 重排，不能直接视为播放器新样式。danmaku_legacy 两版均 absent 且指纹为 sha256('[]')，提示族查询零命中而非弹幕功能消失；danmaku_kotlin 137 类/3 Compose/162 边（基线 57/1/8），danmaku_kotlin_moss 定义 46 不变而消费边 4→10。本单元只提交 player、danmaku 四路径，结论不含通过判定。

本单元仅复核 story（竖屏详情）与 mine（我的）两页在宿主 9.17.0（E000，sha256 f0f880e8…）相对 9.16.1 基线（同源 E000）的静态变化。预取矩阵（E009/E010）显示三条登记路径均仍为 static_invoke_observed，其中 story_native 由 2924 类升到 2956 类（compose_methods 恒为 44、外部调用边 1310→1328），mine_native 由 325 升到 326（边 92→94），mine_account_model 类数与边数完全不变（132/43）但结构指纹改变；story_kotlin 在两侧均为 absent（0 类 0 边）。所有结构哈希变化都不构成“新样式已确认”，仅是可复核的结构差异候选；两侧 protocols 均为空，但未登记协议清单含 Story/KStory/Mine/KMine 等 MOSS，说明本单元没有跨家族消费者证据。全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，因此不得宣称适配通过。模块源码快照工作树 dirty（source_dirty=true），本单元未逐文件读取 HomeVerticalDetail*/Mine* 安装器正文，故 Hook 覆盖保持未知；缺失处一律标注补证任务，不用“稳定/无影响”填补。总判定：installer_and_runtime_validation_required。

## 各页面评估

### comment

评论页五条路径并存：legacy_v2（583 类/741 边）、native_legacy（181/220）、native_next（48/67）、native_exp3（54/52）、compose（2428 类/283 Compose 方法/1101 边）。与基线相比：compose 类 2444→2428、Compose 方法 278→283、边 934→1101，是唯一方法数与边数同升的家族；legacy_v2 仅 +4 类/+6 边；native_next 类 45→48、边 50→67；native_exp3 类 58→54、边 62→52（唯一双降）；native_legacy +9 类/+9 边。全部变化均可由混淆改名、DEX 重排或编译器变化解释，不能判定新增样式或样式下线。协议层 comment_java_moss 两版均 50 定义/50 边；comment_kotlin_moss 定义 130 不变而边 26→23，是评论页唯一协议边下降项，需优先核对消费者是否迁入 Compose 家族。深挖确认 compose 家族样本为 kntr.common.comment.common.service.f/g（带 KReplyInfo 参数方法与 Flow 返回）与 richtext/IconText 等模型类，未见新包前缀；模块 CommentClassicStyleLocator 以 COMPOSE_ENTRY 与 CommentModel 判定 kotlinApplicable，且只接受返回 boolean、参数为 (接口,String,boolean,非基元) 或 (…,int,Object) 的静态 getBool/getBool$default，多 owner 或超过 16 候选直接返回空，落空后才会回退 DexAssistQuery 候选。评论净化、回复按钮、表情与复制桥安装器是否真装上、是否在真机启用均未读到运行条件，保持未知（E001、E011、E013）。

证据：E001, E011, E013

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：583 类/741 边，指纹 b8b891…；基线 579 类/735 边（指纹 8d381d…），小幅同向增长，无 Compose 方法。
- 可能影响：legacy 评论实现的 Hook 落点与调用边可能被重排；模块 legacy 复制/净化桥的目标方法需按签名重新验真，静态存在不证明安装成功。
- 验证：对两版该家族外调边按 owner+描述符做集合差，只保留目标类在基线不存在的边逐条 decompile_class；再用模块 CommentLegacyCopyBridge 的目标方法名在 9.17.0 静态列表中确认存在与签名一致。
- 证据：E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：181 类/220 边（基线 172/211），指纹 86f317…→ 基线 e54284…，类与边同向小幅增长。
- 可能影响：原生 legacy 栈仍有静态痕迹，但增长可能只是辅助类；对 native 绑定目录与补充桥的影响幅度无法由计数判定，缺失项应记作静默降级而非功能消失。
- 验证：逐项列出模块 native 绑定目录期望的类/方法，在 9.17.0 的 181 个类中核对存在性与签名；对不存在的项单独记为待运行期确认。
- 证据：E001

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：48 类/67 边（基线 45/50），类 +6.7% 而边 +34%，指纹 a41887…→ 基线 4a3fda…。
- 可能影响：家族内部耦合度上升；若 Hook 依赖具体调用链而非单点方法，落点可能改变，是否真有新 next 变体未知。
- 验证：取边新增的类 decompile_class 读取调用目标，判断是新增入口还是原有逻辑拆包；并确认模块 matchesKey 收下的 comment.next_appearance 锚点字符串在 9.17.0 仍被读取方引用。
- 证据：E001, E013

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：54 类/52 边（基线 58/62），类与边同时减少，指纹 0b5098…→ 基线 4ef234…，是评论页唯一双降家族。
- 可能影响：可能是实验分支裁剪或代码迁往其它家族，也可能只是混淆合并；若 exp3 由服务端开关开启而静态实现减少，需确认不是模块定位点被移除。
- 验证：先在 9.17.0 中检索 comment.next_appearance_experiment_3 常量与读取方，区分『常量仍在但读取者迁走』与『实验下线』；再在真机用开关分别打开三种外观，观察 CommentClassicStyleLocator 的 NATIVE/KOTLIN reader 数量变化。
- 证据：E001, E013

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：2428 类/283 Compose 方法/1101 边（基线 2444/278/934）；边 +167 而类 -16，指纹 089904…→ 基线 48046c…。
- 可能影响：Compose 复制桥、净化桥、回复按钮、视图访问与表情适配器都以该家族为落点；边增加可能意味排版/组件层级重组，组合函数签名或复用点可能漂移，但类数下降说明不是单纯新增一套实现。
- 验证：按类读取 compose_signatures 与调用边，比对模块 CommentComposeViewAccess/ReplyButtonCompose 期望的组合函数摘要；真机开启 Compose 评论入口后抓安装器日志与 Hook 命中，确认实际安装在哪个组合函数、是否发生回退。
- 证据：E001, E011, E013

### dynamic

动态页三条路径并存：dynamic_legacy（3255 类/103 Compose 方法/2075 边）、dynamic_compose（1187/141/234）、dynamic_opus（1350/94/226）。与基线对比方向不一致：legacy 类 +4 但边 2151→2075（-76）、Compose 方法 105→103；compose 类 1136→1187、Compose 方法 127→141、边 221→234；opus 类 1352→1350、Compose 方法 92→94、边 186→226（+40）。legacy 边下降而 compose/opus 上升，更像代码在家族间迁移或混淆重排，而非单一新样式落地，三者均仍需排除 DEX 重排。协议层 dynamic_java_moss（134/134）与 dynamic_kotlin_moss（382 定义/26 边）两版计数完全一致，未观察到新跨家族消费者或协议边变化。深挖确认 dynamic_opus 样本类集中在 kntr.app.following.opusDetail.api，含 CompositeExternalInterceptor 及其 handleAdClick、firstSnapshotFile 协程体，属 Opus 详情的数据组装、快照缓存与外链/广告点击拦截，是独立实现栈；模块 DynamicPurifyPolicy 依赖宿主 AdditionalType 的 additional_type_goods_VALUE 与 additional_type_up_rcmd_VALUE 常量（读不到时退到 {2,6}）以及逐段正文回调，且 null 一律表示未读到、按保守放行处理，故 Opus 侧是否具备同构信号来源仍未证。动态标签安装器与视频标签偏好的切换条件、平板/宽屏形态、服务端开关均未读到运行条件，记未知（E002、E012、E014）。

证据：E002, E012, E014

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：3255 类/2075 边（基线 3251/2151），类微增而外调边减少 76，Compose 方法 105→103，指纹 494b6f…→ 基线 a02ef6…。
- 可能影响：该家族是动态净化与标签安装器的主要落点；边减少可能代表逻辑内联或迁往 compose/opus，按调用链定位的 Hook 会失配，按类名定位则可能仍可用。
- 验证：对 legacy 做外调边集合差，列出被移除 76 条边的目标类，检查是否包含 DynamicPurifyPolicy 信号来源（正文列表、作者、附加类型）与标签访问点；随后真机执行一条关键词规则并观察卡片是否被删。
- 证据：E002, E014

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：1187 类/141 Compose 方法/234 边（基线 1136/127/221），三项同向上升，指纹 d1bf0f…→ 基线 a43e5e…。
- 可能影响：Compose 动态卡片规模扩大；若净化判定只覆盖 legacy 组合函数，新增组合层可能漏命中，表现为部分卡片无法按关键词/作者规则删除。
- 验证：检索动态净化安装器所 Hook 的组合函数标识在 9.17.0 是否仍存在，并对新增的 14 个 Compose 方法抽样 decompile_class，判断是否引入新的卡片渲染入口（如转发卡、合集卡）。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：1350 类/94 Compose 方法/226 边（基线 1352/92/186），边 +40 而类略降，指纹 600967…→ 基线 70dd32…；样本类位于 kntr.app.following.opusDetail.api。
- 可能影响：Opus 详情栈内部耦合增强，且与净化策略依赖的 AdditionalType 常量、逐段正文回调无同包证据；若 Opus 走独立数据模型，净化与回复入口在该家族可能存在覆盖缺口（未证实）。
- 验证：先定位 9.17.0 中 AdditionalType 枚举类，确认两个 *_VALUE 常量存在且值仍为 2/6；再对 opusDetail.api 下一个正文承载类 decompile_class，确认正文能否经 Signals.textFragments 读取，并在真机对 Opus 卡片逐条记录 shouldRemove 收到的信号是否为 null。
- 证据：E002, E012, E014

### home

home 两条并存栈静态均存在调用边，但相对基线呈现不同形态：home_legacy 类数减 1、外部调用边由 204 降至 198，compose 方法保持 87；home_new_frame 类数与 compose 方法完全不变，调用边由 49 升至 52。前者更像调用点收缩或包装层合并，后者更像在既有 Compose 帧内新增 3 条外调路径，两者都不能直接读作“新样式上线”。home 侧候选源文件包含 HomeFrameListHook、HomeFrameTabLocator、HomeBannerFeatureInstaller、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller、HomeComponentFilterFeatureInstaller、HomeVerticalDetailInstaller/Routing、HostHomeCardSpacingHooks 等多条安装器，但本单元未读取其解析逻辑，因此哪条安装器锚定到变化族、是否有版本兜底、宽屏/平板分支如何选择均未知。seed 未登记 home 协议条目，主页数据面与 UI 面之间的协议消费者无法从登记矩阵确认。source_snapshot 标记 working_tree_dirty，如需追溯必须以文件哈希与 source_tree_sha256=37745f8f… 定位，不得据工作树状态推断覆盖。整体判定：静态调用可见，安装器与运行时启用待验证。

证据：E000, E003

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：fingerprint a56da1e1…（基线 7a842bbb…）；类 767→766、external_invoke_edges 204→198、compose_methods 87 不变。
- 可能影响：若减少的 1 个类与 6 条边落在模块用于定位的类型/方法上，legacy 首页栈的列表与标签过滤类 Hook 可能不再命中；也可能只是混淆改名或包装层合并，功能未变。
- 验证：对 9.17.0 与 9.16.1 分别导出该族类清单做集合差，确认 -1 类是删除、改名还是迁出该族；真机开启模块后按 HomeFrameListHook/HomeTabFilterFeatureInstaller 日志确认 Hook 是否实际命中并对比 9.16.1 行为。
- 证据：E003, E000

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：fingerprint 34c59fa3…（基线 4a3e9002…）；类 196、compose_methods 33 不变，external_invoke_edges 49→52。
- 可能影响：类与方法规模不变而外调边 +3，提示在既有 Compose 帧内多出外部调用点（可能是新数据/工具调用），Compose 侧列表与顶部栏 Hook 的锚点位置可能位移；不构成新家族证据。
- 验证：按 edge 差异定位新增的 3 条调用边所属类，检查是否为已登记 Compose 入口的迁移或重复包装；真机抓该族的安装器日志与 Compose 方法调用计数，确认 33 个 compose 方法中实际被执行的比例。
- 证据：E003, E000

### search

search 两侧家族同时出现小幅结构变化：search_native 类 +3（1702→1705）而外部调用边减少 41（2859→2818）；search_compose 类 +5（3141→3146）、compose 方法 +1（561→562）、调用边 +19（595→614）。两条登记协议 search_java_moss（定义 24、实际调用边 22）与 search_kotlin_moss（定义 52、实际调用边 18）与基线逐项一致，说明协议定义面未变，变化集中在 UI/家族层，而不能反向证明搜索功能面稳定。seed 的未登记协议清单中还列出多套同名语义的搜索 MOSS（app/interfaces/v1/SearchMoss 与 KSearchMoss、app/search/v2/SearchMoss 与 KSearchMoss、broadcast/message/main/SearchMoss、broadcast/message/search/SearchMoss），同一语义存在多个注册名，是否存在跨家族消费者、是否与已登记的 java/kotlin MOSS 指向同一实现，静态矩阵无法判定。候选源文件包括 SearchHomeRecommendLocator、SearchHomeRecommendFeatureInstaller/Policy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner、SettingsSearchMatcher，本单元均未读取，故 MOSS 通道解析点、默认词清洗锚点与推荐净化安装器的覆盖与兜底未知。搜索页还需确认原生与 Compose 并存时的切换条件、服务端开关与宽屏布局，这些在静态视图内不可见。整体判定：静态调用可见，运行时启用待验证。

证据：E000, E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：fingerprint 28e67919…（基线 28a11ecd…）；类 1702→1705、compose_methods 2 不变、external_invoke_edges 2859→2818（-41）。
- 可能影响：类增加而调用边显著减少，可能是调用点被内联/合并或部分路径迁往 Compose 侧；若模块以具体方法描述锚定原生搜索净化点，减少的边可能导致 Hook 落空，也可能只是编译产物重整。
- 验证：对该族做 9.16.1↔9.17.0 方法描述差集，筛出消失的 41 条边所属类并核对是否被 search_compose 侧同类调用替代；真机在原生搜索入口打点，确认 SearchDefaultWordsCleaner 与 SearchPurifyFeatureInstaller 是否实际安装成功。
- 证据：E004, E000

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：fingerprint 4e4c7892…（基线 fcde68da…）；类 3141→3146、compose_methods 561→562、external_invoke_edges 595→614（+19）。
- 可能影响：规模近似线性增长，更像既有 Compose 搜索帧内新增 1 个 compose 方法与若干外调，推荐词/首页推荐净化若挂在具体 composable 上可能因锚点位移而失效；不构成新样式证据。
- 验证：定位新增 compose 方法与 19 条新边所属类，检查是否为 SearchHomeRecommendLocator 目标类型；真机在 Compose 搜索首页验证推荐区域是否被净化，并记录是否被服务端开关切换到另一变体。
- 证据：E004, E000

### detail

detail 三路径并存。detail_legacy 在目标与基线均为 0 类、fingerprint 同为 4f53cda1…，只有 absent 证据，不能据此推断旧原生详情功能消失，也可能是入口迁移或被 theseus 取代。detail_theseus_ugc 类数 1946→1975、compose 方法 25 不变、外部调用边 510→547；detail_theseus_united 类数 4581→4633、compose 方法 99→98、调用边 4257→4199，两者 fingerprint 均变化。协议侧 detail_java_moss 32 定义/35 边两侧一致，detail_kotlin_moss 定义 76 不变但实际调用边 10→38，差异集中在消费者侧而不是协议签名。模块侧存在 DetailModulePurify、DetailUnitedModulePurify、DetailUnitedPresentationPurify、DetailViewPurify、DetailAppPromotion、HomeVerticalDetail 等多套 installer，本轮未读其匹配点、兜底与运行条件；E013 显示同仓定位器采用固定锚点反射 + DEX 语义查询 + 宿主 ClassLoader 验真，安装期不落实验值，因此静态存在不等于 Hook 生效。页面内评论区由独立 compose 家族承载（E011），说明 detail 的净化路径不止 theseus 两栈。

证据：E000, E005, E011, E013

#### 路径：detail_legacy

- 状态：absent
- 变化：目标 9170100 与基线 9161100 均为 0 类、0 调用边、fingerprint 同为 4f53cda18c2b…，仅有 absent 证据，无结构变化可对照。
- 可能影响：若模块仍保留针对旧原生详情栈的 Hook 点，安装后可能无匹配点而只能走兜底；absent 不得读作页面功能消失。
- 验证：在 9.17.0 真机用历史入口/深链尝试进入旧详情栈，抓取 VersionAdapter 安装日志中的 HookPoint 命中与兜底分支，并与 9.16.1 同流程对比。
- 证据：E000, E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类数 1946→1975（+29）、compose 方法 25 不变、外部调用边 510→547（+37），fingerprint 由 67250897… 变为 aba2dbf1…。
- 可能影响：调用边增长提示消费者或调用路径变化，DetailModulePurify 类 Hook 的匹配点可能落空或命中不同重载，实际影响未验证。
- 验证：用 family_evidence 重读该家族类样本，按 method_bodies_sha256 与基线对齐以排除混淆改名/DEX 重排；真机打开 UGC 详情页对比模块开关前后差异并统计安装日志命中数。
- 证据：E000, E005, E013

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类数 4581→4633（+52）、compose 方法 99→98（-1）、外部调用边 4257→4199（-58），fingerprint 由 b0f0b041… 变为 56c25b77…。
- 可能影响：类增而 compose 与调用边同时减少，更像模块拆分/迁移或编译器产物变化而非新样式；DetailUnitedPresentationPurify 依赖的呈现层入口是否仍存在未知。
- 验证：重读 united 家族类样本比对方法体哈希与 compose 签名集合；核对 DetailUnitedPresentationPurify 呈现层 Hook 点真机命中情况，并检查平板/宽屏是否走同一栈。
- 证据：E000, E005

### pgc

pgc 两个登记路径在目标与基线均存在静态调用。pgc_legacy 类数 354→352、外部调用边 399→425、fingerprint 由 2c5cf1a4… 变为 60c8869e…；pgc_theseus 类数 2265→2276、compose 方法 131→134、外部调用边 782→1179（+397），是本单元增幅最大的家族。协议侧 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）在两侧完全一致，说明协议签名未变，差异落在消费者与样式侧。类数微增而调用边大幅增加，可能是 theseus 整合把更多调用方纳入该家族，也可能是新增样式候选，指纹变化同样可能来自混淆改名或 DEX 重排，需用类样本方法体哈希区分。模块侧本单元只登记 PgcAutoActivityPopupLocator/FeatureInstaller/Policy 三个文件，本轮未读到其锚点、兜底以及与 legacy/theseus 双栈的对应关系，源码快照 worktree 为 dirty，无法据此推断 Hook 覆盖。宽屏/平板布局、服务端 A/B 开关与自动弹窗类型均静态不可见，两个路径的 runtime_enabled 与 module_coverage 未闭合。

证据：E000, E006, E014

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类数 354→352（-2）、外部调用边 399→425（+26）、fingerprint 由 2c5cf1a4… 变为 60c8869e…。
- 可能影响：类数微降而调用边增加，可能是重复包装层合并或调用方重组；PgcAutoActivityPopup 相关 Hook 是否仍落在 legacy 栈未知。
- 验证：重读 legacy 类样本确认减少的 2 类是被合并还是移除，并在真机以旧入口打开 PGC 详情页观察自动活动弹窗拦截与净化是否生效，采集安装器命中日志。
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类数 2265→2276（+11）、compose 方法 131→134（+3）、外部调用边 782→1179（+397），fingerprint 由 4df56dbb… 变为 44b6f779…；pgc_player_moss 与 pgc_view_moss 的定义数与调用边两侧不变。
- 可能影响：调用边大幅扩张而协议不变，可能是 theseus 整合纳入更多消费者或存在未归类的新样式候选；模块 PGC 定位器对两栈的覆盖未证实，兜底行为未知。
- 验证：按类样本方法体哈希与 compose 签名比对基线；真机打开 PGC 播放页/详情页验证 PgcAutoActivityPopup 拦截与页面净化，并读取定位器诊断日志确认锚点解析结果；对服务端开关做 A/B 抓包确认是否切换家族。
- 证据：E000, E006, E014

### player

player 登记两条路径都只到 static_invoke_observed，runtime_enabled 与 module_coverage 均为 unknown，requires_installer_review（E007）。player_java：958→953 类（-5）、外部调用边 3222→3308（+86）、指纹 2830ee…→f35508…；类数几乎持平而边数上升，更符合 DEX 重排、混淆改名或内部调用重组，而非整族被替换，但模块 PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerPopupPromotionAdapter 等按类名+参数描述符定位，改名会导致静默失配且无安装失败提示（E000 仅给出源码文件清单，player 相关文件内容未读，不能推断 Hook 覆盖）。player_kotlin：7 类/0 Compose/100 边跃迁到 455 类/37 Compose/841 边，是本页最大结构变化；player_java 仅减少 5 类，无法解释 448 类增量，因此候选解释是族选择器口径或 Kotlin/Compose 元数据识别变化，其次是播放器 UI 真实迁移到 Kotlin + Compose 或 DEX 重新分包。两种解释对模块影响相反：若为真实迁移，播放器 Compose 表层需要 Compose 感知锚点；若为口径变化，实际可 Hook 面不变。当前不具备任何一侧真机安装日志、平板/宽屏分支或服务端开关证据，两路径均不得判为适配通过。

证据：E000, E007, E013

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：953 类/3308 边，基线 958 类/3222 边，指纹由 2830ee… 变为 f35508…；类数同量级（-5）、边数 +86，候选为 DEX 重排、混淆改名或调用重组，未确认为新样式。
- 可能影响：Player 缓冲、倍速、清晰度、码率、弹窗推广等定位器依赖类名与参数描述符；若为改名型变化，安装点会静默回退或失配，模块覆盖 requires_installer_review。
- 验证：对两版 base.apk 的 player 包做类名归一化后的方法签名 diff（不使用结构哈希做等价判断）；采安装器日志确认 PlayerSpeedLocator/PlayerBufferLocator 各安装点命中或回退；真机验证倍速切换、缓冲上限、清晰度强制与竖屏/宽屏分支。
- 证据：E000, E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：455 类/37 Compose 方法/841 边，基线仅 7 类/0 Compose/100 边；数量级跃迁，Compose 从 0 到 37，候选为播放器 UI 迁入 Kotlin+Compose，或族选择器口径、编译器与 Kotlin 元数据识别变化。
- 可能影响：若为真实迁移，播放器 Compose 表层 Hook 需 Compose 感知锚点，原 Kotlin 家族定位常量可能只覆盖少量类；若为归档口径变化，则模块可见面不增不减。两类结论决定是否需要为新族补定位器和兜底。
- 验证：导出目标族 455 类与 37 个 Compose 签名，与基线 player_java/其他族同名同类交叉比对，判断是迁移还是重新归档；再用 E013 所示定位器方式（DEX 语义查询 + 安装期 ClassLoader 验真）核对真实性；最后真机看安装日志与 Compose 端页面 Hook 是否生效。
- 证据：E007, E013

### danmaku

danmaku 两条登记路径结论分裂，且都不含运行期证据（E008）。danmaku_legacy 在目标与基线两侧都是 absent，类数 0、边 0，指纹 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 正是 sha256("[]")，即该族查询在两版都返回空集合；这既可能意味着原生弹幕实现在 9.16.1 之前就已不在该族选择器范围，也可能是族定义/包名匹配缺口，或相关类落在本次未纳入的安装分包，不能据此认定原生弹幕功能消失。danmaku_kotlin 从 57 类/1 Compose/8 边升到 137 类/3 Compose/162 边，danmaku_kotlin_moss 定义数 46 两版不变而消费边 4→10，说明新增调用点集中在既有协议接口而非新接口；未登记协议清单中还列有 Lcom/bapis/bilibili/live/approom/api/grpc/v1/KDanmuMoss、Lcom/bapis/bilibili/app/playerunite/v1/KPlayerMoss 等，是否存在跨家族消费者需要人工确认。DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy 仅在源码清单中被列出，内容未读，无法推断净化 Hook 是否覆盖新增调用点与 Compose 弹幕层。运行期启用、平板/宽屏布局和服务端开关均未知。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线两侧均 absent（0 类/0 边，指纹 4f53cd…=sha256("[]")），为空集摘要在版本间未变化，属于查询/登记口径问题而非本次版本引入的样式变化。
- 可能影响：原生弹幕路径没有静态调用证据，DanmakuPurify 若仍保留 legacy 分支则无覆盖依据；同时也不能反推该路径已被移除，功能状态为未知。
- 验证：在 base.apk 全部 DEX 中检索 danmaku/danmu 包、弹幕渲染自绘 View 与列表适配类，核对族选择器匹配规则；确认其他 split/动态加载模块是否承载这些类；真机打开原生弹幕样式页观察净化是否生效并对比安装日志。
- 证据：E000, E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：137 类/3 Compose 方法/162 边，基线 57 类/1 Compose/8 边；danmaku_kotlin_moss 定义数 46 未变而实际消费边 4→10，新增集中在既有协议接口的调用方。
- 可能影响：协议读取点增多意味着 DanmakuPurify 的拦截锚点周边出现新的合法消费者，若安装器只覆盖旧锚点，净化可能对新增链路无效；KDanmuMoss 等未登记协议是跨家族候选，当前未归类。
- 验证：读取 DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 的实际定位常量与兜底顺序，与目标族 137 类清单及消费边所在类比对；真机开关净化，记录安装日志命中项、弹幕列表差异以及直播/视频两类弹幕入口表现。
- 证据：E008, E000

### story

已知：story_native 在目标侧 2956 类、44 个 compose 方法、1328 条外部调用边，指纹 dafc7376…；基线 2924 类、44 个 compose 方法、1310 条外部调用边，指纹 b56b7342…（E009）。变化量 +32 类、+18 边，而 compose 方法数严格不变，属于“家族内新增少量类/边”的结构刷新候选，尚不能判定为新的竖屏详情样式；也可能只是混淆改名、DEX 重排或编译器产物差异（E009 limitations）。story_kotlin 在目标与基线两侧均为 absent（0 类 0 边、指纹 4f53cda1…），说明该命名下未观察到 Kotlin 家族实现；absent 不等于竖屏详情的 Kotlin/Compose 承载消失，也不能反推宿主只走原生栈——本单元未读到任何能区分“未归类命名”的调用边，故并存栈与切换条件未知。两侧 protocols 为空，本单元未取得 StoryMoss/KStoryMoss 的跨家族消费者证据；竖屏详情到评论区、动态/Opus 家族的跳转只能作为待验证假设（E011、E012 分别是 comment_compose 2428 类与 dynamic_opus 1350 类家族，均不属于本单元登记路径，不能作为 story 路径的覆盖证据）。模块侧相关源码文件为 HomeVerticalDetailFeatureInstaller/HomeVerticalDetailRouting、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess，本单元未读取正文，安装期定位与兜底策略保持未知。module_coverage=requires_installer_review，runtime_enabled=unknown。

证据：E000, E009, E011, E012

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：目标 2956 类 / 44 compose 方法 / 1328 外部调用边（指纹 dafc7376…），基线 2924 类 / 44 / 1310（指纹 b56b7342…）：类 +32、边 +18，compose 方法数不变。
- 可能影响：若新增类落在竖屏详情的分发或卡片渲染链上，按类名/描述符定位的 Hook 点可能失配；compose 方法数不变则不支持“整页改为 Compose 新样式”的推断。未知：安装器是否覆盖新增类。
- 验证：以 module_source 读 HomeVerticalDetailFeatureInstaller.kt 与 HomeVerticalDetailRouting.kt，列出其 HookPoint 描述符；再用 decompile_class 对目标与基线逐一核对同名描述符是否存在，并记录安装期 DEX 定位诊断（如 dex.assist 类诊断键）命中/未命中日志。
- 证据：E000, E009

#### 路径：story_kotlin

- 状态：absent
- 变化：目标与基线两侧均为 0 类、0 compose 方法、0 外部调用边，指纹同为 4f53cda1…，相比基线无变化。
- 可能影响：该登记名未观察到任何类，模块针对此路径的 Kotlin 侧 Hook 无静态目标；无法据 absent 推断竖屏详情 Kotlin/Compose 实现不存在，混淆改名或迁入未归类家族同样会表现为 absent。
- 验证：用 family_evidence 以 story 相关家族名与 kntr 前缀枚举目标侧类集，检索竖屏详情入口（含 Compose 入口）候选；对候选入口 decompile_class 读调用边，确认是否由未登记家族承载，并记录为空的确切查询键。
- 证据：E009

### mine

已知：mine_native 目标 326 类 / 7 个 compose 方法 / 94 条外部调用边（指纹 f6b18de5…），基线 325 / 7 / 92（指纹 75f16dab…），即 +1 类、+2 边、compose 方法数不变（E010）。mine_account_model 在两侧类数 132、compose 方法 0、外部调用边 43 完全相同，但指纹由 2b548e1a… 变为 db7f2792…；在“单位计数未变而哈希改变”的情形下，最保守解释是类名/成员重命名、DEX 重排或重编译，超出类/方法/边这三个计数的字段类型变化同样无法被计数反映，因此不能据此认定账号模型出现新样式。变化可能落在 MineComponent 组件过滤（MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineComponentSnapshotStore/QueryContract/HostBridge）与 MineVipFeatureInstaller、HostMineReadingCard 的数据读取面上，但这些文件本单元未读正文，字段级与解析点级影响保持未知。两侧 protocols 均为空，未登记协议清单含 MineMoss/KMineMoss 与 relation/interfaces，本单元未取得“我的页经 MOSS 协议跨家族消费”的调用边证据，也就不能判断服务端开关或宽屏/平板变体是否被静态覆盖。module_coverage=requires_installer_review，runtime_enabled=unknown。

证据：E000, E010

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：目标 326 类 / 7 compose 方法 / 94 外部调用边（指纹 f6b18de5…），基线 325 / 7 / 92（指纹 75f16dab…）：类 +1、边 +2，compose 方法数不变。
- 可能影响：新增类或边若位于“我的”页组件装配/卡片构建路径上，按描述符定位的 Hook 点可能失配或退化为兜底路径；具体是否影响组件过滤与阅读卡片仍未知，因安装器正文未读。
- 验证：用 module_source 读 MineComponentFilterFeatureInstaller.kt 与 MineComponentSnapshot.kt，提取其依赖的宿主类与方法描述符；再用 decompile_class 在目标与基线间比对同名描述符的方法体哈希，并对新增类读调用边确认是否进入“我的”页装配链；同时核对安装器诊断日志的 hint 命中情况。
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数 132、compose 方法 0、外部调用边 43 在目标与基线完全一致，但指纹由 2b548e1a… 变为 db7f2792…，属计数不变的结构哈希改变。
- 可能影响：成员名或类型层面可能被混淆/重编，字段级读取（账号信息、VIP 状态、组件快照）可能因字段名变化而读空；也可能仅为哈希噪声，对模块无实际影响——两者静态无法区分。
- 验证：对 mine_account_model 抽样类在目标与基线分别 decompile_class，逐字段比对名称与类型并记录差异；用 module_source 读 MineVipFeatureInstaller.kt 与 MineComponentSnapshotQueryContract.kt 确认其字段名/描述符来源是硬编码还是反射查找，若为反射则核对查找失败时的兜底路径与日志。
- 证据：E010

### F001：评论 Compose 家族调用边 +167 而类数 -16：需区分组件重组、代码迁入与样式新增
事实：comment_compose 由基线 2444 类/278 Compose 方法/934 边变为 2428 类/283 方法/1101 边（E001/E015），边增而类减。深挖样本仅 5 个类（E011 自述有界摘录）：kntr.common.comment.common.service.f（含收 KReplyInfo 的方法，另有接收 KReplyInfo+long+model、两 long+model 的变体）与 g（4 个返回 kotlinx.coroutines.flow.Flow 的方法、一个返回 boolean），以及 kntr.common.comment.richtext 的 g$a、i、IconText；在该摘录范围内未见新包前缀，但样本量不足以代表 2428 类，不能据此下『无新样式』结论。模块侧 CommentClassicStyleLocator（E017 全文）：kotlinApplicable 由 COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment 或 kntr.common.comment.card.model.comment.CommentModel 判定；KOTLIN 家族只承认静态、返回 boolean、参数数为 4 或 6 且 p0 为接口、p1 String、p2 boolean、p3 非基元（6 参数时 p4 int、p5 Object）的 getBool/getBool$default，并要求 6 参数 wrapper 与 4 参数 reader 同声明类且前四参一致（isDefaultDelegate）；多 owner 视为歧义直接返回空，resolve 侧缓存点 >16 返回空，select 侧候选 >32 返回空。locate 的降级链为 direct → （enabled 时）DexAssist 候选 → 与缓存 merge，因此签名改写不会导致崩溃，最坏是静默返回空集或旧缓存点。推断（未证）：边数上升更可能来自既有类内部调用重构或逻辑自其它家族迁入，而非新增独立评论样式；此点静态不可判定。
反例与替代解释：若边差中绝大多数目标类在两版同名同签名存在，则『组件层级重组』与『新样式』同时被削弱，降级为结构噪声；若真机 Hook 日志显示 Compose 复制/净化桥仍有命中，则『复用点漂移』被推翻；若 locate 返回空集但 DexAssist 候选命中且功能正常，则 direct 路径失效但不影响功能；若样本外的类出现新包前缀，则『无新样式』被推翻。
建议：先做集合差：把两版 1101/934 条外调边按 owner+描述符对齐，只保留目标类在基线不存在的边，逐条 decompile_class 判定新入口还是重排；再真机打印 dex.assist.comment_classic 诊断值，确认 NATIVE/KOTLIN 两个 reader 列表在 9.17.0 是否非空、是否只靠 DexAssist 候选或缓存 merge 命中，并核对 COMPOSE_ENTRY 与 CommentModel 两个类仍可加载。
证据：E001, E011, E015, E017

### F002：动态 Opus 家族边数 +40：抽样落在 opus 详情 API 栈，与净化信号来源的关系未证
事实：dynamic_opus 由 1352 类/92 Compose 方法/186 边变为 1350/94/226（E002/E016），边 +40 而类略降；dynamic_legacy 反向（类 +4、边 2151→2075），compose 三项同升，三族方向不一致更像家族间迁移或混淆重排。深挖样本（E012）限于 kntr.app.following.opusDetail.api：A（构造收 ImmutableSet）、B（List+Function1→Map）、C（String/String/boolean 值对象）、CompositeExternalInterceptor$firstSnapshotFile$1、$handleAdClick$1，语义是 opus 详情侧请求参数组装、快照缓存与外链/广告点击拦截，属详情栈而非信息流卡片渲染点，且远少于 1350 类。策略侧（E018 全文）：shouldRemove 依序判定 promotion→lockedChargeOnly→author→逐段 textFragments 关键词→semanticBlocked；promotion 优先读宿主 AdditionalType 的 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE，读不到才用兜底 {2,6}；null 表示本次未读到并保守放行。因此即使常量缺失也只是退到兜底集合，风险在类型编号漂移而非直接失效。推断（未证）：Opus 侧是否复用动态卡片的附加类型与正文模型无同包/引用证据，净化和回复入口在该家族是否存在覆盖缺口仍未知；也反向可能成立——opus 详情本就不在动态净化安装范围，属设计未覆盖而非版本回归。
反例与替代解释：若 Opus 卡片复用同一动态卡片模型（引用同一 AdditionalType 并暴露同构正文列表），『Opus 缺净化覆盖』被推翻，仅剩边数增长属内部重构；若真机日志显示信号非 null 且规则命中，同样推翻；若净化安装器本就不面向 Opus 家族，应改判为设计未覆盖而非版本回归；若三类计数差异在同名同签名下消失，则视为 DEX 重排噪声。
建议：两条最小补证：(1) 在 9.17.0 定位宿主 AdditionalType 类，确认两个 *_VALUE 常量存在且数值仍为 2/6，若漂移需同步兜底集合；(2) 先确认动态净化安装器实际安装在哪些家族与 HookPoint，再对 opusDetail.api 之外的 Opus 卡片承载类 decompile_class，确认正文能否经 Signals.textFragments 读取；真机对 Opus 卡片分别启用关键词与推广规则，记录 shouldRemove 收到的各信号是否为 null。
证据：E002, E012, E016, E018

### F003：comment_kotlin_moss 实际调用边 26→23：3 条边的归属与运行时影响未证
事实：comment_kotlin_moss 两版定义数均 130，实际调用边 26→23（E001/E015）；comment_java_moss 维持 50/50；对照组 dynamic_kotlin_moss 382 定义/26 边、dynamic_java_moss 134/134 两版完全一致（E002/E016）。同时 comment_compose 外调边 934→1101。以上只能说明协议边计数与 Compose 家族计数各有一处变动，不能证明二者之间存在迁移关系。E017 中的 isDefaultDelegate 校验只针对宿主 IDeviceDecisionKt 的 getBool/getBool$default，说明模块对委托签名有严格验真，但与 MOSS 通道无关，不能用来解释协议边下降。本轮未取得 comment_kotlin_moss 两侧调用方清单（深挖工具额度在复核阶段已耗尽），因此消失的 3 条边属消费者下线、重载合并、内联还是静态图召回缺失均未知；KotlinMossChannel/KotlinMossReplyBridge 的兜底分支是否被走到也未读到运行条件。
反例与替代解释：若消失的 3 条边同属一个类的重复重载，则『消费者迁移』被推翻，属编译产物差异；若真机两条通道均命中且行为一致，可排除功能影响；若调用方类两版均存在而边不在静态图中，则更可能是静态图召回缺失而非真实调用变化。
建议：用 protocol_evidence 取 comment_kotlin_moss 两侧调用方样本，列出消失的 3 条边的宿主调用方类，检查是否迁入 comment_compose 家族或转为 Java MOSS；随后真机分别触发 Java MOSS 与 Kotlin MOSS 两条回复通道，统计模块通道 Hook 命中次数，并补齐安装器覆盖与运行时启用两项未知。
证据：E001, E002, E015, E017

### F004：home_new_frame 类与方法规模不变、外调边 +3：家族未扩张，但不排除样式变体或目标改名导致的边重分组
事实（E003）：home_new_frame 目标侧 classes=196、compose_methods=33、external_invoke_edges=52，基线为 196/33/49，fingerprint 由 4a3e9002… 变为 34c59fa3…；home_legacy 目标侧 766/87/198，基线 767/87/204。推断：两族类集与方法集规模基本冻结（legacy -1 类、new_frame 0），不符合“新增样式族”的规模特征，更像既有帧内的调用点增删或元素移位。反例与替代解释：外调边若按外部目标类名分组统计，目标类改名/合并/拆分或包装层增删都可使边数变化而不产生新调用；混淆改名、DEX 重排同样能改指纹而计数不变；同一帧内的服务端/设备开关变体也可能在类与方法规模不变的情况下改变实际渲染，不能因计数不变就断言样式未变。未知：E003 预取仅每族两个类样本，-1 类、-6/+3 边的具体所属类未知；模块 HomeFrameTabLocator/HomeFrameListHook 等源码本单元未读，Hook 锚点是否命中这些类不可推测。
反例与替代解释：若归一化后 +3 边全部落在未被任何安装器引用的类上，本项应降为构建噪声；若发现族切分规则把相邻族类移入 home_new_frame（类集规模变化被族边界吸收），则“家族未扩张”被推翻，应转为家族切分/迁移问题；若真机执行集合与 9.16.1 一致而仅数据通道变化，则维持调用路径增量；若真机出现与 9.16.1 不同的布局而类集未变，则应记为服务端/设备开关控制的样式变体，而非新家族。
建议：1) 用同参数 family_evidence 重读 home_legacy/home_new_frame 目标与基线，先按外部目标类名归一化后做边集合差，再区分“真实新增调用”与“改名/重分组”，输出 -1 类与 ±边清单；2) module_source 读取 HomeFrameTabLocator.kt 与 HomeFrameListHook.kt，核对锚点常量是否落在变动类上及是否有兜底分支；3) 真机 9.17.0 采集该族安装器日志与 33 个 compose 方法的执行集合，与 9.16.1 对照确认是否仅是数据通道变化。
证据：E003, E000

### F005：search 两族计数小幅变化而协议仅计数持平：不能据此断定协议结构未变，多套 SearchMoss 注册名未归类
事实（E004）：目标侧 search_native 1705 类/2 compose 方法/2818 外调边（基线 1702/2/2859），search_compose 3146/562/614（基线 3141/561/595），两族 fingerprint 均变化；协议 search_java_moss 定义 24、实际调用边 22，search_kotlin_moss 定义 52、实际调用边 18，两版本逐项相同。推断：协议层在计数维度没有增删迹象，变化集中在两族的类/方法/边计数上；原生 -41 边与 Compose +19 边的幅度不对称，与“部分调用点迁移”相容，但同样与内联/合并、按目标类分组重命名相容，静态计数无法区分。未知：预取只给每族两个类样本（E004 limits），消失/新增边所属类未知；协议无 fingerprint 与签名差集，不能断言协议结构未变；定义数与调用边数单位不同，禁止相除推导覆盖率。E000 的未登记清单含 app/interfaces/v1/SearchMoss|KSearchMoss、app/search/v2/SearchMoss|KSearchMoss、broadcast/message/main/SearchMoss、broadcast/message/search/SearchMoss 等多套同语义注册名，是否与已登记两条 MOSS 指向同一实现、是否存在模块未覆盖的跨家族消费者，均无证据。search 侧候选源文件（SearchHomeRecommendLocator、SearchHomeRecommendFeatureInstaller/Policy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner）本单元未读取，解析点与兜底未知。
反例与替代解释：若差集显示 41 条消失边在 Compose 侧无对应且原生化路径仍在别处被调用，则“迁移”被推翻，应改为两栈并行扩张；若多套 SearchMoss 注册名解析到同一 Impl，则未归类消费者风险可排除；若协议调用方清单显示存在模块未注册的消费类，则登记缺口确认；若服务端开关使某栈在真机从不加载，则静态并列的两族不代表双上线，计数差不应读作功能变化。
建议：1) 用 protocol_evidence 对 search_java_moss / search_kotlin_moss 取完整调用方列表与方法描述，并与 app/interfaces/v1、app/search/v2、broadcast/message 下同名 SearchMoss 注册名比对是否为同一实现；2) 对 search_native 做目标-基线方法描述差集，定位消失的 41 条边所属类，检查是否在 search_compose 的 +19 边中重现（迁移）还是另有承载；3) module_source 读取 SearchHomeRecommendLocator.kt、SearchHomeRecommendFeatureInstaller.kt、SearchPurifyFeatureInstaller.kt、SearchDefaultWordsCleaner.kt，登记锚点常量与失败兜底；4) 真机分别经原生与 Compose 搜索入口触发检索，记录实际命中协议与清洗点，并观察服务端开关是否切换变体。
证据：E004, E000

### F006：静态矩阵无法判定 home/search 实际启用栈；DeviceDecision 键切换并存栈的机制目前只在评论定位器取证，home/search 属待验推断
事实：home_legacy/home_new_frame 与 search_native/search_compose 在目标侧全部为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E003、E004），所以“静态存在调用边”既不证明某栈在真机被选中，也不证明模块在该栈装配成功。另行取证（E013，sha256 2ec67116…）：评论定位器 CommentClassicStyleLocator 以 NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision、KOTLIN_OWNER=kntr.base.dd.IDeviceDecisionKt 与入口 NATIVE_ENTRY=com.bilibili.app.comment3.CommentV3Fragment、COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment 区分旧原生与 Compose 栈，并对缓存的 HookPoint 用当前宿主 ClassLoader 反射验真、失败走 DexAssist 语义查询；这只证明评论族按决策键切换并存栈。推断与边界：把同一模式外推到 home/search 属未验证推断——本单元未读取 HomeFrameTabLocator、HomeFrameListHook、SearchHomeRecommendLocator、SearchHomeRecommendFeatureInstaller 任一源码，无法确认其是否读取同类决策键、常量名在 9.17.0 是否仍存在、以及读取失败后是否有兜底；E011（comment_compose）与 E012（dynamic_opus）只描述评论与动态族，不作为 home/search 结构证据。另：源码快照为 dirty worktree（source_tree_sha256 37745f8f…），追溯须以单文件哈希为准，不得据工作树状态推断覆盖率。
反例与替代解释：若四份定位器源码已包含 9.17.0 的新决策键或新增兜底，则“需真机判定启用栈”的紧迫性下降；若真机显示两版本决策键取值相同且只加载 Compose 栈，则 home_legacy 的边数变化属未启用路径，不应读作功能风险；若两栈均加载而模块只在一栈装配，则确认覆盖缺口；若定位器实际不依赖 DeviceDecision 而按类名/包名硬匹配，则本推断被推翻，应改为类名/描述符匹配脆弱性问题。
建议：1) 按 source_tree_sha256=37745f8f… 与单文件 sha256 记录，读取 HomeFrameTabLocator.kt、HomeFrameListHook.kt、SearchHomeRecommendLocator.kt、SearchHomeRecommendFeatureInstaller.kt，逐条登记决策键常量、入口类型判据与读取失败兜底，核对常量名在 9.17.0 宿主中是否存在；2) 真机分别进入旧原生首页、Compose 首页、原生搜索、Compose 搜索，抓安装器日志：装配成功/失败原因、HookPoint 命中次数、DeviceDecision 语义键取值；3) 对未命中路径记录是否回退到语义 DEX 查询及其结果键，区分“未启用路径”与“覆盖缺口”。
证据：E013, E000, E003, E004

### F007：detail 两 theseus 家族指纹与调用边同步变化、detail_kotlin_moss 调用边 10→38，须先排除 DEX 重排再谈新样式
事实：9.17.0 相对 9.16.1，detail_theseus_ugc 由 1946 类/25 compose/510 边变为 1975/25/547，detail_theseus_united 由 4581/99/4257 变为 4633/98/4199，两者 fingerprint 均变化（E000、E005）；协议侧 detail_java_moss 定义 32、边 35 两侧完全一致，detail_kotlin_moss 定义 76 不变而实际调用边 10→38，差异落在消费者侧而非协议签名（E005）；detail_legacy 两侧 0 类，属 absent 而非删除证据（E005）。united 类增而 compose 方法与调用边同时减少，更像模块拆分/迁移或编译器产物变化。推断（需补证）：E011 的 comment_compose 家族（2428 类/283 compose 方法/1101 边）含以 KReplyInfo 为参数的方法 d，说明评论存在独立 Compose 承载且共同协议有跨家族消费者，但该家族是否由 detail 页实际启用未取得证据；E013 显示同仓 CommentClassicStyleLocator 以 NATIVE_OWNER com.bilibili.lib.dd.DeviceDecision、COMPOSE_ENTRY kntr.common.comment.entry.CommentSectionComposeFragment 等固定名作锚点，安装期仅反射、语义 DEX 查询由 VersionAdapter 后台调度，缓存 HookPoint 复用前用宿主 ClassLoader 验真，说明静态存在锚点不等于 Hook 生效；草稿所称 CommentModel 判据未出现在已读摘录中，属未知。detail 侧各 installer（DetailModulePurify/DetailUnitedModulePurify/DetailUnitedPresentationPurify/DetailViewPurify）的匹配点、兜底与运行条件本轮均未读取，因此这些计数变化既可能是调用方扩张，也可能是混淆改名、DEX 重排或重复包装层，本项保持 needs_runtime。
反例与替代解释：若类样本方法体哈希与基线一致而仅类名/顺序变化，则混淆改名或 DEX 重排解释成立，应撤销“新样式/新路径”判断；若 installer 全文显示锚点为固定类名且该类在 9.17.0 已改名，则属定位器失配而非样式新增；若真机安装日志显示全部 HookPoint 命中，则调用边增长的适配风险下调；若 detail_kotlin_moss 边增长仅来自同方法体多入口的包装类，应视为结构噪声；若 comment_compose 家族在 detail 页无调用边，则评论区路径判断需另证。
建议：先做静态对齐：用 family_evidence 重读 theseus_ugc/united 类样本，按 method_bodies_sha256 与方法签名集合与基线逐类比对，区分“仅改名/重排”与“方法体变化”；对 detail_kotlin_moss 新增 28 条调用边做调用方聚类，判断是否仅为 bridge/包装类增生；再读 DetailModulePurify/DetailUnitedModulePurify/DetailUnitedPresentationPurify/DetailViewPurify 四个 installer 全文登记锚点与兜底，并在 9.17.0 真机采集 HookPoint 命中数与 dex.assist.comment_classic 诊断输出，最后用 UGC 与 united 两种详情入口对比开关前后表现。
证据：E000, E005, E011, E013

### F008：pgc_theseus 调用边 782→1179 而 pgc 协议两侧不变，PgcAutoActivityPopup 定位器对双栈覆盖仍未知
事实：pgc_theseus 由 2265 类/131 compose/782 边变为 2276/134/1179（+11 类、+3 compose、+397 边），fingerprint 44b6f779… 与基线 4df56dbb… 不同；pgc_legacy 由 354 类/399 边变为 352/425，fingerprint 60c8869e… 与基线 2c5cf1a4… 不同；而 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧完全相同（E000、E006）。推断：协议层未变而消费者侧边数大幅扩张，可能是 theseus 整合把更多调用方纳入同一家族，也可能是新增样式候选；legacy 类数微降同时边数上升，更像包装层合并或调用方重组。模块侧本轮只登记 PgcAutoActivityPopupLocator/FeatureInstaller/Policy 三个文件，未读到其锚点类名、匹配点数量与兜底分支，source_snapshot 的 worktree 为 dirty（按文件哈希追溯），因此无法判断它覆盖 legacy 还是 theseus 栈。类比参考：同仓 DynamicPurifyPolicy 采用“读不到即保守放行、只有明确命中才删除”的纯判定层（E014），若 pgc 策略同构，则锚点失配会表现为静默不处理而非崩溃，真机现象容易被误读为“已适配”。
反例与替代解释：若 pgc_theseus 类样本仅类名/顺序变化而方法体哈希不变，则 DEX 重排解释成立，可排除新样式候选；若定位器锚点在 9.17.0 中已不存在或匹配数为 0，则问题属定位器失配而非新增页面栈；若真机在 legacy 与 theseus 入口均观察到拦截生效，则“覆盖未知”可收敛为已观测但未穷尽；若 legacy 减少的 2 类确认是被合并进 theseus 家族，则不属于功能消失。
建议：读 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupPolicy.kt、PgcAutoActivityPopupFeatureInstaller.kt 全文，记录锚点类名/方法签名、匹配点数与兜底；对 pgc_theseus 类样本做方法体哈希比对，判定 +397 边是消费者新增还是重排；真机分别从 PGC 播放页与详情页入口验证自动活动弹窗拦截与净化，并抓取服务端开关差异确认是否切换家族。
证据：E000, E006, E014

### F009：player_kotlin 从 7 类跃迁到 455 类，先排除族归档口径变化再谈播放器新样式
事实：E007 显示 player_kotlin 由基线 7 类/0 Compose 方法/100 条外部调用边变为 455 类/37 Compose 方法/841 边，同期 player_java 由 958 类/3222 边变为 953 类/3308 边。推断：仅凭 player_java 减少 5 类不足以解释 player_kotlin 的 448 类增量，至少需并列考察族选择器口径调整、Kotlin 元数据/编译器版本差异、DEX 重新分包与真实代码迁移四种解释；结构哈希与计数变化本身不能证明新样式，也不能证明功能消失。模块机制旁证：同仓库评论页定位器 CommentClassicStyleLocator（E013，属评论页而非 player 家族，仅作机制类比）采用语义 DEX 查询候选 + 安装期宿主 ClassLoader 反射验真、缓存方法描述、验真失败即不安装，说明按类名与参数描述符定位的安装点在本版本改名/迁移时可能静默回退；该源码不能证明任何 player 定位器的实际匹配结果，也不能证明 Hook 生效。缺口：PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerPopupPromotionAdapter、PlayerEndPageRecommendLocator 等 player 侧源码内容未读（E000 仅为文件清单，工作树 dirty，按文件哈希追溯），播放器 Compose 层覆盖未知；类数、定义数、调用边数单位不同，禁止相除推导覆盖率；运行期启用状态全部 unknown。
反例与替代解释：若按基线样本以同一族口径重跑后 player_kotlin 仍为数十类级别，则跃迁应判为真实代码迁移或新样式，而非口径问题；若增量类在基线 player_java 或其他族中存在同名同类，则更可能是归档口径变化，模块覆盖不变；若这些类实际位于本次未纳入分析的 split/动态模块，则计数受采样范围限制，结论作废需重采。
建议：第一步对两版 base.apk 取 player_kotlin 全类名与方法签名做归一化 diff，明确增量类是新增、改名还是从其他族迁入；第二步用组件化定位日志（同类 E013 的 DEX 语义查询 + 安装期验真）确认每个播放器安装点在目标版本命中还是回退；第三步真机回归倍速、缓冲上限、清晰度/码率强制、弹窗推广过滤与横竖屏切换，并记录 Compose 内播放器页面是否与原生页表现不同。
证据：E007, E013, E000

### F010：danmaku_legacy 两版均为空集摘要，弹幕净化缺原生路径静态依据
事实：E008 中 danmaku_legacy 目标侧与基线侧都是 absent，类数 0、边 0，指纹 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945，即空 JSON 数组的 sha256，说明该族查询在两个版本都零命中，不存在“新样式替代旧样式”的结构变化证据；同页 danmaku_kotlin 由 57 类/8 边增至 137 类/162 边，danmaku_kotlin_moss 消费边由 4 增至 10（定义数 46 不变），新增主要落在既有接口的调用方。推断：DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 若仍以原生弹幕类为锚点，则当前静态证据无法证明其有安装点；未登记协议清单中的 KDanmuMoss、KPlayerMoss 等提示弹幕/播放业务存在跨家族消费者，需人工归类。缺口：净化相关源码内容未读（E000 仅文件清单，工作树 dirty），族选择器规则、分包范围与运行时启用均未知，absent 不等于页面功能消失。
反例与替代解释：若在全部 DEX 或其它 split 中检索到原生弹幕渲染类，则 absent 仅由族选择器口径造成，需先修登记范围；若净化功能在真机对原生样式页确实生效，则说明模块用了未登记锚点，本发现降级为登记缺口；若污染文本主要经服务端开关下发且两版结构无差异，则静态不可见，需以抓包+真机对照替代。
建议：先核对 danmaku_legacy 的族选择器规则与包名模式，在 base.apk 全部 DEX 中检索弹幕渲染相关类确认是否零命中属于口径缺口；再读 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 的定位常量与兜底顺序，与 danmaku_kotlin 的 137 类及 10 条 MOSS 消费边逐一对齐；真机开启净化，分别在视频弹幕、直播弹幕与宽屏/平板布局下记录安装日志命中项和弹幕差异。
证据：E008, E000

### F011：story_native 家族类/边增长但 compose 方法数不变：结构刷新候选，不足以确认新竖屏详情样式
事实：story_native 目标 2956 类 / 44 compose 方法 / 1328 外部调用边，基线 2924 / 44 / 1310（E009），增量 +32 类、+18 边、compose 方法数 0 变化；两侧 story_kotlin 均 absent（0/0/0，指纹 4f53cda1…）。推断：若宿主把竖屏详情迁移到新 Compose 承载，最直接信号应是 compose 方法数增长，而此处不变，因此“新增类”更可能来自业务类扩充、混淆命名变化或 DEX 重排而非新样式。限定：本单元未读到任何 story 家族类的调用边明细，故新增类是否进入详情渲染/分发链未知；未登记协议清单中存在 StoryMoss/KStoryMoss，但本单元两侧 protocols 为空，无跨家族消费者证据。相邻家族 comment_compose（2428 类 / 283 compose 方法，E011）与 dynamic_opus（1350 类 / 94 compose 方法，E012）只说明宿主存在其他承载栈，不能作为 story 路径的覆盖或排除依据。模块侧 HomeVerticalDetail*、StoryActionIcons*、StoryPurify*、PlayerStoryFreeDataPromotionAccess 文件本单元未读正文，Hook 覆盖与兜底一律未知。
反例与替代解释：以下证据可推翻本推断：① 若对目标侧新增 32 类 decompile 后发现其中含 Compose 入口或与竖屏详情路由直接相接的调用边，则“仅结构刷新”不成立，应升级为新承载候选；② 若基线同样存在这些类、仅类名不同（逐个描述符可比对），则差异只是混淆改名；③ 若安装器诊断日志显示 HomeVerticalDetailFeatureInstaller 在目标上 Hook 点全部命中且行为一致，则“影响 Hook 点位”可被削弱；④ 若 story_kotlin 的 absent 是查询键命名不匹配造成，而非宿主真无 Kotlin 家族，则并列栈结论需重写。
建议：最小补证：先 module_source 读 HomeVerticalDetailFeatureInstaller.kt / HomeVerticalDetailRouting.kt 取 HookPoint 描述符清单，再对目标与基线逐一 decompile_class 校验存在性与方法体哈希；同时用 family_evidence 对 story 家族取样新增类并读其调用边。真机侧在 9.17.0 打开竖屏详情，抓安装期 hint/定位诊断与 Hook 命中日志。
证据：E009, E011, E012

### F012：mine_account_model 计数零变化但指纹改变：优先按混淆/重编解释，字段级读取风险待真机验证
事实：mine_account_model 在目标与基线均为 132 类 / 0 compose 方法 / 43 外部调用边，指纹由 2b548e1a… 变为 db7f2792…（E010）；同页 mine_native 由 325 类 / 7 compose 方法 / 92 外部调用边（75f16dab…）变为 326 / 7 / 94（f6b18de5…），compose 方法数不变。推断：在类数、compose 方法数、外部调用边数三项单位全部不变的前提下，哈希改变最可能来自成员重命名、DEX 顺序重排或重编译；但这三项计数天然看不见字段名与字段类型变化，账号模型字段级读取（VIP 状态、组件快照字段）仍可能因重命名而静默读空，反之也可能只是哈希噪声——静态不可区分。限定：本单元未读取 MineVipFeatureInstaller.kt、MineComponentSnapshot.kt、MineComponentSnapshotQueryContract.kt、HostMineReadingCard.kt 正文，无法判断模块是按硬编码描述符还是反射按名查找，也无法判断查找失败是否被保守兜底掩盖成“无数据”；E010 的 limits 声明每族两类样本，但载荷实际只给出族汇总、无类字段明细，故本单元不存在可复核的“我的”页字段级证据。E013（CommentClassicStyleLocator.kt，sha256 2ec67116…）与 E014（DynamicPurifyPolicy.kt，sha256 e76741e1…）均属评论/动态路径，只能作为模块内“反射验真 + 读失败一律保守放行 + 宿主常量读不到即用兜底集合”模式的参照（E014 明示读取失败保守放行、兜底集合 2/6），不构成“我的”页的覆盖或排除证据。两侧 protocols 为空，未登记协议清单中的 MineMoss/KMineMoss、relation/interfaces 消费者与跨家族共用路径未知；服务端 A/B 与宽屏/平板变体在无结构变化时静态不可见。
反例与替代解释：可推翻当前推断的证据：① 若抽样类在目标与基线 decompile 后字段名与类型完全一致、仅文件内顺序不同，则指纹变化可判为重排噪声，风险降级；② 若“我的”页解析点全部按硬编码描述符且目标侧同名描述符方法体哈希一致，则“字段读空”推断不成立；③ 若真机日志显示组件快照与 VIP 状态读取成功且与 9.16.1 行为一致，影响面可缩至 mine_native 新增 1 类的局部；④ 反向情况：若安装器在目标上静默回落到兜底常量且无诊断输出，则说明存在被掩盖的读失败，需升级为具体缺陷；⑤ 若确认 MineMoss/KMineMoss 存在跨家族消费者，则“我的”页并列栈与切换条件需重写，本发现的范围也随之扩大。
建议：最小补证：① module_source 读 MineVipFeatureInstaller.kt 与 MineComponentSnapshotQueryContract.kt，判定字段名/描述符来源是硬编码还是反射按名查找，并登记查找失败时的兜底分支与诊断输出；② 对 mine_account_model 抽样 3–5 个类在目标与基线成对 decompile_class，逐字段比对名称/类型与方法体哈希，解释 db7f2792… 与 2b548e1a… 的差异来源；③ 对 mine_native 新增 1 类与新增 2 条边读调用边，判断是否进入“我的”页组件装配链；④ 真机 9.17.0 进入“我的”页，覆盖未登录/已登录/VIP 三态，比对组件过滤与阅读卡片结果，并保留安装器 hint/定位诊断日志以区分“读失败放行”与“规则命中”；⑤ 按单文件哈希记录本轮所读源码（dirty worktree，source_tree_sha256 37745f8f…），不改动工作树。
证据：E010, E013, E014

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
复核结论与 E015 重新取证一致：五条登记路径全部为 static_invoke_observed，runtime_enabled 全 unknown，module_coverage 全 requires_installer_review，无一条可写通过或已适配。计数（目标/基线）：comment_legacy_v2 583 类/741 边（579/735，指纹 b8b891…/8d381d…）；comment_native_legacy 181/220（172/211）；comment_native_next 48/67（45/50）；comment_native_exp3 54/52（58/62，唯一双降）；comment_compose 2428 类/283 Compose 方法/1101 边（2444/278/934）。协议侧 comment_java_moss 两版均 50 定义/50 边；comment_kotlin_moss 定义 130 不变、边 26→23。深挖 E011 只给出 5 个类样本且明示为有界摘录，落在 kntr.common.comment.common.service（f 带 KReplyInfo 参数方法、g 返回 Flow）与 kntr.common.comment.richtext（g$a、i、IconText），不足以代表 2428 类全集，也不能据此断言『无新包前缀』。E017 全文读定位器：kotlinApplicable 由 COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment 或 kntr.common.comment.card.model.comment.CommentModel 判定；NATIVE 走 com.bilibili.lib.dd.DeviceDecision 的 getBoolean（非静态，参数 2..8，p0 String、p1 boolean）；KOTLIN 只收静态 getBool/getBool$default，参数数为 4 或 6 且 p0 接口、p1 String、p2 boolean、p3 非基元；多 owner 视为歧义返回空，resolve 侧缓存点超 16 返回空、select 侧候选超 32 返回空；direct 为空才用 DexAssist 候选（受 enabled 开关），最终与缓存 merge。因此签名漂移只会静默降级为空/缓存值，不会崩溃，模块侧表现需真机日志判定。各路径的安装器是否装上、五种外观各自的读取者数量、平板/宽屏与服务端开关均未读到运行条件，保持未知。
证据：E015, E001, E011, E017

### 复核页面：dynamic
复核结论与 E016 重新取证一致：三条登记路径全部 static_invoke_observed，runtime_enabled 全 unknown，module_coverage 全 requires_installer_review。计数（目标/基线）：dynamic_legacy 3255 类/103 Compose 方法/2075 边（3251/105/2151），类微增而边 -76；dynamic_compose 1187/141/234（1136/127/221），三项同升；dynamic_opus 1350/94/226（1352/92/186），类略降而边 +40。协议侧 dynamic_java_moss 134 定义/134 边、dynamic_kotlin_moss 382 定义/26 边，两版完全一致，未见协议层新增跨家族消费者。指纹全部变化，但不能读作新样式。E012 样本限于 kntr.app.following.opusDetail.api 的 A（构造收 ImmutableSet）、B（List+Function1→Map）、C（三字段值对象）与 CompositeExternalInterceptor$firstSnapshotFile$1、$handleAdClick$1，语义上属 opus 详情侧的数据组装、快照缓存与外链/广告点击拦截；这是详情栈，不能直接等同动态信息流卡片的正文与附加类型读取点，且样本量远小于 1350 类。E018 全文读 DynamicPurifyPolicy：shouldRemove 顺序为 promotion→lockedChargeOnly→author 规则→逐段 textFragments 关键词→semanticBlocked；promotion 优先读宿主 AdditionalType 的 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE，读不到退兜底 {2,6}；null 一律表示本次未读到并按保守放行处理。故 Opus 家族是否具备同构信号来源、是否存在净化漏命中均未证实。动态标签安装器与视频标签偏好的切换条件、平板/宽屏形态、服务端 A/B 均未读到运行条件，保持未知。
证据：E016, E002, E012, E018

### 复核页面：home
home 两族目标侧证据值均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E003，E000）。计数据族级汇总：home_legacy 766 类/87 compose 方法/198 外调边（基线 767/87/204），home_new_frame 196/33/52（基线 196/33/49），两族指纹均变化。变化幅度极小、类与方法集合规模未扩张，但这只是计数事实：预取视图明确只给每族两个类样本、每协议四个调用方样本（E003 limits），因此 -1 类、-6 边与 +3 边具体落在哪些类/方法未知；若外调边按目标类分组统计，目标改名或包装层合并/拆分会改变边数而不产生新调用，混淆与 DEX 重排同样能改指纹，均未排除。seed 未为 home 登记任何协议，而 E000 的未登记清单含 app/home/v1/HomeMoss、KHomeMoss、feed/v1/KFeedMoss、broadcast/message/main/NativePageMoss 等，主页数据面消费者无法从登记矩阵确认，无法判断 UI 变化是否存在跨家族协议消费者。候选源文件列有 HomeFrameTabLocator、HomeFrameListHook、HomeBannerFeatureInstaller、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller、HomeComponentFilterFeatureInstaller、HomeVerticalDetailRouting、HostHomeCardSpacingHooks 等，本单元一条都未读取，锚点常量、失败兜底、平板/宽屏分支与服务端开关选择全部未知；E013 是评论定位器源码，只能说明评论族存在决策键切换模式，不能充当 home 证据。结论限于静态调用可见，需安装器与真机复核，不得写作适配通过；两条路径状态逐字沿用静态矩阵的 static_invoke_observed。
证据：E000, E003

### 复核页面：search
search 两族目标侧同为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E004，E000）。search_native 1705 类/2 compose 方法/2818 外调边（基线 1702/2/2859），search_compose 3146 类/562 compose 方法/614 边（基线 3141/561/595），两族指纹均变化；协议条目 search_java_moss（定义 24、实际调用边 22）与 search_kotlin_moss（52/18）在两版本逐项持平，但预取只给出 definitions 与 actual_invoke_edges 两个计数，没有协议指纹或方法签名差集，因此只能说计数层面持平，不能据此断言协议结构未变，也不能用定义数去除边数推覆盖率（单位不同）。原生侧 -41 边与 Compose 侧 +19 边幅度不对称，既可能是调用内联/合并或部分路径迁移，也可能是按目标类分组的边因改名重分组，静态计数无法区分；预取仅每族两个类样本（E004 limits），消失/新增边所属类未知。E000 未登记清单列出多套同语义注册名（app/interfaces/v1/SearchMoss 与 KSearchMoss、app/search/v2/SearchMoss 与 KSearchMoss、broadcast/message/main/SearchMoss、broadcast/message/search/SearchMoss），它们与已登记两条 MOSS 是否同一实现、是否存在未覆盖消费者未知。候选源文件 SearchHomeRecommendLocator、SearchHomeRecommendFeatureInstaller/Policy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner、SettingsSearchMatcher 本单元均未读取，解析点与兜底未知；两栈切换条件、宽屏布局与服务端 A/B 静态不可见。结论：静态调用可见，需安装器与真机复核，status 保持 static_invoke_observed。
证据：E000, E004

### 复核页面：detail
已用 fresh_refresh 的 E005 复核草稿数字，全部一致：detail_legacy 在 9.17.0 与 9.16.1 均为 0 类/0 compose/0 边且 fingerprint 同为 4f53cda1…，证据值只能是 absent；detail_theseus_ugc 1946→1975 类、compose 25 不变、边 510→547，fingerprint 67250897…→aba2dbf1…；detail_theseus_united 4581→4633 类、compose 99→98、边 4257→4199，fingerprint b0f0b041…→56c25b77…。两 theseus 路径证据值均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，草稿没有把它们写成适配通过，状态用词正确。协议侧 E005 证实 detail_java_moss 32 定义/35 边两侧一致，detail_kotlin_moss 定义 76 不变而调用边 10→38，差异位于消费者侧而非协议签名，可作为“先排除重排/改名再谈新样式”的依据。需要修正的两处推断边界：其一，E011 采样属 comment_compose 家族（类名 kntr.common.comment.common.service、richtext，方法 d 以 KReplyInfo 为参数），只能证明评论存在独立 Compose 承载与共同协议跨家族消费者，并未证明 detail 页实际走该家族；其二，E013 摘录只显示 CommentClassicStyleLocator 的 DIAGNOSTIC/NATIVE_OWNER/KOTLIN_OWNER/COMPOSE_ENTRY 常量与“安装期仅反射、语义 DEX 查询后台调度、缓存 HookPoint 用宿主 ClassLoader 验真”，未显示草稿所述的 CommentModel 判据，该点应降为未知。detail 多套 installer（ModulePurify/UnitedModulePurify/UnitedPresentationPurify/ViewPurify/AppPromotion/HomeVerticalDetail）的锚点、兜底与运行条件均无本轮证据，Hook 覆盖不可下结论；宽屏/平板分支与服务端样式开关静态不可见。
证据：E000, E005, E011, E013

### 复核页面：pgc
E006 已重新取证并支持草稿全部计数：pgc_legacy 354→352 类、compose 0、边 399→425，fingerprint 2c5cf1a4…→60c8869e…；pgc_theseus 2265→2276 类、compose 131→134、边 782→1179（+397），fingerprint 4df56dbb…→44b6f779…；pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）在两侧完全相同。两路径证据值均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，草稿未把计数变化写成新样式或适配通过，状态用词符合静态矩阵。草稿对“协议不变、差异落在消费者与样式侧”的判断与 E006 一致；对 legacy 类微降而边上升给出的“包装层合并/调用方重组”属候选解释，草稿已标明需靠方法体哈希区分，未被当作结论。需要标注的边界：PgcAutoActivityPopupLocator/Policy/FeatureInstaller 仅出现在候选文件清单，本轮无任何读取证据，因此锚点、匹配点数、legacy/theseus 双栈对应关系与兜底分支均为未知；E014 是 DynamicPurifyPolicy（动态页判定层），“读不到即保守放行”只能作为类比，不能外推到 PGC 策略。服务端 A/B、平板/宽屏布局与自动弹窗类型静态不可见；+397 条边也可能来自 DEX 重排或重复包装层，需边集合差与 decompile 交叉确认。
证据：E000, E006, E014

### 复核页面：player
E007 复核：目标侧 player_java 953 类/3308 条外部调用边（基线 958/3222，指纹 2830ee…→f35508…），player_kotlin 455 类/37 Compose 方法/841 边（基线 7/0/100）。两条登记路径 evidence 均为 static_invoke_observed，runtime_enabled 与 module_coverage 全为 unknown / requires_installer_review，本页没有任何可宣称适配通过的证据。player_java 类数几乎持平（-5）而边数上升（+86），更符合 DEX 重排、混淆改名或调用重组；player_kotlin 属数量级跃迁，需同时考虑真实迁移、族选择器口径调整与 Kotlin 元数据识别变化，且 player_java 仅减少 5 类不足以解释 448 类增量。两类解释对模块影响相反，不能读作“播放器迁入 Compose 新样式”。模块源码层面本页仅读到评论页定位器 CommentClassicStyleLocator（E013，属评论页，仅作按名定位+安装期验真机制的旁证），PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerPopupPromotionAdapter、PlayerEndPageRecommendLocator 等内容未读（E000 只是文件清单，工作树 dirty），安装点命中/回退、平板宽屏分支与服务端开关均未知。定义数、类数与调用边数单位不同，不得相除推导覆盖率。结论：需安装器与真机复核。
证据：E007, E013, E000

### 复核页面：danmaku
E008 复核：danmaku_legacy 目标与基线两侧均 absent（0 类/0 边，指纹 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 即空数组的 sha256），属查询口径层面的空集，既不能读作原生弹幕功能消失，也不能反推其已被新样式替代。danmaku_kotlin 由 57 类/1 Compose 方法/8 边升至 137 类/3 Compose 方法/162 边；danmaku_java_moss 两侧均为 22 定义/20 边不变，danmaku_kotlin_moss 定义数 46 两侧不变而实际消费边 4→10，新增集中在既有协议接口的调用方而非新接口。两条路径 evidence 分别为 absent 与 static_invoke_observed，runtime_enabled 均 unknown，module_coverage 均 requires_installer_review。DanmakuPurifyFeatureInstaller / DanmakuPurifyPolicy 全文未读（E000 仅文件清单），净化锚点是否覆盖新增消费边、是否含 legacy 分支、失败兜底顺序均未知；未登记协议清单中的 KDanmuMoss、KPlayerMoss、KPlayerOnlineMoss 等跨家族消费者尚未归类。结论：需族选择器核对、源码核对与真机（视频/直播/宽屏）验证，absent 不等于功能消失。
证据：E008, E000

### 复核页面：story
复核结论：草稿对本页两条登记路径的定性与静态矩阵一致——story_native 为 static_invoke_observed，story_kotlin 为 absent，未出现被改写成“已适配/通过”的越界。数值可回溯 E009 双侧汇总：story_native 目标 2956 类 / 44 compose 方法 / 1328 外部调用边（dafc7376…），基线 2924 / 44 / 1310（b56b7342…），即 +32 类、+18 边、compose 方法数不变；story_kotlin 两侧 0/0/0、指纹同为 4f53cda1…，确为双侧一致的空族。因此“家族内结构刷新候选、不足以认定新竖屏详情样式”的表述在证据上成立，且摘要把增量与“新增样式”区分的做法正确。需明确保留的限制：E009 的 limits 声明每族两类样本，但载荷中实际只给出族汇总、没有类样本明细，故本单元没有任何 story 类的方法体哈希或调用边可读，新增 32 类是否位于详情分发/卡片渲染链完全未知；模块侧 HomeVerticalDetailFeatureInstaller/HomeVerticalDetailRouting、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess 均未读正文，安装期锚点、定位兜底与运行期启用一律未知（runtime_enabled=unknown、module_coverage=requires_installer_review）。两侧 protocols 为空，而未登记协议清单中存在 StoryMoss/KStoryMoss，其宿主消费者与是否存在跨家族共用路径未取证。E011（comment_compose 2428 类 / 283 compose 方法）与 E012（dynamic_opus 1350 类 / 94 compose 方法）属其他登记页家族，草稿仅将其作为“宿主存在其他承载栈”的边界说明、未当作 story 覆盖证据，这一处理可接受；但引用他们对本页结论无增量，不得据此推断竖屏详情的并列栈已穷尽。服务端 A/B 与宽屏变体在无结构变化时静态不可见。
证据：E000, E009, E011, E012

### 复核页面：mine
复核结论：mine_native 与 mine_account_model 两条路径的状态值与静态矩阵严格一致（均为 static_invoke_observed），未被提升为通过或“已适配”。数值可回溯 E010：mine_native 目标 326 类 / 7 compose 方法 / 94 外部调用边（f6b18de5…），基线 325 / 7 / 92（75f16dab…），即 +1 类、+2 边、compose 方法数不变；mine_account_model 两侧 132 类 / 0 compose 方法 / 43 外部调用边完全相同，但指纹由 2b548e1a… 变为 db7f2792…，属“单位计数不变而哈希改变”。草稿把后者保守解释为重命名/DEX 重排/重编译，并同时指出类数、compose 方法数、调用边数三项单位看不见字段名与字段类型变化，这一双面表述正确，未把哈希变化误判为新样式或功能消失。需保留的限制：E010 的 limits 同样声明每族两类样本，但载荷只有族汇总，本单元没有任何 mine 类字段清单可读，字段级“是否读空”纯属待验证风险；MineComponentFilterFeatureInstaller、MineComponentSnapshot(Store/QueryContract/HostBridge)、MineVipFeatureInstaller、HostMineReadingCard 均未读正文，无法区分模块是按硬编码描述符还是反射按名查找，也无法判断查找失败是否被保守兜底掩盖。两侧 protocols 为空，未登记协议清单含 MineMoss/KMineMoss 与 relation/interfaces，跨家族消费者与“我的”页是否存在 Kotlin/Compose 并列栈未取证。E013（CommentClassicStyleLocator.kt）与 E014（DynamicPurifyPolicy.kt）属评论/动态路径，只能作为“反射验真 + 读失败保守放行”的模块内模式参照，不构成本页覆盖证据，草稿对这点已作说明但引用位置需收紧（已在 F012 修订中处理）。runtime_enabled 全为 unknown、module_coverage 全为 requires_installer_review，服务端开关与宽屏/平板变体静态不可见。
证据：E000, E010, E013, E014

- F001 / revised：计数事实由 E001/E015 支持，定位器细节经 E017 全文重读基本准确，故保留该候选方向；但有三处需收紧：(1) E011 明示为有界摘录（仅 5 个类样本），『未见新包前缀』只能限定在样本内，不能外推到 2428 类；(2) 候选阈值表述不精确：resolve 侧缓存点 >16 返回空、select 侧候选 >32 才返回空，fromJson 也限制 16，不是统一『超 16 直接返回空』；(3) 『direct 与 resolve 同时落空即定位失败』不完整，locate 在 direct 为空时还会走 DexAssist 候选（受 enabled 开关）并与缓存 merge，只有三者皆空才为空集，且空集表现为静默降级而非崩溃。（E001, E011, E015, E017）
- F002 / revised：计数与样本事实由 E002/E016、E012 支持，策略判据由 E018 全文确认，候选方向成立；但草稿标题与正文『实现独立于净化策略所依赖的宿主枚举与正文信号』是超证据断言：E012 样本明确位于 opusDetail.api 详情侧，不等于动态信息流卡片渲染点；且策略对 AdditionalType 常量有 {2,6} 兜底，常量缺失只会退化为兜底数值而非直接失效，需要改写因果表述与结论强度。（E002, E012, E016, E018）
- F003 / revised：边 26→23、定义 130 不变的事实由 E001/E015 支持，且该差异确为评论页唯一协议边下降项，保留为待运行期校准项；但草稿把 isDefaultDelegate（E017，针对宿主 DeviceDecision 的 getBool 委托）当作解释 MOSS 通道边形态的『说明』，属跨机制类比，不能作为证据；同时本轮复核未能取得 comment_kotlin_moss 两侧调用方样本（工具额度已尽），消失的 3 条边归属仍未知，需在报告中明写。（E001, E002, E015, E017）
- F004 / revised：计数与指纹事实与 E003 一致（196/33/52 对 196/33/49），但草稿把结论写成“判定为调用路径增量而非新家族”，并把 +3 边解释为“既有 Compose 帧内新增外调”，两处都超出证据：预取仅给每族两个类样本，无法定位这 3 条边所属类；外调边按外部目标类分组时，目标改名、包装层合并/拆分都会改变边数而不产生新调用，该替代解释草稿未列。修订为“家族规模未扩张”并补齐该替代解释与归一化比对步骤，级别保持 needs_runtime。（E003, E000）
- F005 / revised：E004 支持两族计数变化（1705/2/2818、3146/562/614 对 1702/2/2859、3141/561/595）与协议两项计数持平（24/22、52/18），也支持 E000 的多套 SearchMoss 注册名。但草稿的“协议定义面未变/说明协议层结构不变”属过度外推：证据只有 definitions 与 actual_invoke_edges 两个计数，无协议指纹或签名差集；引号内“部分调用点从原生迁往 Compose”的相容性判断也未被边清单支持。修订为仅表述计数持平，并保留迁移假设为待验，级别保持 candidate。（E004, E000）
- F006 / revised：E013 确证评论定位器以 com.bilibili.lib.dd.DeviceDecision / kntr.base.dd.IDeviceDecisionKt 与 CommentV3Fragment / CommentSectionComposeFragment 作为并存栈判别，并在当前宿主 ClassLoader 下验真缓存 HookPoint；E003/E004 确证 home/search 全部路径 runtime_enabled=unknown。但草稿标题直接写成“宿主样式族由设备决策键与入口 Fragment 常量切换”，把评论族机制当作 home/search 的事实，且 E011/E012 属评论/动态族，不能支撑 home/search。修订为：矩阵“不足以判定启用栈”这一谨慎结论保留，决策键机制明确标注为仅评论族已取证、home/search 属待验推断；级别保持 needs_runtime。（E013, E000, E003, E004）
- F007 / revised：计数与协议侧差异全部经 E005 复核无误（ugc 1946→1975 类/25 compose/510→547 边；united 4581→4633/99→98/4257→4199；java_moss 32 定义 35 边两侧一致；kotlin_moss 76 定义、边 10→38），needs_runtime 定级恰当，排除混淆改名/DEX 重排的方法建议也具体。但原 analysis 把 E011 的 comment_compose 家族直接说成“detail 页评论区由独立 compose 家族承载”，E011 只证明该家族存在且存在以 KReplyInfo 为参数的方法（共同协议跨家族消费者），未证明其由 detail 页启用；同时 E013 摘录只含 DIAGNOSTIC/NATIVE_OWNER/KOTLIN_OWNER/COMPOSE_ENTRY 常量与 ClassLoader 验真、后台语义 DEX 查询说明，未出现“CommentModel 判据”，该描述缺证据。故以 revision 收窄这两处断言并补一条最小补证任务，保留原证据编号与页面归属。（E000, E005, E011, E013）
- F008 / retained：E006 复核显示 pgc_theseus 2265→2276 类、compose 131→134、边 782→1179（+397），pgc_legacy 354→352 类、边 399→425，两 fingerprint 均变，而 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧完全一致，草稿引用无误。草稿没有把 +397 条边说成新样式，明确标注为“theseus 整合纳入更多消费者”或“样式候选”，并把 PgcAutoActivityPopup 三文件全文未读、锚点与双栈覆盖未知、dirty worktree 按文件哈希追溯写为限制，alternatives 已覆盖 DEX 重排、定位器失配与 legacy 类合并三种反解释；E014 仅被用作同仓判定层保守放行的类比而非 PGC 结论。candidate 定级与证据强度匹配，无需改动。（E000, E006, E014）
- F009 / revised：核心事实全部与 E007 对齐（player_kotlin 7/0/100→455/37/841；player_java 958/3222→953/3308），排除性推断方向正确，且已列出族口径/编译器/分包/迁移多重替代解释，未宣称新样式或适配通过，level=candidate 恰当。两处需收紧：一是“448 类增量无法用 Java→Kotlin 迁移解释”表述过强，应为“仅凭 player_java 减少 5 类不足以解释该增量”，以免把未读全量类清单的推断写成定论；二是 E013 是评论页定位器，草稿称“同类定位器”易被读成 player 家族源码证据，需明确仅为同仓库机制旁证，不证明 player 定位器命中与 Hook 生效。（E007, E013, E000）
- F010 / retained：断言逐条对应 E008：danmaku_legacy 目标与基线两侧均 absent、0 类/0 边、指纹为空数组摘要（sha256 4f53cda1…），确为查询口径层面的空集；danmaku_kotlin 57/1/8→137/3/162；danmaku_kotlin_moss 定义 46 不变而消费边 4→10，故“新增落在既有接口调用方”成立。未登记协议 KDanmuMoss、KPlayerMoss 等存在属 E000/seed 清单事实，跨家族消费者仍标为待确认。分析对未读源码的 DanmakuPurifyInstaller/Policy 采用条件式表述（“若仍以原生弹幕类为锚点”），未推断 Hook 覆盖，absent 明确不等于功能消失，并给出登记口径缺陷、未登记锚点、服务端下发三类替代解释，level=candidate 与证据强度相符。（E008, E000）
- F011 / retained：证据支持：E009 双侧汇总可逐项核对——story_native 目标 2956 类 / 44 compose 方法 / 1328 边（dafc7376…），基线 2924 / 44 / 1310（b56b7342…），+32 类、+18 边、compose 方法数不变；story_kotlin 两侧 0/0/0 且指纹同为 4f53cda1…。据此把结论限定为“结构刷新候选、不足以确认新竖屏详情样式”，并显式列出混淆改名、DEX 重排、族归档口径差异作为替代解释，符合“结构哈希变化不等于新样式”的要求；level=candidate 与矩阵 status install-status 未被越界提升。E011（comment_compose）与 E012（dynamic_opus）在文中仅作边界说明并明确“不能作为 story 路径的覆盖或排除依据”，未被当作覆盖证据使用，引用可接受但无增量。与此同时草稿明确声明未读到任何 story 族类级明细、模块源码未读、安装器与运行期未知，未外推 Hook 覆盖，故无过度断言需要修正。（E009, E011, E012）
- F012 / revised：主体成立但存在两处需修：一是正文出现“同页 mine_native 336→… 实为 325→326”的残留错误计数，与 E010 的 325→326 / 92→94 不一致，易被误读为台账错误；二是 evidence_ids 中的 E013、E014 分别指向 CommentClassicStyleLocator.kt（sha256 2ec67116…）与 DynamicPurifyPolicy.kt（sha256 e76741e1…），属评论/动态路径，原文未说明其只作“反射验真 + 读失败保守放行”的模块内模式参照，存在被当作“我的”页覆盖证据的风险。修订保留“计数零变化但指纹改变优先按混淆/重编解释、字段级读取仍是待验证风险、level=needs_runtime”的判断，并补入 E010 的预取限制（每族两类样本，实际载荷仅族汇总、无类字段明细）与“我的”页源码未读的具体文件清单。证据编号按规则不变更。（E010, E013, E014）

### 尚未解决的证据缺口

- [1] 草稿 overview 混入了非本单元的 home/search/detail/pgc/player/danmaku/mine/story 段落，组装最终报告时须按本单元只保留 comment 与 dynamic 两部分，删除跨单元内容与对应引用。
[2] 八条登记路径（comment 五条、dynamic 三条）均无安装器源码读取与真机安装日志证据，runtime_enabled 与 module_coverage 仍为 unknown/requires_installer_review；本轮不得宣称任一路径适配通过。
[3] comment_kotlin_moss 消失的 3 条调用边的宿主调用方清单未取得（复核阶段工具额度耗尽），消费者迁移与编译产物差异无法区分。
- [4] comment_native_exp3 类 58→54、边 62→52 双降的成因未证：matchesKey 仍收 comment.next_appearance_experiment_3（E017），但该常量在 9.17.0 宿主侧是否仍有读取方未检索。
[5] 评论页 E011 仅 5 个类样本（有界摘录），无法代表 2428 类；需要对新增边的目标类做两版集合差与逐类 decompile_class。
[6] dynamic_legacy 外调边 2151→2075 的 76 条被移除边未做集合差，DynamicPurifyPolicy 信号来源（正文列表、作者、附加类型）与标签访问点是否在其内未知。
- [7] dynamic_opus 与宿主 AdditionalType 的引用关系、以及 Opus 卡片正文能否经 Signals.textFragments 读取，均未读源码/反编译确认；兜底集合 {2,6} 是否仍与宿主常量一致未核对。
[8] 动态净化安装器与标签安装器的实际安装家族、切换条件、服务端 A/B 及平板/宽屏形态均未读到运行条件，静态不可见部分保留未知。
[9] 源码快照为 dirty worktree（source_tree_sha256 37745f8f…）；本轮所读 CommentClassicStyleLocator.kt 哈希 2ec67116…、DynamicPurifyPolicy.kt 哈希 e76741e1…，结论按这两个文件哈希追溯，未清理工作树。
- [10] 评论�� CommentLegacyCopyBridge、CommentComposeViewAccess、CommentReplyButtonCompose、CommentEmojiAdapter 等安装点未读全文，其 Hook 落点与 9.17.0 组合函数/方法签名的对应关系未证。
[11] 本单元未读取任何 home/search 模块源码：HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeBannerFeatureInstaller.kt、HomeComponentFilterFeatureInstaller.kt、HomeTabFilterFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt、HomeRecommendPurifyFeatureInstaller.kt、SearchHomeRecommendLocator.kt、SearchHomeRecommendFeatureInstaller.kt、SearchHomeRecommendPolicy.kt、SearchPurifyFeatureInstaller.kt、SearchDefaultWordsCleaner.kt 的锚点常量、匹配方式与失败兜底全部未知，不得据此下 Hook 覆盖结论。
[12] E003/E004 为预取有界视图（每族两个类样本、每协议四个调用方样本），复核阶段未用 family_evidence 重读全量：home_legacy -1 类/-6 边、home_new_frame +3 边、search_native -41 边、search_compose +3 类/+1 compose 方法/+19 边的具体所属类与方法描述均未取得。
- [13] 缺少目标-基线方法描述差集，混淆改名、DEX 重排、包装层合并/拆分与按目标类分组的边重分组均未能排除；边数与类数变化目前只能作计数事实陈述。
[14] 协议侧只有 definitions 与 actual_invoke_edges 两个计数，无 fingerprint 或签名差集；禁止用定义数除边数推覆盖率，也不能断言协议结构未变。
[15] E000 未登记清单中的 app/interfaces/v1/SearchMoss|KSearchMoss、app/search/v2/SearchMoss|KSearchMoss、broadcast/message/main/SearchMoss、broadcast/message/search/SearchMoss 及 app/home/v1/HomeMoss|KHomeMoss、feed/v1/KFeedMoss、broadcast/message/main/NativePageMoss 的宿主消费者未归类，是否与已登记 MOSS 同一实现未知；home 族在 seed 中完全没有登记协议，数据面覆盖缺口未评估。
- [16] 两条 search 协议与多套同名 SearchMoss 的跨家族消费者未取 protocol_evidence 调用方清单，无法判断是否存在 Java/Kotlin/原生/Compose 共用协议路径。
[17] 真机未验证：home/search 实际启用栈、安装器装配成功与命中次数、DeviceDecision 语义键取值、回退到语义 DEX 查询的结果键；runtime_enabled 全为 unknown。
[18] 并存栈切换条件、平板/宽屏布局分支、深浅色分支与服务端 A/B 在静态矩阵中不可见；服务端开关无结构变化时不可静态断言样式已穷尽，也不能宣称某路径失效。
- [19] fresh_refresh 为空，复核阶段未重新取证 home/search；本单元结论依据首条消息下发的 E000/E003/E004 预取视图。E011/E012/E013/E014 属评论与动态族，仅 E013 被用于说明定位器模式，不得外推到 home/search 的结构判断。
[20] 草稿 overview 与 next_steps 含未分配页面（comment、dynamic、detail、pgc、player、danmaku、story、mine）的结论与任务，本单元未复核；这些内容须由对应单元处置，不得并入 home/search 结论。
[21] 所有登记路径 status 只能逐字沿用静态矩阵的 static_invoke_observed；页面级 status installer_and_runtime_validation_required 不得读作适配结论或版本已适配。
- [22] detail_theseus_ugc 与 detail_theseus_united 两族尚未做 method_bodies_sha256/签名集合的逐类基线比对，无法区分“混淆改名/DEX 重排/重复包装层”与真实方法体变化（E005 仅给出汇总计数与两条类样本）。
[23] detail_kotlin_moss 实际调用边 10→38 的调用方未聚类，无法判断是新增消费者、bridge 包装类增生还是族归档口径变化（E005 仅 4 条调用方样本）。
[24] detail 页各 installer（DetailModulePurify / DetailUnitedModulePurify / DetailUnitedPresentationPurify / DetailViewPurify / DetailAppPromotion / HomeVerticalDetail）源码本轮未读，锚点类名、匹配点数量、兜底顺序与运行条件均为未知，Hook 覆盖不可推断。
- [25] E011 的 comment_compose 家族与 detail 页之间的实际调用关系未取证；仅凭“存在以 KReplyInfo 为参数的方法”不能证明 detail 页启用该 Compose 评论家族，需取 detail 页内评论入口的调用边或真机栈。
[26] E013 摘录未包含 CommentModel 判据及 locate 完整逻辑，CommentClassicStyleLocator 的锚点解析失败行为（回退 DexAssistQuery 还是静默不处理）与三条 native/compose 路径的安装器是否实际安装仍未知。
[27] detail_legacy 在两侧同为 0 类的 absent 尚无解释：需确认是族选择器包名/继承规则未覆盖该实现，还是旧原生详情已不在 base.apk，或其他 split 承载。
- [28] pgc 的 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupPolicy.kt、PgcAutoActivityPopupFeatureInstaller.kt 全文未读，锚点、匹配点数、legacy/theseus 双栈对应关系与兜底分支均未知；E014 只是动态页策略的类比，不能外推。
[29] pgc_theseus +397 条外部调用边与 pgc_legacy +26 条边的来源类未定位，需边集合差与 decompile 交叉确认是否为新消费者或重排；legacy 减少的 2 类是被合并进 theseus 还是移除亦未确认。
[30] 两条页面族均缺真机安装日志：各 installer HookPoint 命中数、dex.assist.comment_classic 等诊断键返回值、以及 legacy/theseus/UGC/united/PGC 播放页/PGC 详情页多入口的开关前后差异均未采集，runtime_enabled 仍为 unknown。
- [31] 平板/宽屏布局分支与深浅色配置是否走不同家族或不同安装器未检查，静态矩阵未登记该形态，可能存在未归类调用者。
[32] 服务端 A/B 与页面样式开关对 detail/pgc 家族选择的影响静态不可见，本轮不能宣称所有样式已穷尽。
[33] 源码快照 worktree 为 dirty（source_tree_sha256=37745f8f…，repository_head 5422fad1…），本轮所引 E013/E014 文件哈希已固定（CommentClassicStyleLocator 2ec67116…、DynamicPurifyPolicy e76741e1…），但其余相关 installer 文件哈希尚未登记，复核对齐需补齐。
- [34] player 侧安装器与定位器源码（PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerPopupPromotionAdapter、PlayerEndPageRecommendLocator）内容未读，安装点命中/回退与 Compose 层覆盖未知，E013 仅能作为评论页机制旁证。
[35] player_kotlin 455 类与 player_java 953 类尚未做两版全类名/方法签名归一化 diff，455 类增量的来源（真实迁移、族选择器口径、Kotlin 元数据识别、DEX 分包）未判定。
[36] player 两条路径的 runtime_enabled 全为 unknown；无安装器诊断日志（命中/回退/未安装原因）与真机倍速、缓冲上限、清晰度/码率强制、弹窗推广、横竖屏与平板宽屏回归数据。
- [37] danmaku_legacy 族选择器包名/继承规则未核对，两侧空集是登记缺口还是该实现不在 base.apk（或位于未纳入的 split/动态模块）未确认。
[38] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 全文未读，净化锚点、兜底顺序、开关默认值，以及与 danmaku_kotlin 137 类/10 条 MOSS 消费边的对齐关系均未知。
[39] 未登记协议 KDanmuMoss、KPlayerMoss、KPlayerOnlineMoss、ListenerMoss 等是否存在被 player/danmaku 家族实际调用的跨家族消费者，尚未归类。
- [40] 弹幕与播放器的服务端 A/B、DeviceDecision 语义开关以及平板/宽屏布局分支是否引入第三套渲染路径，静态不可见，仍为未知。
[41] 源码快照为未提交工作树（source_tree_sha256 37745f8f…，source_files_total 689），本单元所引 player/danmaku 相关文件内容未读，结论须按单文件哈希追溯，不得据此推断 Hook 覆盖。
[42] 本轮复核未新增发现：player/danmaku 的候选疑点已由 F009/F010 覆盖，其余观察留待上述补证任务完成后再评估。
- [43] E009、E010 预取只含族汇总，limits 声明的“每族两类样本”未落到载荷中：story_native 新增 32 类 / 18 边、mine_native 新增 1 类 / 2 边、mine_account_model 指纹变化的具体来源类均未定位。
[44] story 模块源码未读正文：HomeVerticalDetailFeatureInstaller、HomeVerticalDetailRouting、StoryActionIconsFeatureInstaller、StoryActionIconsPolicy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess 的锚点常量、定位顺序与失败兜底未知。
[45] mine 模块源码未读正文：MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineComponentSnapshotStore/QueryContract/HostBridge、MineVipFeatureInstaller、HostMineReadingCard 未核对，字段名来源（硬编码 vs 反射）与兜底未知。
- [46] story_kotlin 双侧 absent 的查询键与族名匹配规则未核实，无法排除竖屏详情的 Kotlin/Compose 承载落在未归类命名下；absent 不可读作功能消失。
[47] 两侧 story/mine protocols 均为空，未登记协议清单中的 StoryMoss/KStoryMoss、MineMoss/KMineMoss、relation/interfaces 的宿主消费者与跨家族共用路径未取证。
[48] 无安装器诊断日志与真机运行证据：两页全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，不得宣称适配通过。
- [49] 服务端 A/B、开关驱动的样式变体与平板/宽屏分支在无结构变化时静态不可见，本页家族是否穷尽未知。
[50] 源码快照为 dirty worktree（source_tree_sha256 37745f8f…、repository_head 5422fad1…、captured_at 2026-10-15），本单元涉及的 story/mine 源码均未读，后续需按单文件哈希追溯，不建议清理工作树。
[51] E013/E014 属评论/动态路径，仅为模块内“反射验真 + 读失败保守放行”的模式参照；story/mine 缺少同级别的探针源码核对。
- [52] 待补证新问题（下一轮）：mine_native 新增 1 类 / 2 边是否进入“我的”页组件装配链；mine_account_model 抽样类字段级 diff 与 2b548e1a…→db7f2792… 指纹差异的归因。
[53] 待补证新问题（下一轮）：story_native 新增 32 类是否含 Compose 入口或与竖屏详情路由直接相接，需 family_evidence + decompile_class 成对核对。
[54] 本会话 fresh_refresh 为空，story/mine 未做二次取证，全部结论仅基于首轮预取 E009、E010；未复核服务端是否重跑了这两页。

## 下一步

- [1] 对 comment_compose 与 dynamic_legacy 分别做两版外调边集合差，输出『目标类仅出现在 9.17.0』的边清单，逐条 decompile_class 判定新增入口还是重排，替代当前仅凭计数的推断。
[2] 真机 9.17.0 打开评论页，记录 CommentClassicStyleLocator.locate 的 NATIVE/KOTLIN reader 数量与是否回退 DexAssistQuery，确认 native_legacy/native_next/native_exp3 三条路径的安装器是否实际安装。
[3] 确认 9.17.0 中 AdditionalType 的 additional_type_goods_VALUE 与 additional_type_up_rcmd_VALUE 常量是否存在、数值是否仍为 2/6，避免 DynamicPurifyPolicy 静默落到兜底集合。
[4] 对 kntr.app.following.opusDetail.api 下一正文承载类 decompile_class，确认 Opus 卡片正文能否经 Signals.textFragments 读取，并核对 promotion/lockedChargeOnly 信号来源。
[5] 用 protocol_evidence 获取 comment_kotlin_moss 两版调用方清单，定位消失的 3 条边的宿主类，判断是否迁入 Compose 家族。
- [6] 真机分别触发 Java MOSS 与 Kotlin MOSS 回复通道，统计模块通道 Hook 命中次数，补齐运行时启用与安装器覆盖证据。
[7] 确认动态页平板/宽屏布局与服务端开关是否引入第三套渲染路径；静态矩阵未登记该形态，需以运行期日志判断是否属未归类调用者。
[8] 复核阶段独立重跑边集合差与模块源码核对，确认 dirty worktree（source_tree_sha256 37745f8f…）下 CommentClassicStyleLocator 与 DynamicPurifyPolicy 的文件哈希未被本地修改影响结论。
[9] 以同参数重读 family_evidence(home_legacy/home_new_frame, target)，取完整类与方法清单，消除预取两类的抽样限制
[10] 以 module_source 读取 HomeFrameTabLocator.kt 与 HomeFrameListHook.kt，核对锚点常量与 9.17.0 宿主类名一致性及兜底分支
- [11] 以 module_source 读取 SearchHomeRecommendLocator.kt 与 SearchHomeRecommendFeatureInstaller.kt，确认搜索推荐净化的解析点与失败兜底
[12] 对 search_java_moss / search_kotlin_moss 取完整协议调用方，核对与 app/interfaces/v1 及 app/search/v2 多套 SearchMoss 注册名是否同一实现
[13] 导出 9.16.1↔9.17.0 每族方法描述集合差，区分删除、改名、迁移与新增，排除混淆与 DEX 重排解释
[14] 真机 9.17.0 分别进入旧原生首页与 Compose 首页，记录模块安装日志与 Hook 命中计数，判定实际启用栈
[15] 真机分别从原生与 Compose 搜索入口触发检索，验证默认词清洗与推荐净化是否生效
- [16] 检查搜索页与首页在平板/宽屏与深浅色下的布局分支是否走不同家族或不同安装器
[17] 确认服务端开关对搜索首页推荐与首页帧结构的影响；无结构变化的 A/B 不可静态断言已穷尽
[18] 按 source_tree_sha256=37745f8f… 与单文件哈希追溯修改中的工作树文件，不改动工作树
[19] 用 family_evidence 重读 detail_theseus_ugc 与 detail_theseus_united 类样本，输出方法体哈希/签名差异清单，区分改名与真实方法体变化。
[20] 用 family_evidence 重读 pgc_theseus 与 pgc_legacy 类样本，定位 +397 调用边的来源类与 +26 边的来源类。
- [21] 读 DetailModulePurifyFeatureInstaller/Policy、DetailUnitedModulePurifyFeatureInstaller/Policy、DetailUnitedPresentationPurifyFeatureInstaller/Policy、DetailViewPurifyFeatureInstaller/Policy 全文，登记锚点与兜底。
[22] 读 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupPolicy.kt、PgcAutoActivityPopupFeatureInstaller.kt 全文，确认 legacy/theseus 双栈覆盖与匹配点数量。
[23] 核查 HomeVerticalDetailFeatureInstaller/HomeVerticalDetailRouting 与 HostDetailSurfaces，确认是否存在第三条详情承载路径未纳入静态矩阵。
[24] 真机 9.17.0 采集安装日志：各 installer HookPoint 命中数、dex.assist.comment_classic 等诊断键返回值。
[25] 真机分别经 UGC 详情、united 详情、PGC 播放页、PGC 详情页四入口验证净化与自动弹窗行为，记录开关前后差异。
- [26] 对 detail_kotlin_moss 实际调用边 10→38 做调用方聚类，判断是否为 bridge/包装类增生。
[27] 对 pgc 服务端 A/B 与详情页样式开关做抓包对照，确认是否存在静态不可见的样式切换。
[28] 在平板/宽屏配置下复测 detail 与 pgc 入口，确认是否仍走已登记家族。
[29] 以文件哈希记录本轮 dirty worktree 下所读源码版本，供后续复核对齐，不建议清理工作树。
[30] 补齐 detail_legacy absent 的解释任务：用历史入口/深链在真机确认是否仍有旧原生详情栈存在。
- [31] 对 9.16.1 与 9.17.0 的 base.apk 分别导出 player_java/player_kotlin/danmaku_kotlin 类全清单与方法签名，做归一化 diff，判明增量是新增、改名还是族归档口径变化
[32] 核对 danmaku_legacy 族选择器的包名/继承规则，确认两侧 absent 是登记缺口还是该实现本就不在 base.apk
[33] 在 base.apk 全部 DEX 检索 danmaku/danmu 相关包与自绘弹幕 View 类，并检查是否存在其他 split 承载弹幕实现
[34] 读取 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 的定位常量、兜底顺序与开关默认值，逐条对照 danmaku_kotlin 的 137 类与 10 条 MOSS 消费边
[35] 读取 PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerPopupPromotionAdapter、PlayerEndPageRecommendLocator，确认是否依赖纯类名/描述符匹配
- [36] 采安装器日志，对 player 与 danmaku 各安装点记录命中、回退与未安装原因，区分静态可见与运行期启用
[37] 真机验证 player：倍速切换、缓冲上限、清晰度/码率强制、弹窗推广过滤、横竖屏与平板宽屏分支
[38] 真机验证 danmaku：视频弹幕、直播弹幕、宽屏/平板布局下净化生效情况，并记录 Compose 弹幕层表现
[39] 对未登记协议中的 KDanmuMoss、KPlayerMoss、KPlayerOnlineMoss、ListenerMoss 做消费者归类，确认是否被 player/danmaku 家族实际调用
[40] 对源码未提交修改按文件哈希登记（工作树 dirty，source_tree_sha256=37745f8f…），本报告涉及的 player/danmaku 源文件均未读内容，需补齐后再评估 Hook 覆盖
- [41] 确认服务端 A/B 与设备侧 DeviceDecision 语义锚点是否控制弹幕样式切换，静态不可见部分标记为待运行期验证
[42] 补齐后复核：若族归档口径被证实，撤销 player_kotlin 与 danmaku_kotlin 的“新样式”候选表述，仅保留计数与调用边差异
[43] 读 HomeVerticalDetailFeatureInstaller.kt 与 HomeVerticalDetailRouting.kt，导出 HookPoint 描述符清单，作为 story_native 点位校验基线。
[44] 对 story_native 新增类在目标/基线成对 decompile_class，比对同名描述符方法体哈希，排除混淆改名与 DEX 重排解释。
[45] 用 family_evidence 复核 story 家族目标侧类集与调用边，确认新增 32 类是否进入详情渲染/分发链。
- [46] 核查 story_kotlin 的 absent 查询键定义，确认 absent 是命名不匹配还是宿主确无 Kotlin 承载；记录确切查询键。
[47] 读 StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess，登记其宿主锚点与失败兜底路径。
[48] 读 MineVipFeatureInstaller.kt 与 MineComponentSnapshotQueryContract.kt，确认字段名来源为硬编码还是反射按名查找。
[49] 对 mine_account_model 抽样类在两侧 decompile_class，逐字段比对名称/类型，解释指纹变化来源。
[50] 对 mine_native 新增 1 类与新增 2 条边读调用边，判断是否落在“我的”页组件装配链。
- [51] 检索 StoryMoss/KStoryMoss/MineMoss/KMineMoss 的宿主消费者，判断是否存在跨家族（原生/Kotlin/Compose）共用协议路径。
[52] 真机 9.17.0 采集安装期 hint 与 DEX 定位诊断日志，逐路径记录命中/未命中，区分样式候选与已确认样式。
[53] 真机在“我的”页覆盖未登录/已登录/VIP 账号态与宽屏/平板布局，记录组件过滤与阅读卡片实际结果。
[54] 对服务端开关与 A/B 变体保留未知标注：静态无结构变化时不得宣称所有样式已穷尽。