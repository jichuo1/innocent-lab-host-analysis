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

本单元只审计 comment（5 条登记路径）与 dynamic（3 条）在 9.17.0（f0f880e8…）相对 9.16.1（41efb1c9…）的静态变化。结论：两条页面 8 个家族全部仍是 static_invoke_observed，运行时启用与模块安装器覆盖均为 unknown，因此不能宣称适配通过。可核实的变化是：comment_compose 外部调用边 934→1101、compose 方法 278→283，而类数 2444→2428；comment_native_exp3 类/边同步下降（58→54、62→52）；comment_native_next 边 50→67 上升；dynamic_legacy 边 2151→2075 下降、dynamic_opus 边 186→226 上升、dynamic_compose 127→141。两条页面的 MOSS 协议定义数未变（comment 50/130、dynamic 134/382），但实际调用边出现小幅摆动（comment kotlin 26→23，dynamic kotlin 26→26）。深挖 GetCommentCompose 家族样本（E011）显示该类簇落在 Lkntr/common/comment/… 包，而模块目录 CommentNativeBindingCatalog（E012）硬编码的是 com.bilibili.app.comment3.* 三个处理器类名，二者关系未在静态证据中闭合，是当前最需要真机/定位器确认的缺口。所有指纹变化均可能是混淆改名或 DEX 重排，不视为新样式。

本单元仅覆盖 home 与 search 两页、四个登记路径（home_legacy、home_new_frame、search_native、search_compose）。四路径的静态证据值均为 static_invoke_observed，runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review，因此本报告不宣称任何路径“已适配”。目标 9.17.0 相对基线 9.16.1：home_new_frame 类数与 compose 方法数完全不变（196/33），仅外部调用边 52 对 49；深挖样本显示差异集中在参数顺序与混淆包名（Lap1/b→Vt1/b），更像混淆改名而非新样式；home_legacy 类数 767→766、边 204→198，search_native 类数 1705 对 1702、边 2818 对 2859，search_compose 类数 3146 对 3141、compose 方法 562 对 561、边 614 对 595；search 的 Java/Kotlin MOSS 定义数与调用边（24/22、52/18）两侧一致，说明协议面未扩张，变化位于消费者/调用路径侧。源码快照为未提交工作树（working_tree_dirty=true，source_tree_sha256=37745f8f…），本轮未能读取模块源码验证定位器/安装器逻辑，属于明确缺口。所有结论区分事实（计数与哈希差异）、推断（混淆改名、调用路径迁移）与待真机验证（样式是否并存、Hook 是否命中）。

本单元仅覆盖 detail 与 pgc 两页（9.17.0 对 9.16.1，同签名包 tv.danmaku.bili）。静态矩阵显示：detail 三条登记路径中 detail_legacy 两侧均为 absent（指纹为空集哈希 4f53cda1…），detail_theseus_ugc 与 detail_theseus_united 为 static_invoke_observed；pgc 两条路径（legacy/theseus）均为 static_invoke_observed。四条家族指纹均变化：ugc 类 1946→1975、边 510→547；united 类 4581→4633、边 4257→4199（下降 58）、compose 99→98；pgc_legacy 类 354→352、边 399→425；pgc_theseus 类 2265→2276、compose 131→134、边 782→1179。detail_kotlin_moss 调用边 10→38 明显增长，detail_java_moss（32/35）与 pgc_player_moss（12/3）、pgc_view_moss（14/7）两侧完全一致。所有路径 runtime_enabled 均为 unknown，无 complete_coverage，模块源码快照为 published_unverified_worktree 且工作树 dirty。故本报告只给出静态事实与待验证推断，不构成适配通过结论。证据：E000、E005、E006、E011、E012。

本单元仅覆盖 player 与 danmaku 两个登记页面。9.17.0 相对 9.16.1，player_java、player_kotlin、danmaku_kotlin 三家族的类数、外调边与结构指纹均变化，danmaku_legacy 两侧均为 absent（classes=0、指纹为空集常量）。两侧 MOSS 协议定义数完全一致（播放 18/34、弹幕 22/46），提示协议面稳定而类落点变化，故结构哈希变化不足以确认为新样式。所有路径 runtime_enabled 均为 unknown、module_coverage 为 requires_installer_review，complete_coverage=false；静态调用存在不证明真机启用或 Hook 生效。源码快照 working_tree_dirty=true，模块侧改动需按文件哈希追溯，不得据清单推断 Hook 覆盖。

本单元仅覆盖 story、mine 两页共四条登记路径，全部为预取摘要与有限深挖证据，未做安装器或真机验证，因此不得视为适配通过。story_native 与 mine_native、mine_account_model 三路径在 9.17.0 侧仍为 static_invoke_observed，story_kotlin 双侧为 absent（0 类、空指纹）。两页的已注册协议集合均为空，KStoryMoss/StoryMoss/DynamicMoss、KMineMoss/MineMoss、AccountInterfaceV1Moss 等只出现在全局未注册协议名单，属于未归类候选，不能当作对应页的已确认消费者。seed 的三条 structure_or_call_path_changed 只给出计数与指纹差别，未给出新增类名与新增调用边端点；深挖对照 E013/E014 显示类数与 compose 方法完全一致的家族指纹同样会变，说明当前变化不能直接认定为新样式。模块源码快照为 published_unverified_worktree（working_tree_dirty=true），且 story/mine 相关安装器与策略文件本轮未读取，Hook 覆盖与兜底一律记为未知。

## 各页面评估

### comment

评论区登记 5 条并存栈：comment_legacy_v2、comment_native_legacy、comment_native_next、comment_native_exp3、comment_compose，全部 evidence=static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review（E001）。相对基线：compose 家族类数 2444→2428、compose 方法 278→283、外部调用边 934→1101（+17.9%），是唯一“类少而边多”的方向；legacy_v2 579→583 / 边 741、native_legacy 172→181 / 边 220、native_next 45→48 / 边 50→67 均小幅上行；native_exp3 58→54 且边 62→52，是唯一双降家族。协议侧 comment_java_moss 定义 50、边 50 完全不变；comment_kotlin_moss 定义 130 不变、实际边 26→23 下降，说明协议面没有新增，但调用点集合发生重排。深挖 E011 取到 comment_compose 的 5 个样本（kntr/common/comment/common/service/f、g，richtext/g$a、i、IconText），均无 compose_signatures、方法体极短，未直接体现样式 UI；同时模块 CommentNativeBindingCatalog（E012）会把 LEGACY/NEXT/EXP3 三个 com.bilibili.app.comment3.* 处理器按“含 CommentItem 字段 + 绑定型参数”规则解析，并声明三者可在同一 APK 共存。样本包名与该目录类名不一致，可能是混淆/包迁移，也可能说明该家族桶实际混入了非 UI 协议层类，需运行时确认真实渲染路径。complete_coverage=false，未知不得补白。

证据：E001, E011, E012

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 579→583、外部调用边 735→741、compose 方法 0→0；指纹由 8d381d51… 变为 b8b8915c…。
- 可能影响：旧版 v2 评论路径的静态调用面小幅扩张；模块对该路径的安装器注册是否仍命中未知。
- 验证：真机截图 + 类名/指纹对照，用 module_source 复核 VersionAdapter 中 legacy_v2 的入口类名是否随版本改动；并用 JADX 读 583 类中新增 4 类的字段/调用者。
- 证据：E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 172→181、边 211→220。
- 可能影响：原生 legacy 持有器数量增加，绑定型方法解析范围（CommentNativeBindingCatalog 的 1..5 参数规则）可能命中更多方法。
- 验证：对 com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler 做反射级真机探针，打印 bindingMethods 实际命中数并与 220 条边对照。
- 证据：E001, E012

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 45→48，边 50→67（+34%），为 comment 侧边增幅最大路径。
- 可能影响：Next 样式可能新增绑定/回调入口；若模块仅按旧方法签名 Hook，可能出现部分条目未生效。
- 验证：用 decompile_class 读取 CommentNextContentRichTextHandler 的方法签名，与基线同文件比对新增方法；真机切换 Next 实验位后逐条核对富文本渲染。
- 证据：E001, E012

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 58→54、边 62→52，是唯一类与边双降的评论家族。
- 可能影响：exp3 实验位可能被裁剪或调用点合并；但也可能是 DEX 重排导致统计口径收缩，不能推断样式下线。
- 验证：检查 exp3 处理器类是否仍存在于 APK（decompile_class 按名查 CommentNextExperiment3ContentRichTextHandler），并在真机开启 exp3 开关验证渲染分支是否可达。
- 证据：E001, E012

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2444→2428、compose 方法 278→283、外部边 934→1101（+17.9%）；E011 抽样的 5 个类均落在 Lkntr/common/comment/… 且无 compose_signatures。
- 可能影响：Compose 评论路径的跨家族消费者增多，而模块 CommentCompose* 系列 Bridge 依赖的类名/方法名在抽样中未直接出现，存在定位器失配风险。
- 验证：在真机上对 CommentComposePurifyBridge/CommentComposeViewAccess 打印解析结果（命中/未命中类名），并抽查 E011 中 kntr/common/comment/common/service/g 的 Flow 消费者是否即列表数据源。
- 证据：E001, E011, E012

### dynamic

动态页登记 3 条路径：dynamic_legacy、dynamic_compose、dynamic_opus，均 evidence=static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review（E002）。相对基线：dynamic_legacy 类 3251→3255、compose 方法 105→103、外部边 2151→2075（-3.5%），类基本持平而边下降，符合调用点合并或内联而非功能裁剪的特征；dynamic_compose 类 1136→1187、compose 方法 127→141、边 221→234，是唯一“类与 compose 方法同增”路径，方向指向 Compose 侧继续扩张；dynamic_opus 类 1352→1350 基本持平、compose 方法 92→94、边 186→226（+21.5%），边增幅最大但类数未增，说明既有 Opus 组件之间的连线被加密或新增消费者，而不是新增样式家族。协议侧 dynamic_java_moss 定义 134、边 134 完全不变；dynamic_kotlin_moss 定义 382、边 26→26，均无变化，因此看不到协议层新增的动态样式协议。需要注意 seed 的 unregistered_protocols 中仍能看到 DynamicMoss、KOpusMoss/OpusMoss、KTribeeMoss、CampusMoss 等未登记协议，说明动态页协议面存在未纳入登记集合的部分，本单元不对其做覆盖推断。complete_coverage=false，三条路径的运行时启用、服务端 A/B 分桶、平板/宽屏分支均未知，需真机按 tab 分别取证。

证据：E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3251→3255、compose 方法 105→103、外部边 2151→2075；指纹 a02ef6a4…→494b6f4a…。
- 可能影响：旧版动态列表（含 103 个 compose 方法，说明该桶本身混合 Compose 组件）边数下降，模块 DynamicPurifyPolicy/Installer 依赖的具体调用点可能被内联合并而未变类名。
- 验证：按名比对 DynamicPurifyFeatureInstaller 中登记的过滤/净化方法是否仍存在于 3255 类集合；真机在关注/推荐 tab 各取一次渲染日志确认净化命中。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 1136→1187、compose 方法 127→141、边 221→234。
- 可能影响：Compose 动态组件数量与 compose 方法同步增长，可能新增可组合单元或包装层；模块若按旧方法签名 Hook 可能出现未覆盖的新组合层。
- 验证：抽样比对新增 51 个类的 compose_signatures 与父类，判断是重复包装层还是新组件；真机对比 9.16.1 与 9.17.0 的动态卡片层级树。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1352→1350、compose 方法 92→94、边 186→226（+21.5%）。
- 可能影响：Opus 图文卡片的调用连线显著加密，可能与图文/评论联动或转发入口新增有关；现有 Opus Hook 点的边来源变化未知。
- 验证：用 family_evidence 取 dynamic_opus 类样本核对新增边的消费者类型，并在真机 Opus 详情页验证正文/评论区衔接是否被净化逻辑影响。
- 证据：E002

### home

home 两个已登记家族在 9.17.0 与 9.16.1 之间均标记为结构或调用路径变化。事实层面：home_legacy 类数 767→766、compose 方法 87 不变、外部调用边 204→198、指纹 7a842bbb…→a56da1e1…；home_new_frame 类数 196 不变、compose 方法 33 不变、外部调用边 49→52、指纹 4a3e9002…→34c59fa3…。用 family_evidence 按名重读 home_new_frame 两侧样本后可见：bubble/d、bubble/e、bubble/f 三个类的方法体哈希两侧完全相同，bubble/s 的方法集合一致但形参顺序互换（基线 a(u) / b(u;Function0)，目标 a(u;Function0) / b(u)），HomeFrameViewModel$dispatchAction$1 仅字段类型由 Lap1/b 变为 Vt1/b。这构成“指纹变化可由混淆改名与签名重排解释”的反例证据，不能据指纹变化断言出现新样式。home_legacy 仅拿到有界摘录（两侧各两个类样本未在深挖中重读），其 6 条调用边减少的具体归属未知，也无法区分为迁移出该家族还是新增条件分支。模块侧：HomeFrameTabLocator、HomeFrameListHook、HomeBannerFeatureInstaller、HomeTopBarFeatureInstaller、HomeRecommendPurifyFeatureInstaller 等源码未在本轮成功读取（只读工具额度耗尽），因此定位器与兜底策略对新形态的覆盖只能记为未知，不能推测 Hook 覆盖。运行时开关、平板/宽屏分支、服务端样式选择均未读到运行条件，一律记为未知。

证据：E000, E003, E013, E014

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类数 767→766、外部调用边 204→198、指纹 7a842bbb…→a56da1e1…，compose 方法数 87 未变；具体增减类与边归属未定位。
- 可能影响：若边减少源于组件过滤/横幅植入所依赖的调用点被合并或迁移，HomeComponentFilter、HomeBanner、HomeTopBar 等植入点可能不再命中；但同样可能是 DEX 重排或条件分支合并，当前不能判定功能受损。
- 验证：以相同 family 名在两侧按名抽取调用边清单，逐一比对 inode 级差异；随后在真机 9.17.0 上开日志确认 HomeFrameTabLocator 的定位结果与组件过滤植入次数，并核对 home_legacy 页面是否仍被实际加载。
- 证据：E003

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 196、compose 方法 33 均未变，外部调用边 49→52；样本中 bubble/d、bubble/e、bubble/f 方法体哈希两侧相同，bubble/s 仅参数顺序互换，dispatchAction$1 仅混淆字段类型改名 Lap1/b→Vt1/b。
- 可能影响：当前证据更支持混淆改名/签名重排导致的指纹漂移，对 Bubble、HomeFrameViewModel 动作分发类 Hook 的实际影响尚不能确认；新增 3 条外部调用边的归属未定位，若落在动作分发或 Bubble 控制路径，可能影响 HomeFrameListHook 的挂载稳定性。
- 验证：对 home_new_frame 两侧全量类清单做方法体哈希配对（而非仅指纹），列出未配对类；对 3 条新增边做调用方定位；真机验证 HomeFrameViewModel.dispatchAction 与 bubble 控制器是否仍被安装器选中。
- 证据：E013, E014

### search

search 两个已登记路径均在种子中标为结构或调用路径变化，静态证据值为 static_invoke_observed，运行时未知、模块覆盖需安装器复核。事实层面：search_native 类数 1702→1705、compose 方法 2 不变、外部调用边 2859→2818（减少 41）；search_compose 类数 3141→3146、compose 方法 561→562、外部调用边 595→614（增加 19）。两个已登记协议 search_java_moss（定义 24、实际调用边 22）与 search_kotlin_moss（定义 52、实际调用边 18）在两侧完全一致，说明协议定义与已解析调用边未扩张，变化位于 UI/消费者调用路径一侧，而不是新增协议面。注意：定义数与调用边数单位不同，不能相除得出覆盖率；22 与 18 只是“实际调用边”，不代表其余定义无消费者，也不代表跨家族消费已穷尽。search_native 的调用边减少与 search_compose 的调用边增加并存，构成“调用方从原生迁往 Compose”的一种候选解释，但同样可能由 DEX 重排、条件分支合并或服务端开关隐藏分支造成，静态不可辨。本轮未能读取 SearchHomeRecommendLocator、SearchHomeRecommendFeatureInstaller、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 与 KotlinMossChannel/ReplyBridge 的源码（只读工具额度耗尽），因此首页推荐清理、默认词清理与 MOSS 通道的解析点、兜底与跨家族消费者均记为未知，不做 Hook 覆盖推断。

证据：E000, E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数 1702→1705、外部调用边 2859→2818（净减 41）、compose 方法数仍为 2；协议定义与调用边（24/22、52/18）未变。
- 可能影响：若减少的边属于搜索首页推荐或默认词清理所依赖的消费者，原生路径上的清理植入点可能减少或迁移到 Compose 侧；也可能只是分支合并，属于候选而非结论。
- 验证：抽取 search_native 两侧外部调用边清单并按目标方法配对，列出未配对边；在真机 9.17.0 上分别以原生与 Compose 样式进入搜索页，记录 SearchHomeRecommendLocator 定位成功次数、默认词清理触发次数与 MOSS 调用边实际命中情况。
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数 3141→3146、compose 方法 561→562、外部调用边 595→614（净增 19），指纹 fcde68da…→4e4c7892…；协议侧两族不变。
- 可能影响：边增加与原生侧减少方向相反，可能表示推荐/清理逻辑的 Compose 消费者增多，若模块只覆盖旧原生消费者，Compose 样式下可能出现清理失效或部分生效；但 Compose 方法数仅 +1，也提示变化可能是重排而非新增实现。
- 验证：比对 search_compose 两侧 compose 方法签名集合找出新增的那一个方法及其调用者；结合真机在 Compose 样式下验证 SearchHomeRecommendPolicy 与 SearchPurifyFeatureInstaller 的命中日志；确认是否存在服务端开关切换两套样式。
- 证据：E004

### detail

详情页登记三条路径：detail_legacy 在目标与基线均为 absent（classes=0、指纹为 4f53cda1… 空集哈希），这只说明该家族采集口径在两侧都没有命中类，不等于旧原生详情样式已消失；DetailViewPurifyFeatureInstaller/Policy 一类旧样式 Hook 因此没有可复核的静态落点，属未覆盖未知（E005）。detail_theseus_ugc 与 detail_theseus_united 均为 static_invoke_observed，均有实际外部调用边（547 / 4199），但边数与类数两侧不同：ugc 类 +29、边 +37、compose 方法不变（25）；united 类 +52、compose 方法 99→98、边反而减少 58。这两种方向相反的变化提示结构变化可能来自混淆改名、DEX 重排或内联/迁移，而非样式新增，不能据指纹判定为新样式（E005）。评论区侧，comment_compose 家族在目标 APK 静态存在 2428 类 / 283 compose 方法 / 1101 外部调用边（E011），说明 Compose 评论实现仍在；但模块侧的锚点是硬编码三个 handler 类名（LEGACY/NEXT/EXP3），且只在安装时解析、失败时静默返回空列表（E012），预取摘录未提供该三类的存在性证据。协议面 detail_java_moss 定义 32、调用边 35，两侧不变；detail_kotlin_moss 定义 76 不变但调用边 10→38，Kotlin MOSS 消费者扩大，KotlinMossChannel/KotlinMossReplyBridge 是否覆盖新增调用方未核实。整体：静态可见路径存在，安装器与运行时启用均为未验证。证据：E005、E011、E012、E000。

证据：E000, E005, E011, E012

#### 路径：detail_legacy

- 状态：absent
- 变化：两侧 classes=0、compose_methods=0、external_invoke_edges=0，指纹同为 4f53cda1…（空集哈希），无结构变化，变化=无；absent 不代表旧原生详情页功能消失。
- 可能影响：针对旧原生详情样式的净化/推广位 Hook 在静态层没有可解析的类与方法落点，若真机仍存在旧样式入口，则模块覆盖情况完全未知。
- 验证：真机打开普通稿件详情页并用 decompile_class/JADX 检索当前详情容器类名，与 DetailViewPurifyPolicy、DetailModulePurifyPolicy 中登记的类名/方法签名逐条比对；同时复核 verdict 口径是否把该家族归入了 theseus 家族，确认 4f53cda1… 是采集空集还是家族判定缺失。
- 证据：E005, E012

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1946→1975（+29），外部调用边 510→547（+37），compose 方法 25 不变，家族指纹由 67250897… 变为 aba2dbf1…。规模小幅增长而 compose 方法数不变，更像是现有类内部调用点/编译产物变化或代码迁移，而非新增 Compose 样式家族。
- 可能影响：UGC 详情页模块净化（DetailModulePurify*/DetailUnitedModulePurify*）所依赖的模块容器与调用边在静态层存在，但新增调用边来源未定位，Hook 落点是否移位、是否有未归类调用者绕过净化均未知；DetailModulePurifyPolicy 中登记的模块名是否仍与宿主一致无法从摘录判断。
- 验证：对两侧同名类做方法体哈希与类名对照，定位这 37 条新增调用边的来源类；真机进入普通稿件详情页，逐项输出 DetailModulePurifyPolicy 登记的模块名是否被命中，并抓 logcat 中 FeatureInstallResult 的 installed/complete 状态。
- 证据：E005, E012

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4581→4633（+52），compose 方法 99→98（-1），外部调用边 4257→4199（-58），指纹由 b0f0b041… 变为 56c25b77…。类增加而边减少方向相反，符合重构/内联、重复包装层合并或 DEX 重排的形态；detail_kotlin_moss 调用边 10→38（+28）而 detail_java_moss 32/35 不变，说明 Kotlin 侧消费者扩大而 Java 侧调用面未变。
- 可能影响：united 详情页的展示层净化（DetailUnitedPresentationPurify*）与推广位 Hook 依赖的调用路径可能被内联或迁移，减少的 58 条边中若含被 Hook 的方法，会导致安装成功但实际不生效；Kotlin MOSS 新增调用方是否被 KotlinMossChannel/KotlinMossReplyBridge 覆盖未知。
- 验证：对 united 家族抽样类做 JADX 反编译，检查减少的调用边是否落在净化策略引用的方法上；枚举 detail_kotlin_moss 的 38 条调用边的宿主类，与 KotlinMossChannel 的回调注册点比对；真机打开 united 样式详情页并确认净化项实际生效（而非仅安装日志成功）。
- 证据：E005, E011, E012

### pgc

PGC 页两条登记路径均为 static_invoke_observed。pgc_legacy：类 354→352（-2），外部调用边 399→425（+26），指纹 2c5cf1a4…→60c8869e…；类数下降同时边数上升，指向重构/内联或调用点合并，而非家族消失。pgc_theseus：类 2265→2276（+11），compose 方法 131→134（+3），外部调用边 782→1179（+397，约 +50.8%），指纹 4df56dbb…→44b6f779…；类规模仅小幅变动而边数大幅增长，最可能来自编译/内联策略、生成代码或调用点集中化，而非新增 UI 家族，需以方法体哈希和方法级对照排除混淆与 DEX 重排（E006）。协议面 pgc_player_moss（定义 12、调用边 3）与 pgc_view_moss（定义 14、调用边 7）两侧完全一致，说明 PGC 协议层没有静态可见变化，变化集中在 UI/调用图。模块侧本期源码候选中 PGC 相关只有 PgcAutoActivityPopupLocator/PgcAutoActivityPopupPolicy/PgcAutoActivityPopupFeatureInstaller，其余 PGC Hook 未在候选清单中出现，属未映射候选（unmapped_multi_path_candidates 与 source_catalog_scope=candidate index only），因此不能把这两条路径的覆盖情况视为已知。所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review，且源码快照为 published_unverified_worktree（working_tree_dirty=true），本页不构成适配结论。证据：E006、E000。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类 354→352（-2），外部调用边 399→425（+26），compose 方法 0，指纹 2c5cf1a4…→60c8869e…；规模几乎不变但指纹与边数变化，符合重构/内联或类合并，不足以判定旧样式消失或新增。
- 可能影响：PgcAutoActivityPopupLocator 依赖的旧版 PGC 容器类名/方法签名若被重命名或合并，弹窗自动关闭会静默失效；减少的 2 个类是否承载 Locator 锚点未知。
- 验证：用 decompile_class 按 PgcAutoActivityPopupLocator/Policy 中登记的目标类名在 9.17.0 中重解析，记录命中/未命中；真机打开番剧详情页触发活动弹窗，抓 logcat 确认 Locator 命中的类与方法签名，并记录弹窗是否被关闭。
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2265→2276（+11），compose 方法 131→134（+3），外部调用边 782→1179（+397），指纹 4df56dbb…→44b6f779…；pgc_player_moss（12/3）与 pgc_view_moss（14/7）两侧完全一致，协议面无静态变化，变化集中于 UI 调用图。
- 可能影响：Theseus 版 PGC 详情/播放页的模块净化与弹窗兜底若锚定在被重排或内联的调用边上，可能安装成功但运行时不触发；新增的 397 条边中是否出现未归类的跨家族消费者未知，宽屏/平板分支是否切换家族亦未知。
- 验证：对 pgc_theseus 抽样类 JADX 反编译并按方法体哈希与基线同名类对照，定位新增调用边的宿主；真机分别在小屏与平板/宽屏下打开 PGC 详情页与播放页，记录实际生效的家族（legacy 还是 theseus）与净化/弹窗结果，并核对服务端开关是否导致家族切换。
- 证据：E006

### player

播放页登记两条并存路径：player_java（953 类、0 Compose 方法、3308 条外调边）与 player_kotlin（455 类、37 Compose 方法、841 条外调边），二者均 static_invoke_observed。相对基线，player_java 类数 958→953（−5）、外调边 3222→3308（+86）、指纹变更；player_kotlin 类数 7→455（+448）、外调边 100→841（+741）、Compose 方法 0→37、指纹变更。协议层两侧完全一致：player_java_moss 定义 18 / 实际调用边 2，player_kotlin_moss 定义 34 / 实际调用边 3，说明 MOSS 接口面未见新增或删除，kotlin 家族的规模跃迁更可能来自包归属与检测边界变化（Java 侧同步减少）而非确认的新播放器样式，也可能是 DEX 重排、混淆改名或编译器变化。Compose 方法首次出现在该家族，需真机确认是否为播放页控件层迁移。分区、小窗、横屏/平板宽屏与服务端开关注入点均未读到运行条件，记为未知。模块侧 PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess 等仅出现在源码文件清单中，本单元未读其正文，解析点与兜底策略不得推测。

证据：E007, E000

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类数 958→953（−5）、外调边 3222→3308（+86）、Compose 方法两侧均为 0，结构指纹 2830eeae…→f355088b… 变化。
- 可能影响：若减少的 5 个类恰为模块 locator 目标（如播放速度/缓冲配置持有者），可能导致按类名解析失败；但同名同名替换、包迁移或内联都可能产生同向变化，实际 Hook 命中情况未知。
- 验证：对 player_java 目标侧按类名交集重读 family_evidence，列出仅在基线存在的 5 个类及其方法体哈希；真机在 Feed 详情、PGC 与直播回放播放器上打印 locator 解析结果。
- 证据：E007, E000

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数 7→455（+448）、外调边 100→841（+741）、Compose 方法 0→37，结构指纹 c20595ba…→b9a6ea0f… 变化；player_kotlin_moss 定义数 34 与调用边 3 两侧不变。
- 可能影响：家族判定范围扩大后，原先不计入该家族的 Kotlin 播放代码可能已进入视野，模块若按旧类集合或旧成员签名安装 Hook，可能在新增 Compose 承载的控件层漏挂；也可能相反，为原未覆盖样式提供新挂点。两种方向均无运行证据。
- 验证：重读 player_kotlin 双侧 class_samples，比对同名类 method_bodies_sha256 是否一致（一致则偏向重排/改名）；在 9.17.0 真机上对播放页、小窗与平板宽屏分别验证模块播放相关功能是否生效并记录日志。
- 证据：E007, E000

### danmaku

弹幕页登记两条路径：danmaku_legacy 在目标与基线均为 absent（classes=0、外调边 0、指纹为空集常量 4f53cda1…），danmaku_kotlin 为 static_invoke_observed。danmaku_kotlin 相对基线类数 57→137、Compose 方法 1→3、外调边 8→162，指纹变更。协议侧出现不对称：danmaku_java_moss 定义 22 / 调用边 20 两侧完全相同，danmaku_kotlin_moss 定义数 46 不变但实际调用边 4→10，即 Kotlin 侧消费点增加而接口面未变。这与播放页“协议面稳定、类落点变化”的模式一致，倾向解释为消费端迁移或调用路径重写，而不是新协议版本；也需排除 DEX 重排与去重口径变化。danmaku_legacy 的 absent 只说明该家族命名空间下无可归入类，不能用“页面功能消失”解释，旧弹幕渲染是否仍由未归类类承担需另行查证。DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt 仅出现在源码文件清单，本单元未读正文，净化安装器的解析点、覆盖率分母与兜底均为未知；弹幕与评论区共用 reply MOSS 的假设缺乏本单元证据支持。

证据：E008, E000

#### 路径：danmaku_legacy

- 状态：absent
- 变化：两侧 classes=0、Compose 方法 0、外调边 0，指纹同为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945（空集常量），无结构变化。
- 可能影响：该家族路径无静态类可挂点，模块若仍按 legacy 类名安装弹幕相关 Hook 将无目标；但不能据此推断旧弹幕渲染被移除或页面功能消失，功能可能由 danmaku_kotlin 或未归类类承担。
- 验证：在真机弹幕开关与净化开关下抓取类加载列表，检索是否存在未被归入任一登记家族的弹幕渲染类；核对模块中是否存在仍指向 legacy 类名的解析分支。
- 证据：E008, E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类数 57→137、Compose 方法 1→3、外调边 8→162，指纹 323c06fe…→38fdecc8… 变化；danmaku_kotlin_moss 定义数 46 不变而实际调用边 4→10。
- 可能影响：新增 6 条 Kotlin MOSS 调用边可能带来新的弹幕数据消费者，模块若只挂旧消费点会漏掉新入口；反向也可能是同一逻辑被拆包或去重口径变化，实际命中未知。
- 验证：重读 danmaku_kotlin_moss 目标侧四例调用者样本，逐条核对新增边的 callee 签名与 owner 是否在基线同名存在；真机开启弹幕净化，记录 DanmakuPurifyFeatureInstaller 安装结果与 complete 标志。
- 证据：E008, E000

### story

story 页登记 story_native 与 story_kotlin 两条路径。story_native 在 9.16.1→9.17.0 两侧均为 static_invoke_observed：类数 2924→2956（+32）、compose 方法 44→44（不变）、外部调用边 1310→1328（+18），指纹 b56b7342…→dafc7376…（E009）。变化同时落在类数与调用边上，但预取每家族只给两个类样本，无法代表 2956 个类的实现；E011 中 comment_compose 有 2428 类也只回两个样本，说明该视图是有界摘录，本页结论必须按样本不足处理。story_kotlin 双侧均为 absent：0 类、0 compose 方法、0 外部调用边、空指纹 4f53cda1…，说明静态面没有可独立登记的 Kotlin story 家族；但 absent 只表示该家族桶为空，不表示页面功能消失，Kotlin 实现有可能被并入 story_native 或被其他家族吸收，需按特征而非家族名再检索。本页 protocols 为空，KStoryMoss/StoryMoss、DynamicMoss、KOpusMoss/OpusMoss 等仅存在于 unregistered_protocols，尚未建立与我页的消费者映射，不能推定共同协议在本页生效。模块侧存在 HomeVerticalDetailFeatureInstaller、HomeVerticalDetailRouting、StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller/Policy、PlayerStoryFreeDataPromotionAccess 等候选文件（seed source_files），但本轮未读取其内容，故定位器字符串、失败兜底与实际挂载点均为未知。运行时启用、平板/宽屏布局、服务端开关三类条件没有任何证据，概览级 status 只能保持 installer_and_runtime_validation_required。

证据：E009, E011, E013

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类 2924→2956（+32）、compose 方法 44→44、外部调用边 1310→1328（+18），指纹 b56b7342…→dafc7376…；预取未给出新增类名与新增边端点（E009）。
- 可能影响：若 +32 类为真实新增实现，story 相关 Hook（如 HomeVerticalDetailRouting、StoryPurifyFeatureInstaller 按名/按签名解析的目标）可能漏挂或只覆盖旧路径；若仅为混淆改名与 DEX 重排，则功能面无变化。两种解释当前都不能排除（对照 E013）。
- 验证：先对 story_native 取双侧完整类名与方法签名 diff（不用两样本），把 +32 类与 +18 条外部调用边的端点对齐；再对新增类用 decompile_class 读方法体判断是否承载竖屏详情/Story 样式；最后在 9.17.0 真机打开竖屏详情入口抓模块 Hook 命中日志。
- 证据：E009, E011, E013

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧恒为 0 类、0 compose 方法、0 外部调用边，指纹 4f53cda1…（空集合指纹），无版本间差异。
- 可能影响：静态面没有独立 Kotlin story 家族可供安装器解析，story 相关 Hook 只能落在 story_native（Java/混淆）路径上；不等于 Kotlin 侧页面或功能消失，可能是实现并入其他家族。
- 验证：不按家族名而按代码特征全量检索（如 StoryMoss/KStoryMoss 的消费端类、竖屏详情路由入口），再用 protocol_evidence 检查是否存在跨家族实际调用边；确认后再判定是否需要新增登记家族。
- 证据：E009

### mine

mine 页登记 mine_native 与 mine_account_model 两条路径，两侧均为 static_invoke_observed，无 absent 路径。mine_native：类 325→326（+1）、compose 方法 7→7、外部调用边 92→94（+2），指纹 75f16dab…→f6b18de5…。mine_account_model：类 132→132、compose 方法 0→0、外部调用边 43→43，三项计数完全不变，只有指纹 2b548e1a…→db7f2792… 变化（E010）。这构成首要判断分歧：mine_account_model 的差异没有任何计数级或端点级支持，而深挖对照 E013/E014 显示 home_new_frame 在两侧类数 196、compose 方法 33 完全一致的情况下，指纹仍因方法体哈希变化与字段类型名改名（Lap1/b→LVt1/b）而不同，说明本流水线的指纹对混淆改名/DEX 重排敏感；因此把 mine_account_model 直接读作“协议或账号模型结构变更”缺乏依据。mine_native 的 +1 类与 +2 边是更实质的差异，但 seed 未给出新增类名或边端点，无法判断是组件过滤/VIP 逻辑新增还是迁移，涉及 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、MineComponentSnapshotStore/QueryClient 等解析点，本轮均未读取源码，故按名解析是否会漏挂、安装器是否有兜底全部未知。本页 protocols 为空，KMineMoss/MineMoss、AccountInterfaceV1Moss/KAccountInterfaceV1Moss、FissionMoss 均在全局未注册名单中，属候选而非已确认消费者，需靠调用边而非协议存在性判断。运行时启用、服务端开关、平板/宽屏差异无证据，整体仍为 installer_and_runtime_validation_required。

证据：E010, E013, E014

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类 325→326（+1）、compose 方法 7→7、外部调用边 92→94（+2），指纹 75f16dab…→f6b18de5…，seed 标记为 structure_or_call_path_changed；未给出新增类名与新增边端点（E010）。
- 可能影响：+1 类与 +2 边可能承载新的“我的”组件过滤或 VIP 卡片相关逻辑，导致 MineComponentFilterFeatureInstaller/MineVipFeatureInstaller 按名定位失败或只覆盖旧实现；也可能只是混淆重排，功能面不受影响，当前无法区分。
- 验证：取 mine_native 双侧完整类名 diff 定位新增类，对新增类用 decompile_class 读方法体与其调用者；在 9.17.0 真机进入“我的”页，核对组件过滤、VIP 卡片与阅读卡片（HostMineReadingCard）Hook 是否命中，并检查安装器失败分支是否落到兜底。
- 证据：E010, E013, E014

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类 132→132、compose 方法 0→0、外部调用边 43→43 三项不变，仅指纹 2b548e1a…→db7f2792…；对照 E013/E014，home_new_frame 在计数完全一致时指纹同样变化且仅见字段类型改名，说明指纹变化可仅由混淆改名与方法体哈希变动引起（E010、E013、E014）。
- 可能影响：目前没有计数级证据表明账号模型协议或字段结构发生变化，故“新样式/新协议”判断应降级；若确为改名，按反射字段解析账号模型的 Hook 风险并不升高。但 KMineMoss/MineMoss、AccountInterfaceV1Moss 是否为该模型的跨家族消费者仍未确认，不能断言无影响。
- 验证：对 mine_account_model 取双侧字段与方法签名级 diff（而非两个类样本），确认是否有字段增删或类型变更；对 AccountInterfaceV1Moss、KMineMoss 做 protocol_evidence 找实际调用边与调用方家族；真机抓账号信息加载路径与 VIP 状态读取日志，确认反射解析点是否仍命中。
- 证据：E010, E013, E014

### F001：comment_compose 有界抽样只见 kntr.common.comment.* 数据/富文本模型类，Compose 渲染入口与模块桥接的对应未闭合
事实（E011，有界摘录 5/2428 类）：comment_compose 目标侧样本 kntr/common/comment/common/service/f、common/service/g、richtext/g$a、richtext/i、richtext/IconText 的 compose_signatures 全为空、字段数为 0、方法体为短 getter 或返回 kotlinx.coroutines.flow.Flow；service/f 的方法以 com/bapis/bilibili/main/community/reply/v1/KReplyInfo 与 kntr/common/comment/common/model/O 为参数。据此只能说该家族桶至少混入了数据/富文本模型与 Flow 服务层，不能说它是渲染层。事实（E012）：CommentNativeBindingCatalog 只登记 LEGACY/NEXT/EXP3 三个 com.bilibili.app.comment3.* 原生处理器，bindingMethods 要求 owner 声明 .CommentItem 字段且存在 1..5 参数中的绑定型参数；其作用域是原生外观家族，不解析 Compose 家族，因此“样本包名与该目录不一致”本身不构成定位器失配证据。未知：2428 类中 283 个 compose 方法所在类、以及模块 CommentComposePurifyBridge/CommentComposeViewAccess 实际解析的类名，本轮均未读取，Compose 侧 Hook 覆盖保持 unknown。反例：kntr 类可能只是服务端样式关闭时也会提前加载的协议层；Compose 渲染入口可能仍在 comment3 或其它包，未被采样命中；类减边增也可能来自 lambda 去糖/接口调用点拆分。
反例与替代解释：若按名检索在 kntr/common/comment/** 之外找到 compose 入口类，则“桶混入模型层”只说明统计口径问题，渲染入口未迁移，本发现降级为口径说明；若模块 Compose 桥接的硬编码类名在 9.17.0 解析成功，则失配假设被推翻，指纹变化只剩 DEX 重排/混淆解释；若三步均失败且真机 Compose 样式下净化与复制功能无命中，才可升级为渲染栈变更候选。
建议：补证优先级：(1) 对 comment_compose 用带过滤的 deep dive 按名检索含 Compose 注解/Compose 签名的类，取 3–5 个真实渲染入口类，判定其包前缀是否在 kntr/common/comment 之外；(2) 真机打印 CommentNativeBindingCatalog.mainHandlers 三个类的 classOf 成功/失败、declaredFields 中 CommentItem 命中数与 bindingMethods 数量，回填 native_legacy/native_next/native_exp3 的 module_coverage；(3) 读 CommentComposePurifyBridge/CommentComposeViewAccess 源码（按文件哈希追溯）核对其硬编码类名与前一步得到的类是否一致。在上述任一步完成前，不接受“Compose 已覆盖”或“Compose 已失配”两种结论。
证据：E011, E012, E001

### F002：comment_compose 类数下降而外部调用边上升 17.9%，三条原生家族边数分化，跨家族消费者未被验证
事实（E001）：comment_compose 类 2444→2428、compose 方法 278→283、外部边 934→1101（+167 条）；同侧 comment_legacy_v2 边 735→741、comment_native_legacy 211→220、comment_native_next 50→67 上行，comment_native_exp3 62→52 下行。协议面 comment_java_moss 定义/边 50/50 不变，comment_kotlin_moss 定义 130 不变、实际边 26→23。推断（待验证）：Compose 侧可能存在新增跨家族消费者（入口卡片、表情、回复预览桥接等），exp3 的调用链可能被合并或裁剪。反例与替代解释：边数不是覆盖单位，接口分派、启动顺序、服务端开关在静态计数中不可见；类减边增也可由去内联/内联方向变化、接口调用点拆分为多实现、lambda 去糖方式变更造成；E011 的 5 类有界样本既未覆盖边端点点，也未出现 compose 签名，无法支撑“跨家族”判断；此外 KReplyMoss/ReplyMoss 在 seed 的 unregistered_protocols 中未登记，评论协议面本身存在缺口。
反例与替代解释：若新增边全部落在同一家族内部且为合成访问器/委托方法，则“跨家族消费者”推断被推翻，边增长仅需按重排/去糖解释；若真机仅观察到单一外观家族且 exp3 分支不可达，则 exp3 边下降更可能是实验下线而非统计噪声；反之若实测多家族并存且边端点跨家族，则指向服务端样式分桶叠加真实新增调用。
建议：从 comment_native_next 与 comment_compose 各取 3 条新增外部边的源/目标端点，读取目标方法所属家族，判断是否为同一家族内的合成访问器或真正的跨家族回调；同时枚举 comment_kotlin_moss 26→23 减少的调用方类名。真机侧按 legacy_v2 / native_legacy / native_next / native_exp3 / Compose 五个实验位分别进入评论区，记录实际命中家族与 CommentFamilyCoverage.describe() 输出，确认并存栈切换条件。
证据：E001, E011

### F003：dynamic_opus 边数 +21.5% 与 dynamic_compose 类/compose 方法同增，而 dynamic_legacy 边数下降
事实：dynamic_opus 186→226 边但类 1352→1350、compose 方法 92→94；dynamic_compose 1136→1187 类、127→141 compose 方法、221→234 边；dynamic_legacy 3251→3255 类但边 2151→2075（E002）。协议面动态两侧完全不变（java_moss 134/134，kotlin_moss 382 定义、边 26→26），因此变化只在客户端调用结构。推断：Opus 与 Compose 侧的组件连线加密可能是新转发/评论区入口或包装层叠加，legacy 侧边数下降更像内联合并。反证点：dynamic_legacy 自身含 103 个 compose 方法，说明家族桶边界本身按包名/命名而非渲染技术切分，家族间此消彼长可能只是类在桶间迁移（例如类从 legacy 包移入 compose 包），并非新增样式；服务端 A/B 无结构变化时静态完全不可见。
反例与替代解释：若交叉抽样发现新增类全部来自 legacy 包迁移，则“新组件家族”推断被推翻，仅需更新家族映射；若真机日志显示 Compose 净化安装成功但页面无效果，则问题在 Hook 点语义而非覆盖；若服务端 A/B 分桶在真机间表现不一致，则静态不可见性被确认，需补服务端开关抓取。
建议：先做类名迁移核对：比对两版本中 dynamic_legacy 减少的类是否出现在 dynamic_compose/dynamic_opus 新增集合（可用 family_evidence 交叉抽样）；再在真机分别进入动态关注/推荐/Opus 详情页，记录 DynamicTabsFeatureInstaller、DynamicPurifyFeatureInstaller 的安装日志与实际净化命中条目，验证平板/宽屏是否走不同分支。
证据：E002

### F004：home_new_frame 指纹漂移可由混淆改名解释，不能据此判定新样式
事实：9.17.0 与 9.16.1 的 home_new_frame 均为 196 类、33 个 compose 方法，仅外部调用边 49→52、指纹 4a3e9002…→34c59fa3…（E003）。按名重读样本显示 bubble/d、bubble/e、bubble/f 的 method_bodies_sha256 两侧逐字相同（如 bubble/d 3456…a58、bubble/e 4218…561），bubble/s 仅两方法形参顺序互换（基线 a(u)、b(u;Function0)；目标 a(u;Function0)、b(u)），HomeFrameViewModel$dispatchAction$1 仅字段类型 Lap1/b→Vt1/b 改名（E013、E014）。这说明存在“结构哈希变化≠新样式”的典型反例：类数与 compose 方法数守恒，变化集中在名称与签名顺序层面。仍未闭合的是那 3 条新增外部调用边的归属，以及 bubble/s 方法体哈希差异是否仅由签名顺序影响常量池/字节序造成。模块侧 HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilterFeatureInstaller 等定位器/安装器源码本单元未核对，模块覆盖仍为 requires_installer_review，不能据此推定 Hook 命中或失效。
反例与替代解释：若后续全量类配对比对显示存在 method 集合与字段结构均无对应物的 class（而非改名），或那 3 条新增边落在 dispatchAction / bubble 控制路径且引入新分支，则“仅混淆改名”不成立，需按真实调用路径变化处理；反之若所有样本都能按重命名一一对应，则指纹差异可判为噪声。
建议：对 home_new_frame 两侧做全量方法体哈希配对（不只比对指纹），产出未配对类与未配对调用边清单；同时按文件哈希补读 HomeFrameTabLocator、HomeFrameListHook 等定位器源码，核对目标类/方法签名是否仍可解析；再在真机打开 Hook 日志，确认 HomeFrameViewModel.dispatchAction 与 Bubble 控制器是否被安装器选中，并记录 3 条新增边的浮现代码位置。
证据：E003, E013, E014

### F005：home_legacy 调用边减少 6 条，归属与是否迁移出家族均未定位
事实：home_legacy 由 767 类、204 条外部调用边变为 766 类、198 条，compose 方法数 87 不变。当前仅有每侧两个类样本的有界摘录，无法看到边级明细，因此既无法判断减少的边是属于组件过滤、横幅、顶栏还是推荐净化所依赖的宿主点，也无法排除这些边被合并成单个调用点或落到未加载分支。模块侧 HomeComponentFilterFeatureInstaller、HomeBannerFeatureInstaller、HomeTopBarFeatureInstaller、HomeRecommendPurifyFeatureInstaller 本轮未读取，定位器兜底逻辑未知，不能推断 Hook 覆盖仍有效。此条属明确的证据缺口，而非“无影响”。
反例与替代解释：若边级比对显示减少的边全部指向未被模块使用的内部工具方法，则对功能影响可降级；若减少的边命中原有的植入目标签名，则说明植入点消失需迁移。服务端未开启对应模块也会使静态可见但运行不触发，需以运行时开关记录区分。
建议：按 family 名导出 home_legacy 两侧完整调用边并做目标签名配对，列出 6 条消失边的调用方与目标；随后在真机 9.17.0 上以日志统计各 Home 功能安装器的定位成功/失败次数，确认是否存在兜底路径被启用。
证据：E003

### F006：search 原生边减少与 Compose 边增加并存，已登记协议未变但未登记搜索协议与跨家族消费者未核实
事实：search_native 外部调用边 2859→2818（-41）、类 1702→1705；search_compose 类 3141→3146、compose 方法 561→562、外部调用边 595→614（+19）（E004）。已登记两族协议的定义与实际调用边两侧完全一致（search_java_moss 24 定义/22 调用边，search_kotlin_moss 52/18），即已登记协议面未扩张，函数级变化出现在 UI 消费者一侧（E004）。但该结论只覆盖这两族：seed 的 unregistered_protocols 仍有 app/search/v2/SearchMoss、KSearchMoss、app/interfaces/v1/SearchMoss、broadcast/message/search/SearchMoss 等多条搜索相关协议未纳入比对，不能宣称搜索侧协议面整体未变。方向相反的两个增量构成“原生→Compose 消费者迁移”的候选解释，DEX 重排、条件分支合并或服务端样式开关同样可解释，静态矩阵未记录运行条件，无法判定当前默认样式。SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 及 KotlinMossChannel/KotlinMossReplyBridge 源码本单元未核对，Composable 侧第二组消费者与定位器兜底均为未知。定义数与调用边数单位不同，22 与 18 不构成覆盖率，也不代表其余定义无消费者。
反例与替代解释：若两侧调用边配对后未发现目标签名级的迁移关系（减少与增加的边互不相关），则“迁移”解释不成立；若真机日志显示默认样式仍为原生且模块命中正常，则 Compose 侧边增加可判为无害；若服务端 A/B 在无结构变化情况下切换样式，则静态方法本身对该问题不可见，需以运行开关记录推翻或确认。
建议：先按文件哈希补读 SearchHomeRecommendLocator/Policy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 与 KotlinMossChannel/KotlinMossReplyBridge，记录解析点与失败兜底；再导出 search_native 与 search_compose 两侧调用边并交叉配对，定位那 1 个新增 compose 方法与其调用者，判断减少与增加的边是否相关；随后枚举 search_java_moss 22 条与 search_kotlin_moss 18 条调用边的调用方是否存在 Composable 侧消费者；最后在真机分别以原生与 Compose 样式进入搜索页，记录清理与默认词清理命中日志并确认服务端是否切换样式。
证据：E004

### F007：详情页评论区原生绑定锚点是三个硬编码 handler 类名，解析失败静默返回空列表，静态证据不足覆盖
事实：comment_compose 家族在目标 APK 静态存在 2428 类、283 个 compose 方法、1101 条外部调用边，evidence=static_invoke_observed（E011），说明详情页 Compose 评论区实现仍在包内；模块 CommentNativeBindingCatalog 以三个硬编码字符串为锚点：com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler、ui.nextholder.handle.CommentNextContentRichTextHandler、ui.nextholderexp3.handle.CommentNextExperiment3ContentRichTextHandler，注释明确“三个外观实验可在同一个 APK 中共存”，且只在安装时解析、不进入逐条绑定热路径；bindingMethods 先要求宿主类存在 CommentItem 类型字段，否则 emptyList()，再用“非静态、非 bridge/synthetic、返回 void、参数 1..5、存在 View 容器参数”的启发式筛选（E012）。推断：若宿主把这三个类改名或把 handler 迁入其他前缀包，catalog 会静默返回空列表而不产生安装失败信号，CommentFamilyCoverage 会把该 family 记为未安装或不可见，形成“安装成功但评论净化不生效”的漏覆盖形态。缺口：本轮预取为有界摘录（两家族/两协议各两个样本类、四个调用方样本），未提供三个 handler 类在 9.17.0 或 9.16.1 中的存在性与方法签名，也无法从 E011/E012 判定这三类是否落在 comment_compose 家族内；detail_kotlin_moss 调用边 10→38 也提示 Kotlin MOSS 侧消费者扩大，但其宿主类未核实。故保持 needs_runtime，不宣称覆盖。
反例与替代解释：若检索到三个 handler 中至少一个在 9.17.0 中存在且带 CommentItem 字段并命中过滤条件，则锚点解析成立、当前漏覆盖推断被推翻，问题降级为运行时是否走到该 holder；若基线 9.16.1 同样三缺三，则说明该 catalog 从未在本包生效，属历史未覆盖而非本次回归；若 E011 显示同类目录结构与键方法在基线同量级（2428 类 / 283 compose 方法的基线对照未提供），则家族增长更可能是混淆改名或 DEX 重排所致，而不是新样式上线。E011、E012 任一不支持“handler 存在”即维持当前候选状态。
建议：最小补证：(1) 在 9.17.0 用 decompile_class 按上述三个全名及 ui.holder / ui.nextholder / ui.nextholderexp3 三个包前缀检索，输出命中类的字段（含 CommentItem）与方法签名、方法体哈希；(2) 若命中，逐条套用 catalog 的过滤条件（非静态、void 返回、参数 1..5、含 View 容器参数）判定 bindingMethods 是否会返回空；(3) 真机打开普通稿件详情页评论区，抓 logcat 中 CommentFamilyCoverage 的 per-family 结果与 FeatureInstallResult.Installed.complete，确认该 family 是被记为 0 还是 2。
证据：E011, E012, E005

### F008：PGC Theseus 调用边 782→1179 而类仅 +11，变化集中在 UI 调用图，弹窗定位器与净化落点未取证
事实（E006）：pgc_theseus 类 2265→2276（+11）、compose 方法 131→134（+3）、外部调用边 782→1179（+397，约 +50.8%），家族指纹 4df56dbb…→44b6f779…；pgc_legacy 类 354→352（−2）、外部调用边 399→425（+26）、compose 方法两侧为 0；pgc_player_moss（定义 12 / 调用边 3）与 pgc_view_moss（定义 14 / 调用边 7）两侧完全一致。推断：协议面静态无变化，变化集中在 UI/调用图；类规模仅小幅变动而边数大幅上升，更符合内联、生成代码/桥接调用集中化或 DEX 重排，而不是新增 UI 家族——但 E006 只是每家族两个样本类的有界摘录，未定位新增边的宿主类，故该解释仅为候选。影响面：若被 Hook 的调用点落在被内联或重构的方法上，模块可能安装成功而运行时不触发；反之若 Locator 锚点类未变，则当前风险推断被推翻。缺口：种子 source_files 只列出 PgcAutoActivityPopup*/Policy/FeatureInstaller 三个 PGC 相关文件，且源文件清单为 candidate index（source_catalog_scope=candidate index only，含 unmapped_multi_path_candidates），本单元未取得这些文件的模块源码工具证据，无法判定其解析锚点是否与本次调用图变化重合；两条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，源码快照 published_unverified_worktree / working_tree_dirty=true。
反例与替代解释：若方法级对照显示 +397 条新边来自同一批类的内联调用、且不涉及 pgc_view_moss/pgc_player_moss 订阅点或 Locator 锚点方法，则“可能影响净化/弹窗”的推断被推翻，变化可归为编译或 DEX 重排；若 Locator 登记的类在目标包缺失或签名改变，则升级为确定回归候选。若真机在平板/宽屏实际走 legacy 家族，则本发现对该设备形态需按 pgc_legacy 重做对照。若完整家族枚举显示类增量实为数十个新 UI 类而非 +11，则“非新样式”推断同样被推翻。
建议：最小补证：(1) 对 pgc_theseus 与 pgc_legacy 各取双侧同名类做方法体哈希与方法级对照，输出新增/消失调用边的宿主类，判断是否落在内联或重构方法上；(2) 用 decompile_class 按 PgcAutoActivityPopupLocator/Policy 登记的目标类名在 9.17.0 重解析，记录命中、缺失与签名差异，并记录该文件 sha256（工作树 dirty）；(3) 真机在小屏与平板/宽屏分别打开 PGC 详情页与播放页，记录实际生效家族、活动弹窗是否被自动关闭、净化项是否生效，并核对服务端开关是否切换家族。
证据：E006

### F009：player_kotlin 家族由 7 类跃升至 455 类且新增 37 个 Compose 方法，但 MOSS 定义面两侧完全不变
事实：目标侧 player_kotlin 为 455 类 / 841 外调边 / 37 Compose 方法，基线为 7 类 / 100 外调边 / 0 Compose 方法，指纹 c20595ba…→b9a6ea0f…；player_java 958→953 类、外调边 3222→3308，指纹 2830eeae…→f355088b…；player_java_moss（18 定义 / 2 调用边）与 player_kotlin_moss（34 定义 / 3 调用边）两侧数值完全相同。推断：协议接口面未增删，但定义数不变不证明消费面未变。数量级上 Java 侧只减 5 类，无法解释 Kotlin 侧 +448 类，因此不能把扩张归因于“Java 代码迁入 Kotlin 命名空间”；更可能的解释是家族判定范围/检测口径变化（例如某包前缀新被纳入该家族）、DEX 重排、混淆改名或编译器产物差异，这四类原因在本单元证据下无法区分，故不构成新播放器样式结论。Compose 方法首次出现在该家族（0→37），与“播放页控件层迁移”相容，也与“新纳入包本身含 Compose 代码”相容，二者同样未区分；player_java 侧 Compose 方法仍为 0，不支持控件层整体从 Java 迁向 Kotlin 的简单图景。待真机验证：新增类是否在播放页运行路径上实际加载，以及模块播放侧安装器（PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess 等，本单元仅见源码路径未读正文）能否在新落点解析到目标；分区、小窗、横屏/平板宽屏与服务端开关的运行条件均未读到，记未知。
反例与替代解释：可推翻或替代当前推断的证据：(a) 按类名交集重读 family_evidence 后，若新增 448 类中多数在基线同名同签名、方法体哈希一致 → 属重排/改名或家族边界重划，不构成样式变化；(b) 若新增类在基线完全不存在且集中在单一播放控件包 → 支持真实代码迁移；(c) 若这些类只在特定实验分组或平板/宽屏布局下出现 → 属服务端/配置门控的并存栈，静态无法穷尽；(d) 若更完整的 player_kotlin_moss 调用者样本显示调用边实际增加 → 协议消费面也变了，本推断需扩为协议层变化；(e) 若真机上各 locator 全部解析成功且功能生效 → 只能说明该版本路径可达，仍不等于适配通过。
建议：1) 对 player_kotlin 双侧按类名交集重读 family_evidence，输出仅在目标侧存在的类清单、父类与 compose_signatures 分布，并比对同名类 method_bodies_sha256；2) 同时确认两次构建所用家族判定口径（包前缀/白名单/工具版本）是否一致，若不一致应先排除检测边界变化再谈样式；3) 重读 family_evidence(player_java) 找出基线存在而目标缺失的 5 个类，核查是否为模块播放侧 locator/installer 目标并确认替代落点；4) 真机 9.17.0 分别在 Feed 详情、PGC、小窗、横屏与平板宽屏采集类加载列表与 locator 解析日志，失败项保留在分母；5) 在服务端实验分组与默认分组各测一轮，区分结构变化与开关切换。
证据：E007, E000

### F010：danmaku_kotlin 外调边 8→162、Kotlin MOSS 实际调用边 4→10，而 danmaku_legacy 两侧均为空集
事实：danmaku_kotlin 类数 57→137、Compose 方法 1→3、外调边 8→162，指纹 323c06fe…→38fdecc8…；danmaku_kotlin_moss 定义数 46 两侧相同而实际调用边 4→10；danmaku_java_moss 22 定义 / 20 调用边两侧完全相同；danmaku_legacy 两侧 classes=0、外调边 0、指纹同为空集常量 4f53cda1…，状态 absent。推断（候选，非确认样式）：Kotlin 侧出现 6 条新增 MOSS 调用边而接口定义未变，与“消费端迁移或调用路径重写”相容；但基线仅 8 条外调边、4 条调用边，基数极小，8→162 与 +6 的比例被放大，去重/归并口径变化或家族判定边界变化足以单独造成同等量级落差，因此结构哈希变化不得读作新样式。legacy 两侧同为 absent 且指纹为同一空集常量，只说明该登记命名空间下无可挂点，不能推出旧弹幕渲染或净化功能消失；其功能可能由 danmaku_kotlin 或未归类类承担，本单元无类加载证据。跨家族对照说明：E012 为评论页模块源码（CommentNativeBindingCatalog 安装期解析 LEGACY/NEXT/EXP3 三外观并把失败单位留在分母），仅作“并存栈处理需安装期目录”的方法学参照，不构成本页证据，也不能据此推断弹幕侧存在等价目录或兜底。DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt 正文未读，安装点、分母与兜底均为未知；弹幕与评论区共用 reply MOSS 的假设本单元无证据支持。待真机验证：新增 6 条调用边是否在弹幕开启时真实执行、净化是否落在新消费点；服务端视觉变体若无结构变化则静态不可见，不宣称样式已穷尽。
反例与替代解释：可推翻或替代当前推断的证据：(a) 新增 6 条边与基线边同名同签名、仅 owner 混淆，或去重口径变化 → 不构成新消费点；(b) 更完整调用者样本显示这些边指向评论 reply MOSS → 属跨家族共用消费者而非弹幕新样式；(c) 若目标侧新增类在基线同名同签名且方法体哈希一致 → 归属重排/改名；(d) 若真机上净化在新增消费点前后行为一致且旧渲染类仍被加载 → 结构变化未影响功能可达性（仍不构成适配通过结论）；(e) 若差异仅在某实验分组出现 → 服务端门控并存栈，静态不可穷尽。
建议：1) 重读 protocol_evidence(danmaku_kotlin_moss, target)，逐条核对 4→10 中新增边的 callee 签名与 owner 是否在基线同名存在，并区分弹幕消费点与评论 reply 消费点；2) 读取 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt 正文（按快照文件 sha256 追溯，工作树 dirty 不可依赖状态），确认解析点、并存栈处理与兜底后再更新 danmaku_kotlin 的 module_coverage；3) 真机上开启/关闭弹幕与净化，记录安装结果与 complete 标志，并抓取渲染相关类加载列表，核查 absent 的 legacy 路径是否被未归类类替代；4) 用服务端实验分组对比同版本表现，区分样式门控与结构变化；5) 保留 runtime_enabled=unknown 直到出现日志或解析结果。
证据：E008, E000, E012

### F011：mine_account_model 指纹变化很可能是混淆改名而非协议结构变更
事实：mine_account_model 在 9.16.1→9.17.0 间类数 132→132、compose 方法 0→0、外部调用边 43→43 全部不变，只有指纹由 2b548e1a… 变为 db7f2792…（E010）；mine_native 侧类 325→326、边 92→94 有微增。深挖对照：home_new_frame 双侧类数同为 196、compose 方法同为 33，但指纹 4a3e9002…→34c59fa3… 仍不同，差异可具体观察到字段类型被改名（Lap1/b→LVt1/b）且方法体 sha256 改变（E013、E014）。推断：本流水线指纹包含方法体哈希与类型引用，对混淆改名、DEX 重排天然敏感，所以“structure_or_call_path_changed”标记在 mine_account_model 上不能直接解释为结构变化。影响：若按“结构已变”优先修 Hook，会错误改动本无风险的账号模型反射解析点；反之若真存在协议变更而被当作改名忽略，则 VIP/账号态读取会静默失效。反例/推翻条件：若字段签名级 diff 显示 AccountInterfaceV1Moss 相关字段增删或类型改动，或 43 条边的端点集合发生变化，则“仅改名”推断被推翻。未读到 MineVipFeatureInstaller/MineComponentSnapshot* 的解析代码，故解析点是否强依赖被改名类型仍未知。
反例与替代解释：1) 仅混淆改名/DEX 重排，无功能变化（由 E013/E014 支撑）；2) 账号协议字段真实增删，指纹只是附带结果（若有字段 diff 或边端点变化则成立）；3) 预取样本截断造成的假差异（用完整类名/字段列表重读即可排除）；4) 服务端开关驱动的账号模型变体，静态不可见（需真机抓包）。
建议：先做字段与方法签名级 diff（完整集合而非两个样本），并对 AccountInterfaceV1Moss、KMineMoss 取 protocol_evidence 确认实际调用边与调用方家族；只有确认字段或端点变化后，再投入 MineVipFeatureInstaller 的定位点复核。真机上叠加账号态加载日志作为交叉验证。
证据：E010, E013, E014

### F012：story_native 类数与调用边增长而 compose 方法不变，新增竖屏详情实现尚未定位
事实：story_native 在 9.16.1→9.17.0 间类 2924→2956（+32）、外部调用边 1310→1328（+18），compose 方法 44→44 不变，指纹 b56b7342…→dafc7376…（E009）；story_kotlin 两侧均为 absent（0 类/0 compose/0 边/空指纹 4f53cda1…），本页 protocols 为空（E009）。推断：compose 方法计数不变而类数与调用边同步增长，更可能是普通类（数据/服务/桥接）扩张或新路由模块整体并入，而非新增 Compose 样式家族；方法定义数与调用边数不是同一单位，不做比值或覆盖率推导，此处只作方向判断。样本局限：预取类样本是有界摘录——E011 中 comment_compose 声明 2428 类但摘录只返回少量类样本，且 E009 的 limits 标注“每家族两个类样本”与实际返回数量不一致，采样边界本身待复核；因此 2956 类中的变化分布未知，不能用前几个类代表整套实现。影响（推断）：HomeVerticalDetailRouting、StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller 等按名/按签名解析，本轮未读其源码，若新增实现未被登记，Hook 可能只在旧路径生效，出现同一页部分样式被处理、部分不处理的混合状态；反之若新增类只是混淆拆分，功能面无变化。未知：新增类是否承载竖屏详情/Story 入口、是否被平板/宽屏布局或服务端开关独占启用，均未读到运行条件，故事件分辨率仍需真机验证。
反例与替代解释：1) 新增类属于竖屏详情/Story 新实现，需要新增 Hook 覆盖（若新增类方法体出现 Story/竖屏详情相关调用即成立）；2) 仅 DEX 重排与混淆拆分导致的类计数膨胀，无新逻辑（若类名 diff 显示拆分类且方法体集合等价则成立）；3) 属于其他家族被误并入 story_native 桶（若新增类的调用方集中在动态/Opus 家族则成立）；4) 服务端 A/B 视觉变体无结构变化，静态不可见。
建议：完整取 story_native 双侧类名与方法签名 diff，把 +18 条外部调用边的源/目标端点对齐，判断新边是否落在新增类上；对新增类用 decompile_class 读方法体确认职责，并结合 E011 式有界摘录之外的完整类清单排除混淆拆分；再读 HomeVerticalDetailRouting 与 StoryPurifyFeatureInstaller 的定位字符串，核对是否覆盖新类、是否有失败兜底；最后在 9.17.0 真机竖屏详情入口抓 Hook 命中日志。
证据：E009, E011, E013

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
comment 页 5 条登记路径（comment_legacy_v2、comment_native_legacy、comment_native_next、comment_native_exp3、comment_compose）在 E001/E015 中 status 逐字均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，complete_coverage=false；因此不对任何路径给出“已适配/已生效”判断。数值变化（E001）：legacy_v2 类 579→583、外部边 735→741；native_legacy 172→181、211→220；native_next 45→48、边 50→67；native_exp3 58→54、62→52（唯一类与边双降）；comment_compose 2444→2428 类、compose 方法 278→283、外部边 934→1101。协议：comment_java_moss 定义 50、边 50 不变；comment_kotlin_moss 定义 130 不变、实际边 26→23。E011 为有界摘录（5/2428 类），样本全落在 Lkntr/common/comment/*，compose_signatures 全空、字段数为 0、方法体为短 getter/Flow 返回（service/g 全部返回 kotlinx.coroutines.flow.Flow，service/f 以 KReplyInfo 与 kntr model.O 为参数），只支持“该桶混入数据/富文本模型层”，不能代表 283 个 compose 方法所在类；E012 的 CommentNativeBindingCatalog 只登记三个 com.bilibili.app.comment3.* 原生处理器且要求 owner 声明 CommentItem 字段，作用域是原生家族而非 Compose，故样本包名与该目录不一致本身不构成失配证据。指纹变化未做同名类方法体哈希配对，按混淆改名/DEX 重排候选处理；五家族并存切换条件、服务端实验位与平板/宽屏分支均未读到，保持未知。
证据：E015, E001, E011, E012

### 复核页面：dynamic
dynamic 页 3 条登记路径（dynamic_legacy、dynamic_compose、dynamic_opus）在 E002/E016 中 status 逐字均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，complete_coverage=false。变化（E002）：dynamic_legacy 类 3251→3255、compose 方法 105→103、外部边 2151→2075；dynamic_compose 1136→1187 类、127→141 compose 方法、221→234 边；dynamic_opus 1352→1350 类、92→94 compose 方法、边 186→226。注意 dynamic_legacy 桶自身含 103 个 compose 方法，说明家族按包名/命名切分而非按渲染技术切分，同一类在桶间迁移即可造成一边降一边升；边数与方法定义数不是同一单位，拒绝据此推导覆盖率。协议面 dynamic_java_moss 定义 134、边 134 不变，dynamic_kotlin_moss 定义 382、边 26→26 不变，未见新增动态协议；但 seed 的 unregistered_protocols 仍含 DynamicMoss、KOpusMoss/OpusMoss、KTribeeMoss、CampusMoss、KFeedMoss 等，动态协议面存在未登记部分，不做覆盖推断。三路径的运行时启用、关注/推荐 tab 分桶、Opus 详情入口与平板/宽屏分支均未读到，Module 侧 DynamicPurify/DynamicTabs 安装器源码本轮未读取，全部保持未知。
证据：E016, E002

### 复核页面：home
两路径 status 均逐字保持 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review（E003）。数值与草稿一致：home_legacy 767→766 类、外部调用边 204→198、compose 方法 87 不变，指纹 7a842bbb…→a56da1e1…；home_new_frame 196 类、33 compose 方法均不变，边 49→52，指纹 4a3e9002…→34c59fa3…（E003）。样本级复核支持“结构哈希变化≠新样式”：bubble/d、bubble/e、bubble/f 的 method_bodies_sha256 两侧逐字相同，bubble/s 仅两方法形参顺序互换（基线 a(u)、b(u;Function0)；目标 a(u;Function0)、b(u)），HomeFrameViewModel$dispatchAction$1 仅字段类型 Lap1/b→Vt1/b 改名（E013、E014）。缺口明确：home_legacy 仅有族级摘要，6 条消失边的调用方与目标签名未定位；home_new_frame 3 条新增边未定位，bubble/s 哈希差异是否仅由签名顺序引起亦未闭合。模块侧 HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilter/Banner/TopBar/RecommendPurify 等安装器源码本单元未核对，定位与兜底只能记未知。该页 protocols 为空，且 seed 的 unregistered_protocols 仍含 app/home/v1/HomeMoss、KHomeMoss 等，跨家族协议消费者未评估；平板/宽屏与服务端样式开关的运行条件未读到。不宣称适配通过。
证据：E000, E003, E013, E014

### 复核页面：search
两路径 status 均保持 static_invoke_observed，运行时与模块覆盖仍为 unknown / requires_installer_review（E004）。数值核对一致：search_native 类 1702→1705、外部调用边 2859→2818（-41）、compose 方法仍为 2；search_compose 类 3141→3146、compose 方法 561→562、边 595→614（+19），指纹 fcde68da…→4e4c7892…（E004）。已登记两族协议两侧完全一致（search_java_moss 24 定义/22 调用边，search_kotlin_moss 52/18），但“协议面未扩张”只覆盖这两族：seed 的 unregistered_protocols 仍列出 app/search/v2/SearchMoss、KSearchMoss、app/interfaces/v1/SearchMoss、broadcast/message/search/SearchMoss 等多条搜索相关协议，未纳入比对，不能宣称搜索协议面整体未变。定义数与调用边数单位不同，22/18 不构成覆盖率，也不代表其余定义无消费者。方向相反的边增减只是“原生→Compose 消费者迁移”的候选解释，DEX 重排、条件分支合并、服务端 A/B 同样可产生相同差异。SearchHomeRecommendLocator/Policy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 与 KotlinMossChannel/ReplyBridge 源码本单元未核对，定位点、兜底与 Composable 侧第二组消费者均为未知。
证据：E000, E004

### 复核页面：detail
复核 E005：detail_legacy 两侧 classes/compose_methods/external_invoke_edges=0、指纹同为 4f53cda1…（空集哈希）、evidence=absent；detail_theseus_ugc 目标 1975 类/25 compose/547 边，基线 1946/25/510（指纹 67250897→aba2dbf1）；detail_theseus_united 目标 4633/98/4199，基线 4581/99/4257（指纹 b0f0b041→56c25b77）；detail_java_moss 32 定义/35 边两侧一致，detail_kotlin_moss 定义 76 不变、调用边 10→38。草稿数字与状态全部与 E005 吻合，status 逐字沿用静态矩阵（absent / static_invoke_observed），未改写为通过。限定也基本成立：ugc“类增边增而 compose 方法不变”与 united“类增而边减”的反向变化只被记为结构/调用图或混淆改名、DEX 重排候选，未升级为新样式；absent 未被当作旧原生详情样式消失，而是标注采集口径待核。E011 仅给出 comment_compose 目标侧 2428 类/283 compose/1101 边，基线侧未取；E012 只证明 CommentNativeBindingCatalog 的三个硬编码类名与 bindingMethods 过滤、空列表兜底和“只在安装时解析”注释，未提供三类存在性证据，草稿据此保持 needs_runtime 恰当。残留：E005/E011 为有界摘录（每家族两个样本类、协议各四个调用方），+37/−58 条调用边变化的宿主类未定位；united 展示层净化策略登记的模块名是否仍与宿主一致无静态证据；detail_legacy 的 absent 属空集还是家族判定缺失未核实。
证据：E000, E005, E011, E012

### 复核页面：pgc
复核 E006：pgc_legacy 目标 352 类/425 边，基线 354/399（指纹 2c5cf1a4→60c8869e）；pgc_theseus 目标 2276 类/134 compose/1179 边，基线 2265/131/782（指纹 4df56dbb→44b6f779）；pgc_player_moss 12 定义/3 边与 pgc_view_moss 14 定义/7 边两侧完全一致；两条路径 evidence=static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review，状态逐字与静态矩阵一致，未出现“已适配”表述。theseus 类 +11 而边 +397（约 +50.8%）被明确写为待方法级对照的候选解释（内联/生成代码/调用点集中化/DEX 重排），并给出“若新增边宿主与协议订阅点无交集则降级”的反例条件；legacy（类 −2、边 +26）与 theseus 两条并存路径已分别评审，符合并存栈要求。问题在于证据粒度与模块侧：E006 为每家族两个样本类的有界摘录，新增 397 条边的宿主类、compose 方法 +3 的来源未定位，“不是新增 UI 家族”仍属候选而非结论；本单元未取得任何 PGC 模块源码/定位器工具证据，源文件清单只是 candidate index（含 unmapped_multi_path_candidates），因此草稿对 PgcAutoActivityPopup* 锚点是否与变化重合只能保持未知，不能推断 Hook 失效或生效。平板/宽屏分支、PGC 播放页家族切换与服务端开关均未观测。源码快照 published_unverified_worktree（working_tree_dirty=true，source_tree_sha256=37745f8f…），后续结论须按文件哈希追溯。
证据：E000, E006

### 复核页面：player
播放页两条并存路径的证据状态逐字为：player_java = static_invoke_observed（953 类 / 0 Compose 方法 / 3308 外调边，指纹 2830eeae…→f355088b…，基线 958 类 / 3222 边）；player_kotlin = static_invoke_observed（455 类 / 37 Compose 方法 / 841 外调边，基线 7 类 / 100 边 / 0 Compose，指纹 c20595ba…→b9a6ea0f…）。两侧 MOSS 完全不动：player_java_moss 18 定义 / 2 实际调用边，player_kotlin_moss 34 定义 / 3 调用边，说明协议接口面未增删，但定义数不变不等于消费面不变，不能反推“无影响”。两路径 runtime_enabled 均为 unknown、module_coverage 均为 requires_installer_review，故不宣称任何路径适配通过。关键量化限定：Java 侧只减 5 类，无法解释 Kotlin 侧 +448 类，因此“代码从 Java 迁入 Kotlin 命名空间”单靠这两组计数不足以支撑，家族判定范围变化、DEX 重排与混淆改名同样能产生同向指纹漂移，三者未区分。Compose 方法首次出现在该家族，是否对应播放页控件层迁移未知。分区、小窗、横屏/平板宽屏与服务端开关注入点均未读到运行条件；PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess 等仅见于源码文件清单，正文未读，解析点与兜底不得推测。证据：E007（双侧家族与协议摘要）、E000（样本与基线标识、源码快照字段）。
证据：E007, E000

### 复核页面：danmaku
弹幕页两条路径状态逐字为：danmaku_legacy = absent（两侧 classes=0、外调边 0、Compose 0，指纹为两侧相同的空集常量 4f53cda1…，故无结构变化可言）；danmaku_kotlin = static_invoke_observed（类 57→137、Compose 方法 1→3、外调边 8→162，指纹 323c06fe…→38fdecc8…）。协议侧不对称：danmaku_java_moss 22 定义 / 20 调用边两侧相同，danmaku_kotlin_moss 定义 46 不变而实际调用边 4→10。需注意基数很小（基线 8 条边、4 条调用边），8→162 与 +6 边在比例上被放大，去重/归并口径或家族判定边界变化可单独造成该类落差，不能直接读作新样式。absnet 的 legacy 只表示该登记命名空间下无可归入类，不得据此推断旧弹幕渲染或净化功能消失；其功能可能由 danmaku_kotlin 或未归类类承担，本单元无类加载证据。两路径 runtime_enabled 均 unknown、module_coverage 均 requires_installer_review；DanmakuPurifyFeatureInstaller.kt、DanmakuPurifyPolicy.kt 正文未读，安装点、分母与兜底未知；弹幕与评论区共用 reply MOSS 的假设本单元无证据支持。服务端 A/B 若无结构变化则静态不可见，不宣称样式已穷尽。证据：E008、E000。
证据：E008, E000

### 复核页面：story
story 页登记 story_native 与 story_kotlin，复核后与草稿计数一致：story_native 在 9.16.1→9.17.0 间类 2924→2956、compose 方法 44→44、外部调用边 1310→1328、指纹 b56b7342…→dafc7376…，两侧 evidence 均为 static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review（E009），因此路径 status 只能逐字保留 static_invoke_observed，不得升级为通过或已适配；story_kotlin 两侧均为 0 类/0 compose 方法/0 外部调用边与空集合指纹 4f53cda1…，status=absent，这只说明该家族桶为空，不表示 Kotlin 侧页面功能消失，实现可能并入 story_native 或其他家族（E009）。类数与调用边同时增长说明确有未解释差异，但预取未给出新增类名与新增边端点；compose 方法计数不变仅说明 Compose 签名集合计数未变，不能据此排除新增 UI 样式，也不能排除新竖屏详情实现落在普通类中。采样边界必须按有界摘录处理：E011 显示同类视图对 comment_compose（声明 2428 类）只返回少量类样本，且 E009 的 limits 标注每家族两个类样本与实际返回数不一致，故此采样边界本身待复核，不能用少量样本代表 2956 类实现。E013/E014 的 home_new_frame 对照（同计数下因字段类型改名 Lap1/b→LVt1/b 与方法体哈希变化而指纹漂移）只能支撑“指纹变化≠新样式”的方法论判断，不能替代 story 家族自身的类级 diff。本页 protocols 为空，KStoryMoss/StoryMoss、KOpusMoss/OpusMoss 等仅出现在未注册协议名单，尚未建立跨家族消费者映射。模块侧 HomeVerticalDetailFeatureInstaller/Routing、StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller/Policy 本轮未读源码，定位字符串、多候选回退与失败兜底均为未知；运行时启用、平板/宽屏布局与服务端 A/B 开关无任何证据。
证据：E009, E011, E013

### 复核页面：mine
mine 页登记 mine_native 与 mine_account_model，复核 E010 与草稿计数一致：mine_native 类 325→326、compose 方法 7→7、外部调用边 92→94、指纹 75f16dab…→f6b18de5…；mine_account_model 类 132→132、compose 方法 0→0、外部调用边 43→43 三项完全不变，仅指纹 2b548e1a…→db7f2792… 变化；两条路径两侧 evidence 均为 static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review，故 status 只能逐字保留 static_invoke_observed，不宣称适配通过。mine_account_model 的差异没有任何计数级或端点级支持，且 E013/E014 显示 home_new_frame 在类数 196、compose 方法 33 完全一致时指纹仍因字段类型改名（Lap1/b→LVt1/b）与方法体哈希变化而不同，说明结构指纹对混淆改名与 DEX 重排敏感，把该变化直接读作“协议或账号模型结构变更”缺乏依据，本报告不采纳该解读（E010、E013、E014）。mine_native 的 +1 类与 +2 边是更实质的差异，但 seed 未给出新增类名或边端点，无法判断是新的组件过滤/VIP 逻辑还是迁移拆分；MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、MineComponentSnapshotStore/QueryClient/HostBridge 等解析点本轮均未读源码，按名解析是否漏挂、是否存在多候选兜底全部未知。本页 protocols 为空，KMineMoss/MineMoss、AccountInterfaceV1Moss/KAccountInterfaceV1Moss、FissionMoss 仅在全局未注册名单中，属候选协议而非已确认消费者，必须靠实际调用边判定。运行时启用、服务端开关、平板/宽屏与登录/未登录差异无证据，整体仍为 installer_and_runtime_validation_required。
证据：E010, E013, E014

- F001 / revised：E011 与 E012 原文支持两点事实：目标侧有界样本 5 类全在 kntr/common/comment/* 且 compose_signatures 为空、字段为 0、方法体为短 getter/Flow；CommentNativeBindingCatalog 只登记 LEGACY/NEXT/EXP3 三个 com.bilibili.app.comment3.* 处理器并要求 CommentItem 字段。但草稿把这两个事实直接对撞成“包迁移导致定位器失配”，属推断过度：该目录作用于原生家族，并不解析 Compose 家族，样本与之不符不构成失配证据；且 5/2428 的有界抽样无法代表 283 个 compose 方法所在类。已修订为“抽样只见数据/富文本层，渲染入口与模块 Compose 桥接的对应未闭合”，并降为 needs_runtime。（E011, E012, E001）
- F002 / revised：F002 的全部数值（compose 3444→…实际为 2444→2428 类、278→283、934→1101；legacy_v2 735→741；native_legacy 211→220；native_next 50→67；native_exp3 62→52）与 E001 目标/基线摘要逐项一致，方向性描述成立，反证点也已写明，故保留核心判断。但草稿中“单一相机家族”为无意义残留短语，且把 5 类有界样本当作跨家族消费者讨论的依据，需修正为“边端点未抽样、跨家族消费者未验证”，避免过度外推。（E001, E011）
- F003 / retained：逐项核对 E002/E016：dynamic_opus 186→226 边、类 1352→1350、compose 方法 92→94；dynamic_compose 1136→1187 类、127→141、221→234；dynamic_legacy 3251→3255 类、105→103、边 2151→2075；协议面 java_moss 134/134、kotlin_moss 382 定义与 26→26 边均不变，草稿数值与摘要一一对应。分析已自陈反证点（dynamic_legacy 桶含 103 个 compose 方法说明家族按包名切分、类可能在桶间迁移；服务端 A/B 静态不可见），recommendation 的类名交集核对与真机 tab/宽屏日志方法具体可执行，level=needs_runtime 与“未读到运行条件”的事实一致，无需改写。（E002, E016）
- F004 / revised：核心断言被证据支持：E003 给出两侧 196 类/33 compose 方法与边 49→52；E013/E014 显示 bubble/d、bubble/e、bubble/f 方法体哈希逐字相同、bubble/s 仅形参顺序互换、dispatchAction$1 仅字段类型 Lap1/b→Vt1/b 改名，可作“指纹漂移可由混淆改名解释”的反例。需修订两处：原文把“模块侧重读失败”写成既成事实（无证据支持失败原因），且未点明模块覆盖仍是 requires_installer_review；改为“本单元未核对定位器源码”，并保留新增边与 bubble/s 哈希差异两个未闭合点。level=candidate 与证据强度相符。（E003, E013, E014）
- F005 / retained：断言与证据相符：E003 显示 home_legacy 由 767 类/204 边变为 766 类/198 边、compose 方法 87 不变，而预取限制为“每族两个类样本”，确无逐边明细，因此“6 条消失边归属未定位、无法区分迁移或分支合并”成立。该条未把缺失写成“无影响”，alternatives 给出可降级与需迁移两种方向，recommendation 的边级配对+真机安装器日志可执行；level=needs_runtime 合理，因功能是否受损最终需安装器命中日志判定。（E003）
- F006 / revised：数值与 E004 双向一致（native 2859→2818、1702→1705；compose 595→614、561→562；两族协议 24/22、52/18 两侧相同），“原生→Compose 迁移”被正确写成候选而非结论。需修订：原文称“协议定义与已解析调用边没有扩张”易被读成搜索协议面整体未变，但 seed 的 unregistered_protocols 仍含 app/search/v2/SearchMoss、KSearchMoss、app/interfaces/v1/SearchMoss 等多条未登记搜索协议，该结论应限定在已登记两族；修订补上该限定并要求先读模块源码、枚举调用方，避免把 22/18 当作覆盖证据。（E004）
- F007 / retained：逐句核对：E012 明确给出 LEGACY/NEXT/EXP3 三个全限定类名、“三个外观实验可在同一个 APK 中共存”“只在安装时解析，不进入逐条绑定热路径”的注释，以及 bindingMethods 先判 CommentItem 类型字段否则 emptyList()、再按非静态/非 bridge/synthetic/void 返回/参数 1..5/isBinding(View 子类字段或 getRoot 返回 View 子类) 过滤的实现；E011 给出 comment_compose 目标侧 2428 类、283 compose 方法、1101 外部调用边、evidence=static_invoke_observed，与草稿引用一致。草稿把“解析失败即静默空列表→漏覆盖”标为推断、把三类存在性缺失标为缺口，并保持 needs_runtime 而非宣称覆盖，未越出 E011/E012。E005 只用于 detail_kotlin_moss 10→38 的调用边变化，引用关系正确。发现归属 detail 页可接受（评论区为详情页子面，E011/E012 随该页证据下发），不另作驳回。（E011, E012, E005）
- F008 / revised：结构性事实均可由 E006 逐项复现（theseus 2276/134/1179 对 2265/131/782、legacy 352/425 对 354/399、两协议 12/3 与 14/7 一致、指纹与 runtime/module_coverage 状态），候选级别与反例条件写法合理，故不驳回、不降级。需两处收紧：(1) 原文用 detail_theseus_united“边减少”作跨页对比，但 E005 不在本发现 evidence_ids 内，属未列证引用；(2) 原文断言 PgcAutoActivityPopupLocator/Policy/FeatureInstaller 是“本期 PGC 唯一相关模块候选”，该结论来自种子 source_files 候选索引，本单元未取得任何 PGC 模块源码工具证据，不能作为事实陈述。修订只改写这两处并明确 E006 为有界摘录，level 保持 candidate。（E006）
- F009 / revised：核心事实被 E007 双侧摘要完整支持：player_kotlin 7→455 类、100→841 外调边、Compose 0→37，player_java 958→953、3222→3308，两侧 MOSS 数值完全一致，指纹两侧均变化。但原 analysis 把“包归属与检测边界调整”当作主要解释并暗示与 Java 侧减少相配，量级上不成立（Java 仅 −5），需补入该不对称限定并显式列入家族检测口径/工具版本、DEX 重排与混淆改名等替代解释；level 保持 candidate 合理（结构变化候选，非新样式结论）。补丁只改 analysis/alternatives/recommendation，不动 page 与 evidence_ids。（E007, E000）
- F010 / revised：事实层被 E008 双侧支持：danmaku_kotlin 57→137 类、Compose 1→3、外调边 8→162，danmaku_kotlin_moss 定义 46 不变而调用边 4→10，danmaku_java_moss 22/20 两侧相同，danmaku_legacy 两侧空集。原 analysis 有两处需收紧：基数很小（基线 8 条边、4 条调用边）使比例被放大，去重/家族边界口径变化足以单独解释；且 E012 是评论页模块源码，只能作方法学对照，不能作为弹幕侧证据。已在补丁中显式标注，level 维持 needs_runtime。（E008, E000, E012）
- F011 / retained：E010 支持事实部分：mine_account_model 类 132→132、compose 方法 0→0、外部调用边 43→43 三项均不变，仅指纹由 2b548e1a… 变为 db7f2792…；mine_native 类 325→326、边 92→94 微增。对照证据 E013/E014 真实存在且数值吻合（home_new_frame 两侧 196 类/33 compose 方法/49→52 边，指纹 4a3e9002…→34c59fa3…，字段类型 Lap1/b→LVt1/b，方法体 sha256 不同），足以支撑“流水线指纹对混淆改名与 DEX 重排敏感，故 structure_or_call_path_changed 标记不能直接等同于结构变更”的推断。分析中已明确区分事实与推断，给出推翻条件（字段签名级 diff 或边端点集合变化），并承认未读 MineVipFeatureInstaller/MineComponentSnapshot* 源码导致解析点依赖未知，未把未读源码外推为 Hook 覆盖结论；level=needs_runtime 与“需真机日志交叉验证”的结论匹配。无需修订。（E010, E013, E014）
- F012 / revised：核心事实与方向判断成立：E009 显示 story_native 类 2924→2956、compose 方法 44→44、外部调用边 1310→1328、指纹变化，story_kotlin 两侧 absent，且明确写了方法定义数与调用边数不同单位、禁止相除推覆盖率，也未把指纹变化写成新样式，level=candidate 合适。但草稿分析中“E011 显示 comment_compose 有 2428 类仍只回两个样本”与实际取证不符：E011 摘录至少返回 5 个类样本，与 E009 的 limits 标注“Two class samples per family”自相矛盾，属采样边界描述错误，需按有界摘录重写，不能以错误样本数支撑“样本不足”的论据。另将影响面表述收紧为“本轮未读安装器源码，按名定位是否漏挂未知”，避免暗示已确认漏挂。其余结论与验证方向保留。（E009, E011, E013）

### 尚未解决的证据缺口

- [1] comment_compose 仅有界读到 5/2428 类且均无 compose_signatures，283 个 compose 方法所在类与模块 CommentComposePurifyBridge/CommentComposeViewAccess 的目标类名未读，Compose 侧 Hook 覆盖保持 unknown。
[2] CommentNativeBindingCatalog 三个 com.bilibili.app.comment3.* 处理器（LEGACY/NEXT/EXP3）在 9.17.0 的 classOf 与 bindingMethods 解析结果未取证，native_legacy/native_next/native_exp3 的 module_coverage 仍为 requires_installer_review。
[3] comment 五家族并存切换条件（legacy_v2/native_legacy/native_next/native_exp3/Compose）、服务端实验位与平板/宽屏分支均未读到运行条件，保持未知。
- [4] comment_kotlin_moss 实际边 26→23 的调用方集合未枚举，无法区分调用点重排与消费方下线。
[5] comment_compose 新增外部边（934→1101）的端点未抽样，跨家族消费者假设未验证。
[6] dynamic_legacy(3255 类) 与 dynamic_compose(1187 类)/dynamic_opus(1350 类) 之间未做类名交集与方法体哈希配对，家族桶间类迁移假设待证。
- [7] 动态页未登记协议（DynamicMoss、KOpusMoss/OpusMoss、KTribeeMoss、CampusMoss、KFeedMoss 等）仍不在登记集合，动态协议面存在覆盖缺口。
[8] DynamicPurifyFeatureInstaller、DynamicPurifyPolicy、DynamicTabsFeatureInstaller、DynamicVideoTabPreference 源码本轮未读取，安装器覆盖与失败兜底未知。
[9] 无真机日志与安装器解析结果，comment/dynamic 八条路径 runtime_enabled 全部保持 unknown，不得改写为已适配或已生效。
- [10] 服务端 A/B 样式开关与实验分组未抓取，静态无结构变化的样式变体仍属不可见风险。
[11] 全部家族指纹变化未做同名类方法体哈希配对，混淆改名/DEX 重排与真实结构变化尚未区分。
[12] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…、repository_head 5422fad1…），本单元结论未逐文件 sha256 绑定。
- [13] 草稿 overview 第二段及 next_steps [9]–[50] 属于 home/search/detail/pgc/player/danmaku/story/mine 等未分配页面，不应计入本单元结论，需在最终报告中剔除。
[14] home_legacy 6 条消失外部调用边（204→198）的调用方与目标签名配对未做，无法判断是迁移出家族、分支合并还是 DEX 重排（E003 仅有族级摘要）。
[15] home_new_frame 3 条新增外部调用边的归属未定位；bubble/s 方法体哈希差异是否只由形参顺序引起，需全量方法体配对确认（E013、E014 仅覆盖 5 个类样本）。
- [16] Home 侧模块源码未核对：HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilter/Banner/TopBar/RecommendPurify Installer、HostHomeCardSpacingHooks，定位点与兜底仍为未知，module_coverage 维持 requires_installer_review。
[17] home 页 protocols 为空，而 seed 的 unregistered_protocols 含 app/home/v1/HomeMoss、KHomeMoss、app/feed/v1/KFeedMoss 等，Home 跨家族协议消费者未评估。
[18] search_native（2859 vs 2818）与 search_compose（595 vs 614）两侧调用边未做边级交叉配对，“原生→Compose 迁移”仍是候选解释。
- [19] search_compose 新增的那 1 个 compose 方法（561→562）及其调用者未定位。
[20] Search 侧模块源码未核对：SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner、KotlinMossChannel、KotlinMossReplyBridge，解析点与兜底未知。
[21] search_java_moss 22 条与 search_kotlin_moss 18 条实际调用边的调用方未枚举，是否存在 Composable 侧第二组消费者未知；禁止据此推导覆盖率。
- [22] 种子 unregistered_protocols 中 app/search/v2/SearchMoss、KSearchMoss、app/interfaces/v1/SearchMoss 等未登记搜索协议未纳入比对，“搜索协议面未变”仅在已登记两族成立。
[23] 两条页面的服务端 A/B 样式开关、平板/宽屏分支与默认样式选择未读到运行条件，home_legacy、home_new_frame、search_native、search_compose 的 runtime_enabled 一律保持 unknown。
[24] home_legacy、search_native、search_compose 未做全量方法体哈希配对，指纹漂移是否纯属混淆改名/DEX 重排只在 home_new_frame 有样本级反例。
- [25] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…、repository_head 5422fad1…），后续模块源码结论须按具体文件 sha256 逐条追溯。
[26] 本单元 fresh_refresh 为空，home/search 的复核依据为预取 E003/E004 与 E013/E014，未额外重新取证；module_source 仅本次会话核对过 comment 侧文件（E012），不覆盖 home/search 定位器。
[27] CommentNativeBindingCatalog 的 LEGACY/NEXT/EXP3 三个全限定类名（comment3.ui.holder / ui.nextholder / ui.nextholderexp3）在 9.17.0 与 9.16.1 中的存在性、CommentItem 字段与方法签名未取证，bindingMethods 是否返回空列表仍为未知；需 decompile_class 按包前缀检索。
- [28] comment_compose 基线侧计数未取（目标 2428 类/283 compose/1101 边），无法判断该类簇是增长、代码迁移还是混淆改名产物，也不能据此推断 Compose 评论样式新增。
[29] detail_legacy 两侧 classes=0 且指纹为 4f53cda1…（空集哈希），是采集空集还是家族判定缺失未核实；不得据此推断旧原生详情样式消失。
[30] detail_theseus_ugc +37 条、detail_theseus_united −58 条外部调用边，以及 pgc_theseus +397 条边、+3 compose 方法的宿主类均未定位；E005/E006/E011 均为有界摘录（每家族两个样本类、协议各四个调用方），方法级对照未做。
- [31] detail_kotlin_moss 调用边 10→38 的 38 条边宿主类未枚举，无法判断 KotlinMossChannel / KotlinMossReplyBridge 是否覆盖新增消费者。
[32] detail_theseus_united 展示层净化与推广位 Hook（DetailUnitedPresentationPurify*/DetailAppPromotion*）、DetailModulePurifyPolicy 登记的模块名与 9.17.0 宿主是否仍一致，未取得模块源码证据（快照 working_tree_dirty=true，需按文件 sha256 追溯）。
[33] PGC 模块侧除种子 source_files 列出的 PgcAutoActivityPopup*/Policy/FeatureInstaller 外无映射证据，且 source_catalog_scope=candidate index only 存在 unmapped_multi_path_candidates，两页 module_coverage 只能维持 requires_installer_review。
- [34] 平板/宽屏等设备形态下 PGC 与详情页实际走 legacy 还是 theseus/united 家族、以及服务端 A/B 开关是否切换家族，静态不可见，未观测。
[35] 两页全部登记路径 runtime_enabled=unknown；缺少 logcat 中 FeatureInstallResult 的 installed/complete 与 CommentFamilyCoverage per-family 结果，“安装成功”与“运行生效”仍未区分。
[36] detail_java_moss（32/35）与 detail_kotlin_moss（76 定义）的定义数不变而调用边变化，跨家族消费者（评论区/动态页共同协议）是否存在未逐一确认。
- [37] 本单元 fresh_refresh 为空，复核阶段未能独立再取证，E007/E008 使用的是首条消息下发的预取视图（每家族两例类样本、每协议四例调用者、runtime unknown），未按全量结构重读；引用满足“已有证据可复核”，但不构成全量覆盖。
[38] player_kotlin 由 7 类→455 类的类级配对未做：仅目标侧存在的类清单、父类与 compose_signatures 分布、同名类 method_bodies_sha256 比对均缺失，无法区分“新纳入包/检测口径变化”“真实代码迁移”“混淆改名/DEX 重排”。
[39] player_java 基线存在而目标缺失的 5 个类未列出，无法判断是否命中模块播放侧 locator/installer 目标类；PlayBufferLocator、PlayerSpeedLocator、PlayerCapabilityAccess、SponsorPlayerLocator 等正文未读，解析点与兜底未知。
- [40] 播放页分区、小窗、横屏/平板宽屏与服务端开关注入点均未读到运行条件；两路径 runtime_enabled=unknown、module_coverage=requires_installer_review 保持原样，无任何真机日志。
[41] danmaku_kotlin_moss 4→10 的 6 条新增边 callee 签名与 owner 未逐条核对，弹幕消费点与评论 reply 消费点未区分；danmaku_kotlin 家族检测口径是否与基线一致未确认。
[42] danmaku_legacy 在两侧均为 absent 且指纹为同一空集常量，真机类加载列表未取证，旧弹幕渲染是否由未归类类承担、模块是否仍存在指向 legacy 类名的解析分支均未知。
- [43] DanmakuPurifyFeatureInstaller.kt / DanmakuPurifyPolicy.kt 正文未读，净化安装器解析点、覆盖率分母与兜底未知；danmaku 页 module_coverage 无法更新。
[44] 服务端 A/B 与实验分桶对 player/danmaku 的影响无法静态观测，本轮不宣称任何样式已穷尽，也不宣称适配通过。
[45] 源码快照 working_tree_dirty=true、source_tree_sha256=37745f8f…、repository_head=5422fad1…；本轮所有模块侧结论均为未读或按清单推断，后续须绑定到具体文件 sha256 追溯，不得依赖工作树状态。
- [46] mine_native 的 +1 类与 +2 条外部调用边尚无类名/端点：需导出双侧完整类名与方法签名 diff，并与调用边端点对齐后才能判断是新逻辑还是迁移拆分。
[47] mine_account_model 字段与方法签名级完整 diff 未做：E010 只说 132/0/43 不变、指纹变化，字段增删与类型变更仍需全量比对，不能仅凭两个类样本判定“仅改名”。
[48] AccountInterfaceV1Moss/KAccountInterfaceV1Moss/KMineMoss/FissionMoss 仅在未注册协议名单中，未做 protocol_evidence，跨家族消费者与实际调用边仍未知，不能断言账号模型无影响。
- [49] MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、MineComponentSnapshot* 与 HostMineReadingCard 本轮未读源码，定位字符串、多候选解析与失败兜底均未知；源码快照 working_tree_dirty=true，后续引用须按文件 sha256（如 E012 展示的 sha256 形态）追溯。
[50] story_native 的 +32 类与 +18 条外部调用边端点未给出，新增类职责（竖屏详情/Story 样式/桥接）未确认，compose 方法数不变不能排除新增 UI 样式。
[51] HomeVerticalDetailFeatureInstaller/Routing、StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller/Policy、PlayerStoryFreeDataPromotionAccess 本轮未读，story 页 module_coverage 仍为 requires_installer_review，不存在已确认的 Hook 覆盖结论。
- [52] E009 的 limits 标注“每家族两个类样本”与 E011 实际返回多个类样本（comment_compose 声明 2428 类）不一致，采样上界口径需澄清后再评估样本代表性，否则任何“抽样代表整套实现”的推断都无效。
[53] story_kotlin 的 absent 只表示该家族桶为空，Kotlin/新实现是否并入 story_native 或其他家族、或由服务端开关控制，尚未按代码特征（StoryMoss 消费端、竖屏详情路由入口）全量检索。
[54] 两条页面的 runtime_enabled 全为 unknown：缺少 9.17.0 真机 Hook 命中日志、FeatureInstallResult installed/complete 与家族覆盖率输出，不得推断运行时启用。
- [55] 平板/宽屏布局、登录/未登录状态与服务端实验分组对 story/mine 的结构性与视觉差异无任何证据，静态不可见的 A/B 变体不能宣称已穷尽。
[56] E012（CommentNativeBindingCatalog 硬编码 comment3.* 处理器类名）属于 comment 页证据，与本单元 story/mine 无直接映射，不能借其推断 story/mine 的安装器覆盖。

## 下一步

- [1] 真机探针：对 CommentNativeBindingCatalog 的 LEGACY/NEXT/EXP3 三类打印 classOf 结果、CommentItem 字段命中数与 bindingMethods 数量，回填 comment 侧 installer 覆盖。
[2] 真机进入评论区，分别在 legacy_v2 / native_legacy / native_next / native_exp3 / Compose 五个实验位下记录实际渲染家族与 CommentFamilyCoverage.describe() 输出，确认并存栈的切换条件。
[3] 用 decompile_class 读取 CommentNextContentRichTextHandler 与 CommentNextExperiment3ContentRichTextHandler 的方法签名，与基线同名文件比对，判断 next 边 +34%、exp3 边 -16% 是新增入口还是裁剪。
[4] 对 E011 中的 kntr/common/comment/common/service/g 用 decompile_class 读取 Flow 方法体，确认谁是评论数据消费者，判定其是否为 Compose 渲染入口。
[5] 动态页：交叉抽样 dynamic_legacy 减少类与 dynamic_compose/dynamic_opus 新增类，确认是否存在家族桶间类迁移。
- [6] 动态页真机在关注/推荐/Opus 详情页分别抓 DynamicPurifyFeatureInstaller 与 DynamicTabsFeatureInstaller 安装日志，验证净化与 tab 偏好在三家族上的实际生效情况。
[7] 补充抓取评论区与动态页服务端样式开关（若可读），以区分结构变化与 A/B 分桶；静态不可见部分在报告中保持 unknown。
[8] 复核阶段：核对本轮所有指纹变化是否可由混淆改名/DEX 重排解释，避免把结构哈希变化写成新样式结论。
[9] 重跑 home_new_frame 两侧全量类配对，输出未配对类、未配对字段与方法体哈希差异清单，判定指纹漂移是否为混淆改名
[10] 导出 home_legacy 两侧完整外部调用边（204 vs 198）并做目标签名配对，定位消失的 6 条边
- [11] 导出 search_native（2859 vs 2818）与 search_compose（595 vs 614）两侧调用边并交叉配对，确认是否存在跨家族消费者迁移
[12] 补读 SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchPurifyFeatureInstaller、SearchDefaultWordsCleaner 源码，核实定位点与兜底路径（源文件哈希需按 working_tree_dirty 追溯）
[13] 补读 HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilterFeatureInstaller、HomeBannerFeatureInstaller、HomeTopBarFeatureInstaller 源码，核实对新形态的定位与兜底
[14] 核对 search_java_moss / search_kotlin_moss 的 22 与 18 条实际调用边调用方，确认是否存在 Composable 侧消费者（不推导覆盖率）
[15] 真机 9.17.0 分别在原生与 Compose 样式进入搜索页，记录清理功能命中日志与默认样式判定
- [16] 真机 9.17.0 验证 Home 页 Bubble、动作分发、组件过滤与横幅植入的实际命中与失败计数
[17] 采集服务端样式开关/实验分组记录，区分静态不可见的 A/B 变体与真实结构变化
[18] 用 decompile_class 检索 comment3 的 holder / nextholder / nextholderexp3 三个包前缀，输出命中类、CommentItem 字段与方法签名，判定 CommentNativeBindingCatalog 是否会返回空列表。
[19] 枚举 detail_kotlin_moss 的 38 条实际调用边宿主类（基线 10 条），与 KotlinMossChannel/KotlinMossReplyBridge 的注册点比对，确认新增消费者是否被覆盖。
[20] 对 detail_theseus_ugc / detail_theseus_united 各抽样同名类做方法体哈希与方法级对照，定位 ugc +37、united -58 条调用边变化的宿主类。
- [21] 用 decompile_class 按 PgcAutoActivityPopupLocator/Policy 登记的目标类名在 9.17.0 重解析，记录命中/缺失与签名差异。
[22] 对 pgc_legacy（354→352 类）与 pgc_theseus（类 +11、边 +397）做方法级对照，排除混淆改名、DEX 重排与内联造成的指纹变化。
[23] 真机小屏与平板/宽屏分别打开普通详情页与 PGC 详情/播放页，记录实际生效家族（legacy / theseus / united）与服务端开关差异。
[24] 抓取 logcat 中 FeatureInstallResult 的 installed/complete 与 CommentFamilyCoverage 的 per-family 状态，区分“安装成功”与“运行时生效”。
[25] 触发 PGC 活动弹窗并记录 Locator 命中的类与方法签名，确认弹窗自动关闭是否仍生效。
- [26] 核实 detail_legacy 在两侧 classes=0 的采集口径，确认 4f53cda1… 是家族判定缺失还是真实无类，不以 absent 推断旧原生样式消失。
[27] 把库存源码中的 PGC 相关 Hook（除 PgcAutoActivityPopup* 外）补入映射，消除 source_catalog_scope=candidate index only 带来的覆盖盲区。
[28] 在报告中固定记录源码快照 37745f8f…、repository_head 5422fad1… 与 working_tree_dirty=true，后续结论须按文件哈希追溯而非依赖工作树状态。
[29] 复核完成后对每条登记路径保留 runtime_enabled=unknown，直到有真机日志或安装器解析结果支撑启用判定。
[30] 按类名交集重读 family_evidence(player_kotlin, target/baseline)，输出仅在目标侧存在的类清单、父类与 compose_signatures 分布，并比对同名类 method_bodies_sha256，判定跃迁是代码迁移还是新样式。
- [31] 重读 family_evidence(player_java) 找出基线存在而目标缺失的 5 个类，核查是否为模块播放侧 locator/installer 的目标类，并确认替代落点。
[32] 重读 protocol_evidence(danmaku_kotlin_moss, target)，核对 4→10 中新增 6 条调用边的 callee 签名与 owner，区分弹幕消费点与评论 reply 消费点。
[33] 真机 9.17.0 播放页分层验证：Feed 详情、PGC、小窗、横屏与平板宽屏各跑一轮，记录类加载与模块 locator 解析成功/失败，失败项保留在分母。
[34] 真机弹幕净化开关对照验证：开启/关闭、登录/未登录、实验分组/默认分组四组合，记录 DanmakuPurifyFeatureInstaller 安装结果与 complete 标志。
[35] 读取 DanmakuPurifyFeatureInstaller.kt 与 DanmakuPurifyPolicy.kt 正文（按快照文件哈希追溯），确认解析点、并存栈处理与兜底，再更新 danmaku_kotlin 的 module_coverage。
- [36] 读取 PlayerSpeedLocator.kt、PlayerBufferLocator.kt、PlayerCapabilityAccess.kt 正文，核对目标签名是否覆盖 9.17.0 新增 Compose 承载控件，避免据类存在推定 Hook 覆盖。
[37] 核查模块中是否仍存在指向 danmaku_legacy 类名的解析分支，以及该类名在真机类加载中是否存在，避免将 absent 解读为功能消失。
[38] 用服务端实验分组对照采样，确认 player/danmaku 的差异是否由开关下发引起；静态无结构变化的样式必须记为未知而非已穷尽。
[39] 记录 source 快照 working_tree_dirty=true 与 source_tree_sha256，把每条模块源码结论绑定到具体文件 sha256，复核阶段逐条回溯。
[40] 把本单元两条重点发现的状态保留为 candidate / needs_runtime，待真机日志出现后再决定是否升级结论，不得直接改写为适配通过。
- [41] 对 story_native 与 mine_native 分别取双侧完整类名、方法签名 diff，输出新增/删除/改名三张清单，定位 +32（story）与 +1（mine）的具体类
[42] 把 story_native +18、mine_native +2 条外部调用边的源/目标端点对齐，判断新边是否落在新增类上
[43] 对 story 新增类与 mine 新增类用 decompile_class 读方法体，确认职责（竖屏详情/Story 样式 vs 组件过滤/VIP）
[44] 用 module_source 读 HomeVerticalDetailFeatureInstaller、HomeVerticalDetailRouting、StoryPurifyFeatureInstaller，确认定位字符串是否覆盖 9.17.0 新增类及失败兜底
[45] 用 module_source 读 MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、MineComponentSnapshotStore/QueryClient，确认是否存在可迁移的多候选解析
- [46] 对 AccountInterfaceV1Moss、KMineMoss、KStoryMoss、KOpusMoss 做 protocol_evidence，确认实际调用边与跨家族消费方，区分候选协议与已确认消费者
[47] 对 mine_account_model 取字段级 diff，排除“指纹变化=结构变化”的误判
[48] 真机 9.17.0 验证：分别进入竖屏详情/Story 入口与“我的”页，记录 Hook 命中与未命中项，覆盖平板/宽屏与登录/未登录两种状态
[49] 记录服务端开关无法静态观测的缺口，用同账号在不同实验分组下对比页面结构，确认是否存在静态不可见的样式变体
[50] 复核源码快照 working_tree_dirty=true 的影响：按文件 sha256 固定本轮引用的模块源码版本，避免引用未提交改动