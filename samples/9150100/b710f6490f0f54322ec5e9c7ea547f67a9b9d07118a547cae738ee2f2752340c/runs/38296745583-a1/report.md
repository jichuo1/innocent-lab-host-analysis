## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2420 | 274 | 938 | static_invoke_observed |
| comment_legacy_v2 | 576 | 0 | 739 | static_invoke_observed |
| comment_native_exp3 | 60 | 0 | 66 | static_invoke_observed |
| comment_native_legacy | 173 | 0 | 209 | static_invoke_observed |
| comment_native_next | 46 | 0 | 49 | static_invoke_observed |
| comment_other_ui:(root) | 221 | 2 | 498 | static_invoke_observed |
| comment_other_ui:adapter | 7 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 217 | 0 | 97 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 239 | 31 | 255 | static_invoke_observed |
| danmaku_kotlin | 57 | 1 | 10 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1951 | 25 | 494 | static_invoke_observed |
| detail_theseus_united | 4589 | 98 | 4167 | static_invoke_observed |
| dynamic_compose | 947 | 112 | 161 | static_invoke_observed |
| dynamic_legacy | 3221 | 103 | 2092 | static_invoke_observed |
| dynamic_opus | 1333 | 92 | 219 | static_invoke_observed |
| dynamic_other:appointment | 28 | 3 | 18 | static_invoke_observed |
| dynamic_other:card | 411 | 82 | 292 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 58 | static_invoke_observed |
| dynamic_other:commonPerf | 12 | 1 | 3 | static_invoke_observed |
| dynamic_other:commonUi | 20 | 5 | 10 | static_invoke_observed |
| dynamic_other:lightBrowser | 70 | 18 | 28 | static_invoke_observed |
| dynamic_other_legacy | 2095 | 4 | 2101 | static_invoke_observed |
| home_legacy | 1008 | 128 | 227 | static_invoke_observed |
| home_new_frame | 197 | 33 | 48 | static_invoke_observed |
| mine_account_model | 132 | 0 | 54 | static_invoke_observed |
| mine_native | 324 | 7 | 95 | static_invoke_observed |
| pgc_legacy | 352 | 1 | 302 | static_invoke_observed |
| pgc_theseus | 2241 | 131 | 826 | static_invoke_observed |
| player_java | 948 | 0 | 3223 | static_invoke_observed |
| player_kotlin | 7 | 0 | 100 | static_invoke_observed |
| search_compose | 3149 | 556 | 591 | static_invoke_observed |
| search_native | 1674 | 2 | 2898 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2944 | 44 | 1376 | static_invoke_observed |

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
- unregistered_protocol:Lcom/bapis/bilibili/app/home/v1/KHomeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/im/v1/KimMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KHistoryMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KMediaMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/mine/v1/KMineMoss;: protocol_signature_or_call_path_changed
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
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/message/search/SearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v1/KBroadcastRoomMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v1/KLaserMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/broadcast/v2/KLaserMoss;: protocol_signature_or_call_path_changed
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

{'added': 4, 'removed': 68, 'changed': 7455}

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

# AI 分析未完成

请求失败或达到调用限制；详情见 ai-analysis.json。不能将本次结果视为完整 AI 分析。

# AI 适配分析

AI 建议；证据引用已检查，仍须人工及真机验证。

本轮为阶段二复核。独立重读 comment、dynamic 双侧证据（E007/E008）：草稿的类数与调用边数字全部吻合，但发现一处关键错误——comment_kotlin_moss 双侧 definitions 均为 130、actual_invoke_edges 均为 26，草稿所称"调用边 50→26（-24）"不成立，实际双侧持平，F004 已修订。E007/E008 直接捕获多处混淆改名实例（评论 caller 方法 n→o、动态 caller 类 i1→e1、DynamicDetailFragment fg→gg、compose data 类 k→j），支持"指纹变化主要为 R8 漂移、非新样式"的判断。协议层 comment_java_moss（50/50）、dynamic_java_moss（134/134）、两个 Kotlin MOSS 双侧持平，方法名一致，未见协议切换。player/detail/home/search/pgc/story/mine 因工具预算耗尽未能重新读取，相关断言依据草稿会话取证（E001-E006）与目标侧矩阵交叉保留，并明确标注待复核。F003 因 baseline 数字与源码依赖均未验证，保留 needs_runtime 并注明缺口。所有路径 runtime_enabled 仍为 unknown，未登记的 comment_other_ui:*、dynamic_other:* 子家族与大量 K* MOSS 未注册协议留待补证。本报告不构成任何路径的适配验收。

## 各页面评估

### comment

复核确认（E007 双侧）：五条路径均 static_invoke_observed。目标/基线：legacy_v2 576/739 vs 586/761；native_legacy 173/209 vs 181/243；native_next 46/49 vs 47/64；native_exp3 60/66 vs 67/84；compose 2420/938 vs 2378/939。四条非 Compose 家族轻度收敛，compose 类增 42 边减 1。协议层 comment_java_moss 双侧 definitions 50、调用边 50 持平；comment_kotlin_moss 双侧 definitions 130、调用边 26 持平——草稿「调用边 50→26」系误读，已修订。caller 样本仅见混淆改名（userCallback caller 方法 n→o，doVote/answerQuestion/translateReply caller 不变），KReplyMoss(v1) 方法名双侧一致，评论 Kotlin MOSS 静态调用面未收缩。评论页是模块功能密度最高页面（净化/过滤/分节/拓扑），且 changes 中另有 7 个 comment_other_ui:* 未登记子家族标记结构变化，本轮未取证。runtime_enabled 全部 unknown，不能宣称任何 hook 命中。

证据：E000, E007, E001

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 586→576、外部调用 761→739，轻度收敛，指纹变更。
- 可能影响：CommentPurify/CommentFilter/CommentTopology 等 installer 依赖的类名与方法签名存在漂移风险，部分 hook 可能失配。
- 验证：真机 9.15.0 打开评论区对比净化/过滤命中点；读取诊断中心核查 CommentTopology 的 DexAssist 兜底日志。
- 证据：E007

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 181→173、边 243→209，收敛幅度评论页最大（边约 -14%）。
- 可能影响：原生 legacy 评论分支，如 installer 依赖该家族类名，需确认是否被内联或改名。
- 验证：真机切至原生 legacy 分支验证列表渲染与排序语义。
- 证据：E007

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 47→46、边 64→49（边约 -23%）。
- 可能影响：小家族边数下降明显，需判断是删减还是内联。
- 验证：真机在 next 分支做点击/展开链路测试。
- 证据：E007

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 67→60、边 84→66。
- 可能影响：exp3 分支轻度收敛，可能内联或删减。
- 验证：真机在实验开启状态验证 exp3 可用性。
- 证据：E007

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2378→2420（+42）、边 939→938；compose_methods 双侧 274 持平。
- 可能影响：类增边平，Compose 评论仍有内部调整；ReplyTopologyComposeMenu 等定位依赖需跟随，但本页 comment_kotlin_moss 调用边双侧持平，未见协议面收缩。
- 验证：真机验证 Compose 评论过滤/分节/拓扑功能并核查 installer 命中日志。
- 证据：E007

### dynamic

复核确认（E008 双侧）：legacy 3221/2092 vs 3193/2143（+28/-51）；compose 947/161 vs 953/143（-6/+18）；opus 1333/219 vs 1313/195（+20/+24），与草稿数字一致。协议层 dynamic_java_moss 双侧 134 定义/134 调用边、dynamic_kotlin_moss 双侧 382 定义/26 调用边持平；dynDetail/subscriptionClick/dynAllPersonal 方法名双侧一致，仅 caller 混淆改名（DynamicDetailFragment fg→gg、followinglist/service i1→e1、compose data k→j），支持「结构再分配、非协议切换」。注意 compose 同名类 A 字段形态大变（I/Object/Object → Function1/Function0/Function0/D71.C），同名混淆类不可当作同一源类对比，字段层面存在实际改动。changes 中另有 8 个 dynamic_other:* 未登记子家族标记变化，本轮未取证。runtime_enabled 全部 unknown。

证据：E000, E008, E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 +28、边 -51，收敛型，compose_methods 104→103。
- 可能影响：legacy 动态内部收敛，DynamicPurifyFeatureInstaller 语义假设可能需微调。
- 验证：真机对比 9.14.0 与 9.15.0 的动态净化命中点数量。
- 证据：E008

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 -6、边 +18，正向扩张；同名类 A 字段形态大变。
- 可能影响：字段级改动真实存在，需确认分支语义是否稳定。
- 验证：真机逐项验证 compose 分支动态卡片可见性；必要时 decompile_class 对比同名类 A。
- 证据：E008

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 +20、边 +24。
- 可能影响：扩张型修改，需确认 opus 详情页语义偏移；对应 KOpusMoss 在未注册协议变更列表中，模块覆盖未知。
- 验证：真机验证 opus 详情页内容渲染与净化。
- 证据：E008

### home

本轮因工具预算耗尽未能重新读取双侧证据；目标侧矩阵确认 legacy 1008 类/227 边、new_frame 197 类/48 边（E000），与草稿一致。「双侧数完全持平、仅指纹变化」依据草稿会话取证记录（E006 引用），标记为待复核。若成立则属改名型轻度改动，存在类名漂移或内联重写可能。无登记协议。runtime_enabled 全部 unknown，HomeTabFilter/HomeBanner/HomeVerticalDetail 等 installer 定位覆盖需真机核对。

证据：E000, E006

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，仅指纹变；本轮未独立复核。
- 可能影响：首页多 installer 依赖该家族结构，若改名超出定位器覆盖则 hook 失配。
- 验证：真机验证首页净化、tab 过滤、banner 移除命中点；补一次双侧 page_evidence 复核。
- 证据：E000, E006

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，仅指纹变；本轮未独立复核。
- 可能影响：新框架层存在类名漂移风险。
- 验证：真机验证 HomeVerticalDetailFeatureInstaller 注入是否成功。
- 证据：E000, E006

### search

本轮预算耗尽未重新读取；目标侧矩阵确认 native 1674 类/2898 边、compose 3149 类/591 边（E000），与草稿一致。草稿称二者双侧数字完全持平仅指纹变，且 search_java_moss 边 24→22（-2）、search_kotlin_moss 52 定义/18 边持平，均待复核。runtime_enabled 全部 unknown，SearchPurify/SearchHomeRecommend installer 需真机核对。

证据：E000, E006

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：草稿记录类/边完全持平，仅指纹变；本轮未独立复核。
- 可能影响：搜索页内部结构未变但类名可能漂移。
- 验证：真机验证 SearchPurifyFeatureInstaller 既有 hook 点是否命中。
- 证据：E000, E006

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：草稿记录类/边完全持平，仅指纹变；本轮未独立复核。
- 可能影响：compose 分支需单独核对。
- 验证：真机验证 search compose 分支交互链。
- 证据：E000, E006

### detail

E003 目标侧确认：detail_legacy absent（全零指纹、samples 空）、theseus_ugc 1951 类/494 边、theseus_united 4589 类/4167 边；baseline 侧摘录截断，草稿记录 ugc 1906→1951（+45）、united 4485→4589（+104），待复核。changes 列表无 detail_legacy 记录，佐证其双侧一致 absent。协议层草稿记录 detail_java_moss 双侧 32 定义/35 边、detail_kotlin_moss 双侧 76 定义/10 边持平（含 ViewMoss.executeView 与 KViewMoss.playPause 调用样本），待复核。runtime_enabled 全部 unknown。

证据：E000, E003, E006

#### 路径：detail_legacy

- 状态：absent
- 变化：双侧一致全零指纹（changes 无该路径记录，佐证未变化），非 9.15.0 单侧功能移除。
- 可能影响：静态矩阵未捕获该家族，不等价于真机侧功能消失，需区分识别边界与实际缺失。
- 验证：对 9.15.0 APK 做 dex 级 family 搜索，或真机验证是否存在 legacy 详情页。
- 证据：E000, E003

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：草稿记录类 +45、边 -5；本轮未独立复核 baseline。
- 可能影响：theseus ugc 分支类名漂移会导致 installer 失配。
- 验证：真机验证 ugc 分支 feature installer 命中。
- 证据：E000, E003

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：草稿记录类 +104、边 +27；本轮未独立复核 baseline。
- 可能影响：united 分支扩张，相关 installer 需定位核对。
- 验证：真机验证 united 分支 installer 命中。
- 证据：E000, E003

### pgc

本轮预算耗尽未重新读取；目标侧矩阵确认 legacy 352 类/302 边、theseus 2241 类/826 边（E000），与草稿一致。草稿称双侧数字完全持平仅指纹变，pgc_player_moss 12 定义/3 边、pgc_view_moss 14 定义/7 边持平，待复核。runtime_enabled 全部 unknown，PgcAutoActivityPopupFeatureInstaller（其定位器 PgcAutoActivityPopupLocator 在 E005 的 VersionAdapter 导入中可见）需真机核对。

证据：E000, E006, E005

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，仅指纹变；本轮未独立复核。
- 可能影响：轻度演进，类名漂移风险待真机确认。
- 验证：真机验证 pgc legacy 分支净化。
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，仅指纹变；本轮未独立复核。
- 可能影响：轻度演进。
- 验证：真机验证 pgc theseus 分支互动。
- 证据：E000, E006

### player

E004 目标侧确认：player_java 948 类/3223 边（样本 playerbizcommon 面板/背景类）、player_kotlin 7 类/100 边（样本 PlayHistoryMemoryStore 协程类）；baseline 侧摘录截断，草稿记录 java 962→948（-14）、kotlin 8→7、边 150→100（-33%），待复核。协议层 player_java_moss 18 定义/2 边、player_kotlin_moss 34 定义/3 边（目标侧，E000），草稿称双侧持平。player_kotlin 若边数下降属实则为全页最大收敛，但 baseline 数字与 KotlinMossChannel/KotlinMossReplyBridge 依赖断言均未验证，F003 保留 needs_runtime。runtime_enabled 全部 unknown。

证据：E000, E004, E006

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：草稿记录类 -14、边 -12；目标侧 948/3223 已确认，baseline 未复核。
- 可能影响：轻度收敛，个别基于类名的 installer 可能需重定位。
- 验证：真机验证 PlayerCodecForce/PlayerSpeed/PlayerQuality 各 hook 是否命中。
- 证据：E000, E004

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：草稿记录类 -1、边 -50（-33%）；目标侧 7/100 已确认，baseline 未复核，数值待验证。
- 可能影响：若属实为全页最大收敛，可能为编译期合并或调用入口合并，会影响相关 hook。
- 验证：补读双侧 page_evidence 验证数值；真机逐一验证播放器 Kotlin 相关 feature。
- 证据：E000, E004

### danmaku

目标侧矩阵确认 danmaku_kotlin 57 类/10 边、danmaku_legacy absent（E000）；changes 列表无 danmaku_legacy 记录，佐证双侧一致 absent。草稿记录 danmaku_java_moss 22 定义、边 22→20（-2），danmaku_kotlin_moss 46 定义/4 边持平，本轮未复核。runtime_enabled 全部 unknown，DanmakuPurifyFeatureInstaller 需真机核对。

证据：E000, E006

#### 路径：danmaku_legacy

- 状态：absent
- 变化：双侧一致全零（changes 无该路径记录，佐证未变化），非 9.15.0 单侧移除。
- 可能影响：静态矩阵未捕获，不等同于功能消失。
- 验证：对 9.15.0 APK 做 dex 级搜索或真机验证 legacy 弹幕是否存在。
- 证据：E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平（目标侧 57/10 已确认）；本轮未独立复核 baseline。
- 可能影响：若持平则弹幕净化链路结构未变。
- 验证：真机验证弹幕净化是否工作。
- 证据：E000

### story

目标侧矩阵确认 story_native 2944 类/1376 边、story_kotlin absent（E000）；changes 列表仅有 story_native，佐证 story_kotlin 双侧一致 absent。草稿称 story_native 双侧一致持平仅指纹变，为轻度内部重写，本轮未复核。无登记协议。runtime_enabled 全部 unknown，StoryPurify/StoryActionIcons installer 需真机核对。

证据：E000, E006

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，指纹变（目标侧 2944/1376 已确认）；本轮未独立复核 baseline。
- 可能影响：轻度内部重写可能导致 hook 点漂移。
- 验证：真机验证 story 页控件过滤功能。
- 证据：E000, E006

#### 路径：story_kotlin

- 状态：absent
- 变化：双侧一致全零（changes 无该路径记录，佐证未变化）。
- 可能影响：静态矩阵未捕获，不等于功能消失。
- 验证：若有 story-kotlin 分支，需真机验证或补充识别规则。
- 证据：E000

### mine

目标侧矩阵确认 mine_native 324 类/95 边、mine_account_model 132 类/54 边（E000）；草稿称双侧数完全持平仅指纹变，本轮未复核。无登记协议。E005 确认 VersionAdapter.kt 被真实读取（sha256 782f6fc7…，含 PgcAutoActivityPopupLocator 与 DexAssist 系列导入），其 MineEntryPoint 定位结果与工作树脏状态相关（F006）。runtime_enabled 全部 unknown，MineComponentFilter/MineVip installer 需真机核对。

证据：E000, E005, E006

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，指纹变（目标侧 324/95 已确认）；本轮未独立复核 baseline。
- 可能影响：轻度内部重写导致类名偏移风险。
- 验证：真机验证 mine 页控件过滤与 VIP 识别。
- 证据：E000, E006

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：草稿记录类/边双侧持平，指纹变（目标侧 132/54 已确认）；本轮未独立复核 baseline。
- 可能影响：账号模型类名偏移会影响依赖其字段的 hook。
- 验证：真机验证账号模型相关语义。
- 证据：E000, E005

### F001：登记家族指纹全变但类/边数小幅波动，呈混淆漂移形态，非新样式信号（部分页面的双侧持平待复核）
复核确认（E007/E008）：comment、dynamic 全部登记家族指纹变化且类/边小幅增减；E007 直接捕获混淆改名实例（comment_kotlin_moss 的 userCallback caller 方法 n→o），E008 捕获 DynamicDetailFragment fg→gg、followinglist/service i1→e1、compose data k→j。这与 R8 小版本改名/重排一致，不构成新样式信号。修订说明：home/search/pgc/story/mine 的「双侧数完全持平」本轮因工具预算耗尽未独立复核，数值依据草稿会话取证记录（E001-E006）与目标侧矩阵（E000）交叉一致，标记为待复核而非既证事实；「无法排除个别类名漂移超出定位器覆盖」保留。
反例与替代解释：若真机出现某一家族全部 hook 失配，则证明漂移超出定位器覆盖，需重写识别签名；若补充取证显示某持平家族实际存在字段级新增，则本条结论需按页修正。
建议：不因指纹变化做结构性重构。优先对仅指纹变化、双侧数待复核的 home/search 家族补一次 page_evidence 双侧读取，其余通过 9.15.0 真机逐一确认 installer 命中。
证据：E000, E001, E002, E003, E004, E006, E007, E008

### F002：动态 Compose 与 Opus 家族正向扩张、legacy 收敛，协议层双侧持平，属结构再分配而非协议切换
复核确认（E008）：目标/基线 dynamic_legacy 3221/2092 vs 3193/2143、dynamic_compose 947/161 vs 953/143、dynamic_opus 1333/219 vs 1313/195，与草稿一致。协议层 dynamic_java_moss 双侧 134/134、dynamic_kotlin_moss 双侧 382 定义/26 调用边，dynDetail/subscriptionClick/dynAllPersonal 方法名双侧一致，协议切换断言成立。修订说明：删除草稿「无字段/签名的 radical 变化」的绝对化表述——caller 样本显示 compose 同名类 A 字段形态大变（I/Object/Object → Function1/Function0/Function0/D71.C），同名混淆类不代表同一源类，字段层面存在实际改动，但该改动在混淆类粒度、不构成协议切换证据。
反例与替代解释：若真机验证 compose 分支某核心回调不可达，则扩张含语义变更，需跟进定位；若补证显示 KDynamicMoss 有其他未观察调用者，则调用边 26 需重新评估。
建议：真机对调整后的动态 Compose/Opus 分支做回归验证；若需进一步区分 A 类语义，可用 decompile_class 对比 Lkntr/app/following/followinglist/A; 两版实现。
证据：E008

### F003：player_kotlin 家族边数疑为 150→100（-33%），且其对 KotlinMossChannel/KotlinMossReplyBridge 的依赖未验证（待真机与源码补证）
复核缺口：本轮 page_evidence 预算耗尽，player 页仅获得目标侧（E004 摘录：player_java 948/3223、player_kotlin 7/100，样本为 PlayHistoryMemoryStore 协程类），基线侧类 8→7、边 150→100 的数值无法独立验证，暂依赖草稿会话记录。「KotlinMossChannel/KotlinMossReplyBridge 依赖这类入口点」是对模块源码的断言，本轮未读取这两个文件，不能确认其 Hook 对象与 player_kotlin 家族的对应关系。已确认的旁证：player_kotlin_moss 双侧定义 34/调用边 3 持平（E000 目标侧与草稿记录一致），未观察到协议层收缩。此问题需真机运行验证 + 源码补读，缺口明确。
反例与替代解释：若复核后确认边数下降且源码确有依赖，则该发现维持为播放器与评论 Compose 共同的风险项；若边数实际持平，则整条撤销。
建议：最小补证任务：1) 重新读取 player 页 page_evidence 双侧，验证 player_kotlin 类 8→7、边 150→100；2) 读取 KotlinMossChannel.kt 与 KotlinMossReplyBridge.kt 源码，确认其定位目标；3) 真机触发 PlayerQuality/PlayerCodecForce/PlayerCapability 相关功能，记录 hook 命中。
证据：E000, E004

### F004：【修订】comment_kotlin_moss 调用边并非 50→26：双侧 definitions 130、调用边 26 均持平，草稿误读
E007 双侧明确：comment_kotlin_moss target 与 baseline 的 definitions 均为 130、actual_invoke_edges 均为 26，不存在 -24 的调用边下降。caller 样本对比仅显示混淆改名：doVote/answerQuestion/translateReply 的 caller（Lkntr/common/comment/card/data/f;）不变，userCallback 的 caller 方法由 n 改为 o；KReplyMoss(v1) 各方法名双侧一致。comment_java_moss 双侧 50/50 持平。修订结论：评论 Kotlin MOSS 静态调用面未收缩，评论页无需针对该协议做适配动作；该协议登记完整（v1 KReplyMoss 已注册，unregistered 列表仅含 v2 版本）。
反例与替代解释：若后续证据显示调用边在不同构建/分发渠道间波动，则需区分构建差异与运行链路差异，再评估评论 Kotlin 功能风险。
建议：撤销该风险项；将「main/community/reply/v2/KReplyMoss 出现在未注册协议变更列表」作为服务端可能迁移的观察项列入 remaining_gaps，静态无法判断 v2 是否启用。
证据：E007, E000

### F005：detail_legacy / danmaku_legacy / story_kotlin 双侧一致 absent，需排查识别边界
复核确认：E003 目标侧 detail_legacy 为 absent（全零指纹 4f53cda1…、samples 空）；静态矩阵 changes 列表中无 detail_legacy/danmaku_legacy/story_kotlin 的变更记录，与双侧一致 absence 吻合。三条路径共用同一全零指纹，说明识别规则在这三个页面家族上匹配为空。识别边界与真实移除在静态层面无法区分，absent 也不等于页面功能消失。
反例与替代解释：若搜索显示存在但矩阵未登记，则需更新识别规则；若确认不存在，可标记为已移除并评估是否有宿主替代实现承接该功能。
建议：对 9.15.0 APK 做一次 dex 级家族搜索（detail legacy 集群、danmaku legacy 集群、story kotlin 集群），确认类簇是否真实存在。
证据：E000, E003

### F006：模块源码快照 source_dirty=true，文件哈希已留痕，需按哈希与模块仓库比对追溯
复核确认：快照级 source_dirty=true 成立（E000）；E005/E006 显示 VersionAdapter.kt（sha256 782f6fc7…）与 HookEntry.kt（sha256 e461ae22…）确被真实读取，非占位摘录。修订说明：「两个文件逐文件标记 working_tree_dirty=true」未在当前可见摘录中出现，属草稿会话的额外细节，本轮无法确认 dirty 归属到具体文件，只能确认快照级标记；「与 git HEAD 对比」中的仓库修订号仅能对应 APK 仓库修订 13faec2a…，模块源码仓库的基线未知。
反例与替代解释：若哈希与仓库修订一致，则 dirty 标记为行尾/权限级差异，可忽略；若不一致，需重开 fresh checkout 重新取证后再下结论。
建议：用 E005/E006 记录的文件哈希与模块源码仓库当前提交逐一比对，确认工作树脏状态是否影响 installers/定位器行为；不建议清理工作树，建议重开 fresh checkout 复跑模块源码取证。
证据：E000, E005, E006

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
复核通过：五条路径 status 与静态矩阵逐字一致；数字经 E007 双侧确认；修正草稿 comment_kotlin_moss 调用边误读；补入 7 个 comment_other_ui:* 未登记子家族缺口。
证据：E000, E007, E001

### 复核页面：dynamic
复核通过：三条路径数字与协议层持平经 E008 双侧确认；补充 compose 同名类 A 字段形态大变的事实与 8 个 dynamic_other:* 缺口。
证据：E000, E008, E002

### 复核页面：home
草稿评估保留；「双侧持平」本轮未独立复核，已在正文与 next_steps 标注补证任务。
证据：E000, E006

### 复核页面：search
草稿评估保留；search_java_moss 边 -2 等断言待复核。
证据：E000, E006

### 复核页面：detail
E003 目标侧确认三条路径状态与 absent 指纹；baseline 侧数字待复核；F005 保留。
证据：E000, E003, E006

### 复核页面：pgc
草稿评估保留；「双侧持平」待复核；PgcAutoActivityPopupLocator 存在性经 E005 导入清单佐证。
证据：E000, E006, E005

### 复核页面：player
目标侧数字经 E004 摘录确认；baseline 数字与源码依赖断言未验证，F003 维持 needs_runtime 并注明缺口。
证据：E000, E004, E006

### 复核页面：danmaku
草稿评估保留；absent 佐证经 changes 列表核对；协议数字待复核。
证据：E000, E006

### 复核页面：story
草稿评估保留；story_kotlin 双侧一致 absent 经 changes 列表核对；「双侧持平」待复核。
证据：E000, E006

### 复核页面：mine
草稿评估保留；E005 确认 VersionAdapter.kt 真实读取；F006 修订为快照级脏标记。
证据：E000, E005, E006

- F001 / revised：E007/E008 证实 comment/dynamic 指纹变化伴随小幅数量波动及混淆改名实例（n→o、i1→e1、fg→gg、k→j），支持混淆漂移结论；但 home/search/pgc/story/mine 的「双侧数完全持平」本轮因预算耗尽未独立复核，修订为待复核表述并补充 E000/E007/E008 证据。（E000, E001, E002, E003, E004, E006, E007, E008）
- F002 / revised：数字与协议层持平均经 E008 双侧确认，结论保留；但草稿「无字段/签名的 radical 变化」绝对化——compose 同名类 A 字段形态大变（I/Object/Object → Function1/Function0/Function0/D71.C），已修订措辞并注明同名混淆类对比的局限。（E008）
- F003 / needs_more_evidence：player 页 baseline 侧数字（类 8→7、边 150→100）本轮无法独立验证（page_evidence 预算耗尽，E004 摘录仅 target 侧）；「KotlinMossChannel/KotlinMossReplyBridge 依赖该入口」的源码断言未读取对应文件确认。level 维持 needs_runtime，正文补充具体补证任务。（E000, E004）
- F004 / revised：核心断言与证据矛盾：E007 显示 comment_kotlin_moss 双侧 definitions 130、actual_invoke_edges 26 均持平，草稿「50→26（-24）」系将 50（comment_java_moss 的 definitions）误用作基线调用边。修订为调用边未下降、仅混淆改名（userCallback caller n→o）；投票/翻译/用户回调链路无需按此前的收敛假设做真机专项排查。（E007, E000）
- F005 / retained：E003 目标侧确认 detail_legacy absent 全零指纹；changes 列表无这三条路径的记录，佐证双侧一致 absence；识别边界与真实移除静态不可区分，候选处置（dex 级搜索）保留。（E000, E003）
- F006 / revised：source_dirty=true 为快照级事实（E000），E005/E006 文件真实读取且 sha256 留痕；但「逐文件 working_tree_dirty=true」未在可见摘录中确认，属草稿会话细节，修订为快照级脏标记+按文件哈希与模块仓库提交比对，不建议清理工作树。（E000, E005, E006）

### 尚未解决的证据缺口

- comment_other_ui:*（root/adapter/nextwidget/span/view/webview/widget）7 个未登记子家族标记 structure_or_call_path_changed，未做家族取证，与评论页登记路径的并存关系未知。
- dynamic_other:*（appointment/card/commonCore/commonPerf/commonUi/lightBrowser/dynamic_other_legacy）8 个未登记子家族同上，未取证。
- 大量未注册 K* MOSS 协议变更（如 app/dynamic/v2/KOpusMoss、main/community/reply/v2/KReplyMoss、app/view/v1/KViewMoss、app/playerunite/v1/KPlayerMoss 等）为调查候选而非确认新样式；KOpusMoss 与 dynamic_opus 家族的协议对应关系、reply v2 相对评论 v1 是否为服务端迁移方向，静态证据不足。
- 资源变更 7455 changed/68 removed/4 added 未做任何分析，静态矩阵无资源维度，可能含样式与文案变化。
- player 页 baseline 侧数字（player_kotlin 类 8→7、边 150→100）与 home/search/pgc/story/mine 的「双侧持平」断言未经本轮独立复核，待 page_evidence 补证。
- KotlinMossChannel.kt、KotlinMossReplyBridge.kt、ReplyTopologyComposeMenu.kt 源码未读取，不能推断其对 KReplyMoss/KDynamicMoss 的 Hook 覆盖与兜底。
- 服务端 A/B 与样式开关在无结构变化时静态不可见，不能宣称评论/动态样式已穷尽。
- 全部路径 runtime_enabled=unknown，模块 Hook 生效与否需真机 installer 命中验证，本轮不构成适配验收。

## 下一步

- 真机安装 9.15.0 并启用各 FeatureInstaller，逐 hook 点记录命中，填补全部 runtime_enabled=unknown。
- 对 detail_legacy / danmaku_legacy / story_kotlin 三条双侧一致 absent 路径做 9.15.0 APK 的 dex 级家族搜索，区分识别边界与真实移除。
- 补证 player 页：重读双侧 page_evidence 验证 player_kotlin 类 8→7、边 150→100；读取 KotlinMossChannel.kt、KotlinMossReplyBridge.kt 源码确认其定位目标与 KReplyMoss/KDynamicMoss 桥接覆盖。
- 对 comment_other_ui:* 七个与 dynamic_other:* 八个未登记子家族做 page_evidence 取证，确认是否并存于登记路径及其调用边。
- 对未注册 K* MOSS 做协议取证，优先 KOpusMoss（与 dynamic_opus 的对应）、reply/v2 KReplyMoss（与评论 v1 的迁移可能）、KViewMoss、KPlayerMoss，判断新链路或既有协议改名。
- 对 home/search/pgc/story/mine 仅指纹变化家族补双侧 page_evidence 复核，并做混淆映射比对确认漂移在定位器覆盖内。
- 按文件哈希（E005: 782f6fc7…、E006: e461ae22…）追溯模块源码工作树脏状态与仓库提交的一致性。
- 对 7455 项资源变更抽样分析，确认是否涉及评论/动态/播放器 UI 样式与文案。