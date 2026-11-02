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
| comment_compose | 2528 | 288 | 1115 | static_invoke_observed |
| comment_legacy_v2 | 574 | 0 | 728 | static_invoke_observed |
| comment_native_exp3 | 57 | 0 | 55 | static_invoke_observed |
| comment_native_legacy | 182 | 0 | 248 | static_invoke_observed |
| comment_native_next | 44 | 0 | 57 | static_invoke_observed |
| comment_other_ui:(root) | 225 | 2 | 511 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 216 | 0 | 111 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 241 | 31 | 281 | static_invoke_observed |
| danmaku_kotlin | 137 | 3 | 164 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1975 | 25 | 522 | static_invoke_observed |
| detail_theseus_united | 4669 | 98 | 4193 | static_invoke_observed |
| dynamic_compose | 1413 | 183 | 270 | static_invoke_observed |
| dynamic_legacy | 3273 | 105 | 2156 | static_invoke_observed |
| dynamic_opus | 1349 | 95 | 224 | static_invoke_observed |
| dynamic_other:appointment | 32 | 4 | 19 | static_invoke_observed |
| dynamic_other:card | 429 | 89 | 307 | static_invoke_observed |
| dynamic_other:commonCore | 26 | 0 | 62 | static_invoke_observed |
| dynamic_other:commonPerf | 14 | 1 | 2 | static_invoke_observed |
| dynamic_other:commonUi | 20 | 5 | 9 | static_invoke_observed |
| dynamic_other:lightBrowser | 78 | 19 | 30 | static_invoke_observed |
| dynamic_other:playershare | 1 | 0 | 3 | static_invoke_observed |
| dynamic_other_legacy | 2106 | 4 | 2161 | static_invoke_observed |
| home_legacy | 785 | 88 | 184 | static_invoke_observed |
| home_new_frame | 199 | 33 | 46 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 327 | 7 | 94 | static_invoke_observed |
| pgc_legacy | 357 | 0 | 307 | static_invoke_observed |
| pgc_theseus | 2255 | 132 | 913 | static_invoke_observed |
| player_java | 954 | 0 | 3305 | static_invoke_observed |
| player_kotlin | 466 | 37 | 897 | static_invoke_observed |
| search_compose | 3152 | 562 | 614 | static_invoke_observed |
| search_native | 1695 | 2 | 2913 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2969 | 45 | 1419 | static_invoke_observed |

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
- dynamic_other:playershare: structure_or_call_path_changed
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

本单元覆盖 comment（5 条登记路径）与 dynamic（3 条登记路径），对比基线 9180100→目标 9180200（同签名、同 arm64）。八条路径指纹全部变化，证据值一律为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，complete_coverage=false，故本报告不宣称任何适配通过。量级上 comment 家族类数变化在 -5~+27 之间，compose_methods 基本持平（288→288 附近）；dynamic_legacy 类数 +19 但 compose_methods 保持 105，dynamic_compose 外部调用边 -17。协议层 comment_java_moss 与 dynamic_java_moss 的定义数与实际调用边相等（50/50、134/134），而 kotlin_moss 定义远多于实际调用边（130/23、382/27），说明 Kotlin 通道存在未解析消费者，兜底覆盖需安装器侧核实。冻结源码暴露两个关键安装期解析点：CommentComposeViewAccess 通过反射解析 AndroidCompositionLocals_androidKt.getLocalView 与 Composer.consume(CompositionLocal)，DynamicPurifyPolicy 优先读宿主 AdditionalType 常量并以 {2,6} 兜底；两者都在安装期定型、热路径无二次回退，结构或混淆变化会表现为静默降级而非异常。

本单元覆盖 home（home_legacy、home_new_frame）与 search（search_native、search_compose）四条登记路径，目标 9.18.0(9180200)，基线 9.18.0(9180100)。四族指纹全部变化且四条路径均标记结构或调用路径变化，需要复核：home_legacy 类 785（基线 782）而外部调用边 184（基线 203）；home_new_frame 类 199（190）而边 46（54）；search_native 类 1695（1704）而边 2913（2865）；search_compose 类 3152（3131）而边 614（617）。四族 compose_methods 完全未变（88/33/2/562），搜索两条 Moss 协议的定义数与实际调用边也完全未变（java 24/22、kotlin 52/18），说明变化集中在宿主 UI/数据类集合的重排或迁移，而非协议接口面。所有路径 evidence 仅为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，故不得判定适配通过。home 侧协议登记为空，搜索侧存在 3 个未登记 SearchMoss 家族，协议覆盖缺口需计入未知。源码快照为脏工作树（source_tree_sha256 37745f8f…，captured_at 2026-10-15），模块侧结论按文件 sha256 追溯，不代表安装器或真机覆盖。search 侧唯一读到的定位器 SearchHomeRecommendLocator 对候选/状态类施加 singleOrNull 唯一性约束并只枚举单字符嵌套后缀，是本单元最需要真机验证的静默退化点。

本单元只覆盖 detail 与 pgc 两页，样本 9.18.0(9180200, sha256 48138d…) 对基线 9180100(a12d3e…)，同包同证书 arm64-v8a。detail 三条登记路径：detail_legacy 两侧均为空集且指纹同为 4f53cda1…（空集哈希），判为 absent，不等于旧原生详情页功能消失；detail_theseus_ugc(1975 类/25 Compose/522 边)与 detail_theseus_united(4669 类/98 Compose/4193 边)均为 static_invoke_observed，指纹较基线变化，但类数仅 ±2/±10、Compose 方法数不变，幅度更像 R8 重排/改名/代码迁移，尚不能称新样式。detail_java_moss(32 定义/35 边)与 detail_kotlin_moss(76 定义/34 边)两版计数完全一致，说明协议定义层未见新增消费者，但实际调用边数量不等于覆盖率。pgc 两栈并存：pgc_legacy 类 345→357、边 301→307 增加，pgc_theseus 类 2258→2255、Compose 134→132、外部调用边 982→913 明显减少，属重心迁移候选；pgc_player_moss(12/3)与 pgc_view_moss(14/7)两版一致。四路径 runtime_enabled 均为 unknown，module_coverage 均 requires_installer_review，complete_coverage=false 且源码快照 working_tree_dirty=true，因此本报告只给静态事实与待验推断，不宣称适配通过。

本单元仅覆盖 player 与 danmaku 两页，对照 9180100→9180200（同版本名 9.18.0，仅 version_code 不同）。player_java 为 954 类/3305 条外部调用边（基线 953/3300），player_kotlin 为 466 类/37 个 Compose 方法/897 边（基线 480/37/891）；danmaku_kotlin 为 137/3/164，与基线五项计数完全一致，danmaku_legacy 两侧均 absent；协议侧定义数与实际调用边数两侧完全相同（player 18/2 与 34/3；danmaku 22/20 与 46/12）。三处家族指纹变化但计数几乎或完全不变，最先应排查混淆改名、DEX 重排与代码迁移，而不是判定新样式。全部 runtime_enabled 为 unknown、complete_coverage=false、模块覆盖 requires_installer_review，本报告不宣称任何路径适配通过。

本单元覆盖 story 与 mine 两页、四个登记路径。sample 9.18.0(9180200) 与基线 9180100 同包同证书，仅 code 递增，属相邻小版本对比（E000）。静态矩阵显示：story_native 与 mine_native、mine_account_model 均为 static_invoke_observed，story_kotlin 为 absent；四路径 runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review（E009/E010）。三类变化均为 structure_or_call_path_changed。数值上 story_native 类数 2969←2974、边数 1419←1470 而降、compose_methods 恒为 45；mine_account_model 类数 132、边数 43 与基线完全一致仅指纹变化；mine_native 类数 327←326，边数 94、compose_methods 7 不变。因此没有证据支持"新样式产生"或"功能消失"，只能作为待复核的结构/调用路径差异。本轮未取得 story/mine 的直接运行条件、安装器命中记录与模块 Hook 生效证据，结论止于静态候选，不得视为适配通过。

## 各页面评估

### comment

comment 页五条家族并存：legacy_v2（574 类/728 边）、native_legacy（182/248）、native_next（44/57）、native_exp3（57/55）、compose（2528 类/288 compose 方法/1115 边）。与基线相比类数分别为 -5、+6、-5、-1、+27，外部调用边分别为 -26、+3、-1、-1、-27；数量级变化小、方向不一致，更像 DEX 重排与混淆改名叠加，而非新增样式，但指纹全变，仍需逐路径确认调用方。compose 家族占比最大，模块侧 CommentComposeViewAccess 依赖 androidx.compose.ui.platform 与 androidx.compose.runtime 的稳定符号（getLocalView、Composer.consume），resolve 失败即返回 null，属静默降级路径，因此 compose 家族任何结构变化都应优先做真机解析验证。协议层 comment_java_moss 定义 50/调用边 50、comment_kotlin_moss 定义 130/调用边 23，Kotlin 侧大量定义没有对应实际调用边，跨家族消费者是否覆盖无法从静态矩阵判断。所有路径 runtime_enabled 均为 unknown，安装器是否注册到 native_next/exp3 未核实。

证据：E000, E001, E011, E013

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类数 579→574、外部调用边 754→728、指纹由 c5e0f69… 变为 8ca51ee…；降幅约 1%，与日志类、包装类被合并/裁剪的量级一致。
- 可能影响：legacy_v2 是评论主链路，模块侧 CommentLegacyCopyBridge/经典样式定位若按类名与调用点匹配，改名或迁移会让 hook 点失配且不报错。
- 验证：在 9180200 上对比 legacy_v2 的类名集合与基线差集，确认是否有类被删除或仅在 DEX 间移动；对 CommentClassicStyleLocator 打印命中/未命中日志统计。
- 证据：E000, E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类数 176→182（+6）、外部调用边 245→248（+3）、指纹由 29fb0f0… 变为 32c92a7…。
- 可能影响：规模小幅上升，可能是新增小类或内联展开；native_legacy 与 native_next/exp3 并存，若切换条件由服务端开关控制，静态无法判断实际启用分支。
- 验证：检索新增 6 个类的调用者是否落在 CommentNativeBindingCatalog 的绑定范围内；真机下按版本/服务端开关分别进入评论区，记录 native 家族实际加载的绑定表条目。
- 证据：E000, E001

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类数 49→44（-5）、外部调用边 58→57（-1）、指纹由 2449027… 变为 39e97d0…。
- 可能影响：native_next 规模最小，5 个类消失也可能是合并到相邻类；若模块只对 next 家族注册 Hook，删除会让该分支完全失去补丁面。
- 验证：用反编译对比 44 类的超类/接口签名，确认是否迁移到 legacy 或 compose 家族；真机 next 开关分支下检查模块安装日志中的家族选择项。
- 证据：E000, E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类数 58→57（-1）、外部调用边 56→55（-1）、指纹由 67ad049… 变为 929d62b…。
- 可能影响：变化最小，可能只是单个类重排或常量跳动；exp3 属实验家族，启用条件通常由服务端 A/B 决定，静态不可见。
- 验证：确认 57 类集合与基线的差集是否为空（仅顺序变化）；用同一账号在实验组/对照组分别进入评论区，观察 exp3 类是否被加载。
- 证据：E000, E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类数 2501→2528（+27）、compose_methods 289→288（-1）、外部调用边 1142→1115（-27）、指纹由 9c77cdf… 变为 67e96ff…。
- 可能影响：compose 家族体量最大且是模块 CommentComposeViewAccess 的唯一宿主 ABI 依赖面；类数上升而调用边下降的组合提示内部实现重构或包装层增删，反射解析点一旦失配，Copy/Purify/ReplyButton 三条 Compose 桥会同时空转。
- 验证：在 9180200 真机打印 CommentComposeViewAccess.resolve 的返回值（consume/local 是否非空）；若为 null，进一步确认 AndroidCompositionLocals_androidKt 与 Composer.consume 的重载签名是否变化；同时用 288 个 compose 方法样本比对 CommentComposePurifyBridge 的目标签名命中率。
- 证据：E001, E011, E013

### dynamic

dynamic 页三条家族：legacy（3273 类/105 compose 方法/2156 边）、compose（1413/183/270）、opus（1349/95/224）。相对基线：legacy 类数 +19、调用边 +20 而 compose_methods 保持 105；compose 类数 -8、compose_methods +1、调用边 -17；opus 类数 -21、compose_methods 不变 95、调用边 -3。三条路径均出现“类数变化但 compose 方法数几乎不动”的组合，与混合栈（原生 + Compose + Opus）并存一致，不能据此断言新样式。协议层 dynamic_java_moss 134/134 边齐平，dynamic_kotlin_moss 382 定义仅 27 条实际调用边，缺口显著；动态相关 Moss（DynamicMoss、KOpusMoss、OpusMoss、mall/tab3/dynamic/v1/OpusMoss、FeedMoss 等）全部位于未登记协议清单，说明存在模块未纳入的跨家族数据消费者。模块侧 DynamicPurifyPolicy 以 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE 常量判定带货与 UP 推荐，读不到时回退 {2,6}，并对文本逐段回调匹配；若 opus 家族换了数据来源，净化会静默放行。

证据：E000, E002, E012, E014

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类数 3254→3273（+19）、外部调用边 2136→2156（+20）、compose_methods 105→105、指纹由 1aee4b8… 变为 3a4ffd1…。
- 可能影响：legacy 家族最大，新增 19 类可能为卡片类型或净化判定输入；模块 DynamicPurifyFeatureInstaller 若按类型/卡片类绑定，新增分支不会被治理而表现为漏删。
- 验证：取新增类与 AdditionalType 常量的引用关系，确认是否引入新的 additional_type；真机开启动态净化，统计每类卡片命中与未命中（读不到的 Signals 字段记 null 而非 false）。
- 证据：E002, E014

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类数 1421→1413（-8）、compose_methods 182→183（+1）、外部调用边 287→270（-17）、指纹由 76028ed… 变为 9c97046…。
- 可能影响：调用边下降 17 而 compose 方法增 1，提示调用被合并到更少入口或部分逻辑迁出；Compose 侧净化/复制桥依赖稳定 composable 签名，入口收敛会让按方法注册的 hook 只覆盖到部分卡片。
- 验证：对 183 个 compose 方法做签名与基线的差集，检查 Hook 目标方法是否仍在；真机在 Compose 动态页打印桥接安装日志与方法命中计数。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类数 1370→1349（-21）、compose_methods 95→95、外部调用边 227→224（-3）、指纹由 72569a3… 变为 e50b06c…。样本仍为 kntr/app/following/opusDetail/api 下的 Kotlin 数据类与 CompositeExternalInterceptor 协程续体，未出现新界面族特征。
- 可能影响：Opus 家族体量收缩但 compose 方法数不变，属于结构调整候选；模块是否对 opus 卡片做净化取决于它是否走 dynamic_java_moss 或未登记的 OpusMoss/KOpusMoss，静态矩阵未回答。
- 验证：核对 21 个消失类是否迁移至 mall/tab3/dynamic/v1/OpusMoss 或 kntr/app/following 其他包；真机进入 Opus 详情与动态流，抓 DynamicPurifyPolicy.Signals 的 promotion/lockedChargeOnly 是否仍能读到非空值。
- 证据：E002, E012, E014

### home

home 两条登记路径并存于目标版本：E015 抽样的 home_legacy 家族仍含 Ltv/danmaku/bili/ui/main2/HomeFragmentV2、StartupFragmentV2、AccountMineRequestResource 等旧原生 Fragment/资源枚举类，说明旧 View 栈未被移除；home_new_frame 家族规模明显更小（199 类、33 个 compose 方法、46 条外部边），符合“新框架只承载新入口/新卡片容器”的形态，但本单元未读到任何运行时切换条件，哪条栈在真机渲染为未知。变化性质上，home_legacy 类 +3 而外部边 −19、home_new_frame 类 +9 而边 −8，类数增、边数减的组合与 R8 改名/DEX 重排/重复包装层合并都相容，不能据此认定“出现新样式”，也不能排除代码迁移到共享实现后调用边被合并。home 侧协议登记为空（E003 protocols={}），而种子未登记协议中同时出现 HomeMoss、KHomeMoss、feed/v1 KFeedMoss 等，故首页数据协议层既无登记证据也无缺口清单闭合，模块对首页协议级 Hook 的覆盖不能由本单元证据推断。模块侧存在多个首页安装器与定位器源文件（HomeFrameListHook、HomeFrameTabLocator、HomeTopBarFeatureInstaller 等），但本单元未读取其实现，安装条件、候选唯一性、兜底行为均记为未知，仅能标注 module_coverage 需安装器复核。结论：两条首页路径都必须分别真机验证，重点确认旧/新栈的实际挂载、模块安装日志中的定位候选，以及服务端开关是否只切换视觉而无可静态观测的结构差异。

证据：E000, E003, E015

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 785（基线 782）、外部调用边 184（基线 203）、compose_methods 88 未变、指纹 61d12f32…→08b1d49a… 变化；E015 抽样仍见 HomeFragmentV2/StartupFragmentV2，旧原生栈仍存在。
- 可能影响：类数增而调用边减，可能是混淆改名/DEX 重排或调用被合并到共享层；若模块按类名/字段形状定位首页旧栈，候选集变化可能使定位落空或命中不同类，实际安装结果未知。
- 验证：在 9180100 与 9180200 上分别运行模块，抓首页旧栈安装日志与反射定位结果（解析到的类、字段、方法签名），对比两份类名集合在 tv.danmaku.bili.ui.main2 前缀下的差异；真机确认旧 Fragment 栈是否仍被实际挂载。
- 证据：E003, E015

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类 199（基线 190）、外部调用边 46（基线 54）、compose_methods 33 未变、指纹 1bef27c7…→c2fe89cd… 变化；无协议登记。
- 可能影响：新框架家族规模小、外部边减少 8 条，可能是新框架与旧栈共享实现后的边合并，也可能是重排；若有独立的新框架安装器，候选唯一性前提需重新确认，本单元未读其源码故不作覆盖结论。
- 验证：离线对拍两版本 home_new_frame 家族类名与方法体哈希，标记新增/消失类；真机用 Activity/View 层 dump 判断新框架是否承载首页主体；记录服务端开关或实验位对渲染路径的影响。
- 证据：E003, E015

### search

search 两条路径规模差异很大：search_native 1695 类、2913 条外部调用边、仅 2 个 compose 方法，属典型原生 View 搜索栈；search_compose 3152 类、562 个 compose 方法，但 E016 抽样（Lkntr/app/search/B、D 持有 androidx.compose.runtime.State 字段）与 E017 调用者（kntr/app/search/repository/p、aggregate/repository/b、comic/repository/b）共同表明该家族同时包含 Compose UI 与数据仓库层，家族标签不等于“纯 UI 样式”，跨家族消费者确实存在。变化形态为 search_native 类 −9 但边 +48、search_compose 类 +21 但边 −3，compose 方法数两侧均未变，搜索两条 Moss 协议定义与边完全未变（E004/E017），因此协议面稳定而宿主类集合被重排，属于“结构或调用路径变化，样式未确认”。模块侧搜索协议解析以 Kotlin/Java Moss 通道为主，实际调用边 18/22 条分布在仓库层，说明协议 Hook 的命中点更可能落在数据层而非 Compose 组合函数；本单元未读取 SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 等实现，其安装条件、兜底路径记为未知。另外搜索有三类未登记协议（app/search/v2/SearchMoss、broadcast/message/search/SearchMoss、interfaces/v1/SearchMoss），登记表不能代表搜索协议全貌。结论：两条路径分别需真机验证，且 search_compose 侧的定位器唯一性风险须优先排查。

证据：E000, E004, E016, E017

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类 1695（基线 1704，减 9）、外部调用边 2913（基线 2865，增 48）、compose_methods 2 未变、指纹 433d4628…→27b995a5… 变化。
- 可能影响：类减少而调用边增加 48，提示出现新的委托/包装层或调用点迁移；模块搜索净化若按精确方法签名 Hook，可能漏掉新增调用点，是否生效未知。
- 验证：对拍两版本的搜索调用边集合（owner/callee 签名），列出新增 48 条边所属包；在 9180200 真机上打开搜索页与默认搜索词净化，抓 Hook 命中日志确认新增边是否经过模块挂载点。
- 证据：E004, E017

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类 3152（基线 3131，增 21）、外部调用边 614（基线 617，减 3）、compose_methods 562 未变、指纹 f6d999cc…→8cf08a20… 变化；E016 抽样类持有 androidx.compose.runtime.State，E017 显示 kntr/app/search 仓库类属本家族并直接调用 KSearchMoss。
- 可能影响：SearchHomeRecommendLocator（E018）要求 discover 根类、data 状态类与投递宿主各自 singleOrNull，本族类 +21 可能引入第二个候选而使定位返回 null 并静默不 Hook；家族同时承载数据层，协议边稳定不代表 UI 路径稳定。
- 验证：用模块自身定位器在 9180100/9180200 两版安装期执行，打印 Points.deliveryCandidateCount、delivery/state 是否为 null 及解析到的字段名；对 discover 与 search2.main.data 命名空间做全量类枚举对拍，确认是否存在 singleOrNull 之外的候选或多字符嵌套后缀类。
- 证据：E004, E016, E018

### detail

详情页三条路径并存格局未变，但性质不同。detail_legacy 在目标与基线都是 0 类、0 Compose、0 外部调用边，指纹为同一个空集哈希 4f53cda1…，只能判 absent——静态矩阵未见该家族命中，不能推出旧原生详情实现已删除或页面功能消失；也可能是当前指纹口径未覆盖该栈的类名形态。detail_theseus_ugc 1973→1975 类、Compose 25→25、外部调用边 525→522，细节上是 +2 类/-3 边；detail_theseus_united 4679→4669 类、Compose 98→98、边 4180→4193，为 -10 类/+13 边；两者指纹均变。类数与 Compose 方法数几乎不动、仅边数小幅抖动，符合混淆改名、DEX 重排与调用点内联/迁移，不能证明出现新样式；但 -10 类可能是真实删除的模块，需按类名与方法体哈希定位。协议侧 detail_java_moss 32 定义/35 边、detail_kotlin_moss 76 定义/34 边两版逐项相同，说明未观测到协议层新增或改签名消费者；仍不能据边数推导覆盖率，接口分发与反射调用不可见。模块侧 DetailAppPromotionFeatureInstaller、DetailModulePurifyFeatureInstaller/Policy、DetailUnitedModulePurify*/DetailUnitedPresentationPurify*、DetailViewPurify*、HomeVerticalDetail* 在快照中只出现文件名与路径，未读取其定位器与安装条件，所以任何 Hook 是否命中 detail 家族均为未知；且快照 working_tree_dirty=true，需按文件哈希追溯。另一处需注意的静态事实：评论 Compose 家族本次深挖观测到 2528 类/288 Compose 方法/1115 外部调用边（E011），而模块侧 CommentComposeViewAccess 通过 AndroidCompositionLocals_androidKt.getLocalView + CompositionLocal.consume 在安装期解析宿主 Compose ABI，解析失败被 runCatching 吞掉返回 null（E013）——一旦宿主 Compose 版本变动，详情页评论区相关 Hook 可能静默不安装而无日志。

证据：E000, E005, E011, E012, E013

#### 路径：detail_legacy

- 状态：absent
- 变化：目标与基线均为 classes=0、compose_methods=0、external_invoke_edges=0，指纹同为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945（空集哈希），无结构变化。
- 可能影响：detail_legacy 在静态矩阵中不可见，DetailViewPurifyFeatureInstaller 等以 legacy 类为锚点的 Hook 是否存在可解析目标无法从静态证据判断；不得据此推断旧原生详情页已下线或功能消失。
- 验证：真机进入普通视频详情页后 dump 当前 Activity/Fragment 全限定名与类加载器来源，比对 DetailViewPurifyFeatureInstaller 定位器在安装期的解析日志（命中/未命中/回退），并按文件哈希记录所用模块版本。
- 证据：E000, E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：classes 1973→1975(+2)、compose_methods 25→25、external_invoke_edges 525→522(-3)，指纹由 ed2491aa… 变为 5e32fd5a…。增量极小且 Compose 方法数不变，与混淆改名/DEX 重排/调用点迁移一致。
- 可能影响：UGC 详情栈仍是主命中家族，但 -3 条调用边的归属未知；若被移除的边位于模块定位器所依赖的方法体上，UGC 详情净化/推广 Hook 会静默不生效。深挖同页可见 kntr/app/following/opusDetail/api 家族样本含 CompositeExternalInterceptor 及其 handleAdClick 回调类（E012），提示 Opus 详情存在独立的广告点击旁路，模块是否覆盖未读源码不能判定。
- 验证：用 JADX 对 9180200 与 9180100 分别导出 detail_theseus_ugc 类名+方法体哈希做 diff，定位 +2/-3/-10 的具体类与方法；再读 DetailAppPromotionFeatureInstaller 与 DetailModulePurifyPolicy 的锚点方法名，逐个核对是否仍存在于目标类；真机在 UGC 详情页与 Opus 详情页各打一次 Hook 安装日志。
- 证据：E000, E005, E012

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：classes 4679→4669(-10)、compose_methods 98→98、external_invoke_edges 4180→4193(+13)，指纹由 cce82b5d… 变为 c6cbf881…。总量基本守恒，仅边数微增，倾向重排而非新样式。
- 可能影响：united 栈的模块净化/展示净化策略（DetailUnitedModulePurifyPolicy、DetailUnitedPresentationPurifyPolicy）若按类名或方法签名定位，-10 个类可能正好包含被净化对象或定位锚点；反之若消失类为无关适配层则无影响，两种可能静态无法区分。
- 验证：按 method_bodies_sha256 对两版 united 家族做类级 diff，列出消失的 10 个类与其调用者；再用 decompile_class 读 DetailUnitedModulePurifyPolicy 引用的类名常量，检查是否落在消失集合内；真机在 united 详情页验证净化项是否仍生效。
- 证据：E000, E005

### pgc

PGC 页登记两条路径，两侧都是 static_invoke_observed，没有 absent。变化方向相反是本次最值得注意的静态信号：pgc_legacy 由 345 类/301 外部调用边升到 357 类/307 边（+12 类/+6 边），指纹 14717f3a… → e0071b25…；pgc_theseus 由 2258 类/134 Compose 方法/982 边降到 2255 类/132 Compose/913 边（-3 类/-2 Compose/-69 边），指纹 b9f79e23… → 53ca22f6…。legacy 扩张加 theseus 外部调用边大幅收缩，作为候选符合“重心从 theseus 栈向 legacy 栈迁移”，但同量级的另一解释是 R8 内联、方法合并或 DEX 重排导致边数减少，以及新增类属于无关适配层；不读到实际运行条件前不能宣称栈切换已发生。协议侧 pgc_player_moss 12 定义/3 实际调用边、pgc_view_moss 14 定义/7 边，两版完全相同，说明未观测到协议定义或消费者变动，-69 条边未落在或未被解析到这两个协议上；定义数与边数不同单位，不能相除求覆盖率，只有 3 与 7 条静态边也不代表播放/视图协议只在少数路径使用。模块侧 PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupFeatureInstaller/Policy 在快照中仅有文件名，未读取其 Activity/Popup 定位口径与兜底顺序，因此无法判断自动弹窗 Hook 命中 legacy 还是 theseus 弹层，也无法判断缩容后是否有锚点丢失。宽屏/平板分支与服务端开关均未在静态证据中出现，属未知。运行期启用状态全部 unknown，module_coverage 均 requires_installer_review。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：classes 345→357(+12)、compose_methods 0→0、external_invoke_edges 301→307(+6)，指纹 14717f3a20ad3f0f0f1b911c241725b89e2683fb5aeed1f027ac94c989422b45 → e0071b256a080f8257efcefee37c5865e4f5cbba97d12bac472f3ecd43e7d8f8。新增 12 个类未见 Compose 方法，属 View/Java 侧结构。
- 可能影响：legacy 栈类数增加可能引入新的番剧详情/播放承载页或弹层承载类，使 PgcAutoActivityPopupFeatureInstaller 的定位目标发生位移；若新类为同名族复制品，Hook 可能挂到未启用的一份上，表现为净化或弹窗拦截失效而非报错。
- 验证：按类名与 method_bodies_sha256 列出 9180200 相对基线新增的 12 个 legacy 类及其调用者，用 decompile_class 查看是否为 Activity/Dialog/Popup 子类；再读 PgcAutoActivityPopupLocator 的候选枚举与优先级，检查新增类是否落在其候选集合外；真机进入番剧详情与播放页记录实际 Activity 栈与 Hook 日志。
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：classes 2258→2255(-3)、compose_methods 134→132(-2)、external_invoke_edges 982→913(-69)，指纹 b9f79e234a1a559255a8d68b938b8f28694196efd6f1b1119f5add8e7171540f → 53ca22f650ba83f89406df6016def0a18c8193b0ff408e14556c8f64cdd5bdb8。类数与 Compose 方法数变化很小而外部调用边减少约 7%，两条协议的 12/3 与 14/7 计数两版一致。
- 可能影响：theseus 栈外部调用边收缩可能意味着部分 Compose/View 呈现路径被合并或下线；若模块以 theseus 类或方法为锚点（净化、弹窗拦截），锚点可能已迁移，Hook 会静默失效。反向影响是若实际运行已切到 legacy，则针对 theseus 的验证与修复投入无收益。
- 验证：导出两版 pgc_theseus 的调用边清单（调用者类+方法+被调签名）做集合差，明确 -69 边的来源模块与是否被内联；用 protocol_evidence 复核 pgc_view_moss/pgc_player_moss 的调用者是否两版一致；真机在番剧详情、播放页与自动弹窗场景各采集一次栈与模块 Hook 安装日志，判定实际生效栈。
- 证据：E000, E006

### player

事实（E007）：player_java 类数 953→954（+1）、外部调用边 3300→3305（+5）、compose_methods 仍为 0，指纹 9721f66…→746cdb8…；player_kotlin 类数 480→466（−14）、compose_methods 37→37、边 891→897（+6），指纹 9c22f38…→f314119…；两条 MOSS 协议的定义数与调用边数两侧完全一致（player_java_moss 18/2、player_kotlin_moss 34/3），协议层未见新增或消失的调用关系。E000 将 player_java、player_kotlin 均标为 structure_or_call_path_changed。推断：java 侧 +1 类不足以吸收 kotlin 侧 −14 类，说明 Kotlin 实现可能被合并进其他层、迁移或在打包中被裁剪；但边数总量微增、协议边界不变，也完全符合 R8 改名池收缩与 DEX 重排的表现，因此不能据此认定播放器出现新样式或功能缺失。模块侧未读到 player 定位器（PlayerBufferLocator、PlayerSpeedLocator、PlayerCapabilityAccess、SponsorPlayerLocator 等）本体，其安装期解析结果、平板/宽屏分支、服务端开关与兜底行为一律未知；只能确认 prefetch 标注 module_coverage=requires_installer_review、complete_coverage=false。真机是否启用、Hook 是否生效均未验证，不得表述为通过。建议把类级清单与方法体哈希对齐作为首要补证，其次抓安装期定位日志与播放页 Hook 回调计数。

证据：E007, E000, E013

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类数 953→954（+1），外部调用边 3300→3305（+5），compose_methods 恒为 0，结构指纹 9721f66…→746cdb8…；对应 player_java_moss 定义 18、调用边 2 两侧不变。
- 可能影响：若为真实增删，MOSS 调用点或定位器候选会位移，缓冲/倍速/画质/赞助商等安装期反射解析可能失配；也可能仅由混淆改名与 DEX 重排导致，暂无调用边证据说明语义变化。
- 验证：对 9180200 与 9180100 做 player_java 类级清单与方法体 sha256 对齐；在真机安装期日志中核对各 player 定位器的解析命中/返回 null；统计播放页 Hook 回调次数并与基线对比；覆盖平板与宽屏入口。
- 证据：E007, E000

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数 480→466（−14），compose_methods 37→37，外部调用边 891→897（+6），指纹 9c22f38…→f314119…；player_kotlin_moss 定义 34、调用边 3 两侧不变。
- 可能影响：Kotlin 侧实现类减少而协议不变，可能意味着实现被合并/迁移或裁剪；依赖具体类名与签名的 Hook 点存在失配风险，但无证据表明 Compose 渲染路径数量变化（compose_methods 不变）。
- 验证：按方法体哈希把 466 个类与基线 480 个类做双向差集，确认缺失的 14 类是被重命名、内联还是删除；真机分别验证播放器主界面与浮层 Hook 日志；检查是否存在残留旧类名兜底路径。
- 证据：E007, E000

### danmaku

事实（E008）：danmaku_kotlin 在两侧均为 137 类、3 个 Compose 方法、164 条外部调用边，五项计数完全一致，但结构指纹由 97cb0f1… 变为 b65c81e…；danmaku_java_moss 22 定义/20 边与 danmaku_kotlin_moss 46 定义/12 边两侧完全一致；danmaku_legacy 在目标与基线均为 0 类、0 边，指纹为 4f53cda…（空集哈希），evidence 值为 absent。推断：计数不变而指纹变化的解释首先是 R8 改名、DEX 重排或编译器差异，因为哈希不同也允许少量类替换恰好抵消计数，所以仍需类级对齐才能定论；absent 只说明该家族在本次归类口径下无类命中，不能推出旧原生弹幕页功能消失。另需注意跨家族消费者：E000 的 unregistered_protocols 含 com.bapis.bilibili.live.approom.api.grpc.v1.KDanmuMoss 等直播弹幕相关协议，直播与点播弹幕若共用净化策略，其消费者不在本页四家族静态矩阵内，属未登记覆盖缺口，而非确认新增样式。DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 源码本次未读到安装条件与过滤回调实现，服务器 A/B 与开关条件均未知；runtime_enabled 全部 unknown、complete_coverage=false，不得判定弹幕净化已适配。

证据：E008, E000

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线均为 0 类、0 Compose 方法、0 外部边，指纹同为 4f53cda…（空集哈希），本次配对中无增量变化。
- 可能影响：该家族无静态命中，可能表示旧原生弹幕实现已在此前版本移除，也可能只是本仓库的家族归类口径不再匹配；若旧路径在真机仍可达，则弹幕净化缺少静态落点。
- 验证：对 base.apk 按已知旧弹幕类名与包前缀做离线字符串/类检索确认是否确实无该类；在真机分别进入旧版播放器入口与新版播放器入口，记录弹幕渲染组件与净化回调是否被调用。
- 证据：E008, E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类数 137、compose_methods 3、外部调用边 164 与基线完全一致，但结构指纹 97cb0f1…→b65c81e…；danmaku_kotlin_moss 46 定义/12 边不变。
- 可能影响：目前无证据表明样式或家族结构变化；若指纹变化仅来自混淆改名与 DEX 重排，则 Hook 落点语义可保持不变，但依赖类名的弹幕净化定位器仍需安装器期确认，不能以计数相同代替覆盖结论。
- 验证：将 137 个类逐类方法体 sha256 与基线对齐，按差集判定是重命名还是实现替换；在真机打开弹幕开关，记录 DanmakuPurify 安装期解析结果与过滤命中计数；对照屏蔽前后弹幕条数确认策略实际生效。
- 证据：E008, E000

### story

story 页登记两条家族路径。story_native 在目标包中仍有 2969 类、45 个 Compose 方法、1419 条外部调用边，静态调用存在，但类数比基线少 5、边数少 51，指纹由 28025f3f… 变为 a5c8e67f…；compose_methods 两版同为 45，说明 Compose 侧方法数量口径未变，减少集中在普通类与调用边，更符合混淆改名、DEX 重排、封装层合并或少量代码迁移，尚不能判定为新样式或旧样式下线（E009）。story_kotlin 两侧均为 0 类、0 Compose 方法、0 边、指纹为空态 4f53cda1…，该家族在 9.18.0 静态不可见，absent 仅表示本家族抽取窗口内无类，不等于页面 Kotlin 实现不存在，其它已登记家族可能在承载同一页面（E009）。两路径 runtime_enabled 均为 unknown，module_coverage 为 requires_installer_review，源文件清单中的 StoryActionIconsFeatureInstaller/StoryPurifyFeatureInstaller/HomeVerticalDetailFeatureInstaller 本轮未读取，故无法确认模块在 story 路径上的定位器命中与兜底逻辑。附带说明：动态/Opus 相关实现作为独立家族存在（E012，深挖动态 Opus 家族样本），提示 story 区域可能存在跨家族消费者，但该证据不指向 story_native 本身，不能据此推断 story 的 Hook 覆盖。

证据：E009, E012, E000

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类数 2969←2974、外部调用边 1419←1470 均下降，compose_methods 恒为 45，指纹由 28025f3f… 变为 a5c8e67f…，登记为 structure_or_call_path_changed（E009）。
- 可能影响：若减少来自混淆改名/DEX 重排，则模块按类名或签名解析的入口可能解析失败而落入兜底；若来自代码迁移，则原 Hook 点可能迁至未登记家族，功能表现为部分项失效。当前无安装器命中证据，具体影响未知（E009）。
- 验证：对同一 family 名分别取 target/baseline 的完整类清单做差集，先剔除同方法体哈希的改名对，再看剩余缺失类是否被其它家族收录；随后核对 StoryActionIconsFeatureInstaller/StoryPurifyFeatureInstaller 的定位器候选与安装期日志（E009）。
- 证据：E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧均为 0 类、0 Compose 方法、0 外部调用边，指纹为空态 4f53cda1…，无结构变化可比（E009）。
- 可能影响：本家族在本轮抽取窗口内无静态调用边，模块若依赖该家族名做定位则无对象可挂；是否会话期由其它家族承载同一 UI 未知（E009）。
- 验证：确认抽取规则对该家族的类名前缀/包名覆盖是否生效（可用已知有类的前缀反证抽取未失效），并在真机 story 页抓取类加载与方法调用日志确认是否存在同名 Kotlin 实现（E009）。
- 证据：E009

### mine

mine 页登记 mine_native 与 mine_account_model 两条路径，均为 static_invoke_observed，runtime_enabled unknown，module_coverage 为 requires_installer_review（E010）。mine_native：327←326 类，+1 类；compose_methods 7 与外部调用边 94 完全不变，指纹 96810670… → a259ab51…，单类增减不足以说明样式变化，需排除内部类/合成类随混淆池调整而新增的可能（E010）。mine_account_model：132 类、43 边、0 Compose 方法两侧完全一致，仅指纹 abd9520a… → 91335afb… 变化，类数与边数同口径相等时指纹变化最典型的解释是方法体常量/顺序或 DEX 重排，而非新样式；但指纹算法若含调试信息或字符串池则改名也会造成同类情况，需进一步比对方法体哈希集合才能定性（E010）。源文件清单中包含 MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineComponentSnapshotStore/QueryClient/QueryContract、MineVipFeatureInstaller 与 HostMineReadingCard，说明 mine 页存在组件过滤、VIP 展示与快照协议多条互相独立的模块入口，本轮均未读取源码，因此不能判断上述结构差异是否触及实际 Hook 点（E010）。

证据：E010, E000

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类数 327←326（+1），外部调用边 94 与方法数口径（compose_methods 7）不变，指纹 96810670… → a259ab51…，登记为 structure_or_call_path_changed（E010）。
- 可能影响：单类增减可能只是混淆池或合成类变化，未必影响模块定位；但若新增类为组件过滤/挂载宿主的新包装层，则按旧结构解析的 Hook 可能漏挂，行为表现为个别卡片样式或过滤不生效（E010）。
- 验证：取 target 与 baseline 的 mine_native 类清单做差集，定位新增的 1 个类的父类、方法签名与调用方，判断是包装层还是真实新实现；再比对方法体哈希确认其余 326 类是否仅改名（E010）。
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数 132、外部调用边 43、compose_methods 0 与基线完全一致，仅指纹 abd9520a… → 91335afb… 变化（E010）。
- 可能影响：数量相同的结构变化更可能来自改名、常量或 DEX 重排，对模块的字段/方法名反射解析影响取决于具体符号是否被改；若模块依赖字符串常量或枚举值，仍可能静默失配，当前未知（E010）。
- 验证：对比两版 132 个类的方法体哈希集合与方法/字段名集合，区分“仅改名”与“逻辑改动”；并在真机 mine 页核对账号模型相关展示（VIP/等级/统计）与快照查询是否返回预期字段（E010）。
- 证据：E010

### F001：comment_compose 结构变动需对照模块 Compose 侧多处硬编码短名定位器逐点核验
事实：comment_compose 类数 2501→2528（+27）、compose_methods 289→288、external_invoke_edges 1142→1115（-27）、指纹 9c77cdf…→67e96ff…，evidence 仍为 static_invoke_observed，runtime_enabled=unknown（E001/E019/E011）。模块侧本轮实读三份源码：CommentComposeViewAccess.resolve 只反射 androidx.compose.ui.platform.AndroidCompositionLocals_androidKt#getLocalView 与 androidx.compose.runtime.Composer#consume(CompositionLocal)，全部包在 runCatching{}.getOrNull()，失败返回 null（E013）；CommentComposeCopyBridge 另有一整套混淆短名依赖——ComposeCommentText 按字段名 a(Long)/i(枚举且枚举值恰为 ORIGIN/TRANSLATING/TRANSLATION)/j/k/o/p/b/c 解析正文与 id，并需 RENDERER、ACTION、SOURCE 三个类名与 ACTION 内部类唯一匹配，任一不满足即 FeatureInstallResult.Skipped 并 logError（E021）；CommentComposePurifyBridge 依赖 kntr.common.comment.card.model.comment.CommentModel、CommentVoteRenderer、CommentUserInfoRendererModel 的 $a..$d 四槽装饰、构造函数参数序以及 kntr.common.comment.card.store.CardStore 与 a..z 枚举，失败同样 Skpped/logError（E022，注：源码中为 Skipped）。推断（未验证）：因此该类数上升/调用边下降的组合不是风险定位依据，真正会被 DEX 重排或再混淆打破的是上述硬编码短名与类名；这些点彼此独立，表现为某一能力单独缺失而非全部同时失效，且失败默认保留宿主原行为、仅在日志中留痕。待真机验证：resolve 是否返回非空、Copy/Purify 各 install 的 Installed/Skipped 与 hookCount。
反例与替代解释：若真机四组定位全部命中且 installed==expected，则本次 comment_compose 指纹变化可归因为 DEX 重排或再混淆但短名未变，本条降级为无适配影响；若 resolve 命中而 Copy/Purify 的 expected 变大或某个能力 Skipped，则问题在桥接注册表而非 Compose ABI；若 resolve 为 null，则需反编译 9180200 中 androidx.compose 相关类确认 getLocalView/Composer.consume 的签名与重载是否变化。反之，若所有定位都命中且 hookCount 无异常，仍不能宣称页面适配通过，因为 runtime_enabled 仍为 unknown。
建议：在 9180200 真机安装期记录四组定位结果：(1) CommentComposeViewAccess.resolve 是否为 null（null 时打印缺失符号名）；(2) CommentComposeCopyBridge 的 ComposeCommentText.resolve 与 RENDERER/ACTION/SOURCE 解析结果、renderInstalled/renderExpected 计数；(3) CommentComposePurifyBridge 的 VOTE/FOLLOW/QUICK 三项 outcome(installed, expected) 及 missing-compose-structure 日志；(4) 对 9180100/9180200 做 kntr.common.comment 下类名与字段名差集，重点看 a/i/j/k/o/p/b/c 与 $a..$d 槽位是否改名。只有定位全部命中且 hookCount 与 installable 面一致，才能把本次指纹变化归为 DEX 重排/混淆改名。
证据：E001, E011, E013, E019, E021, E022

### F002：Kotlin MOSS 定义/调用边缺口是两版共有的测量口径未解状态，不是 9180200 的变化，且评论与动态都可能存在未解析消费者
事实：comment_kotlin_moss 定义 130、实际调用边 23；comment_java_moss 定义 50、调用边 50；dynamic_kotlin_moss 定义 382、调用边 27；dynamic_java_moss 定义 134、调用边 134（E001/E002）。这四组数字在基线 9180100 与目标 9180200 逐项相同（E019/E020），即该缺口并非本版结构变化的结果，而是静态调用解析对 Kotlin 通道（接口实现、invoke-custom/lambda、跨 DEX dispatch）口径未解时的既有形态。另未登记协议清单中 DynamicMoss、KOpusMoss、OpusMoss、mall/tab3/dynamic/v1/OpusMoss、FeedMoss/KFeedMoss、ReplyMoss/KReplyMoss 等成组出现（E000），按登记口径它们只是调查候选而非已确认漏挂路径。推断（未验证）：Kotlin MOSS 的消费者可能经接口或 lambda 进入，静态矩阵无法区分“未被调用”与“调用边未被解析”，因此 130/382 不能当作实现规模，23/27 不能当作覆盖数，也不能据此断言评论回复或动态净化有实际漏挂。受限点：本轮仍未读取 KotlinMossChannel.kt / KotlinMossReplyBridge.kt（在 source 快照的 unmapped_multi_path_candidates 中），不得推测其注册表覆盖；本条为候选而非已确认风险。
反例与替代解释：若差额定义全部属后台/旁路协议或调用边解析器对 invoke-custom/lambda 形态失明，则缺口是测量口径问题而非覆盖漏洞；若差额中有定义被评论回复或动态卡片链路引用却未注册，则构成真实的未覆盖消费者，需要在模块侧补挂并另立发现；两版计数相同这一点也支持“与本次版本升级无关”的解释，但不足以排除既有漏挂。
建议：最小补证任务：(1) 按文件哈希读取 KotlinMossChannel.kt 与 KotlinMossReplyBridge.kt，列出注册表逐条目标（类名+方法签名）与安装条件；(2) 对 comment_kotlin_moss 130 条定义、dynamic_kotlin_moss 382 条定义做“是否有代码引用其类型/方法”的类级回溯（含接口实现与 lambda 生成类），把 23/27 之外的差额分为“有引用但边未解析”“无引用（死定义）”两类；(3) 在真机安装日志中核对注册表条目是否被安装、是否命中。所有结论以运行时安装日志为准，不以静态计数代替。
证据：E000, E001, E002, E019, E020

### F003：dynamic_opus 收缩需在 AdditionalType 常量读取点核验 DynamicPurifyPolicy 的数值兜底是否掩盖符号变化
事实：dynamic_opus 类数 1370→1349（-21）、external_invoke_edges 227→224（-3）、compose_methods 95→95、指纹 72569a3…→e50b06c…，evidence=static_invoke_observed，runtime_enabled=unknown（E002/E020）。深挖样本（E012）仅覆盖 5/1349 类，形态为 kntr/app/following/opusDetail/api 下的数据类、Comparator 与 CompositeExternalInterceptor$firstSnapshotFile$1/$handleAdClick$1 协程续体，未见新界面族特征；该样本量不足以代表全族，也不能用于判断 21 个消失类的下落。模块侧实读 DynamicPurifyPolicy.kt（sha256 e76741e1…，E014）：判定优先读宿主 AdditionalType 上的 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE，读不到才用 FALLBACK_PROMOTION_ADDITIONAL_TYPES={2,6}；关键词按文本片段逐段匹配；文档注释写明“读取失败一律保守放行；只有明确命中某条判据才删除”。注意 Signals 中 promotion 与 lockedChargeOnly 是非空 Boolean 且默认 false，只有 authorName/authorMid 为可空，因此在 Signals 层“没读到”与“确实为 false”不可区分。推断（未验证）：若 opus/动态卡片结构调整改了 AdditionalType 常量名或旁路了读取入口，净化会静默走数值兜底或直接放行，表现为“看起来没生效/漏删”，而不是误删；dynamic_legacy +19 类与 dynamic_compose -17 边提示三栈入口在重排，单看 opus 一路不足以定论。
反例与替代解释：若真机显示常量按原名可读、命中卡片数与 9180100 同场景一致，则 -21 类可归因为 DEX 重排/包结构调整，本条降级；若常量读不到但净化仍靠 {2,6} 命中部分卡片，说明兜底掩盖了符号漂移，需单独记录为潜在漂移并补齐字段名映射；若常量可读但某类卡片始终不命中，则问题更可能在卡片的 AdditionalType 取值本身变化，而非模块判定层。
建议：把验证点定在构造 Signals 的上游读取处而不是 Signals 字段：真机在动态流与 Opus 详情分别 hook AdditionalType 常量反射的调用点，记录常量是否按原名取到、取到值与实际命中卡片数，并区分“读不到→走 {2,6} 兜底”和“读到且非推广”两种情形；同时抓附加类型枚举的字段名清单，与两版差集比对，判断是否改名。另需对 21 个消失类做 kntr/app/following/opusDetail/api 及相关包的类名差集，确认迁移去向（含是否流入未登记的 OpusMoss/KOpusMoss 消费者，后者仅作调查候选）。
证据：E002, E012, E014, E020

### F004：搜索首页推荐定位器把“候选唯一”当硬前提，9.18.0 类集合重排可能让它静默不 Hook
事实（E018，文件 sha256 1c569369…，脏工作树快照）：SearchHomeRecommendLocator.locate 依赖 com.bilibili.search2.api.SearchSquareType.getType():String，按 discover.a..discover.z 加 SearchDiscoverViewModel 作为根类，再以 NESTED_SUFFIXES=('a'..'z')+('0'..'9') 单字符后缀加 declaredClasses 枚举投递宿主；delivery() 要求 getHistoryList 存在、接收方法唯一（typedList 的 List<SearchSquareType>）、refresh 可选唯一、carrier 字段唯一；state() 要求 search2.main.data.a..z 中存在唯一的 square 字段与匹配构造器；discoveryCache 再要求 payload 字段、NegativeFeedback 字段、构造器（3 或 5 参）、getValue/setValue 均唯一。locate 全程 runCatching 包裹，任一环节失配即返回 null 或使 delivery/state 为 null，而 deliveryCandidateCount 仅作记录“不参与功能判定”。静态侧目标版本 search_compose 类 3152（基线 3131，+21）、search_native 1695（1704，−9），search_compose 指纹与外部边均变化（E004/E016），说明宿主类集合被重排。推断：类集合被重排时，discover/data 命名空间候选数一旦从 1 变 2，singleOrNull 即失配，功能以“无异常、无日志”的方式不生效；若新增嵌套类使用 R8 双字符后缀（$aa），单字符后缀枚举根本发现不了该类，属漏发现而非歧义。反例：本单元没有 9180200 上 Points 的运行值，也没有证据表明候选数已变；类计数增减完全可由混淆池改名解释，此时定位器仍唯一命中。验证：在 9180100/9180200 两版安装期分别 dump Points（deliveryCandidateCount、delivery/state 是否为 null、解析到的字段名）并对比；对 discover 与 search2.main.data 做全量类名导出，检查是否存在第二个符合形态的宿主或双字符嵌套类；真机开搜索首页推荐净化，前后对比 discover 卡片是否出现。
反例与替代解释：可推翻当前推断的证据：①9180200 上 deliveryCandidateCount==1 且 delivery/state 均非 null，说明候选仍唯一，退化风险不成立；②对拍显示 discover/data 类只是被改名/迁移到其他包，属实现迁移而非候选歧义，应重写定位规则而不是加兜底；③若 search2.discover 整体被新框架取代、旧类仅作为死代码保留，则静态可见结构变化与线上页面无关，需以真机渲染路径为准。
建议：把 deliveryCandidateCount 与各 singleOrNull 失配原因提升为安装期可见日志（含候选二进制名），先在两版上取得对比数据；若确认为候选歧义则按类型/泛型形状而非“唯一”做选择并保留歧义时禁用；若为双字符嵌套后缀漏发现，将有界枚举扩展为 aa..zz 与静态探测口径一致，再进真机验证。
证据：E018, E016, E004

### F005：首页两套栈指纹同时变化但方向相反（类增、边减），只能记为结构重排候选
事实：home_legacy 类 785（基线 782）、外部调用边 184（基线 203）、compose_methods 88 未变，指纹 08b1d49a…→61d12f32…；home_new_frame 类 199（基线 190）、外部调用边 46（基线 54）、compose_methods 33 未变，指纹 c2fe89cd…→1bef27c7…（E003）。E015 目标侧有界摘录确认 Ltv/danmaku/bili/ui/main2/ 前缀类仍存在（如持有 HomeFragmentV2 类型字段的 ui/main2/A;、AccountMineRequestResource 枚举），说明旧原生首页栈类未被删除、两栈并存；草稿提到的 StartupFragmentV2 未在本次摘录中出现，需按名重读后再引用，不作为本项证据。推断：类数增加而外部调用边减少，与 R8 改名、DEX 重排、调用被合并进新的包装层、合成类（lambda/默认参数桥）增减、或逻辑迁移到共享实现都相容；方法定义数与调用边数不是同一单位，不能用 184/203 之类比值推算覆盖率或“适配损失比例”。home 侧协议登记为空（E003 protocols={}），而种子未登记清单含 HomeMoss、KHomeMoss、feed KFeedMoss，故首页协议层既无登记证据也无可穷尽缺口清单，不能以空协议表推出“首页协议无变化”。影响面只能限定为：以类/字段形状定位首页的安装器需重新确认候选；HomeFrameListHook、HomeFrameTabLocator、HomeTopBarFeatureInstaller 等源码本轮未读，安装条件、候选唯一性与兜底行为属未知，不能推断 Hook 覆盖。验证：双版本按 tv.danmaku.bili.ui.main2 与 home_new_frame 家族做类名集合+方法体哈希对拍，标记新增/消失/合成类；两版真机抓安装期定位日志；用 View/Activity dump 判断实际挂载栈，并记录服务端开关与宽屏/平板分支。
反例与替代解释：可推翻当前推断的证据：①对拍显示新增类全是混淆池改名或合成类（如 -$$Lambda、Kotlin 默认参数桥），则指纹变化不代表新样式；②若旧栈类虽在但首页 Activity 只挂新框架，home_legacy 的边减少只是死代码收缩，影响应下调；③若安装日志显示两族定位均唯一命中且真机净化行为与基线一致，则本项降为已复核的静态重排。
建议：先做双版本静态对拍（类名集合、方法体哈希、调用边 owner/callee 对）以区分“改名重排”与“结构新增”，再在 9180200 真机抓首页两条栈的安装日志确认候选；把 HomeMoss/KHomeMoss/feed 协议补登记或显式记为缺口，避免用空协议表当作无变化结论。
证据：E003, E015, E000

### F006：搜索协议层计数零变化，但实际消费者全在 search_compose 家族且存在未登记 SearchMoss
事实：search_java_moss 定义 24、实际调用边 22；search_kotlin_moss 定义 52、实际调用边 18，两侧在基线与目标完全相同（E004）。E017 目标侧 caller_samples（总边数 18，摘录仅示部分）显示 Lkntr/app/search/aggregate/repository/b; 直接构造 KSearchMoss 并调用 searchOGV，该仓库类按家族划分归属 search_compose；E016 同族抽样为持有 State/CoroutineScope 字段、仅含 invoke 的小类。推断：本轮静态可见的搜索协议接口面未变，说明这些 RPC 契约在 9.18.0 未被改动；但“协议未变”不能外推到 UI 路径——宿主侧变化（search_native −9 类/+48 边、search_compose +21 类/−3 边，E004）发生在家族内部，不体现在 Moss 边上；方法定义数与调用边数不同量纲，不可相除推覆盖率。证据边界：样本只覆盖 18 条 kotlin 边中的若干条，不能据此断言调用者全体属 search_compose；search_java_moss 的 22 条边调用者本轮未读到，其家族归属未知。登记缺口：种子未登记清单含 app/search/v2/KSearchMoss、broadcast/message/search/SearchMoss、interfaces/v1/SearchMoss（另有 broadcast/message/main 下两个 SearchMoss），模块是否消费这些家族在本单元无证据，不能宣称搜索协议 Hook 覆盖完整。影响：若净化按协议通道解析响应，命中点在数据层即可跨 UI 家族生效；若某入口改走未登记协议，静态不可见、运行时也不会命中。验证：枚举未登记 SearchMoss 家族的实际调用者并标注上游页面；按 tab（综合/番剧/漫画/OGV）真机开关净化，抓 KotlinMossChannel 与协议注入点日志，同时补齐 java_moss 调用者清单。
反例与替代解释：可推翻当前推断的证据：①若未登记的三个 SearchMoss 家族在 9180200 中无任何实际调用者（仅生成代码残留），则协议缺口无运行时意义；②若真机日志显示搜索净化只经由已登记的 kotlin/java Moss 通道生效且所有 tab 均命中，则本项应降级为登记表整洁问题；③若目标版本把搜索响应改由其他协议（如 polymer 或 broadcast）承载，则“协议未变”结论需整体复核。
建议：把未登记的搜索协议家族补入登记表或明确标注为不覆盖范围，并对每个家族列出实际消费者与上游页面；用真机按 tab 维度验证协议边命中，而不是以定义数/边数未变作为“搜索协议适配”的依据；对家族标签增加 UI 与数据层区分，避免把仓库类当作样式候选。
证据：E017, E016, E004, E000

### F007：详情页评论 Compose 视图定位为“静默失败”路径，宿主 Compose ABI 变动不会被发现
事实：detail 两栈均为 static_invoke_observed，detail_theseus_ugc 25 个 Compose 方法、detail_theseus_united 98 个 Compose 方法（E005）；同轮深挖显示评论 Compose 家族在目标包内 2528 类、288 Compose 方法、1115 条外部调用边（E011），说明详情页评论区确实存在成规模的 Compose 实现，而非仅有旧 View。模块侧 CommentComposeViewAccess.resolve 依次解析 androidx.compose.ui.platform.AndroidCompositionLocals_androidKt.getLocalView、CompositionLocal、Composer.consume 三个符号，任一为 null 就 return null，且整体包在 runCatching{}.getOrNull() 中（E013，sha256 d73672e5…），即宿主 Compose 升级或签名变化时不会抛错、不会留日志，只会让依赖该访问器的评论区 Hook 不安装。触发路径：详情页评论卡片渲染 → 需要从 Composer 读 LocalView → resolve 失败 → Hook 缺席 → 用户看到“模块没生效”但无崩溃、无日志。推断：这是本轮最容易被误判为“宿主样式变化导致适配失败”的静默缺口；但评论家族是否实际由 detail 页加载、以及外壳是否在安装期调用该 resolve，均未读到调用方源码，故不宣称 Hook 覆盖缺失，仅登记为候选。替代解释：resolve 用的是 Compose 稳定公开符号（LocalView/Composer.consume），跨版本可能长期不变；也可能是该访问器只服务于评论区内嵌子功能，对详情页主净化无影响。
反例与替代解释：若对 9180200 反编译显示 Composer.consume 与 getLocalView 签名与 9180100 完全一致，则 ABI 变动这一推断被推翻，问题只在调用侧；若静态找到 resolve 返回 null 后存在明确兜底分支，则“静默失效”降级为可恢复缺口；若真机日志显示评论区 Hook 正常安装生效，则本条候选不成立。
建议：复现与确认分三步：一，在真机详情页评论区触发一次目标 Hook，抓模块日志确认 CommentComposeViewAccess.resolve 的返回值（当前实现不打日志，需以只读方式在验证构建里加一行判定输出，勿改动工作树中的现有文件以满足追溯）；二，用 decompile_class 读目标包内 androidx.compose.runtime.Composer 是否存在 consume 方法、AndroidCompositionLocals_androidKt 是否存在 getLocalView，与基线 apk 对比签名；三，静态追一遍 CommentComposeViewAccess 的调用者，确认 resolve 为 null 时上层是否有兜底（例如退回 View 树遍历）。
证据：E011, E013, E005

### F008：PGC 两栈重心可能由 theseus 移向 legacy，弹窗定位器命中面未知
事实：pgc_legacy 类 345→357、外部调用边 301→307 上升，pgc_theseus 类 2258→2255、Compose 方法 134→132、外部调用边 982→913 明显下降，两侧指纹均变化（E006）；pgc_player_moss 12 定义/3 边与 pgc_view_moss 14 定义/7 边两版逐项不变，说明 -69 条边不在或未被静态解析到这两条协议上。推断：同一版本内 legacy 扩张而 theseus 收缩，符合 PGC 两条并存栈之间承载权重迁移的候选画像；这会直接改变 PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupFeatureInstaller/Policy 的命中对象——若模块候选集合仍偏向 theseus 类名（或反之只认 legacy Activity 短名），自动弹窗拦截会挂到一条用户实际看不到的栈上，表现为“模块无效果”且无异常。反例：边数减少同样可由 R8 内联、匿名类合并、DEX 重排造成，与栈切换无关；新增 12 个 legacy 类也可能是与 PGC 详情无关的公共适配层被归族。区分二者需要类/方法级 diff 与真机栈，不能靠总数相减。另需说明：定义数与调用边数不是同一单位，本条不使用任何“覆盖率”式推导；服务端 A/B 无结构变化时静态不可见，本页不排除尚有未穷尽样式。
反例与替代解释：若类级 diff 显示变化集中在混淆单字符类名重排、方法体哈希基本一致，则“重心迁移”推断被推翻，应按重排处理；若真机日志显示 PGC 详情与弹窗仍由 theseus 栈承载且定位器命中，则迁移候选不成立；若模块定位器的兜底分支已同时覆盖 legacy Activity 与 theseus Compose 弹层，则本条影响降级为验证项而非风险。
建议：最小补证任务：(1) 对 9180200 与 9180100 各导出 pgc_legacy/pgc_theseus 类名+方法体哈希，取交集差，定位 -69 边与 +12 类的归属包名；(2) decompile_class 读 PgcAutoActivityPopupLocator 的候选类名/父类判据与兜底顺序，逐个核对是否存在于目标包；(3) 真机进入番剧详情页并在自动弹窗场景复现，采集 Activity/Fragment 全限定名、弹窗类名与模块 Hook 安装日志，验证实际生效栈；(4) 平板/宽屏与未登录两种条件下重复一次，确认是否存在按屏宽或登录态切换的并存栈。
证据：E006, E000

### F009：player 两族计数小幅变动、Kotlin 族少 14 类而 MOSS 协议计数不变：类级对齐与安装器/真机验证均未完成
事实（E007）：player_java 类 953→954、外部调用边 3300→3305、compose_methods 两侧 0；player_kotlin 类 480→466、边 891→897、compose_methods 37→37；player_java_moss 18 定义/2 边、player_kotlin_moss 34 定义/3 边两侧完全一致。E000 标记 player_java、player_kotlin 为 structure_or_call_path_changed，两族 runtime_enabled=unknown、module_coverage=requires_installer_review、complete_coverage=false。口径限制：族按包前缀归类，同一类在族间迁移或归类调整会同时改变两族计数，因此「java 仅 +1 无法吸收 kotlin 的 −14」不成立为算术结论，只能作为待验证假设；MOSS 的 definitions 含重载与 $default 合成方法，与 actual_invoke_edges 不是同一单位，不能相除、不能互推覆盖。推断（待验证）：边数微增、compose_methods 与协议定义/边两侧不变，与 R8 改名池变化、DEX 重排、编译器差异相容；同样与实现内联、迁出 player 族边界相容。两种解释均未被静态证据排除，不得据此认定出现新播放器样式或功能缺失。E013（sha256 d73672e5…）属 comment 侧 Compose 访问器源码，仅说明模块在别处存在 runCatching 解析失败返回 null 的软失败写法，不能外推到 player 定位器；PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerCapabilityAccess、SponsorPlayerLocator 本体本会话未读，其安装期解析条件、平板/宽屏与服务端开关分支、失败兜底全部未知。真机启用状态未验证，不得宣称适配通过。
反例与替代解释：可推翻「仅重排/迁移」的证据：类级方法体哈希差集显示 466 类相对基线 480 类存在实现改写而非改名或内联；或 player 族边界外也找不到缺失类的同位实现；或安装期日志中任一 player 定位器解析失败/返回 null，或真机播放页 Hook 命中计数为 0 而基线非 0。反之若差集全部为改名且方法体哈希一致、定位全部命中，也只能把指纹变化归为非语义，仍需真机确认路径启用。
建议：1) 对 9180200 与 9180100 导出 player_java/player_kotlin 类级 method_bodies_sha256 清单做双向差集，并在 player 族边界外按同名/同哈希反查，区分重命名、内联、跨族迁移与真实删除；2) 按文件 sha256 固定快照后阅读 PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerCapabilityAccess、SponsorPlayerLocator，记录候选枚举、解析失败返回值与兜底分支；3) 真机抓安装期定位日志，记录各定位器命中/返回 null；4) 播放页统计缓冲、倍速、画质、赞助商相关 Hook 回调次数并与 9180100 同场景对比；5) 覆盖平板/宽屏与不同播放器入口，确认是否存在并存栈。
证据：E007, E000, E013

### F010：danmaku_kotlin 五项计数不变而指纹变化、legacy 两版同为 absent：静态口径无法区分重排与新样式，直播弹幕消费者与净化策略源码均未覆盖
事实（E008）：danmaku_kotlin 目标与基线均为 137 类、3 个 Compose 方法、164 条外部调用边，结构指纹 97cb0f1…→b65c81e…；danmaku_java_moss 22 定义/20 边、danmaku_kotlin_moss 46 定义/12 边两侧一致；danmaku_legacy 两侧 0 类 0 边、evidence=absent、指纹为两侧同一常量 4f53cda…（与空集合序列化一致的常量，仅表示本次归类口径下无命中）。口径限制：definitions 含重载与 $default 合成方法，与 actual_invoke_edges 不是同一单位，46 与 12 的差不能读作覆盖率、未解析消费者比例或失效证据；预取证据每族仅两个类样本，不能代表整套实现。推断（待验证）：计数五项不变而哈希不同，与 R8 改名、DEX 重排、编译器差异相容，但同样允许少量类替换恰好抵消计数，因此「计数相同」既不证明无变化，也不证明出现新样式，类级方法体哈希对齐是必需步骤；absent 不等于旧原生弹幕实现或页面功能消失。跨家族缺口：E000 的 unregistered_protocols 含 KDanmuMoss、KLaserMoss 等直播弹幕相关协议，其消费者不在本页四家族矩阵内，是否与点播弹幕共用净化策略未知，属未登记待查项而非确认新增样式。DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy 本会话未读，安装条件、屏蔽判据、失败兜底与服务端开关路径未知；服务端 A/B 若无结构变化可静态不可见。runtime_enabled 全为 unknown、complete_coverage=false，不得判定弹幕净化已适配。
反例与替代解释：可推翻「非语义变化」的证据：类级方法体哈希显示 137 类存在实现替换而非改名；或安装期解析失败、过滤命中为 0；或直播场景弹幕完全不受策略影响而点播受影响；或族边界外检索不到缺失类的同位实现。反向可支持非语义判断的证据：差集全部为改名且方法体哈希一致、安装期解析与过滤命中与基线一致——但即便如此仍需真机确认路径启用。
建议：1) 对 9180200/9180100 的 danmaku_kotlin 137 类逐类 method_bodies_sha256 对齐，输出差集与重命名映射，并在族边界外按同名反查缺失落点；2) 按文件 sha256 固定快照后阅读 DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy，记录安装条件、屏蔽判据、解析失败兜底与是否读服务端开关；3) 真机开/关净化各采集一次弹幕条数与过滤命中计数，并记录安装期解析结果；4) 分别进入点播与直播场景，判定是否共用同一策略，并把 KDanmuMoss/KLaserMoss 等协议的消费者补入静态登记；5) 对 base.apk 离线检索已知旧弹幕类名与包前缀，确认 absent 是归类口径差异还是实现移除。
证据：E008, E000

### F011：story_native 类与调用边同时下降而 Compose 方法数不变，不能判为新样式
事实：story_native 由 2974 类/1470 边变为 2969 类/1419 边，compose_methods 恒为 45，指纹由 28025f3f… 变为 a5c8e67f…（E009）。推断：Compose 方法数不变而普通类与传入边减少，优先考虑混淆改名/内联、DEX 重排、封装层合并或少量非 UI 代码迁移，而不是新样式替换。反例：若差集类中既有 UI 布局宿主又有协议消费者、且找不到同方法体哈希的改名对，则更可能是真实的代码迁移或功能下线，此时旧定位器需重写。旁证：同一 APK 内 Opus/动态实现以独立家族存在，样本为 kntr.app.following.opusDetail.* 等（E012，深挖 dynamic_opus），提示 story 区域的可视内容可能由跨家族消费者投递，story_native 的召唤点未必覆盖全部呈现路径；但该深挖结果不包含任何 story 类，不能作为 story Hook 已覆盖或已失效的证据。
反例与替代解释：可推翻当前推断的证据：(1) 差集内出现承载 story 卡片布局的宿主类且无同哈希改名对；(2) 模块安装器日志显示定位器在 9180200 上解析失败或落入兜底分支；(3) 真机 story 页样式与 9180100 明显不同且调用栈指向新增/迁移类。反之，若差异类全为合成类或改名对可一一配对，则本次结构变化与样式无关。
建议：先用同 family 名对 target/baseline 取完整类清单做差集，并按 method_bodies_sha256 配对识别改名；对剩余缺失类逐个确认是否在其它家族出现。随后读取 StoryActionIconsFeatureInstaller.kt 与 StoryPurifyFeatureInstaller.kt，核实其候选类名/方法签名是否落在差异集合内，并检查安装期解析失败时是否有兜底而非静默关闭。
证据：E009, E012

### F012：mine_account_model 计数完全一致仅指纹变化，mine_native 仅多 1 类：更像改名而非新实现
事实：mine_account_model 两侧均为 132 类/43 边/0 Compose 方法，仅指纹由 abd9520a… 变为 91335afb…；mine_native 由 326 类增至 327 类，边数 94 与 compose_methods 7 不变，指纹由 96810670… 变为 a259ab51…（E010）。推断：类数与边数同口径相等时指纹变化通常来自方法体常量、符号表顺序或 DEX 重排；mine_native 的单类增量可能是混淆池波动或新增包装层。这两者是结构候选差异，均未证明影响模块行为。缺失：源文件清单中的 MineComponentFilterFeatureInstaller、MineComponentSnapshot(Store/QueryClient/QueryContract)、MineVipFeatureInstaller、HostMineReadingCard 本轮未读取，mine 页至少存在组件过滤、快照查询、VIP 展示三条独立入口，其安装条件与降级路径全部未知。
反例与替代解释：可推翻当前推断的证据：(1) mine_account_model 存在方法体哈希差异的类且方法名未变，说明逻辑确有改动；(2) mine_native 新增类被模块安装器直接当作挂载宿主或判据来源；(3) 真机 mine 页出现过滤项/VIP 卡片/统计卡样式与基线不一致。若三者皆无，则本次差异应按“结构噪声、非样式变化”结案，但仍不构成适配通过。
建议：对 mine_native 差集里新增的 1 个类取值其父类、方法签名与调用方，判定是包装层还是真实新实现；对 mine_account_model 比对 132 个类的方法/字段名集合与 method_bodies_sha256 集合，确认是否仅改名。再读 MineComponentFilterFeatureInstaller.kt 与 MineVipFeatureInstaller.kt，确认定位器是否按字段名或枚举常量匹配；若依赖字符串常量，改名即可能导致静默失配。
证据：E010

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
登记 5 条路径全部保持静态矩阵 evidence=static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，complete_coverage=false，本轮不宣称任何路径适配通过。逐路径：(1) comment_legacy_v2 类 579→574、外部调用边 754→728、指纹 c5e0f69…→8ca51ee…（E001/E019），降幅约 1%，与类合并/裁剪同量级，不能判为新样式；(2) comment_native_legacy 176→182 类、245→248 边、指纹 29fb0f0…→32c92a7…；(3) comment_native_next 49→44 类、58→57 边、指纹 2449027…→39e97d0…；(4) comment_native_exp3 58→57 类、56→55 边、指纹 67ad049…→929d62b…；(5) comment_compose 2501→2528 类、289→288 compose 方法、1142→1115 边、指纹 9c77cdf…→67e96ff…。四族原生家族变化在 ±6 类内，方向不一致，符合 DEX 重排/混淆改名的解释，但静态矩阵无法区分删除、迁移与服务端开关切换。协议层 comment_java_moss 定义 50/实际调用边 50，comment_kotlin_moss 130/23，且基线与目标完全相同，说明该缺口不是 9180200 引入的版本变化，只是测量口径未解释的既有状态（E001/E019）。模块侧：本轮实读 CommentComposeViewAccess.kt（sha256 d73672e5…），resolve 仅反射 androidx.compose.ui.platform.AndroidCompositionLocals_androidKt#getLocalView 与 Composer#consume(CompositionLocal)，整体包在 runCatching{}.getOrNull()，失败返回 null（E013）。另实读 CommentComposeCopyBridge.kt（1783fcbf…）与 CommentComposePurifyBridge.kt（6ab7905a…）：三座 Compose 桥并非共用同一解析面，而是各自独立的静默降级点——Copy 桥依赖 ComposeCommentText 的硬编码混淆短名（a/i/j/k/o/p/b/c、枚举名集合 ORIGIN/TRANSLATING/TRANSLATION）与 RENDERER/ACTION/SOURCE 类名，Purify 桥依赖 kntr.common.comment.card.model.comment/CommentModel、CommentVoteRenderer、CommentUserInfoRendererModel 的 $a/$b/$c/$d 装饰槽以及 kntr.common.comment.card.store.CardStore+a..z 枚举，失败一律走 FeatureInstallResult.Skipped 并记录日志而非异常（E021/E022）。因此类数上升而调用边下降不能作为风险定位，真正的风险面是这些硬编码短名是否仍在 9180200 命中。native/legacy 家族未做类名差集，CommentClassicStyleLocator、CommentNativeBindingCatalog、installer 是否注册到 next/exp3 分支均未读，属未知。
证据：E000, E001, E011, E013, E019, E021, E022

### 复核页面：dynamic
登记 3 条路径全部保持 evidence=static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，complete_coverage=false。逐路径：(1) dynamic_legacy 类 3254→3273（+19）、外部调用边 2136→2156（+20）、compose_methods 105→105、指纹 1aee4b8…→3a4ffd1…；(2) dynamic_compose 1421→1413（-8）、compose_methods 182→183（+1）、边 287→270（-17）、指纹 76028ed…→9c97046…；(3) dynamic_opus 1370→1349（-21）、compose_methods 95→95、边 227→224（-3）、指纹 72569a3…→e50b06c…（E002/E020）。三族均呈“类数变动、compose 方法数几乎不动”的组合，与原生+Compose+Opus 混合栈并存一致，属结构候选而非已确认新样式；dynamic_compose 的 -17 边/+1 compose 方法也只能说明入口可能收敛，不能推出 Hook 目标消失。dynamic_opus 深挖样本（E012）只含 5/1349 类，均为 kntr/app/following/opusDetail/api 下的数据类、Comparator 与 CompositeExternalInterceptor$… 协程续体样本，未见新界面族特征，但该样本量不足以代表全族，21 个消失类的迁移去向（含是否流入未登记 Opus 协议）仍是未知。协议层 dynamic_java_moss 134/134，dynamic_kotlin_moss 382/27，基线与目标完全一致，属既有测量口径状态而非本版变化。模块侧实读 DynamicPurifyPolicy.kt（e76741e1…）：判定优先读宿主 AdditionalType 上的 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE，读不到回退 {2,6}，关键词按文本片段逐段匹配、不拼接整段正文，且注释明确“读取失败一律保守放行”（E014）。需注意 Signals 的 promotion/lockedChargeOnly 是非空 Boolean（默认 false），因此“读不到示例常量”与“确实为 false”在 Signals 上不可区分，必须在上游读取点打点。dynamic_legacy 新增 19 类与 AdditionalType 常量的引用关系未核查，DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller 等安装器未读，宽屏/平板与服务端开关分支均未验证。
证据：E000, E002, E012, E014, E020

### 复核页面：home
两条登记路径在目标版本并存，status 均逐字取静态矩阵值 static_invoke_observed（E003）：home_legacy 类 785（基线 782）、外部调用边 184（基线 203）、compose_methods 88 未变，指纹 08b1d49a…→61d12f32…；home_new_frame 类 199（基线 190）、边 46（基线 54）、compose_methods 33 未变，指纹 c2fe89cd…→1bef27c7…。变化形态是类增、边减且 compose 方法数两侧完全未变，这与 R8 改名、DEX 重排、调用合并进共享包装层、合成类（lambda/默认参数桥）增删、实现迁移都相容，不能据此认定出现新样式，也不能排除代码迁移。E015 目标侧有界摘录确认 Ltv/danmaku/bili/ui/main2/ 前缀类仍存在（如 ui/main2/A; 持有 HomeFragmentV2 类型字段、AccountMineRequestResource 枚举），说明旧原生栈类未被移除；摘录中并未出现 StartupFragmentV2，该名需按名重读，不能外推。home_new_frame 体量明显更小，只能视为候选容器家族，真机挂载哪一栈、切换条件（服务端实验、宽屏/平板、登录态）均未读到，runtime_enabled=unknown。home 侧 protocols 为空（E003），而种子未登记清单含 HomeMoss、KHomeMoss、feed KFeedMoss，首页协议层既无登记证据也未闭合缺口，不能以空协议表推出“协议无变化”。HomeFrameListHook、HomeFrameTabLocator、HomeTopBarFeatureInstaller 等安装器本轮未读源码，安装条件、候选唯一性与兜底记为未知，module_coverage 仍为 requires_installer_review。验证：双版本类名集合+方法体哈希对拍、两版真机安装期定位日志、View/Activity dump 判断实际挂载栈。
证据：E000, E003, E015

### 复核页面：search
两条登记路径 status 均为静态矩阵原值 static_invoke_observed（E004），不作通过表述。search_native 类 1695（基线 1704，−9）、外部调用边 2913（基线 2865，+48）、compose_methods 2 未变；search_compose 类 3152（基线 3131，+21）、边 614（基线 617，−3）、compose_methods 562 未变；两族指纹均变化，属“结构或调用路径变化，样式未确认”。协议侧 search_java_moss 24/22、search_kotlin_moss 52/18 在基线与目标完全相同（E004），说明本轮静态可见的搜索 RPC 契约面未变，任何样式差异都不体现在协议层；但定义数与调用边数不是同一单位，不能相除推覆盖率，也不能以保证协议未变推出页面适配。E016 抽样（Lkntr/app/search/A..E）多为持有 State/CoroutineScope 字段、仅含 invoke 的小类，形态更像 R8 合并出的 lambda/合成类，为“家族内类集合重排”而非“新 UI 样式”提供了替代解释；E017 目标侧 caller_samples 显示 aggregate/repository/b 等数据仓库类被划入 search_compose，说明该家族标签混杂 UI 与数据层，家族计数不能当样式指标。E018 显示 SearchHomeRecommendLocator 以 discover.a–z + SearchDiscoverViewModel 为根、按单字符后缀枚举嵌套宿主，Points.deliveryCandidateCount 明确“不参与功能判定”，delivery/state 可空；若候选歧义则可能静默不 Hook，但本轮未取得任何运行时 Points 值，属待验证风险而非已成立缺陷。搜索未登记协议含 app/search/v2/KSearchMoss、broadcast/message/search/SearchMoss、interfaces/v1/SearchMoss，覆盖缺口未闭合；SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 未读源码，安装条件与兜底未知。验证：两版定位器 Points 对比、discover 与 search2.main.data 全量类名导出、按 tab 真机抓 Hook 命中日志。
证据：E000, E004, E016, E017, E018

### 复核页面：detail
复核 E005 目标/基线两侧计数：detail_legacy 两版均为 0 类/0 Compose/0 边且指纹同为 4f53cda1…，status=absent 与静态矩阵一致，只能说明该口径下未命中，不能推出旧原生详情实现已删除；detail_theseus_ugc 1973→1975 类、25→25 Compose、525→522 边，指纹 ed2491aa…→5e32fd5a…；detail_theseus_united 4679→4669 类、98→98 Compose、4180→4193 边，指纹 cce82b5d…→c6cbf881…；detail_java_moss 32 定义/35 边、detail_kotlin_moss 76 定义/34 边两版逐项相同。草稿对这些数字的引用无误，且未把 static_invoke_observed 改写成通过或已适配，complete_coverage=false、module_coverage=requires_installer_review 得以保留。需收紧之处：path_reviews 的 detail_theseus_ugc 条目用 E012（dynamic_opus 家族样本）论证“Opus 详情存在独立广告点击旁路”，该证据属动态页家族且为截断摘录，把 kntr/app/following/opusDetail 包归属到详情页尚未验证，只能作为未定归属的观察。整体空白在模块侧：DetailAppPromotionFeatureInstaller、DetailModulePurify*/Policy、DetailUnitedModulePurify*/PresentationPurify*、DetailViewPurify*、HomeVerticalDetail* 仅有文件名，未读定位器、安装条件与失败兜底，故五条路径的 Hook 覆盖仍属未知。E011（sample_limit=5）与 E012（truncated=true）为有界摘录，不能外推到 comment/dynamic 整套实现。
证据：E000, E005, E011, E012, E013

### 复核页面：pgc
复核 E006：pgc_legacy 345→357 类、0→0 Compose、301→307 外部调用边，指纹 14717f3a…→e0071b25…；pgc_theseus 2258→2255 类、134→132 Compose、982→913 边，指纹 b9f79e23…→53ca22f6…；pgc_player_moss 12 定义/3 边、pgc_view_moss 14 定义/7 边两版逐项相同。草稿计数引用准确，两条路径 status 保持 static_invoke_observed，runtime_enabled=unknown 与 requires_installer_review 未改动，并明确拒绝用定义数除调用边数推导覆盖率，口径正确。需保留的审慎点：+12 个 legacy 类与 -69 条 theseus 外部调用边的归属未定位，R8 内联、匿名类合并、DEX 重排都能产生同样读数，因此“重心由 theseus 移向 legacy”只能作为候选画像，不能表述为已确认的栈切换；协议两侧计数相同也不等于调用者集合相同，未做调用者比对，不能据 12/3、14/7 判断播放或视图协议只在少数路径使用。最大静态空白在模块侧：PgcAutoActivityPopupLocator、PgcAutoActivityPopupPolicy、PgcAutoActivityPopupFeatureInstaller 只有文件名，候选枚举、父类判据与兜底顺序未读，自动弹窗 Hook 命中 legacy Activity 还是 theseus Compose 弹层、缩容后是否丢锚点均为未知。宽屏/平板、登录态与服务端开关分支在证据中不出现，属未知而非不存在。
证据：E000, E006

### 复核页面：player
事实（E007，本会话重新取证，目标 9180200 / 基线 9180100）：player_java 类 953→954、外部调用边 3300→3305、compose_methods 两侧为 0，指纹 9721f66…→746cdb8…；player_kotlin 类 480→466、边 891→897、compose_methods 37→37，指纹 9c22f38…→f314119…；player_java_moss 定义 18/边 2、player_kotlin_moss 定义 34/边 3 两侧一致。E000 将 player_java、player_kotlin 列为 structure_or_call_path_changed，且两族 runtime_enabled=unknown、module_coverage=requires_installer_review、complete_coverage=false。注意口径：族按包前缀归类，类在族间迁移或归类调整会同时改变两族计数，因此「java +1 吸收不了 kotlin −14」只能列为待验证假设；MOSS 定义数含重载与 $default 合成方法，与 actual_invoke_edges 不是同一单位，不能相除或互推覆盖。本会话未读到任何 player 定位器源码（PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerCapabilityAccess、SponsorPlayerLocator 仅在 source_files 名单中），其安装期解析条件、平板/宽屏分支、服务端开关与兜底一律未知。预取证据每族仅两个类样本、每协议四个调用者样本，不能外推为整套实现。真机启用与 Hook 生效均未验证，不得表述为适配通过。
证据：E007, E000

### 复核页面：danmaku
事实（E008，本会话重新取证）：danmaku_kotlin 目标与基线均为 137 类、3 个 Compose 方法、164 条外部调用边，但结构指纹 97cb0f1…→b65c81e…；danmaku_java_moss 22 定义/20 边、danmaku_kotlin_moss 46 定义/12 边两侧一致；danmaku_legacy 两侧 0 类 0 边、evidence=absent、指纹为同一常量 4f53cda…（与空集合序列化一致的常量，只说明本次归类口径无命中，不等于旧原生弹幕功能消失）。计数不变而哈希变化与 R8 改名、DEX 重排、编译器差异相容，但同样允许少量类替换恰好抵消计数，故不能据此判定无样式变化；反之也不能判定出现新样式。协议定义数含重载与 $default 合成方法，与调用边不是同一单位，46 与 12 的差不能读作覆盖率或未解析消费者比例。E000 的 unregistered_protocols 含 com.bapis.bilibili.live.approom.api.grpc.v1.KDanmuMoss、broadcast/v1 KLaserMoss 等直播相关协议，其消费者不在本页四家族静态矩阵内，属未登记覆盖缺口而非确认新样式。DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy 源码本会话未读，安装条件、屏蔽判据、失败兜底与服务端开关均未知；runtime_enabled 全部 unknown、complete_coverage=false，不得判定弹幕净化已适配。
证据：E008, E000

### 复核页面：story
story 页登记两条路径，均按预取视图 E009（两家族各 2 条类样本、protocols 为空表）复核。story_native：目标 2969 类 / 45 Compose 方法 / 1419 外部调用边，基线 2974 / 45 / 1470，指纹 28025f3f… → a5c8e67f…，status 逐字为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，change 登记为 structure_or_call_path_changed。类数与调用边同时下降而 compose_methods 持平，只能说明抽取窗口内结构与调用面变化，不能区分混淆改名、内联、DEX 重排、封装层合并或少量代码迁移；本单元未做类级差集与 method_bodies_sha256 配对，故新/旧样式均不能判定。story_kotlin：目标与基线均为 0 类 / 0 Compose 方法 / 0 边、空态指纹 4f53cda1…，status 逐字为 absent；absent 仅表示本家族抽取窗口内无类，不等于页面 Kotlin 实现不存在，也不能据此推断其它家族承载同一 UI。story 家族 protocols 为空表，未登记 StoryMoss/KStoryMoss 的消费者，跨家族投递路径未知。源文件清单中的 StoryActionIconsFeatureInstaller/StoryPurifyFeatureInstaller/HomeVerticalDetailFeatureInstaller/HomeVerticalDetailRouting 本轮未读取，story 页定位器命中、兜底分支、原生与 Compose 并存栈及切换条件均未知。E012（dynamic_opus 目标家族样本）仅作跨家族存在性旁证，不含任何 story 类，不能用于推断 story Hook 的覆盖或失效。
证据：E009, E012, E000

### 复核页面：mine
mine 页登记两条路径，均引用预取视图 E010 复核，protocols 为空表。mine_native：327 类 / 7 Compose 方法 / 94 外部调用边，基线 326 / 7 / 94，指纹 96810670… → a259ab51…，status 逐字为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review。单类增减且边数与 Compose 方法数不变，既可能是混淆池/合成类波动，也可能是新增包装层，本轮未做类级差集，无法判定是否触及模块挂载点。mine_account_model：132 类 / 0 Compose 方法 / 43 边两侧完全一致，仅指纹 abd9520a… → 91335afb… 变化；计数同口径相等时指纹变化最常见解释是常量、符号顺序或 DEX 重排，但也可能来自真实逻辑改动，需方法体哈希集合比对才能定性。mine 页协议表为空，未登记 MineMoss/KMineMoss 等（见未登记协议清单）的消费者与调用边，组件过滤、VIP 展示与快照查询之间的共享协议关系未知。源文件清单中 MineComponentFilterFeatureInstaller、MineComponentSnapshot、MineComponentSnapshotStore/QueryClient/QueryContract、MineVipFeatureInstaller、HostMineReadingCard 本轮均未读取，三条独立入口的安装条件、定位器匹配方式（字段名/枚举常量/字符串常量）与失败降级路径全部未知；宽屏/平板与服务端开关分支亦未取证。
证据：E010, E000

- F001 / revised：事实层成立（comment_compose 类 2501→2528、compose 方法 289→288、边 1142→1115、指纹变化，E001/E019；E013 证实 resolve 仅反射 getLocalView 与 Composer.consume 且失败返回 null），但分析层被本轮实际读取的 E021/E022 推翻两点：(a) Copy/Purify/ReplyButton 三座 Compose 桥并不共用同一解析面，Copy 桥、Purify 桥各自有独立的硬编码混淆短名定位器，缺失时返回 Skipped 并记录日志，不会“同时空转”；(b) 草稿要求“对 288 个 compose 方法抽样比对桥接命中率”与源码不符——Copy 桥注册目标是 RENDERER 类中带 CommentModel 与 Composer 参数的实例方法，Purify 桥目标是 CommentVoteRenderer 等固定类，288 个 compose 方法不是 Hook 目标面。另“类数上升而调用边下降提示包装层增删”属未验证推断，“compose 方法数与宿主 Compose 运行时版本直接相关”亦无证据。故降为静态证据 + 待真机，并改写验证任务。（E001, E011, E013, E019, E021, E022）
- F002 / revised：计数事实成立且未跨页误用：comment_java_moss 50/50、comment_kotlin_moss 130/23、dynamic_java_moss 134/134、dynamic_kotlin_moss 382/27，并明确写了“23/27 不能当覆盖数、130/382 不能当实现规模”的口径警示，alternatives 也给出了测量口径失灵的反解释，主体可保留（level=candidate）。但需补一条关键限定：这四组数字在 9180100 与 9180200 完全相同（E001/E019、E002/E020），因此这不是本版引入的变化，只是既有未解释状态；草稿把该缺口与“本版变化”并列叙述易被误读为回归。同时草稿承认未读 KotlinMossChannel/KotlinMossReplyBridge，本轮因只读取证阶段结束同样未读，故必须保留为推断并在 remaining_gaps 显式登记，不得升级。（E000, E001, E002, E019, E020）
- F003 / revised：主体成立：dynamic_opus 1370→1349、边 227→224、compose 方法 95 不变、指纹变化（E002/E020），E012 样本确为 kntr/app/following/opusDetail/api 下数据类与协程续体；E014 证实 AdditionalType 常量名、FALLBACK {2,6}、逐段匹配与“读取失败一律保守放行”，因此“读不到→漏删而非误删”的推断有代码依据。需修正一处技术错误：E014 显示 Signals 的 promotion 与 lockedChargeOnly 是非空 Boolean（默认 false），只有 authorName/authorMid 与 textFragments 可承载“没读到”，所以草稿要求“验证 promotion/lockedChargeOnly 是否仍能读到非空值”在 Signals 层不可能实现，读失败与真 false 在该层不可区分，必须把打点上移到构造 Signals 的读取点/常量反射处。同时 E012 仅 5/1349 类，样本代表性须显式限定。（E002, E012, E014, E020）
- F004 / retained：核心断言有证据支撑：E018 显示 SearchHomeRecommendLocator 的根候选为 discover.a–z + SearchDiscoverViewModel，二级后缀只枚举单字符 a–z/0–9，Points 中 delivery/state 可为 null，且 deliveryCandidateCount 的注释明确“仅用于区分「宿主没有该结构」与「候选歧义」，不参与功能判定”；E004 显示 search_compose 类 3152（基线 3131，+21）、search_native 1695（1704，−9）且两族指纹均变化，构成“宿主类集合被重排”的事实基础；E016 抽样为该家族内的小 invoke 类。finding 已置于 needs_runtime，并明确写出“没有 9180200 上 Points 的运行值”，没有把推断当成结论，也列出了可推翻推断的反例与双版对比验证方法，符合不宣称适配通过的要求。证据边界：本次 E018 摘录在下述细节处被截断，locate() 内各 singleOrNull 判据、delivery() 的 getHistoryList/唯一接收方法、state() 的唯一 square 字段、discoveryCache 的 3 或 5 参构造器与 getValue/setValue 唯一性均未在本次有界摘录中直接读到，仅与 Points 行为声明相容；该部分留作补证缺口，不据此外推。（E018, E016, E004）
- F005 / revised：计数与指纹方向均与 E003 一致：home_legacy 785/184（基线 782/203）、home_new_frame 199/46（基线 190/54），四族 compose_methods 未变，指纹两侧不同；E015 摘录确认 tv.danmaku.bili.ui.main2 前缀类仍在（含持有 HomeFragmentV2 类型字段的 ui/main2/A; 与 AccountMineRequestResource 枚举），支持“旧原生栈未被删除”。level=candidate 与“不能认定新样式”的结论合规。需修订处：草稿把 E015 抽样描述为“仍含 HomeFragmentV2、StartupFragmentV2”，但本次有界摘录中只出现 HomeFragmentV2（作为字段类型），StartupFragmentV2 未出现，属对截断内容的过度外推；同时应显式写明数字为“方法定义/调用边不同量纲、不可相除”。补丁仅改 analysis，页面与 evidence_ids 不变。（E003, E015, E000）
- F006 / revised：协议计数零变化与 E004 完全一致（java 24/22、kotlin 52/18，基线与目标相同），E017 样本中 aggregate/repository/b 直接构造 KSearchMoss 并调用 searchOGV，E016 同族抽样为小型 invoke 类，因此“协议面稳定但家族内混杂数据层”的判断成立，level=static_evidence 仍与证据强度匹配。需修订处：草稿称“实际消费者全在 search_compose 家族”，但 E017 只给出 total_callers=18 与截断的 caller_samples，18 条边未逐条枚举，且 search_java_moss 的 22 条边调用者本轮完全未读到，属由样本外推为全体；补丁将断言收窄为“样本所示调用者属 search_compose”，并把 java_moss 调用者未读、未登记 SearchMoss 家族消费者未知作为显式缺口。页面与 evidence_ids 不变。（E017, E016, E004, E000）
- F007 / retained：核心事实断言由被读到的源码支撑：E013 为 truncated=false 的完整源码，CommentComposeViewAccess.resolve 依次解析 AndroidCompositionLocals_androidKt.getLocalView、CompositionLocal、Composer.consume，任一缺失即 return null，且整体包在 runCatching{}.getOrNull() 中，失败路径不抛错、不记录日志，与草稿描述逐句对应；E005 佐证 detail 两栈均为 static_invoke_observed、Compose 方法数 25/98、runtime_enabled=unknown；E011 佐证目标包内 comment_compose 家族存在 2528 类/288 Compose 方法/1115 边，规模上不是零星实现。草稿同时把“评论家族是否由 detail 页加载”“外层是否在安装期调用 resolve”“null 后是否有回退”明确标为未读源码、不宣称 Hook 覆盖缺失，未越界；level=candidate 与 static_invoke_observed 的矩阵状态一致，未改写为通过。E011 为 sample_limit=5 的有界摘录，故本条只能作为候选而非已确认缺口，retained 而非升级。（E011, E013, E005）
- F008 / retained：全部计数与指纹变化经 E006 双侧核对无误：pgc_legacy 345→357 类、301→307 边、指纹 14717f3a…→e0071b25…；pgc_theseus 2258→2255 类、134→132 Compose、982→913 边、指纹 b9f79e23…→53ca22f6…；pgc_player_moss 12/3 与 pgc_view_moss 14/7 两版一致。草稿没有把 -69 条边或 +12 个类当作结论：明确列出 R8 内联、匿名类合并、DEX 重排、公共适配层归族等多种替代解释，写明“不能靠总数相减”，并说明定义数与调用边数不同单位、不作覆盖率推导，符合计数不得外推的要求。level=needs_runtime 恰当：实际生效栈与弹窗归属必须真机判定，静态只能定位候选。保持 retained 的前提是结论只能以“候选画像”表述，不得在最终报告中升级为已发生的栈切换；定位器源码未读的空白已在正文声明。（E006, E000）
- F009 / revised：核心计数断言与 E007/E000 逐项吻合（player_java 953→954、边 3300→3305、compose 0；player_kotlin 480→466、边 891→897、compose 37；MOSS 18/2 与 34/3 两侧相同），推断部分有保留且未宣称适配通过，故保留。需修订三点：(1) 草稿用 E013（comment 侧 CommentComposeViewAccess 源码）作 player 定位器 runCatching 软失败的类比，属跨页外推，必须删除「若 player 各定位器同构」的假设链；(2) 「java 侧 +1 类不足以吸收 kotlin 侧 −14 类」隐含跨族相加，族按包前缀归类、类可跨族迁移，应降为待验证假设；(3) 补上定义数与调用边不是同一单位的口径说明。修订后 level 仍为 candidate（结构变化是否语义化未定）。（E007, E000, E013）
- F010 / revised：计数与指纹断言与 E008 完全一致（137/3/164 两侧相同、指纹 97cb0f1…→b65c81e…、legacy 两侧 0/0 absent、协议 22/20 与 46/12 不变），absent 未被误读为功能消失，直播协议缺口有 E000 支撑，保留。需修订：(1) 把 4f53cda… 的表述精确化为「两侧同一常量指纹，与空集合序列化一致」，避免暗示已证明为空集；(2) 补入 definitions 与 actual_invoke_edges 单位不可比、46 与 12 不能读作覆盖率的说明；(3) 明确预取每族仅两个类样本，不得外推整套实现。level 维持 needs_runtime（净化是否生效只能真机判定），但结论前置静态类级差集。（E008, E000）
- F011 / retained：E009 直接支持事实部分：story_native 2974→2969 类、1470→1419 边、compose_methods 恒为 45、指纹 28025f3f…→a5c8e67f…，status 为 static_invoke_observed；story_kotlin 两侧空态。标题与结论保持在“候选、非新样式”的保守口径，未把计数下降或 absent 外推为样式下线或适配结论。alternatives 已给出可推翻条件（差集内 UI 宿主类无同哈希改名对、安装器解析失败/落兜底、真机样式差异指向迁移类），推导链条可复核。E012 仅为 dynamic_opus 目标家族样本，草稿明确写出其不含任何 story 类、不能推断 story Hook 覆盖，引用方式未越界。assigned 工具中无类级差集与 method_bodies_sha256 配对结果，analysis 末尾已把该缺失登记为待补证任务而非确定性判断，故保留原级 candidate。（E009, E012）
- F012 / retained：E010 直接支持计数事实：mine_native 326→327 类、94 边与 7 Compose 方法不变、指纹 96810670…→a259ab51…；mine_account_model 两侧 132 类/43 边/0 Compose 方法、仅指纹 abd9520a…→91335afb… 变化。草稿把两者定性为“结构候选差异、未证明影响模块行为”，并明确写出 MineComponentFilterFeatureInstaller、MineComponentSnapshot(Store/QueryClient/QueryContract)、MineVipFeatureInstaller、HostMineReadingCard 未读取、三条入口安装条件与降级路径未知，未以“无影响/稳定”填补缺口，符合证据边界。level 取 needs_runtime 恰当：现有证据全为静态计数与指纹，定性依赖类级差集与真机/安装器日志。alternatives 给出三条可推翻条件，可复核。（E010）

### 尚未解决的证据缺口

- [1] comment 的 legacy_v2/native_legacy/native_next/native_exp3 尚未做两版类名与方法签名差集，删除、迁移与 DEX 重排未区分（E001/E019 仅有汇总计数）；CommentClassicStyleLocator.kt、CommentNativeBindingCatalog.kt、CommentSectionFeatureInstaller.kt 等安装器源码本轮未读，next/exp3 分支是否注册、失败是否走 logError 均未知。
[2] CommentComposeCopyBridge/CommentComposePurifyBridge 依赖的硬编码混淆短名与类名（ComposeCommentText 的 a/i/j/k/o/p/b/c、CommentUserInfoRendererModel 的 $a..$d、CardStore+a..z 枚举、RENDERER/ACTION/SOURCE/CommentVoteRenderer）在 9180200 是否仍命中未验证；只能由真机安装日志（Installed/Skipped/hookCount）证实。
[3] KotlinMossChannel.kt 与 KotlinMossReplyBridge.kt 仍未读取（source 快照列为 unmapped_multi_path_candidates），Kotlin MOSS 130/382 条定义中未解析部分属于“有引用未解析”还是“死定义”未分类，Kotlin 通道 Hook 覆盖不得推测。
- [4] dynamic_opus 的 21 个消失类迁移去向未知，E012 样本仅 5/1349 类，不能代表全族；是否与未登记的 OpusMoss/KOpusMoss/mall.tab3.dynamic.OpusMoss 等协议消费者相关仍为调查候选。
[5] dynamic_legacy 新增 19 类与 AdditionalType 常量的引用关系未核查，dynamic_compose 的 183 个 compose 方法两版差集未做；DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller、DynamicVideoTabPreference 本轮未读。
[6] dynamic_compose 调用边 287→270（-17）与 compose 方法 182→183 的组合只能说明入口可能收敛，Hook 目标是否仍在未验证；Compose 侧净化/复制桥的具体注册目标未在动态页读取。
- [7] 两条页面的 runtime_enabled 全为 unknown：服务端 A/B 开关、登录态、平板/宽屏分支均未取得运行条件证据；静态矩阵不可见的服务端视觉变体不能宣称已穷尽。
[8] 本轮引用文件为 dirty 工作树快照（source_tree_sha256 37745f8f…，head 5422fad1…），引用文件哈希：E013 d73672e5…、E014 e76741e1…、E021 1783fcbf…、E022 6ab7905a…；复核阶段预算耗尽，home/search 等其他页面的 E015/E016/E017/E018 未在本单元使用，不构成对本单元的补证。
[9] 按名重读 E018 全量（未截断）以确认 locate()/delivery()/state()/discoveryCache 的 singleOrNull 判据细节，本次摘录在 fun locate(loader: 处截断。
- [10] 在 9180100 与 9180200 两版安装期实际取得 SearchHomeRecommendLocator.Points（deliveryCandidateCount、delivery/state 是否为 null、解析到的字段名），当前无任何运行值。
[11] 导出 com.bilibili.search2.discover 与 com.bilibili.search2.main.data 全量类名并检查是否存在 $aa 等双字符嵌套后缀宿主，验证单字符后缀枚举是否漏发现。
[12] 对 home_legacy/home_new_frame 与 search_native/search_compose 做双版本类名集合+方法体哈希对拍，识别 -$$Lambda、默认参数桥等合成类与改名项，区分重排与真实结构新增。
- [13] 真机以 Activity/View dump 判断首页实际挂载栈（HomeFragmentV2 旧栈 vs home_new_frame），记录服务端实验位、宽屏/平板与登录态分支。
[14] 按文件哈希重读 HomeFrameListHook、HomeFrameTabLocator、HomeTopBarFeatureInstaller、HomeComponentFilterFeatureInstaller、HomeExtraCardPolicy 等首页安装器，确认候选唯一性与解析失败兜底；当前仅出现在 source_files 清单中，未读实现。
[15] 按文件哈希重读 SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner、SearchHomeRecommendFeatureInstaller 与 SearchHomeRecommendPolicy，确认安装条件与兜底路径。
- [16] 枚举并标注未登记的 app/search/v2/KSearchMoss、broadcast/message/search/SearchMoss、interfaces/v1/SearchMoss 的实际调用者与上游页面，判定是否构成搜索净化漏挂路径。
[17] 补齐首页协议登记（HomeMoss、KHomeMoss、feed KFeedMoss 等）或写入明确的不覆盖范围，避免以 protocols={} 推出首页协议无变化。
[18] 逐条枚举 search_java_moss 的 22 条实际调用边调用者与家族归属，本轮只读到 kotlin 边样本，java 边消费者未知。
- [19] 对搜索各 tab（综合/番剧/漫画/OGV）与首页推荐做真机开关对比，抓 Hook 命中日志，确认静态可见调用边是否被真正挂载（所有路径 runtime_enabled 仍为 unknown）。
[20] 确认源码快照为脏工作树（source_tree_sha256 37745f8f…，head 5422fad1…），本轮引用文件需记录 sha256（E018 1c569369…、E013 d73672e5…、E014 e76741e1… 等）以便追溯行号未漂移。
[21] detail 模块侧定位器未读：DetailAppPromotionFeatureInstaller、DetailModulePurifyFeatureInstaller/Policy、DetailUnitedModulePurify*/DetailUnitedPresentationPurify*、DetailViewPurify*、HomeVerticalDetailFeatureInstaller/Routing 仅见文件名，锚点类/方法、安装条件与失败兜底均未知；需按文件 sha256 固定版本补读（工作树 dirty，source_tree_sha256=37745f8f…，head 5422fad1…）。
- [22] detail_legacy 两版 absent 的成因未定：需离线检索 base.apk 内旧原生详情类名与包前缀，确认是归类前缀未覆盖还是实现迁出，不得据 absent 推断页面功能消失。
[23] 未做类级 diff：detail_theseus_united 消失的 10 类、detail_theseus_ugc 的 +2 类/-3 边、pgc_legacy 新增 12 类的类名+method_bodies_sha256 清单均未生成，重排/内联/真实删除仍不可区分。
[24] pgc_theseus -69 条外部调用边来源未定位；pgc_player_moss/pgc_view_moss 仅比对计数，未比对调用者集合，计数相同不能排除调用者替换。
- [25] PgcAutoActivityPopupLocator、PgcAutoActivityPopupPolicy、PgcAutoActivityPopupFeatureInstaller 源码未读，无法判断候选枚举是否同时覆盖 legacy Activity 与 theseus Compose 弹层、以及兜底顺序。
[26] CommentComposeViewAccess.resolve 的调用者与 null 返回后的回退分支未读；两版 APK 中 androidx.compose.runtime.Composer.consume 与 AndroidCompositionLocals_androidKt.getLocalView 是否签名一致未核对，ABI 变动推断待证。
[27] 评论 Compose 桥接侧同样以 runCatching 返回 null 收敛失败（CommentComposeCopyBridge sha256 1783fcbf…、CommentComposePurifyBridge sha256 6ab7905a…），其调用方及与 detail 页评论区的加载关系未验证。
- [28] E011（sample_limit=5）与 E012（truncated=true）为有界/截断摘录，不能代表 comment_compose、dynamic_opus 整套实现；kntr/app/following/opusDetail 包归详情页还是动态页未验证。
[29] 五条 detail/pgc 路径 runtime_enabled 全部 unknown，无真机 Activity 栈、类加载器来源与 Hook 安装/命中日志，UGC 详情、Opus 详情、番剧详情与播放页实际启用栈未判定。
[30] 平板/宽屏、未登录态与服务端 A/B 分支在 detail/pgc 证据中均不出现，属未知；不排除未归类调用者与并存栈被静态口径漏掉。
- [31] detail_java_moss/detail_kotlin_moss 定义数远多于实际调用边（76/34），未解析消费者与接口分发/反射调用不可见，兜底覆盖仍缺安装器侧证据。
[32] 本会话 fresh_refresh 为空；E005/E006 由本轮 prefetch 重读，E011/E012/E013 取自会话证据包（E013 为完整源码），后续结论需以相同文件哈希复读以保持追溯。
[33] player 两族与 danmaku_kotlin 均未做类级 method_bodies_sha256 双向差集，指纹变化属改名、DEX 重排、跨族迁移还是实现替换尚无证据（E007/E008 只给汇总计数与两个类样本）。
- [34] player 定位器源码（PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerCapabilityAccess、SponsorPlayerLocator）本会话未读，安装期解析条件、返回 null 兜底、平板/宽屏与服务端开关分支全部未知。
[35] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 未读，净化安装条件、屏蔽判据、失败兜底与是否读服务端开关未知。
[36] 所有路径 runtime_enabled=unknown、complete_coverage=false，缺少真机安装期解析日志与 Hook 命中计数；不得以静态计数替代运行时确认。
- [37] danmaku_legacy 两版均为 0 类 0 边并共用同一常量指纹，需离线检索旧弹幕类名与包前缀，才能区分归类口径差异与实现移除。
[38] E000 unregistered_protocols 中的 KDanmuMoss、KLaserMoss 等直播弹幕协议消费者未登记，无法判断直播与点播是否共用净化策略。
[39] 服务端 A/B 视觉变体若无结构变化则静态不可见，本报告不能声称已穷尽 player/danmaku 的所有样式分支。
- [40] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，head 5422fad1…；E013 sha256 d73672e5…），后续引用需按文件哈希固定，本轮未逐文件核对行号漂移。
[41] story_native 未做 target/baseline 完整类清单差集与 method_bodies_sha256 配对，无法区分混淆改名/DEX 重排、封装层合并与真实代码迁移；1419←1470 边减少的来源未定位
[42] story_kotlin 的 absent 未做抽取前缀反证（用已知有类的前缀验证抽取规则生效），也未取证运行时是否存在同名 Kotlin 实现，抽取窗口外的实现仍未知
- [43] StoryActionIconsFeatureInstaller.kt、StoryPurifyFeatureInstaller.kt 未读取：定位器候选类名/方法签名、安装期解析失败时的兜底分支、热路径是否存在二次回退均未知
[44] HomeVerticalDetailFeatureInstaller.kt/HomeVerticalDetailRouting.kt 未读取：story 相关路由是否存在原生/Compose 多路径并存、切换条件、平板/宽屏分支与服务端开关未知
[45] story 与 mine 两页 protocols 均为空表，StoryMoss/KStoryMoss、MineMoss/KMineMoss 等已出现在未登记协议清单中，其跨家族消费者与实际调用边未核对，不能以空协议表推出“协议无变化”
- [46] mine_native 新增的 1 个类未定位父类/方法签名/调用方，无法判定是混淆池波动还是新增包装层；其余 326 类未做方法体哈希比对
[47] mine_account_model 132 类的字段名/方法名集合与 method_bodies_sha256 集合未比对，指纹变化是改名、常量/符号顺序调整还是真实逻辑改动仍未定性
[48] MineComponentFilterFeatureInstaller.kt、MineVipFeatureInstaller.kt、MineComponentSnapshot.kt 与 MineComponentSnapshotStore/QueryClient/QueryContract、HostMineReadingCard.kt 未读取，组件过滤、快照查询、VIP 展示三条入口的安装条件、匹配依据（字段名/枚举/字符串常量）与降级路径未知
- [49] 两条 page 的 runtime_enabled 全为 unknown：未在 9180200 真机上采集 story 页与 mine 页的安装期定位日志、Hook 命中计数与开关前后页面差异
[50] 未覆盖平板/宽屏、未登录与服务端 A/B 分组条件下的并存栈与切换条件；服务端控制的样式变体若无结构变化，静态不可见
[51] 源快照 source_tree_sha256=37745f8f…、working_tree_dirty=true、head 5422fad1…，本轮引用文件未记录文件级 sha256，行号漂移风险未排除
- [52] 本单元仅完成静态证据审查，两条路径结论保持 static_invoke_observed / absent 原值，不得表述为适配通过；升级结论需上述差集、安装器源码与真机日志齐备

## 下一步

- [1] 真机 9180200 安装后打印 CommentComposeViewAccess.resolve 结果，确认 getLocalView 与 Composer.consume 是否仍可解析（E013）
[2] 对 comment_compose 的 288 个 compose 方法做基线与目标差集，定位 CommentComposePurifyBridge/CommentComposeCopyBridge 失配项（E011）
[3] 对 legacy_v2/native_legacy/native_next/native_exp3 逐家族做类名差集，区分删除、迁移与重排（E001）
[4] 核对 CommentClassicStyleLocator 与 CommentNativeBindingCatalog 在目标版本的命中日志，确认安装器是否注册到 next/exp3 分支
[5] 回溯 comment_kotlin_moss 130 条定义中的未解析消费者，核对 KotlinMossChannel 注册表（E001/E000）
- [6] 真机打印 DynamicPurifyPolicy.Signals 各字段（区分 null 与 false），覆盖率以运行时数据而非静态计数表达（E014）
[7] 确认宿主 AdditionalType 的 additional_type_goods_VALUE/additional_type_up_rcmd_VALUE 在 9180200 是否存在，未命中时记录实际常量名
[8] 对 dynamic_compose 183 个 compose 方法与基线差集，检查净化/复制桥目标入口是否收敛（E002）
[9] 核对 21 个消失的 dynamic_opus 类是否迁移至 mall/tab3/dynamic/v1/OpusMoss 等其他包（E012）
[10] 梳理未登记协议清单中的 DynamicMoss/KOpusMoss/OpusMoss/FeedMoss，确认是否有跨家族消费者驱动动态卡片数据
- [11] 分别以服务端 A/B 实验组与对照组进入评论区与动态页，记录实际加载的家族，静态不可见部分标为未知
[12] 复核冻结源码为 dirty 工作树，按文件 sha256 记录本轮引用文件（如 E013 d73672e5…、E014 e76741e1…）以便追溯
[13] 在 9180100 与 9180200 两版上分别执行模块安装期探测，dump SearchHomeRecommendLocator 的 Points（deliveryCandidateCount、delivery/state 是否为 null、解析到的字段/方法名），形成对比表以判定搜索首页推荐是否静默退化。
[14] 对两版本导出 com.bilibili.search2.discover、com.bilibili.search2.main.data 与 home 两家族的全量类名集合及方法体哈希，区分混淆改名/DEX 重排与真实结构新增；明确标记合成类与包装层。
[15] 检查 discover 命名空间是否存在 R8 双字符嵌套后缀（$aa 等）类；把静态探测口径从 a-z0-9 扩展到 aa-zz，确认单字符后缀枚举是否漏掉投递宿主。
- [16] 真机在 9180200 上分别验证搜索首页推荐净化、搜索各 tab（综合/OGV/漫画）净化与默认搜索词清除，抓 Hook 命中日志，记录开关前后页面差异。
[17] 真机确认首页实际渲染栈：通过 Activity/View dump 判断 home_legacy（HomeFragmentV2）与 home_new_frame 哪条在用，并记录宽屏/平板分支与服务端实验位影响。
[18] 抓首页两族安装器（HomeFrameListHook、HomeFrameTabLocator、HomeTopBarFeatureInstaller 等）的安装日志，确认定位候选是否唯一命中；本单元未读其源码，需按文件哈希追溯后补读实现再下结论。
[19] 枚举未登记的 app/search/v2/KSearchMoss、broadcast/message/search/SearchMoss、interfaces/v1/SearchMoss 的实际调用者，标注上游页面，判定是否构成搜索净化漏挂路径。
[20] 补充首页协议登记（HomeMoss/KHomeMoss/feed KFeedMoss 等）或明确写入不覆盖范围，避免以空协议表推出“首页协议无变化”。
- [21] 复核源码快照为脏工作树（source_tree_sha256 37745f8f…）带来的追溯风险：对引用文件记录 sha256，并在复核阶段确认行号未漂移，不建议清理工作树。
[22] 所有四条路径保持 static_invoke_observed 状态，待上述真机与安装器证据齐备后再评估是否可变更结论；当前不得表述为适配通过。
[23] 对 9180200 与 9180100 分别导出 detail 两栈与 pgc 两栈的类名+method_bodies_sha256 清单，做集合差，定位 detail_theseus_united 消失的 10 类、detail_theseus_ugc 变动项与 pgc_theseus 减少的 69 条调用边来源。
[24] 用 decompile_class 读取 kntr/app/following/opusDetail/api/CompositeExternalInterceptor 及其 handleAdClick 调用方，确认 Opus 详情广告旁路属于详情页还是动态 feed 页，并核对 DetailAppPromotionFeatureInstaller 的锚点是否覆盖它。
[25] 静态追踪 CommentComposeViewAccess.resolve 的调用者，确认返回 null 时是否有回退路径；对比两版 apk 中 androidx.compose.runtime.Composer.consume 与 AndroidCompositionLocals_androidKt.getLocalView 的签名是否一致。
- [26] 读取 DetailViewPurifyFeatureInstaller / DetailModulePurifyFeatureInstaller / DetailUnitedModulePurifyFeatureInstaller 的定位器与安装条件（按文件哈希固定版本），逐条核对锚点类是否仍存在于目标包的对应家族。
[27] 读取 PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupPolicy 的候选枚举与兜底顺序，判断其是否同时覆盖 legacy Activity 与 theseus Compose 弹层。
[28] 复核 detail_java_moss/detail_kotlin_moss 与 pgc_player_moss/pgc_view_moss 的调用者清单在两版之间是否完全一致，排除仅计数相同而调用者已替换的情况。
[29] 真机验证（需运行条件）：进入 UGC 详情页、Opus 详情页、番剧详情页与播放页，各采集 Activity 栈、类加载器来源与模块 Hook 安装/命中日志，判定四类路径的实际启用栈。
[30] 在平板/宽屏与未登录条件下重复上述采集，检查是否存在按屏宽、登录态或服务端开关切换的并存栈与未归类调用者。
- [31] 真机复现 PGC 自动弹窗场景，记录弹窗类名与 PgcAutoActivityPopupFeatureInstaller 是否命中，验证弹窗定位器在缩容后的 theseus 栈上是否仍有锚点。
[32] 对模块日志增加（在验证构建中）定位器解析结果的可见性记录，避免 runCatching 吞掉 null 导致适配问题被误判为宿主样式变化。
[33] 记录所有验证所用模块源码文件哈希（工作树 dirty，source_tree_sha256=37745f8f…，head 5422fad1…），以便结论可追溯到具体快照。
[34] 把本单元结论标注为静态+推断，待上述真机与类级 diff 结果回填后再评估是否升级为已确认变化；在此之前不宣称任何路径适配通过。
[35] 对 9180200/9180100 生成 player_java、player_kotlin、danmaku_kotlin 三家族类级清单与方法体 sha256 差集，判定指纹变化属重命名、重排还是实现替换。
- [36] 真机抓安装期日志，记录 PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerCapabilityAccess、SponsorPlayerLocator 的解析命中与兜底分支。
[37] 真机统计播放页缓冲、倍速、画质、赞助商 Hook 回调次数，并与 9180100 同场景对比，确认路径是否启用。
[38] 覆盖平板/宽屏与不同播放器入口，确认是否存在并存栈与切换条件导致的定位差异。
[39] 对 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 阅读源码，确认安装条件、屏蔽判据、失败兜底与服务端开关读取路径。
[40] 真机开关弹幕净化，对比前后弹幕条数与过滤命中计数，验证策略实际生效。
- [41] 对 base.apk 离线检索旧弹幕类名与包前缀，确认 danmaku_legacy 的 absent 是功能移除还是归类口径差异。
[42] 补登记 com.bapis.bilibili.live.approom.api.grpc.v1.KDanmuMoss 等直播弹幕协议的消费者，判断是否与点播弹幕共用净化策略。
[43] 在报告中保持 player/danmaku 各路径 status 为静态矩阵原值，不因计数接近而改写为已适配。
[44] 对 story_native 与 mine_native、mine_account_model 分别取 target/baseline 完整类清单做差集，并按 method_bodies_sha256 配对区分改名与真实改动（复核阶段可用的最小补证任务）。
[45] 读取 StoryActionIconsFeatureInstaller.kt 与 StoryPurifyFeatureInstaller.kt，记录其候选类名/方法签名与解析失败时的兜底分支，逐条对照 story_native 差异类。
- [46] 读取 HomeVerticalDetailFeatureInstaller.kt/HomeVerticalDetailRouting.kt，确认 story 相关路由是否存在多路径（原生/Compose）并存与切换条件，弥补 story_kotlin absent 的覆盖缺口。
[47] 读取 MineComponentFilterFeatureInstaller.kt、MineVipFeatureInstaller.kt、MineComponentSnapshot.kt 与 MineComponentSnapshotStore/QueryClient/QueryContract，确认 mine 页三条入口的安装条件与共享快照协议消费者。
[48] 在真机 9180200 上抓取 story 页与 mine 页的安装期定位日志，核对定位器命中/兜底结果与 runtime_enabled，记录 Hook 实际生效项。
[49] 核对 story 页是否存在 Opus/动态等跨家族消费者，确认 StoryMoss/KStoryMoss 类协议是否有除 story_native 之外的调用方，避免把单家族观察当作页面全覆盖。
[50] 对 mine 页检查宽屏/平板与服务端开关分支，确认组件过滤与 VIP 展示在不同布局下是否走不同宿主类。
- [51] 确认 story_kotlin absent 是否由抽取前缀未覆盖导致：用已知有类的前缀做反证，再决定是否需要重跑该家族抽取。
[52] 记录本轮源快照 working_tree_dirty=true 的文件哈希，复核阶段以相同哈希重读源码，避免工作树变动影响结论追溯。