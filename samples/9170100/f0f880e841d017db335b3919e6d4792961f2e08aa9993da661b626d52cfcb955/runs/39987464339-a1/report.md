## 模块源码快照

- 来源：published
- 捕获时间（UTC）：2026-10-15T14:19:32.431433Z
- 源码 HEAD：5422fad1e3f798252619d610a0504573ff47211b
- 快照 SHA-256：2fa2d3b70f73fa431ed83267a9519c726a41b67de39eb7ee785813de39067120
- 源码树 SHA-256：37745f8f27c41c22eab6e0bc780c6af700d650f49c3f004f862bf9c5f1548a5c
- 含未提交修改：True
- 时效状态：published_unverified_worktree

复用历史静态证据 run 39983150017；本轮只重新执行 AI 审查。模块源码重新绑定到上述快照。

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

本单元覆盖 tv.danmaku.bili 9.17.0（f0f880e8…）相对 9.16.1（41efb1c9…）的评论区与动态页八个登记家族。两侧全部家族均为 static_invoke_observed、runtime_enabled=unknown、module_coverage=requires_installer_review，prefetch 也标明 complete_coverage=false，因此本报告只登记静态调用存在与结构变化，不作适配结论。评论区五个家族（legacy_v2、native_legacy、native_next、native_exp3、compose）签名全部变化；其中 comment_compose 方法数 278→283、compose_methods 278→283 区间的 283 与外部调用边 934→1101（+167）是本页最大结构变化，而 comment_native_exp3 是唯一类数（58→54）与外部边（62→52）同时缩减的家族，方向相反需要单独核对。动态页三家族 signature 全变：dynamic_legacy 外部边 2075（-76），dynamic_compose 类数 1136→1187、compose_methods 127→141、外部边 221→234，dynamic_opus 类数 1352→1350 基本持平但外部边 186→226（+40）。两条 MOSS 协议定义数两侧完全一致（comment java 50/kotlin 130、dynamic java 134/kotlin 382），只有 kotlin_moss 实际调用边上 comment 26→23 下降、dynamic 保持 26，说明协议层不是本轮变化主因。关键深挖结论：Compose 评论自由复制依赖混淆字段名单点解析（E013），原生三外观目录把 handler 全限定名写死（E014）；两者在签名全变的情况下都可能静默降级为 Skipped/partial，而不是崩溃。运行时启用、安装器覆盖与真机生效均未验证。

本单元仅覆盖 home、search 两页四条登记路径，样本 9.17.0(9170100) 对基线 9.16.1(9161100)，同签名同仓库。四条路径证据值均为 static_invoke_observed，runtime_enabled 与 module_coverage 分别为 unknown 与 requires_installer_review，故不存在任一路径的适配结论。home 两家族 fingerprint 均变化，规模基本持平（legacy 767→766 类、204→198 边；new_frame 196 类不变、49→52 边），但预取 E003 只有家族摘要，没有落到 home 的具体类样本与方法体，无法区分结构变化与混淆改名/DEX 重排。search 两家族 fingerprint 亦变化（native 1702→1705 类、2859→2818 边；compose 561→562 compose 方法、595→614 边），search_java_moss 24/22 与 search_kotlin_moss 52/18 与基线计数相同，但定义数与调用边数不是同一单位，不能推算覆盖率。模块侧源码快照 working_tree_dirty，按文件哈希追溯，未读到的定位器/安装器匹配逻辑一律记为未知。

本单元复核 detail（详情）与 pgc（番剧/影视）两页，共 5 条登记路径。对比 9.16.1→9.17.0：detail_legacy 两侧均 absent（结构性缺席，不等于页面功能消失）；detail_theseus_ugc 类 1946→1975、外调用边 510→547、Compose 25→25；detail_theseus_united 类 4581→4633、边 4257→4199、Compose 99→98；pgc_legacy 类 354→352、边 399→425；pgc_theseus 类 2265→2276、Compose 131→134、边 782→1179。五条路径指纹全部变化，但指纹变化本身不构成新样式证据，需先排除混淆改名、DEX 重排与编译器变化。detail_kotlin_moss 定义数 76 不变而实际调用边 10→38，是本次最值得深挖的跨家族消费者增长信号；pgc 两个协议定义与调用边完全未变。所有路径 runtime_enabled 均为 unknown，module_coverage 均为 requires_installer_review，源码快照 working_tree_dirty=true，结论只能停在静态观察，不宣称适配通过。

本单元只提交 player 与 danmaku 两页共四个登记路径。9.17.0 相对 9.16.1 出现三处登记变化：player_kotlin 类数 7→455、Compose 方法 0→37，player_java 类数 958→953 而外部调用边 3222→3308，danmaku_kotlin 类数 57→137、外部边 8→162。两侧播放器与弹幕的 MOSS 定义数完全一致（player_java 18 / player_kotlin 34 / danmaku_java 22 / danmaku_kotlin 46），说明协议层未见变化，家族结构变化更可能来自归类口径、DEX 重排、Kotlin/Compose 迁移或调用方增加，而非新样式确认。danmaku_legacy 两版均为 absent（0 类 0 边、指纹相同），不能据此推断弹幕功能消失。四个路径 runtime_enabled 全部未知、complete_coverage=false、module_coverage=requires_installer_review，本报告只给候选结论与补证任务，不宣称适配通过。

本单元仅提交 story、mine 两页共 4 条登记路径（E000 指派）。story_native、mine_native、mine_account_model 三条路径为目标侧 static_invoke_observed，story_kotlin 在基线与目标两侧均为 absent。两页 complete_coverage 均为 false，runtime_enabled 全为 unknown，module_coverage 全为 requires_installer_review，故本报告只给静态变化与待验证假设，不构成适配结论。变化类型全部是 structure_or_call_path_changed：story_native 类数 +32、外部调用边 +18 而 Compose 方法数不变；mine_native +1 类/+2 边；mine_account_model 三类计数完全一致（132/0/43）但结构哈希变化，优先按混淆改名或方法体变化处理，不作为新样式候选。协议层无已登记证据：StoryMoss/KStoryMoss、MineMoss/KMineMoss 均落在未登记清单（E000），跨家族消费者与共同协议调用边缺失；sample 变更还含 7121 个资源变更/15 个新增资源，重排与重编译是必须排除的替代解释。APK 访问已禁用，本轮只依据冻结静态证据与固定源码快照（working_tree_dirty=true）。

## 各页面评估

### comment

评论区五条路径并存且签名全部变化，静态矩阵中 legacy_v2（583 类/741 边）、native_legacy（181/220）、native_next（48/67）、native_exp3（54/52）、compose（2428 类/283 compose 方法/1101 边）都仍可见实际调用边，说明旧/新原生与 Compose 四类实现未被单点替代，属并存栈而非替换（E001）。变化方向分裂：compose 外部边 934→1101（+167），是唯一显著增长者；native_next 边 50→67（+17）而类数仅 +3；native_exp3 类数 58→54、边 62→52 双双回落，是唯一缩减家族；legacy_v2 类数 +4、边 +6，接近噪声量级。协议侧 comment_java_moss 定义 50/边 50 侧完全一致，comment_kotlin_moss 定义 130 未变但实际调用边 26→23 下降，说明 MOSS 协议未新增样式，下降的 3 条边可能来自调用方迁移或被 Compose 路径吸收，但未逐条比对调用者，仍属未知。模块侧有三处可直接影响本页的静态脆弱点：CommentComposeCopyBridge 中 ComposeCommentText.resolve 以混淆字段名 a/i/j/k/o/p/b/c 加枚举常量集合 {ORIGIN,TRANSLATING,TRANSLATION} 单点匹配模型（E013）；CommentNativeBindingCatalog 把三个 handler 全限定名以常量写死并要求类内存在 CommentItem 字段与 View 型绑定参数（E014）；CommentFamilyCoverage 明确把未注册方法留在分母，partial 与 missing 不会升级为 ok（E014）。因此即使类仍存在，方法解析失败会表现为功能静默缺失。prefetch 每家族仅给两份类样本，不足以代表整套实现；安装器覆盖、切换条件、平板/宽屏布局、服务端开关对样式选择的影响均未读到运行条件，记为未知。

证据：E001, E011, E013, E014

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类数 579→583、外部调用边 735→741，签名 b8b8915c… 与基线 8d381d51… 不同；增量接近噪声量级，未区分新增调用还是混淆重排。
- 可能影响：旧版 V2 评论路径静态仍存在调用边；若模块在该路径上有孤儿绑定（无新增注册），会表现为该家族覆盖 partial 而非整体失效，影响面取决于未读的 Locator 实现。
- 验证：反编译比对 9.16.1/9.17.0 中该家族的类清单与方法体哈希，确认 6 条新增边的具体调用者与首帧渲染方法是否同名同签名；真机上开启模块后在旧版 V2 入口复现长按复制与净化。
- 证据：E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类数 172→181、外部边 211→220，签名 86f3175b… 变化；CommentNativeBindingCatalog.LEGACY 常量指向的 CommentContentRichTextHandler 仍需按名确认是否仍在该包。
- 可能影响：原生旧外观的正文绑定方法可能被新增包装层吸收；若 handler 改名或移包，catalog 的 bindingMethods 会返回空列表，覆盖率记 missing。
- 验证：用 JADX 按名重读 com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler，核对是否仍有 CommentItem 字段与 1..5 参数的 View 型绑定方法；真机在原生旧外观视频评论区分页验证文字复制与净化是否生效。
- 证据：E001, E014

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类数 45→48、外部边 50→67（+17，增幅明显高于类数增幅），签名 4a3fda7a… 变化，提示新增调用方而非单纯类合并。
- 可能影响：Next 外观调用边显著增密，绑定/分发入口可能新增一层包装；模块对 CommentNextContentRichTextHandler 的按名解析若只覆盖旧入口，新增调用边的位置会漏挂。
- 验证：列出该家族新增 17 条外部边的调用方类，逐条判断是否落在 catalog 预期的绑定方法集合内；真机切换 Next 实验外观后验证复制、净化与回复按钮三条 Hook 是否同时生效。
- 证据：E001, E014

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类数 58→54（-4）、外部边 62→52（-10），是五家族中唯一双缩减者，签名 0b5098d4… 变化。
- 可能影响：该外观可能被降级、合并进 next，或其中一部分类被迁移；若 CommentNextExperiment3ContentRichTextHandler 未随之调整，exp3 家族会记 missing。需注意 class 减少不等于页面功能消失。
- 验证：反编译确认 exp3 包下 4 个消失类是否出现在 next/legacy 包中（迁移）或整体删除；真机在实验外观入口确认 exp3 是否仍可被服务端下发，并抓取模块日志中 CommentFamilyCoverage 的 exp3= 值。
- 证据：E001, E014

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类数 2444→2428（减少），但 compose_methods 278→283、外部边 934→1101（+167，约 +17.9%），签名 089904c2… 变化；同一时期类数下降与边数大幅增长并存，提示方法体/调用路径重构而非样式新增。
- 可能影响：Compose 评论仍是本页方法级变化最大的路径。模块 ComposeCommentText.resolve 用混淆字段名 a/i/j/k/o/p/b/c 与枚举集合单点匹配（E013），字段若被重排会静默返回 missing-text-shape，导致自由复制/净化在 Compose 评论全量失效但不报错；同时 dispatch 定位依赖参数类型内唯一含 actionClass 子类消费方法的字段，类型层新增字段会触发 ambiguous-more-action。
- 验证：按名重读 kntr/common/comment 模型类，核对 a(Long)/i(枚举)/j、k、o、p(同型富文本)/b、c(Long) 是否仍成立、枚举是否仍恰为 ORIGIN/TRANSLATING/TRANSLATION；再确认 1101 条边中新增部分的调用方是否落在 renderer 静态性校验（modelIndex≥0 且带 Composer 参数）覆盖范围内；真机在 Compose 评论页长按验证复制菜单与净化开关。
- 证据：E001, E011, E013

### dynamic

动态三条路径签名全部变化，且三家族变化方向互不相同，属并存栈的多点移动而非单一路径替换（E002）。dynamic_legacy 类数 3251→3255 基本持平，但外部调用边 2151→2075（-76，约 -3.5%），compose_methods 105→103 略降，说明旧动态路径的调用被削薄；dynamic_compose 从 1136→1187 类、compose_methods 127→141、外部边 221→234，是唯一在类数与方法数上同时扩张且 compose_methods 净增 14 的家族，与评论区 compose 扩张方向一致；dynamic_opus 类数 1352→1350 几乎不动，但外部边 186→226（+40，约 +21.5%），compose_methods 92→94 微增，属“结构不变、调用关系显著增密”，是动态页最需要单独解释的一项。深挖 opus 家族样本只拿到 kntr/app/following/opusDetail/api 下的 api 层类：数据容器、ImmutableSet 构造、以及 CompositeExternalInterceptor 的协程 ContinuationImpl 子类，均无 compose_signatures（E012）。这意味着 Opus 页面存在以协程拦截器/Map 组装构成的非 Compose 中间层，模块若只挂在渲染/Text 层，可能位于这条拦截链之后或之外，实际生效顺序未知。协议侧 dynamic_java_moss 定义 134/边 134、dynamic_kotlin_moss 定义 382/边 26，两侧完全一致，说明本轮动态变化不来自 MOSS 协议增删；但 unregistered_protocols 中仍含 app/dynamic/v1/DynamicMoss、v2/KOpusMoss、OpusMoss、dynamic/interfaces/feed/FeedMoss 等未登记项，是否存在未登记的跨家族消费者无法静态排除。DynamicPurifyFeatureInstaller / DynamicTabsFeatureInstaller / KotlinDynamicMossWatch 源码未在本轮读取，故模块侧定位器对上述调用边增密的覆盖记为未知，需补证。prefetch 每家族仅两份类样本，不能代表 1350 类整体；服务端 A/B 无结构变化不可见。

证据：E002, E012

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类数 3251→3255、外部边 2151→2075（-76）、compose_methods 105→103，签名 494b6f4a… 与基线 a02ef6a4… 不同；类数几乎不变而边数下降，方向与 compose/opus 相反。
- 可能影响：旧动态路径仍是最多调用边的家族，但削薄可能意味着部分子路径被迁移到其他实现；模块若在 legacy 上以“类存在”判定适配，会高估覆盖（CommentFamilyCoverage 式的 partial 语义同理适用于动态侧）。
- 验证：按名重读旧动态家族的类与方法体哈希，定位 76 条消失边的原调用方类别，判断是否指向评论/转发/正文渲染的 Hook 锚点；真机在旧版动态流与动态详情分别验证净化与富文本长按。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类数 1136→1187（+51）、compose_methods 127→141（+14）、外部边 221→234（+13），签名 d1bf0fee… 变化；是动态三家族中唯一类数和 Compose 方法数同时扩张者。
- 可能影响：动态页 Compose 实现体量增长，若模块仅以固定类名/固定方法名点位注册，新增的 14 个 Compose 方法不会被覆盖，覆盖率停在 partial；同时类数增长也可能只是 DEX 重排或包装层，需排除后才能称为新样式。
- 验证：对比两侧该类家族的类清单，区分新增类是真新增还是既有类拆分/改名；抽查新增 14 个 Compose 方法的参数中是否出现与评论区 ComposeCommentText 同形的富文本模型（字段 a/i/j/k）；真机在 Compose 动态流触发长按复制与净化。
- 证据：E002, E013

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类数 1352→1350、compose_methods 92→94 基本持平，但外部边 186→226（+40，约 +21.5%），签名 60096774… 变化；属结构稳定、调用关系增密。
- 可能影响：Opus 页面静态仍在活跃调用，新增 40 条边集中在非 Compose 的 api/拦截器层（样本见 CompositeExternalInterceptor、ImmutableSet 构造与 Function1 Map 组装，E012），说明 Opus 数据在进入渲染前有独立装配链；模块若命中渲染层则语义仍在，但 Opus 特有的图文/统计字段净化可能完全未被这条链覆盖。
- 验证：列出新增 40 条边中真实调用 kntr/app/following/opusDetail/api 的调用方，确认其上游是 Opus 详情页还是动态流内嵌卡片；按名重读 kntr/app/following/opusDetail 与 KOpusMoss 消费者，核对模块是否存在对应解析点；真机打开单条 Opus 详情页验证富文本复制与净化。
- 证据：E002, E012

### home

登记路径 home_legacy 与 home_new_frame 均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，本页无任何可验证的启用或覆盖结论。相对基线 9.16.1：home_legacy 类数 767→766、compose 方法 87→87、外部调用边 204→198、fingerprint 由 7a842bbb… 变为 a56da1e1…；home_new_frame 类数 196→196、compose 方法 33→33、外部调用边 49→52、fingerprint 由 4a3e9002… 变为 34c59fa3…。两条路径规模近似持平而哈希双变，符合“结构或调用路径变化”的登记语义，但也与混淆改名、DEX 重排、编译器版本变化的典型表现重合，预取 E003 未给出 home 家族的类样本，因此不能宣称出现新样式或旧样式消失。home 家族 protocols 为空，服务端开关驱动的样式差异可能静态完全不可见。模块候选中 HomeFrameListHook、HomeFrameTabLocator、HomeBannerFeatureInstaller、HomeComponentFilterFeatureInstaller、HostHomeCardSpacingHooks、HomeRecommendPurifyFeatureInstaller 等分别依赖帧 Tab 定位、Banner 与卡片过滤、卡片间距等定位点，其匹配条件本轮未读取，不能由“类存在/fingerprint 变化”推断 Hook 生效。最小补证：按 family 取 home 具体类，做 target 与 baseline 方法体哈希比对，并读 HomeFrameTabLocator 与 HomeFrameListHook 的定位条件；真机在首页逐开关（顶部栏、Banner、推荐净化、Tab 过滤、卡片间距）观察命中日志，并覆盖平板/宽屏。

证据：E003, E000

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类数 767→766、compose 方法 87 不变、外部调用边 204→198，fingerprint 7a842bbb…→a56da1e1…；规模微缩而哈希变化，性质（真实结构变化或改名/重排）未定。
- 可能影响：legacy 首页帧内的 HomeFrameListHook、HomeBannerFeatureInstaller、HomeRecommendPurifyFeatureInstaller、HomeTabFilterFeatureInstaller 等定位点可能失配或落到不同类上；实际匹配条件未读源码，影响范围未知。
- 验证：用 family_evidence(home_legacy) 取具名类并在 baseline 侧比对方法体哈希；JADX 读 HomeFrameTabLocator/HomeFrameListHook 的类与方法匹配条件；真机在首页逐功能开关记录命中与未命中日志。
- 证据：E003, E000

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 196 不变、compose 方法 33 不变、外部调用边 49→52，fingerprint 4a3e9002…→34c59fa3…；调用边小幅增加，可能新增外部消费者或仅为重排。
- 可能影响：HomeFrameTabLocator、HomeComponentFilterFeatureInstaller、HostHomeCardSpacingHooks 面向新帧的定位与间距 Hook 可能出现部分命中；新增 3 条调用边的实际调用方未知。
- 验证：对新帧家族抽样类做方法体哈希比对并列出新增调用边来源；读 HomeFrameTabLocator 与 HostHomeCardSpacingHooks 定位条件；真机验证宽屏/平板下新帧 Tab 与卡片间距是否仍被处理。
- 证据：E003, E000

### search

登记路径 search_native 与 search_compose 均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review。相对基线 9.16.1：search_native 类数 1702→1705、compose 方法 2→2、外部调用边 2859→2818、fingerprint 28a11ecd…→28e67919…；search_compose 类数 3141→3146、compose 方法 561→562、外部调用边 595→614、fingerprint fcde68da…→4e4c7892…。原生侧调用边减少 41 而类数增加 3，Compose 侧 compose 方法仅 +1 而调用边 +19，两个方向不一致，既可能是界面栈调整，也可能是编译器与 DEX 布局变化，静态层面无法判定“新搜索样式”成立。协议登记 search_java_moss 24 定义/22 调用边、search_kotlin_moss 52 定义/18 调用边，与基线完全相同；但没有跨家族消费者清单与逐协议调用者样本，且定义数与调用边数不是同一单位，禁止相除推导覆盖率。seed 的 unregistered_protocols 中仍有多条 SearchMoss 相关协议（app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss 等），说明搜索数据面存在未登记通道，默认词、热搜、搜索首页推荐是否复用已登记协议无法静态确认。模块侧 SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller、SearchHomeRecommendPolicy 与 SearchHomeRecommendLocator 的解析目标本轮未读取，不推断 Hook 覆盖。最小补证：取两家族具名类做基线比对，读 locator 的类名/字段匹配条件，真机观察搜索页默认词与推荐卡片。

证据：E004, E000

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数 1702→1705、compose 方法保持 2、外部调用边 2859→2818（减少 41），fingerprint 28a11ecd…→28e67919…；类增边减，重排与迁移均可解释。
- 可能影响：SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller 依赖的原生搜索数据/视图定位点可能在新增类中被重包装，或调用边被移入未登记协议通道；具体影响未知。
- 验证：family_evidence(search_native, baseline) 抽样类方法体比对；protocol_evidence 读 search_java_moss 调用者并区分其是否被 Kotlin 侧消费；module_source 读 SearchDefaultWordsCleaner 与 SearchPurifyFeatureInstaller 的匹配条件；真机验证默认词与净化效果。
- 证据：E004, E000

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数 3141→3146、compose 方法 561→562、外部调用边 595→614，fingerprint fcde68da…→4e4c7892…；compose 方法增量与调用边增量不成比例，需排除编译器/重组因素。
- 可能影响：SearchHomeRecommendFeatureInstaller 与 SearchHomeRecommendPolicy 面向的搜索首页推荐 Compose 卡片可能仍存在但宿主类名或层级变动；SearchHomeRecommendLocator 定位是否仍命中未知。
- 验证：取 search_compose 家族类样本与基线比对 compose 签名差异；module_source 读 SearchHomeRecommendLocator 与 SearchHomeRecommendPolicy 的定位/兜底分支；真机对比开启与关闭时搜索首页推荐卡片。
- 证据：E004, E000

### detail

详情页三条路径分化明显。detail_legacy 在 9.17.0 与 9.16.1 两侧均为 absent（0 类/0 边），只能说明静态特征未命中，不能说明旧原生详情已消失。detail_theseus_ugc 呈小幅结构扩张：类 +29、外部调用边 +37、Compose 方法数持平 25，指纹 aba2db…（基线 672508…）。detail_theseus_united 出现反向组合：类 +52 而外部调用边 -58、Compose 99→98，指纹 56c25b…（基线 b0f0b0…）。类增长与边下降同时出现，更像是调用解析粒度、内联/包装层或 DEX 排布变化，而不是“样式收敛”。协议侧 detail_java_moss 定义 32、边 35 与基线完全一致；detail_kotlin_moss 定义 76 不变但实际调用边 10→38，说明协议契约没变、消费者或调用点增多，属于跨家族传播面变化而非新协议。模块侧冻结源码包含 DetailAppPromotionFeatureInstaller、DetailModulePurify*、DetailUnitedModulePurify*、DetailUnitedPresentationPurify*、DetailViewPurify*、HomeVerticalDetail* 等安装器/策略，但均未提供逐方法命中记录；KotlinMossChannel.kt、KotlinMossReplyBridge.kt 被列为 unmapped_multi_path_candidates，无法判定被哪个安装器注册、覆盖哪些调用者。源码 dirty（source_tree_sha256 37745f8f…，head 5422fad1…）需按文件哈希追溯。综上：这些路径静态可观察，运行时是否启用、模块 Hook 是否命中均未知。

证据：E000, E005, E011, E013, E014

#### 路径：detail_legacy

- 状态：absent
- 变化：9.17.0 与 9.16.1 均为 0 类 / 0 Compose 方法 / 0 外部调用边，指纹两侧同为 4f53cd…（空集哈希），无结构变化。
- 可能影响：旧原生详情家族在静态侧无锚点，依赖该类名的安装器/定位器命中情况未知；absent 不能推出页面功能消失，也不能推出模块对该路径无影响。
- 验证：在 9.17.0 真机进入普通视频详情，抓取运行期类清单检索 legacy 详情特征并与 9.16.1 对照；同时确认模块日志中是否存在对应安装器的注册与命中条目（当前证据中无此日志）。
- 证据：E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1946→1975（+29），外部调用边 510→547（+37），Compose 方法 25→25，指纹 672508…→aba2db…；规模扩张但 Compose 面持平。
- 可能影响：UGC 详情侧的类集合与调用点有增量，逐方法注册可能新增未覆盖项；指纹变化亦可能来自混淆改名或 DEX 重排，无法据此断言新样式或模块失效。
- 验证：对两侧做类名单 diff（区分改名/新增/重排），抽样方法体哈希核对是否为同一实现；真机在 UGC 视频详情确认净化与复制类功能是否触发，并采集模块按 family 记录的 installed 结果。
- 证据：E005, E013

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4581→4633（+52），外部调用边 4257→4199（-58），Compose 方法 99→98，指纹 b0f0b0…→56c25b…；类增与边减并存。
- 可能影响：调用边下降与类扩张方向相反，最可能是调用解析、内联/重复包装层或编译产物变化，而非功能收敛；DetailUnited* 净化策略的定位点是否仍命中需逐条核对。
- 验证：对比两侧 united 家族的调用边端点集合，定位减少的边落在哪些被调用方法；用 JADX 读取一个减少边的调用方确认是否为内联或包装层；真机在 united 详情页验证模块净化项的实际生效范围。
- 证据：E005

### pgc

番剧/影视页两条路径均 static_invoke_observed。pgc_legacy 类数 354→352（-2）但外部调用边 399→425（+26），指纹 2c5cf1…→60c886…；类略减而边增加，需先排除 DEX 重排与调用解析差别，再判断是否有真实新增调用者。pgc_theseus 变化更剧烈：类 2265→2276（+11）、Compose 方法 131→134（+3）、外部调用边 782→1179（+397，约 +51%），指纹 4df56d…→44b6f7…。+51% 的边增长远高于 +0.5% 的类增长，更像相同类集合上新出现的调用者或更完整的调用边解析，而不是新界面家族整体迁入；Compose +3 只说明存在少量组合函数增删，不足以确认新样式。协议侧 pgc_player_moss（定义 12、边 3）与 pgc_view_moss（定义 14、边 7）在两侧完全一致，共同协议契约未见变化，因此 pgc 差异更可能来自页面内消费者与安装器覆盖，而非 MOSS 契约迁移。模块侧只有 PgcAutoActivityPopupFeatureInstaller/PgcAutoActivityPopupPolicy 与 PgcAutoActivityPopupLocator 三份相关源码被登记，未提供 locator 在 9.17.0 的命中记录；宽屏/平板分支、服务端开关与自动弹窗触发条件均未读到，运行条件未知。协议标识不是路径，不得计入路径评审。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类 354→352（-2），外部调用边 399→425（+26），Compose 方法两侧 0，指纹 2c5cf1…→60c886…；类减而边增。
- 可能影响：legacy 番剧页的调用面扩大但类集合收缩，可能是调用解析差异或重复包装层导致；自动活动弹窗定位器在该路径的锚点是否仍存在未知，不宜按“结构未变”处理。
- 验证：对 9.16.1/9.17.0 legacy 家族做类名单与方法体哈希 diff，定位 +26 条边的端点；真机在旧版式番剧详情/播放页观察自动活动弹窗拦截是否触发并输出定位器解析日志。
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2265→2276（+11），Compose 方法 131→134（+3），外部调用边 782→1179（+397），指纹 4df56d…→44b6f7…；边增速显著高于类增速。
- 可能影响：调用边扩张可能意味着新调用者接入 theseus 番剧页，模块若按旧调用点注册会漏覆盖；Compose +3 为样式候选信号但未确认，服务端 A/B 变体静态不可见。
- 验证：抽样对比两侧 Compose 签名与方法体哈希，确认 +3 是否为新增界面组合；列出新增调用边的调用方清单并逐一判断是否属于 player/view 消费者；真机在 theseus 番剧页（含宽屏/平板布局）验证净化与弹窗拦截的实际表现。
- 证据：E006

### player

player 页登记 player_java 与 player_kotlin 两条路径，均为 static_invoke_observed，运行时未知。最显著的变化是 player_kotlin 由 7 类 / 0 Compose 方法 / 100 边涨到 455 类 / 37 方法 / 841 边（约 65 倍类数），但同一侧 player_kotlin_moss 定义 34、实际调用边 3 与基线逐字相同，player_java_moss 定义 18、边 2 也相同。协议层零变化叠加家族层数十倍增长，更像家族划分边界、DEX 重排或 Kotlin/Compose 代码迁移，而不是新播放器样式；也可能是播放器 UI 真实迁入 Kotlin 家族，二者静态都未被区分。player_java 端类数小幅下降而调用边上升，提示部分类被迁出或加了包装层，不能用边数上升推断 Hook 覆盖变好。模块侧源码清单含 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator 等定位器，但本单元未读取，其解析签名与兜底分支属未知，需要安装器日志才能判断命中。另 unregistered_protocols 中仍列有 playerunite 的 PlayerMoss/KPlayerMoss 与 playeronline 的两个协议，说明播放器协议登记集合本身不完整，18/34 个定义不能当作播放器协议全集。

证据：E007, E000, E014

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：target 953 类 / 3308 边 / 指纹 f355088b…；baseline 958 类 / 3222 边 / 指纹 2830eeae…。类数 -5、边数 +86，家族指纹变更；同侧 player_java_moss 定义 18、实际调用边 2 两版完全一致。
- 可能影响：若模块以 Java 播放器类为解析锚点（倍速、缓冲、清晰度、能力位等定位器），类被迁出或套上包装层会导致安装期解析失败并落入兜底分支；调用边增加只说明静态可达路径变化，不证明 Hook 命中或功能生效。
- 验证：按类名+方法体哈希把 9.16.1 / 9.17.0 的 player_java 类清单逐条对齐，确认减少的 5 个类是迁入 player_kotlin、被去混淆改名，还是被合并；真机安装模块后采集安装器日志中各 player 定位器的 resolved/failed 与 complete 标记。
- 证据：E007, E000

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：target 455 类 / 37 Compose 方法 / 841 边 / 指纹 b9a6ea0f…；baseline 仅 7 类 / 0 Compose 方法 / 100 边 / 指纹 c20595ba…。同侧 player_kotlin_moss 定义 34、实际调用边 3 两版一致。
- 可能影响：两种解释并存：一是播放器 Kotlin/Compose 层真实扩编，模块的 Kotlin 侧会话与速度类锚点需要新解析点；二是家族归类边界或 DEX 拆分改变，多出的类原本就存在于基线其他家族，模块现有锚点其实未变。任一情况下都不能由类数与边数增长宣称播放器适配变更完成。
- 验证：把新增的 448 个类按类名与方法体哈希在基线的其他家族中反查，若命中则判定为归类迁移而非新增实现；未命中时再对比两版同名类的方法体哈希差异，并在真机上打开视频播放，输出各定位器实际解析到的类名与失败原因。
- 证据：E007, E014

### danmaku

danmaku 页登记 danmaku_legacy 与 danmaku_kotlin 两条路径。danmaku_legacy 两版均为 0 类 / 0 边、指纹同为 4f53cda…（空集），证据值为 absent，这只说明该管线在两个版本都未识别到 legacy 弹幕实现，既不能证明旧实现被删除，也不能证明弹幕功能消失；旧实现若被去混淆改名或并入其他家族，静态矩阵就看不见。danmaku_kotlin 则明显扩张：57→137 类、Compose 方法 1→3、外部调用边 8→162；而 danmaku_kotlin_moss 定义 46 两版不变、实际调用边 4→10，danmaku_java_moss 保持 22/20 不变。定义数不变而实际调用边增加，更像调用方增加或重排后出现新可达路径，而非协议结构变更，需要逐个定位这 6 条新增边的调用方，确认是否来自直播、互动或播放器内嵌等跨家族消费者。模块侧 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 在源码清单内但本单元未读取，净化挂点与跳过条件均属未知，因此新增调用方是否绕过净化无法静态判定。

证据：E008, E000

#### 路径：danmaku_legacy

- 状态：absent
- 变化：target 与 baseline 均为 0 类 / 0 Compose 方法 / 0 外部调用边，指纹同为 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945（空集不变），无新增也无消失迹象。
- 可能影响：旧版弹幕家族在两版都没有静态目标，因此任何针对 legacy 弹幕类的 Hook 在本版本都没有可定位对象；但同时无法区分“确实不存在”与“存在但没被这条分类规则归入”，模块净化功能的兜底分支是否被走到仍属未知。
- 验证：不依赖家族分类，直接在 9.16.1 / 9.17.0 的 DEX 中按 legacy 弹幕类名、父类与关键方法签名搜索，判断是缺失还是未归类；真机打开视频页后查看净化安装器日志中的 resolved/failed 计数，确认是否落到兜底。
- 证据：E008, E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：target 137 类 / 3 Compose 方法 / 162 边 / 指纹 38fdecc8…；baseline 57 类 / 1 Compose 方法 / 8 边 / 指纹 323c06fe…。danmaku_kotlin_moss 定义 46 不变、实际调用边 4→10；danmaku_java_moss 定义 22、边 20 两版一致。
- 可能影响：调用边由 8 增至 162 后，若模块净化 Hook 仍挂在旧调用点上，新增调用方可能走不同渲染或装配路径而绕过净化；反之若新增边只是重排产生的重复包装层，则实际行为不变。由于跨家族消费者未核实，无法判定哪一类弹幕实现真正被覆盖。
- 验证：对齐 46 个 moss 定义的方法体哈希确认协议未变；列出新增的 6 条 moss 调用边与全部外部边的调用方类，逐一对两版比对并标注其所属家族；真机分别对普通视频、直播、互动弹幕开关净化，记录未被净化的具体弹幕类型。
- 证据：E008, E000

### story

story 页登记两条路径。story_native 在 9.17.0 为 static_invoke_observed：2956 类、44 个 Compose 方法、1328 条外部调用边；基线 9.16.1 为 2924/44/1310，指纹 b56b7342…→dafc7376…（E009）。类 +32、边 +18 而 Compose 方法数保持 44，形态是“实现体量增加但 Compose 表面未增”，既可能是新增页面/逻辑类，也可能是 DEX 重排或类从其他家族迁入，静态矩阵无法区分。story_kotlin 两侧均 absent，空集指纹 4f53cda1… 两版完全一致，说明静态层没有观察到该家族的 Kotlin/Compose 调用边；这不等于页面没有 Compose 实现，只表示本轮没有可引用边。协议侧 KStoryMoss/StoryMoss 在未登记清单（E000），没有跨家族消费者与共同协议调用边可查，服务端 A/B 下发的新样式静态不可见。模块侧 StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、StoryActionIconsPolicy、PlayerStoryFreeDataPromotionAccess 与 HomeVerticalDetailRouting 的解析目标是否仍命中新版本类，未读到运行条件与命中日志，记为未知。E012 显示动态/Opus 的 1350 类实现位于 Lkntr/app/following/opusDetail 等独立命名空间，与 story 家族分开计数，故 story_native 的增量不能自动等同覆盖或遗漏 Opus 样式；E014 显示同一 APK 内可并存 LEGACY/NEXT/EXP3 三套外观并在安装时解析，说明并存栈需按家族单独计数，类存在不得升级为完整覆盖。

证据：E009, E000, E012, E014

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：目标 2956 类/44 Compose 方法/1328 边，基线 2924/44/1310，指纹 b56b7342…→dafc7376…；类 +32、边 +18，Compose 方法数不变（E009）。
- 可能影响：若为真实新增类或调用路径迁移，StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、HomeVerticalDetailRouting 的目标类/方法解析可能偏移或漏挂；若为 DEX 重排则功能面不变，两种解释静态阶段无法区分。
- 验证：对两版按 story 家族导出类名+方法体哈希清单做差集，定位 32 个新增类的包名归属；用 JADX 核对各 installer 的目标类名、方法签名与参数类型是否仍在目标 APK 中；真机开 story 页抓模块安装结果日志（Installed/失败单位）确认是否命中。
- 证据：E009, E000, E014

#### 路径：story_kotlin

- 状态：absent
- 变化：基线与目标两侧类数/Compose 方法/调用边均为 0，空集指纹 4f53cda1… 两版一致，无结构变化可查（E009）。
- 可能影响：静态层无该家族调用边，模块不能声称覆盖 Kotlin/Compose 版 story；若服务端或本地开关切到 Compose 实现，静态证据不会体现，属登记缺口而非功能消失。
- 验证：最小补证任务：真机在 story 页做布局树/类加载采样，确认是否加载 Compose 渲染路径；比对 story 家族与 comment_compose 等已知 Compose 家族的类命名空间差异，判断是否为家族命名空间未纳入扫描所致。
- 证据：E009

### mine

mine 页登记 mine_native 与 mine_account_model，目标侧均为 static_invoke_observed。mine_native 由 325 类/7 Compose 方法/92 边变为 326/7/94，指纹 75f16dab…→f6b18de5…（E010），即 +1 类、+2 边、Compose 表面不变。mine_account_model 更需谨慎：类数 132、Compose 方法 0、外部调用边 43 在基线与目标完全一致，但指纹由 2b548e1a… 变为 db7f2792…（E010）；计数全等而结构哈希变化，最可能是混淆改名、方法体字节码变化或 DEX 重排，而不是新样式或新模型。真实风险在解析方式：E013 显示模块对宿主模型采用混淆短字段名（a/i/j/k）加枚举名集合与类型一致性护栏来定位语义字段，同类做法若用于 mine 快照链路（MineComponentSnapshotStore、MineComponentSnapshotQueryContract、MineComponentSnapshotHostBridge、HostMineReadingCard），字段短名重排会让解析 runCatching 静默返回 null 而不报错。MineComponentFilterFeatureInstaller 与 MineVipFeatureInstaller 的组件过滤、会员区块 hook 是否仍命中新类，未读到安装器运行条件与命中记录，记为未知。MineMoss/KMineMoss 未登记（E000），服务端下发的账号区块或卡片样式若只走协议字段变化，静态层不可见；E014 的“类存在不等于覆盖、失败单位留在分母”同样适用于此处，不能因家族仍 present 就判定过滤完整。

证据：E010, E013, E014, E000

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：目标 326 类/7 Compose 方法/94 边，基线 325/7/92，指纹 75f16dab…→f6b18de5…；+1 类、+2 边，Compose 方法数不变（E010）。
- 可能影响：新增 1 类与 2 条外部调用边可能改变组件快照来源或会员区块加载路径，MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、HostMineReadingCard 的解析点与过滤名单可能未覆盖新调用者。
- 验证：对两版 mine 家族做类名差集与方法体哈希差集，定位新增类与两条新边两端；用 JADX 核对 MineVipFeatureInstaller 目标签名；真机进入 mine 页验证组件过滤、会员卡与阅读卡是否生效，并抓安装器结果日志确认失败单位。
- 证据：E010, E014

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：132 类/0 Compose 方法/43 边在基线与目标完全一致，指纹 2b548e1a…→db7f2792…（E010）；无类或调用边增减，仅有结构哈希变化。
- 可能影响：无计数变化而哈希变化，优先怀疑混淆改名/方法体变化导致按短字段名解析的账号模型读取失效；若解析静默失败，mine 页账号区块快照（MineComponentSnapshotStore/HostBridge）会读到空值而不抛错。
- 验证：以混淆短名字段表（a/b/c…）与方法体哈希逐项对比两版该家族，确认变化是重命名、方法体重写还是类搬迁；用 decompile_class 读 MineComponentSnapshotQueryContract 的字段解析容忍度；真机抓 mine 账号区块快照的 null/默认值返回率。
- 证据：E010, E013

### F001：Compose 评论自由复制依赖混淆字段名单点解析，签名全变后可能静默降级
事实：comment_compose 外部调用边 934→1101、compose_methods 278→283、类数 2444→2428，签名 089904c2… 全变（E001）；样本类 kntr/common/comment/common/service/f、g 与 richtext 的 IconText/getRaw 显示模型与服务层都在该家族内（E011）。模块 CommentComposeCopyBridge 的 ComposeCommentText.resolve 明确按混淆名 a(Long)/i(枚举，必须恰为 ORIGIN/TRANSLATING/TRANSLATION)/j、k(同型)/o、p(必须与 j 同型)/b、c(Long) 逐字段匹配，任一不满足即返回 null，install 走 missing("missing-text-shape") 并返回 Skipped（E013，文件 sha256 1783fcbf…，工作树 dirty）。dispatch 侧还要求 context 参数类型中“恰好一个”字段能消费 actionClass 子类，否则 ambiguous-more-action。推断：在字段布局或枚举常量发生变化的版本上，功能会静默缺失而非崩溃；覆盖率停在 Skipped，不会被误报为 ok（CommentFamilyCoverage 语义见 E014）。这是“结构哈希变化≠新样式”的典型场景，也说明类仍存在不足以证明 Hook 覆盖。反例/替代解释：283 个 compose 方法中只要仍存在一个满足静态性与 Composer 参数要求、且字段形态未变的 renderer，resolve 就能成功，此时本推断被推翻；也可能模型类被强类型化为 KReplyInfo 而根本不再使用该混淆形态。
反例与替代解释：可推翻本推断的证据：按名重读模型类后若 a/i/j/k/o/p/b/c 全部类型匹配且枚举恰为三常量，则解析成功、推断不成立；若 renderer 类中带 modelClass 参数的方法全部带 Composer 参数且非 static，则 render 覆盖也不成立为缺口。反之若 resolve 返回 null 或 actionClass.declaredClasses 出现多个候选，则确认降级路径会被真实触发。
建议：补证任务：用 decompile_class 按名读取 kntr/common/comment 下被判为模型的类，逐字段记录类型与枚举常量集；再读取 renderer 类，统计带 modelClass+Composer 参数的非静态方法数量并与 283 的家族计数对照（注意方法定义数与调用边数不同单位，不得相除得覆盖率）。真机侧开启模块后在 Compose 评论页长按，采集 free_copy_compose_missing-text-shape / free_copy_compose_ambiguous-more-action 日志是否出现。
证据：E001, E011, E013, E014

### F002：原生三外观 handler 类名硬编码，exp3 双缩减与 next 边增密方向相反
事实：CommentNativeBindingCatalog 以字符串常量写死三个 handler 全限定名（CommentContentRichTextHandler / CommentNextContentRichTextHandler / CommentNextExperiment3ContentRichTextHandler），并要求类中存在以 .CommentItem 结尾的字段且绑定方法含 View 型参数，否则 bindingMethods 直接返回空列表（E014，sha256 b9767153…）。静态矩阵显示 native_next 类数 45→48、外部边 50→67（+17），native_exp3 类数 58→54、外部边 62→52（-10），是同一页里唯一方向相反的两项（E001）。推断：exp3 的缩减可能是实验外观被合并进 next（next 边增密与此相符），也可能是独立迁移；若 exp3 handler 被改名/移包，catalog 解析为空、CommentFamilyCoverage 记 missing，行为是“该外观下不生效”而不是崩溃。因两家族类名都是明文常量而非特征匹配，FQN 变动是可直接触发失效的路径。另需注意 class 减少不等于页面功能消失，也不等于新样式出现。
反例与替代解释：可推翻本推断的证据：若 exp3 消失的 4 个类只是内部实现类被拆入 next 包而三个 handler FQN 全部仍存在且仍含 CommentItem 字段，则 catalog 解析不受影响，缩减只是重构；若 next 新增的 17 条边全部落在已有绑定方法内部而非新增绑定入口，则也不构成 Hook 缺口。反之若 decompile 显示 handler 改名或 CommentItem 字段消失，则 bindingMethods 必然为空，本推断升级为确认失效路径。
建议：补证任务：用 decompile_class 按三个 FQN 逐个确认类是否存在、字段是否含 CommentItem、绑定方法是否仍满足 View 型参数判定；对 exp3 缺失的 4 个类在 next/legacy 包内按方法体哈希反查是否为迁移。真机侧在服务端可下发 exp3 与 next 外观的账号上分别进入评论详情，读取 CommentFamilyCoverage 输出的 exp3=/next= 状态（ok/partial/missing）。
证据：E001, E014

### F003：动态 Opus 结构持平但调用边增密约 21.5%，增密样本落在非 Compose 的 opusDetail api/拦截器层
事实：dynamic_opus 类数 1352→1350、compose_methods 92→94 基本不动，外部边 186→226（+40），签名 60096774… 全变；同期 dynamic_legacy 外部边 2151→2075（-76，compose_methods 105→103）、dynamic_compose 类数 1136→1187 且 compose_methods 127→141、外部边 221→234（E002/E016）。E012 的 opus 样本全部位于 kntr/app/following/opusDetail/api：A（ImmutableSet→List 容器）、B（List+Function1→Map 组装）、C（值对象 equals/hashCode）、CompositeExternalInterceptor$firstSnapshotFile$1 与 $handleAdClick$1（ContinuationImpl 子类），均无 compose_signatures，说明 Opus 数据在进入渲染前有一条独立装配/拦截链；样本量极小，不能代表 1350 类整体。模块侧本轮补读 DynamicPurifyFeatureInstaller（E018，sha256 74f8c301…）：其装点为 dynamic.purify.moss 的 DYNAMIC_MOSS_CLASS 与 KotlinDynamicMossWatch.K_MOSS_CLASS，按 FEED_METHODS/ROOT_FEED_METHODS 的 reply 类或 asyncName 解析，并要求 DynamicItem 的 listBuilder/clearTopicList/upList/wholeUpList 成员存在，均不满足即 missing("no-dynamic-hook-point")，部分满足记 partial，源码中未见针对 opusDetail.api 或 CompositeExternalInterceptor 的解析点。推断：动态页净化/过滤挂在 Moss protobuf 响应边界，而 Opus 的 api/拦截器装配链不在该安装器的静态覆盖范围内，类数稳定也不会被“类存在”检查发现；但这是“该文件未见覆盖”，不等于全模块无覆盖。反例/替代解释：+40 条边可能主要是 lambda/ContinuationImpl 合成类内部调用被计入，属编译器或 DEX 组织差异；也可能集中在本轮 API 增密无关的广告/统计分支（handleAdClick 类）；此外 feeds 解析失败时的 partial 语义可能已由未读的 DynamicTabsFeatureInstaller 或其它安装点补足。
反例与替代解释：可推翻本推断的证据：若 40 条新增边的源类全部为同一拦截器类的合成协程方法且不触及正文/卡片字段，则属编译产物差异；若 opusDetail.api 与 Opus 详情页渲染关键路径不相连（仅广告/快照分发），则“模块未覆盖该链”无功能意义；若 DynamicTabsFeatureInstaller 或 KotlinDynamicMossWatch 已对 opus 家族另行注册装点，则覆盖缺口不成立。反之若新增边中有调用方直接读取富文本/统计字段，或真机在 Opus 详情页观察到净化未生效且日志缺失装点，则缺口成立。
建议：补证任务：decompile_class 读取 CompositeExternalInterceptor 及其调用方，列出新增边的源类与目标方法并标注是否涉及正文/卡片/富文本字段；按名核对 KOpusMoss、app/dynamic/v2/OpusMoss、dynamic/interfaces/feed/FeedMoss 等未登记协议的消费者是否落在 opus 家族。模块侧继续读取 DynamicTabsFeatureInstaller 与 KotlinDynamicMossWatch（仍未读，记未知），确认是否存在 opusDetail 包定位点或兜底。真机在单条 Opus 详情页与动态流内嵌卡片分别验证净化与长按复制，并记录 dynamic_opus 的运行时启用状态与装点日志（区分安装成功与运行期命中）。
证据：E002, E012, E016, E018

### F004：home 两家族 fingerprint 双变且无类样本，无法区分结构变化与混淆/DEX 重排
事实（E003）：home_legacy 由 767 类/87 compose 方法/204 边变为 766/87/198，fingerprint 7a842bbb…→a56da1e1…；home_new_frame 由 196/33/49 变为 196/33/52，fingerprint 4a3e9002…→34c59fa3…。两条路径同时被登记为 structure_or_call_path_changed（E000）。推断：legacy 侧规模微缩、new_frame 侧规模持平，变化幅度都很小，不能排除混淆改名、类排序或编译器变化；反过来也不能据此否定首页帧或 Tab 层发生迁移。E003 的 limits 明确只有每家族两份类样本、每协议四个调用者样本，而 prefetch 实际未落出 home 家族的类样本，所以本页“哪个类变了、变成什么”属未知。影响面推断：legacy 与 new_frame 分别对应不同首页帧/组件过滤与间距 Hook，若定位点随类名或继承结构迁移，HomeFrameTabLocator、HostHomeCardSpacingHooks 等会静默不命中，且宿主不会报错，用户侧表现为“净化/间距功能部分失效”而非崩溃。反例：如果目标与基线方法体哈希在重命名映射后一致，当前变化只是打包噪声，则无适配动作。
反例与替代解释：可推翻当前推断的证据：1) 差异类方法体哈希在改名对齐后完全一致 → 判定为混淆/重排噪声；2) 差异类中出现新的首页帧容器或 Tab 宿主并被外部调用 → 确认为真实结构变化；3) 真机日志显示现有定位器在 9.17.0 全部命中 → 影响被高估。
建议：先用 family_evidence 取 home_legacy 与 home_new_frame 在 target/baseline 两侧的具名类，逐一做方法体哈希比对并列出差异类；再只对差异类用 decompile_class 读 JADX 输出，确认是否新帧/新 Tab 宿主；最后真机按功能开关逐条观察 Hook 命中日志。
证据：E003, E000

### F005：search 两路径调用边与 compose 方法数反向变动，MOSS 计数虽与基线相同但调用者与未登记协议未验证
事实（E004）：search_native 1702→1705 类、2859→2818 边（-41）；search_compose 3141→3146 类、561→562 compose 方法、595→614 边（+19）；search_java_moss 24 定义/22 边与 search_kotlin_moss 52 定义/18 边两侧数值完全一致。抽样边界须写明：E004 的 protocols 段只有 summary，未给出任何调用者类样本，因此“边数一致”只证明已登记协议的数量面未变，不能推出消费者集合、调用点位置或语义未变；定义数与调用边数不是同一单位，禁止相除推算覆盖率。推断：原生侧边减而类增、Compose 侧方法 +1 而边 +19，方向不对称，更像类被重包装或调用边迁入新类，而非整块样式重写。E000 的 unregistered_protocols 列出多条搜索相关未登记协议（app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/SearchMoss 等），这些通道的调用者未登记；若默认词/热搜/搜索首页推荐改走其中一条，静态上会表现为“已登记边数不变”而实际语义改变。影响：SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller 的清理与净化可能对新调用者不生效；但这五个模块文件本会话均未读取，其匹配条件与兜底分支属未知，不推断 Hook 覆盖。反例：若已登记 MOSS 的调用者集合与基线同名同类且落在模块定位器范围内，或未登记 SearchMoss 在 target 包中没有任何实际调用边，则当前差异只是打包噪声。
反例与替代解释：可推翻当前推断的证据：1) protocol_evidence 显示两套 MOSS 的调用者集合在两侧同名同类且都落在模块已登记的定位器范围内 → 协议面担忧不成立；2) 四个未登记 SearchMoss 通道在 target DEX 中均无实际调用边 → 降级为不相关；3) 类级方法体哈希在改名对齐后一致 → 结构差异判为混淆/DEX 重排噪声；4) 真机默认词清理与推荐净化行为与 9.16.1 一致 → 影响被高估。
建议：用 protocol_evidence 分别取 search_java_moss 与 search_kotlin_moss 的调用者类，与基线同名比对并交叉检查 Java↔Kotlin 跨家族消费；对 unregistered_protocols 中的 app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/SearchMoss 逐一确认在 target DEX 中是否存在实际调用边；再用 module_source 读 SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller 的实际解析条件与兜底分支，按文件 sha256 记录工作树 dirty 状态下所读版本（source_tree_sha256 37745f8f…，head 5422fad1…）；真机分别验证搜索页默认词、热搜与搜索首页推荐卡片，并记录是否受服务端实验开关与宽屏形态控制。
证据：E004, E000

### F006：四条路径的启用状态与安装器覆盖均为未知，模块侧家族覆盖计数不可外推到 home/search
事实：seed 中四条路径 runtime_enabled 均为 unknown，module_coverage 均为 requires_installer_review，home/search 的 complete_coverage 均为 false，status 为 installer_and_runtime_validation_required（E000）。深挖 E014（CommentNativeBindingCatalog/CommentFamilyCoverage）显示模块的覆盖记账是按家族、按安装结果累计，且注释明确“失败单位留在分母里；没有注册的方法不能由类存在升级为完整覆盖”——该实现属于评论家族，不能当作 home/search 已被覆盖的证据，只能说明这类计数是安装期统计而非运行期证明。推断：即便 home/search 的定位器在安装期登记成功，也不能推出运行时路径被启用，更不能推出 Hook 生效；源码快照 working_tree_dirty、captured_at 为发布态未复核工作树，HomeFrameTabLocator、SearchHomeRecommendLocator 等候选文件本轮未读取内容，其匹配条件与兜底逻辑属未知。影响：任何“已适配/无影响”的表述都缺证据支撑，实际风险集中在静默不命中。
反例与替代解释：可推翻当前推断的证据：1) 真机日志证明四条路径对应的安装器全部安装完成且运行期命中 → 覆盖未知可收窄；2) 源码显示定位器有强兜底（如按接口/父类扫描）并覆盖新增类 → 定位失配风险下降；3) 若两版本运行期行为一致且日志一致 → 本次结构变化影响可判为噪声。
建议：先读 HomeFrameTabLocator、HomeFrameListHook、SearchHomeRecommendLocator、SearchHomeRecommendPolicy 的实际匹配条件与兜底分支，按文件 sha256 记录所读版本；再在真机上采集模块安装日志（安装成功/失败家族名）与首页、搜索页功能命中日志；同时确认 home/search 是否受服务端实验开关控制。
证据：E014, E003, E004, E000

### F007：评论原生绑定目录按三个写死 handler 类名解析，9.17.0 中三者存在性未验证，落空时静默降级为 partial/skipped
事实：E014 显示 CommentNativeBindingCatalog 以常量写死三个完整类名 LEGACY=com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler、NEXT=com.bilibili.app.comment3.ui.nextholder.handle.CommentNextContentRichTextHandler、EXP3=com.bilibili.app.comment3.ui.nextholderexp3.handle.CommentNextExperiment3ContentRichTextHandler，并按 EXP3→NEXT→LEGACY 作为 mainHandlers；bindingMethods 先用 declaredFields 中是否存在类型名以 .CommentItem 结尾的字段做前置判定，再筛选非静态、非桥接、非合成、返回 void、参数数 1..5 且存在“绑定型”参数（含 View 字段或含返回 View 的 getRoot）的方法，任一前置条件不满足即返回空列表，注释明确“失败单位留在分母里”“不能由类存在升级为完整覆盖”。E013/E017（同文件 sha256 1783fcbf…）显示 Compose 侧走的是完全不同的定位方式：按 a(Long)/i(三值枚举 ORIGIN/TRANSLATING/TRANSLATION)/j/k 同型/o/p 同型解析模型，并注明字段语义在 20 份 APK 中核对过——说明“按字段形状解析”在改名后仍可能命中，而“按全限定类名解析”的绑定目录一旦改名即返回空，两者并存会形成数据侧可读、UI 绑定点未注册的半覆盖形态。范围边界：这三个 FQN 属 com.bilibili.app.comment3 原生外观家族，本会话未下发 comment_native_legacy/next/exp3 的家族证据；E011 的 comment_compose（2428 类、283 Compose 方法、1101 外部调用边，样本仅见 kntr/common/comment/*）与 E005 的 detail_theseus_ugc/united 计数都不能证明这三个 FQN 在 9.17.0 仍存在，故存在性目前为未知，而非已确认缺失。推断：若 9.17.0 仅改 handler 类名或将三个外观合并，bindingMethods 返回空且不抛错，覆盖静默下降并被记入分母。反例：detail_theseus_ugc 类 +29、Compose 25→25 可能意味着评论侧实现基本未动，本风险不成立。
反例与替代解释：可推翻当前推断的证据：1) 三个 FQN 在 9.17.0 全部存在，且 bindingMethods 对每个返回非空方法列表；2) CommentItem 后缀字段与 getRoot 绑定型参数形状在两版一致，说明前置过滤未产生版本差异；3) 真机日志显示三个 family 的 record 均为 installed 且 complete=true。支持推断的证据：三个 FQN 中任一在 9.17.0 缺失，或存在但 bindingMethods 返回空列表，或日志显示只命中 1-2 个 family / 状态为 partial。补充替代解释：类数变化也可能仅来自混淆改名与 DEX 重排，此时“FQN 不匹配”并不等于该外观下线。
建议：最小补证任务：1) 对 9.17.0 DEX 精确检索三个 FQN 的存在性，并检查是否新增第四个 exp 变体类名；同时拉取 comment_native_legacy/next/exp3 的家族证据，确认 handler 类是否仍落在这些家族内（本会话只有 comment_compose 与 detail_theseus_* 证据，不足以判定）。2) 真机详情页采集 CommentFamilyCoverage 的 record(family, installed/FeatureInstallResult) 与 complete 输出，区分“类不存在”与“类存在但方法被前置过滤（返回空列表）”两种落空形态，失败项保留在分母。3) 若发现第四变体，需在目录中显式登记；不得以“类存在”或“目录常量未改”升级为完整覆盖。
证据：E014, E011, E013, E005

### F008：pgc_theseus 外部调用边 782→1179（+51%）而类数仅 +11，需先排除解析/包装层变化再判断消费者扩张
事实：E006 预取的 pgc 两侧对比显示 pgc_theseus 类 2265→2276（+11）、Compose 方法 131→134（+3）、外部调用边 782→1179（+397），指纹 4df56d…→44b6f7…；pgc_legacy 类 354→352（-2）而边 399→425（+26）。同时 pgc_player_moss（定义 12/边 3）与 pgc_view_moss（定义 14/边 7）在两个版本完全一致，说明 MOSS 契约没有迁移，pgc 侧变化更可能发生在页面内调用者与调用边解析层面。方法定义数与调用边数不是同一单位，无法用 +397/+11 之类比例推导覆盖率，这里只能作结构性提示。推断：+51% 的边增长若集中在少数被调用方法上，可能是新增调用者或反编译对 invoke 解析更完整；若分散在大量类上，则更可能是重复包装层或 DEX 重排。影响面：若确有新调用者接入 theseus 番剧页播放/视图链路，按旧调用点注册的模块会漏覆盖；若只是解析差异，则属于假阳性。反例：Compose 仅 +3，且这些家族在 9.16.1 已是 static_invoke_observed，无法证明新样式；服务端 A/B 变体在无结构变化时静态不可见。待真机验证。
反例与替代解释：可推翻当前推断的证据：1) 边集合差显示新增边集中于同一调用方且该调用方是新增类（则支持真实消费者扩张）；2) 新增边全部来自已知包装层/转发方法，且方法体哈希与基线一致（则支持解析/包装层解释）；3) 真机日志显示 pgc 自动弹窗定位器在两侧版本命中同一批锚点（则模块面风险降低）。
建议：最小补证任务：1) 导出 pgc_theseus 两侧调用边的(调用方, 被调用方)集合做差，把 +397 条边按调用方聚类，识别是集中还是弥散；2) 抽样 2-3 个新增调用方，用反编译读取方法体确认是新消费者还是包装/内联导致的重复边；3) 结合 PgcAutoActivityPopupLocator/PgcAutoActivityPopupPolicy 的解析日志，在 theseus 番剧详情与播放页（含宽屏布局）各触发一次，确认定位器命中与兜底分支。
证据：E006

### F009：player_kotlin 家族 7→455 类、37 个 Compose 方法：疑似归类边界重映射或 Kotlin 迁移，非已确认新播放器样式
事实（E007）：target player_kotlin 455 类/37 Compose 方法/841 外部调用边/指纹 b9a6ea0f…，baseline 7 类/0/100/c20595ba…，类数约 65 倍；同侧 player_kotlin_moss 定义 34、实际调用边 3，player_java_moss 定义 18、边 2，两版逐项一致；player_java 由 958 类/3222 边/2830eeae… 变为 953 类/3308 边/f355088b…。须注意 E007 的预取限制为每家族两个类样本、每协议四个调用者样本，以上均为家族摘要，未做逐类核对。推断：协议层零变化叠加家族层暴涨，优先支持“家族划分口径变化 / DEX 重排 / Kotlin+Compose 代码迁入”，而非播放器样式换代；真实迁移同样能产生该形态，静态无法区分，故 level 保持 candidate。影响面：源码清单含 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerCapabilityAccess，但本单元未读取其正文，声明的解析签名、版本分支与兜底条件全部为未知；只能提出待验证推断——锚点若随迁移改变，安装期解析可能静默失败并落入兜底，表现为倍速/缓冲/清晰度开关无反应而非崩溃，这项目前没有任何实读源码或运行日志支撑。E014（CommentNativeBindingCatalog / CommentFamilyCoverage）属评论家族，只能说明模块把失败单位保留在分母、类存在不能升级为完整覆盖的记账语义，既不是 player 安装器的命中证据，也不是失败证据。E000 的 unregistered_protocols 仍列 playerunite 的 PlayerMoss/KPlayerMoss 与 playeronline 的 PlayerOnlineMoss/KPlayerOnlineMoss，说明 18/34 个定义并非播放器协议全集，协议登记集合本身存在缺口。
反例与替代解释：若按类名+方法体哈希能在 9.16.1 的其他家族中找到这 448 个“新增”类，则“Kotlin 播放器真实扩编”被推翻，应判为归类重映射；若这些类在两版都只出现在该家族且同名方法体哈希有差异，则支持真实结构变化；若类名与方法签名完全一致、仅方法体哈希不同，则优先判为编译器或去混淆产物。若跨家族反查后连方法体哈希也一致，则即便家族规模变化，也只能按“未归类/重排”统计，不能记为样式候选。附带项：若 playerunite/playeronline 协议在 9.16.1 就已存在且无调用边变化，则协议缺口属长期既有问题，不构成本次回归。
建议：先用类名+方法体哈希完成 9.16.1 / 9.17.0 两版类清单对齐，并把 448 个“新增”类跨家族反查，判定是归类迁移、改名还是真实新增；再按名读取 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerCapabilityAccess 正文，列出声明的解析签名、版本分支与兜底条件（本次未读，结论为未知）；随后真机安装模块，采集安装器日志中各定位器的 resolved/failed 与 complete 标记，并实际切换倍速、缓冲、清晰度各一次确认生效，明确区分“安装成功”与“运行期命中”。在任何一步取得结果前，不得以边数增长或类数增长替代覆盖结论。
证据：E007, E000, E014

### F010：danmaku_kotlin 外部边 8→162、moss 实际调用边 4→10（定义数仍 46）：调用方扩张候选，需确认是否绕过净化挂点
事实（E008）：danmaku_kotlin 由 57 类 / 1 Compose 方法 / 8 边升到 137 类 / 3 方法 / 162 边，指纹变化；danmaku_kotlin_moss 定义 46 两版不变而实际调用边 4→10；danmaku_java_moss 定义 22、边 20 两版一致；danmaku_legacy 两版均 0 类 0 边、空集指纹相同，证据值为 absent。推断：协议定义数完全不变而实际调用边增加 6 条，指向新增调用者或重排后出现的新可达路径，比“弹幕协议改版”更可能；但调用方归属家族未核实，跨家族消费者（直播、互动、播放器内嵌）是否在列未知。影响面：DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 在源码清单内但本单元未读取，净化挂点与跳过条件未知；若挂点位于旧调用路径，新增调用方可能构成未被净化的渲染或装配分支，表现为部分弹幕类型（如互动/直播/特殊样式）仍然出现。absent 的 danmaku_legacy 不能作为“旧实现已删除”或“弹幕功能消失”的证据，只能记为静态矩阵未识别。E013/E014 为评论侧模块源码，未覆盖弹幕安装器，仅提示模块倾向按字段语义与枚举常量做严格校验，弹幕侧是否采用同等严格度仍需读源码确认。
反例与替代解释：若这 6 条新增 moss 调用边的调用方类名与方法体哈希在基线中已存在（只是家族归属或编号变化），则“调用方扩张”被推翻，应判为分类/DEX 重排；若 46 个 moss 定义的方法体哈希也发生变化，则可能是协议层改动而非调用边增加；若真机开净化后所有弹幕类型都被清理，则“新增路径绕过净化”这一假设被推翻。
建议：先对齐 46 个 moss 定义的方法体哈希，再列出 10 条 moss 调用边与 162 条外部边的调用方类并逐一对两版比对、标注所属家族；随后读 DanmakuPurifyFeatureInstaller/Policy 确认挂点与跳过条件，真机分别对普通视频、直播、互动弹幕开关净化并记录未被净化的具体类型与日志。
证据：E008, E000, E013, E014

### F011：story_native 增量与 Compose 表面脱钩：新增类/+18 边可能是重排或家族迁移，不能视为新样式
事实：story_native 目标侧 2956 类/44 Compose 方法/1328 外部调用边，基线 2924/44/1310，指纹 b56b7342…→dafc7376…（E009）；类 +32、边 +18，Compose 方法数不变，story_kotlin 在两侧都是 absent 且空集指纹一致。触发路径：进入 story 页 → 宿主加载 story 家族类 → 模块 installer（StoryPurifyFeatureInstaller/StoryActionIconsFeatureInstaller/HomeVerticalDetailRouting）按类名与方法签名解析并挂 hook，若解析目标随重排或迁移改变，hook 会落到失败单位而不报错。可能受影响功能：story 净化、操作图标、免流数据入口与竖屏详情路由。另一条线索：E012 显示动态/Opus 的 1350 类实现位于 Lkntr/app/following/opusDetail 等命名空间，与 story 家族独立计数；E014 显示同一 APK 可并存 LEGACY/NEXT/EXP3 三套外观且覆盖状态按家族分别记录、失败单位留在分母。因此 story 的类增既可能是新增页面实现，也可能是其他家族类迁入或版本整体重编译（sample 恰有 7121 个资源变更、15 个新增资源）。运行时是否启用、实际命中哪一套外观均为未知，本条目只作待验证假设。
反例与替代解释：可推翻当前推断的证据：①32 个新增类全部位于无关包且与 story 入口无调用关系，说明是编译/重排噪声；②两版同名类的方法体哈希完全一致，说明只是类索引重排；③真机日志显示 installer 全部 Installed 且 hook 命中，说明增量未破坏解析；④若发现 story 家族外存在被服务端开关激活的 Opus/Compose 实现，则问题从“重排”转为“家族归属错误”。
建议：先做静态差集再上机：导出两版 story 家族“类名+方法体哈希”清单，取新增 32 类与 18 条新边的两端命名空间，判断是新增实现还是从其他家族迁入；随后用 JADX 逐个核对三个 installer 的目标类名/参数类型是否仍存在；最后在 9.17.0 真机打开 story 页，抓模块安装结果（含失败单位）与 hook 命中日志，并确认是否存在第二套未挂 hook 的入口类。
证据：E009, E000, E012, E014

### F012：mine_account_model 计数全等而结构哈希变化：应按混淆改名/方法体变化处理，并检查短字段名解析的静默失败
事实：mine_account_model 目标与基线均为 132 类、0 Compose 方法、43 外部调用边，仅指纹 2b548e1a…→db7f2792…（E010）；mine_native 同期 325→326 类、92→94 边、Compose 方法数保持 7。计数全等而哈希变化，最经济的解释是混淆短名重排、方法体字节码变化或 DEX 重排，而不是新增账号模型样式；既然结构指纹变化不等于新样式，本页不应出现“账号模型样式更新”的描述。推断风险：E013 显示模块对宿主模型用混淆短字段名（a、i、j、k）加枚举常量名集合、字段类型一致性等语义护栏定位正文，并用 runCatching 返回 null 兜底；若 mine 快照链路（MineComponentSnapshotStore、MineComponentSnapshotQueryContract、MineComponentSnapshotHostBridge、HostMineReadingCard）采用同类短名解析，一次改名就会让读取静默降级为空值而非抛错。E014 亦显示覆盖计数把失败单位留在分母，类存在不得升级为完整覆盖。MineMoss/KMineMoss 未登记（E000），服务端下发的账号区块与会员卡样式若只走协议字段层面，静态证据完全看不到。触发条件、运行时启用与安装器兜底是否命中均为未知。
反例与替代解释：可推翻当前推断的证据：①字段表与方法体哈希逐项比对后差异为零，说明只是类索引/常量池重排，风险可撤销；②差异集中在非模型字段的新增字段，说明是数据扩展而非解析破坏；③MineComponentSnapshot 解析基于注解/序列化名而非混淆短名，则短名重排不会造成静默失败；④真机日志显示 mine 快照与会员卡均正常取值，说明该指纹变化无功能影响。
建议：对两版 mine_account_model 做字段表+方法体哈希逐项对比，把差异分类为“重命名”“方法体重写”“类搬迁”三类并给出计数；用 decompile_class 读 MineComponentSnapshotQueryContract/Store 的字段解析容忍度，确认是否依赖短名硬编码与是否有类型/枚举护栏；真机在 mine 页记录账号区块快照的 null 或默认值返回率，并对照模块安装结果日志中的失败单位。
证据：E010, E013, E014, E000

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
fresh_refresh=E015 复核后维持草稿结论：五条登记路径（legacy_v2 583类/741边、native_legacy 181/220、native_next 48/67、native_exp3 54/52、compose 2428类/283 compose方法/1101边）在 9.17.0 侧仍为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，不存在任何适配结论（E001/E015）。变化方向确实分裂：compose 外部边 934→1101、compose_methods 278→283；native_next 边 50→67 而类数仅 45→48；native_exp3 类 58→54、边 62→52 为唯一双缩减；legacy_v2 +4类/+6边近噪声。协议侧 java 50定义/50边两侧一致，kotlin 130定义不变而边 26→23，草稿把下降 3 条边归为未知/可能调用方迁移而非新样式，口径正确。本轮重读 CommentComposeCopyBridge（E017，sha256 1783fcbf…）确认字段单点匹配与 Skipped 分支描述属实：resolve 仅按 a(Long)/i(枚举且集合必须恰为 ORIGIN/TRANSLATING/TRANSLATION)/j/k(同型)/o、p(同型)/b、c(Long)/原文字段 a(String) 匹配，任一缺失或 o、p 类型不符即返回 null，install 随后 missing("missing-text-shape")→Skipped；dispatch 侧确以 declaredClasses.singleOrNull 选 action 子类，多重候选即 ambiguous-more-action（E013/E017）。CommentNativeBindingCatalog 的三个 handler FQN 字符串常量与“无 .CommentItem 字段即返回 emptyList”、CommentFamilyCoverage 不把未注册方法升级为 ok 亦经 E014 证实。局限：prefetch 每家族仅数份类样本，不能代表 2428 类整体；compose 家族 283 个方法中哪些真正被 Hook 未逐一读取；exp3 缩减是迁移还是实验下线未定；平板/宽屏与服务端 A/B 的样式选择条件未读到运行条件，保持未知。
证据：E001, E011, E013, E014, E015, E017

### 复核页面：dynamic
fresh_refresh=E016 与 E002 一致：三路径签名全变、均 static_invoke_observed、runtime 与安装器覆盖未知（E002/E016）。数据面：legacy 3255类/2075边（2151→2075，-76）且 compose_methods 105→103；compose 1136→1187类、127→141、221→234；opus 1350类（1352→1350）、compose_methods 92→94、外部边 186→226（+40）而类数几乎不动，故 opus 属“结构持平、调用关系增密”，草稿将其登记为样式候选而非新样式，口径正确。E012 的 opus 样本全部落在 kntr/app/following/opusDetail/api（A/B/C 数据容器、ImmutableSet→Map 组装、CompositeExternalInterceptor 的 firstSnapshotFile/handleAdClick ContinuationImpl），全部无 compose_signatures，说明存在独立于 Compose 渲染的装配/拦截层；但样本占比极小，不能外推到 1350 类，草稿已声明该限制。本轮补读 DynamicPurifyFeatureInstaller（E018，sha256 74f8c301…）：其装点解析 dynamic.purify.moss 的 DYNAMIC_MOSS_CLASS 与 KotlinDynamicMossWatch.K_MOSS_CLASS，按 FEED_METHODS/ROOT_FEED_METHODS 的 reply 类与 asyncName 匹配，并要求 listBuilder/clearTopicList/upList/wholeUpList 存在，否则 missing("no-dynamic-hook-point")/partial；源码中未见对 opusDetail.api 或 CompositeExternalInterceptor 的定位，故“opus 装配链不在该安装器覆盖内”属静态可支持的推断，但 DynamicTabsFeatureInstaller 与 KotlinDynamicMossWatch 仍未读，Opus 详情页是否存在其它安装点保持未知。协议侧 java 134/134、kotlin 382/26 两侧一致，未登记协议（DynamicMoss、OpusMoss、KOpusMoss、FeedMoss 等）的消费者仍未归类。
证据：E002, E012, E016, E018

### 复核页面：home
复核确认：本页只有 E003（fresh 预取，target 9.17.0 / baseline 9.16.1）与 E000 可用。四个数值与草稿一致：home_legacy 767 类/87 compose 方法/204 边/fingerprint 7a842bbb…→766/87/198/a56da1e1…；home_new_frame 196/33/49/4a3e9002…→196/33/52/34c59fa3…。E003 两侧 families 仅给出 summary，未附任何 class_samples，protocols 两侧均为空，因此本页无法列出“哪个类变了”，草稿对此保持未知是正确的，未把 fingerprint 变化写成新样式或旧样式消失。两条路径的 evidence 值均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，path_reviews 的 status 逐字沿用，未出现“已适配/通过”。两处需保留的不确定性：其一，legacy 侧类数 -1 而调用边 -6、new_frame 侧边 +3 而类数与 compose 方法数不变，方向差异可能来自重命名、内联或包装层变化，静态无法区分；其二，模块侧候选文件（HomeFrameTabLocator、HomeFrameListHook、HomeBannerFeatureInstaller、HostHomeCardSpacingHooks 等）本会话未读，E013/E014/E017 属评论家族、E018 属动态家族，均不能外推到首页定位条件，故“可能静默不命中”只能作为待验证推断。另需注意 home 家族 protocols 为空、resource_change_counts 显示 7121 个变更资源，服务端开关与资源驱动的样式差异可能静态完全不可见。页面评估文字与补证任务方向正确，无需修订。
证据：E003, E000

### 复核页面：search
复核确认：E004（fresh 预取）显示 search_native 1702/2/2859/28a11ecd…→1705/2/2818/28e67919…，search_compose 3141/561/595/fcde68da…→3146/562/614/4e4c7892…；两条 MOSS 协议两侧完全一致（java 24 定义/22 边，kotlin 52 定义/18 边），与草稿一致。E004 的 protocols 段同样只有 summary，未给出任何调用者样本，因此“调用边数不变”只能停在计数层，不能推出消费者集合未变；草稿明确写了定义数与调用边数不同单位、禁止相除推覆盖率，这一点成立。E000 的 unregistered_protocols 确实含 app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/SearchMoss 等多条搜索相关未登记协议，故“数据面存在未登记通道”是事实而非猜测；但草稿没有对这些未登记协议在 target 包中是否真有调用边下结论，属正确留白。两条路径 status 逐字为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，无适配结论。需保留的缺口：SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller、SearchHomeRecommendPolicy、SearchHomeRecommendLocator 本会话均未读取，定位条件与兜底分支未知；搜索结果的样式分派是否受服务端实验或宽屏/平板形态影响，静态不可见。页面评估无需修订。
证据：E004, E000

### 复核页面：detail
复核与 E005 逐项一致：detail_legacy 两侧 0 类/0 Compose 方法/0 外部调用边、指纹同为 4f53cd…（空集哈希），草稿保留 absent 且明确“不等于功能消失”，未升级为结论；detail_theseus_ugc 1946→1975 类、510→547 边、Compose 25→25、指纹 672508…→aba2db…；detail_theseus_united 4581→4633 类、4257→4199 边、Compose 99→98、指纹 b0f0b0…→56c25b…，类增边减的反向组合被正确归为调用解析/内联/重复包装层候选，而非“样式收敛”，符合“结构哈希变化不等于新样式”的要求。协议侧 detail_java_moss 定义 32/边 35 两侧一致，detail_kotlin_moss 定义 76 不变而实际调用边 10→38，草稿据此判定“契约未变、消费者或调用点增多”并把跨家族消费者分析列入补证，未用定义数与边数相除推算覆盖。三条 path_reviews 的 status 逐字沿用静态矩阵取值，各自给出已知状态、变化、影响、验证方法与证据编号，runtime_enabled 全程保持 unknown。两点需在后续收紧：其一，页评估把评论区线索（E011 comment_compose 家族、E013/E014 评论源码）作为详情页佐证，但 E014 写死的三个 handler FQN 位于 com.bilibili.app.comment3 原生外观家族（comment_native_*），其家族证据本会话未随 E005 下发，F007 已按此改写措辞以免证据越界；其二，两家族差异目前只有汇总计数，无类名单与方法体哈希 diff，平板/宽屏布局与详情页服务端样式开关未读到，相关分支保持未知。
证据：E000, E005, E013, E014

### 复核页面：pgc
复核与 E006 一致：pgc_legacy 类 354→352、外部边 399→425、Compose 两侧 0、指纹 2c5cf1…→60c886…；pgc_theseus 类 2265→2276、Compose 131→134、外部边 782→1179、指纹 4df56d…→44b6f7…。两条 path_reviews 的 status 均为 static_invoke_observed 并逐字沿用静态矩阵，未出现“通过/已适配”表述；对奖惩方向的异常组合（legacy 类减边增、theseus 边增速远高于类增速）分别给出解析差异、内联/包装层、DEX 重排与真实新调用者两类互斥解释，并明确“方法定义数与调用边数不是同一单位”，未做覆盖率除法。协议侧 pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧完全一致，草稿据此判定 MOSS 契约未迁移、差异更可能落在页面内消费者与安装器覆盖，该推断与证据相符；同时明确协议标识不计入路径评审。缺口在页面内证据仍只有汇总计数与每家族两个类样本：未做类名单/方法体哈希 diff，未读取 PgcAutoActivityPopupLocator 在 9.17.0 的命中记录，宽屏/平板分支、自动弹窗触发条件与服务端开关均未读到，故这些分支保持未知，F008 亦维持 candidate 级别。
证据：E000, E006

### 复核页面：player
复核确认（E007，两侧重读）：player_java 与 player_kotlin 均为 static_invoke_observed，runtime_enabled=unknown，module_coverage=requires_installer_review，本页不存在任何可升级为适配结论的路径。player_java 953 类/0 Compose/3308 边/指纹 f355088b… 对基线 958/0/3222/2830eeae…，类减 5、边增 86；player_kotlin 455 类/37 Compose 方法/841 边/b9a6ea0f… 对基线 7/0/100/c20595ba…，类数约 65 倍。协议侧 player_java_moss 18 定义/2 实际调用边、player_kotlin_moss 34/3 两版逐项相同。协议零变化与家族层暴涨并存，优先支持家族归类边界变化、DEX 拆分或 Kotlin+Compose 代码迁入，但真实迁移同样能产生该形态，静态不可区分；边数上升只表示静态可达路径变化，不能当作 Hook 覆盖变好。E007 的限制是每家族仅两个类样本、每协议四个调用者样本，上述数字是家族摘要而非逐类核对。播放器侧定位器（PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerCapabilityAccess）源码本单元未读，解析签名、版本分支与兜底均为未知；草稿引用的 E014 属评论家族绑定目录，仅说明模块“失败单位留在分母”的记账语义，不构成本页证据，因此本页证据项只列 E007 与 E000。E000 显示 playerunite/playeronline 协议仍未登记，18/34 个定义不是播放器协议全集。宽屏/平板与服务端 A/B 分支静态不可见，保持未知。
证据：E007, E000

### 复核页面：danmaku
复核确认（E008，两侧重读）：danmaku_legacy 为 absent、danmaku_kotlin 为 static_invoke_observed，runtime_enabled 均 unknown，本页无适配结论。danmaku_legacy 两版均 0 类/0 Compose/0 边且指纹同为 4f53cda…，属两版一致而非本次新增缺失；absent 只表示该分类规则未识别到目标实现，不能推断旧实现被删除或弹幕功能消失，需按类名/父类/关键签名在 DEX 级搜索补证。danmaku_kotlin 由 57 类/1 Compose 方法/8 外部边/323c06fe… 变为 137 类/3/162/38fdecc8…；协议侧 danmaku_kotlin_moss 定义 46 两版不变而实际调用边 4→10，danmaku_java_moss 22 定义/20 边两版一致——定义数不变而调用边增加的组合更符合新增调用方或重排后新增可达路径，但调用方家族归属（直播、互动、播放器内嵌等跨家族消费者）尚未标注，因此是否绕过净化属待验证假设。E008 每家族仅两个类样本、每协议四个调用者样本，162 条外部边未逐条归属，不得外推为覆盖结论。DanmakuPurifyFeatureInstaller/Policy 未读，净化挂点与跳过条件为未知；E013/E014 属评论家族源码，只能作为模块倾向严格字段/枚举校验的旁证，不支撑弹幕侧结论，故本页证据项只列 E008 与 E000。
证据：E008, E000

### 复核页面：story
复核通过：story_native 目标 2956 类/44 Compose 方法/1328 边对基线 2924/44/1310，指纹 b56b7342…→dafc7376…，+32 类/+18 边而 Compose 表面不变，数字与 E009 一致，状态逐字为 static_invoke_observed；草稿按重排/迁移候选处理、不判新样式，并给出两版类名+方法体哈希差集与 installer 目标复核步骤，方向正确。story_kotlin 两侧空集指纹一致、状态逐字为 absent，未把 absent 写成功能消失，另给真机布局树/类加载采样补证任务，符合规范。登记的并存路径（native/kotlin 两家族）均已覆盖，无遗漏。需保留的限定：E012 的 opusDetail 独立命名空间与 E014 的三外观并存、失败单位留分母属 comment/dynamic 侧证据，对 story 仅为类比推断而非直接观测；StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、HomeVerticalDetailRouting 的目标命中与运行时启用均未读到证据，保持 unknown，无适配结论。
证据：E009, E000, E012, E014

### 复核页面：mine
复核通过：mine_native 325/7/92→326/7/94、指纹 75f16dab…→f6b18de5…；mine_account_model 两侧 132 类/0 Compose 方法/43 边计数全等，仅指纹 2b548e1a…→db7f2792…（E010），两路径状态均逐字为 static_invoke_observed。草稿把计数全等加哈希变化归为混淆改名/方法体变化/DEX 重排候选而非新样式，符合结构哈希变化不等于新样式的限制条款。短字段名静默失败风险仅引用 E013 的 comment 侧 ComposeCommentText 实现作条件推断，未断言 mine 快照链路已失效，并安排 decompile_class 读 MineComponentSnapshotQueryContract 验证解析容忍度，边界正确；该契约源码本会话未读取，草稿未据其下结论。MineMoss/KMineMoss 未登记已在 E000 标注。mine_native 与 mine_account_model 两条登记路径均分别分析，安装器命中条件与运行时启用保持未知，无适配结论。
证据：E010, E000, E013, E014

- F001 / retained：本轮独立重读 CommentComposeCopyBridge.kt（E017，sha256 1783fcbf…，工作树 dirty）逐条核实草稿断言：resolve 仅按混淆短名 a(Long)、i(枚举且常量集合必须恰为 ORIGIN/TRANSLATING/TRANSLATION)、j、k(与 j 同型)、o/p(均须与 j 同型)、原文字段 a(String)、b/c(Long) 匹配，任一缺失或枚举不符即 return null；install 随后走 missing("missing-text-shape")→FeatureInstallResult.Skipped；action 侧用 declaredClasses.singleOrNull 选含 sourceClass 字段与一个 Long 字段的子类，失败即 ambiguous-more-action；render 侧要求非 static、含 modelClass 参数与 Composer 参数，并在上下文类型中恰好找到一个能消费 actionClass 子类的 store 字段，否则静默跳过该方法。E013 摘录与之一致，E001/E015 支持该家族签名与调用边已变化（934→1101、compose_methods 278→283、类数 2444→2428），E011 显示家族内模型/服务类仍存在。草稿已把结论限定为“可能静默降级”并给出可推翻条件（存在字段形态未变的 renderer 或模型强类型化），未把结构哈希变化说成新样式，也未声称 Hook 生效；局限（每家族仅数份类样本、未逐一读取 283 个方法）已在草稿中声明。无需修订。（E001, E011, E013, E015, E017）
- F002 / retained：E014 摘录直接证实 CommentNativeBindingCatalog 以三个字符串常量写死 LEGACY/NEXT/EXP3 全限定名，并在 owner 无 .CommentItem 后缀字段时 return emptyList，绑定方法需非 static、非 bridge/synthetic、返回 Void、参数 1..5 且含 View 型（字段为 View 子类或 getRoot 返回 View）参数；同文件 CommentFamilyCoverage 确认未装上的方法留在分母、partial 不升级为 ok。E001/E015 给出方向相反的计数（native_next 45→48 类、50→67 边；native_exp3 58→54 类、62→52 边），草稿据此提出“exp3 可能并入 next 或迁移”的推断而非结论，并明确 class 减少不等于功能消失、不等于新样式。反例（4 个类仅内部实现搬迁、三 FQN 仍存在且含 CommentItem 字段）与升级条件（FQN 改名或字段消失致 bindingMethods 为空）均已写明，可推翻性充分；未宣称适配通过。保留。（E001, E014, E015）
- F003 / revised：数据面断言（dynamic_opus 1352→1350 类、compose_methods 92→94、外部边 186→226 即 +40、签名全变，且与 legacy -76、compose +51 类并存）由 E002/E016 支持；E012 的样本确实全部落在 kntr/app/following/opusDetail/api 且无 compose_signatures，支持“存在非 Compose 装配/拦截层”的推断。但草稿写“DynamicPurifyFeatureInstaller 本轮未读、模块侧定位器覆盖记未知”，本轮已读 E018，需据实修订：该安装器装点为 dynamic.purify.moss 的 DYNAMIC_MOSS_CLASS 与 KotlinDynamicMossWatch.K_MOSS_CLASS，按 FEED_METHODS/ROOT_FEED_METHODS 的 reply 类与 asyncName 解析并要求 listBuilder/clearTopicList/upList/wholeUpList 成员存在，未命中即 missing("no-dynamic-hook-point") 或 partial，源码中未见对 opusDetail.api/CompositeExternalInterceptor 的解析点。因此把“模块是否覆盖 opus 装配链”从纯未知改为“该安装器静态未见覆盖，其余安装点仍未读”，同时保留编译器合成 ContinuationImpl/lambda 与广告/统计分支两种替代解释，维持 candidate 级别，不外推为功能失效。（E002, E012, E016, E018）
- F004 / retained：逐项核对通过。(1) 数值全部与 E003 一致：legacy 767/87/204/7a842bbb… → 766/87/198/a56da1e1…，new_frame 196/33/49/4a3e9002… → 196/33/52/34c59fa3…。(2) “E003 未落出 home 家族类样本”属实：E003 两侧 families 下只有 summary 键，无 class_samples，protocols 为空，草稿对该缺口的自述准确，未用截断样本外推。(3) 影响面表述被限定为“可能失配/可能不命中”，并给出可推翻条件（改名对齐后方法体哈希一致即判为混淆/重排噪声），符合结构哈希变化≠新样式的口径。(4) level=candidate 恰当：既无类级方法体哈希比对，也无任何 home/search 相关 module_source 读取（E013/E014/E017 属评论家族、E018 属动态家族，均不可外推），不能升为 static_evidence。未发现把低计数或未检出误判为新样式的问题。（E003, E000）
- F005 / revised：核心事实全部与 E004/E000 吻合（search_native 类增 3 而边减 41；search_compose compose 方法 +1 而边 +19；两条 MOSS 两侧 24/22 与 52/18 完全一致；unregistered_protocols 确含多条 SearchMoss 相关通道），保留该发现。需修订两点：其一，evidence 中的建议出现“记录搜狗推荐是否走新入口”，在本单元全部证据里没有任何依据，属无出处的具体化，必须删除；其二，E004 的 protocols 段只有 summary、无调用者样本，草稿未点明这一抽样边界，应在分析中显式写明“计数相同仅证明已登记协议的数量面未变，消费者集合未取证”，避免读者把计数一致当成消费者未变。（E004, E000）
- F006 / retained：核对通过，但需明确其证据边界（该边界草稿已自行写明，故不必修订）。事实层：E000 中四条路径 runtime_enabled=unknown、module_coverage=requires_installer_review，home/search 的 complete_coverage=false、status=installer_and_runtime_validation_required；E003/E004 两侧同样标注 runtime unknown。E014（CommentNativeBindingCatalog/CommentFamilyCoverage，sha256 b9767153…）确为评论家族实现，其“失败单位留在分母、类存在不能升级为完整覆盖”的记账语义只能说明这类计数是安装期统计而非运行期证明，草稿已显式排除把它当作 home/search 已覆盖的证据，未发生外推；真正支撑本发现的是 E000 的字段本身。E013/E017（CommentComposeCopyBridge）与 E018（DynamicPurifyFeatureInstaller）同属其他家族，本会话不存在任何 home/search 的 module_source 读取记录，故“HomeFrameTabLocator、SearchHomeRecommendLocator 等匹配条件未知”成立，不能推测 Hook 覆盖。level=needs_runtime 恰当：结论落在“启用与覆盖需真机安装/命中日志”。唯一残余问题是该发现标题覆盖 home+search 四条路径而 page 字段登记为 search，属跨页归并，不改页（页字段不可通过补丁变更），已在 remaining_gaps 说明。（E000, E003, E004, E014）
- F007 / revised：核心事实链成立且可复核：E014 给出 CommentNativeBindingCatalog 三个写死 FQN（LEGACY/NEXT/EXP3）、EXP3→NEXT→LEGACY 顺序、bindingMethods 的 CommentItem 字段前置判定与失败单位留在分母的注释；E013/E017（同一文件 sha256 1783fcbf…）给出 CommentComposeCopyBridge 按字段形状（a/i/j/k/o/p + 三值枚举）解析并注明 20 份 APK 核对，说明“按名解析”与“按形状解析”是两条独立路线，前者改名即静默落空。推断部分（半覆盖、静默降级为 partial/skipped）已标注为推断并给出待验证项，不与事实混写。需修正的是证据范围：三个 FQN 属 com.bilibili.app.comment3 原生外观家族（comment_native_*），而 E011 是 comment_compose 家族（2428 类/283 Compose 方法/1101 边，样本仅 kntr/common/comment/*），不能也不应被当作这三个 FQN 的存在性证据；E005 只覆盖 detail_theseus_ugc/united/legacy 计数，只能说明承载评论区的主页面静态可观测。原分析把三者并列易被读成同一家族的覆盖缺口，故修订措辞、保留 candidate 级别与全部原证据编号。（E014, E011, E013, E005）
- F008 / retained：数字与 E006 完全一致（pgc_theseus 类 2265→2276、Compose 131→134、外部边 782→1179；pgc_legacy 类 354→352、边 399→425），且 MOSS 两侧一致（player 12 定义/3 边、view 14 定义/7 边）的引用也准确。分析明确声明“方法定义数与调用边数不是同一单位”，拒绝用 +397 与 +11 相除推算覆盖率，把边增长列为结构性提示而非失效结论；同时给出互斥解释（新增真实消费者 vs 反编译解析更完整/内联与重复包装层/DEX 重排）与可推翻条件，并把 Compose +3 明确标为样式候选、指出服务端 A/B 变体在无结构变化时静态不可见。级别 candidate 与“待真机验证、runtime_enabled 保持 unknown”一致，无夸大，无需修订。（E006）
- F009 / revised：数字与 E007 逐项一致（953/3308/f355088b… 对 958/3222/2830eeae…；455/37/841/b9a6ea0f… 对 7/0/100/c20595ba…；协议 18/2 与 34/3 两版相同），level=candidate 与“未能区分归类迁移/真实迁移”这一状态相符，核心技术判断保留。需修订两点：1）草稿在 player 发现中把 E014（CommentNativeBindingCatalog/CommentFamilyCoverage，评论家族）作为模块证据引用，跨家族旁证容易被读成 player 安装器证据，需在正文明确其只承载记账语义检查而不构成命中/失败证据；2）草稿以“源码清单内含 PlayerSpeedLocator 等”直接推出“锚点若改变会静默失败落兜底”，但本单元未读过任何一份 player 定位器正文，解析签名与兜底分支均未知，该句必须标为待验证推断，并补上 E007“每家族两个类样本”的抽样限制。证据本身不支持升级或拒绝。（E007, E000, E014）
- F010 / retained：逐项与 E008 对齐：danmaku_kotlin 57→137 类、Compose 1→3、外部边 8→162、指纹 323c06fe…→38fdecc8…；danmaku_kotlin_moss 定义 46 不变而实际调用边 4→10；danmaku_java_moss 22 定义/20 边两版一致；danmaku_legacy 两版 0 类 0 边、指纹同为 4f53cda…。断言边界也正确：absent 被明确限制为“静态矩阵未识别”，未升级为“旧实现删除/功能消失”；新增调用方归属于未核实，只提出“可能绕过净化挂点”的待验证假设并给出证伪条件（真机全类型净化成功、或 6 条新增边调用方在基线已存在）；E013/E014 明确标注为评论侧源码、不覆盖弹幕安装器，属旁证而非结论依据。未发现把低计数、absent 或服务端条件误判为新样式的表述，也未见以定义数除调用边数推算覆盖率的错误，故原文保留。（E008, E000, E013, E014）
- F011 / retained：逐项核对成立：E009 证实 story_native 目标 2956 类/44 Compose 方法/1328 边对基线 2924/44/1310，指纹 b56b7342…→dafc7376…，+32 类/+18 边而 Compose 表面不变，数字与断言一致；story_kotlin 两侧空集指纹一致、按 absent 处理正确。E012（opusDetail 独立命名空间）与 E014（LEGACY/NEXT/EXP3 并存、失败单位留分母）为 comment/dynamic 侧证据，草稿仅作类比推断并明确标注未知与待验证假设，未越界。备择解释覆盖重排/迁移/installer 全命中/家族归属错误四条推翻路径，level=needs_runtime 与静态不可判性匹配，引用的证据编号均真实。保留。（E009, E000, E012, E014）
- F012 / retained：核对成立：E010 证实 mine_account_model 两侧 132 类/0 Compose 方法/43 边计数全等，仅指纹 2b548e1a…→db7f2792…，草稿按混淆改名/方法体变化/DEX 重排候选处理而非新样式，符合结构哈希变化不等于新样式。E013 的短字段名（a/i/j/k）+枚举名集合+类型护栏+runCatching 返回 null 模式属实，草稿以条件句（若 mine 快照链路采用同类解析）引用，未断言该链路已失效，并给出字段表/方法体哈希 diff、decompile_class 读 MineComponentSnapshotQueryContract、真机 null 率三步可证伪验证；MineComponentSnapshot 系列源码本会话未读，草稿未据此下结论。level=candidate 恰当，证据编号真实。保留。（E010, E013, E014, E000）

### 尚未解决的证据缺口

- [1] comment_native_legacy/next/exp3 三个 handler FQN 在 9.17.0 中是否仍存在、是否仍有 .CommentItem 字段，未按名反编译确认；exp3 消失的 4 个类是迁移进 next/legacy 还是实验下线仍未定（E014 仅给出模块侧常量与判定逻辑）。
[2] CommentComposeCopyBridge 依赖的 kntr/common/comment 模型类（MODEL 常量所指类）在 9.17.0 上 a/i/j/k/o/p/b/c 字段类型与 ORIGIN/TRANSLATING/TRANSLATION 三常量是否仍成立，本轮只读模块源码（E013/E017），未读宿主模型类。
[3] comment_compose 家族 283 个 compose 方法中，带 modelClass+Composer 参数且非 static 的 renderer 数量与新增调用边落点未逐条清点；方法定义数与调用边数不同单位，禁止相除得覆盖率。
- [4] comment_kotlin_moss 实际调用边 26→23 的 3 条消失边调用方未逐条比对，无法区分调用方迁移与其它原因（E001/E015）。
[5] dynamic_compose 类数 +51、compose_methods +14 未做类级“类名+方法体哈希”diff，无法排除 DEX 重排、类拆分或包装层导致的计数增长（E002/E016）。
[6] dynamic_legacy 外部边 -76 的消失边原调用方与目标方法未定位，削薄是否触及正文/转发渲染锚点未知。
- [7] dynamic_opus +40 条增密边的调用方未列出；CompositeExternalInterceptor 是否仅服务广告/快照分发、是否连接正文富文本字段均未读，编译器合成与广告分支两种替代解释未排除（E012）。
[8] DynamicTabsFeatureInstaller、KotlinDynamicMossWatch 源码仍未读，动态页是否存在 Moss 边界之外的装点与兜底未知；DynamicPurifyFeatureInstaller 本轮只读到截断段（E018）。
[9] 未登记协议的消费者未归类：app/dynamic/v1/DynamicMoss、app/dynamic/v2/OpusMoss/KOpusMoss、dynamic/interfaces/feed/FeedMoss、main/community/reply/v2/ReplyMoss 等，是否存在跨家族消费者无法静态排除（E000）。
- [10] 两侧所有登记路径 runtime_enabled 均为 unknown，没有真机安装/命中日志；CommentFamilyCoverage 与动态侧安装结果（ok/partial/missing）均未采集，静态观察不得升级为已适配（E014/E018）。
[11] 平板/宽屏与折叠屏布局下的样式选择、服务端 A/B 开关是否切换 comment/dynamic 家族，未读到运行条件；无结构变化时静态不可见，保持未知。
[12] 源码为 working_tree_dirty 快照（source_tree_sha256 37745f8f…，head 5422fad1…），E013/E014/E017/E018 结论需按文件 sha256 追溯；若工作树后续变动需重新对齐。
- [13] unmapped_multi_path_candidates 中的 KotlinMossChannel.kt、KotlinMossReplyBridge.kt、ReplyTopologyComposeMenu.kt 等未归入任何登记安装器，评论/动态相关装点是否经此类文件注册未知（E000）。
[14] home 与 search 四家族的类级证据仍缺：E003/E004 只有家族 summary，无 class_samples，因此“哪个类/方法变了”未定；下一步需按家族取 target/baseline 具名类做方法体哈希对齐比对，并单列差异类。
[15] home/search 相关的模块源码在本会话均未读取（HomeFrameTabLocator、HomeFrameListHook、HomeBannerFeatureInstaller、HomeComponentFilterFeatureInstaller、HomeTabFilterFeatureInstaller、HomeTopBarFeatureInstaller、HostHomeCardSpacingHooks、SearchDefaultWordsCleaner、SearchPurifyFeatureInstaller、SearchHomeRecommendFeatureInstaller、SearchHomeRecommendPolicy、SearchHomeRecommendLocator），其类名/字段匹配条件、版本分支与失败兜底仍为未知；不得用评论家族 E013/E014/E017 或动态家族 E018 的读取结果替代。
- [16] search 两条已登记 MOSS 协议只有定义数与调用边数摘要，无调用者样本，跨家族（Java↔Kotlin）消费者是否存在未取证；unregistered_protocols 中的 app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss、broadcast/message/main/SearchMoss 在 target DEX 中是否有实际调用边尚未确认。
[17] 四条路径的 runtime_enabled 与安装器覆盖全部为 unknown：缺少模块安装日志（家族 installed/partial/failed 与 complete 标记）与运行期命中日志，“安装成功”与“运行期命中”未区分。
[18] home 家族 protocols 为空，且两版资源变更量很大（changed 7121 / added 15），服务端开关与资源驱动的首页样式差异可能静态完全不可见；平板/宽屏/折叠屏形态下走 home_new_frame 还是 legacy 未取证。
- [19] search 页样式是否受服务端实验开关控制、宽屏布局是否改变分派路径，静态不可见，须真机比对；在取得运行条件前，所有路径保持 unknown，不宣称样式已穷尽。
[20] 源码为 published_unverified_worktree（working_tree_dirty=true，head 5422fad1…，tree 37745f8f…），后续结论须按文件 sha256 追溯所读版本。
[21] F006 标题覆盖 home 与 search 四条路径而 page 字段登记为 search，属跨页归并；本轮按不可变更页字段保留，若需精确归属应在下一轮拆分为分页发现。
- [22] 发现可复核性的共同反例尚未排除：若差异类在改名/重排对齐后方法体哈希一致，则应把 home/search 的 fingerprint 变化登记为打包噪声并更新静态矩阵备注。
[23] detail_theseus_ugc/united 目前只有汇总计数与每家族两个类样本，缺“类名单+方法体哈希”diff，无法区分混淆改名、DEX 重排、内联/包装层与真实结构变化（尤其 united 类 +52 而边 -58 的反向组合）。
[24] detail_legacy 两侧均 absent，无运行期锚点证据，无法判定是静态特征未命中还是该路径在 9.17.0 不再启用；需真机详情页类清单采样。
- [25] F007 涉及的三个 handler FQN（LEGACY/NEXT/EXP3）在 9.17.0 的存在性仍未取证；comment_native_legacy/next/exp3 家族证据本会话未下发，E011（comment_compose）与 E005（detail_theseus_*）不能替代。
[26] CommentFamilyCoverage 的 record(family, installed/FeatureInstallResult) 与 complete 标志没有任何运行期输出，无法区分“类不存在”与“类存在但 bindingMethods 被前置条件过滤为空”。
[27] detail_kotlin_moss 实际调用边 10→38 的调用方未定位；KotlinMossChannel.kt、KotlinMossReplyBridge.kt 仍在 unmapped_multi_path_candidates，其归属安装器与覆盖调用者未知。
- [28] pgc_theseus +397 条外部调用边未按调用方聚类，未抽样读取新增调用方方法体，真实消费者扩张与解析差异两种解释仍未分离。
[29] pgc_legacy 类 -2 而边 +26 的反向组合尚无用例解释，缺类名单与方法体哈希 diff。
[30] PgcAutoActivityPopupLocator/PgcAutoActivityPopupPolicy 在 9.17.0 的解析命中与兜底分支未读取，自动弹窗触发条件与服务端开关未知。
- [31] 番剧/影视页宽屏与平板布局走 pgc_legacy 还是 pgc_theseus 的切换条件未读到，相关分支只能保持未知；静态不可见的服务端 A/B 变体不能宣称已穷尽。
[32] 所有登记路径 runtime_enabled=unknown、module_coverage=requires_installer_review，无任何安装器 installed/partial/skipped 日志，适配结论不成立。
[33] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，head 5422fad1…），后续结论需按文件 sha256 追溯；本轮未核对 E013/E014 之外模块源码在 9.17.0 的实际命中行为。
- [34] player 定位器源码（PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、PlayerCapabilityAccess、PlayerQualityFeatureInstaller）本轮未读，解析签名、版本分支与兜底分支仍为未知，F009 的影响面只能保持推断级。
[35] player_kotlin 新增的 448 个类尚未在 9.16.1 其他家族中做类名+方法体哈希反查，“归类重映射”与“Kotlin 播放器真实扩编”两种解释无法在本轮区分。
[36] player_java 减少的 5 个类未做逐类对齐，无法判断是迁入 player_kotlin、改名还是合并。
- [37] danmaku_kotlin_moss 的 46 个定义方法体哈希未对齐，协议层“零变化”目前只依据定义数不变这一弱证据。
[38] danmaku_kotlin 的 162 条外部边与 10 条 moss 调用边的调用方类未逐条列出并标注家族归属，直播、互动、播放器内嵌等跨家族消费者是否构成未被净化路径仍未知。
[39] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 未读，净化挂点、跳过条件与失败兜底均未知，“新增调用方绕过净化”缺乏源码层判据。
- [40] danmaku_legacy 的 absent 仅为分类规则未识别，尚未按 legacy 弹幕类名/父类/关键签名在两侧 DEX 级搜索，不能判定实现是否真实存在或是否被改名并入其他家族。
[41] 两页全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，真机安装器日志（各定位器 resolved/failed、complete 标记、CommentFamilyCoverage 类似的 record 输出）尚未采集，安装成功与运行期命中未区分。
[42] E007/E008 预取限制为每家族两个类样本、每协议四个调用者样本；按名重读完整家族与协议清单的抽样复核尚未执行，结论不得外推为逐类覆盖。
- [43] unregistered_protocols 中 playerunite PlayerMoss/KPlayerMoss 与 playeronline PlayerOnlineMoss/KPlayerOnlineMoss 是否构成播放器协议缺口、是否有跨家族实际调用边，尚未核定与补登记。
[44] 宽屏/平板布局与服务端 A/B 开关下的样式选择在两侧均无结构证据，静态不可见，保持未知，不得宣称样式已穷尽。
[45] 源码为 working_tree_dirty 快照（head 5422fad1…，source_tree_sha256 37745f8f…），player/danmaku 相关模块文件的 sha256 追溯尚未落实，结论需按文件哈希而非目录状态追溯。
- [46] story_native 新增 32 类/18 条边的端点未定位，未做两版类名+方法体哈希差集，重排/迁移/新增实现未判定（E009）
[47] StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、HomeVerticalDetailRouting、HomeVerticalDetailFeatureInstaller 的目标类名/签名在 9.17.0 是否仍存在未用 JADX 逐一复核
[48] story_kotlin absent 的原因（家族命名空间未纳入扫描 vs 确无 Compose 调用边）未判定，需真机布局树与类加载采样
- [49] mine_account_model 的指纹变化未做字段表/方法体哈希逐项分类（重命名/方法体重写/类搬迁）（E010）
[50] MineComponentSnapshotQueryContract/Store/HostBridge 与 HostMineReadingCard 是否硬编码混淆短名未读源码，静默失败假设未证实
[51] MineVipFeatureInstaller 与 MineComponentFilterFeatureInstaller 对 mine_native 新增 1 类/2 条新调用边的覆盖与命中条件未知
- [52] StoryMoss/KStoryMoss、MineMoss/KMineMoss 在未登记协议清单（E000），跨家族消费者与共同协议实际调用边分析缺失，需补登记或标注未归类调用者
[53] 服务端 A/B 下发的 story/mine 新样式若无结构变化则静态不可见，样式穷尽性不可声明，相关分支保持未知
[54] 平板/宽屏/折叠屏形态下 story 与 mine 的并存栈与切换条件无任何证据
- [55] 真机 9.17.0 上 story/mine 的模块安装结果（Installed/失败单位/跳过原因）与 hook 命中日志未采集，全部路径 runtime_enabled 保持 unknown，不得宣称适配通过
[56] 源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，head 5422fad1…），E013/E014 深挖结论需按文件 sha256 追溯，后续源码变更需重新对齐
[57] sample 的 7121 个资源变更与 15 个新增资源是否涉及 story/mine 布局或合规改动未核对，仅作为结构哈希变化不等于新样式的反向核对项（E000）

## 下一步

- [1] 按名重读 kntr/common/comment 模型类字段（a/i/j/k/o/p/b/c 与三值枚举），确认 ComposeCommentText.resolve 在 9.17.0 上是否仍成立。
[2] 按三个 handler FQN 复查 com.bilibili.app.comment3.ui.*handle 包，确认 CommentNativeBindingCatalog 常量与 CommentItem 字段判定是否仍命中。
[3] 用方法体哈希反查 comment_native_exp3 缺失的 4 个类是否迁移进 next/legacy 包，区分实验下线与单纯重构。
[4] 定位 comment_compose 新增约 167 条外部边中落在 renderer/dispatch 覆盖范围内的比例，逐条标注调用方，不得以方法数相除推算覆盖率。
[5] 读取 DynamicPurifyFeatureInstaller / DynamicTabsFeatureInstaller / KotlinDynamicMossWatch 源码，核对动态三家族与 opusDetail 包的定位器与兜底（当前记为未知）。
- [6] 反编译 CompositeExternalInterceptor 及调用方，判定 dynamic_opus +40 条边属于广告/统计分支还是正文卡片链路。
[7] 核对未登记协议 app/dynamic/v1/DynamicMoss、v2/KOpusMoss/OpusMoss、main/community/reply/v2/ReplyMoss 的消费者是否落在登记家族内，补登或标记为未归类调用者。
[8] 真机验证清单（需开启模块并抓日志）：Compose 评论长按复制、三套原生外观分别进入评论详情、Compose/旧版动态流长按、Opus 详情页净化，逐项记录 CommentFamilyCoverage 与动态侧安装结果。
[9] 补齐平板/宽屏布局与服务端 A/B 开关下的样式选择证据；静态不可见的分支明确保持未知，不得宣称样式已穷尽。
[10] 按 E013/E014 的文件 sha256 记录源码工作树 dirty 状态对应的版本，后续若源码变更需重新对齐深挖结论。
- [11] 对 home_legacy 与 home_new_frame 分别用 family_evidence 取 target/baseline 具名类，做方法体哈希对齐比对，产出差异类清单
[12] 对 search_native 与 search_compose 做同样的类级方法体哈希比对，特别核对 compose 方法增量（561→562）对应的具体签名
[13] 用 protocol_evidence 拉取 search_java_moss 与 search_kotlin_moss 的调用者类，交叉检查是否存在跨家族（Java↔Kotlin）消费者
[14] 确认 unregistered_protocols 中 app/interfaces/v1/SearchMoss、app/search/v2/SearchMoss、broadcast/message/search/SearchMoss 在 target 包内是否具有实际调用边
[15] 读 HomeFrameTabLocator 与 HomeFrameListHook，记录帧 Tab 的类名/字段匹配条件及失败兜底，按文件 sha256 追溯 working_tree_dirty 状态
- [16] 读 SearchHomeRecommendLocator 与 SearchHomeRecommendPolicy，记录搜索首页推荐的定位条件与兜底分支
[17] 读 SearchDefaultWordsCleaner 与 SearchPurifyFeatureInstaller，确认默认词清理依赖的数据来源是否落在已登记 MOSS 通道
[18] 真机在首页逐开关（顶部栏、Banner、推荐净化、Tab 过滤、Tab 底色、卡片间距）采集命中与未命中日志
[19] 真机在搜索页验证默认词、热搜、搜索首页推荐三处，并记录是否受服务端实验开关控制
[20] 在平板/宽屏与折叠屏形态下重复首页与搜索页验证，确认宽屏走的是 home_new_frame 还是 legacy 帧
- [21] 采集模块安装日志中的家族安装结果，区分“安装成功”与“运行期命中”，不得混用为覆盖结论
[22] 若差异类方法体在改名对齐后完全一致，则将 home/search 的 fingerprint 变化登记为混淆/DEX 重排噪声并更新静态矩阵备注
[23] 对 9.17.0 精确检索三个评论 handler FQN（LEGACY/NEXT/EXP3）是否存在，并检查是否出现新的 exp 变体类名；结果用于判定 CommentNativeBindingCatalog 是部分命中还是完全落空。
[24] 真机采集 CommentFamilyCoverage 的 record(family, installed) 与 complete 输出，区分“类存在但方法被前置过滤”与“类不存在”两种落空形态，失败项保留在分母。
[25] 导出 detail_theseus_ugc / detail_theseus_united 两侧类名单与方法体哈希 diff，区分混淆改名、DEX 重排、重复包装层与真实结构变化，再谈样式候选。
- [26] 对 detail_theseus_united 减少的 58 条调用边做端点定位，抽样 1-2 处确认是内联/包装层变化还是调用路径被移除。
[27] 核验 detail_kotlin_moss 实际调用边 10→38 的具体调用方，确认新增消费者是否落在 KotlinMossChannel.kt / KotlinMossReplyBridge.kt 的注册范围内；这两个文件当前处于 unmapped_multi_path_candidates，先确定其归属安装器。
[28] 对 pgc_theseus 的 +397 条调用边按调用方聚类，抽样 2-3 个新增调用方读取方法体，判断新消费者与解析差异。
[29] 在 pgc_legacy 与 pgc_theseus 各自的详情/播放页（含平板/宽屏布局）触发一次，输出 PgcAutoActivityPopupLocator 的解析与兜底日志，确认服务端开关与切换条件。
[30] 记录源码为 dirty 快照（source_tree_sha256 37745f8f…，head 5422fad1…），后续结论按文件 sha256 追溯，不清理工作树。
- [31] 补证 detail_legacy 的运行期锚点：真机详情页类清单中检索 legacy 详情特征，确认 absent 是静态未命中还是该路径确实不再启用。
[32] 真机验证项统一标注为待验证，静态观察不得升级为“已适配”；所有路径的 runtime_enabled 在取得启动日志前保持 unknown。
[33] 按类名+方法体哈希对齐 9.16.1 与 9.17.0 的 player_java / player_kotlin 类清单，判定 -5 类与 +448 类是迁移、重命名还是归类边界变化。
[34] 把 player_kotlin 新增的 448 个类在基线其他家族中反查，若命中则改写本次结论为归类重映射而非新播放器实现。
[35] 读取 PlayerSpeedLocator / PlayerSpeedSessionLocator / PlayerBufferLocator 源码，列出声明的解析签名、版本分支与兜底路径。
- [36] 真机安装模块后采集安装器日志中各 player 定位器的 resolved/failed 与 complete 标记，并实际切换倍速、缓冲、清晰度验证生效。
[37] 对齐 danmaku_kotlin_moss 的 46 个定义方法体哈希，确认协议层是否真的零变化。
[38] 列出 danmaku_kotlin 的 162 条外部边与 10 条 moss 调用边的调用方类，逐一对两版比对并标注家族归属（含直播/互动等跨家族消费者）。
[39] 读取 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy，确认净化挂点、跳过条件与失败兜底是否覆盖新增调用方。
[40] 真机分别对普通视频、直播、互动弹幕开关净化，记录未被净化的弹幕类型与对应日志，作为绕过假设的判据。
- [41] 核对 unregistered_protocols 中 playerunite / playeronline 系列是否存在跨家族消费者，决定是否补登记为播放器协议。
[42] source_dirty=true：按文件哈希与快照 head 5422fad1 追溯涉及的 player/danmaku 模块源码，避免把未提交改动当作已发布实现。
[43] APK 访问当前被禁用（apk_access_disabled=true），结构提取需在访问恢复后重跑，本报告结论限于既有冻结证据。
[44] 对宽屏/平板布局与服务端 A/B 开关补充说明：无结构变化时静态不可见，相关路径只能标为未知并等待真机比对。
[45] 导出 9.16.1 与 9.17.0 两版 story 家族的“类名+方法体哈希”清单并做差集，标注 32 个新增类与 18 条新边的命名空间归属（对应 E009）。
- [46] 用 JADX 逐个核对 StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller、HomeVerticalDetailRouting 的目标类名与参数类型在目标 APK 中是否仍存在。
[47] 对两版 mine_account_model 做字段表与方法体哈希逐项对比，把差异分类为重命名/方法体重写/类搬迁并计数（对应 E010）。
[48] 用 decompile_class 读 MineComponentSnapshotQueryContract、MineComponentSnapshotStore、MineComponentSnapshotHostBridge 的字段解析逻辑，确认是否硬编码混淆短名及是否有类型/枚举护栏（参照 E013 的模式）。
[49] 核对 MineComponentFilterFeatureInstaller 与 MineVipFeatureInstaller 的目标签名、安装器命中条件与兜底分支，确认 mine_native 新增 1 类/2 边是否落在未覆盖调用者上。
[50] 真机（9.17.0）分别进入 story 页与 mine 页，采集模块安装结果日志（Installed/失败单位/跳过原因），区分“解析失败”与“解析成功但样式不同”。
- [51] 真机在 story 页做布局树与类加载采样，判定是否存在未登记的 Compose/Kotlin 实现，补登记 story_kotlin 的 absent 缺口。
[52] 在 mine 页记录账号区块快照、会员卡与阅读卡的取值结果（null/默认值比例），验证短名解析是否静默降级。
[53] 补登记协议证据：把 StoryMoss/KStoryMoss、MineMoss/KMineMoss 纳入协议矩阵，按家族列出消费者与实际调用边，当前未登记导致跨家族消费者分析缺失（E000）。
[54] 排查 sample 中 7121 个资源变更与 15 个新增资源是否伴随布局/合规改动，作为“结构哈希变化≠新样式”的反向核对项。
[55] 复核阶段需重读 prefetch 截断部分（每家族仅两个类样本、每协议四个调用者样本）与 source_dirty=true 的固定源码快照，确认结论未建立在抽样样本之上。