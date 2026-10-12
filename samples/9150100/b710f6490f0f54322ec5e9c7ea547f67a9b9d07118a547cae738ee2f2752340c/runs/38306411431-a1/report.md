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

针对 B 站 9.15.0（9150100）相对基线 9.14.0（9140400，同签名证书）的宿主适配静态审计。全部登记家族均报告 structure_or_call_path_changed，多为类数/调用边小幅增减（如 comment_legacy_v2 586→576 类），未见新增或消失的登记路径。声明为 absent 的路径（detail_legacy、danmaku_legacy、story_kotlin）两侧指纹一致，属矩阵登记而非功能消失。各家族 compose_methods 两侧基本一致，指纹差异更可能来自混淆改名/DEX 重排而非新样式。Kotlin MOSS 协议静态调用边偏少（如 comment_kotlin_moss 130 定义仅 26 实际调用边）。模块 VersionAdapter（E011，深挖核实）采用运行时候选类验证+签名匹配的自动定位与缓存机制，且带 DexAssist 兜底诊断。comment_compose 抽样（E012，深挖）与 comment_kotlin_moss 调用边（E013，深挖）已核实含义。所有结论为静态观察，运行期启用状态未知，全部页面 requires_installer_review，需真机验证。

## 各页面评估

### comment

评论页五条登记路径全部报告结构或调用路径变化，幅度均为小幅（几至十几类、几十条边）。comment_compose 抽样核实（E012）：类位于 kntr/common/comment 包（card/service/page/imageviewer 子层），仍以混淆短名类为主，无新增 Compose 样式迹象；compose_methods 两侧均为 274。Kotlin MOSS（E013）核实：KReplyMoss 的 doVote/userCallback/answerQuestion/translateReply/detailList/foldList/dialogList 等被 comment_compose 内多个 repo/数据类实际调用，回调路径明确；但仅 26 条静态调用边相对 130 定义覆盖有限。各路径 runtime_enabled 均未知，需真机验证。

证据：E000, E001, E012, E013

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 586→576，边 761→739，指纹变化；规模小幅缩减
- 可能影响：依赖固定类名/签名的评论过滤 hook 有漂移风险，VersionAdapter 自动定位可缓解
- 验证：真机打开视频评论区，开启评论过滤拓扑功能，核对渲染与过滤是否正常
- 证据：E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 181→173，边 243→209，指纹变化
- 可能影响：CommentPurify/Section Installer 的候选类需复核是否覆盖此路径
- 验证：真机切换 native legacy 评论样式，确认净化功能生效
- 证据：E001

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 47→46，边 64→49，小家族大幅变化
- 可能影响：类少边降幅约 23%，可能为方法内联或调用方迁移，需 installer 复核
- 验证：真机打开 native next 评论，确认注入点未失效
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 67→60，边 84→66，指纹变化
- 可能影响：实验路径由服务端开关控制，静态边缩减可能与开关代码有关
- 验证：真机开启实验3评论样式验证功能是否阻断
- 证据：E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2378→2420，compose_methods 274 不变，边 939→938；抽样见 kntr/common/comment 子层混淆类
- 可能影响：规模微增而 Compose 方法不变，更倾向 DEX 重排/新增非样式类；针对 Compose 定位的过滤模块需重新覆盖类名
- 验证：真机打开新版 Compose 评论，验证过滤与净化功能
- 证据：E001, E012, E013

### dynamic

动态页三路径均变化：dynamic_legacy 类 3193→3221、边 2143→2092；dynamic_compose 边 143→161 增加（compose_methods 亦由 112 增至 112 不变——两者均已核实预取数据一致），dynamic_opus 边 195→219 增加。Kotlin MOSS 两侧定义 382、实际调用边均 26，未变。变化幅度不大；dynamic_other:* 系列家族同样登记变化但未入路径矩阵，作为排查候选而非确认新样式。运行期未知。

证据：E000, E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3193→3221，边 2143→2092
- 可能影响：DynamicPurify 过滤器候选类需覆盖新增的约 28 类
- 验证：真机打开动态页验证净化识别旧版动态卡是否正常
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：边 143→161，compose_methods 112 不变
- 可能影响：新增调用边可能涉及 Compose 中间层，需核对注入方法签名
- 验证：真机打开新版动态页验证净化在新框架下生效
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1313→1333，边 195→219
- 可能影响：Opus 长文折叠/净化逻辑可能受影响
- 验证：真机打开 Opus 长文验证折叠净化功能
- 证据：E002

### home

home_legacy 类 1031→1008（减23）而边 222→227（微增），home_new_frame 类 182→197（增15）而边 53→48（减5）。compose_methods 两侧分别为 128/33 不变。变化呈组件提取/合并或 R8 重排特征，未见新样式确凿证据。结论保持需 installer 与真机复核。

证据：E000, E003

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 1031→1008，边 222→227
- 可能影响：HomeBanner/TopBar/ComponentFilter Installer 若用硬编码类名可能漂移；VersionAdapter 可缓解
- 验证：真机打开首页验证 banner/顶部过滤/推荐净化功能
- 证据：E003

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类 182→197，边 53→48
- 可能影响：新框架新增类而调用边减，疑内部收编，注入点需复核
- 验证：真机使用新版首页框架验证净化功能
- 证据：E003

### search

search_native 类 1625→1674（增49），边 2760→2898（增138）；search_compose 类微增2，边 594→591，compose_methods 556 一致。两个 MOSS 协议定义与调用边两侧完全一致。search_native 的增量最需要 installer 核对覆盖范围；未见确凿新样式。

证据：E000, E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类 1625→1674，边 2760→2898
- 可能影响：SearchPurify 过滤范围若针对固定类名，可能漏匹配新增的 49 类
- 验证：真机搜索验证过滤功能与结果页正常
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类 3147→3149，边 594→591，compose_methods 一致
- 可能影响：微调，风险低，但需确认 Compose 定位未漂移
- 验证：真机使用新版 Compose 搜索验证净化
- 证据：E004

### detail

detail_legacy 两侧 evidence=absent（指纹为空哈希 4f53…2945 一致），属矩阵登记而非功能消失，不能据此判定细节页降级。detail_theseus_ugc 类 1906→1951（增45）边微减；detail_theseus_united 类 4485→4589（增104）边 4140→4167 微增。detail_kotlin_moss 定义 76 仅 10 实际调用边。这些 unified/ugc 家族搜索房间确为模块动态净化目标。

证据：E000, E005

#### 路径：detail_legacy

- 状态：absent
- 变化：两侧登记均无类且指纹一致
- 可能影响：登记性质，不表示详情页功能消失；运行时若实际调用旧路径则超出矩阵覆盖，需真机观察
- 验证：真机打开视频详情页确认正常加载且无未注入痕迹
- 证据：E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1906→1951，边 499→494
- 可能影响：DetailAppPromotion/DetailModule 相关 Installer 需覆盖新增约 45 类
- 验证：真机打开 UGC 详情验证净化与推广过滤功能
- 证据：E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4485→4589，边 4140→4167
- 可能影响：调用边增量集中在少数类；DetailUnited 净化 Installer 需人工核对
- 验证：真机打开详情 united 模式验证功能
- 证据：E005

### pgc

pgc_legacy 类 357→352，边 397→302（减95，约24%）；pgc_theseus 类 2194→2241（增47）而边 4407→826（减约81%），是本次最剧烈的调用边变化。compose_methods pgc_theseus 两侧均 131 不变。边骤减更可能反映调用方迁移/接口收拢（如 MOSS 重构）而非功能移除，也可能是代码合并。pgc_player_moss/pgc_view_moss 定义与调用边两侧完全一致，即协议层未变。推断（待验证）：调用路径重构概率高于功能删除。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类 357→352，边 397→302
- 可能影响：边显著减少，可能存在合并或移除内部调用
- 验证：真机打开 PGC 详情页验证加载与净化功能
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2194→2241，边 4407→826（约 -81%）
- 可能影响：调用路径大幅重构，模块若有针对 theseus 边依赖的注入点风险最高
- 验证：真机打开番剧 theseus 详情页，验证功能与注入是否正常
- 证据：E006

### player

player_java 类 962→948（减14），边 3235→3223（微减）；player_kotlin 类 8→7，边 150→100（减约33%）。协议定义与调用边两侧完全一致（player_java_moss 18/2、player_kotlin_moss 34/3）。player 边骤减不强于调用路径迁移或代码收拢。

证据：E000, E007

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类 962→948，边 3235→3223
- 可能影响：PlayerQuality/Speed/StatusBar 等 Installer 定位点可能受影响
- 验证：真机播放视频验证清晰度/倍速/状态栏功能
- 证据：E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类 8→7，边 150→100
- 可能影响：类少边减，可能 helper 合并；需 installer 复核
- 验证：真机播放视频，验证 Kotlin 路径相关功能
- 证据：E007

### danmaku

danmaku_legacy 两侧均 absent，指纹一致（空哈希），登记性质，不代表弹幕功能消失。danmaku_kotlin 类数 57 两侧一致，边 8→10（+2），仅微调。danmaku_java_moss 定义 22 / 边 20 两侧一致，danmaku_kotlin_moss 定义 46 / 边 4 两侧一致。整体变化最小。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：两侧登记均无类且指纹一致
- 可能影响：登记性质，不影响弹幕功能判定；运行时如有旧路径则超出矩阵
- 验证：真机播放视频观察弹幕层
- 证据：E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类 57 不变，边 8→10
- 可能影响：微调，DanmakuPurify 注入风险低但需复核
- 验证：真机播放视频验证弹幕净化/显示
- 证据：E008

### story

story_kotlin 两侧一致登记 absent，指纹一致。story_native 类 2884→2944（增60）边 1389→1376（微减），compose_methods 44 一致。增类不减边，可能为内部代码拆分。需 installer 复核 StoryPurify/StoryActionIcons 是否覆盖新增类。

证据：E000, E009

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类 2884→2944，边 1389→1376
- 可能影响：Story 相关 Installer 覆盖面需扩展至新增类
- 验证：真机打开竖版 Story 验证功能
- 证据：E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧一致登记 absent
- 可能影响：登记性质，不代表功能消失
- 验证：真机观察竖版页是否存在未登记的 Kotlin 路径
- 证据：E009

### mine

mine_native 类 318→324（增6）边 98→95（减3），指纹变化轻微。mine_account_model 类数 132 与边 54 两侧一致，但指纹由 85fd…25f 变为 1af8…074，说明虽有相同结构规模仍存在方法体或字节序变化，无法由计数推出语义——区分处理而非直接等价。provider 类搜索变更两侧一致说明非结构性改动。

证据：E000, E010

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类 318→324，边 98→95
- 可能影响：MineComponentFilter/MineVip Installer 若定位固定类可能漏覆盖
- 验证：真机打开 Mine 页面验证过滤与 VIP 功能
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类 132、边 54 一致但指纹不同
- 可能影响：结构不变但存在内部变更，可能影响 Provider/Service 层识别；需补颗粒度证据
- 验证：真机打开 mine 相关 account 模块相关页面验证
- 证据：E010

### F001：评论 Kotlin MOSS 静态调用覆盖有限（KReplyMoss 26/130 边），评论方向桥覆盖未知
事实（E013）：comment_kotlin_moss 定义 130、静态调用边 26（两侧一致），可见调用者为 comment_compose 内 _REPO/数据层类调用 doVote/userCallback/answerQuestion 等。事实（E017）：模块 KotlinMossReplyBridge 是 kotlinx protobuf ↔ Java protobuf 的线格式往返桥，安装在 (Object, SerializationStrategy, DeserializationStrategy, Handler, ProtoBuf)V 五参回调泛型入口；源码注释称 suspend 形态经匿名回调也汇入同一入口，但其文档对象是动态页 dynAll/dynVideo。评论 KReplyMoss 各具体方法（doVote/userCallback 等）是否被该桥覆盖：源码未证实，属未知。推断：静态边 26/130 的低覆盖可能由 Compose 层内联/反射造成，静态穷举不足；待真机验证：打开评论楼中楼/投票/图片评论，检查桥是否被触发。
反例与替代解释：若评论响应未走该回调入口或方法被进一步内联，静态边数即不可推断覆盖；应改用运行时日志（诊断中心 dex.assist.* 与 ModernHookLog）确认实际命中，而不是继续依赖静态边计数。
建议：勿假定 KotlinMossReplyBridge 已覆盖评论 KReplyMoss 调用：先在真机上触发评论互动（投票、回复、楼中楼、翻译），用模块日志确认桥是否安装与命中；若未命中，为评论通道单独补安装点（复用 callbackEntry 形态匹配）而不是复用动态页假设。
证据：E013

### F002：comment 家族与 comment_other_ui:* 多处指纹变化，需排查混淆与 DEX 重排，非新样式
事实：E000 显示 comment_legacy_v2/comment_native_legacy/next/exp3/comment_compose 及 6 个 comment_other_ui:* 家族均 structure_or_call_path_changed；E012 抽样核实 comment_compose 类集中在 kntr/common/comment 子层，无新增顶层样式入口，compose_methods 两侧均为 274。推断：comment 家族变化更可能为混淆改名/DEX 重排/调用方迁移，而非新评论区样式。待真机验证：comment_compose 与 legacy 行为需真机确认，以及服务端样式开关静态不可见。
反例与替代解释：若 comment_other_ui 家族仅被 comment_native_* 消费且运行由实验开关关闭，则实际影响仅出现在实验开启场景；需真机切换 native/legacy 开关验证。
建议：保持 comment_other_ui:* 排查候选状态，优先检查 comment_native_next/exp3 定位器（类少且边降幅大）是否仍能落到实际类，再判断是否需要新增 hook 点；勿将指纹变化判定为新样式。
证据：E000, E001

### F003：动态页变化属排查候选；动态过滤的 Kotlin↔Java protobuf 桥对 9.15.0 未复核
事实：三路径小幅结构变化（legacy 3193→3221 类/2143→2092 边，compose 边 143→161 且 compose_methods 112 不变，opus 边 195→219），dynamic_kotlin_moss 定义 382/边 26 两侧一致（E015）。事实（E017）：动态过滤判据建立在 Java 版响应类上，经 KotlinMossReplyBridge 的 ProtoBuf 往返；过滤无改动时直接返回原对象。dynamic_other:* 家族仅登记变化，为排查候选而非确认新样式。待真机验证：动态过滤桥在 9.15.0 是否正常安装并过滤。
反例与替代解释：若边数差异由 DEX 重排而非真实调用方迁移造成，则实际影响有限；dynamic_other:* 家族需按名重读具体类样本再判断。
建议：真机打开动态页并开启净化，验证动态卡过滤与 Opus 长文折叠；同时核对 KotlinMossBridgeMembers.resolve 在 9.15.0 是否成功，失败则桥整体退回观测方式。
证据：E000, E002

### F004：mine_native 与 mine_account_model 存在指纹级差异， Installer 定位需复查
事实：E010 显示 mine_native 类 318→324、边 98→95；mine_account_model 类数 132 与边 54 两侧一致但指纹不同。推断：指纹不同的根因混淆改名/DEX 重排/方法体修改，无法仅靠数量差异判断语义；MineComponentFilterFeatureInstaller 与 MineVipFeatureInstaller 的定位若依赖固定类名可能在 mine_account_model 内漂移。待真机验证：能否在真机上访问 Mine 页面的相应过滤能力。
反例与替代解释：若这些指纹差异源于字符串常量池重排，则语义不变；需读具体类字节段或依赖 VersionAdapter 自动定位补证。
建议：真机打开『我的』页面，检查 MineComponentFilterFeatureInstaller 与 MineVipFeatureInstaller 是否正常注入；并复核 VersionAdapter 中 MineEntryPoint（E011 提及该类型含字段漂移风险）是否能命中。
证据：E010, E011

### F005：search_native 新增约 49 类与 138 条边，SearchPurify 覆盖面需复核
事实：E004 显示 search_native 类 1625→1674，边 2760→2898；而 search_compose 微调，且 search two 家族 MOSS 定义与调用边两侧完全一致。推断：增量集中在 native 层，可能为新增功能或拆分出辅助类；不一定服务端 A/B 的新搜索样式。待真机验证：SearchPurify 插件在 native 层的表现以及是否覆盖新增类群体。
反例与替代解释：若新增类仅涉及与登录/签名相关代码（与本模块无关），则净化功能不受影响；需读取新增类列表判断是否与模块 hook 范围相关。
建议：真机验证搜索净化功能是否正常，并核对 SearchPurifyFeatureInstaller 在 9.15.0 里是否有随 VersionAdapter 自动补覆盖，而非使用旧硬编码类名。
证据：E004, E011

### F006：detail_theseus_united 家族规模微增（约 +104 类、+27 边），DetailUnited 净化需人工核对
事实：E005 显示 detail_theseus_united 类 4485→4589、边 4140→4167；detail_theseus_ugc 类 1906→1951、边 499→494。detail_legacy 两侧 absent 一致。推断：增量集中在某些类，可能是 Detail united 模块有方法接入或分裂，需 installer 人工核对。待真机验证：DetailUnited 净化功能是否在 9.15.0 真机正常运行。
反例与替代解释：若边增长是由方法计数差异（方法定义数与调用边单位不同）导致，则实际影响有限；需结合真实识别到的这些方法验证。
建议：真机打开普通视频详情页，观察 DetailUnitedModulePurifyFeatureInstaller / DetailUnitedPresentationPurifyFeatureInstaller 是否有未注入或缺失新方法点。
证据：E005

### F007：pgc_theseus 静态边 4407→826 且协议层一致：归属/迁移原因未知，需按名重读验证
事实（E006）：pgc_theseus 类 2194→2241 而边 4407→826（-81%），pgc_legacy 边 397→302 且 compose_methods 基线 0、目标 1；登记协议 pgc_player_moss/pgc_view_moss 定义与边两侧完全一致。推断：协议层未变下边骤减更可能是家族归属重划、调用方迁往未登记协议或 DEX 重排，而非功能删除；草稿仅凭名称推测迁往 KPlayerMoss，无证据。待真机验证：番剧详情功能与模块 PGC 净化点命中均未知。
反例与替代解释：也可能是矩阵家族归属重划（部分边计入其他家族而非消失）或服务端开关使运行期路径不同；静态无法排除。
建议：真机打开番剧详情页验证功能；若模块日志显示 PGC 净化点 MISSING，再按名重读 KPlayerMoss/KViewMoss 的实际调用者样本确认迁移动向，补候选类。
证据：E006

### F008：player_kotlin 边数由 150 减至 100，类数仅减 1：合并或调链收拢候选
事实：E007 显示 player_kotlin 类 8→7，边 150→100；player_java 类 962→948、边 3235→3223。player_kotlin_moss 与 player_java_moss 定义与边数两侧完全一致。推断：player_kotlin 少类多减边说明该层内部有合并或调用收拢，需确认是否涉及 PlayerQuality/PlayerSpeed 等 Installer 目标。待真机验证：真机播放中对应功能是否仍可拦截。
反例与替代解释：若减少的边多为品牌无关的 helper 方法收拢且不涉及 player_installers 目标，则可判定影响有限。
建议：真机核对播放器相关 Installer（PlayerQuality/Speed/StatusBar/CodecForce 等）是否仍能定位到目标方法。
证据：E007

### F009：VersionAdapter 自动定位/缓存机制在 9.15.0 中的运行有效性待真机验证
事实：通过 module_source 读取 VersionAdapter.kt（E011）确认模块具备基于 KavaRef 的候选类自动定位、签名匹配（HookPoint/ListConstructorPoint）、原子缓存读写与 DexAssist 兜底诊断（dex.assist.* 前缀，含 comment_topology/player_quality），并有 HostThreadGuard 线程守卫。推断：模块已为这次指纹漂移预留分层适配机制，但实际是否能解到 9.15.0 的混淆类需真机验证。待真机：安装后首次启动触发适配并查看诊断中心 DEX_ASSIST 日志（如 dex.assist.comment_topology 的 state=FOUND/MISSING）。
反例与替代解释：若真机适配全部 FOUND 且 hook 点稳定，则本报告所指多数指纹漂移无实际影响；若出现 MISSING，则需针对对应家族补充候选类列表。
建议：在真机上启动 B 站并触发一次完整适配，读取诊断中心 dex.assist.* 各条目的 state 与 detail，确认各功能点是否 FOUND；MISSING 的点进入 installer 手补。
证据：E011

### F010：unregistered_protocol 变化名单庞大，仅 KReplyMoss 有调用者证据，其余影响未取证
事实：E000 记录 90+ 条 unregistered_protocol 变化；有调用者证据的仅 E013 的 comment KReplyMoss（计数两侧一致），KPlayerMoss/KViewMoss 与 pgc 边聚变的关联仅为名称推测（见 F007）。其余协议（im/mall/broadcast/live 等）无读取证据，影响未知。
反例与替代解释：GenRPC 统一升级假设未经源码验证，不得作为安全结论。
建议：仅对模块源码实际触达的评论回复链路先行真机验证；其余 unregistered_protocol 记为观察集合，逐条按名重读补证后再归类，本轮不给出影响结论。
证据：E013

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
评论五条路径均小幅变化；E012 抽样与 E014 重取证据显示 kntr/common/comment 混淆类，compose_methods 两侧均 274，无新增 Compose 样式入口；Kotlin MOSS 定义 130/边 26 两侧一致。指纹变化更可能为混淆/DEX 重排；运行期未知。
证据：E000, E014, E012, E013

### 复核页面：dynamic
动态三路径小幅变化（legacy 3193→3221 类/2143→2092 边，compose 边 143→161 且 compose_methods 112 不变，opus 边 195→219）；Kotlin MOSS 382/26 两侧一致（E015）。动态过滤判据由 KotlinMossReplyBridge（E017）走 ProtoBuf 往返，未改动则直接返回原对象。dynamic_other:* 为排查候选，运行期未知。
证据：E000, E015, E017

### 复核页面：home
home_legacy 1031→1008 类/222→227 边，home_new_frame 182→197 类/53→48 边，compose_methods 不变。呈组件合并/R8 重排特征，未见确认新样式。全部为静态观察，运行期未知。
证据：E000, E003

### 复核页面：search
search_native 1625→1674 类/2760→2898 边，search_compose 微调，compose_methods 556 一致，两个 MOSS 协议两侧完全一致。增量集中于 native 层，可能为新增功能或拆分类，不构成确认新样式；运行期未知。
证据：E000, E004

### 复核页面：detail
detail_legacy 两侧 absent 且指纹一致，属矩阵登记性质。detail_theseus_ugc 1906→1951/499→494；detail_theseus_united 4485→4589/4140→4167。detail_kotlin_moss 定义 76/静态边 10 两侧一致。推断增量或为 united 模块接入或分裂，运行期未知。
证据：E000, E005

### 复核页面：pgc
最剧烈变化：pgc_theseus 类 2194→2241 而边 4407→826；pgc_legacy 类 357→352、边 397→302，compose_methods 基线 0、目标 1。pgc_player/view_moss 协议两侧一致。最可能为调用方迁移/矩阵重划/DEX 重排，而非功能删除；运行期未知。
证据：E000, E006

### 复核页面：player
player_java 962→948 类/3235→3223 边微减；player_kotlin 8→7 类、150→100 边（-33%）；协议两侧完全一致。边降幅大而仅少 1 类，疑合并或调用收拢，静态无法判定是否触及播放器 Installer 目标，运行期未知。
证据：E000, E007

### 复核页面：danmaku
danmaku_legacy 两侧一致 absent（登记性质）。danmaku_kotlin 类 57 不变、边 8→10；协议两侧一致。本页变化最小，风险最低但运行期未知。
证据：E000, E008

### 复核页面：story
story_kotlin 两侧一致 absent（登记性质）。story_native 2884→2944 类/1389→1376 边，compose_methods 44 一致；增类不减边或为内部拆分，运行期未知。
证据：E000, E009

### 复核页面：mine
mine_native 318→324 类/98→95 边；mine_account_model 类 132、边 54 两侧一致但指纹不同，说明存在计数无法反映的内部变化。MineEntryPoint 注释（E016）明确字段名会随 R8 漂移；运行期未知。
证据：E000, E010, E016

- F001 / revised：KReplyMoss 的静态调用者样本（comment_compose 内 card/data/f 等调用 doVote/userCallback）确有 E013 支持，但原断言「调用路径与模块 KotlinMossReplyBridge 注入面一致」被源码证伪：E017 显示该桥安装在五参回调泛型入口，文档以动态页 dynAll/dynVideo 为对象，评论 KReplyMoss 各具体方法的桥覆盖未在源码中证实。必须修正并降级为 needs_runtime。（E013, E017）
- F002 / retained：E012 抽样与 E014 重取证据支持：comment 家族及 other_ui:* 指纹变化无 Compose 方法数变化，更可能为混淆/DEX 重排或调用方迁移；保持排查候选级别与不把指纹变化当新样式的结论。（E000, E014, E012）
- F003 / revised：结论方向正确，但原 analysis 含表述瑕疵（compose_methods 由 112 增至 112 不变），且未引用动态桥源码这一直接相关证据；补上并修正。（E015, E017）
- F004 / retained：E010 支持计数一致但指纹不同，E016 证实 VersionAdapter 注释明确 MineEntryPoint 字段名会随 R8 漂移，结论与 level=needs_runtime 恰当。（E010, E016）
- F005 / retained：E004 数字核对无误，协议一致，candidate 级别与替代解释恰当，未越界。（E004, E016）
- F006 / retained：E005 数字核对无误，legacy 缺席一致为登记性质，保持 candidate 与真机核对要求，处置合规。（E005）
- F007 / revised：数字与推断方向正确，但迁往 KPlayerMoss/KViewMoss 仅基于名称推测而非调用者证据；pgc_player_moss/pgc_view_moss 两侧完全一致使内部迁入无法由现有证据确认。收窄为未知并修正。（E006）
- F008 / retained：E007 数字核对无误，协议一致；candidate 级别与合并/收拢假设合理，未超出静态证据范围。（E007）
- F009 / retained：E016 重读确认 FOUND/MISSING/NOT_APPLICABLE、dex.assist 前缀诊断含 comment_topology/player_quality、缓存与手动重适配机制；excerpt 尾部截断但 F009 本就标 needs_runtime，结论未越界。（E011, E016）
- F010 / revised：范围过宽：E013 仅覆盖 KReplyMoss 调用者样本且评论 MOSS 计数两侧未变；90+ 条 unregistered_protocol 的变化幅度与影响未逐条取证，草稿却以集体结论与未经验证的 GenRPC 假设呈现。收窄并作待补证。（E013, E017）

### 尚未解决的证据缺口

- 全部路径 runtime_enabled=unknown，需真机验证后才能评估模块生效；本轮仅完成静态证据审查，不构成适配验收
- 模块源码工作树 source_dirty=true，按文件哈希追溯（E016 782f6fc7…/E017 e152445e…），未提交修改与构建产物一致性未核实；结论需绑定当前哈希
- E016 只读到 MineEntryPoint 定义处，VersionAdapter 适配主流程（候选验证→缓存写入→快路径）未逐行读完
- F001：评论 KReplyMoss 是否被 KotlinMossReplyBridge 覆盖需真机日志确认（触发评论互动读 dex.assist 日志）
- F003：KotlinMossBridgeMembers.resolve 依赖的 kotlinx.serialization 三个类名在 9.15.0 宿主中未混淆与否未复核（源码注释仅明示 9.14.0）
- F007：pgc_theseus 边骤减的归因（家族重划/迁往未登记协议/DEX 重排）需按名重读 KPlayerMoss/KViewMoss 调用者样本
- F010：其余 90+ 条 unregistered_protocol 未逐条读取调用者证据，影响范围未知，留待下次补证
- E014/E015 为截断摘录视图，未据此对完整调用者/类样本逐一确认，必要时按名重读

## 下一步

- 真机安装并启动 B 站，触发一次 VersionAdapter 完整适配，读取诊断中心 dex.assist.* 日志，确认各 hook 点 state 是否 FOUND（E011）
- 真机验证评论模块：打开评论楼中楼、投票、图片评论、翻译，验证 CommentFilter/CommentPurify/CommentTopology 及 KotlinMossReplyBridge 是否仍能拦截（E012、E013）
- 真机验证动态页与 Opus 长文的净化与折叠功能，确认 dynamic_legacy/compose/opus 三路径在新版本中仍受 DynamicPurifyFeatureInstaller / DynamicTabsFeatureInstaller 覆盖（E002）
- 真机验证搜索净化功能在 9.15.0 下的覆盖，特别是 search_native 新增的约 49 类是否影响 SearchPurifyFeatureInstaller 定位（E004）
- 真机打开视频详情页（UGC 与 united 模式）验证 DetailModulePurifyFeatureInstaller / DetailUnitedModulePurifyFeatureInstaller / DetailUnitedPresentationPurifyFeatureInstaller 是否正常注入（E005）
- 真机打开番剧详情页验证 pgc_theseus 调用路径重构后功能仍正常，并检查模块 PGC 相关 Installer 是否需要补候选类（E006）
- 对 changes 列表中的 unregistered_protocol 的 KReplyMoss/KPlayerMoss/KViewMoss 等模块生态协议逐条归类，优先真机验证模块实际调用范围，其余协议记录为后续观察集合
- 对 comment_native_next/comment_native_exp3 等小家族（类少边降幅大）优先复核 installer 定位器是否能命中 9.15.0 实际类