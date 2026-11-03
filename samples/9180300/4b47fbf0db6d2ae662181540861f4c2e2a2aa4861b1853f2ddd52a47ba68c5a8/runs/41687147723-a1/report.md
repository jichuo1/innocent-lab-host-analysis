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
| comment_compose | 2512 | 288 | 1125 | static_invoke_observed |
| comment_legacy_v2 | 576 | 0 | 728 | static_invoke_observed |
| comment_native_exp3 | 56 | 0 | 51 | static_invoke_observed |
| comment_native_legacy | 171 | 0 | 239 | static_invoke_observed |
| comment_native_next | 47 | 0 | 51 | static_invoke_observed |
| comment_other_ui:(root) | 226 | 2 | 479 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 24 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 221 | 0 | 129 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 251 | 31 | 306 | static_invoke_observed |
| danmaku_kotlin | 136 | 3 | 165 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1973 | 25 | 544 | static_invoke_observed |
| detail_theseus_united | 4675 | 99 | 4300 | static_invoke_observed |
| dynamic_compose | 1391 | 183 | 278 | static_invoke_observed |
| dynamic_legacy | 3271 | 105 | 2144 | static_invoke_observed |
| dynamic_opus | 1381 | 95 | 229 | static_invoke_observed |
| dynamic_other:appointment | 32 | 4 | 19 | static_invoke_observed |
| dynamic_other:card | 429 | 89 | 307 | static_invoke_observed |
| dynamic_other:commonCore | 26 | 0 | 62 | static_invoke_observed |
| dynamic_other:commonPerf | 13 | 1 | 2 | static_invoke_observed |
| dynamic_other:commonUi | 23 | 5 | 7 | static_invoke_observed |
| dynamic_other:lightBrowser | 83 | 19 | 30 | static_invoke_observed |
| dynamic_other:playershare | 1 | 0 | 3 | static_invoke_observed |
| dynamic_other_legacy | 2111 | 4 | 2126 | static_invoke_observed |
| home_legacy | 781 | 88 | 192 | static_invoke_observed |
| home_new_frame | 192 | 33 | 50 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 325 | 7 | 94 | static_invoke_observed |
| pgc_legacy | 358 | 1 | 327 | static_invoke_observed |
| pgc_theseus | 2256 | 131 | 813 | static_invoke_observed |
| player_java | 949 | 0 | 3298 | static_invoke_observed |
| player_kotlin | 473 | 37 | 886 | static_invoke_observed |
| search_compose | 3136 | 562 | 622 | static_invoke_observed |
| search_native | 1705 | 2 | 2845 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2961 | 45 | 1553 | static_invoke_observed |

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

本单元覆盖 comment（5 条登记路径）与 dynamic（3 条登记路径），基线 9180200 → 目标 9180300（同版本名 9.18.0，证书一致，arm64-v8a）。8 条路径在目标侧仍为 static_invoke_observed，但各家族指纹全部变化，类数、外部调用边数增减方向不一致（comment_compose 类数 -16、边 +10、compose 方法恒 288；comment_native_legacy -11 类 / -9 边；comment_native_next +3 类 / -6 边；dynamic_opus +32 类 / +5 边；dynamic_compose -22 类 / +8 边）。这些计数单位不同，不能相除或推断覆盖率，也不能据此判定新样式或功能消失。模块侧 CommentNativeBindingCatalog 以三个硬编码全限定名（LEGACY/NEXT/EXP3）在安装期解析绑定方法，未见兜底分支，若宿主改名/迁移则该家族静默 missing；CommentFamilyCoverage 明确把失败单位留在分母。所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review，installer 是否命中、真机是否启用均未验证，故本报告只给出待验证候选与补证任务，不宣称适配通过。服务端开关/AB 无结构变化时静态不可见，样式穷尽性未知。

本单元覆盖 home 与 search 两页、四条登记路径（home_legacy、home_new_frame、search_native、search_compose），目标 9.18.0/9180300 对基线 9180200。四条路径全部只有 static_invoke_observed：静态调用边存在，但 runtime_enabled 均为 unknown，module_coverage 均为 requires_installer_review，不能宣称适配通过。数值上变化集中在类数与外部调用边（home_legacy 781/785 类、192/184 边；home_new_frame 192/199 类、50/46 边；search_native 1705/1695 类、2845/2913 边；search_compose 3136/3152 类、622/614 边），两族 compose 方法数（88/33/2/562）与基线完全一致，说明指纹变化更像 DEX 重排/混淆改名，而非新增样式，但调用边方向性变化（home +8/+4、search -68/+8）需按族复核。模块侧读到两个真实定位器：HomeFrameTabLocator 依赖未混淆锚点 HomeFrameViewModel 与 serialName 精确比对，SearchHomeRecommendLocator 依赖 search2.discover/search2.main.data 的包名+短名有界枚举，二者都可能在宿主改名后静默不安装。search_compose 的深挖重读因只读预算耗尽未完成，相关判断保留为缺口。目录级结论：home 需按 frameSwitch 双框架分别真机验证；search 需分别验证原生列表与 Compose 主页两条并存栈。

本单元覆盖 detail 与 pgc 两页共 5 条登记路径。detail_legacy 在两版均登记为 absent；detail_theseus_ugc、detail_theseus_united 与 pgc_legacy、pgc_theseus 均仅为 static_invoke_observed。两版之间四家族指纹全部变化，类数、Compose 方法数与外部调用边数出现非等比甚至反向变动（ugc 类数 -2、边数 +22；pgc_theseus 边数 -100、Compose -1）。detail 侧 Java/Kotlin MOSS 定义数与调用边数两版一致，说明协议层未见结构变化。运行期启用、安装器解析命中、定位器兜底与 Hook 实际生效均未验证，module_coverage 仍为 requires_installer_review；下文变化一律按候选处理，不构成适配通过结论。

本单元审计 tv.danmaku.bili 9.18.0（9180300）相对 9180200 的 player 与 danmaku 两页，全部结论基于冻结静态证据与固定源码快照，未做真机验证，不代表适配通过。player_java 与 player_kotlin 两侧均为 static_invoke_observed，但类数与外部调用边、结构指纹同时变化（java 954→949 类、3305→3298 边；kotlin 466→473 类、897→886 边，compose_methods 37 不变）；danmaku_legacy 两侧均为 absent（0 类、同一空集指纹），danmaku_kotlin 137→136 类、164→165 边、compose_methods 3 不变。四条 moss 协议（player_java 18/2、player_kotlin 34/3、danmaku_java 22/20、danmaku_kotlin 46/12）定义数与实际调用边两版完全一致，未见协议面增删。两页 complete_coverage 均为 false、runtime_enabled 全为 unknown、module_coverage 为 requires_installer_review，安装器覆盖与真机启用均未证实；源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），源码侧结论只按文件哈希追溯，不推断未读源码的 Hook 覆盖。

本单元覆盖 story 与 mine 两页共 4 条登记路径。9180200→9180300 的静态差异集中在 story_native（类 2969→2961、外部调用边 1419→1553、compose 方法 45 不变）与 mine_native（类 327→325、边 94 不变、compose 7 不变）；mine_account_model 三项计数完全一致（132/0/43）但结构指纹仍变化，说明指纹对混淆改名/DEX 重排敏感，不能据此判定样式更新。story_kotlin 两侧均为空集指纹（4f53cda1…），本版本静态未检出该家族，不等价于 STORY 页无 Kotlin/Compose 实现。四条路径 evidence 分别为 static_invoke_observed、absent、static_invoke_observed、static_invoke_observed，runtime_enabled 全部 unknown，模块侧 story/mine 安装器源码正文本轮未读取，安装器与运行时覆盖均未验证，不宣称适配通过。资源层面仅 changed 1、无增删（E000）。

## 各页面评估

### comment

评论区在目标包仍有 5 条并存路径被静态观察：legacy_v2（576 类 / 728 边）、native_legacy（171 类 / 239 边）、native_next（47 类 / 51 边）、native_exp3（56 类 / 51 边）、compose（2512 类 / 288 compose 方法 / 1125 边）。相对基线变化方向不一致：legacy_v2 类 +2、边持平 728；native_legacy 类 -11、边 -9；native_next 类 +3、边 -6；native_exp3 类 -1、边 -4；compose 类 -16 但边 +10，且 compose 方法数 288 未变。类数下降与调用边上升同时出现，说明指纹变化可能来自混淆改名、DEX 重排或代码迁移，而非确定的新样式；两种计数不同单位，不得相除估覆盖率。协议侧 comment_java_moss（50 定义 / 50 实际调用边）与 comment_kotlin_moss（130 定义 / 23 实际调用边）在两侧完全一致，Kotlin 侧大量定义无实际调用边，是否被评论区家族消费静态未知。模块侧多处安装器（CommentClassicStyleLocator、CommentLegacyCopyBridge、CommentComposeCopyBridge/PurifyBridge、CommentNativeSupplementBridge、CommentReplyButton* 等）依赖类定位，CommentNativeBindingCatalog 直接写死三个 handler 全限定名且无兜底，native 三家族类数同时变化时定位命中率必须实测。全部路径 runtime_enabled=unknown，未见真机启用证据，unknown 家族不在登记范围内，不能外推。

证据：E000, E001, E011, E013

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 574→576（+2），外部调用边 728→728（持平），指纹由 8ca51ee1… 变为 f4e982e6…，compose 方法始终为 0。
- 可能影响：CommentClassicStyleLocator / CommentLegacyCopyBridge 等旧样式定位器与复制桥按类结构特征匹配，指纹变化但边数持平，可能只是改名/重排，也可能迁移了消费点；是否仍被评论区宿主加载未知。
- 验证：对两侧 legacy_v2 家族逐类比对 method_bodies_sha256，确认是否有真实方法体变化；在 9180300 真机进入视频详情评论区，观察 CommentClassicStyleLocator 的定位日志与 CommentFamilyCoverage.describe() 是否输出 legacy 相关 ok/partial/missing。
- 证据：E001, E013

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 182→171（-11），外部调用边 248→239（-9），指纹 32c92a7e…→4ef41d88…。
- 可能影响：CommentNativeBindingCatalog.LEGACY 为硬编码类名 com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler；类数收缩可能来自合并/改名，若目标包不再有该类，bindingMethods 返回空且无兜底，原生旧样式绑定与补充桥（CommentNativeSupplementBridge）会静默缺失。
- 验证：在 9180300 上用 KavaMemberLookup/类存在性检查确认三个 handler 全限定名是否仍存在且仍声明 CommentItem 类型字段；对缺失类记录为 missing 而非 partial，并在真机对比原生旧样式评论的净化与复制行为。
- 证据：E001, E013

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 44→47（+3），外部调用边 57→51（-6），指纹 39e97d04…→a2a28dd0…。
- 可能影响：同上，NEXT handler（nextholder.handle.CommentNextContentRichTextHandler）若改名或方法签名变化，安装期绑定可能部分/全部失败；边减少 6 条属于同一量级波动，不能单独证明降级。
- 验证：核对 NEXT handler 是否存在、是否仍有 1..5 参数且含 View 子类参数的 void 绑定方法；在真机原生新样式评论上检查绑定方法与净化/回复按钮生效情况，记录部分安装 vs 完全缺失。
- 证据：E001, E013

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 57→56（-1），外部调用边 55→51（-4），指纹 929d62b1…→78b078b6…。
- 可能影响：EXP3 handler（nextholderexp3.handle.CommentNextExperiment3ContentRichTextHandler）为实验外观家族，类数基本稳定、边小幅下降；实验样式由服务端开关控制，静态不可见其启用条件，不能确认该路径在真机出现。
- 验证：先确认 EXP3 类名与绑定方法仍可解析，再在开启对应实验的服务端配置账号上验证；若拿不到实验开关，明确记为未覆盖的运行条件而非通过。
- 证据：E001, E013

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2528→2512（-16），compose 方法 288→288（不变），外部调用边 1115→1125（+10），指纹 67e96ff5…→eec0da3c…。
- 可能影响：Compose 评论区仍由 CommentComposeCopyBridge / CommentComposePurifyBridge / CommentComposeViewAccess / CommentReplyButtonCompose 消费；类数下降而调用边上升，可能是 DEX 重排或调用点迁移，也可能是 CommentComposeViewAccess 依赖的视图访问点变换导致 Copy/Purify 桥失效。
- 验证：对 compose 家族逐类比对方法体哈希并抽查新增的 10 条外部调用边来源类；真机在 Compose 样式评论区验证复制、净化、回复按钮三条功能的安装日志与 CommentFamilyCoverage 记录（ok/partial/missing）。
- 证据：E001, E011

### dynamic

动态页目标包仍三条路径并存：dynamic_legacy（3271 类 / 105 compose 方法 / 2144 边）、dynamic_compose（1391 类 / 183 compose 方法 / 278 边）、dynamic_opus（1381 类 / 95 compose 方法 / 229 边）。相对基线：legacy 类 -2、边 -12；compose 类 -22、边 +8，compose 方法 183 不变；opus 类 +32、边 +5，compose 方法 95 不变。三家族指纹全部变化。类数与调用边数增减方向相互矛盾（compose 类减边增、opus 类显著增边微增），符合 DEX 重排/代码迁移特征，不能判定为新样式；也无法从计数推断模块 Hook 覆盖率。协议侧 dynamic_java_moss 134 定义 / 134 实际调用边两侧一致，dynamic_kotlin_moss 382 定义 / 27 实际调用边两侧一致，Kotlin 侧定义远多于实际调用边，是否有跨家族消费者静态未知。关键缺口：种子提供的 unregistered_protocols 含 app/dynamic/v2 的 OpusMoss、KOpusMoss 及 mall/tab3/dynamic/v1/OpusMoss、dynamic/interfaces/feed 的 FeedMoss/KFeedMoss 等，说明 Opus 相关服务协议尚未登记到本路径的协议覆盖里，dynamic_kotlin_moss 的 382 定义不能替代 Opus 协议消费者核实。模块侧 DynamicPurifyFeatureInstaller、DynamicPurifyPolicy、DynamicTabsFeatureInstaller、DynamicVideoTabPreference、KotlinDynamicMossWatch 与 HostAgentDynamicRpc 均按类/协议定位，未读到的运行条件（宽屏/平板、服务端开关、Tab 切换）保持未知，全部路径 runtime_enabled=unknown。

证据：E000, E002, E012

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3273→3271（-2），外部调用边 2156→2144（-12），compose 方法 105 不变，指纹 3a4ffd1e…→ac5e7b5b…。
- 可能影响：旧版原生动态列表仍是最大类集，DynamicPurifyFeatureInstaller / DynamicTabsFeatureInstaller 的定位若依赖具体类特征，指纹变化可能使净化或 Tab 改造只部分命中；边数小幅下降也可能只是调用点迁移。
- 验证：抽样比对两侧 legacy 家族方法体哈希，定位减少的 12 条外部调用边来源；真机在原生动态 Tab 检查 DynamicPurifyPolicy 是否实际被调用并输出安装日志。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 1413→1391（-22），compose 方法 183 不变，外部调用边 270→278（+8），指纹 9c970461…→7505ad5e…。
- 可能影响：Compose 动态流若被服务端开关或宽屏布局选中，其消费点变化会影响 DynamicPurifyFeatureInstaller 的策略注入；类减少而边增加说明结构确有变动但性质未定，可能在 Compose 内部调用链重排。
- 验证：确认动态 Compose 入口 Composable 与策略调用点是否仍存在，读取实际调用边新增来源；在平板/宽屏与手机两种布局下分别观察 Compose 动态渲染是否生效。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1349→1381（+32），compose 方法 95 不变，外部调用边 224→229（+5），指纹 e50b06c7…→787472ec…。
- 可能影响：Opus 家族类数明显增加，但对应服务协议 OpusMoss/KOpusMoss（app/dynamic/v2 与 mall/tab3/dynamic/v1）仍在 unregistered_protocols 中，dynamic_kotlin_moss 的 382 定义/27 边未确认覆盖 Opus 协议消费；因此模块对该路径的协议级 Hook 是否存在消费者、是否有兜底均未知。
- 验证：在登记协议集合补齐 OpusMoss/KOpusMoss 前，先静态确认哪些类引用这些 stub 并核对 classes 增量是否集中在新包（如 kntr/app/following/opusDetail）；真机进入 Opus 动态详情验证 DynamicPurifyPolicy/KotlinDynamicMossWatch 的日志与 missing 项。
- 证据：E002, E012, E000

### home

home 页登记两条路径，且宿主自 8.92.1 起同时打包两套首页框架。模块源码 HomeFrameTabLocator（E016，sha256 474ba2f5…）明确写出 MainActivityV2 通过 tv.danmaku.bili.common.home.c#b() 的 frameSwitch 二选一：屏幕尺寸档位 large/medium（平板、宽屏）、服务端 dd.use_new_home_frame 或 SP sp_key_new_home_frame_test 任一为真即走新框架，且新框架不经过 TabHost 和 HomeFragmentV2。这条陈述是模块作者对宿主的理解，本单元未在目标 DEX 中重读到 frameSwitch 的实现，因此只能作为待验证前提，不能当作已确认运行条件。静态数值：home_legacy 由 781 类/192 边/88 compose 方法（基线 785/184/88），home_new_frame 由 192 类/50 边/33 compose 方法（基线 199/46/33）；两族 compose 方法数与基线逐字相同，类数各减少 4 与 7，调用边反向增加，符合混淆改名与 DEX 重排的解释，但没有排除有方法被内联或迁移。深挖 E014 抽样确认目标中仍存在 Ltv/danmaku/bili/ui/main2/StartupFragmentV2、HomeFragmentV2 等 legacy 类；E015 抽样确认存在 Ltv/danmaku/bili/khome/vm/HomeFrameViewModel$dispatchAction$1，即 HomeFrameTabLocator 使用的未混淆锚点类名 HomeFrameViewModel 仍在目标中，这支持新框架定位器的第一个前提，但不证明后续 serialName、字段顺序、default_selected 判定在目标上成立。E016 还写明：若 default_selected 读不到，整层返回 Failed、过滤不安装，属于有意的失败单位。结论：两条路径都只有静态调用存在，真机启用与安装器覆盖均未验证，服务端 A/B 与宽屏分支静态不可见。

证据：E003, E014, E015, E016

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：目标 781 类、88 个 compose 方法、192 条外部调用边，指纹 30add8fd…；基线 785 类、88 个 compose 方法、184 条边，指纹 61d12f32…。类数 -4、调用边 +8，compose 方法数不变，属结构指纹变化而非新增 compose 样式。
- 可能影响：若真机当前走 legacy 框架，E014 抽样显示 StartupFragmentV2、HomeFragmentV2、AccountMineRequestResource 等类仍在，模块 HomeFrameListHook/BottomBar/HomeTopBar 一类安装器有可定位目标；但 E016 指出宽屏或服务端/SP 开关打开时宿主改走 khome，legacy 钩子可能装上也无人调用，表现为“无效果而非报错”。
- 验证：在 9180300 上分三种条件启动：手机档位并关闭 dd.use_new_home_frame 与 sp_key_new_home_frame_test；切到平板/宽屏档位；仅打开服务端开关。每种条件记录是否加载 HomeFragmentV2/TabHost 以及 HomeFrameListHook、HomeTabFilterFeatureInstaller 的安装日志，确认 legacy 路径的实际启用。
- 证据：E003, E014, E016

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：目标 192 类、33 个 compose 方法、50 条外部调用边，指纹 5108f740…；基线 199 类、33 个 compose 方法、46 条边，指纹 1bef27c7…。compose 方法数一致，类数 -7、边 +4。
- 可能影响：E015 抽样确认 tv.danmaku.bili.khome.vm.HomeFrameViewModel 及其 dispatchAction 协程体仍在目标中，HomeFrameTabLocator 的未混淆锚点前提成立；但其后续判定（HomeTabData/HomeTabItemData 的 serialName 精确比对、按 dex 字段排序重建顺序、default_selected 必须为 int）在 9180300 上未读到，任一不满足即返回 Failed 并整层不安装，影响底栏与顶栏 Tab 过滤、HomeFrameTabLocator 共用缓存。
- 验证：真机进入新框架后抓 HomeFrameTabLocator.resolve 的 Resolution（Found/Failed+reason），并核对 top/bottom 槽指向的字段与 default_selected 可读；随后确认底栏与顶栏 Tab 净化是否真的安装、服务端默认选中项（首页/推荐）是否被保留。
- 证据：E003, E015, E016

### search

search 页登记两条并存栈：search_native（1705 类/2845 边/2 compose 方法，基线 1695/2913/2）与 search_compose（3136 类/622 边/562 compose 方法，基线 3152/614/562）。两族 compose 方法数与基线逐字相同，search_native 调用边减少 68 而类数增加 10，search_compose 边增加 8 而类数减少 16；这种类数/边数反向变动更符合混淆改名、内联或 DEX 重排，但不能排除有调用点被迁移到另一族，因此不能据此判定样式变更，也不能据此判定覆盖完整。协议层登记的 search_java_moss（24 定义/22 实调用边）与 search_kotlin_moss（52/18）与基线完全一致，未见协议形状变化；但 seed 的 unregistered_protocols 同时列出 SearchMoss/KSearchMoss（app/interfaces/v1、app/search/v2、broadcast/message/search 等）与 KOpusMoss 等大量未登记协议，说明搜索与动态共同协议存在未归类的跨家族消费者，静态矩阵的 complete_coverage=false，缺失不能升级为无影响。深挖 E018 抽样确认目标仍有 Lcom/bilibili/search2/api/BaseSearchItem（未混淆，109 方法、52 字段，含 cardType/cardStyle/getCardStyle 等卡片样式入口）、com.bilibili.search2.stardust.expose.c、search2.result.o、search2.share.a，属于原生搜索家族主干，支持 search_native 仍是活体结构。E017（sha256 1c569369…）读到 SearchHomeRecommendLocator 的真实定位逻辑：以未混淆 SearchSquareType.getType、SearchReferral$Guess、com.bilibili.search2.discover.* 根类（a–z 与 SearchDiscoverViewModel）加 Outer$a–z/0–9 后缀枚举、com.bilibili.search2.main.data.* 单字母状态类、MainSearchViewModel 存在性为判据，并用 singleOrNull 做唯一性裁决。该定位器对短名池高度敏感，任一候选缺失或多出都会让 delivery 为 null 而不抛异常，安装器可能静默跳过。search_compose 的深挖重读在预算耗尽后失败，其内部类改动未核实，保留为缺口。

证据：E004, E017, E018

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：目标 1705 类、2 个 compose 方法、2845 条外部调用边，指纹 1e901ad8…；基线 1695 类、2 个 compose 方法、2913 条边，指纹 433d4628…。类数 +10、调用边 -68，compose 方法数不变。
- 可能影响：E018 抽样显示 BaseSearchItem、search2.stardust.expose、search2.result、search2.share 仍在目标中，原生搜索列表骨架存在；但外部调用边减少 68 条，若被清洗的卡片入口依赖具体调用边（如 Getter/Builder 变更），SearchPurifyFeatureInstaller 一类的安装点可能落入未命中分支。E017 也表明搜索推荐/主页数据走 discover 与 main.data 包，与原生列表分属不同定位点，二者不能互相代证。
- 验证：在 9180300 上打开搜索结果页，对比净化开/关时卡片类型集合与负反馈入口是否一致；抓 SearchPurifyFeatureInstaller 与 DefaultWordsCleaner 的安装结果与失败原因，并按 BaseSearchItem.getCardStyle/cardType 的实际实例核对是否有未处理的新 cardType。
- 证据：E004, E017, E018

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：目标 3136 类、562 个 compose 方法、622 条外部调用边，指纹 0ab85c9b…；基线 3152 类、562 个 compose 方法、614 条边，指纹 f6d999cc…。compose 方法数一致、类数 -16、边 +8。
- 可能影响：该类 compose 方法规模不变说明 Compose 实现主体未被替换；但 search_compose 家族在目标上的内部抽样因只读预算耗尽未能重读（缺口），无法确认是否包含 E017 所要求的 discover 根类、discover 内部投递宿主与 main.data 状态类。若投递宿主移出 a–z 与 SearchDiscoverViewModel 池，delivery 会为 null，SearchHomeRecommendFeatureInstaller 可能不安装而首页推荐/历史直出不被清洗。
- 验证：对 9180300 的 com.bilibili.search2.discover.* 与 com.bilibili.search2.main.data.* 做类清单核对（是否存在、是否为匿名内部类、重载签名是否仍为 List<SearchSquareType>/List<Guess> 单参数），再真机进入搜索主页抓 locate 返回值与 Points.deliveryCandidateCount，区分“宿主无该结构”与“候选歧义”。
- 证据：E004, E017

### detail

detail 页三路径中 detail_legacy 两版均为 0 类、0 Compose、0 边，fingerprint 为同一空集哈希，evidence=absent，只能说明冻结静态证据里没有该家族，不能推断旧原生详情页在真机消失。detail_theseus_ugc 类数 1975→1973（-2）、外部调用边 522→544（+22）、Compose 方法 25→25 不变；detail_theseus_united 类数 4669→4675（+6）、Compose 98→99（+1）、外部调用边 4193→4300（+107），两者指纹均变化。类数与边数不是同一单位，不能相除推导覆盖率；ugc 类数下降而边数上升，更像调用点/内联或兼容代码变化，而非整屏替换。detail_java_moss（定义 32、边 35）与 detail_kotlin_moss（定义 76、边 34）两版完全相同，说明共同协议层未观察到结构变化，变化集中在 UI 家族侧。模块侧 DetailModulePurify/UnitedModulePurify/UnitedPresentationPurify/DetailViewPurify 安装器与策略、HomeVerticalDetail 路由仅出现在源码清单中，本单元未读取其解析条件，故哪套净化策略命中 ugc 或 united、是否存在兜底均为未知。

证据：E000, E005, E013

#### 路径：detail_legacy

- 状态：absent
- 变化：两版均为 0 类、0 Compose 方法、0 外部调用边，fingerprint 相同（4f53cda1…b945，空集哈希），静态证据仍为 absent。
- 可能影响：模块无法在旧原生详情家族注册 Hook；是否存在其它家族承接旧入口、安装器是否因此走兜底路径均未知，不能用 absent 推断页面功能消失。
- 验证：真机分别从首页普通视频卡片与搜索/动态入口进入详情，记录实际承载 Activity/Fragment 与模块安装日志中的家族解析结果；对 absent 家族核对安装器是否记录 skipped 原因。
- 证据：E000, E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类数 1975→1973（-2）、外部调用边 522→544（+22）、Compose 方法 25→25 不变，fingerprint 由 5e32fd5a… 变为 fbab905a…。
- 可能影响：若 +22 边包含新增模块渲染/回调调用点，UGC 净化策略的匹配面可能漏项；反之若只是重排或内联，则现有策略仍可能命中。二者静态证据无法区分。
- 验证：按 owner+callee 描述符对齐两版边集，列出 ugc 新增/消失的具体调用点；对差异最大的若干点用 JADX 读方法语义；真机开 UGC 详情页并打开模块过滤，记录策略命中与新增模块类型是否被处理。
- 证据：E000, E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类数 4669→4675（+6）、Compose 方法 98→99（+1）、外部调用边 4193→4300（+107），fingerprint 由 c6cbf881… 变为 5ff05521…。
- 可能影响：唯一新增 Compose 方法可能是新的展示单元，现有 UnitedPresentation 策略若按固定签名或固定模块类型匹配，可能覆盖不到；也可能只是既有 Composable 的 lambda/内联产物，影响为零。
- 验证：定位新增 Compose 方法的 owner 与签名，检查策略匹配条件是否依赖该类名/签名；真机进 united 详情页，对比开关净化前后的展示单元清单与安装日志。
- 证据：E000, E005

### pgc

pgc 页两路径均观察到静态调用边，但走向相反：pgc_legacy 类数 357→358（+1）、Compose 方法 0→1、外部调用边 307→327（+20），fingerprint 变化，是 legacy 家族首次出现 Compose 方法的候选信号，可能与旧原生页中嵌入 Compose 弹窗/浮层有关；pgc_theseus 类数 2255→2256（+1）、Compose 132→131（-1）、外部调用边 913→813（-100），说明存在调用点合并、内联或路径减少，边数净减与类数微增同时出现，不能直接读作功能删减。两个 pgc 协议两版完全一致（player_moss 定义 12/边 3、view_moss 定义 14/边 7），协议层未见结构变化，变化集中在 UI 家族。模块侧仅有 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupPolicy/Installer 出现在源码清单，本单元未读取其定位锚点与兜底逻辑，因此弹窗定位是否依赖上述减少的调用边、以及平板/宽屏与服务端开关下的实际分支，全部为未知；pgc_legacy 新增的 Compose 方法是否落在弹窗路径上也未验证。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类数 357→358（+1）、Compose 方法 0→1、外部调用边 307→327（+20），fingerprint 由 e0071b25… 变为 8b3b022f…；该家族首次出现 Compose 方法。
- 可能影响：若新增 Compose 方法承载活动弹窗或浮层，按 View/Adapter 结构注册的 legacy Hook 可能完全拦截不到，出现“旧路径已 Hook 但弹窗仍在”的效果；也可能新方法与广告/活动无关。
- 验证：读该 Compose 方法的 owner 与调用方，确认其是否位于弹窗/活动展示链；真机在 PGC 旧详情/播放页触发活动弹窗，分别记录 Hook 命中与未命中时的视图层级，并与服务端活动开关开/关各测一次。
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类数 2255→2256（+1）、Compose 方法 132→131（-1）、外部调用边 913→813（-100），fingerprint 由 53ca22f6… 变为 d45b73aa…；协议侧 pgc_player_moss 与 pgc_view_moss 两版计数不变。
- 可能影响：净减 100 条边可能使 PgcAutoActivityPopupLocator 原先依赖的调用点锚点消失，导致定位失败或落到兜底分支；也可能是同一逻辑被内联合并，锚点仍在。静态边数无法判定定位器是否仍能命中。
- 验证：按 owner 汇总两版 pgc_theseus 边集差异，标出被移除边的 owner 是否出现在定位器候选路径中；用 JADX 复核定位器读取的字段/方法签名在新包中是否仍存在；真机记录安装期定位日志与弹窗触发结果。
- 证据：E000, E006

### player

播放页两条登记路径都存在静态调用，但都发生了结构变动且运行条件未知。player_java 由 954 类/3305 外部调用边变为 949 类/3298 边，指纹 746cdb81…→f78e5c5c…；降幅仅 5 类、7 边，相对家族总量属微调级，符合 R8 混淆改名合并、DEX 重排或少量类迁移的表现，不能据此认定出现新播放样式。player_kotlin 反向变化：类 466→473（+7）、外部调用边 897→886（−11）、compose_methods 保持 37、指纹 f314119…→2942010…；Compose 入口方法数未变，说明新增 7 个类更可能落在非 Compose 数据/工具层，但仍需按名核实是否属于播放器面板相关包。协议面 player_java_moss（18 定义/2 实际调用边）与 player_kotlin_moss（34 定义/3 边）两版完全一致，说明播放页协议方法面未见增删，变化集中在本地实现结构。源码侧模块为该页准备了 PlayerBufferLocator/PlayerSpeedLocator/SponsorPlayerLocator/PlayerCapabilityAccess 等多个按结构解析的定位器，配合 E013 所显示的覆盖记账语义（安装失败保留在分母、类存在不升级为完整覆盖），当前 evidence=static_invoke_observed 与 module_coverage=requires_installer_review 只能说明调用边存在，无法说明对应定位器在目标 APK 上解析成功，也无法说明 Hook 在真机生效。是否影响缓冲、倍速、赞助屏蔽等具体功能，属未知，需按路径条目给出的最小补证任务逐条确认。

证据：E000, E007, E013

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：目标 949 类/3298 外部调用边/指纹 f78e5c5c…，基线 954 类/3305 边/指纹 746cdb81…；类数与边数同向小幅下降，player_java_moss 定义 18、实际调用边 2 两版一致。
- 可能影响：若消失的 5 个类中包含模块定位器依赖的锚点类或字段（缓冲、倍速、赞助、能力开关相关定位器均在候选源码清单内），相应功能可能在安装期解析失败且静态无差异；目前无运行条件证据，影响面未知。
- 验证：用 family_evidence(family=player_java,side=target/baseline) 按名重读两侧类清单取差集，再用 module_source 读 PlayerBufferLocator.kt、PlayerSpeedLocator.kt、SponsorPlayerLocator.kt 的解析锚点逐条对照；真机装模块后抓安装结果日志确认是否 Installed 且 complete。
- 证据：E007, E000, E013

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：目标 473 类/37 compose_methods/886 外部调用边/指纹 2942010b…，基线 466 类/37/897 边/指纹 f3141193…；类增边减，Compose 入口数不变；player_kotlin_moss 定义 34、实际调用边 3 两版一致。
- 可能影响：新增 7 个类若位于播放器面板/倍速/画质相关包，可能是旧实现迁移或包装层；边数下降可能来自调用内联或合并。当前无法判定对面板 Hook 的影响，属未知。
- 验证：用 family_evidence(family=player_kotlin) 重读两侧类名差集，对新增类与消失类各取 1–2 个用 decompile_class 读方法签名，判断是否为迁移或改名；真机在播放页对比倍速与画质面板实际呈现。
- 证据：E007, E000

### danmaku

弹幕页两条登记路径状态差异明显。danmaku_legacy 在目标与基线两侧都是 0 类、0 外部调用边、指纹同为 4f53cda1…（空集哈希），evidence 为 absent；这是登记口径下没有可枚举类，不等于旧弹幕功能消失，也不能反推模块 legacy 净化路径已失效或已生效。danmaku_kotlin 两侧均有静态调用：目标 136 类/3 compose_methods/165 边/指纹 29da02c2…，基线 137 类/3/164 边/指纹 b65c81e6…，属类减 1、边增 1 的微调，叠加指纹变化，需要先排除混淆改名与 DEX 重排再谈样式变化。协议面更值得注意：danmaku_java_moss 有 22 个定义且实际调用边达 20，danmaku_kotlin_moss 有 46 个定义、12 条实际调用边，两版数值完全一致——说明弹幕协议方法面稳定且确有消费者，而 legacy 家族却被登记为 absent，二者并存更可能是家族归类口径问题（legacy 类被并入 kotlin 家族或落入未归类协议消费者），需要按类名核实而不是按家族标签下结论。模块侧 DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 的定位条件、兜底分支以及是否跨家族消费同一协议，静态证据未覆盖，且三条路径 runtime_enabled 全为 unknown；按 E013 的记账语义，类存在或调用边存在都不能升级为完整覆盖，故本页最终适配状态仍为未验证。

证据：E000, E008, E013

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线两侧均为 0 类、0 外部调用边，指纹同为 4f53cda1…（空集哈希），无差异；同期 danmaku_java_moss 仍有 22 定义/20 实际调用边。
- 可能影响：该家族在登记口径下无可枚举类，模块 legacy 弹幕净化定位路径的静态落点无法证实；可能是归类缺失，也可能是实现已并入其他家族或未归类协议消费者，功能是否受影响未知。
- 验证：用 module_source 读 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt，确认定位锚点是否硬依赖 legacy 类名及有无兜底分支；再在目标侧按弹幕相关类名直接检索，并用 family_evidence(danmaku_java,side=target) 核对 20 条调用边的消费者归属。
- 证据：E008, E000, E013

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：目标 136 类/3 compose_methods/165 外部调用边/指纹 29da02c2…，基线 137 类/3/164 边/指纹 b65c81e6…；类减 1、边增 1、Compose 方法数不变；danmaku_kotlin_moss 46 定义/12 实际调用边两版一致。
- 可能影响：小幅差异更像混淆改名、DEX 重排或单类迁移，尚无证据指向新弹幕样式；但若消失的 1 个类承载净化/发送回调锚点，弹幕净化与发送过滤可能受影响，当前运行条件未知。
- 验证：用 family_evidence(family=danmaku_kotlin) 重读两侧类清单取差集并对差异类用 decompile_class 读方法体；真机在视频页开关弹幕与净化功能并抓安装器日志，确认净化安装结果与是否命中该家族。
- 证据：E008, E000

### story

story_native 是本页唯一静态可观察家族：类数 2969→2961（-8），外部调用边 1419→1553（+134），compose 方法 45→45，指纹由 a5c8e67f… 变为 3ae368a1…，evidence 保持 static_invoke_observed（E009、E000）。调用边显著增长而类数略减，更像宿主内部调用被内联、包装层合并或新增调用目标，而非控件家族新增；但预取只给摘要，消失的 8 个类与新增边的目标描述符均未读到，因此该判断仍是候选解释。story 页 protocols 字典两侧均为空，无法从协议侧解释边增长；未注册协议清单含 app/story/v1/StoryMoss 与 KStoryMoss，但清单不按页归属，消费者归属未知。模块侧 source_files 列出 HomeVerticalDetailFeatureInstaller/Routing、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess，正文本轮未读，Hook 选择器（混淆类名、方法签名或结构过滤）无法确定，不得推测覆盖。story_kotlin 两侧 0 类 / 0 compose 方法 / 0 边，指纹为空集哈希 4f53cda1…，evidence=absent；这表示该家族在本版本静态未检出，STORY 内容可能由 story_native 内的 45 个 Compose 方法承载。两项结论均需真机与源码补证，不能写成已适配。

证据：E000, E009, E016

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：classes 2969→2961（-8），external_invoke_edges 1419→1553（+134），compose_methods 45→45，fingerprint a5c8e67f…→3ae368a1…，evidence 仍为 static_invoke_observed（E009、E000）。
- 可能影响：若 STORY 相关安装器按具体混淆类或方法签名 Hook，调用点迁移会使安装命中率下降；是否影响动作图标、净化策略与视频竖屏详情路由未知，本轮未读安装器正文。
- 验证：对两版本 story_native 类集合按 method_bodies_sha256 做差集，列出消失的 8 类与新增外部调用边的目标描述符；用 decompile_class 反编译新增边目标确认是否落在 STORY 卡片/动作条渲染；真机在 STORY 页查看安装日志与开关生效情况。
- 证据：E000, E009, E016

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧均为 classes 0、compose_methods 0、external_invoke_edges 0，fingerprint 同为 4f53cda1…（空集哈希），evidence=absent，无可比差异。
- 可能影响：该家族静态未检出，不能据此认为 STORY 页不存在 Kotlin/Compose 实现；story_native 的 45 个 Compose 方法可能是实际渲染者，Kotlin MOSS 通道在本页的覆盖未知。
- 验证：读取 story_native 的 compose_signatures 明细，确认 Composable 是否属于 STORY 容器；核对 KotlinMossChannel / KotlinMossReplyBridge 在真机的安装日志与本页是否存在回连请求；若两者皆无，登记 absent 维持并在报告中保留缺口。
- 证据：E000, E009

### mine

mine_native 与 mine_account_model 两条路径均为 static_invoke_observed，但变化形态不同。mine_native：类 327→325（-2）、外部调用边 94→94、compose 方法 7→7，指纹由 a259ab51… 变为 7b5ce0f2…；边与 Compose 方法完全不变而类数减 2，最省解释是包装/合成类合并或迁移，也可能是真实功能类移除，需差集确认。mine_account_model：类 132、compose 0、边 43 三项两侧一致，指纹却由 91335afb… 变为 63bdafd5…；同一 APK 内计数不变而哈希变化，直接印证结构哈希不是样式判别器，可能是混淆改名、DEX 顺序或常量池变化。资源层面仅 changed 1、无新增删除（E000）。协议侧 mine 页 protocols 为空，未注册清单含 app/mine/v1/MineMoss 与 KMineMoss，共同协议是否有跨家族消费者未登记，属于覆盖缺口。模块侧来源含 MineComponentFilterFeatureInstaller、MineComponentSnapshot 及其 Store/QueryClient/QueryContract/HostBridge、MineVipFeatureInstaller、HostMineReadingCard，正文本轮未读，无法判断其定位依赖类名还是结构条件，因此组件过滤、VIP 卡片、阅读卡在 9180300 的安装结果均记为未知。

证据：E000, E010, E013

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：classes 327→325（-2），external_invoke_edges 94→94，compose_methods 7→7，fingerprint a259ab51…→7b5ce0f2…，evidence 保持 static_invoke_observed（E010）。
- 可能影响：消失的 2 个类是否属于组件过滤、VIP 或阅读卡所依赖的持有类未知；边数不变提示外部调用面未扩张，但静态不可判定 Hook 是否仍能命中。
- 验证：对 mine_native 类集合做方法体哈希差集，列出消失的 2 类及其父类/字段用途；用 decompile_class 确认是否为合成或包装类；真机在“我的”页查看 MineComponentFilter、MineVip、HostMineReadingCard 的安装与运行日志。
- 证据：E000, E010, E013

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：classes 132→132、compose_methods 0→0、external_invoke_edges 43→43 完全一致，fingerprint 91335afb…→63bdafd5…；证据值为 static_invoke_observed，属“计数不变、哈希变”的形态（E010）。
- 可能影响：提示该族未新增类型，变化可能仅来自混淆改名、字段顺序或常量池；但若指纹由方法体真实变化驱动，账号模型语义变化会影响依赖该模型的模块快照与登录态展示，当前无法区分。
- 验证：对 132 个类按方法体哈希与字段名集合逐类对拍，若差集为空即判定为重排/改名；若存在非空差集则升级为语义变化并重新评估 MineMoss 消费者；同时用 module_source 读取 MineComponentSnapshotStore 确认快照键是否含混淆类名。
- 证据：E000, E010

### F001：原生评论三套外观 handler 依赖硬编码类名、catalog 内无结构回退，目标包三族指纹变化后安装器命中率未验证
事实：E013 显示 CommentNativeBindingCatalog 把 LEGACY=com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler、NEXT=…nextholder.handle.CommentNextContentRichTextHandler、EXP3=…nextholderexp3.handle.CommentNextExperiment3ContentRichTextHandler 写成常量，mainHandlers 顺序 EXP3→NEXT→LEGACY；bindingMethods 仅当类存在、声明字段类型名以 .CommentItem 结尾时才枚举 1..5 参数、含 View 子类参数的非静态非桥接 void 方法，否则返回 emptyList；catalog 内未见按父类、接口或类名模式回退的替代定位器。E021 显示 CommentPurifyFeatureInstaller 在 points==null 时仍会安装 compose 桥并调用 installKotlinChannel，最后以 missing("missing-adapter-point") 记账，因此 catalog 解析为空不会静默升级为成功，但也没有第二套原生定位器承接。E001/E019 给出三族双侧计数：native_legacy 182→171 类、248→239 边，native_next 44→47 类、57→51 边，native_exp3 57→56 类、55→51 边，三族指纹全部改变。推断：指纹变化与类/边小幅波动可能来自改名、内联或 DEX 重排，不能据此断言某个 handler 类结构改变；但硬编码绑定一旦失配即整族 zero-hook，是明确的结构性风险。未知：三个全限定名在 9180300 是否仍存在、是否仍声明 .CommentItem 字段、绑定方法签名是否仍在 1..5 参数窗口内；缺哪一族、是否被服务端外观开关关闭均未取证。
反例与替代解释：若目标上三个全限定名均存在且字段/签名检查通过，则本次风险收敛为混淆改名导致的指纹变化，可推翻“绑定失败”推断；若仅 LEGACY 失配而 NEXT/EXP3 正常，更可能是旧样式被服务端下线而非模块回归，需外观开关证据区分；若 points 非空但 catalog 为空、而 compose 桥与 kotlin 通道照常安装（E021 路径），则表现为原生样式无 hook 而 Compose 样式正常，属 api 层缺失而非渲染层失效。
建议：先在目标包对三个全限定名做类存在性与字段类型检查（.CommentItem 结尾、含 View 子类字段或 getRoot()），再对缺失家族比对两侧绑定方法签名集合；真机读取安装日志中每个家族 resolved/missing 结果与 CommentFamilyCoverage.describe()，把缺失单位保留在分母。若确认某族改名，补的是基于字段类型+View 参数特征的结构化兜底定位，而不是第四个硬编码类名。
证据：E013, E001, E019, E021

### F002：comment_compose 类数下降但外部调用边增加 10 条，复制/净化桥的真实消费点未确认
事实：comment_compose 目标侧 2512 类、288 个 compose 方法、1125 条外部调用边，基线 2528/288/1115（E011、E001/E019）；E011 的 5 个抽样类覆盖 kntr/common/comment/common/service/*、imageviewer/data、card/action，其中至少两个类方法体哈希为空集（e3b0c44…），说明抽样里混有空壳/签名类，抽样不足以代表 2512 类。compose 方法数两侧恒为 288，而类数与调用边反向变化，这种矛盾本身是 DEX 重排、类内联/拆分或调用点迁移的典型形态，两侧单看任一侧都会得出相反结论，不能判定为新样式或渲染路径消失。E022 显示 CommentComposeViewAccess 只依赖 androidx compose 运行时（getLocalView、Composer.consume 以及 CompositionLocal 类型），不依赖宿主混淆名，因此 compose 家族类数变化不能直接推成“视图访问点变换导致复制/净化桥失效”；现存风险更集中在被 Hook 的 Composable 调用点与 VersionAdapter 提供的 purify 点位是否仍被调用。E021 显示安装器对每项能力分别记账（installedCount/expectedCount、缺失项加入 missing 组），可据安装日志区分 partial 与 missing。未知：新增 10 条外部调用边的来源类、减去的 16 个类是否为无方法体空壳、真机 Compose 样式下复制/净化/回复按钮三项能力各自的安装结果。
反例与替代解释：若差分显示变化集中在空壳类且方法体哈希与基线一一对应，则类数下降是噪声，“消费点迁移”推断可推翻；若新增边来自真实 Compose UI 调用链并绕过已 Hook 的点位，则支持迁移假设；若三项能力安装计数完整而功能仍异常，问题应转向运行时策略而非定位，需另取 Hook 命中日志。
建议：先做逐类方法体哈希差分：确认减去的 16 类是否为空方法体空壳、288 个 compose 方法是否一一对应；再定位新增 10 条外部调用边的来源类，检查其是否仍经过已 Hook 的 Composable 与 purify 点位；真机在 Compose 样式评论区读取每项能力的 installed/expected 与 missing 组，记录复制、净化、回复按钮三项分别 ok/partial/missing。
证据：E011, E001, E019, E022

### F003：dynamic_opus 类数 +32 而 Opus 服务协议仍在未登记清单，协议级共同消费者与兜底无法确认
事实：dynamic_opus 目标侧 1381 类、95 个 compose 方法、229 条外部调用边，基线 1349/95/224（E012、E002/E020），compose 方法数不变、指纹整体改变；已登记协议 dynamic_java_moss 134 定义/134 实际调用边、dynamic_kotlin_moss 382 定义/27 实际调用边两侧完全一致，说明本轮差异不在已登记协议集合内。E012 给出的 5 个抽样类全部落在 kntr/app/following/opusDetail/api（A/B/C、CompositeExternalInterceptor 及 firstSnapshotFile$1、handleAdClick$1 等协程续体），类名指向广告与外部拦截辅助逻辑，提示 +32 类可能集中在 API/拦截侧而非渲染侧；但样本 5/1381，只能当线索，不能据此断定样式或渲染路径变化。协议层事实：种子 unregistered_protocols 明确列出 app/dynamic/v2 OpusMoss、KOpusMoss，mall/tab3/dynamic/v1 OpusMoss，dynamic/interfaces/feed FeedMoss、KFeedMoss，均未进入本路径协议登记；定义数与实际调用边数不是同一单位，382:27 既不能算覆盖率，也不能证明这些 stub 无跨家族消费者（可能存在接口分发或反射调用）。未知：opusDetail 新类是否实现或调用上述 stub、是否被净化策略消费、是否有兜底；相关模块安装器源码本轮未读取，故不对其 Hook 选择器作任何推断。
反例与替代解释：若登记补齐后 OpusMoss 消费者均经由已 Hook 的共同协议入口且无漏点，则“协议覆盖缺口”可推翻；若新增 32 类确为广告/快照拦截辅助（CompositeExternalInterceptor、handleAdClick 命名暗示此路径），则类数增长既不代表新样式也不代表协议变化，应作为干扰项排除；若新增类确实承载渲染或净化策略调用点，才升级为渲染侧结构变化候选。
建议：先把 OpusMoss/KOpusMoss/mall-tab3 OpusMoss 与 FeedMoss/KFeedMoss 登记进 dynamic 路径协议集后重算实际调用边与消费者类；静态确认 kntr/app/following/opusDetail 新增类（含 CompositeExternalInterceptor 系列）是否引用这些 stub，并检查包级分布确认 +32 类是否集中在拦截/广告辅助包；真机进入 Opus 动态详情读取净化相关安装与命中结果，同时记录平板/宽屏与服务端开关条件。
证据：E012, E002, E020

### F004：新首页框架未混淆锚点在目标存在，但 serialName/字段序判定细节与失败分支未静态核实
事实：E015 的 home_new_frame 抽样包含 Ltv/danmaku/bili/khome/vm/HomeFrameViewModel$dispatchAction$1，其 this$0 类型与 E016 常量 VIEW_MODEL_CLASS = tv.danmaku.bili.khome.vm.HomeFrameViewModel 逐字一致，说明 9180300 仍保留该未混淆锚点，定位器至少能开始两跳泛型收集。E016 可见注释还表明：解析依赖 Companion serializer() 的 SerialDescriptor.serialName 与 TAB_DATA_SERIAL/TAB_ITEM_SERIAL 精确比对，并按 dex 字段排序规则重建声明顺序、要求与反序列化构造器 (int, 元素类型…) 的参数窗口逐类型相同，结果按 ClassLoader 缓存。E003 显示该族由 199 类/46 边变为 192 类/50 边、Compose 方法数恒为 33，属结构指纹变化，不能据此判定新样式或功能消失。推断：真正风险是严格比对不满足时定位失败、相关 Tab 过滤表现为“不生效但不报错”；但失败分支的具体形态（是否返回 Failed、是否整层不安装，是否有 default_selected 类型门槛）在 E016 的可见摘录之外，未读到，不能当作已确认。
反例与替代解释：若真机只走 legacy 框架（手机档位且两个开关均关），该定位器不会被调用，本次结构变化与首页过滤无关；若真机定位成功且 Tab 行为符合预期，则类数/边数差异可归因于混淆与 DEX 重排，本发现应降级为无影响。
建议：先补读 HomeFrameTabLocator.kt 完整解析体（失败返回值类型、default_selected 判定、缓存写入条件），再在 9180300 真机以宽屏档位或打开 dd.use_new_home_frame / sp_key_new_home_frame_test 进入新框架，记录定位返回值与失败原因字符串，并核对 top/bottom 槽字段、default_selected 实际取值以及底栏/顶栏过滤是否真正安装生效。
证据：E003, E015, E016

### F005：搜索主页推荐定位器以 discover/main.data 固定短名池与类型化投递边界解析，目标侧候选数未核实
事实：E017 显示 SearchHomeRecommendLocator 以未混淆锚点 SQUARE=com.bilibili.search2.api.SearchSquareType、GUESS=SearchReferral$Guess、固定前缀 DISCOVER=com.bilibili.search2.discover. 与 STATE=com.bilibili.search2.main.data. 组成一级候选（discover.a–z 与 discover.SearchDiscoverViewModel）与二级匿名内部类后缀池（a–z、0–9），注释明示探测失败以 ClassNotFoundException 计，且 Points.deliveryCandidateCount 仅用于区分“宿主没有该结构”与“候选歧义”，不参与功能判定。E004 显示 search_native 由 1695 类/2913 边变为 1705 类/2845 边、search_compose 由 3152 类/614 边变为 3136 类/622 边，Compose 方法数不变，属结构变动而非已确认新样式。E018 可见样本支持 search2.api.BaseSearchItem（52 字段、109 方法，含 cardType 与 getCardStyle）、search2.stardust.expose.c、search2.result.o 仍在；但该抽样未覆盖 discover 与 main.data 包，也未覆盖 search2.share，不能据此判定 discover 结构存续或消失。推断：若投递宿主移出既有短名池或候选不唯一，定位可能返回空投递并导致推荐/历史直出不安装；该 null 分支与唯一性裁决的具体实现（如 singleOrNull）在 E017 摘录外，未读到。
反例与替代解释：若投递宿主名仍落在既有短名池内且候选唯一，则当前风险仅存在于极端命名，可判为未触发；若目标改用未登记的 SearchMoss/KSearchMoss 通道直接投递而不经 discover 类，则失效原因在协议路径迁移而非命名池，需按协议锚点重新定位。
建议：先补读 SearchHomeRecommendLocator.locate 完整实现与 quickLocate 差异，再对 9180300 枚举 com.bilibili.search2.discover.*、com.bilibili.search2.main.data.* 与 MainSearchViewModel 的类清单及接收方法签名（是否仍为单参数 List<SearchSquareType> / List<Guess>），随后真机记录 locate 返回值与 deliveryCandidateCount，区分宿主无结构、候选歧义与结构命中三种情形。
证据：E004, E017, E018

### F006：home_legacy 结构指纹变化但 compose 方法数不变，指向混淆/重排；宽屏与服务端开关使其可用性无法静态确定
事实：E003 显示 home_legacy 由基线 785 类/184 边/88 compose 方法变为 781 类/192 边/88 compose 方法，compose 方法数逐字相同；E014 抽样确认目标仍存在 tv.danmaku.bili.ui.main2.StartupFragmentV2、HomeFragmentV2、AccountMineRequestResource 等 legacy 主干类，说明该类不是被整体移除。E016 明确写出宿主自 8.92.1 起由 MainActivityV2 用 tv.danmaku.bili.common.home.c#b() 的 frameSwitch 在 legacy 与 khome 间二选一，且宽屏 large/medium 档位、服务端 dd.use_new_home_frame 或 SP sp_key_new_home_frame_test 都会改走新框架。推断：类数与边数的反向小幅变动更像混淆改名与 DEX 重排，不构成新样式证据；但 legacy 钩子的实际调用时机取决于 frameSwitch，在本单元未重读该宿主方法的情况下无法静态确定，属“装得上但可能无人调用”的高风险结构。
反例与替代解释：若三种条件下均走 legacy 且钩子调用计数正常，则当前指纹变化可判定为无害混淆/重排；若宽屏条件下 HomeFragmentV2 从不实例化，则 legacy 相关 Hook 需要按 khome 路径补兜底，而非修复 legacy 定位。若进一步在 DEX 中读到 frameSwitch 的实际常量开关名与默认值，可推翻“服务端可控不可见”的判断。
建议：分别以手机档位关闭两开关、平板/宽屏档位、仅开服务端开关三种条件冷启动 9180300，记录 MainActivityV2 走的是哪套框架、TabHost/HomeFragmentV2 是否被实例化，以及 HomeFrameListHook、HomeTabFilterFeatureInstaller 的安装与调用计数，确认 legacy 路径在真实分支下的启用状态。
证据：E003, E014, E016

### F007：详情页两套 Theseus 家族外部调用边均上升、类数方向不一致，不能据此判定新样式
事实：detail_theseus_ugc 由 1975 类/522 边/25 Compose 变为 1973 类/544 边/25 Compose；detail_theseus_united 由 4669 类/4193 边/98 Compose 变为 4675 类/4300 边/99 Compose；两版 version_name 同为 9.18.0，但 version_code 9180200→9180300、APK sha256 与 size 均不同，属相邻构建。两族变化方向并不一致：ugc 类数下降而边数上升（-2/+22），united 类数、Compose 方法与边数同向上升但幅度悬殊（+6/+1/+107）。detail_java_moss 与 detail_kotlin_moss 两版定义数/边数完全一致（32/35、76/34），说明已登记的共同协议层没有结构变化，变化集中在 UI 家族。推断：ugc 更符合 R8 内联/调用点集中或兼容分支调整；united 的 +1 Compose 也可能是既有 Composable 的 lambda/内联产物，故两族均不能读作整套详情实现替换或新样式落地。E013 显示同一 feature 层的覆盖记账把未注册方法留在分母，明确不允许由“类存在/边存在”升级为完整覆盖（该源码属评论家族安装器，仅作口径佐证，不代表 detail 安装器实现）。未知：DetailModulePurify/UnitedModulePurify/UnitedPresentationPurify/DetailViewPurify 安装器未读取，ugc 与 united 的命中条件、候选歧义与安装失败兜底未验证；未登记的 ViewMoss/LegacyViewMoss 变体消费者未核对；服务端 module 开关对家族选择的影响未知；runtime_enabled 全为 unknown。
反例与替代解释：若边集差异全部落在同一 owner 的既有方法体内或仅 lambda/桥接方法改名，则属编译器/DEX 重排，本推断被推翻；若 JADX 显示新增边指向新的广告/活动模块类型且策略未覆盖，则从 candidate 升级为需补 Hook 的具体缺口；若真机日志显示 ugc 家族解析成功且净化命中情况与基线一致，则影响判断不成立。
建议：先对两版按 owner+callee 描述符对齐边集，分别输出 ugc/united 的新增与消失清单，标注是否 lambda/bridge，并对差异最大的 5 个调用点用 JADX 读语义，确认是内联产物还是新增展示/回调；再读 DetailModulePurifyPolicy 与 DetailUnitedModulePurifyPolicy 的匹配条件，核对 united 新增 Compose 方法签名是否落入覆盖范围；真机分别进入普通视频（UGC）详情与 united 详情，记录安装日志中的家族解析结果、策略命中数与未注册方法数，并在服务端 module 开关切换后复测，全程不把类/边存在当作覆盖。
证据：E000, E005, E013

### F008：PGC 两路径变化方向相反：legacy 在两版对比中首次出现 Compose 方法计数，theseus 外部调用边净减 100
事实：pgc_legacy 357→358 类、Compose 方法 0→1、外部调用边 307→327（+20）；pgc_theseus 2255→2256 类、Compose 方法 132→131（-1）、外部调用边 913→813（-100）；pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两版完全不变。推断：协议层稳定而 UI 家族侧同时出现“legacy 出现 Compose 方法计数”和“theseus 调用边净减”，可确认 UI 家族调用图发生了静态变化；但变化是否落在活动弹窗/浮层展示链上尚未确认，-100 边也可能来自内联合并或同一逻辑迁移，legacy 的 0→1 亦可能来自 compose_signatures 识别口径或方法签名变化而非真实新增 Composable，故不能读作功能删减，absent 类结论同样不适用。unknown：PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupPolicy/Installer 的候选构造方式（按字段/签名还是按调用边祖先）、候选歧义处理与失败兜底本单元均未读取；legacy 新增 Compose 方法的 owner 与调用方未定位；未登记的 pgc gateway view v1 KViewMoss 消费者未核对；平板/宽屏档位与服务端活动开关造成的分支未验证；两路径 runtime_enabled=unknown、module_coverage=requires_installer_review。
反例与替代解释：若 pgc_theseus 被移除的 100 条边全部属同一 owner 的内部调用、且定位器读取的方法签名仍存在，则锚点未移动，本推断被推翻；若 legacy 新增 Compose 方法经 JADX 确认为识别口径/签名变化产物或与活动弹窗无调用关系，则对弹窗 Hook 无影响；若真机在服务端活动开关开与关下均观察到定位器成功且弹窗被抑制，则风险降为无适配缺口的候选变体（仍需记录为未覆盖的服务端变体）。
建议：先读 PgcAutoActivityPopupLocator/PgcAutoActivityPopupPolicy/PgcAutoActivityPopupInstaller，记录锚点形态、候选歧义与失败兜底；再按 owner 对齐两版 pgc_theseus 边集，标出消失边的 owner 是否出现在定位器候选路径，并用 JADX 复核定位器读取的字段/方法签名在新包中是否仍存在；对 pgc_legacy 的 compose_signatures 明细与新增 Compose 方法用 JADX 定位 owner 与调用方，判断是真实新增展示单元、识别口径变化还是与活动弹窗无关的渲染迁移；真机在 PGC 旧详情与 theseus 详情各触发一次活动弹窗，记录定位成功/失败日志，并在服务端活动开关开/关、宽屏与手机布局下各复测。
证据：E000, E006

### F009：player_java 类数与调用边小幅同降、指纹变化，优先按混淆/重排解释；定位器锚点尚未核实
目标 9180300 相对基线 9180200，player_java 由 954 类/3305 外部调用边变为 949 类/3298 边，结构指纹 746cdb81…→f78e5c5c…；同期 player_java_moss 的定义数 18 与实际调用边 2 两版完全相同，player_kotlin 466/897→473/886 且 compose_methods 保持 37，一侧减类减边、一侧增类减边，协议面计数未动。这种形态优先解释为 R8 混淆改名、DEX 重排或少量类迁移，结构哈希变化本身不证明出现新播放样式，也不证明旧样式失效。真正需要排查的是这 5 个消失类与 7 个新增类是否为模块定位器依赖的锚点：候选源码清单（E000）中有 PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、SponsorPlayerLocator、PlayerCapabilityAccess 等多个按类结构与字段解析的定位器，若消失类恰是其锚点，安装期解析可能落空；但定位器也可能使用未混淆的稳定名或序列化名锚点（同类思路见 E016），此时类名漂移对其无影响，因此影响面属未知而非常见故障。E013 显示的“失败单位留在分母、类存在不升级为完整覆盖”来自评论家族的 CommentFamilyCoverage，属同模块记账语义示例，不能替代播放页安装结果。E007 只提供汇总摘要、无类样本，故 player_java 的 static_invoke_observed 与 requires_installer_review 只能视为待验证。
反例与替代解释：若差集出的类全部是混淆内部类、合成 lambda 或协程状态机类（如 E012 中 CompositeExternalInterceptor$…$1 这类 ContinuationImpl 形态），则结构变化无功能含义，本推断被推翻；若这些类是包内改名后的等价物（方法签名与字段类型可比对一致），则锚点仍在，影响不成立；反之若锚点字段类型或 getRoot 类结构消失，则推断成立。另一替代解释是定位器本就走未混淆锚点（类似 E016 的序列化名比对与 E017 的短名候选枚举），那家族层面的类名漂移就与它无关，须逐条核对模块源码才能定论。第三种可能是边数下降来自内联或调用合并而非类删除，需按 owner+callee 描述符比对边集。
建议：第一步用 family_evidence(family=player_java, side=target) 与 side=baseline 按名重读（E007 仅汇总，需取类清单）得到两侧类名差集并记录消失类；第二步用 module_source 逐条读取 PlayerBufferLocator.kt、PlayerSpeedLocator.kt、PlayerSpeedSessionLocator.kt、SponsorPlayerLocator.kt、PlayerCapabilityAccess.kt，记录每个定位器使用的锚点（是否依赖混淆类名、字段名、getRoot 形态）与失败兜底分支，再与差集对照，标出实际受影响的定位器；第三步对差集类抽样 decompile_class 判断是迁移改名还是删除，并核对 -7 条外部调用边是否由内联产生；第四步真机安装模块，在播放页抓安装结果与 Hook 日志，分别验证缓冲、倍速、赞助屏蔽是否被触发并记录定位失败日志。
证据：E007, E000, E013

### F010：弹幕 legacy 家族两侧 absent 而 java/kotlin moss 仍有 20/12 条实际调用边，须先判定归类缺失再判定功能影响
danmaku_legacy 在目标与基线两侧都是 0 类、0 外部调用边、同一哈希，按登记口径为 absent；由于两侧一致，本次升级没有可观测的家族级回归，且 absent 不等于旧弹幕功能消失。与此同时 danmaku_java_moss 有 22 个定义、20 条实际调用边，danmaku_kotlin_moss 有 46 个定义、12 条实际调用边，两版计数完全一致：这提示弹幕协议方法面在本次升级中未见增删，但计数相同并不排除方法体替换、调用边换 owner 或消费者变化；且这 20 条边的消费者类尚未识别，不能默认属于弹幕业务。danmaku_kotlin 侧 137→136 类、164→165 边、compose_methods 3 不变、指纹 b65c81e6…→29da02c2…，属微调级差异，同样需先排除混淆改名与 DEX 重排再谈样式候选；家族归属是否因归类口径（legacy 类并入 kotlin 家族，或落入未归类协议消费者，如 unregistered_protocols 中的 live DanmuMoss）而整体偏移，静态摘要无法判定。模块 DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 出现在候选源码清单（E000）但本轮未读取，其类名/协议锚点、跨家族消费与失败兜底均未知；E013 中“失败单位留在分母”来自评论家族的 CommentFamilyCoverage，只能作为同模块记账语义类比。两条登记路径 runtime_enabled 均为 unknown、module_coverage=requires_installer_review。
反例与替代解释：若 DanmakuPurifyPolicy 同时匹配 kotlin 家族与协议路径，或 installer 有明确兜底分支，则 legacy absent 对功能无影响，本推断降级为纯归类问题；若这 20 条 danmaku_java_moss 调用边实际来自播放统计、在线人数等非弹幕业务，则不能作为弹幕路径存在证据，需重新分配家族；若真机上弹幕净化仍生效且有安装成功日志，则说明差异仅为命名与归类。反向推翻条件是：真机日志显示净化 installer 因找不到类而安装失败，且失败类名属于 legacy 家族，或 base apk 中确不存在 legacy 侧的净化/发送回调实现类。第三种可能是弹幕渲染已迁至播放器家族或未登记协议，需按类名检索确认。
建议：用 module_source 读取 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt，列出类名/协议锚点、跨家族匹配条件与兜底分支；用 family_evidence(family=danmaku_kotlin, side=target/baseline) 取类名差集，对差异类用 decompile_class 读方法体，判断是否承载净化或发送回调；再追查 danmaku_java_moss 那 20 条实际调用边的消费者类 owner 与方法名，判断是否属弹幕业务；核对 unregistered_protocols 中弹幕相关 MOSS（如 live DanmuMoss）与本页路径的关系；最后真机在视频页开关弹幕与净化，记录安装结果、命中家族与类缺失堆栈。
证据：E008, E000, E013

### F011：story_native 类减 8、外部调用边增 134：须先排除 DEX 重排/调用点迁移，才谈 STORY Hook 是否受影响
事实：目标 story_native 2961 类 / 1553 外部调用边 / 45 Compose 方法，基线 2969 / 1419 / 45，两侧 evidence 均为 static_invoke_observed，指纹 a5c8e67f…→3ae368a1…（E009、E000）。类数减 8 与外部调用边增 134 方向相反，静态上至少有三类未区分解释：宿主新增外部调用目标或调用点上移、内联与包装层重构导致调用面重排、DEX 重排/混淆改名造成的类别集合差异；预取仅给每家族 2 个类样本，消失的 8 类与新增边的目标描述符均未读到，故不能断言“未涉及 STORY 渲染路径”，也不能判定为新样式或功能消失。story 页 protocols 字典两侧为空，只说明本页未登记协议消费者，不构成“无协议侧解释”的证明；未注册清单含 app/story/v1/StoryMoss 与 KStoryMoss，其消费者归属与兜底未知。模块侧 source_files 列出 HomeVerticalDetailFeatureInstaller/Routing、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess，本轮未读正文，Hook 选择器是混淆类名、方法签名还是结构过滤无法确定，不得推算覆盖。E016 显示首页 khome 定位器以未混淆锚点 + SerialDescriptor.serialName 精确比对、不依赖逐版变化的混淆名，可作为“story 安装器是否同构”的对照假设，但它是首页框架定位器证据，不是 story 页覆盖证明。story_kotlin 两侧 0 类、指纹为空集哈希 4f53cda1…，属 absent：仅表示未检出，不等于 STORY 页没有 Kotlin/Compose 实现，story_native 内 45 个 Compose 方法的归属仍未核实。结论保持 needs_runtime：静态结构变化已确认，是否影响 STORY 功能需源码与真机补证。
反例与替代解释：可推翻当前推断的证据：a) 差集为空或消失的 8 类全为编译器合成/桥接/重复包装类、新增边目标仅描述符字面差异 → 应改判为构建噪音而非调用点迁移；b) 新增边目标明确落在 STORY 卡片或动作条渲染方法 → 从“Hook 可能落空”转为“渲染路径扩张、需重定 Hook 点”；c) module_source 显示 story 安装器与 E016 同构（锚点+序列化名/结构过滤）→ 类名变化不足以导致失败，需另解释边增长；d) 真机日志显示安装成功且功能生效 → 静态边增仅为宿主重构，影响下调；e) 若 story_native 的 45 个 Compose 方法确认为 STORY 容器且 KotlinMossChannel 无本页回连 → 可维持 story_kotlin absent 并记录为协议层缺口。
建议：1) 对两版本 story_native 类集合按 method_bodies_sha256 做集合差集，输出消失的 8 类与新增 134 条外部调用边的目标描述符清单，先判定是否为空差集/纯重排（构建噪音）。2) 对落在 STORY 卡片、动作条、渲染容器的差集目标用 decompile_class 反编译确认调用语义。3) 用 module_source 读取上述 6 个 story 相关文件，逐条记录 Hook 选择器形态与失败兜底。4) 读取 story_native 的 compose_signatures 明细，确认 45 个 Composable 是否属 STORY 容器，并据此解释 story_kotlin 的 absent。5) 真机在 STORY 页与视频竖屏详情验证动作图标、净化开关、免费推广数据访问，抓取安装失败日志与家族解析结果。6) 追查 StoryMoss/KStoryMoss 是否存在跨家族消费者，补登协议或明确记为未知。
证据：E009, E000, E016

### F012：mine_account_model 计数一致而指纹变化：指纹不可作样式判别器；变化来源与 mine_native 减 2 类的影响仍属未知
事实：mine_account_model 两侧 classes 132、compose_methods 0、external_invoke_edges 43 完全相同，fingerprint 由 91335afb… 变为 63bdafd5…；mine_native classes 327→325、external_invoke_edges 94→94、compose_methods 7→7，fingerprint a259ab51…→7b5ce0f2…；两条路径 evidence 均保持 static_invoke_observed（E010、E000）。可静态确认的是：计数不变而哈希变化说明该指纹不是类型增减或新样式的判别依据，不能用指纹变化反推 mine 页发生了样式切换。但变化来源仍未确定——方法体内容修改、常量池/字符串、注解与字段顺序、DEX 重排或混淆改名都会产生相同观察，本轮未做逐类方法体哈希对拍，故不能把“仅重排/改名”写成结论，也不能把哈希变化当作语义变更证据。资源层面 added=0、removed=0、changed=1（E000），仅能排除资源驱动的结构解释，不解释代码侧哈希。mine 页 protocols 两侧为空，只表示未登记协议消费者；未注册清单含 app/mine/v1/MineMoss 与 KMineMoss，跨家族消费者与兜底策略未登记，属覆盖缺口。模块侧来源含 MineComponentFilterFeatureInstaller、MineComponentSnapshot（Store/QueryClient/QueryContract/HostBridge）、MineVipFeatureInstaller、HostMineReadingCard，本轮未读正文，无法判断快照键与过滤器是否写入混淆类名、是否有兜底；E013 显示评论侧安装以字段类型/返回类型等结构条件筛选绑定方法并把失败单位保留在分母，属同类策略对照，不构成 mine 覆盖证据。mine_native 消失的 2 类是否为组件过滤/VIP/阅读卡依赖的持有类未确认。结论保持 static_evidence：结构性观察成立，功能影响未知。
反例与替代解释：可推翻当前判断的证据：a) 若逐类方法体哈希差集非空（存在真实改体/增删方法），则“重排/改名”解释不成立，需按语义变化重审指纹一并重估账号模型对快照的影响；b) 若 mine_native 消失的 2 类被证明是组件过滤器或阅读卡直接依赖的持有类，影响从“未知”升级为优先修复项；c) 若 module_source 显示快照键/过滤器含混淆类名且无兜底，则类名变化本身即可导致过滤项静默丢失，属确定性缺口；d) 若真机日志显示三类 Hook 均安装成功且行为一致、且逐类对拍确认仅重排，则计数与指纹差异可降级为构建噪音。
建议：1) 对 mine_account_model 逐类比对方法体哈希与字段名/字段类型集合：差集为空则记为可解释的重排/改名；差集非空则升级为语义变化并重估账号模型字段对快照的影响。2) 对 mine_native 差集定位消失的 2 类，确认父类、字段类型、引用方，判断是合成/包装类还是业务持有类。3) 用 module_source 读取 MineComponentSnapshotStore、MineComponentSnapshotQueryContract、MineComponentFilterFeatureInstaller、MineVipFeatureInstaller，检查快照键与过滤器是否依赖混淆类名/方法名、失败是否有兜底。4) 真机在“我的”页验证组件过滤、VIP 卡片、阅读卡的安装状态，并在重复进入页面后复核一致性。5) 补登或明确记录 MineMoss/KMineMoss 的消费者归属，未取得证据时保留为未知。
证据：E010, E000, E013

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
复核采用 fresh_refresh E019 与预取 E001 的目标/基线双侧数据：五条路径在目标侧仍只有 static_invoke_observed。计数为 legacy_v2 576 类/728 边（基线 574/728）、native_legacy 171/239（182/248）、native_next 47/51（44/57）、native_exp3 56/51（57/55）、comment_compose 2512 类/288 compose 方法/1125 边（2528/288/1115）。类数与外部调用边增减方向互不一致，而 compose 方法数与两侧完全一致的 Java/Kotlin MOSS 定义数（50/50、130/23）说明现有一致性变化更像混淆改名或 DEX 重排，不能判定新样式或功能消失；两类计数单位不同，禁止相除估覆盖率。E013 证实 CommentNativeBindingCatalog 把 LEGACY/NEXT/EXP3 三个全限定名写死，mainHandlers 顺序 EXP3→NEXT→LEGACY，bindingMethods 在类缺失或字段类型不以 .CommentItem 结尾时返回 emptyList，catalog 内部确无按结构回退的兜底定位器；但 E021 显示 CommentPurifyFeatureInstaller 在 points 缺失时仍会走 compose 桥并调用 installKotlinChannel，最后以 missing(...) 记账，因此“缺失即静默成功”的说法需要校正为“catalog 无替代定位器、但安装层有降级与分母记账”。E022 进一步表明 CommentComposeViewAccess 通过 androidx compose ABI（getLocalView 与 Composer.consume）解析，与宿主混淆类名无关，compose 家族类数变化不能直接推成视图访问/复制桥失效；复制与净化的失败风险更可能落在注入点解析与 VersionAdapter 点位。E011 的 5 个抽样类中含方法体哈希为空集（e3b0c44…）的空壳类，抽样无法代表 2512 类整体。全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，未取得任何真机安装或命中日志；评论相关 ReplyMoss/KReplyMoss 仍在 unregistered_protocols 中，共同协议跨家族消费者未知。
证据：E019, E001, E011, E013, E021, E022

### 复核页面：dynamic
复核采用 fresh_refresh E020 与预取 E002 双侧数据：三条路径目标侧均只有 static_invoke_observed，dynamic_legacy 3271 类/105 compose 方法/2144 边（基线 3273/105/2156）、dynamic_compose 1391/183/278（1413/183/270）、dynamic_opus 1381/95/229（1349/95/224）。两族 compose 方法数完全不变而类数与调用边反向变化，属重排/迁移候选而非已确认新样式；已登记协议 dynamic_java_moss（134 定义/134 实际调用边）与 dynamic_kotlin_moss（382/27）两侧数值一致，说明本轮结构差异不在已登记协议集合内，且定义数与实际调用边数不是同一单位，382 个定义远多于 27 条边既不能证明也无从否认 Opus 协议的跨家族消费者（可能存在接口分发或反射调用）。E012 的 5 个抽样类集中在 kntr/app/following/opusDetail/api（A/B/C、CompositeExternalInterceptor 及其 firstSnapshotFile$1、handleAdClick$1 等续体），类名指向广告/快照拦截辅助逻辑，提示 +32 类可能落在 API 拦截侧而非渲染侧，但 5/1381 的抽样不能外推到整族，只能作为待验证线索。协议层缺口具体：种子 unregistered_protocols 含 app/dynamic/v2 OpusMoss、KOpusMoss，mall/tab3/dynamic/v1 OpusMoss，dynamic/interfaces/feed FeedMoss/KFeedMoss，均未登记进本路径协议集。模块侧 DynamicPurifyFeatureInstaller/DynamicPurifyPolicy/DynamicTabsFeatureInstaller/DynamicVideoTabPreference 的定位锚点与兜底本轮因工具预算耗尽未读取，按规则不作任何 Hook 覆盖推断。服务端外观/实验开关与平板宽屏分支静态不可见，所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review。
证据：E020, E002, E012

### 复核页面：home
home 登记两条路径，均只有 static_invoke_observed：home_legacy（781 类/88 Compose 方法/192 外部调用边，基线 785/88/184，E003）与 home_new_frame（192/33/50，基线 199/33/46，E003）。两族 Compose 方法数与基线逐字相同，类数各减 4 与 7、调用边反向增加，符合混淆改名/DEX 重排解释，但未排除内联或迁移，计数单位不同也不能推导覆盖率。运行侧 runtime_enabled=unknown、module_coverage=requires_installer_review，两条路径均未验证安装命中。E014 抽样中 StartupFragmentV2、HomeFragmentV2 只以字段/构造器类型出现在 ui.main2 包装类样本里，未见其本身作为类样本；E015 抽样含 khome/vm/HomeFrameViewModel$dispatchAction$1。E016 的 frameSwitch、large/medium 档位与 dd.use_new_home_frame / sp_key_new_home_frame_test 二选一仅为模块作者在源码注释中的陈述，本单元未在目标 DEX 重读 MainActivityV2 分支，服务端 A/B 与宽屏分支静态不可见。
证据：E003, E014, E015, E016

### 复核页面：search
search 登记两条并存栈，均为 static_invoke_observed：search_native（1705 类/2 Compose 方法/2845 外部调用边，基线 1695/2/2913）与 search_compose（3136/562/622，基线 3152/562/614，E004）。两族 Compose 方法数不变，原生族类数 +10 而边 -68、Compose 族类数 -16 而边 +8，方向相反，不能据此判定新样式、覆盖完整或功能消失。协议层 search_java_moss（24 定义/22 实调用边）与 search_kotlin_moss（52/18）与基线一致，未见协议形状变化，但 complete_coverage=false，多个 SearchMoss/KSearchMoss 变体仍未归类。E018 可见样本支持 BaseSearchItem（52 字段/109 方法，含 cardType、getCardStyle）与 search2.stardust.expose.c、search2.result.o 仍在；摘录未包含 discover 包或 search2.share.* 样本，属有界抽样。E017 可见 ROOT_NAMES（discover.a–z + SearchDiscoverViewModel）、NESTED_SUFFIXES、DISCOVER/STATE 常量与 Points.deliveryCandidateCount，支持“短名池 + 候选歧义”风险，但 locate 实现体在摘录之外，唯一性裁决与 null 分支未读到；search_compose 内部结构亦未复核。
证据：E004, E017, E018

### 复核页面：detail
detail 页三条登记路径分别核对，状态严格沿用静态矩阵。detail_legacy：两版均 0 类/0 Compose/0 外部调用边，fingerprint 同为 4f53cda1…（空集哈希），status=absent；只能说明冻结静态证据中无该家族，不能用 absent 推断旧原生详情页在真机消失或功能缺失。detail_theseus_ugc：status=static_invoke_observed，类 1975→1973（-2）、外部调用边 522→544（+22）、Compose 方法 25→25 不变，fingerprint 5e32fd5a…→fbab905a…。detail_theseus_united：status=static_invoke_observed，类 4669→4675（+6）、Compose 98→99（+1）、外部调用边 4193→4300（+107），fingerprint c6cbf881…→5ff05521…。类数与调用边不是同一单位，禁止相除或据此推导覆盖率；ugc 类降边升更像调用点集中/内联或兼容分支调整，united 唯一的 +1 Compose 也可能是既有 Composable 的 lambda/内联产物，两者均未确认。detail_java_moss（32 定义/35 边）与 detail_kotlin_moss（76 定义/34 边）两版完全一致，共同协议层未见结构变化，变化集中在 UI 家族侧；未登记的 ViewMoss/LegacyViewMoss 变体消费者仍未核对，故「共同协议无遗漏」不能断言。模块侧 DetailModulePurify/UnitedModulePurify/UnitedPresentationPurify/DetailViewPurify 及 HomeVerticalDetail 路由只出现在源码候选清单，本单元未读取其解析锚点、候选歧义处理与失败兜底，因此 ugc/united 实际命中哪套策略、缺失家族是否走兜底均为未知。所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本页不宣称适配通过。
证据：E000, E005, E013

### 复核页面：pgc
pgc 页两条登记路径均核对，状态严格沿用静态矩阵。pgc_legacy：status=static_invoke_observed，类 357→358（+1）、Compose 方法 0→1、外部调用边 307→327（+20），fingerprint e0071b25…→8b3b022f…；在该两版对比中首次出现 Compose 方法计数，但 0→1 也可能来自 compose_signatures 识别口径变化或方法签名变化而非真实新增 Composable，需与真实新增区分。pgc_theseus：status=static_invoke_observed，类 2255→2256（+1）、Compose 132→131（-1）、外部调用边 913→813（-100），fingerprint 53ca22f6…→d45b73aa…；边数净减可能与类数微增同源于内联合并、同逻辑迁移或路径减少，不能读作功能删减，也不能据此判定定位器锚点失效。协议侧 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两版完全一致，说明变化不在已登记协议层；但未登记的 pgc gateway view v1 KViewMoss 消费者未核对，跨家族共用情况仍未知。模块侧 PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupPolicy/Installer 仅在源码清单中出现，本单元未读取其候选构造方式（按字段/签名还是按调用边祖先）与失败兜底，故 -100 边是否触及定位锚点、legacy 新增 Compose 方法是否落在活动弹窗/浮层路径均为未知。平板/宽屏档位（large/medium）与服务端活动开关分支静态不可见，未被排除；两路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本页不宣称适配通过。
证据：E000, E006

### 复核页面：player
player 两条登记路径在 E007 中均为 static_invoke_observed：player_java 954 类/3305 外部调用边（基线）→ 949/3298（目标），player_kotlin 466/897 → 473/886，compose_methods 保持 37；两族指纹均变化，而两侧 moss 计数完全一致（player_java_moss 18 定义/2 实际调用边，player_kotlin_moss 34/3）。E007 只下发汇总摘要、无类样本，因此消失的 5 类与新增的 7 类身份未取得差集，指纹变化既不等于新播放样式，也不等于功能失效。模块侧缓冲、倍速、赞助、能力、画质、状态栏等定位器与安装器仅出现在候选源码清单（E000），本轮未读取其解析锚点，Hook 覆盖未知；E013 的覆盖记账语义只来自评论家族 catalog，只能作为同模块记账实现示例，不能充当播放页安装结果。两条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本页结论保持待验证，不宣称适配通过，也无证据判定具体功能失效。
证据：E007, E000, E013

### 复核页面：danmaku
danmaku 两条登记路径状态不同（非三条）。danmaku_legacy 在基线与目标两侧均为 0 类/0 外部调用边/同一哈希，evidence=absent，说明基线即无该家族，本次升级未产生可观测回归，absent 也不等于旧弹幕功能消失。danmaku_kotlin 137 类/164 边 → 136/165，compose_methods 3 不变，指纹变化属微调级。协议侧 danmaku_java_moss（22 定义/20 实际调用边）与 danmaku_kotlin_moss（46/12）两版计数完全一致，提示协议方法面未见增删，但相同计数不排除方法内部替换与调用边消费者变更；20 条 java_moss 边的消费者身份未取证，不能默认属弹幕业务，unregistered_protocols 中另有 live DanmuMoss 等未登记项。DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 仅见于候选清单（E000），锚点、兜底与跨家族消费均未读取。两条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本页不能判定净化生效或失效。
证据：E008, E000, E013

### 复核页面：story
story 页登记两条路径。story_native 状态 static_invoke_observed（E009、E000）：classes 2969→2961（-8）、external_invoke_edges 1419→1553（+134）、compose_methods 45→45，fingerprint a5c8e67f…→3ae368a1…；runtime_enabled=unknown、module_coverage=requires_installer_review，因此仅确认存在静态调用边，不确认真机启用、也不确认模块安装命中。两个方向相反的计数变化在预取样本（每家族 2 类）内无法归因：新增调用目标、内联/包装层重构、DEX 重排或混淆改名都能产生同类观察，未做类级方法体哈希差集前不能判定为新样式、功能消失或 Hook 落空。story_kotlin 状态 absent：两侧 0 类/0 Compose 方法/0 边、指纹为空集哈希 4f53cda1…，表示该家族本版本静态未检出，不能反推 STORY 无 Compose 实现（story_native 内 45 个 Compose 方法的归属未核对）。story 页 protocols 两侧为空，仅表示未登记协议消费者；未注册清单含 app/story/v1/StoryMoss 与 KStoryMoss，归属与兜底未知。模块侧 HomeVerticalDetailFeatureInstaller/Routing、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess 正文本轮未读，选择器形态未知，不得推算覆盖。补证：类级差集与新增边目标反编译、compose_signatures 明细、逐文件 module_source、STORY 页真机安装与功能日志。
证据：E009, E000

### 复核页面：mine
mine 页两条路径均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E010、E000）。mine_native：classes 327→325（-2）、external_invoke_edges 94→94、compose_methods 7→7，fingerprint a259ab51…→7b5ce0f2…；消失的 2 类身份未读出，是否为组件过滤/VIP/阅读卡依赖的持有类未知，边与 Compose 方法不变提示外部调用面未扩张，但不足以判定 Hook 仍可命中。mine_account_model：classes 132、compose_methods 0、外部边 43 三项两侧一致而 fingerprint 91335afb…→63bdafd5…，静态可确认指纹不能判别类型增减或新样式；但变化来源（混淆改名/DEX 重排/常量池 vs 方法体语义修改）本轮未区分，需逐类方法体哈希对拍后才能定级。资源层 added=0、removed=0、changed=1，不能解释代码侧哈希差异。mine 页 protocols 两侧为空，仅指未登记协议消费者；未注册清单含 app/mine/v1/MineMoss 与 KMineMoss，跨家族消费与兜底未登记。模块侧 MineComponentFilterFeatureInstaller、MineComponentSnapshot 及其 Store/QueryClient/QueryContract/HostBridge、MineVipFeatureInstaller、HostMineReadingCard 正文本轮未读，快照键与过滤器是否写入混淆类名未知；E013 只显示评论侧以字段类型/返回类型筛选绑定方法并把失败单位留在分母，属同类策略对照，不构成 mine 覆盖证据。
证据：E010, E000

- F001 / revised：E013 支持核心事实：catalog 写死三个全限定名、mainHandlers 顺序 EXP3→NEXT→LEGACY、bindingMethods 在缺 .CommentItem 字段时返回 emptyList，catalog 内确实没有按父类/接口/类名模式回退的替代定位器；E001/E019 支持三族计数与指纹双侧变化。但草稿两处推断需校正：(1)“三者同时变化说明至少一个 handler 结构改动”超出证据，指纹整体变化同样可由改名或 DEX 重排造成，handler 类是否变化未被核对；(2)“静默 missing”不准确，E021 显示安装器在 points 缺失时仍走 compose 桥与 installKotlinChannel 并以 missing 记账，缺口是被记入分母而非静默成功。因此保留该发现、下调表述强度并保留 needs_runtime。（E013, E001, E019, E021）
- F002 / revised：E011 支持 comment_compose 目标侧 2512 类/288 compose 方法/1125 边且抽样中含空方法体空壳类，E001/E019 支持基线 2528/288/1115，因此“类减 16、边增 10、compose 方法不变”的矛盾事实成立，不能判定新样式。但草稿把 CommentComposeViewAccess 当作可能失效的宿主依赖点，与 E022 不符：该访问器通过 androidx.compose.ui.platform.AndroidCompositionLocals_androidKt#getLocalView 与 Composer.consume 解析，属 Compose 运行时 ABI，与宿主混淆名无关；失效风险应重定向到注入的 Composable 点位与 VersionAdapter 点位解析。保留发现为 candidate 并修订分析。（E011, E001, E019, E022）
- F003 / revised：E012/E002/E020 支持 dynamic_opus 类 1349→1381、边 224→229、compose 方法 95 不变、两侧指纹不同，也支持两份已登记 MOSS 计数两侧完全一致以及 OpusMoss/KOpusMoss/FeedMoss 未登记。但草稿把“新增结构落在 Opus 详情 API 侧而非渲染侧”基于 5 个抽样类写成较强判断，并给出 needs_runtime；实际该判断只是抽样线索（续体名指向广告/快照拦截），且协议登记与消费者追查是静态可完成的任务，运行期验证并非当前唯一缺口，故降级为 candidate 并修订措辞与等级。（E012, E002, E020）
- F004 / revised：核心前提成立：E015 抽样含 HomeFrameViewModel$dispatchAction$1 且 this$0 类型为 Ltv/danmaku/bili/khome/vm/HomeFrameViewModel，与 E016 常量 VIEW_MODEL_CLASS 逐字一致；E016 可见注释确实要求 Companion serializer() 的 serialName 与 TAB_DATA_SERIAL 精确比对、按 dex 字段排序重建顺序并与构造器参数窗口逐类型一致，故“锚点可用≠解析成功”的推断有据（E003 的 199→192 类/46→50 边变化也只支持结构变动，不支持新样式判定）。但草稿把“default_selected 必须为 int”和“Resolution.Failed 整层不安装”当作 E016 已写明的事实，这两点在本次可见的有界摘录中未出现（摘录止于 SKIPPED_PACKAGES），应降为待补读/待真机验证项。故修订分析措辞，保留 needs_runtime 级别与运行时验证建议。（E003, E015, E016）
- F005 / revised：E017 可见部分支持短名池与歧义风险：ROOT_NAMES 为 DISCOVER 前缀 a–z 加 SearchDiscoverViewModel，NESTED_SUFFIXES 为 a–z 与 0–9，DISCOVER/STATE 为固定包前缀，注释还说明约 700 次类加载探测、未命中抛 ClassNotFoundException，且 Points.deliveryCandidateCount “仅用于区分宿主没有该结构与候选歧义”；E004 显示两族类数/边数确有反向变动；E018 可见样本支持 BaseSearchItem 等原生主干仍在。但草稿断言“以 singleOrNull 作为唯一性裁决”和“候选缺失使 delivery/state 为 null、安装器静默跳过”属 locate 实现体的细节，本次摘录止于 fun locate(loader: ，未读到，需降为推断；同时草稿把 search2.share.a 列为 E018 已确认样本，可见摘录只到 search2.result.o，share 未出现，应改为未抽样覆盖。故修订措辞，保留 needs_runtime。（E004, E017, E018）
- F006 / retained：断言与证据匹配且已恰当分级：E003 显示 home_legacy 785/184/88 → 781/192/88，Compose 方法数逐字相同，只支持“混淆改名/DEX 重排”的推断而非新样式；E014 抽样确认 ui.main2 下 StartupFragmentV2、HomeFragmentV2 仍被引用、AccountMineRequestResource 枚举仍在，排除整体移除；E016 注释给出 frameSwitch 在 legacy 与 khome 间二选一、宽屏档位与服务端/SP 开关可改变分支，草稿已明确该陈述为模块作者对宿主的理解、本单元未在目标 DEX 重读 frameSwitch 实现，未越权断言运行条件。级别 candidate 合适，验证方案（三种启动条件 + 安装/调用计数）可直接执行。（E003, E014, E016）
- F007 / revised：数值全部与 E005 一致（ugc 1975/522/25→1973/544/25；united 4669/4193/98→4675/4300/99；java_moss 32/35、kotlin_moss 76/34 两版相同），推断已给出反例，等级 candidate 合适；但标题与正文「类数反向变动」只对 ugc 成立，united 类数与边数同向上升（+6/+107，幅度悬殊），需精确化以避免把两族混为一类变化。另补充未登记 ViewMoss 变体消费者未核对的限定。（E000, E005, E013）
- F008 / revised：计数与 E006 一致（legacy 357→358 类、0→1 Compose、307→327 边；theseus 2255→2256 类、132→131 Compose、913→813 边；两个 pgc 协议两版不变），needs_runtime 等级合适；但正文「至少一条弹窗/活动展示链的静态锚点发生了移动」超出证据，仅能证明 UI 家族调用图有变化，落点未确认；0→1 Compose 还可能是识别口径变化，需在分析与反例中并列。（E000, E006）
- F009 / revised：计数与指纹断言与 E007 相符（player_java 954/3305→949/3298，player_kotlin 466/897→473/886，compose 37 不变，两侧 moss 18/2 与 34/3 一致），候选级判断与替代解释（混淆改名、DEX 重排、内联、锚点本就走未混淆名，见 E016 同类策略）成立，故保留。但两句需收紧：一是“任一类被移除或改名都会让安装期解析落空”属过度断言，只有消失/改名类恰为定位器锚点时才成立，且定位器可能使用未混淆锚点；二是 E013 的“失败单位留在分母”来自 CommentNativeBindingCatalog.kt 中的 CommentFamilyCoverage，属评论家族记账实现，只能作为同模块记账语义示例，不能当作播放页安装结果。此外 E007 仅提供汇总、无类样本，差集尚未取得，补丁已把起点与新证据缺口写明。（E007, E000, E013）
- F010 / revised：legacy 两侧 absent、kotlin 微调、java/kotlin moss 计数一致均有 E008 支撑，“absent 不等于功能消失、先判定归类再谈功能影响”的取向正确，needs_runtime 与未知状态吻合，故保留。需修正三处事实与措辞：页面只有两条登记路径，草稿写“三条路径”有误；协议面应表述为“定义数与实际调用边计数两版完全一致，提示未见增删”，不能写成“没有任何增删”，相同计数不排除方法内部替换或消费者变更；E013 的记账语义来自评论家族 catalog，只能类比。另外 20 条 danmaku_java_moss 调用边的消费者身份未取证，不能默认属弹幕业务，补丁中已明确列为缺口。（E008, E000, E013）
- F011 / revised：核心事实（2969→2961 类、1419→1553 边、45→45 Compose、指纹变化、两侧 static_invoke_observed）与 E009/E000 一致，结论 level=needs_runtime 与“不宣称适配通过”的方向正确，故不拒绝。但草稿两处需修正：(1) 标题把“调用点迁移使 STORY 安装器落空”写成优先方向，属未经验证的因果框架；(2) 正文“story 页 protocols 两侧为空，边增长没有协议侧解释”把“未登记协议消费者”误当作“不存在协议层解释”，属过度推断。修订为：空字典只说明未登记，StoryMoss/KStoryMoss 归属未知；同时补明 8 类消失与 134 边增长需先排除构建噪音/重排，E016 仅作首页定位器结构筛选的对照假设、不是 story 覆盖证据，story_kotlin absent 不等于无 Compose 实现。（E009, E000, E016）
- F012 / revised：计数与哈希事实（mine_account_model 132/0/43 两侧一致而指纹 91335afb…→63bdafd5…；mine_native 327→325 类、边 94/94、Compose 7/7）与 E010 完全一致，“指纹变化不等于新样式、不能反推样式切换”这一判别性结论成立，E013 的结构筛选描述与模块源码摘录相符且已声明为跨页对照。但草稿“静态即可确认指纹至少对混淆改名、DEX 顺序或常量池排列敏感”为过度归因：计数不变而方法体语义被修改同样会产生哈希变化，本轮未做逐类方法体对拍，来源应记为未确定，故修订措辞并收紧结论边界，level 维持 static_evidence（仅结构性观察成立、功能影响未知）。（E010, E000, E013）

### 尚未解决的证据缺口

- [1] 三个原生评论 handler 全限定名（CommentContentRichTextHandler / CommentNextContentRichTextHandler / CommentNextExperiment3ContentRichTextHandler）在 9180300 的存在性、.CommentItem 字段与绑定方法签名均未核对，无法判断哪一族失配（E013 只证明编写方式，不证明目标命中）。
[2] comment_compose 未做逐类方法体哈希差分，新增的 10 条外部调用边来源类与减去的 16 类性质（空壳/内联/迁移）未知。
[3] 评论侧共同协议缺口：unregistered_protocols 中的 ReplyMoss/KReplyMoss 未登记，comment_java_moss/comment_kotlin_moss 是否被跨家族消费者共用未知；Kotlin MOSS 130 定义/23 实际调用边不能代表覆盖。
- [4] comment 与 dynamic 全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，本轮未取得任何真机安装日志、Hook 命中或 CommentFamilyCoverage.describe() 输出，不得宣称适配通过。
[5] DynamicPurifyFeatureInstaller / DynamicPurifyPolicy / DynamicTabsFeatureInstaller / DynamicVideoTabPreference 源码本轮读取预算耗尽未读，其定位锚点、候选歧义处理与兜底均未知，不作推断。
[6] dynamic_opus 的 +32 类仅由 5 个抽样类（集中在 opusDetail/api，含 CompositeExternalInterceptor 广告拦截续体）提示，未做包级类分布与全量差分，不能确定落在 API 拦截侧还是渲染侧。
- [7] OpusMoss / KOpusMoss / mall-tab3 OpusMoss / FeedMoss / KFeedMoss 未登记进 dynamic 协议集，实际调用边与消费者类无法统计。
[8] dynamic_compose 新增 8 条外部调用边来源类未定位；服务端外观开关与平板/宽屏分支静态不可见，样式穷尽性未知。
[9] 两个页面均未获得服务端实验开关证据，comment_native_exp3 与 dynamic_opus 的样式运行条件未覆盖，若无法取得应显式记为未覆盖而非通过。
- [10] 源码快照为脏工作树（source_tree_sha256 37745f8f…，working_tree_dirty=true），E021 亦标记 dirty；结论只能按文件哈希绑定该快照，不能外推到其它提交。
[11] E016 为有界摘录：未读到 default_selected 类型门槛、Resolution.Failed 分支与“失败即整层不安装”的实际代码，需补读 HomeFrameTabLocator.kt 完整解析体（按 sha256 474ba2f5… 追溯）。
[12] E017 为有界摘录：未读到 locate/quickLocate 实现体内的唯一性裁决（如 singleOrNull）与 delivery 为 null 后的处理，需补读 SearchHomeRecommendLocator.kt 全文（sha256 1c569369…）。
- [13] frameSwitch（tv.danmaku.bili.common.home.c#b()）在 9180300 目标 DEX 中未重读，dd.use_new_home_frame 与 sp_key_new_home_frame_test 的默认值与读取顺序仍未知。
[14] E018 抽样未覆盖 com.bilibili.search2.discover.*、com.bilibili.search2.main.data.* 与 search2.share.*，草稿中 search2.share.a 的存在性在可见摘录内未被证实。
[15] search_compose 家族在目标上的内部结构未单独重读（预算耗尽），562 个 Compose 方法内容是否被替换未核实。
- [16] 四条路径 runtime_enabled=unknown、module_coverage=requires_installer_review：尚无安装日志证明 HomeFrameTabLocator、HomeFrameListHook、SearchPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller 在 9180300 上实际命中。
[17] home_legacy 4 类减少与 search_native 68 条边减少未逐条比对来源，内联/迁移与删除未区分。
[18] complete_coverage=false：unregistered_protocols 中 SearchMoss/KSearchMoss/HomeMoss 等变体的跨家族消费者未归类，搜索与首页共同协议是否另有消费者未知。
- [19] 服务端 A/B 与外观实验无结构变化时静态不可见；平板/宽屏档位分支、服务端开关组合下的真实样式穷尽性未知。
[20] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，HEAD 5422fad1…），本单元结论仅能按文件哈希追溯，未提交修改的影响未评估。
[21] E014 抽样中 StartupFragmentV2、HomeFragmentV2 仅以字段/构造器类型出现，未作为类样本被直接读取，legacy 主干的方法级可用性未核实。
- [22] 未读取 DetailModulePurifyPolicy / DetailUnitedModulePurifyPolicy / DetailUnitedPresentationPurifyPolicy / DetailViewPurifyPolicy 及其安装器，ugc/united 的家族命中条件、候选歧义处理与失败兜底仍为未知。
[23] 未读取 PgcAutoActivityPopupLocator 与 PgcAutoActivityPopupPolicy/Installer，pgc 活动弹窗定位锚点、兜底分支及是否依赖 -100 边中的调用点未知。
[24] 未做 detail_theseus_ugc/united 与 pgc_legacy/theseus 两版按 owner+callee 描述符的边集对齐，新增/消失边中 lambda/bridge/内联产物与真实新调用点尚未区分。
- [25] detail_theseus_united 新增的 1 个 Compose 方法与 pgc_legacy 新增 Compose 方法的 owner/调用方未用 JADX 定位，是否落在净化或弹窗展示路径未确认。
[26] detail_legacy 的 absent 未取得安装器 skipped 原因，是否存在其它家族承接旧入口的兜底路径未登记。
[27] 未核对未登记的 ViewMoss/LegacyViewMoss（detail）与 pgc gateway view v1 KViewMoss（pgc）消费者，跨家族共用协议与 complete_coverage=false 的缺口未补齐。
- [28] 无任何真机 Hook 命中日志：家族解析结果、策略命中数、未注册方法数均未采集，全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review。
[29] 平板/宽屏（large/medium）档位与服务端实验/活动开关造成的分支静态不可见，未做真机对照，不能宣称样式已穷尽。
[30] 未核对 DEX 重排/混淆映射变动，指纹变化来源（重排 vs 真实代码迁移）未区分。
- [31] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），detail/pgc 相关策略文件未按文件哈希逐一追溯未提交修改对结论的影响。
[32] 未对 APK 资源变更（changed=1）做内容核对，无法排除其对详情/PGC 页布局或文案的影响。
[33] player_java 与 player_kotlin 的类清单差集未取得：E007 仅下发汇总摘要（classes/compose_methods/edges/fingerprint），无类样本；消失的 5 类与新增的 7 类身份仍未知，需按名重读两侧类清单。
- [34] 播放页模块定位器（PlayerBufferLocator、PlayerSpeedLocator、PlayerSpeedSessionLocator、SponsorPlayerLocator、PlayerCapabilityAccess、SponsorPlayerBindings 等）本轮未读取，无法判断其锚点是否依赖混淆类名/字段，也无法判断是否存在失败兜底；Hook 覆盖范围不得推测。
[35] DanmakuPurifyFeatureInstaller/DanmakuPurifyPolicy 本轮未读取，legacy absent 是否导致净化定位落空、是否存在跨家族匹配或兜底，均无证据。
[36] danmaku_java_moss 20 条实际调用边的消费者类与业务归属未识别，无法确认其是否属弹幕业务。
- [37] danmaku_legacy 与基线同为 absent，未确认目标侧是否存在以其他类名承载的旧弹幕净化/发送回调实现（需按类名直接检索），也未核对 unregistered_protocols 中 live DanmuMoss 等未登记项与本页路径的关系。
[38] player_java 减少的 7 条外部调用边与 player_kotlin 减少的 11 条边未按 owner+callee 描述符比对，无法区分内联/合并与真实删除。
[39] 两条路径（四条家族）runtime_enabled=unknown、module_coverage=requires_installer_review，缺真机安装结果与 Hook 命中日志，适配状态仍未验证。
- [40] 服务端开关/A-B 与平板宽屏分支在播放页、弹幕页是否有结构不可见的实现切换未取证；static 侧不可见不等于无分支。
[41] resource_change_counts 显示 changed=1，本轮未核对变更资源是否影响播放页或弹幕页布局/文案。
[42] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），草稿与复核引用的模块文件均需按各自 sha256 追溯，未提交修改对结论的影响未评估。
- [43] 两侧 APK 的混淆映射与 DEX 重排情况未单独核对，指纹变化的来源（重排/改名/真实迁移）尚未定论。
[44] player_java_moss 2 条、player_kotlin_moss 3 条、danmaku_kotlin_moss 12 条实际调用边的具体消费者与调用点未枚举，协议面“一致”只建立在计数层面。
[45] story_native 缺失的 8 个类与新增 134 条外部调用边的目标描述符未取得：需两版本按 method_bodies_sha256 做类集合差集后才能区分 DEX 重排/构建噪音与真实调用点迁移。
- [46] story_native 内 45 个 Compose 方法（compose_signatures）归属未核，因此 story_kotlin 的 absent 只能记为未检出，不能断言 STORY 页无 Kotlin/Compose 实现。
[47] story 侧 6 个模块文件（HomeVerticalDetailFeatureInstaller/Routing、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess）正文未读，Hook 选择器是混淆类名、方法签名还是结构过滤，以及失败是否有兜底，均未知。
[48] StoryMoss / KStoryMoss 未登记协议的消费者归属未知：是否存在跨家族共用、是否被 story 相关 Hook 消费未验证。
- [49] mine_native 消失的 2 个类身份未定位，是否为合成/包装类或组件过滤/VIP/阅读卡依赖的持有类未确认。
[50] mine_account_model 计数一致而指纹变化的来源未区分（混淆改名/DEX 重排/常量池 vs 方法体语义修改），需逐类方法体哈希与字段集合对拍。
[51] MineComponentSnapshotStore / QueryContract / QueryClient / HostBridge 与 MineComponentFilterFeatureInstaller 正文未读，快照键与过滤器是否写入混淆类名、命中失败是否有兜底未知。
- [52] MineMoss / KMineMoss 未登记协议的跨家族消费者归属与兜底策略未登记。
[53] story 与 mine 四条路径 runtime_enabled 均为 unknown、module_coverage 均为 requires_installer_review：未取得真机安装成功/失败日志与功能验证，报告不得升级为适配通过。
[54] source_snapshot 为 working_tree_dirty=true（source_tree_sha256 37745f8f…），相关模块文件的未提交修改对结论的影响需按文件哈希逐一追溯。
- [55] 服务端开关/AB 在 story 与 mine 页是否存在无结构变化的样式分支静态不可见，样式穷尽性仍未知。

## 下一步

- [1] 在 9180300 真机 dump CommentFamilyCoverage.describe()，逐家族记录 ok/partial/missing，作为 native/compose/legacy 三侧安装结果的一手证据。
[2] 校核 CommentNativeBindingCatalog 三个全限定名在目标包是否仍存在、是否仍声明类型名以 .CommentItem 结尾的字段，并对缺失家族补结构化兜底定位。
[3] 对 comment_compose 做逐类方法体哈希差分，抽取新增 10 条外部调用边的来源类，判断是否为真实 Compose UI 调用链迁移。
[4] 对 comment_native_legacy/native_next/native_exp3 分别比对两侧绑定方法签名集合（参数个数、View 子类参数、void 返回）差异。
[5] 在视频详情评论区分别覆盖原生旧样式、原生新样式、实验三样式与 Compose 样式，验证复制/净化/回复按钮四项功能并记录缺失项。
- [6] 把 OpusMoss、KOpusMoss、mall/tab3 的 OpusMoss、FeedMoss/KFeedMoss 登记进 dynamic 路径协议集后重算实际调用边。
[7] 静态确认 kntr/app/following/opusDetail 新增类（含 CompositeExternalInterceptor 系列）是否实现或调用 Opus 协议 stub，以及是否被 DynamicPurifyPolicy 消费。
[8] 在平板/宽屏与手机两种布局下分别进入动态 Tab 与 Opus 详情，记录 DynamicTabsFeatureInstaller/DynamicVideoTabPreference 是否生效。
[9] 对 dynamic_compose 新增 8 条外部调用边定位来源类，判断 Compose 动态流是否绕过 DynamicPurifyFeatureInstaller 注入点。
[10] 记录服务端外观/实验开关是否可获得；不可获得时把 exp3 与 Opus 样式的运行条件明确记为未覆盖，而非通过。
- [11] 所有结论区分事实、推断与待真机验证三级，最终判定仍以 installer 命中日志和真机功能验证为准，不以指纹或计数变化替代。
[12] 真机分三种启动条件（手机档位+双开关关、宽屏/平板档位、仅服务端开关）确认 9180300 实际走 legacy 还是 khome，并记录 MainActivityV2 分支日志。
[13] 抓取 HomeFrameTabLocator.resolve 的 Resolution 与 Failed reason，核对 HomeTabData/HomeTabItemData serialName、字段顺序与 default_selected 在目标上是否成立。
[14] 枚举并核对 9180300 中 com.bilibili.search2.discover.*、com.bilibili.search2.main.data.*、MainSearchViewModel 的类清单与方法签名，判定 SearchHomeRecommendLocator 是候选歧义还是宿主无结构。
[15] 复核对 search_compose 家族的深挖重读（本单元因预算耗尽缺失），确认 562 个 compose 方法未发生内部替换。
- [16] 对 home_legacy 的 4 类减少与 search_native 的 68 条边减少做逐条来源比对，排除内联/迁移而非删除造成的差异。
[17] 用 unregistered_protocols 中的 SearchMoss/KSearchMoss/HomeMoss 变体核查搜索与首页是否存在跨家族的共同协议消费者，补齐 complete_coverage=false 的缺口。
[18] 按文件哈希（source_tree_sha256 37745f8f…，working_tree_dirty=true）追溯 HomeFrameTabLocator/SearchHomeRecommendLocator 未提交修改对结论的影响，不清洗工作树。
[19] 安装器侧核对 module_coverage=requires_installer_review 的四条路径在目标上是否实际完成安装，并保留失败单位在分母中，不以类存在升级为覆盖。
[20] 对 9180200 与 9180300 两版按 owner+callee 描述符导出 detail_theseus_ugc/united 与 pgc_legacy/theseus 的边集差异清单，标注新增/消失边的 owner 与是否 lambda/bridge。
- [21] 用 JADX 读 detail_theseus_united 新增的那 1 个 Compose 方法及其调用方，确认是否为新展示单元或仅内联产物。
[22] 用 JADX 定位 pgc_legacy 新增 Compose 方法的 owner，检查其调用链是否经过活动弹窗/浮层展示路径。
[23] 读取 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupPolicy/Installer，记录解析锚点、候选歧义处理与失败兜底，判断 -100 边是否影响定位。
[24] 读取 DetailModulePurifyPolicy、DetailUnitedModulePurifyPolicy、DetailUnitedPresentationPurifyPolicy，核对新增类/Compose 方法是否落入匹配条件之外。
[25] 真机 A：普通视频详情（UGC）与 united 详情各一次，采集安装日志中的家族解析结果、策略命中数与未注册方法数量。
- [26] 真机 B：PGC 旧详情/播放页触发活动弹窗，记录定位器成功与失败分支，并在服务端活动开关开/关下各测一次。
[27] 真机 C：平板/宽屏（large/medium 档位）与手机布局下复测 detail 与 pgc，确认是否存在静态不可见的服务端/尺寸分支。
[28] 核对安装日志是否把安装失败单位保留在分母（参照同 feature 层覆盖记账实现），禁止以类存在或静态边存在推导覆盖率。
[29] 检查两版 APK 的 DEX 重排/混淆映射变动，区分指纹变化来源是重排还是真实代码迁移。
[30] 对 absent 的 detail_legacy 记录安装器 skipped 原因，确认是否存在其它家族承接旧入口的兜底。
- [31] 汇总以上结果前明确标注：未取得真机 Hook 命中日志前，所有路径结论保持 static_invoke_observed / 未知，不得写为已适配。
[32] 用 family_evidence(player_java, target/baseline) 取类名差集，列出目标侧消失的 5 个类
[33] 用 family_evidence(player_kotlin, target/baseline) 取类名差集，对新出现的 7 个类抽样 decompile_class 读签名
[34] 用 module_source 读 PlayerBufferLocator.kt / PlayerSpeedLocator.kt / SponsorPlayerLocator.kt，把锚点与差集逐条对照
[35] 用 module_source 读 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt，确认家族锚点与兜底分支
- [36] 用 family_evidence(danmaku_kotlin, target/baseline) 取差集并对差异类 decompile_class
[37] 追查 danmaku_java_moss 20 条实际调用边的消费者类，判断是否属弹幕业务
[38] 核对未归类协议消费者清单中是否存在弹幕相关 MOSS（如 live DanmuMoss）并标注为未归类候选
[39] 真机安装模块后抓播放页安装结果日志，分别验证缓冲/倍速/赞助屏蔽是否被 Hook 触发
[40] 真机在视频页开关弹幕净化，记录安装结果、命中家族与异常堆栈
- [41] 对 9180300 与 9180200 做资源变更（changed=1）核对，确认是否影响播放/弹幕页布局或文案
[42] 以 source_tree_sha256 37745f8f… 记录源码快照脏树状态，对引用的模块文件逐一按 sha256 追溯
[43] 补证平板/宽屏档位与服务端开关是否改变播放器或弹幕页实现分支（当前静态不可见）
[44] 对 story_native 两版本类集合按 method_bodies_sha256 做差集，输出消失的 8 类与新增外部调用边目标描述符清单
[45] 对 story_native 新增调用边目标用 decompile_class 反编译，确认是否进入 STORY 卡片/动作条渲染路径
- [46] 用 module_source 读取 HomeVerticalDetailFeatureInstaller/Routing、StoryActionIconsFeatureInstaller/Policy、StoryPurifyFeatureInstaller、PlayerStoryFreeDataPromotionAccess，记录 Hook 选择器形态
[47] 读取 story_native 的 compose_signatures 明细，确认 45 个 Compose 方法是否属于 STORY 容器，解释 story_kotlin 的 absent
[48] 对 mine_native 差集定位消失的 2 类，确认父类与引用方是否为包装/合成类或组件过滤依赖类
[49] 对 mine_account_model 逐类比对方法体哈希与字段名集合，判定是否仅为重排/改名
[50] 用 module_source 读取 MineComponentSnapshotStore、MineComponentSnapshotQueryContract、MineComponentFilterFeatureInstaller，确认快照键与过滤器是否依赖混淆类名及是否有兜底
- [51] 真机复测：STORY 页动作图标/净化/竖屏详情，我的页组件过滤/VIP 卡片/阅读卡，采集安装成功与失败日志
[52] 补证 StoryMoss/KStoryMoss 与 MineMoss/KMineMoss 的消费者归属，明确是否跨家族共用及未注册协议的处理方式
[53] 若真机条件不足，将四条路径的 runtime_enabled 与 module_coverage 保持 unknown/requires_installer_review，不做适配通过结论