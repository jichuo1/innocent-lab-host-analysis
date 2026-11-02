## 模块源码快照

- 来源：published
- 捕获时间（UTC）：2026-10-15T14:19:32.431433Z
- 源码 HEAD：5422fad1e3f798252619d610a0504573ff47211b
- 快照 SHA-256：2fa2d3b70f73fa431ed83267a9519c726a41b67de39eb7ee785813de39067120
- 源码树 SHA-256：37745f8f27c41c22eab6e0bc780c6af700d650f49c3f004f862bf9c5f1548a5c
- 含未提交修改：True
- 时效状态：historical

复用历史静态证据 run 41310041821；本轮只重新执行 AI 审查。模块源码保留历史快照。

## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2501 | 289 | 1142 | static_invoke_observed |
| comment_legacy_v2 | 579 | 0 | 754 | static_invoke_observed |
| comment_native_exp3 | 58 | 0 | 56 | static_invoke_observed |
| comment_native_legacy | 176 | 0 | 245 | static_invoke_observed |
| comment_native_next | 49 | 0 | 58 | static_invoke_observed |
| comment_other_ui:(root) | 228 | 2 | 500 | static_invoke_observed |
| comment_other_ui:adapter | 7 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 218 | 0 | 103 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 242 | 32 | 306 | static_invoke_observed |
| danmaku_kotlin | 137 | 3 | 164 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1973 | 25 | 525 | static_invoke_observed |
| detail_theseus_united | 4679 | 98 | 4180 | static_invoke_observed |
| dynamic_compose | 1421 | 182 | 287 | static_invoke_observed |
| dynamic_legacy | 3254 | 105 | 2136 | static_invoke_observed |
| dynamic_opus | 1370 | 95 | 227 | static_invoke_observed |
| dynamic_other:appointment | 32 | 4 | 19 | static_invoke_observed |
| dynamic_other:card | 414 | 89 | 307 | static_invoke_observed |
| dynamic_other:commonCore | 26 | 0 | 62 | static_invoke_observed |
| dynamic_other:commonPerf | 13 | 1 | 2 | static_invoke_observed |
| dynamic_other:commonUi | 24 | 5 | 7 | static_invoke_observed |
| dynamic_other:lightBrowser | 80 | 19 | 32 | static_invoke_observed |
| dynamic_other:playershare | 1 | 0 | 3 | static_invoke_observed |
| dynamic_other_legacy | 2099 | 5 | 2196 | static_invoke_observed |
| home_legacy | 782 | 88 | 203 | static_invoke_observed |
| home_new_frame | 190 | 33 | 54 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 326 | 7 | 94 | static_invoke_observed |
| pgc_legacy | 345 | 0 | 301 | static_invoke_observed |
| pgc_theseus | 2258 | 134 | 982 | static_invoke_observed |
| player_java | 953 | 0 | 3300 | static_invoke_observed |
| player_kotlin | 480 | 37 | 891 | static_invoke_observed |
| search_compose | 3131 | 562 | 617 | static_invoke_observed |
| search_native | 1704 | 2 | 2865 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2974 | 45 | 1470 | static_invoke_observed |

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
- dynamic_other:playershare: new_family_candidate
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
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/HistoryMoss;: protocol_signature_or_call_path_changed
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

{'added': 5, 'removed': 0, 'changed': 7905}

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

本单元审计 9.18.0 评论区 5 条已登记路径与动态页 3 条已登记路径，基线 9.17.0。全量静态矩阵显示 8 条路径 evidence 均为 static_invoke_observed、runtime_enabled 未知、module_coverage 需安装器复核，故本报告不给出通过结论。结构层面：评论区五族并存，compose 族 +71 类/+6 compose 方法/+39 调用边，native_legacy 类数 -16、边 -18，native_next 类数不变但边 66→58，说明"指纹变化≠新样式"需要先排混淆与 DEX 重排。动态页 dynamic_compose 类数 1234→1421（+187）、compose 方法 151→182、边 232→287，是本次最显著增量，抽样到 kntr/app/following/followinglist 下的 Compose 状态持有者。两页 MOSS 协议定义/调用计数逐项不变（comment 50/50、130/23；dynamic 134/134、382/27），但计数相等不证明字段或路由未变。已核实的模块源码解析点包括 CommentClassicStyleLocator 的 DD 布尔读取签名与 kntr 适用性门控，以及 DynamicPurifyFeatureInstaller 的 Moss 同步/异步/Kotlin 包装三重安装口径；两者对 9.18.0 的实际命中均未验证。

本单元覆盖 home / search 两页共四条登记路径（home_legacy、home_new_frame、search_native、search_compose），对比 9.17.0（基线）与 9.18.0。四条路径静态证据值均为 static_invoke_observed，runtime_enabled 全部 unknown，module_coverage 全部 requires_installer_review，故本报告只能给出变化与验证任务，不判定适配通过。事实：两页全部家族 fingerprint 均变化，但方法定义数/类数/调用边数单位不同，不能相除推覆盖率；home_legacy 类数 744→782（+38）而外部调用边 228→203（−25），home_new_frame 类数 198→190、边 51→54，search_native 1704/2865→1701/2880，search_compose 3136/607→3131/617，compose_methods 除 home_legacy 87→88 外均持平。search_kotlin_moss（52 定义/18 边）与 search_java_moss（24/22）计数与基线一致，但调用者样本只落在 search_compose 的 kntr.app.search.* 仓库，Java 侧跨家族消费者未取证。推断：调用边减少可能来自 R8 内联或代码迁移，不证明 Hook 点消失。源码侧已核实 SearchHomeRecommendLocator 依赖硬编码包名/短名枚举（E017），HomeFrameListHook 依赖构造器全覆盖与 FilteredTabList 标记（E018）；其余首页安装器未读，保持未知。快照工作树 dirty，按文件哈希追溯（E017/E018 各自 sha256）。

本单元仅覆盖 detail 与 pgc 两页，静态矩阵来自 E000/E005/E006（样本 9.18.0 a12d3eac…，基线 9.17.0 b3950fd3…，同证书）。detail 页三路径中 detail_legacy 两侧均为 absent 且空集指纹一致，detail_theseus_ugc 与 detail_theseus_united 为 static_invoke_observed；pgc 页两路径均为 static_invoke_observed。变化集中在家族结构哈希与调用边：detail_theseus_united 类 4617→4679 而外部调用边 4196→4180；detail_kotlin_moss 定义 76 不变而调用边 38→34；pgc_legacy 类 366→345、调用边 455→301；pgc_theseus 调用边 904→982、compose 方法 131→134；pgc_player_moss、pgc_view_moss 与 detail_java_moss 计数两侧一致。所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review，complete_coverage=false，家族摘录每族仅 2 类样本，源码 source_dirty=true。结论仅到静态调用被观测，不能判定适配通过，也不构成样式新增或功能消失的证明。

本单元仅覆盖 player 与 danmaku 两页，样本 9.18.0 (9180100, sha256 a12d3eac…eeb6cb9, arm64-v8a) 对基线 9.17.0 (9170300, sha256 b3950fd3…ac7b57f)，两者证书一致。事实：player_java 类 954→953、外部调用边 3308→3300、compose 仍 0、指纹变化；player_kotlin 类 458→480、边 836→891、compose 仍 37、指纹变化；danmaku_legacy 两侧均 absent（classes=0，空集指纹 4f53cda1…）；danmaku_kotlin 类 135→137、边 162→164、compose 仍 3。协议面：player_java_moss 18 定义/2 边、player_kotlin_moss 34 定义/3 边两侧不变；danmaku_java_moss 22 定义/20 边不变，danmaku_kotlin_moss 46 定义不变而实际调用边 10→12。complete_coverage=false，runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review；resource changed 7905 只说明资源哈希变动，结构哈希与计数变化不等于新样式。源码快照 working_tree_dirty=true 且 freshness=historical，本轮 APK access disabled，player/danmaku 相关模块源码（DanmakuPurifyFeatureInstaller、PlayerBufferLocator 等）未被实际读取，相关 Hook 覆盖一律记为未知。

本单元只覆盖 story 与 mine 两页、共四条登记路径，全部为静态证据层结论：story_native、mine_native、mine_account_model 的 evidence 值为 static_invoke_observed，story_kotlin 两侧均为 absent。事实：9.18.0 对 9.17.0，story_native 由 2954 类/44 compose 方法/1439 外部调用边/指纹 f410eec8… 变为 2974/45/1470/28025f3f…（E009）；mine_native 由 327/7/96/ae6321bd… 变为 326/7/94/96810670…，mine_account_model 计数完全不变（132/0/43）但指纹由 ebf9deed… 变为 abd9520a…（E010）。推断：mine_account_model 同计数异指纹更符合混淆改名或 DEX 重排；story_native 的小幅增量无法区分编译产物变化、包装层增删与真实新样式。四个家族的 runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review，注册协议为空，本页无面对面协议消费者证据；预取未给出这四个家族的类样本，故不作样式定性。全程未验证任何 Hook 真机生效，APK 访问关闭，未做新反编译，缺口保留为未知。

## 各页面评估

### comment

评论区在 9.18.0 仍是五族并存：legacy_v2（579 类/754 边）、native_legacy（176/245）、native_next（49/58）、native_exp3（58/56）、compose（2501/289 compose 方法/1142 边），无任何一族在静态矩阵中消失，因此不能把类数下降解读为页面功能下线。相对 9.17.0，legacy_v2 边 743→754 而类数 580→579，属"少类多边"，可能是方法内联/迁移或边解析变化；native_legacy 192→176、边 263→245 同步收缩，需先排查 DEX 重排与死代码裁剪；native_next 类数 49 不变但边 66→58、指纹改变，是最典型的"结构哈希变化但类集合不变"情形；native_exp3 类数 55→58、边持平 56；compose 族 2430→2501、283→289、1103→1142，增量方向与动态页 Compose 扩张一致。协议侧 comment_java_moss 50 定义/50 边、comment_kotlin_moss 130 定义/23 边，两侧完全一致，只说明协议面在本次统计口径下稳定，既不证明协议无字段变更，也不证明调用方在真机走到。模块侧可核实的具体解析点：CommentClassicStyleLocator 以 com.bilibili.lib.dd.DeviceDecision.getBoolean（实例、返回 boolean、p[0]=String、p[1]=boolean）与 kntr.base.dd.IDeviceDecisionKt.getBool/getBool$default（静态、4 或 6 参）作为经典样式读取器，并由 kntr.common.comment.entry.CommentSectionComposeFragment 或 kntr.common.comment.card.model.comment.CommentModel 是否存在决定 kotlin 家族适用性；该定位器明确接受多候选时按类去歧义、超 16 个候选返回空，因此宿主若新增同名重载或迁包，会静默落到空读取器而不是报错。本轮证据未包含 9.18.0 中上述四个锚点类/方法的实际存在性，故经典样式族的模块覆盖仍为未知。此外 prefetch 明确说明 comment 侧省略了类样本（有界摘录），深挖样本仅 5 个类、且这 5 个类的 compose_signatures 均为空，属抽样，不能代表 2501 类的整体实现。

证据：E000, E001, E012, E014

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类数 580→579、外部调用边 743→754、compose 方法 0→0，指纹由 0a6d90ff… 变为 c5e0f691…；少一类而多 11 条边，不符合整体下线特征。
- 可能影响：模块侧 legacy 复制/净化桥（CommentLegacyCopyBridge、CommentPurifyFeatureInstaller）若按类名或方法描述定位接收者，可能因边端点迁移而不命中；是否受影响取决于解析点实现，本轮未读该文件。
- 验证：拉取两侧 legacy_v2 边端点列表做差集，确认新增 11 条边是否落到同一接收者；真机在旧样式页面打点 legacy 桥的安装与命中日志，比对 9.17.0 同名日志。
- 证据：E001, E000

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类数 192→176（-16）、边 263→245（-18）、compose 方法 0，指纹 62bf1867…→29fb0f08…；类与边同向收缩。
- 可能影响：原生绑定目录（CommentNativeBindingCatalog）与补充桥（CommentNativeSupplementBridge）以类/成员登记为定位依据，收缩可能导致若干登记项解析失败并走兜底或跳过；具体受影响登记项未知。
- 验证：把 9.17.0 与 9.18.0 的 native_legacy 类名集合做差，标记消失的 16 个类并核对是否在 NativeBindingCatalog 中出现；随后在原生评论区抓取安装器 resolve 失败日志。
- 证据：E001, E000

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类数保持 49、边 66→58（-8）、compose 方法 0，指纹 49f54dff…→2449027d…；类集合稳定而边减少，属结构哈希变化不等于新样式的典型样本。
- 可能影响：next 家族仍静态存在，但调用边减少可能意味着部分入口被合并到别的路径；若模块仅为 next 安装 Hook，可能出现"装上但应用层不走"的空覆盖。
- 验证：对 8 条消失边逐条定位调用方方法，判断是否被内联到 legacy_v2/compose 路径；真机在 next 开关打开与关闭两种状态下各抓一次 hook 命中计数。
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类数 55→58（+3）、边 56→56 持平，指纹 51ab749a…→67ad0490…；规模基本持平但结构哈希变化。
- 可能影响：exp3 属实验通道，模块若将其视为候选兜底，需确认新增 3 类是否引入新的读取入口；当前无证据表明它成为主路径。
- 验证：核对新增 3 类的父类与是否有 Compose/LazyList 字段，判断是否为实验包装层；结合服务端实验开关真机切换观测实际渲染路径。
- 证据：E001, E000

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类数 2430→2501（+71）、compose 方法 283→289（+6）、边 1103→1142（+39），指纹 4d15c77d…→9c77cdfc…；增量为五族最大。
- 可能影响：Compose 路径是复制桥/净化桥与回复按钮 Compose 实现的主要落点，规模增长意味着新增可组合函数可能不在现有 Hook 名单内，出现"部分 Compose 文本未处理"的风险；但新增类是否被实际组合调用未知。
- 验证：用 CommentComposeViewAccess 与 CommentComposePurifyBridge 的白名单/签名匹配逻辑，对照 9.18.0 新增的可组合方法描述，列出未覆盖项；真机在 Compose 评论区分别验证正文、表情与复制入口。
- 证据：E001, E012, E014

### dynamic

动态页三族（legacy 3254/105/2136、compose 1421/182/287、opus 1370/95/227）在 9.18.0 全部仍静态可见，不存在某条路径消失的静态证据。相对 9.17.0 的关键变化集中在 dynamic_compose：类数 1234→1421（+187，约 +15%）、compose 方法 151→182、外部边 232→287，是唯一大幅正向增长的族；dynamic_legacy 类数 3261→3254、compose 方法 103→105、边 2060→2136，属"略减类、增边"；dynamic_opus 1376→1370、94→95、边 230→227，基本持平但指纹改变。深挖抽样显示 compose 族落在 kntr.app.following.followinglist 包，样本类持有 LazyListState、CoroutineScope、FollowingListViewModel、MutableState，并有 ui/wide 引用，说明该族至少包含关注列表与宽屏布局的 Compose 状态持有者；但 5 个样本的 compose_signatures 全为空，说明族边界按类归属而非可组合签名划分，不能据此断言新增了可组合 UI 样式。模块侧可核实的安装口径来自 DynamicPurifyFeatureInstaller：它按 dynamic.purify.moss 解析 DYNAMIC_MOSS_CLASS，对每个 feed 同时安装同步方法、异步方法与 Kotlin `*MossKtxKt` 包装（以 KavaMemberLookup 读取 K_MOSS_CLASS 声明方法名集合判断 kotlinExpected），并在无可用 feed 时返回 missing("no-dynamic-hook-point")；其注释自述版本覆盖为离线核对的 9.7.0–9.11.0，未覆盖 9.18.0。因此 9.18.0 的 Purify/Tabs 是否仍能在 Moss 边界上装到，只能靠安装器日志确定，静态调用存在不等于 Hook 生效。另需注意：seed 的 unregistered_protocols 含 app/dynamic/v2 的 OpusMoss/KOpusMoss 与 DynamicMoss，而页面 protocols 只登记 dynamic_java_moss 与 dynamic_kotlin_moss，Opus 专属 Moss 是否存在跨族消费者在现有证据中不可判定。两类协议计数（134/134、382/27）两侧一致，同样只能说明定义与边数量口径稳定。

证据：E000, E002, E011, E013

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类数 3261→3254（-7）、compose 方法 103→105（+2）、边 2060→2136（+76），指纹 b7565e6b…→1aee4b8c…；边增长幅度远大于类变化。
- 可能影响：legacy 仍是大头路径，边增多可能是卡片渲染入口下沉或新卡片类型接入；模块若在 legacy 卡片层级做净化，可能出现部分新卡片不经旧 Hook 点的情况，当前无法确认。
- 验证：对 +76 条新增边按接收者聚类，确认是否集中到新的卡片 ViewHolder；真机分别以综合页与视频页标签抓取净化命中日志，核对 DynamicPurifyFeatureInstaller 报告的 feed 数与 installed 数。
- 证据：E002, E013

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类数 1234→1421（+187）、compose 方法 151→182（+31）、边 232→287（+55），指纹 da87e05c…→76028ed3…；三指标同向显著增长，为本次最大结构变化。
- 可能影响：抽到的 kntr.app.following.followinglist 类持有 LazyListState/CoroutineScope/FollowingListViewModel，并引用 ui/wide，提示 Compose 侧列表与宽屏布局可能是新增消费者；若动态页部分卡片改由 Compose 渲染，现有面向 legacy 的净化/显隐 Hook 将出现覆盖缺口，但新增类是否在动态页路由中被组合调用未知。
- 验证：在 9.18.0 中确认 kntr.app.following.followinglist 的入口方法与动态页 tab 是否互达（检查 who calls 该包的 ComposableLambda 与 ViewModel）；真机在宽屏/平板与手机两种配置下记录 Compose 路径的文本与条目渲染日志，并与 legacy 路径命中数对比。
- 证据：E002, E011, E013

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类数 1376→1370（-6）、compose 方法 94→95（+1）、边 230→227（-3），指纹 0ea59ce6…→72569a39…；规模基本持平但指纹改变。
- 可能影响：Opus 路径静态仍在，但 seed 的 protocols 未登记 Opus 专属 Moss（unregistered_protocols 列出 KOpusMoss/OpusMoss），模块是否在 Opus 加载边界有兜底未知；若仅依赖 dynamic_java_moss/dynamic_kotlin_moss，Opus 图文可能绕过净化。
- 验证：确认 9.18.0 中 KOpusMoss/OpusMoss 是否有来自动态页的调用方，以及是否与 DynamicMoss 共用响应容器；真机在动态页 Opus 卡片上验证关键词过滤与推广卡片剔除是否生效。
- 证据：E002, E000

### home

home 两条路径并存：home_legacy 782 类 / 88 compose 方法 / 203 外部调用边，基线 744 / 87 / 228；home_new_frame 190 类 / 33 / 51，基线 198 / 33 / 51→54。两家族 fingerprint 均变化，但类数与调用边数不是同一单位，不能换算为覆盖率，也不能由哈希变化断言出现新样式。已读源码显示新框架过滤边界 HomeFrameListHook 挂在 tab/bottom 列表字段上、以 FilteredTabList 标记防止 copy() 回写覆盖全量，并对嵌套构造做同线程深度计数（E018）：该设计对构造器集合的变化敏感，而 home_new_frame 类数减少 8 是需要区分的点。home_legacy 调用边减少 25 与类数增加 38 方向相反，可能是 R8 内联/重排或真实调用点迁移，静态不可判定。模块侧 HomeFrameTabLocator、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller 等本单元未读取，installer 覆盖与兜底路径保持未知。结论：需要安装期定位日志与真机勾选隐藏验证补齐。

证据：E003, E015, E018

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类数 744→782（+38）、compose 方法 87→88、外部调用边 228→203（−25），fingerprint 08b1d4…（9.18.0）对 1ae88d…（9.17.0）；抽样类仍位于 tv.danmaku.bili.ui.main2（StartupFragmentV2、HomeFragmentV2），未见包级迁移。
- 可能影响：若调用边减少来自真实被移除的调用点，依赖旧调用边定位的首页 banner/顶栏/推荐净化 Hook 可能挂不上；若只是内联或 DEX 重排，则影响为零。当前无法区分。
- 验证：对 9.17.0 与 9.18.0 同名类做方法体哈希对拍，列出 9.18.0 中消失的调用边目标；真机在首页分别开启 banner 隐藏、顶栏净化、推荐过滤并观察安装期日志是否报告定位失败。
- 证据：E003, E015

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 198→190（−8）、compose 方法 33→33、外部调用边 51→54（+3），fingerprint c2fe89…（9.18.0）对 d94225…（9.17.0）；家族内存活的 tab/bottom 列表数据类未在抽样中出现。
- 可能影响：HomeFrameListHook 依赖对数据类全部构造器的挂载及 FilteredTabList 标记识别，若构造器集合或嵌套形态变化，隐藏项可能过滤不掉，或过滤后勾选面板无法恢复（源码层面已见该风险的设计约束，运行结果未知）。
- 验证：反编译 9.18.0 确认 tab/bottom 列表数据类构造器数量与是否存在默认参数构造器嵌套；真机隐藏一个 tab 后重启、再打开勾选面板确认该 tab 仍列出并可恢复。
- 证据：E003, E018

### search

search 两条路径并存：search_native 1704 类 / 2 compose 方法 / 2865 外部调用边（基线 1701 / 2 / 2880），search_compose 3131 / 562 / 617（基线 3136 / 562 / 607）。共同协议计数与基线完全一致（search_java_moss 24 定义 / 22 边，search_kotlin_moss 52 定义 / 18 边），但定义数与调用边数不是覆盖率口径，且 Kotlin 侧调用者样本全部落在 kntr.app.search.* 仓库（aggregate、comic、repository），属 search_compose 家族，Java MOSS 的调用者样本本轮未取到，跨家族消费者仍未知。源码侧已核实 SearchHomeRecommendLocator 以硬编码包名与短名白名单定位投递宿主，存在约 20 根类 × 36 后缀的有界枚举，并用 singleOrNull 做唯一性判定（E017）：任一条件不满足即返回 null 并在安装期静默跳过，而非报错。search_compose 类数 −5 与 fingerprint 变化不足以判定该结构仍在原处。结论：搜索净化/猜你想搜相关 Hook 的安装期命中情况需要反编译确认类清单与真机日志双证。

证据：E004, E016, E017

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数 1701→1704（+3）、compose 方法 2→2、外部调用边 2880→2865（−15），fingerprint 27b995…（9.18.0）对 71eaa4…（9.17.0）；search_java_moss 定义 24 / 实际调用边 22 与基线相同。
- 可能影响：Java MOSS 定义与边数持平说明协议面未变，但 15 条外部调用边减少可能影响基于旧调用点定位的搜索请求侧 Hook；由于未取得 Java MOSS 调用者样本，无法判断 search_native 类是否仍是这些定义的消费者。
- 验证：取 search_java_moss 的 caller_samples 或反编译 SearchMoss 实现类，确认 search_native 家族是否存在调用 SearchMoss 方法的调用边；真机在旧（原生）搜索页触发一次搜索，观察搜索净化安装日志是否命中。
- 证据：E004, E016

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数 3136→3131（−5）、compose 方法 562→562、外部调用边 607→617（+10），fingerprint 8cf08a…（9.18.0）对 b64bbc…（9.17.0）；Kotlin MOSS 调用者样本（E016）集中在 kntr.app.search.aggregate/comic/repository 下的仓库类，调用 searchOGV、searchComic、searchReserve、searchAddReserve 等。
- 可能影响：请求侧确实由 Compose 家族仓库发起，但搜索首页推荐投递宿主与主搜索状态类依赖 com.bilibili.search2.discover.*、com.bilibili.search2.main.data.* 的短名与类型签名（E017），若这些类改名或迁移，定位返回 null 并静默跳过，表现为「开关开着却没效果」。
- 验证：反编译 9.18.0，核对 com.bilibili.search2.discover.{a..z,SearchDiscoverViewModel} 与 main.data.{a..z} 是否存在，检查 getHistoryList、单参 List<SearchSquareType> 的 void 接收方法、discover 类型字段与 NegativeFeedback 构造器参数集是否仍唯一；真机在 Compose 搜索页验证猜你想搜/默认词清理。
- 证据：E004, E016, E017

### detail

detail 页登记三条路径。detail_legacy 在目标与基线两侧都是 absent，指纹同为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945，说明该家族名在两次采集中都没有解析出类集合，这是登记口径的空结果，不是 9.18.0 才出现的删除；旧原生详情实现是否仍随宿主分发、以及 DetailViewPurifyFeatureInstaller / DetailModulePurifyFeatureInstaller 是否有可用 legacy 定位点，静态不可判定（E005）。detail_theseus_ugc 两侧均为 static_invoke_observed：类 1976→1973、外部调用边 529→525、compose 方法 25→25、指纹改变，量级变化很小，更接近混淆改名/DEX 重排或重复包装层折叠，而非新样式（E005）。detail_theseus_united 类 4617→4679（+62）但外部调用边 4196→4180（-16）、compose 方法 98 不变，类增边减的组合更符合新增内部包装/lambda 层，不能据此推断新样式引入（E005）。协议面 detail_java_moss 定义 32、真实调用边 35，两侧完全一致；detail_kotlin_moss 定义 76 不变、真实调用边 38→34，减少 4 条需要按调用方逐条定位，且方法定义数与调用边数不是同一单位，不能相除换算覆盖率。深挖样本显示评论区 Compose 家族在目标包内规模很大（2501 类、289 compose 方法、1142 条外部调用边，E012，有界摘录），且经典样式定位依赖 DeviceDecision 的 comment.next_appearance 锚点与 CommentV3Fragment / CommentSectionComposeFragment 双入口（E014），因此 detail 页是多入口并存栈，前几个类样本不足以代表整套实现，实际启用样式仍需真机与安装器侧确认。

证据：E000, E005, E012, E014

#### 路径：detail_legacy

- 状态：absent
- 变化：目标与基线两侧 evidence 均为 absent，指纹同为空集哈希 4f53cda…，类数/调用边/compose 方法两侧都为 0，没有可比较的结构差异。
- 可能影响：无法判断宿主是否已不再携带旧原生详情实现，也无法判断 DetailViewPurifyFeatureInstaller、DetailModulePurifyFeatureInstaller 的 legacy 定位点是否有落点；该路径模块覆盖仍为 requires_installer_review。不能据此认为旧原生路径被废弃或页面功能消失。
- 验证：在 9.18.0 真机上按 CommentClassicStyleLocator 的 NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision、NATIVE_ENTRY=com.bilibili.app.comment3.CommentV3Fragment 及锚点 comment.next_appearance 做装载探测（E014），并导出 dex.assist.comment_classic 诊断；若类可装载而 detail_legacy 聚合仍为空，应把该 absent 记为登记口径缺口而非宿主删除。
- 证据：E000, E005, E014

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1976→1973、外部调用边 529→525、compose 方法 25→25，家族指纹由 729a51a7… 变为 ed2491aa…；变化幅度与混淆改名或重复包装层合并一致。
- 可能影响：DetailUnitedModulePurifyFeatureInstaller / DetailUnitedPresentationPurifyFeatureInstaller 若依赖固定成员名或固定调用边形态解析 UGC 模块，可能部分匹配点漂移；runtime_enabled=unknown，无法确定这些边在真机被走到。
- 验证：对 9.17.0 与 9.18.0 的 detail_theseus_ugc 抽样（超过 2 类）做方法体哈希逐类对比，并把减少的 4 条调用边还原到具体调用方类与方法描述符，确认是内联/折叠还是入口迁移；同时在真机读模块安装日志中该家族定位命中数。
- 证据：E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4617→4679（+62）、外部调用边 4196→4180（-16）、compose 方法 98→98，指纹由 cafecc5c… 变为 cce82b5d…；类增而边减，方向不一致。
- 可能影响：可能是新增内部包装类/匿名类导致类数上升、同时部分外部调用被折叠；DetailUnitedModulePurifyPolicy 与 DetailUnitedPresentationPurifyPolicy 的判据若绑定具体类层级，需要重新确认落点，暂不能说是新样式。
- 验证：抽取 +62 的新增类样本并检查是否为 lambda/包装层；对 98 个 compose 方法做前后签名与调用方比对；在真机 9.18.0 上对 united 版详情页采集模块安装/未命中日志，确认策略类实际读取的字段在两侧是否仍存在。
- 证据：E005, E012

### pgc

pgc 页两条路径均为 static_invoke_observed，且都登记了结构变化（E006）。pgc_legacy：类 366→345（-21）、外部调用边 455→301（-154）、compose 方法两侧均为 0、指纹由 a7bb4411… 变为 14717f3a…。调用边降幅远大于类数降幅，属于需要优先归因的变化：既可能是 PgcAutoActivityPopupLocator / PgcAutoActivityPopupPolicy 所依赖的旧原生入口被合并或迁移到 Theseus 容器，也可能是 R8 内联、去虚拟化、重复包装层折叠或 DEX 重排造成的边消失。pgc_theseus：类 2262→2258、compose 方法 131→134（+3）、外部调用边 904→982（+78）、指纹由 1b944d7c… 变为 b9f79e23…；compose 入口与调用边同向上升，与「能力向 Theseus 迁移」相容，但同样可由新增包装层解释。协议面 pgc_player_moss（定义 12、调用边 3）与 pgc_view_moss（定义 14、调用边 7）在两侧完全一致，说明变化集中在 UI 家族内部，而非 PGC 播放/详情协议定义本身改变。两路径 runtime_enabled 均为 unknown、module_coverage 均为 requires_installer_review，因此不能确认 PGC 自动弹窗策略在 9.18.0 上生效或失效；本页未读取服务端开关与平板/宽屏切换条件，服务端 A/B 若无结构变化则静态不可见，不能宣称所有样式已穷尽。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类 366→345、外部调用边 455→301（约 -34%）、compose 方法 0→0、家族指纹由 a7bb4411… 变为 14717f3a…；pgc_player_moss / pgc_view_moss 的定义与调用边计数两侧一致，变化限于该 UI 家族内部。
- 可能影响：若 PgcAutoActivityPopupLocator 的候选基于旧原生的类集合或调用形态，9.18.0 上可能出现候选命中数下降、歧义或定位失败，进而使 PgcAutoActivityPopupFeatureInstaller 少装 Hook；但边数下降也可由内联/折叠造成，不能等同于功能删除。
- 验证：真机 9.17.0 与 9.18.0 分别在 PGC 详情页、PGC 播放页采集定位器诊断与安装日志，记录 legacy 路径候选数与命中数；对 pgc_legacy 抽样超过 2 类做方法体哈希与方法描述符对比，并把减少的调用边逐条回溯到调用方，区分内联折叠与入口迁移。
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2262→2258、compose 方法 131→134（+3）、外部调用边 904→982（+78）、指纹由 1b944d7c… 变为 b9f79e23…；compose 入口与调用边同向增加。
- 可能影响：Theseus 版 PGC 容器内 Compose 入口增加，若模块定位器按旧成员名单或旧调用边形态匹配，可能漏挂或多挂 Hook；新增 3 个 compose 方法是否为包装层尚未判定。
- 验证：对 9.18.0 新增的 3 个 compose 方法逐一定位调用方，判断是否为新包装层；在真机 Theseus 版 PGC 页面采集 PgcAutoActivityPopup 相关安装命中日志，并与 pgc_legacy 的诊断结果对照，确认实际生效路径。
- 证据：E006

### player

两条登记路径均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，故本页不存在“适配通过”结论。事实：player_java 类 954→953（-1）、外部调用边 3308→3300（-8）、compose 方法仍为 0，指纹由 ac88f659… 变为 9721f668…；player_kotlin 类 458→480（+22）、边 836→891（+55）、compose 方法仍为 37，指纹由 c539764c… 变为 9c22f386…。协议面无变化：player_java_moss 18 定义/2 实际调用边，player_kotlin_moss 34 定义/3 实际调用边，两侧完全相同，属于“家族类结构漂移但协议签名面不动”的组合，推断优先考虑 R8 混淆池改名、DEX 重排、协程包装层新增或代码在 dex 间迁移，而非新播放器样式。影响面：模块侧 PlayerBuffer/PlayerSpeed/PlayerCapability/Sponsor 等定位器若依赖固定描述符或类名枚举，-1 类与 +22 类都可能改变命中集合；若依赖返回类型/方法体语义匹配，则相对不敏感——但本轮未读这些源码，命中与否为未知。已知缺口：外部调用边数不等于方法定义数，也无从推出覆盖率；接口派发与实际启用均未被静态证据解析。最小补证：对两版 player_kotlin 全量类清单按 method_bodies_sha256 对齐，并对新增类反编译定性；真机 attach 后 dump 定位器安装日志确认点位 installed/failed。

证据：E000, E007

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类数 954→953（-1），外部调用边 3308→3300（-8），compose 方法保持 0，家族指纹 ac88f65948e4c2dc48381769b49f0307c918bce21a7fb136d0b8f7571bc5ef44→9721f668747aefd755252420160c5e3b46be5b66bb8fac37026ea486c6489b12；对应 player_java_moss 定义 18、实际调用边 2，两版相同。
- 可能影响：若模块的 Java 播放器定位依赖固定类名/描述符或类枚举，少 1 个类、少 8 条边可能使某个 Hook 点不再命中或被改名合并；协议面不变说明 Java 侧播放器 Moss 消费结构未变，故更可能是混淆/DEX 重排或代码迁移；对模块的实际覆盖率未知。
- 验证：先用 family_evidence 取 player_java 目标与基线全量 class_samples，按 method_bodies_sha256 对齐后列出消失/改名的类与方法；对差异项用 decompile_class 反编译确认是否播放器决策/缓冲相关；真机 attach 后读取 VersionAdapter 安装日志，确认 Java 侧各播放 Hook 点 installed/failed；对命中点下断点核对 invoke 是否真的发生。
- 证据：E000, E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数 458→480（+22），外部调用边 836→891（+55），compose 方法保持 37，家族指纹 c539764cee2beb77638ccd986aa6467245d91b7933ee8e6efc66a3a65414950f→9c22f386b6ce847d08411b2acf859351158e9b09e503a94f224dff2cc1060582；player_kotlin_moss 定义 34、实际调用边 3，两版相同。
- 可能影响：新增 22 类与 55 条边而 compose 方法与 Moss 协议面均不变，说明增量不像新播放 UI 样式，更像共享/协程包装类或非播放路径类被计入同一家族；若模块按类名白名单枚举 Kotlin 播放器边界，扩容会改变候选集与歧义度，需实机确认缓冲/倍速/清晰度 Hook 是否仍落到同一批方法。
- 验证：用 family_evidence 导出 player_kotlin 全量类并筛掉 compose_signatures 为空且不引用播放器包前缀的类，确认 37 个 compose 方法归属未迁移；对 2–3 个新增类做 JADX 反编译定性；真机分别进入普通播放、番剧播放、小窗/宽屏播放，观察 PlayerBufferFeatureInstaller/PlayerSpeedFeatureInstaller 是否报告点位缺失。
- 证据：E000, E007

### danmaku

本页两条登记路径状态不同：danmaku_legacy 为 absent（两侧 classes=0、边 0、空集指纹 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945），danmaku_kotlin 为 static_invoke_observed（类 135→137、边 162→164、compose 保持 3、指纹 97597a31…→97cb0f15…）。关键点是不能把 absent 读成“旧原生弹幕消失”：同一份靶包里 danmaku_java_moss 仍有 22 个定义与 20 条实际调用边且两版不变，说明 Java 侧 Moss 消费者确实存在，只是未被归入 danmaku_legacy 这个家族口径；家族归属规则本轮未读到，属未知。协议面唯一变化是 danmaku_kotlin_moss 实际调用边 10→12（定义仍 46），即新增 2 条 Kotlin 侧调用点，而类只增 2——与“新增一个消费者类、内部多一条协议调用”相容，也可能只是共用协议的新调用者，两种解释都未被排除。对模块的影响集中在 DanmakuPurifyFeatureInstaller/Policy：若按固定描述符 Hook 净化边界，新增 2 条边可能漏挂；若按类型化定位则需 install 复核，本轮未读该源码，Hook 覆盖为未知。complete_coverage=false，runtime 全 unknown，弹幕渲染样式（原生/Compose/Opus 类）与平板/宽屏、服务端开关分支均无运行证据。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线均为 classes=0、compose 方法 0、外部调用边 0，指纹同为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945（空集哈希），即该家族口径下两版都没有匹配到类，不构成版本间新增/删除。
- 可能影响：absent 只表示当前家族归属规则未命中，不能推出旧原生弹幕或弹幕净化路径已消失；同一靶包 danmaku_java_moss 的 22 定义/20 实际调用边两版不变，说明 Java 侧弹幕协议消费者仍在，可能落在其它家族或未归类调用者里；模块若以 legacy 家族类名安装净化 Hook，诊断上可能表现为“无点位”，属待验证而非已失效。
- 验证：用 protocol_evidence 取 danmaku_java_moss 全部 20 条 caller_samples 的 owner/方法描述符，逐个反编译确认所属页面与渲染栈；核对家族归属规则（包名前缀、DEX 归属或方法体哈希）以判断 absent 是口径问题还是结构缺失；真机在弹幕开关打开/关闭两种状态下抓净化 Hook 的触发日志（是否 installed、是否被调用），并在可回滚的服务端样式下对比观察。
- 证据：E000, E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类数 135→137（+2），外部调用边 162→164（+2），compose 方法保持 3，家族指纹 97597a31107d81289f3b1dc237dc47357c11a3c59bdee40e0bcacffacd7d7002→97cb0f15bd58c6ee310895c1043f3fd344e58754e40af5ab11a28cb88be9ab14；协议侧 danmaku_kotlin_moss 定义 46 不变、实际调用边 10→12（+2）。
- 可能影响：Kotlin 字符栈仍在且协议调用点净增 2，意味着弹幕拉取/发送/上报中可能多出一个调用者或一个新增调用点；模块若按固定方法描述符安装净化 Hook，新增的 2 条边可能不被覆盖，若按类型化边界解析则命中变化未知。类数与边数的同量增加也可能来自单个包装类计入，不足以证明出现新的弹幕样式。
- 验证：用 protocol_evidence 对 danmaku_kotlin_moss 做 target/baseline caller_samples 差分，取出新增 2 条 caller 的类名与方法描述符并反编译定性；确认 3 个 compose 方法在两版是否为同一批方法（按 compose_signatures 对齐）；真机开净化后观察新增调用点是否被触发，并分别验证原生播放页、宽屏/平板布局与 Opus/动态内弹幕入口。
- 证据：E000, E008

### story

story 页只登记两条路径。story_native 在 9.18.0 相对 9.17.0 出现小幅结构变化：类数 2974←2954、compose 方法 45←44、外部调用边 1470←1439、结构指纹 28025f3f…←f410eec8…（E009 两侧摘要）。这属于「结构哈希变了」而非「新样式已确认」：+20 类、+1 compose 方法、+31 边的量级同样可由 Compose 编译器产物差异、内联 lambda 增删、MOSS/KTX 包装层增删或类迁移解释，预取没有下发任何 story 类样本或调用方，无法据类名判断是否出现了新的原生/Compose 并存栈。story_kotlin 在两侧均为 0 类、0 compose 方法、0 外部调用边，指纹同为空集哈希 4f53cda1…，即在本采集口径下该家族不可见；这可能表示 story 的 Kotlin/Compose 实现被归并进 story_native（该家族已有 45 个 compose 方法），也可能表示本页尚未迁移，预取不足以区分。模块侧只知存在 StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、HomeVerticalDetailFeatureInstaller 等源码文件，未逐点读取其定位成员，故「story 定位点在 9.18.0 是否仍命中」为未知。结论：静态调用存在，运行开关与安装器覆盖均未验证，不做适配通过判断。

证据：E009, E013, E018

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：9.18.0 为 2974 类 / 45 compose 方法 / 1470 外部调用边 / 指纹 28025f3f…；基线 9.17.0 为 2954 / 44 / 1439 / 指纹 f410eec8…（E009），整体小幅增长，预取未附类样本。
- 可能影响：若增量来自改类名或成员迁移，按名/构造函数解析的 story 定位点（StoryPurify、StoryActionIcons、HomeVerticalDetail 等 installer，本轮未逐点读取源码）可能装上但零命中；实际是否失效未知，不能由计数变化推定。
- 验证：对 story_native 两侧以同一参数重读 family_evidence，做类名集合差集与同名类 method_bodies_sha256 比对；对差集内的类用 decompile_class 确认是 Compose 包装/lambda 还是新页面实现；9.18.0 真机逐开关开启后抓安装日志中 resolved/miss 与回调计数。
- 证据：E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧均为 0 类 / 0 compose 方法 / 0 外部调用边，指纹同为 4f53cda1…（空集），本口径下无可观测变化（E009）。
- 可能影响：若宿主把 story 迁到 Kotlin/Compose 家族而本模块仍按原生类名定位，会出现定位落空；但 absent 不等于页面功能消失，当前也无迁移证据，影响待定。
- 验证：核查 story_native 的 45 个 compose 方法归属类是否已是 Kotlin/Compose 实现（判断家族归并口径）；对 story 入口 Fragment 类名定向 decompile_class 检查父类与调用者；向采集侧确认 story_kotlin 的归并规则是否存在双重计数或缺省合并。
- 证据：E009

### mine

mine 页登记两条路径，变化方向互不一致。mine_native：类数 326←327、compose 方法 7←7 不变、外部调用边 94←96、指纹 96810670…←ae6321bd…（E010），是「少一类、少两条边」的收缩型变化，方向与新增页面样式相反，更像去重、合成类减少或包装层合并。mine_account_model：两侧计数完全一致（132 类 / 0 compose / 43 边），但结构指纹由 ebf9deed… 变为 abd9520a…（E010）——成员数与调用边数都不变而指纹改变，最保守的解释是混淆改名、DEX 重排或方法体级微调，而不是新样式。另一个必须记录的口径问题是家族边界不等于页面边界：深挖样本显示 account/mine 侧请求资源枚举 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource 被归入 home_legacy 家族（E015），说明 mine 的账号/请求消费者可以落在本单元计数之外，单家族计数不能用来断言覆盖。模块侧 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、MineComponentSnapshot* 与 HostMineReadingCard 依赖按成员身份解析，同类改名场景下模块另有缓存 HookPoint 并用当前 ClassLoader 复验的 DEX 兜底路径（见 E014 的定位器形态，属跨家族源码先例，非 mine 本人已读实现），是否真的触发为未知。两条路径的 runtime_enabled 均为 unknown，故全部结论停留在静态调用存在层。

证据：E010, E014, E015

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：9.18.0 为 326 类 / 7 compose 方法 / 94 外部调用边 / 指纹 96810670…；基线 327 / 7 / 96 / ae6321bd…（E010），classes 与 edges 各降 1 与 2，compose 方法数不变。
- 可能影响：收缩型变化更可能来自合成类或包装层合并，但也可能有个别组件被移除；MineComponentFilterFeatureInstaller / MineVipFeatureInstaller 与快照桥若正好引用被移除成员，会表现为过滤或 VIP 分支不生效，是否发生未知。
- 验证：以相同参数重读 mine_native 两侧 family_evidence，列出仅存在于 9.17.0 的类与仅在 9.18.0 出现的类，对消失类用 decompile_class 确认是否 lambda/合成访问器；真机核对 MineComponentSnapshot 面板是否有数据、VIP 分支日志是否命中。
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：两侧计数完全一致（132 类 / 0 compose 方法 / 43 外部调用边），指纹由 ebf9deed… 变为 abd9520a…（E010），属同基数异哈希。
- 可能影响：同计数异指纹优先按改名/DEX 重排处置；若成员名或方法描述变化，账号模型侧读取（MineVipFeatureInstaller、MineComponentSnapshotQueryContract 一类命名契约）可能解析失败并走兜底或产出空快照。同时该类消费者可能统计在 home_legacy 等其它家族（E015 中 AccountMineRequestResource 即属该家族），故跨家族影响范围未知。
- 验证：对 mine_account_model 两侧同名类逐类比对 method_bodies_sha256 与字段表，区分「仅改名」与「方法体变化」；对差异类用 decompile_class 读实际读取点；真机在 9.18.0 核对账号态变化（登录/切换/刷新）时 mine 快照与 VIP 判断是否更新。
- 证据：E010, E014, E015

### F001：dynamic_compose 类数 +187、样本集中在 kntr 关注列表 Compose 状态持有者，动态页归属未确认（净化装在协议边界，不受渲染族迁移影响）
事实：dynamic_compose 从 1234 类/151 compose 方法/232 边升至 1421/182/287，指纹 da87e05c…→76028ed3…（E002、E020）。复读的 5 个样本全在 kntr/app/following/followinglist：C 持 LazyListState+CoroutineScope，D 持 State/MutableState/CoroutineScope/ui/wide/g/FollowingListViewModel 并接收 ComposableLambda 与 Function2，E 接 Function0；但这些样本 compose_signatures 全为空，说明族按类/包归属而非按可组合签名划分（E021）。因此可核实的是“Compose 相关类集合扩张”，不可核实的是“新增可组合样式”或“该实现服务于动态页”。另据 E013，DynamicPurifyFeatureInstaller 的过滤点在 DynamicMoss#dynAll/executeDynAll 与 *MossKtxKt 包装的 protobuf 边界，按返回类型解析容器，与卡片由 legacy 还是 Compose 渲染无关；因此渲染族迁移不会让关键词/推广/充电专属过滤失效，草稿原有“Compose 卡片绕过净化”的推断应撤回。推断：若这些 Composable 确被动态页复用，风险落在 UI 层显隐与位置敏感功能（E013 中 clearTopicList、upList/videoUpList 的 pos 重排、DynamicTabs 一类安装器）以及 feed 解析失败时的 missing("no-dynamic-hook-point")，这些均未取证。反例/替代解释：DEX 重排或混淆改名可让实现被重新分桶；followinglist 可能属于关注页而被族分类按 kntr 前缀纳入；服务端开关控制的样式切换不改变结构。
反例与替代解释：若调用方检索显示 followinglist 与动态页无调用边，或 9.17.0 已存在同构类只是改名，则“新增 Compose 消费者”推断被推翻；若 feed 全部安装成功且关键词/推广过滤在 Compose 卡片上生效，则“净化覆盖缺口”推断被推翻。
建议：最小补证：1) 在 9.18.0 中检索 kntr/app/following/followinglist 的 ComposableLambda/Function2 持有类调用方，确认是否与动态页 tab 互达；2) 与 9.17.0 同名包类清单做差集，区分新增实现与包迁移；3) 真机执行 DynamicPurifyFeatureInstaller，记录 dynamic.purify.moss 解析结果、每个 feed 的同步/异步/Kotlin 包装安装情况与 missing 原因（重点 no-dynamic-hook-point），并另测 UI 层显隐/tabs 功能，而不是把净化命中当作渲染族判断依据。
证据：E002, E021, E013

### F002：经典样式定位器绑定 DD 布尔读取器与 CommentV3Fragment/CommentSectionComposeFragment 入口，9.18.0 锚点存在性未取证
事实：CommentClassicStyleLocator（sha256 2ec67116…，E022）登记 NATIVE_OWNER=com.bilibili.lib.dd.DeviceDecision（方法名 getBoolean，非静态、返回 boolean、p[0]=String、p[1]=boolean）、NATIVE_ENTRY=com.bilibili.app.comment3.CommentV3Fragment、KOTLIN_OWNER=kntr.base.dd.IDeviceDecisionKt（getBool/getBool$default，静态、4 或 6 参、p[0] 为接口、p[1]=String、p[2]=boolean、p[3] 非原始类型），并只用 COMPOSE_ENTRY=kntr.common.comment.entry.CommentSectionComposeFragment 或 kntr.common.comment.card.model.comment.CommentModel 的存在决定 kotlin 家族是否适用。失败是静默的：多 declaringClass（多 owner 歧义）、单 owner 方法数 >16、候选总数 >32 都返回空；缓存描述符经 resolve 复用时要求描述符逐项相等且 singleOrNull，任一不符即整族返回空；只有 missing() 与 DIAGNOSTIC=dex.assist.comment_classic 会暴露空集合。注释侧结构确有变动：comment_compose 类 2430→2501、compose 方法 283→289，native_legacy 类 192→176、边 263→245（E001）。推断：若 9.18.0 迁包、新增同名重载或把 KOTLIN 首参从接口改为其他类型，定位器会退化为空读取器，表现为经典样式开关“开而无效”而非安装报错。当前无任何证据表明这四个锚点在 9.18.0 已缺失，故这是条件风险而非回归结论。反例/替代解释：类数变化可能纯由 DEX 重排或混淆改名引起；样式可能由服务端实验决定，读取器存在与否与页面表现无直接映射。
反例与替代解释：若锚点全部存在且描述符与 verified 一致、missing 集合为空，则“定位器失效”推断被推翻，剩余风险只在 Composable 覆盖广度；若锚点缺失而页面样式也无异常，则更可能该开关已由服务端关闭，而非模块适配退化。
建议：最小补证：1) 在 9.18.0 中确认 DeviceDecision、kntr.base.dd.IDeviceDecisionKt、com.bilibili.app.comment3.CommentV3Fragment、CommentSectionComposeFragment 与 CommentModel 的存在性，并打印 getBoolean/getBool 的完整描述符；2) 检查是否出现新的多 owner 候选或单 owner 方法数超过 16 使 select 走空；3) 读取 dex.assist.comment_classic 诊断与 CommentClassicStyleFeatureInstaller 的 missing 集合；4) 随后再用真机确认开关打开时样式是否实际变化。
证据：E022, E001

### F003：comment 侧两族 Moss 计数两侧不变，但 ReplyMoss/KReplyMoss 未登记，计数不变不能替代方法集合比对
事实：comment_java_moss 两侧均为 50 定义/50 实际边，comment_kotlin_moss 均为 130/23（E001）。同时 seed 的 unregistered_protocols 含 Lcom/bapis/bilibili/main/community/reply/v2/ReplyMoss 与 KReplyMoss，而 comment 页 protocols 只登记 java/kotlin moss 两项（E000）。推断：定义数与边数相等只说明统计口径不变；方法改名、字段增删、重载拆分或路由合并都可能不改变这两个数；回复协议族未登记意味着评论区回复链路的协议消费者没有契约级覆盖证据。反例/替代解释：若两侧生成类的方法集合确实完全一致，则本项不构成风险；protobuf 生成类整体重排也可能让计数保持而语义变化，反向同理不可由计数单独排除。局限：本轮未取两族的 caller_samples，跨家族消费者（如模块 KotlinMossReplyBridge / KotlinMossChannel 的解析条件）未核实。
反例与替代解释：若方法名/描述符差集为空且 ReplyMoss 无评论页调用方，则“协议层存在隐蔽改动或覆盖缺口”的推断被推翻；若差集非空但模块按返回类型而非方法名解析，则影响应下调为候选观察。
建议：最小补证：1) 对上述两个协议 owner 做 9.17.0 与 9.18.0 的方法名+描述符集合差集，而不是只比对计数；2) 确认 ReplyMoss/KReplyMoss 是否有评论区调用方，据此决定补登记或显式记录“不覆盖”；3) 取 comment_kotlin_moss 的 caller_samples，确认 23 条边来自哪些家族，避免以总计数代替跨族覆盖结论。
证据：E000, E001, E002

### F004：SearchHomeRecommendLocator 依赖硬编码包/短名/嵌套后缀枚举，定位失败以空值上报而无版本兜底
事实（E017，sha256 1c569369…，可见摘录）：SQUARE=com.bilibili.search2.api.SearchSquareType，GUESS=com.bilibili.search2.api.SearchReferral$Guess；DISCOVER=com.bilibili.search2.discover.，STATE=com.bilibili.search2.main.data.；ROOT_NAMES = discover + a..z，再加 discover+SearchDiscoverViewModel（共 27 项）；NESTED_SUFFIXES = a..z + 0..9（36 项）；注释说明未命中的嵌套名以 ClassNotFoundException 消耗，探测每宿主进程只在安装期执行一次并进入类缓存，quickLocate 与 Hook 回调不触发。Points 中 delivery: Delivery?、state: StatePoint? 均可空，另有 deliveryCandidateCount，注释写明它「仅用于区分宿主没有该结构 与 候选歧义，不参与功能判定」。由此可确认的是：定位依赖宿主包名/短名/嵌套后缀的固定形态，缺结构时以空值收束而非抛错或搜索兜底。9.18.0 search_compose 类数 3136→3131、fingerprint 变化（E004）；Kotlin MOSS 已下发调用者样本全部落在 search_compose 的 kntr.app.search.aggregate/repository（E016），与 discover/main.data 投递宿主定位是两条不同链路。推断：若 9.18.0 中 discover/main.data 下短名改名、嵌套后缀变双字符或投递方法签名的泛型形态变化，locate 退化并在安装期静默跳过，表现为开关开着无效果。未核验（摘录在 locate(loader 起始处截断）：singleOrNull 收束方式、getHistoryList 判据、唯一单参 List<SearchSquareType> 且返回 void 的方法判据、NegativeFeedback 3/5 参构造器判据是否与草稿描述一致；注释中「约 20 个根类」与实际 27 项不一致，需按实现复核，探测成本估算随之偏高。反例：类数 −5 可能只是 DEX 重排或无关类迁出，fingerprint 变化本身不证明结构改变；若安装期日志显示定位成功且 deliveryCandidateCount=1，本推断被推翻。
反例与替代解释：可推翻本推断的证据：两包类集合与 locate 实际判据完全一致且 deliveryCandidateCount=1；或 locate 对缺结构存在非空兜底分支（摘录未覆盖，需按名重读）；或 9.17.0 与 9.18.0 对应方法体哈希一致；或真机日志显示定位成功。
建议：按名重读 SearchHomeRecommendLocator 完整 locate 实现（E017 摘录截断处之后），列出真实判据而非沿用注释；反编译 9.18.0 导出 com.bilibili.search2.discover.*、com.bilibili.search2.main.data.*、SearchSquareType 与 SearchReferral$Guess 的类清单与方法签名，逐条对拍；抓一次安装期定位日志，记录 locate 返回值、deliveryCandidateCount 与是否出现 ClassNotFoundException；真机在 Compose 与原生搜索页分别验证猜你想搜与默认词清理。
证据：E004, E016, E017

### F005：home_new_frame 类数减少 8，需确认 tab/bottom 数据类构造器覆盖与 FilteredTabList 标记仍成立
事实：HomeFrameListHook（E018，sha256 947bf3f7…）把过滤挂在 HomeTabData 列表元素的全部构造器上，用 ThreadLocal 深度计数只在最外层构造结束时处理一次，结果包成 FilteredTabList；process 遇到 source is FilteredTabList 直接 return，filterFrameTabs 在全删光时原样放行。9.18.0 home_new_frame 为 190 类 / 33 compose 方法 / 54 外部调用边，基线 198 / 33 / 51（E003），fingerprint 亦变化。证据边界：E003 对 home_new_frame 只下发 summary，未下发类样本，因此无法确认 9.18.0 中 tab/bottom 列表数据类的构造器数量与嵌套形态是否与 9.17.0 一致，也不能声称样本中「未见」该类——这是待补证项而不是已排除项。推断：若减少的 8 个类涉及该数据类或其构造器形变（新增/拆分默认参数构造器、委托静态工厂），挂载点可能缺失或深度计数不收敛，导致隐藏项失效；若构造器集合不变，行为应与基线一致。未知：HomeFrameTabLocator 与 HomeTabFilterFeatureInstaller 未读取，无法判断构造器缺失时安装器是否有兜底或失败上报。反例/替代解释：类数减少可能来自 R8 合并到既有类或无关类迁出，构造器集合不变。
反例与替代解释：可推翻本推断的证据：反编译显示构造器数量与 9.17.0 一致；或真机上述两步行为正常；或安装期日志显示构造器 Hook 全部命中。
建议：反编译确认 9.18.0 中 tab/bottom 列表数据类的构造器数量与嵌套形态；真机设置隐藏一个 tab，重启后确认列表缺项且勾选面板仍列出该项（验证 FilteredTabList 标记生效），再取消勾选确认恢复。
证据：E003, E018

### F006：home_legacy 类数 +38 与外部调用边 −25 方向相反，需区分内联/重排与真实调用点迁移
事实：home_legacy 9.18.0 为 782 类、88 compose 方法、203 外部调用边，基线 744 / 87 / 228（E003）；E015 下发样本中的 A0、A 及 userprotocol/m 均位于 tv.danmaku.bili.ui.main2，StartupFragmentV2 与 HomeFragmentV2 仅作为这些样本类的字段类型出现，另有一项 AccountMineRequestResource（main2 包内枚举，与首页导航无直接关系）。据此只能说可见样本仍落在 main2 包，不能据此断言家族内容未变或已迁移。推断：调用边减少 25 条若为真实移除，依赖具体调用点定位的首页装配 Hook（banner、顶栏、推荐净化等安装器）可能找不到目标；若为 R8 内联合并或 DEX 重排，实际 Hook 点不变。当前静态证据无法区分这两者，且类数与调用边数不是同一单位，不可换算。未知：HomeBannerFeatureInstaller、HomeTopBarFeatureInstaller、HomeRecommendPurifyFeatureInstaller 未读取，其定位依据是符号名、描述符还是调用边，以及失败是否有兜底，均未知；E015 中出现的 AccountMineRequestResource 也提示该家族归并可能混入跨功能类，需先确认家族口径再解释计数。
反例与替代解释：可推翻本推断的证据：消失的调用边目标全部在 9.18.0 中仍被同签名调用（仅调用者内联）；或真机所有首页装饰类功能均生效。
建议：对 9.17.0/9.18.0 同名类做方法体哈希对拍并列出消失的调用边目标；真机分别开启 banner 隐藏与首页推荐净化，检查安装期是否报定位失败、功能是否生效。
证据：E003, E015

### F007：pgc_legacy 调用边 455→301 与 pgc_theseus 904→982 并存，疑似 PGC 能力向 Theseus 迁移（未确认）
事实（E006）：pgc_legacy 类 366→345、外部调用边 455→301、compose 方法 0→0、指纹由 a7bb4411… 变为 14717f3a…；pgc_theseus 类 2262→2258、compose 方法 131→134、外部调用边 904→982、指纹由 1b944d7c… 变为 b9f79e23…；pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧完全一致。推断：legacy 边数大幅下降而 theseus 的 compose 入口与调用边同向上升，与「旧原生 PGC 入口被 Theseus 容器合并或迁移」相容；但 E006 的家族摘录每族仅 2 类样本（有界摘录），且协议计数未变，无法排除 R8 内联、去虚拟化、重复包装层折叠或 DEX 重排。影响：若 PgcAutoActivityPopupLocator 的候选集或 PgcAutoActivityPopupPolicy 的判据依赖旧原生调用形态，9.18.0 上可能候选减少或歧义，导致 Hook 少装；反向风险是 theseus 侧重复安装同一策略。runtime_enabled 全为 unknown、module_coverage 为 requires_installer_review，静态调用存在不证明真机路径启用，更不证明 Hook 生效。
反例与替代解释：若对 pgc_legacy 抽样类做方法体哈希比对后，减少的 154 条边均可归因为方法体被内联进更少的调用点（类集合与成员语义不变）、且真机安装日志显示 legacy 定位点命中数与 9.17.0 一致，则迁移推断被推翻，应降级为编译/混淆性结构漂移。反之若 legacy 定位点命中显著减少、theseus 侧新增 compose 入口承接了对应调用，则迁移假设得到支持。若服务端开关在两侧都未打开该弹窗，则两路径边数差异与功能表现无关，本发现应保持 needs_runtime。
建议：先用真机双版本 A/B 采集 PgcAutoActivityPopupFeatureInstaller 安装日志与定位器诊断，记录两条路径各自的候选数与命中数；再对 pgc_legacy 抽样超过 2 类做方法体哈希与描述符对比，把 455→301 的减少逐条归因到调用方，区分内联折叠与入口迁移。归因完成前不得将该变化报告为 PGC 旧原生路径废弃或适配通过。
证据：E006, E000

### F008：detail_kotlin_moss 调用边 38→34（定义数不变）与 detail_theseus_united 类增边减，需按调用方定位而非按计数推断覆盖
事实（E005）：detail_java_moss 定义 32、真实调用边 35，两侧完全一致；detail_kotlin_moss 定义 76 不变而真实调用边 38→34；detail_theseus_ugc 类 1976→1973、边 529→525、compose 25→25；detail_theseus_united 类 4617→4679（+62）而边 4196→4180（-16）、compose 98→98；detail_legacy 两侧 absent 且空集指纹一致。E005 属有界摘录（每族 2 类样本、每协议 4 个 caller 样本），以上均为家族级计数，不能外推为逐类对应关系。E014（E022 为同一文件、同一 sha256 2ec67116… 的重复读取）只证明模块侧 CommentClassicStyleLocator 以 DeviceDecision 的 comment.next_appearance 为锚点、并存在 CommentV3Fragment / CommentSectionComposeFragment 双入口的定位设计，不证明任一入口在 9.18.0 真机被装载或启用；E012 的 comment_compose 规模（2501 类、289 compose 方法、1142 条外部调用边，仅 5 类样本）登记在评论页家族下，本单元未取得其与 detail 页归属关系的页面级证据，只能作为「detail 页可能存在多入口并存栈」的旁证，不作为结论依据。推断：Kotlin MOSS 减少的 4 条边更可能来自调用方迁移或包装层折叠；united 的类增边减更像新增内部包装/lambda，不能记为新样式。方法定义数与调用边数不是同一单位，不能相除推导覆盖率，也不能用协议边数推断 Hook 覆盖面。影响：KotlinMossChannel / KotlinMossReplyBridge 的解析条件、DetailUnitedModulePurifyFeatureInstaller / DetailUnitedPresentationPurifyFeatureInstaller 的匹配点可能部分落空，落空范围未知；detail_legacy 的 absent 也无法区分登记口径缺失与宿主路径变化。
反例与替代解释：若能证明 4 条减少边对应的调用方方法体在 9.18.0 仍存在、仅描述符被重写（混淆改名），则「调用方迁移」被推翻；若能证明 E012 的 comment_compose 与 detail Kotlin MOSS 边完全不相交，则评论区规模不能作为 detail 页依据，本发现应缩窄为纯协议边计数变化。若真机 9.18.0 上 DetailUnited 净化与 Kotlin MOSS 通道日志显示与基线相同的命中集合，则结构哈希变化可归因为 DEX 重排/重复包装层，本发现降为无行为变更。
建议：把 4 条减少的 Kotlin MOSS 调用边逐条还原到调用方类与方法描述符，读取 KotlinMossChannel / KotlinMossReplyBridge 的解析条件确认是否依赖被改写的成员；核查 united 新增 62 类中 lambda/包装层占比，并比对 98 个 compose 方法签名两侧对应关系。对 detail_legacy 在 9.18.0 上以 DeviceDecision（NATIVE_OWNER/NATIVE_ANCHOR=comment.next_appearance）与 CommentV3Fragment 做装载探测并导出 dex.assist.comment_classic 诊断，区分登记口径缺失与宿主路径变化。真机 9.17.0 与 9.18.0 分别采集 detail 模块净化与 Kotlin MOSS 通道的安装命中日志，作为判定 Hook 是否生效的唯一依据；在拿到日志前不将任何路径记为已适配。
证据：E005, E012, E014, E022

### F009：player_kotlin 类+22/边+55 而 compose 与 Moss 协议面不动：结构漂移候选，不足以称新样式
事实：player_kotlin 9.17.0→9.18.0 类数 458→480（+22）、外部调用边 836→891（+55），compose 方法保持 37，指纹 c539764c…→9c22f386…；player_java 侧反向少 1 类（954→953）、少 8 边（3308→3300）、compose 仍 0；两版 player_kotlin_moss 均为 34 定义/3 实际调用边，player_java_moss 均为 18 定义/2 实际调用边（E007）。推断：compose 方法数与协议签名面同时不变而类与边净增，更符合 DEX 重排、R8 混淆池扩张、协程/包装类新增或代码跨 dex 迁移，也可能只是非播放路径类被判进同家族；不能用计数增加推出新增播放器样式，也不能用边数除以类数推算覆盖率（单位不同）。对模块的影响取决于定位方式：PlayerBuffer/PlayerSpeed/PlayerCapability/Sponsor 等定位器若按固定描述符或类枚举选择，候选集扩容会改变命中与歧义度；本轮未读取这些定位器源码，也未做全量类样本对齐，命中与否属未知。补充限制：预取每族仅两类样本，边数增量的接收类分布未观测。
反例与替代解释：可推翻当前推断的证据包括：新增 22 类经反编译全部与播放器无关（说明只是家族口径变宽而非结构变化）；或按方法体哈希对齐后 37 个 compose 方法与 3300 条 Java 边的语义主体逐一对应，仅描述符改名（说明纯混淆/DEX 重排）；反之若发现新的播放器渲染/控制类且持有播放器会话字段并有外部调用者，则应升级为新样式候选并单独建点。另需注意 source_snapshot 为 historical 且工作树 dirty，源码哈希可追溯但可能不含本次改动。
建议：先做静态对齐再上机：用 family_evidence 拉 player_kotlin 与 player_java 两侧全量 class_samples，按 method_bodies_sha256 与 compose_signatures 对齐，列出净增类中引用播放器包前缀或持有播放器会话字段的项，并对 2–3 个新增类用 decompile_class 反编译定性。随后读 PlayerBufferLocator/PlayerSpeedLocator/PlayerCapabilityAccess 等源码确认定位依据，再在真机分别进入普通视频、番剧、小窗与宽屏播放，读取版本适配器点位安装日志（installed/failed/ambiguous），确认缓冲/倍速/清晰度 Hook 不仅安装成功而且被实际调用。
证据：E000, E007

### F010：danmaku 双栈并存：legacy 家族 absent 但 Java Moss 仍有 20 条实际调用边，Kotlin 侧调用边 +2
事实：danmaku_legacy 在两版均为 classes=0/边=0/空集指纹，而 danmaku_java_moss 保持 22 定义、20 条实际调用边不变；danmaku_kotlin 家族 135→137 类、162→164 边、compose 保持 3，danmaku_kotlin_moss 定义 46 不变而实际调用边 10→12（E008）。推断：Java 与 Kotlin 两条弹幕协议消费栈同时存在，legacy 的 absent 更像家族归属口径（包名前缀/DEX 归属/方法体哈希规则未读到）未匹配，或旧栈代码整体归入未归类调用者，不能读成旧原生弹幕功能消失；Kotlin 侧新增 2 条边可能是新增一个消费者类（类 +2 与边 +2 同量）内部调用协议，也可能是共用协议的新调用点，亦可能是 $default/重载包装产物，三种解释均未被排除。对模块的影响集中在 DanmakuPurifyFeatureInstaller/Policy：若按固定描述符安装净化 Hook，新增 2 条边可能漏挂；若按类型化边界解析则需安装期复核——本轮未读这两个文件，覆盖为未知。旁证而非本页证据：comment 页 CommentClassicStyleLocator 采用“安装期仅反射 + 语义 DEX 查询集中调度 + HookPoint 描述符缓存并用当前宿主 ClassLoader 复验”（E014），说明该模块整体存在缓存点位与宿主升级错位的风险类型，但不能据此推断 danmaku 净化边界的实际行为。限制：预取 caller 每协议仅四条样本，未做 caller 全量差分，也未扫描弹幕渲染栈（原生/Compose/Opus 类）、平板/宽屏与服务端开关分支。
反例与替代解释：可能推翻当前推断：若 Java 侧 20 条调用边的 owner 全部属于直播/互动而非视频弹幕，则 danmaku_java_moss 与视频弹幕净化无关，legacy absent 才可能是真实结构缺失；若 Kotlin 侧新增的 2 条边落在同一类同一方法的重载或 $default 包装（KotlinMoss 常见形态），则属于编译产物差异而非新调用点；若 danmaku_kotlin_moss 定义 46 未变而签名集合出现差集，则计数相等掩盖了真实协议面变化。若真机上两条栈的净化 Hook 均被命中且计数随开关变化，则家族口径问题不影响功能，可降级为口径缺陷。反之若某条栈 installed 但零命中，需按包装层与协程调用点继续深挖。
建议：三条并行补证：(1) protocol_evidence 对 danmaku_java_moss 与 danmaku_kotlin_moss 各取全部 caller_samples 做 target/baseline 差分，输出新出现的 2 个 Kotlin caller 及 Java 侧 20 条边的 owner 包名，逐个 decompile_class 判定属原生/Compose/Opus 哪一渲染栈、是否弹幕净化边界，并排除 $default 包装；(2) 读 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt（按固定 source_tree_sha256 追溯），核对其解析点是固定描述符还是类型化边界、是否有跨家族兜底与安装失败上报；(3) 真机在净化开关开/关各跑一遍，收集 installed/failed 与命中计数，并覆盖宽屏/平板与服务端样式回滚分支。
证据：E000, E008, E014

### F011：mine_account_model 计数不变而指纹改变：优先按混淆改名/DEX 重排处置，并把跨家族消费者计入影响面
事实：mine_account_model 在 9.18.0 与 9.17.0 两侧均为 132 类、0 compose 方法、43 外部调用边，但结构指纹由 ebf9deed… 变为 abd9520a…（E010）；同家族的 mine_native 则是 327→326 类、96→94 边、7 compose 方法不变，指纹 96810670…←ae6321bd…（E010）。推断：外部调用边数与成员数完全不动、只有哈希变化，与「新增页面样式」不相容，更符合 R8 改名、DEX 重排、编译期 synthetic 增删或方法体级微调。第二个事实来自深挖样本：account/mine 侧的请求资源枚举 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource（含 ACCOUNT_UPDATE/REFRESH/RESELECTED/RESUME/SELECTED 等常量）被归入 home_legacy 家族（E015），说明家族切分不等于页面切分，mine 的账号/请求消费者可能分布在本单元两个家族之外，只用家族计数谈覆盖会漏。模块侧先例（跨家族源码，非 mine 已读实现）：定位器会把 HookPoint 描述缓存起来并在使用前用当前宿主 ClassLoader 复验，说明改名场景下存在 DEX/反射兜底路径（E014）；但该兜底是否覆盖 mine 的解析点、以及 MineComponentFilterFeatureInstaller/MineVipFeatureInstaller 是否走它，本轮未读源码，为未知。两条路径 runtime_enabled 均为 unknown，不得据此宣称适配。
反例与替代解释：可推翻当前推断的证据：①两侧同名类 method_bodies_sha256 大量变化且出现新的 Compose/UI 类，说明是真样式改动而非重排；②采集侧确认指纹算法包含 DEX 分卷号或类顺序，则同计数异哈希完全不具信号；③在 home_legacy 家族里找到 mine 页真正的 UI 承载类，说明 mine 的家族划分本身已迁移，当前 mine 增量只是残留壳。
建议：先把 mine_account_model 两侧同名类的 method_bodies_sha256 与字段表逐条比对，判定是纯改名还是方法体变化；对命中的差异类用 decompile_class 读出实际成员，再回到 MineVipFeatureInstaller/MineComponentSnapshotQueryContract 核对解析点是否仍能命中；同时把 home_legacy 等其它家族中出现的 AccountMineRequestResource 一类调用者登记为 mine 的跨家族消费者。真机侧在登录态切换与下拉刷新后观察 mine 快照面板与 VIP 分支日志，任何一步缺失都继续记为未知。
证据：E010, E014, E015

### F012：story_native 小幅增量与「story_kotlin 恒为空」并存：既不能判为新样式，也不能排除 Kotlin/Compose 迁入 story_native 家族
事实：story_native 由 2954 类/44 compose 方法/1439 外部调用边/指纹 f410eec8… 变为 2974/45/1470/28025f3f…，story_kotlin 两侧均 0 类/0 方法/0 边、空集指纹 4f53cda1…（E009）。E009 仅下发两族 summary，未附任何 class_samples，故本单元无法把增量归因到具体类，也无法在「新样式」「包装层增删」「编译器产物/合成类差异」之间取舍。本页唯一可观测家族自身已含 45 个 compose 方法，所以「story_kotlin absent」既可能是 Kotlin/Compose 实现被计入 story_native 的归并口径，也可能是尚未迁移；absent 不等于页面功能消失，两种解释均未被证据排除。story 页 protocols 为空（E009），没有协议消费者可交叉验证。推断部分仅作机制类比：已冻结的其它页面源码显示，模块的动态页安装器按返回类型解析 Moss 边界并依赖逐页不同的 getter 名（getUpList 与 getVideoUpList）（E013），首页框架过滤挂在该数据类的全部构造器上并按最外层构造结束处理（E018），即命中依赖具体成员名与构造器集合而非页面是否存在。但本轮未读 StoryPurifyFeatureInstaller / StoryActionIconsFeatureInstaller / HomeVerticalDetailFeatureInstaller 的任何解析点与期望成员，故 story 定位点在 9.18.0 是否仍能命中为未知，不得由上述先例推定命中或失效。两条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，不作适配通过判断。
反例与替代解释：可推翻当前推断的证据：①差集里出现完整的新页面 Fragment/Composable 入口且被 story 页入口调用，则倾向真实新样式或新的并存栈；②差集全部是单方法合成/invokable 类且方法体哈希与基线同名类一致、总方法体内容无变化，则偏向编译产物或包装层变化；③采集侧确认 Kotlin/Compose 代码一律计入 story_native，则 story_kotlin 的 absent 只是口径产物，不能作为任何迁移判断依据；④若读到的 story installer 解析点使用返回类型/方法体语义而非硬编码名，则即使出现类改名也仍可能命中，「零命中」推断失效。
建议：对 story_native 两侧以同一参数重读 family_evidence，做类名集合差集与同名类 method_bodies_sha256 对拍，并把差集拆成「Compose 包装/lambda」「MOSS/KTX 包装」「页面/ViewModel 实现」三类；对第三类用 decompile_class 读其调用者是否来自 story 页真实入口；读 StoryPurifyFeatureInstaller 与 StoryActionIconsFeatureInstaller（按固定 source_tree_sha256 追溯）导出「期望类名/方法名/返回类型/构造器」清单，与 9.18.0 结构逐条对拍；向采集侧确认 story_kotlin 的归并规则，判断其恒为 0 是口径产物还是真实缺失；最后在 9.18.0 真机逐开关抓 installer 的 resolved/miss 与 Hook 回调计数，把 runtime_enabled 从 unknown 变为实测值。
证据：E009, E013, E018

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
评论区 9.18.0 静态五族并存（legacy_v2 579 类/754 边、native_legacy 176/245、native_next 49/58、native_exp3 58/56、compose 2501 类/289 compose 方法/1142 边，E019、E001），没有任何登记路径在矩阵中消失，因此类数下降不能读作页面功能下线；五族 evidence 均为 static_invoke_observed，runtime_enabled 全部 unknown，module_coverage 全为 requires_installer_review，故本页只能给变化与验证任务，不判定适配。相对 9.17.0：legacy_v2 类 580→579 而边 743→754（少类多边）、native_legacy 类 192→176 边 263→245（同向收缩）、native_next 类持平 49 而边 66→58、native_exp3 类 55→58 边持平 56、compose 类 +71/方法 +6/边 +39；除 native_next 外指纹全部改变，必须先用类名集合差集与同名类方法体哈希排除 DEX 重排、混淆改名与内联，再谈结构变化。协议侧 comment_java_moss 50 定义/50 边、comment_kotlin_moss 130/23 两侧计数完全一致（E001），这只说明统计口径未变，不能证明方法名、描述符或路由未变。模块侧已读全的解析点：CommentClassicStyleLocator（sha256 2ec67116…，E022）以 com.bilibili.lib.dd.DeviceDecision.getBoolean 与 kntr.base.dd.IDeviceDecisionKt.getBool/getBool$default 为经典样式读取器，verified 逐项校验非抽象/非桥/返回 boolean 与参数描述符，select 在多 declaringClass、单 owner 超过 16 个方法或总数超过 32 个候选时返回空——即宿主新增同名重载或迁包时会静默退化为空读取器；kotlin 家族仅当 kntr.common.comment.entry.CommentSectionComposeFragment 或 kntr.common.comment.card.model.comment.CommentModel 存在时适用，同时仍登记 NATIVE_ENTRY com.bilibili.app.comment3.CommentV3Fragment（草稿"超 16 个候选返回空"表述不完整，已修正）。9.18.0 上述锚点与描述符本轮未取证，经典样式族的实际命中仍为未知。E012 的 compose 抽样 5 类中 3 类无任何方法、compose_signatures 全为空，属有界摘录，不能代表 2501 类的实现。
证据：E019, E001, E022, E012

### 复核页面：dynamic
动态页三族在 9.18.0 静态全部可见（legacy 3254 类/105 compose 方法/2136 边、compose 1421/182/287、opus 1370/95/227，E020、E002），无任何路径消失的静态证据；三条路径 evidence 均 static_invoke_observed、runtime_enabled unknown、module_coverage requires_installer_review，本页不给适配结论。变化集中在 dynamic_compose：类 1234→1421、compose 方法 151→182、边 232→287，三指标同向增长，指纹 da87e05c…→76028ed3…；dynamic_legacy 类 3261→3254 而边 2060→2136（+76）；dynamic_opus 类 1376→1370、边 230→227，规模基本持平但指纹改变。E021 复读显示 compose 族 5 个样本全部落在 kntr/app/following/followinglist：C 持 LazyListState+CoroutineScope，D 持 State/MutableState/CoroutineScope/ui/wide/g/FollowingListViewModel 且构造器接收 ComposableLambda 与 Function2，E 接 Function0，说明该族含 Compose 列表与宽屏布局的状态与 lambda 持有者；但 5 个样本 compose_signatures 全为空，族边界按类/包归属而非可组合签名划分，因此只能判定为"Compose 相关类集合扩张"，不能判定新增可组合样式，更不能判定其出现在动态页。样本同时提示这些类可能属于关注页、被族口径按 kntr 前缀纳入，本轮未检索其调用方，动态页归属未知。模块侧 DynamicPurifyFeatureInstaller（sha256 74f8c301…，E013）在 protobuf 边界（DynamicMoss#dynAll、executeDynAll 与 *MossKtxKt 包装，综合页 dynAll 与视频页 dynVideo 同判据）过滤，无可用 feed 时返回 missing("no-dynamic-hook-point")，其注释自述离线核对仅覆盖 9.7.0–9.11.0。因此草稿"渲染族从 legacy 迁到 Compose 会绕过净化 Hook"的推断不成立：净化装在协议边界，不依赖卡片渲染族；真正的缺口候选在 UI 层显隐/tabs 参与点与 feed 解析结果，均未验证。协议侧 dynamic_java_moss 134/134、dynamic_kotlin_moss 382/27 两侧一致，只说明计数口径稳定；KOpusMoss/OpusMoss 未登记，是否存在动态页跨族消费者静态不可判定。
证据：E020, E002, E021, E013

### 复核页面：home
home 两条登记路径并存，静态状态均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，本单元不给出适配结论。home_legacy：9.18.0 为 782 类 / 88 compose 方法 / 203 外部调用边（基线 744 / 87 / 228），fingerprint 08b1d4… 对 1ae88d…；E015 仅下发两个类样本（main2/A0、main2/A）及 userprotocol/m、AccountMineRequestResource，可见样本仍在 tv.danmaku.bili.ui.main2，但样本量不足以推断包级迁移，compose 方法 +1 是否为新入口需按名重读。home_new_frame：190 类 / 33 / 54（基线 198 / 33 / 51），fingerprint c2fe89… 对 d94225…；预取 E003 对该族只下发 summary，无类样本，故 tab/bottom 列表数据类构造器数量及 FilteredTabList 所依赖的形态无法静态确认。E018 显示 HomeFrameListHook 挂全部构造器、以 ThreadLocal 深度计数只处理最外层，并用 FilteredTabList 跳过宿主 copy() 回写、全删光时原样放行兜底：该设计对构造器集合变化敏感，但空结果不会破坏宿主。指纹全变≠新样式，需用同名类方法体哈希区分 R8 内联、DEX 重排与真实迁移。HomeFrameTabLocator、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller、HomeBannerFeatureInstaller 等未读取，定位失败兜底未知。验证：两版方法体哈希对拍 + 消失调用边目标清单 + 真机隐藏/恢复 tab 与 banner/顶栏/推荐净化开关日志；宽屏与服务端开关分支静态不可见。
证据：E003, E015, E018

### 复核页面：search
search 两条登记路径并存，静态状态均为 static_invoke_observed，runtime unknown、module_coverage requires_installer_review。search_native：1704 类 / 2 compose 方法 / 2865 外部调用边（基线 1701 / 2 / 2880），fingerprint 27b995…；search_compose：3131 / 562 / 617（基线 3136 / 562 / 607），fingerprint 8cf08a…。共同协议计数两侧相同（search_java_moss 24 定义 / 22 边，search_kotlin_moss 52 / 18），但定义数与调用边数不是同一单位，不能相除推覆盖率，也不能排除方法名与描述符集合变化。E016 仅下发部分 caller_samples，可见样本全部来自 search_compose 的 kntr.app.search.aggregate/repository，故 search_native 是否为 Java/Kotlin MOSS 消费者仍未确认，跨家族消费者问题开放。E017 确认 SearchHomeRecommendLocator 依赖硬编码类型名（SearchSquareType、SearchReferral$Guess）与 com.bilibili.search2.discover./main.data. 前缀 + a..z 短名 + $a..z/$0..9 后缀的有界枚举探测；Points 中 delivery、state 可空，deliveryCandidateCount 仅用于区分「宿主无此结构」与「候选歧义」，注释还写明未命中名会抛 ClassNotFoundException、每进程安装期只探测一次并缓存。据此「结构改名→定位为空→功能静默不生效」是可核查的候选风险；但 singleOrNull 收束与五项具体判据不在可见摘录内（截断于 locate(loader），需按名重读。验证：导出两包与两个 API 类型清单对拍、抓安装期 locate 返回与候选数、真机双搜索页验证净化与猜你想搜。
证据：E004, E016, E017

### 复核页面：detail
三条登记路径逐项与 E005 复核一致：detail_legacy 在 9.17.0 与 9.18.0 两侧 evidence 均为 absent、类数/compose 方法/调用边都为 0、指纹同为 4f53cda…（空集哈希），因此该空结果是登记口径结果，不能读作 9.18.0 才发生的删除，也不能推断旧原生详情实现已从宿主移除；legacy 侧模块定位点（DetailViewPurifyFeatureInstaller / DetailModulePurifyFeatureInstaller）是否有落点仍为 requires_installer_review。detail_theseus_ugc 类 1976→1973、外部调用边 529→525、compose 方法 25→25、指纹 729a51a7…→ed2491aa…；detail_theseus_united 类 4617→4679（+62）、边 4196→4180（-16）、compose 98→98、指纹 cafecc5c…→cce82b5d…，两族都是小幅计数漂移且方向不一致的组合，与混淆改名、DEX 重排、内部包装/lambda 层变化相容，不构成新样式证据。协议面 detail_java_moss（32 定义/35 边）两侧完全一致，detail_kotlin_moss 定义 76 不变而真实调用边 38→34；定义数与调用边数不是同一单位，不能相除换算覆盖率。E012（comment_compose：2501 类/289 compose 方法/1142 边，5 类有界样本）与本页家族无归属证据，只能当规模旁证，不能外推为 detail 页实现全貌；E014 仅证明模块侧以 com.bilibili.lib.dd.DeviceDecision 的 comment.next_appearance 锚点与 CommentV3Fragment / CommentSectionComposeFragment 双入口定位（E022 为同一文件同一哈希的重复读取），不证明任一入口在 9.18.0 真机启用。三路径 runtime_enabled 全 unknown、complete_coverage=false，本报告不判定适配通过。
证据：E000, E005, E012, E014, E022

### 复核页面：pgc
两条登记路径与 E006 复核一致，且都登记了 requires_review 的结构/调用路径变化。pgc_legacy：类 366→345（-21）、外部调用边 455→301（-154）、compose 方法 0→0、指纹 a7bb4411…→14717f3a…；边降幅远大于类降幅，是需要优先归因的信号，但 E006 每族仅 2 类样本，无法据此排除 R8 内联、去虚拟化、重复包装层折叠或 DEX 重排，也不能直接推论旧原生 PGC 入口被合并或下线。pgc_theseus：类 2262→2258、compose 方法 131→134（+3）、外部调用边 904→982（+78）、指纹 1b944d7c…→b9f79e23…，compose 入口与边同向上升，与能力向 Theseus 迁移相容，同样可由新增包装层解释；新增 3 个 compose 方法的调用方未定位。协议面 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧一致，说明变化集中在 UI 家族内部而非 PGC 协议定义本身，但协议计数相等不证明字段或路由未变。两路径 runtime_enabled=unknown、module_coverage=requires_installer_review，PgcAutoActivityPopupLocator / PgcAutoActivityPopupPolicy / PgcAutoActivityPopupFeatureInstaller 是否命中、是否存在候选歧义与兜底分支均未验证；本轮未读取平板/宽屏切换条件与服务端开关，无结构变化的 A/B 静态不可见，不能声称已穷尽样式。
证据：E000, E006

### 复核页面：player
两条登记路径 status 严格保留静态矩阵值 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，故本页不产生适配通过结论。事实（E000/E007）：player_java 类 954→953、外部调用边 3308→3300、compose 方法仍 0、指纹 ac88f659…→9721f668…；player_kotlin 类 458→480、边 836→891、compose 方法仍 37、指纹 c539764c…→9c22f386…；两版 player_java_moss 均为 18 定义/2 实际调用边，player_kotlin_moss 均为 34 定义/3 实际调用边。草稿对“类/边漂移而 compose 与协议签名面不动”的对立解释（R8 改名、DEX 重排、协程包装新增、代码迁移、家族口径变宽）均未被排除，处理正确：未把计数变化写成新播放器样式，也未用边数除以类数推覆盖率。草稿中“本轮未读 PlayerBuffer/PlayerSpeed/PlayerCapability/Sponsor 定位器源码”与 evidence 一致，Hook 覆盖仍为未知；这些定位器文件虽出现在 source_files 清单，仅代表候选存在、不代表已读内容。需修正的表述：草稿“APK access disabled”不是已记录事实，已改为“本轮未读取这些定位器源码”。抽样限制保留：预取每族两类样本、预取 caller 最多四条，未做全量 method_bodies_sha256 对齐，属已声明缺口而非结论。
证据：E000, E007

### 复核页面：danmaku
两条登记路径状态不同且按原值保留：danmaku_legacy=absent（两版 classes=0、边 0、空集指纹 4f53cda1…），danmaku_kotlin=static_invoke_observed（类 135→137、边 162→164、compose 保持 3、指纹 97597a31…→97cb0f15…）；runtime_enabled 均为 unknown、module_coverage 均 requires_installer_review（E000/E008）。草稿核心判断成立：同一靶包 danmaku_java_moss 保持 22 定义/20 实际调用边且两版不变，说明 Java 侧弹幕协议消费者确实存在，absent 只能读作家族归属口径未命中，不能读成旧原生弹幕或净化路径消失；danmaku_kotlin_moss 定义 46 不变、实际调用边 10→12，与家族类 +2/边 +2 同量，属“新增调用点/单一包装消费者”候选，两种解释均未排除。渲染栈家族（原生/Compose/Opus 类弹幕）、平板与宽屏分支、服务端开关均无运行证据，弹幕渲染样式差异静态不可见。缺口与草稿一致：未读 DanmakuPurifyFeatureInstaller/Policy，净化 Hook 的解析点形态（固定描述符或类型化）与安装结果均未知；预取 caller 每协议仅四条，未做 caller 全量差分。
证据：E000, E008

### 复核页面：story
story 页登记两条路径。story_native：9.18.0 为 2974 类 / 45 compose 方法 / 1470 外部调用边 / 指纹 28025f3f…，基线 9.17.0 为 2954 / 44 / 1439 / f410eec8…（E009）；state 取静态矩阵原值 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，故静态调用存在不等于运行启用或 Hook 生效。+20 类 / +1 compose 方法 / +31 边属小幅增长，与 Compose 编译器产物、KTX/MOSS 包装层或合成 lambda 增删同阶，不能作为新样式证据；且 E009 只下发两族 summary，未附任何 class_samples，本单元拿不到 story 类名，增量归因为未知。story_kotlin 两侧均 0 类 / 0 compose 方法 / 0 边、空集指纹 4f53cda1…、evidence=absent；absent 不等于页面功能消失，也无法区分「归并进 story_native（该族已含 45 个 compose 方法）」与「尚未迁移」。story 页 protocols 为空（E009），不能从协议消费者侧交叉验证。模块侧本轮未读 StoryPurifyFeatureInstaller / StoryActionIconsFeatureInstaller / HomeVerticalDetailFeatureInstaller 的任何定位成员；E013、E018 只是其它页面已冻结源码的机制先例（按返回类型与逐页不同 getter 名解析 Moss 边界；过滤挂在数据类全部构造器上并按最外层构造结束处理），说明模块命中依赖具体成员名与构造器集合，但不能据此推定 story 命中或失效。验证任务：以同一参数重读 story_native 两侧做类名差集与同名类 method_bodies_sha256 对拍，对差集类 decompile_class 归入 Compose 包装 / MOSS 包装 / 页面实现三类；读上述 installer 源码形成期望成员清单；真机逐开关抓 resolved/miss 与回调计数。综上仅记录变化与验证任务，不作适配结论。
证据：E009, E013, E018

### 复核页面：mine
mine 页登记两条路径，变化方向互不一致。mine_native：9.18.0 为 326 类 / 7 compose 方法 / 94 外部调用边 / 指纹 96810670…，基线 9.17.0 为 327 / 7 / 96 / ae6321bd…（E010），state 取静态矩阵原值 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review。少一类、少两条边是收缩型变化，更可能来自合成类或包装层合并、去重，也可能有个别组件被移除；两种解释静态不可分，需做类名差集 + decompile_class 归因，不能把边数下降直接读成路径下线。mine_account_model：两侧 132 类 / 0 compose 方法 / 43 外部调用边完全一致，仅结构指纹由 ebf9deed… 变为 abd9520a…（E010）；同基数异哈希优先按 R8 改名、DEX 重排或方法体微调处置，须先排除混淆再谈样式。口径问题必须记录：家族边界不等于页面边界——E015 显示 account/mine 侧请求资源枚举 Ltv/danmaku/bili/ui/main2/AccountMineRequestResource（含 ACCOUNT_UPDATE/REFRESH/RESELECTED/RESUME/SELECTED）被归入 home_legacy 家族，说明 mine 的账号/请求消费者可落在本页两个家族之外，用家族计数断言覆盖会漏。模块侧本轮未读 MineComponentFilterFeatureInstaller / MineVipFeatureInstaller / MineComponentSnapshotQueryContract / HostMineReadingCard，其解析点是硬编码名还是走 DEX 兜底为未知；E014 只是 comment 页定位器先例（缓存 HookPoint 描述、复用前用当前宿主 ClassLoader 验真、另有 DexAssist 通道），不证明 mine 存在同等兜底。验证任务：两侧同名类方法体哈希与字段表对拍；对差异类 decompile_class 读实际读取点；真机在登录态切换、切换账号与下拉刷新后观察 mine 快照面板与 VIP 分支日志。两路径 runtime 均未验证，不作适配结论。
证据：E010, E014, E015

- F001 / revised：E002/E021 支持“dynamic_compose 三指标同向增长、5 个样本集中在 kntr/app/following/followinglist 且 compose_signatures 全为空”。但原分析把影响写成“Compose 渲染会让动态卡片绕过现有净化 Hook”，与 E013 冲突：DynamicPurifyFeatureInstaller 装在 DynamicMoss#dynAll/executeDynAll 与 *MossKtxKt 的 protobuf 边界，不依赖卡片渲染族，渲染栈迁移本身不构成绕过。修订为：保留“Compose 相关类集合扩张、动态页归属未确认”作为候选，影响面改指向 UI 层显隐/tabs 与 feed 解析结果，并保留 DEX 重排/族口径/关注页归属等替代解释。（E002, E021, E013）
- F002 / revised：E022 完整支持定位器的解析逻辑，但草稿两处不精确：候选上限实为总数超过 32 或单 owner 超过 16 时返回空（并非统一“超 16”），且漏登记 NATIVE_ENTRY com.bilibili.app.comment3.CommentV3Fragment；同时草稿把结论级别定为 needs_runtime，而“锚点是否存在”是可静态核实的前置条件，缺失与否本身尚无障碍证据支持回归定性。修订为 candidate 并补足 select/resolve/missing 的静默失败路径与 KOTLIN 家族 p[0].isInterface 约束。（E022, E001）
- F003 / revised：E001/E002 支持四族 Moss 定义数与边数两侧一致，但原发现同时覆盖 comment 与 dynamic 两页协议，与 page=comment 的归属不符，且未使用 seed 中与本页直接相关的 ReplyMoss/KReplyMoss 未登记事实。修订为只保留 comment 侧两族 + main/community/reply/v2 未登记协议，动态侧协议问题移入 remaining_gaps；结论仍为计数不变不能替代方法集合比对，级别保持 candidate。（E000, E001, E002）
- F004 / revised：核心断言在 E017 可见摘录内成立：定位完全依赖硬编码类型名（SearchSquareType、SearchReferral$Guess）与 com.bilibili.search2.discover./main.data. 前缀加 a..z 短名、$a..z/$0..9 后缀的有界枚举；Points 的 delivery/state 为可空类型，失败以空值表达；deliveryCandidateCount 注释明确只用于区分「宿主无此结构」与「候选歧义」，不参与功能判定。但草稿中的具体判据细节（singleOrNull 收束、getHistoryList、唯一单参 List<SearchSquareType> void 方法、NegativeFeedback 3 或 5 参构造器）不在下发摘录内——摘录截断在 locate(loader 处，不能作为已核实事实陈述；且 ROOT_NAMES 实际为 27 项（a..z 加 SearchDiscoverViewModel），与源码注释「约 20 个根类 × 36 后缀 ≈ 700 次探测」不一致，属注释与实现的口径偏差。故按补丁收窄为已核实部分并把其余标为待按名重读；level 仍为 candidate，9.18.0 类数 3136→3131 与 fingerprint 变化本身不能证明该结构已变。（E004, E016, E017）
- F005 / revised：E018 完整支持事实部分：HomeFrameListHook 挂在数据类全部构造器上、以 ThreadLocal 深度计数只在最外层构造结束时处理、结果装进 FilteredTabList 并在 process 中识别标记跳过 copy() 回写、filterFrameTabs 在结果为空时原样放行。E003 确认 home_new_frame 190 类 / 33 compose / 54 边对基线 198 / 33 / 51。但草稿 analysis 中「E003/E015 侧 home_legacy 抽样同时在 main2 包」的旁证对 home_new_frame 构造器形态没有支撑力：E003 对该族只下发 summary，类样本未下发，E015 只是 home_legacy 侧样本。按补丁把该旁证替换为明确的证据缺口，结论方向（构造器集合变化风险未静态排除、需真机）与 needs_runtime 级别不变。（E003, E018）
- F006 / revised：计数事实成立（E003：home_legacy 782 类 / 88 / 203 对基线 744 / 87 / 228），发现本身也明确未断言失效，方向正确。但草稿把 StarterFragment/HomeFragmentV2 说成「抽样类」不准确：E015 实际抽样的类是 Ltv/danmaku/bili/ui/main2/A0、A、userprotocol/m、AccountMineRequestResource，StartupFragmentV2 与 HomeFragmentV2 只是这些样本类的字段类型，仍可支撑「抽样仍在 main2 包」但支撑力更弱。按补丁更正措辞，并补充 E015 中还出现 AccountMineRequestResource 这一非导航相关枚举，提示该家族可能混入功能类、家族归并口径本身待确认；level 保持 candidate，不升级为失效结论。（E003, E015）
- F007 / retained：逐项与 E006 核对：pgc_legacy 366→345 / 455→301 / compose 0→0 / 指纹 a7bb4411…→14717f3a…；pgc_theseus 2262→2258 / 131→134 / 904→982 / 指纹 1b944d7c…→b9f79e23…；pgc_player_moss 12 定义 3 边、pgc_view_moss 14 定义 7 边两侧一致，数字与草稿完全相符。发现把解释限定为“相容”，同时显式列出 R8 内联／去虚拟化／包装层折叠／DEX 重排等替代解释，并保留 runtime_enabled=unknown、module_coverage=requires_installer_review 与「静态调用存在≠路径启用≠Hook 生效」的限定，未把边数下降等同于功能删除或迁移完成，也未把 E006 的每族 2 类有界样本外推成整族结论；等级 candidate（未确认迁移假设）与证据强度匹配。对 PgcAutoActivityPopupLocator/Policy 的表述为条件句（“若依赖旧原生调用形态”），未宣称已读取这些文件的 Hook 覆盖，符合不得推测未读源码的约束。（E006, E000）
- F008 / revised：E005 全部计数与草稿一致（java_moss 32/35 两侧相同；kotlin_moss 76 定义、边 38→34；ugc 1976→1973、529→525、compose 25→25；united 4617→4679、4196→4180、compose 98→98；detail_legacy 两侧 absent 且空指纹相同），核心断言成立，方法定义数与调用边数不可相除的口径提醒也正确，故不拒绝、不降级。但有两处表述需要收紧：其一，E012 的 comment_compose（2501 类/289 compose 方法/1142 边，5 类有界样本）登记在评论页家族下，本单元没有页面级证据证明它与 detail 页的归属关系，原文把它当作 detail 页“多入口并存栈”的依据偏强，应降为规模旁证；其二，E014（与 E022 同文件同哈希 2ec67116…）只证明模块侧以 DeviceDecision 的 comment.next_appearance 为锚点、存在 CommentV3Fragment / CommentSectionComposeFragment 双入口，并未证明任一入口在 9.18.0 真机启用，原文“样式启用受宿主开关与装载探测约束”属未取证外推，需标明未验证。据此给出修订补丁，等级仍为 needs_runtime（两路径 runtime 未观测）。（E005, E012, E014, E022）
- F009 / revised：计数与协议面断言与 E007 两侧预取逐项吻合（player_java 953/3300/0 与 954/3308/0；player_kotlin 480/891/37 与 458/836/37；两侧 moss 18/2 与 34/3），level=candidate 与“结构漂移不等于新样式”的定位正确，替代解释（R8 改名、DEX 重排、协程包装、代码迁移、家族口径变宽）均已列出。唯一需修正处：草稿称“本轮 APK access disabled”，这是未在证据中出现的环境描述，改为“本轮未读取这些定位器源码”，且不改变“Hook 覆盖未知”的结论。evidence_ids 不变。（E000, E007）
- F010 / revised：核心断言由 E008 双侧预取支撑：danmaku_legacy 两版 classes=0/边=0/空集指纹；danmaku_java_moss 22 定义/20 实际调用边两侧一致；danmaku_kotlin 135/162→137/164；danmaku_kotlin_moss 46 定义、边 10→12。因此“absent 只是家族归属口径未命中，不等于旧原生弹幕或净化路径消失”与“Kotlin +2 边有至少两种未排除解释”均成立，level=needs_runtime 恰当。需修订处：原文以 comment 页的 CommentClassicStyleLocator（E014）推断 danmaku 侧净化缓存在宿主升级后可能错位，属跨页类比，不能作为本页证据，已在 analysis 中显式降级为旁证；同时补充预取 caller 每协议仅四条、未做全量差分的抽样限制。evidence_ids 保留不变。（E000, E008, E014）
- F011 / retained：逐条核对：①「132 类 / 0 compose 方法 / 43 边两侧一致、指纹 ebf9deed…→abd9520a…」与「mine_native 327→326 类、96→94 边、7 compose 方法不变」均由 E010 的 target/baseline summary 直接支持，gut 未改口径；②「account/mine 侧 AccountMineRequestResource 枚举被归入 home_legacy」由 E015（home_legacy target 的 class_sample 含该枚举及其 ACCOUNT_UPDATE/REFRESH/RESELECTED/RESUME/SELECTED 字段）直接支持，用于说明家族切分≠页面切分的论证成立，未把该样本反推为 mine 已读实现；③「定位器缓存 HookPoint 描述、复用前用当前宿主 ClassLoader 验真」与 E014 的注释与结构一致，且原文已标注为跳家族源码先例、非 mine 已读实现，未越界；④结论停留在 candidate，未因计数不变、未检出或哈希变化而宣称新样式或失效，也未把计数当作覆盖率；⑤把「MineVipFeatureInstaller / MineComponentSnapshotQueryContract 是否走兜底」明确记为未知，符合证据边界。推荐动作（同名类 method_bodies_sha256 与字段表对拍、差异类 decompile_class、真机登录态切换与刷新观测）具体可执行。保留原归属页 mine，无需修改。（E010, E014, E015）
- F012 / revised：事实层面成立：E009 明确给出 story_native 2954/44/1439/f410eec8… → 2974/45/1470/28025f3f…，story_kotlin 两侧 0/0/0 与空集指纹 4f53cda1…，protocols 为空；亦未把 +20 类/+31 边判为新样式。但两处表述需收紧：一，草稿只说「预取无类样本」，未说明 E009 实际只下发两族 summary、完全没有 class_samples，读者无法判断抽样程度；二，E013（dynamic Moss 边界按返回类型与 getUpList/getVideoUpList 解析）与 E018（HomeFrameListHook 挂全部构造器、最外层构造结束处理）均另属其它页面，草稿虽标注为先例，但将其直接与「story 模块可能零命中」并置，暗示性强于证据强度，应显式声明这是机制类比、本轮未读任何 story installer 源码。修订仅调整 analysis/recommendation/alternatives 三处措辞与推理边界，title、page、level（candidate）与 evidence_ids 不变，不新增未取证结论。（E009, E013, E018）

### 尚未解决的证据缺口

- [1] 9.18.0 中四个经典样式锚点（com.bilibili.lib.dd.DeviceDecision、kntr.base.dd.IDeviceDecisionKt、com.bilibili.app.comment3.CommentV3Fragment、kntr.common.comment.entry.CommentSectionComposeFragment/CommentModel）的存在性与 getBoolean/getBool 完整描述符未取证，CommentClassicStyleLocator 的实际命中仍未知。
[2] comment 与 dynamic 两页均未做基线/目标类名集合差集与同名类 method_bodies_sha256 对拍，legacy_v2 少类多边、native_legacy 减 16 类、native_next 减 8 边究竟属迁移、内联、混淆改名还是真实收缩未定。
[3] comment_native_legacy 减少的 16 个类是否出现在 CommentNativeBindingCatalog / CommentNativeSupplementBridge 的登记表中未核对，绑定目录解析失败与兜底路径未验证。
- [4] comment_compose 新增的 6 个 compose 方法与 71 个类是否落在 CommentComposeViewAccess / CommentComposePurifyBridge 的匹配范围内未比对；E012 抽样 5 类中 3 类无方法且 compose_signatures 全空，覆盖广度无从外推。
[5] comment 侧 comment_java_moss / comment_kotlin_moss 的 caller_samples 本轮未取，两族的方法名与描述符集合差集、跨家族消费者（KotlinMossReplyBridge、KotlinMossChannel）未核实。
[6] ReplyMoss/KReplyMoss（main/community/reply/v2）仍未登记为页面协议，是否存在评论区调用方未知，不能以计数相等替代覆盖结论。
- [7] dynamic_compose 的 kntr/app/following/followinglist 类是否与动态页 tab 互达未检索，无法排除“关注页被按 kntr 前缀纳入同族”；其 Compose 相关类扩张是否影响 UI 层显隐/tabs 参与点同样未知。
[8] dynamic_legacy 新增的 76 条外部调用边未按接收类聚类，是否集中到新的卡片 ViewHolder、是否改变净化/显隐参与点未定；dynamic_opus 减 3 条边的调用方也未定位。
[9] KOpusMoss/OpusMoss 与 DynamicMoss 是否存在跨族消费者、Opus 卡片是否共用同一响应容器未取证，dynamic_opus 是否需要独立协议覆盖仍未知。
- [10] DynamicPurifyFeatureInstaller 的注释自述版本覆盖仅离线核对到 9.7.0–9.11.0；9.18.0 上 dynamic.purify.moss 解析、每个 feed 的同步/异步/Kotlin 包装安装结果与是否出现 missing("no-dynamic-hook-point") 均无日志证据。
[11] dynamic 侧 dynamic_java_moss（134/134）与 dynamic_kotlin_moss（382/27）计数不变同样未做方法集合比对，需并入动态页补证，不因 F003 修订而视为已覆盖。
[12] 两页全部登记路径 runtime_enabled 仍为 unknown，缺少同宿主版本下开关开/关的 Hook 命中计数对照，本报告不构成任何适配结论。
- [13] 宽屏/平板布局与服务端 A/B 样式分支静态不可见（E021 中出现 ui/wide 引用但未证其在动态页生效），需真机双配置对照，静态不得宣称所有样式已穷尽。
[14] source_snapshot working_tree_dirty=true（source_tree_sha256 37745f8f…，HEAD 5422fad1…），本轮源码结论只对应冻结快照文件哈希（如 CommentClassicStyleLocator 2ec67116…、DynamicPurifyFeatureInstaller 74f8c301…），不代表发布态源码。
[15] 本单元证据来自预取 E003/E004 与既有深挖 E015–E018；fresh_refresh 未包含 home/search 条目，如需严格「重新取证」口径需服务端确认，当前复核基于 E003/E004。
- [16] E003 对 home_new_frame 仅下发 summary，E004 对两族同样只下发摘要，complete_coverage=false；families 的类样本不足以代表整套实现，需按名重读 family_evidence 的 target/baseline 全量 class_samples 后再判断是否存在 tab/bottom 数据类与 discover/main.data 宿主类的形态变化。
[17] SearchHomeRecommendLocator 的 locate 主体未在可见摘录内（截断于 locate(loader），singleOrNull 收束方式、getHistoryList 判据、单参 List<SearchSquareType> void 方法判据、NegativeFeedback 3/5 参构造器判据均未经本轮证据核验，需按名重读。
[18] ROOT_NAMES 实际为 27 项，与 E017 注释中「约 20 个根类 × 36 后缀 ≈ 700 次类加载探测」不一致，实际探测成本与注释估算存在偏差，需以实现为准复核。
- [19] search_native 是否为 search_java_moss / search_kotlin_moss 的消费者未确认：E016 只下发部分 caller_samples 且全部属 search_compose，Java MOSS 调用者样本本轮完全未取到，跨家族消费者问题开放。
[20] HomeFrameTabLocator、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller、HomeBannerFeatureInstaller、HomeRecommendPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller、SearchPurifyFeatureInstaller 均未读取，安装器对其定位对象缺失时是否有兜底、失败是否上报仍为未知（module_coverage=requires_installer_review）。
[21] home_legacy 203 对 228 的外部调用边差异未归因：缺 9.17.0/9.18.0 同名类方法体哈希对拍与消失调用边目标清单，无法区分内联、DEX 重排与真实调用点迁移。
- [22] 四条登记路径 runtime_enabled 全为 unknown，无安装期 Hook 命中计数与真机功能差分；宽屏/平板布局与服务端 A/B 视觉分支静态不可见，不能宣称样式已穷尽。
[23] E015 样本中含 tv.danmaku.bili.ui.main2.AccountMineRequestResource（与 mine/account 请求相关），提示 home_legacy 家族归并口径可能混入跨功能类，需与 mine 单元交叉确认后再用该类计数解释首页影响面。
[24] 源码快照工作树 dirty（source_tree_sha256 37745f8f…，HEAD 5422fad1…），所有源码结论仅对应冻结快照文件哈希，非发布态；未提交改动是否触及本次定位逻辑未复核。
- [25] pgc_legacy 455→301 的 154 条边未逐条归因：E006 每族仅 2 类样本，无法区分 R8 内联/去虚拟化、重复包装层折叠、DEX 重排与入口迁移；需对两侧做同名类方法体哈希与方法描述符差集。
[26] pgc_theseus 新增的 3 个 compose 方法调用方未定位，无法判断是新包装层还是新入口，也未排除与 pgc_legacy 重复安装同一策略的风险。
[27] PgcAutoActivityPopupLocator / PgcAutoActivityPopupPolicy / PgcAutoActivityPopupFeatureInstaller 的实际定位依据（硬编码类名、返回类型还是方法体语义）与候选缺失时的兜底分支未读取，pgc 两路径 module_coverage 仍为 requires_installer_review。
- [28] detail_legacy 在两侧均为 absent，尚不能区分“登记口径未解析出类集合”与“宿主不再携带旧原生详情实现”；需在 9.18.0 真机做 DeviceDecision / CommentV3Fragment 装载探测并导出 dex.assist.comment_classic 诊断（E014/E022 只证明定位器设计，不证明命中）。
[29] detail_kotlin_moss 减少的 4 条调用边未还原到调用方类与方法描述符，KotlinMossChannel / KotlinMossReplyBridge 的解析条件是否依赖被改写的成员未知。
[30] detail_theseus_ugc（-3 类/-4 边）与 detail_theseus_united（+62 类/-16 边，compose 不变）的计数漂移未做逐类方法体哈希比对，无法确认是混淆改名、包装层合并还是真实结构变化。
- [31] E012 的 comment_compose 家族（2501 类，5 类样本）与 detail 页的归属关系缺少页面级证据，不能作为 detail 页实现全貌或 Compose 覆盖依据；需确认家族归并规则后再判断是否属于 detail 页覆盖缺口。
[32] detail 与 pgc 全部登记路径 runtime_enabled 均为 unknown、complete_coverage=false：尚无真机安装日志证明定位器命中与 Hook 回调发生，因此不得给出适配通过结论。
[33] 未读取平板/宽屏布局切换条件与服务端灰度开关；无结构变化的 A/B 分支静态不可见，不能声称所有样式已穷尽。
- [34] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，HEAD 5422fad1…，captured_at 2026-10-15T14:19:32Z，freshness=historical），所有源码侧结论需按文件哈希追溯，不能视为发布态代码；本轮未做未提交改动的差异核对。
[35] E005/E006 均为有界摘录（每族 2 类样本、每协议 4 个 caller 样本），后续应以 family_evidence / protocol_evidence 按名重读全量结构，替代基于预取摘要的家族级推断。
[36] player 两族未做全量 class_samples 对齐：预取每族仅两类样本，+22 类与 −1 类的具体差异未产出，无法排除“家族口径变宽”这一替代解释。
- [37] player_kotlin 净增的 22 类中没有任何一项被 decompile_class 反编译定性，是否含播放器控制/缓冲/会话类仍未知。
[38] PlayerBufferLocator / PlayerSpeedLocator / PlayerSpeedSessionLocator / PlayerCapabilityAccess / SponsorPlayerLocator 等定位器源码本轮未读取，其定位依据（固定描述符、返回类型还是方法体语义）未知，故 ±类数对命中率的影响方向无法判断。
[39] player 两族 runtime_enabled 仍为 unknown，complete_coverage=false；点位安装结果（installed/failed/ambiguous）与实际调用计数均未采集。
- [40] danmaku_legacy absent 的成因未定：家族归属规则（包名前缀/DEX 归属/方法体哈希）未读到，无法区分口径缺失与结构缺失。
[41] danmaku_java_moss 的 20 条实际调用边所属页面与渲染栈未逐个判定（原生/Compose/Opus/直播），无法确认其与视频弹幕净化的关系。
[42] danmaku_kotlin_moss 新增 2 条调用边未做 caller 差分定位，也未反编译定性，是否为 $default/重载包装产物未知。
- [43] DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt 本轮未读取，净化 Hook 的解析点形态、跨家族兜底与失败上报机制未知。
[44] 两个 Moss 协议仅比对定义数与实际调用边数，未做方法名与描述符集合差集，计数相等不足以证明协议面未变。
[45] 服务端控制样式（含灰度回滚）、平板/宽屏布局分支在静态证据中不可见，弹幕渲染样式家族是否穷尽未验证。
- [46] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，HEAD 5422fad1…）且 freshness=historical，任何源码结论都需按文件哈希追溯，不能视为发布态源码。
[47] 本轮 fresh_refresh 为空，未收到服务端对 comment/dynamic 之外页面的重新取证内容；本单元 story/mine 结论仅建立在预取 E009、E010 与模块侧 E013、E014、E015、E018 之上，若需复核口径变化须补一次重读。
[48] story：E009 仅含两族 summary、无 class_samples，+20 类 / +1 compose 方法 / +31 边 的类级归因（新样式 vs 包装层 vs 编译器产物）尚未完成，需按名重读 family_evidence 取差集与 method_bodies_sha256。
- [49] story：story_kotlin 两侧恒为 0（空集指纹 4f53cda1…），采集侧家族归并规则（Kotlin/Compose 实现是否一律计入 story_native）未确认，absent 的语义仍未知。
[50] story：StoryPurifyFeatureInstaller / StoryActionIconsFeatureInstaller / HomeVerticalDetailFeatureInstaller 的定位成员与期望类名/方法名/返回类型本轮未读，模块能否命中 9.18.0 story 结构为未知；E013、E018 只是其它页面的机制先例，不可外推。
[51] mine：mine_native 326←327 类、94←96 边的收缩型变化未做类名差集归因，无法区分合成/包装层合并与成员移除。
- [52] mine：mine_account_model 同基数异哈希（ebf9deed…→abd9520a…）尚未做同名类方法体哈希与字段表对拍，混淆改名、DEX 重排与方法体变化三种解释并存。
[53] mine：MineComponentFilterFeatureInstaller / MineVipFeatureInstaller / MineComponentSnapshotQueryContract / MineComponentSnapshot* / HostMineReadingCard 的解析点（硬编码名或 DEX 兜底）本轮未读，E014 的兜底先例属 comment 页，不能移用到 mine。
[54] mine：E015 显示 AccountMineRequestResource 等 mine 侧消费者落在 home_legacy 家族，跨家族消费者清单尚未系统枚举，家族计数不足以支撑覆盖结论。
- [55] story 与 mine 两条页面共四个家族 runtime_enabled 全为 unknown、module_coverage 全为 requires_installer_review：缺 9.18.0 真机 installer 安装日志（resolved/miss/ambiguous）与 Hook 回调计数，这是本轮无法给出适配结论的主因。
[56] 服务端下发样式开关、宽屏/平板布局分支在两页均未观测，静态矩阵不可见部分不能宣称已穷尽。
[57] 两页 protocols 均登记为空，但宿主存在大量未登记协议（如 MineMoss/KMineMoss、StoryMoss/KStoryMoss），其调用方是否构成 story/mine 的真实数据边界尚未核查。
- [58] source_snapshot working_tree_dirty=true（source_tree_sha256 37745f8f…，HEAD 5422fad1…），所有源码结论须按文件哈希追溯，未提交修改对定位逻辑的影响未评估。

## 下一步

- [1] 以 9.17.0 与 9.18.0 的类名集合差集复核 comment_native_legacy 减少的 16 个类，逐个核对是否出现在 CommentNativeBindingCatalog 登记表中，区分迁移、混淆改名与真删除。
[2] 对 comment_native_next 消失的 8 条调用边做调用方定位，判断是否被内联进 legacy_v2 或 compose 路径，避免把边减少误判为路径下线。
[3] 在 9.18.0 中验证 com.bilibili.lib.dd.DeviceDecision、kntr.base.dd.IDeviceDecisionKt、kntr.common.comment.entry.CommentSectionComposeFragment、kntr.common.comment.card.model.comment.CommentModel 四个 owner 的存在性与方法描述符，作为 CommentClassicStyleLocator 能否命中的前置条件。
[4] 用 CommentComposeViewAccess 与 CommentComposePurifyBridge 的匹配逻辑对照 comment_compose 新增的 6 个 compose 方法与 71 个类，列出未覆盖的可组合入口清单。
[5] 复核 dynamic_compose 的 kntr.app.following.followinglist 包是否存在指向动态页 tab 的调用边，先排除"关注页被归入同族"的替代解释，再决定是否为覆盖缺口。
- [6] 对 dynamic_legacy 新增的 76 条边按接收类聚类，确认是否集中到新的卡片 ViewHolder，并判断是否绕过现有净化 Hook 点。
[7] 真机运行 DynamicPurifyFeatureInstaller，记录 dynamic.purify.moss 解析、每个 feed 的同步/异步/Kotlin 包装安装结果与 missing 原因，重点看是否出现 no-dynamic-hook-point。
[8] 确认 KOpusMoss/OpusMoss 在 9.18.0 中是否有动态页调用方，以及 Opus 卡片是否共用 DynamicMoss 响应容器，用于判断 dynamic_opus 是否需要独立协议覆盖。
[9] 对两页四个 Moss 协议做方法名与描述符集合差集，替代仅比对定义数与边数，并在报告中显式记录未登记协议清单的处理结论。
[10] 在宽屏/平板与手机两种配置下分别抓取动态页 Compose 与 legacy 渲染日志，验证 dynamic_compose 的 LazyListState/ui.wide 使用是否对应真实双栏布局。
- [11] 记录本轮冻结源码工作树为 dirty（source_tree_sha256 37745f8f…，HEAD 5422fad1…），所有源码结论均需以该快照文件哈希追溯，不得视为发布态源码。
[12] 为 comment 与 dynamic 两页补齐 runtime_enabled 观测：在相同宿主版本下分别开启/关闭各路径相关开关，采集 Hook 命中计数并把 unknown 状态显式落入下一轮矩阵。
[13] 反编译 9.18.0，导出 com.bilibili.search2.discover.* 与 com.bilibili.search2.main.data.* 类清单与方法签名，逐条比对 SearchHomeRecommendLocator 的五项判据（E017）
[14] 抓取一次安装期定位日志，记录 locate 返回值、deliveryCandidateCount 与候选歧义情况，确认是否为静默 null
[15] 取 search_java_moss 的 caller_samples，确认 22 条实际调用边是否全部来自 search_compose，排除/确认 search_native 是 Java MOSS 消费者
- [16] 反编译 9.18.0 中 home_new_frame 的 tab/bottom 列表数据类，核对构造器数量与嵌套形态是否与 9.17.0 一致
[17] 对 9.17.0 与 9.18.0 做同名类方法体哈希对拍，列出 home_legacy 减少的 25 条外部调用边目标，判定内联或真实移除
[18] 读取 HomeFrameTabLocator、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller，确认构造器/字段定位失败时是否有兜底路径
[19] 真机验证 home：隐藏一个 tab 后重启，确认缺项与勾选面板可恢复；再验证 banner/推荐净化开关的实际效果
[20] 真机验证 search：在旧（原生）与 Compose 搜索页分别触发搜索，确认净化与猜你想搜 Hook 命中
- [21] 记录服务端开关/宽屏（平板）形态下的搜索与首页表现，标注哪些样式变化静态不可见
[22] 按 E017/E018 的 sha256 追溯源码快照（工作树 dirty），复核未提交修改是否影响上述定位逻辑
[23] 真机对比 9.17.0 与 9.18.0：在 PGC 详情页与 PGC 播放页分别采集 PgcAutoActivityPopupFeatureInstaller 安装日志与 PgcAutoActivityPopupLocator 诊断，记录 legacy/theseus 两路径候选数与命中数。
[24] 对 pgc_legacy 抽样 30 类（超出预取的 2 类样本）做方法体哈希与方法描述符对比，逐条归因 455→301 的调用边减少是内联折叠还是入口迁移。
[25] 复核 PgcAutoActivityPopupPolicy / PgcAutoActivityPopupFeatureInstaller 是否硬编码 legacy 类名或调用形态，并确认候选缺失时的兜底分支行为。
- [26] 抽取 pgc_theseus 新增的 3 个 compose 方法，定位其调用方，判定是否为新包装层，并确认该路径 PGC 页面是否存在重复安装风险。
[27] 对 detail_kotlin_moss 减少的 4 条调用边逐条还原到调用方类与方法描述符，读取 KotlinMossChannel / KotlinMossReplyBridge 的解析条件，判断是否依赖被改写的成员。
[28] 核查 detail_theseus_united 新增的 62 个类是否为 lambda/包装层，比对 98 个 compose 方法签名在两侧的对应关系，不将结构哈希变化直接记为样式新增。
[29] 复核 detail_legacy 的 absent：在 9.18.0 上做 DeviceDecision / CommentV3Fragment 装载探测并导出 dex.assist.comment_classic 诊断，区分登记口径缺失与宿主路径消失。
[30] 检查 DetailUnitedModulePurifyPolicy、DetailUnitedPresentationPurifyPolicy、DetailViewPurifyPolicy 是否依赖发生变化的成员名单，形成逐条命中清单。
- [31] 在平板/宽屏及被读取样本之外的布局模式下验证两条 pgc 路径的切换条件；服务端 A/B 若无结构变化则静态不可见，需按真机实际配置记录命中的路径。
[32] 补全 module_coverage：确认安装器对 detail 与 pgc 的定位器安装结果（当前均为 requires_installer_review），并记录失败项。
[33] 按名重读两个页面的完整家族与协议结构（预取每族仅 2 类样本、complete_coverage=false），避免用前几个类代表整套实现。
[34] 因 source_snapshot working_tree_dirty=true，按文件哈希追溯 module_source 的未提交改动，确保结论引用冻结快照而非本地修改。
[35] 用 family_evidence 分别取 player_kotlin/player_java 目标与基线全量 class_samples，按 method_bodies_sha256 与 compose_signatures 对齐，产出净增/净减类清单与可疑播放器类短名单。
- [36] 对 player_kotlin 净增类中的 2–3 个代表项调用 decompile_class，判定是否播放器控制/缓冲/会话类，排除“家族口径变宽”这一替代解释。
[37] 用 protocol_evidence 对 danmaku_java_moss 取全部 20 条 caller_samples，确认 Java 侧弹幕协议消费者所属页面与渲染栈（原生/Compose/Opus/直播）。
[38] 用 protocol_evidence 对 danmaku_kotlin_moss 做 target/baseline caller_samples 差分，定位新增的 2 条调用边的类与方法描述符并反编译定性。
[39] 读 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt（按固定 source_tree_sha256 追溯），核对净化 Hook 的解析点、是否存在跨家族消费者兜底与安装失败上报。
[40] 读 PlayerBufferLocator.kt / PlayerSpeedLocator.kt / PlayerCapabilityAccess.kt 等定位器，确认其定位依据是固定描述符、返回类型还是方法体语义，据此判断 ±类数变化对命中率的影响方向。
- [41] 核对 danmaku_legacy 家族归属规则（包名前缀/DEX 归属/方法体哈希），解释 classes=0 是口径缺失还是结构缺失，并记录结论所依据的源码哈希。
[42] 真机 attach（9.18.0 与 9.17.0 各一次）dump 版本适配器点位安装日志，统计 player 与 danmaku 各 Hook 点的 installed/failed/ambiguous 数量并按点位名归类。
[43] 在真机分别覆盖普通播放、番剧播放、小窗与宽屏/平板布局，验证缓冲、倍速、清晰度与弹幕净化 Hook 的实际调用计数，而非仅安装成功。
[44] 验证弹幕净化在开关打开与关闭两种状态下的差分行为，确认两条栈（Java/Kotlin）中至少各有一个可观测边界被命中。
[45] 记录服务端样式开关（若可灰度回滚）下弹幕渲染栈变化，明确静态不可见部分，不宣称所有样式已穷尽。
- [46] 在所有结论中保留 runtime_enabled=unknown 与 complete_coverage=false 标注；工作树 dirty 时按文件哈希引用源码，不建议清理工作树。
[47] 对 story_native、mine_native、mine_account_model 三个家族分别以 baseline/target 两侧重读 family_evidence，导出类名集合差集与同名类 method_bodies_sha256 对照表（本轮预取未下发这四个家族的类样本）。
[48] 对 mine_account_model 中 method_bodies_sha256 不同的类逐个用 decompile_class 读取，判定是纯改名、字段顺序变化还是读取逻辑变化。
[49] 读 StoryPurifyFeatureInstaller.kt、StoryActionIconsFeatureInstaller.kt、HomeVerticalDetailFeatureInstaller.kt 的定位成员，形成「模块期望的类名/方法名/返回类型」清单，用于与 9.18.0 静态矩阵对拍。
[50] 读 MineComponentFilterFeatureInstaller.kt、MineVipFeatureInstaller.kt、MineComponentSnapshotQueryContract.kt，确认其解析点是硬编码名还是走 DEX 兜底定位器。
- [51] 在 9.18.0 真机上抓模块安装日志，记录 story 与 mine 各 installer 的 resolved/miss 与 Hook 回调计数，验证 runtime_enabled 是否真为开启（当前为 unknown）。
[52] 检查 home_legacy 等非本单元家族中出现的 mine/account 调用者（如 AccountMineRequestResource 的使用点），登记为跨家族消费者以补齐影响面。
[53] 确认采集侧家族归并规则：story_native 内 45 个 compose 方法是否即为 Kotlin/Compose 实现，从而解释 story_kotlin 恒为 0。
[54] 针对宽屏/平板与服务端开关做一次真机对照（同版本双设备或改配置），确认 story/mine 是否存在静态不可见的视觉分支。