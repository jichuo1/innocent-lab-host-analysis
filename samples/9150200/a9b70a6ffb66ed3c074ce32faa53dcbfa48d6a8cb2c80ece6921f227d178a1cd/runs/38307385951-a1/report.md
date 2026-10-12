## 静态事实核对（程序计算）

登记页面 10 个，登记路径 25 条；其中 22 条有静态调用证据，3 条未检出。路径数量与状态以静态矩阵为准，AI 文字可能存在计数或解释错误。

方法定义数与调用边数不是同一计量单位，二者相除不能作为覆盖率或故障判据。证据 ID 校验只检查引用存在，不代表每项 AI 推论都已验证。未提交源码应按文件哈希追溯，不应为采纳 AI 建议而清理或丢弃工作树。

# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 已完成独立分析（见后文），运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2417 | 274 | 918 | static_invoke_observed |
| comment_legacy_v2 | 581 | 0 | 734 | static_invoke_observed |
| comment_native_exp3 | 60 | 0 | 59 | static_invoke_observed |
| comment_native_legacy | 156 | 0 | 177 | static_invoke_observed |
| comment_native_next | 45 | 0 | 46 | static_invoke_observed |
| comment_other_ui:(root) | 227 | 2 | 524 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 24 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 217 | 0 | 110 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 232 | 33 | 342 | static_invoke_observed |
| danmaku_kotlin | 56 | 1 | 9 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1953 | 25 | 515 | static_invoke_observed |
| detail_theseus_united | 4602 | 98 | 4163 | static_invoke_observed |
| dynamic_compose | 956 | 112 | 170 | static_invoke_observed |
| dynamic_legacy | 3227 | 105 | 2193 | static_invoke_observed |
| dynamic_opus | 1341 | 92 | 190 | static_invoke_observed |
| dynamic_other:appointment | 26 | 3 | 19 | static_invoke_observed |
| dynamic_other:card | 412 | 82 | 290 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 58 | static_invoke_observed |
| dynamic_other:commonPerf | 12 | 1 | 4 | static_invoke_observed |
| dynamic_other:commonUi | 21 | 5 | 8 | static_invoke_observed |
| dynamic_other:lightBrowser | 72 | 18 | 32 | static_invoke_observed |
| dynamic_other_legacy | 2091 | 4 | 2137 | static_invoke_observed |
| home_legacy | 1004 | 128 | 236 | static_invoke_observed |
| home_new_frame | 196 | 33 | 46 | static_invoke_observed |
| mine_account_model | 132 | 0 | 54 | static_invoke_observed |
| mine_native | 324 | 7 | 95 | static_invoke_observed |
| pgc_legacy | 353 | 0 | 401 | static_invoke_observed |
| pgc_theseus | 2249 | 131 | 742 | static_invoke_observed |
| player_java | 953 | 0 | 3225 | static_invoke_observed |
| player_kotlin | 7 | 0 | 100 | static_invoke_observed |
| search_compose | 3149 | 556 | 616 | static_invoke_observed |
| search_native | 1674 | 2 | 2789 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2958 | 44 | 1380 | static_invoke_observed |

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
- dynamic_kotlin_moss: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/account/interfaces/v1/KAccountInterfaceV1Moss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/ad/im/v1/KBusinessChatMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KOpusMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/dynamic/v2/KTribeeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/home/v1/KHomeMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KHistoryMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KMediaMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/interfaces/v1/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/search/v2/KSearchMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/childchannel/v1/KKidsChannelMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/show/mixture/v1/KMixtureMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KLegacyViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/app/view/v1/KViewMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/community/interfacess/watch/v1/KWatchInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/dynamic/interfaces/feed/v1/KFeedMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/customer/interfaces/KCustomerInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/gateway/interfaces/v1/KImGatewayApiMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/im/interfaces/v1/KImInterfaceMoss;: protocol_signature_or_call_path_changed
- unregistered_protocol:Lcom/bapis/bilibili/live/app/interfaces/api/grpc/v1/KMoreLiveMoss;: protocol_signature_or_call_path_changed

## 原生资源变化

{'added': 0, 'removed': 0, 'changed': 1}

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

目标为 tv.danmaku.bili 9.15.0（9150200），证书与基线 9.15.0（9150100）一致，属小步版本迭代。静态矩阵显示所有登记路径均为 static_invoke_observed，runtime_enabled=unknown，各页面状态本质上都是 requires_installer_review，两端都未达到通过或已适配条件。本报告基于预取证据 E001–E010 的结构摘要与调用样本，以及深挖证据 E011（comment_native_legacy 类切片）、E012（comment_kotlin_moss 实际调用方样本）、E013（CommentKotlinPurifier.kt 源码，该文件纳入 working_tree_dirty，按克希希 4db3…口径追溯）。主要推断：1) 本期变化更多是调用路径级漂移而非新样式家族，各家族类数基本守恒，未见新增页面；2) comment_kotlin_moss 实际调用集中在 kntr/common/comment 的 Compose KMP 通道，CommentKotlinPurifier 依赖 protobuf 生成代码固定方法名反射，锚点呈脆弱特性；3) 多个页面存在并存栈，切换条件在本次证据窗口内未读取到。此为草稿报告，最终结论需复核阶段确认。

## 各页面评估

### comment

评论页五个家族均标记 structure_or_call_path_changed。legacy_v2 类 576→581、调用边 739→734，小幅漂移。comment_native_legacy 变化最大（类 173→156、调用边 209→177），深挖样本（E011）显示该家族是 comment3/ui/holder 下的 RecyclerView 混淆类，类数收缩更可能来自迁移/重排而非新样式。comment_kotlin_moss 深挖（E012）实际调用方全部在 kntr/common/comment 下，走 KReplyMoss 的 detailList/foldList/doVote/userCallback 等，调用边 26 条两端一致。协议 130 定义仅 26 条有实际调用边，是否在宿主运行态都激活未知。CommentKotlinPurifier（E013）通过 protobuf 生成代码方法名反射，本期未见 KReplyMoss 签名变化，形状解析大概率仍稳，但需真机日志验证不出现 top-shape/links-shape skip。

证据：E001, E011, E012, E013

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类数 +5，调用边 -5，指纹变更
- 可能影响：若模块按类名定位该家族入口，需确认重命名后锚点是否仍命中
- 验证：真机开出旧评论版本开关，确认运行态选栈仍走 legacy_v2；对照模块日志有无 hook 未命中
- 证据：E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 173→156，调用边 209→177，属最大变动
- 可能影响：家族规模收缩，若模块按类名/超类定位需复查 locator
- 验证：用 decompile_class 核对该家族 E 持有人方法体是否仅重排非行为变化；真机确认该栈是否运行
- 证据：E001, E011

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 46→45，调用边 49→46
- 可能影响：小幅漂移，模块覆盖未知
- 验证：确认与 legacy 的切换开关，真机日志验证是否命中
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类数不变，调用边 66→59
- 可能影响：外部调用边下降，入口可能迁移
- 验证：用 family_evidence 拉该家族基线类样本，比对方法签名
- 证据：E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2420→2417，调用边 938→918
- 可能影响：Compose 通道类库变动，关注 kntr/common/comment 包路径是否整体迁移
- 验证：真机启用 Compose 评论，确认渲染与净化行为
- 证据：E001, E012

### dynamic

三个家族均有变化。dynamic_legacy 类 3221→3227，调用边 2092→2193，是本期调用边增幅较大的家族之一，属调用路径级扩张；dynamic_compose 类 947→956，调用边 161→170；dynamic_opus 调用边下降 219→190，存在 opus 侧向 legacy/compose 边迁移可能。dynamic_kotlin_moss 签名与调用边数两端一致，未见协议结构变化。外围支撑域 dynamic_other:*（card/appointment/commonCore/commonPerf/commonUi/lightBrowser）也被标记，属并存栈/支撑组件需审查。运行态动态页用哪一条返回栈未知。

证据：E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3221→3227，调用边 2092→2193
- 可能影响：调用边扩张可能让模块 Hook 点位置偏移
- 验证：真机开左右滑细条观察进入哪一条返回栈；拉取 dynamic_legacy 家族基线/目标样本比对
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 947→956，调用边 161→170
- 可能影响：Compose 动态渲染结构性变化需留意
- 验证：打开动态 tab，观察是走 compose 还是 legacy；抓请求看 KFeedMoss
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1333→1341，调用边 219→190
- 可能影响：调用边下降，opus→其他家族的迁移可能让旧 Hook 点失活
- 验证：真机打开动态长文卡片，确认 opus 栈到位
- 证据：E002

### home

home_legacy 类 1008→1004（减少 4）、调用边 227→236；home_new_frame 类 197→196、调用边 48→46，且在新框架上类数净减 1。两侧规模守恒，指纹变化更可能是 DEX 重排或混淆改名。无协议条目（protocols 为空），首页走 KHomeMoss 未在本页注册，属 unregistered 协议变化项。运行态 home 用哪条栈未知。

证据：E003

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 1008→1004，调用边 227→236
- 可能影响：首页 Hook 的入口类可能改名或下移
- 验证：真机观察首页 tab 内 home_legacy 渲染是否正常
- 证据：E003

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类 197→196，调用边 48→46
- 可能影响：home 新框架入口若被 Hook 需复查 locator
- 验证：确认 home 新框架开关，在新框架上真机回归
- 证据：E003

### search

search_native 类数不变（1674），调用边 2898→2789，减少 109 条是本期第二大降幅，指向部分搜索链路外移（可能向 compose 或 KSearchMoss 迁移，具体去向证据不足）；search_compose 类数不变，调用边 591→616，小幅上升。search_java_moss 与 search_kotlin_moss 签名和调用边数两端一致。需关注 SearchPurifyFeatureInstaller 是否仍定位到同一入口。

证据：E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数不变，调用边 2898→2789
- 可能影响：调用边收缩需确认不是入口静默迁移
- 验证：真机搜索关键字，确认结果页渲染与相关净化生效
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数不变，调用边 591→616
- 可能影响：Compose 搜索轻微扩边，模块覆盖未知
- 验证：真机启用 Compose 搜索，确认列表与净化行为
- 证据：E004

### detail

detail_legacy 两端均 absent（类 0、调用边 0、fingerprint 相同），absent 不等于功能消失，只能说明该路径在本矩阵下不可静态观测。本期 detail 变化集中在 Theseus 架构内：detail_theseus_ugc 类 1951→1953、调用边 494→515；detail_theseus_united 类 4589→4602、调用边 4167→4163。detail_kotlin_moss 签名与调用边数两端一致，未见协议结构变化。detail_legacy 的 fimg 与 danmaku_legacy、story_kotlin 相同（空集 pattern），说明该家族在两个版本里都没有结构体被审计器捕获，不是本期才变空。

证据：E005

#### 路径：detail_legacy

- 状态：absent
- 变化：两端完全一致 absent，无结构差异
- 可能影响：若模块在此路径有 Hook 配置，本次无实质变动；若预期存在则矩阵命名与实际不匹配
- 验证：确认模块是否声明 Hook 该家族；确认矩阵中 detail_legacy 是否已被废弃或合并进这些斯
- 证据：E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1951→1953，调用边 494→515
- 可能影响：小幅调整，详情页净化行为的入口位置未明
- 验证：真机打开普通视频详情，看相关推荐、PlayerEndPageRecommend 等效果
- 证据：E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4589→4602，调用边 4167→4163
- 可能影响： united 栈仍是最大栈，模块 Detail* 净化主战场稳定性需真机确认
- 验证：真机打开视频详情主页，确认净化与推广清理仍生效
- 证据：E005

### pgc

pgc_legacy 类 352→353、compose_methods 1→0，调用边 302→401，是调用边增幅最大的页面之一，说明 PGC 旧链路被放入了更多外部调用；pgc_theseus 类 2241→2249、调用边 826→742，调用边反降，可能是边迁移而非功能消失。pgc_player_moss 与 pgc_view_moss 签名与调用边数两端一致。PGC 侧自动弹窗安装器不受协议结构影响，但入口类可能改名。

证据：E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类352→353，compose 1→0，调用边302→401
- 可能影响：compose 方法数归 0，说明该家族的 Compose tórm可能被剥离，需模块复核
- 验证：真机打开番剧详情，确认相关净化效果
- 证据：E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2241→2249，调用边 826→742
- 可能影响：调用边下降，模块依赖的 Theseus PGC 入口可能改名
- 验证：真机打开番剧页面，确认 DetailUnitedModulePurify 等效果
- 证据：E006

### player

player_java 类 948→953、调用边 3223→3225，规模基本不变；player_kotlin 类数不变，仅指纹变化。player_java_moss/player_kotlin_moss 签名和调用边数两端一致。PlayerCapability/PlayerCodecForce/PlayerQuality 等安装器需确认 Hook 点在 91502 上仍被命中。

证据：E007

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类 948→953，调用边 3223→3225
- 可能影响：规模扩大但幅度小
- 验证：真机打开视频，确认清晰度/倍速 Hook 命中
- 证据：E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数不变，仅指纹变化，调用边 100→100
- 可能影响：解释状态重排，方法语义未知，需深挖
- 验证：真机打开视频，确认 PlayerSpeed/PlayerQuality Hook 命中
- 证据：E007

### danmaku

danmaku_legacy 两端均 absent（类 0、调用边 0），说明该路径在两个版本里都没有可静态观测的结构，不是本期才变空。danmaku_kotlin 类 57→56、调用边 10→9，是收紧而非消失。danmaku_java_moss 签名与调用边数两端一致；danmaku_kotlin_moss 签名与调用边数也一致（46 定义/4 边），未见结构性协议变化。DanmakuPurifyFeatureInstaller 对该家族有依赖关系，但本期未见方法级结构变化，风险等级较低。

证据：E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：两端完全一致 absent，无结构
- 可能影响：模块若在此路径有 Hook 配置，本次无关；若预期存在，属于矩阵命名与实际不匹配
- 验证：确认矩阵中 danmaku_legacy 是否已废弃或转为 Kotlin 通道
- 证据：E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类 57→56，调用边 10→9
- 可能影响：1 个类收缩，模块覆盖未知
- 验证：真机播放带弹幕视频，确认弹幕正常渲染无显著差异
- 证据：E008

### story

story_native 类 2944→2958、调用边 1376→1380，规模小幅扩；story_kotlin 两端都是 absent；本页无协议条目。相关安装器为 StoryPurify、StoryActionIcons、HomeVerticalDetailRouting，需确认入口是否仍命中。

证据：E009

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类2944→2958，调用边1376→1380
- 可能影响：小幅漂移，story 栈的入口定位未知
- 验证：真机从推荐页向下滑入 story 页面，确认净化和图标效果
- 证据：E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两端均为 absent
- 可能影响：与 danmaku_legacy/detail_legacy 同属无结构变化
- 验证：确认矩阵中 story_kotlin 命名是否已从代码库移除
- 证据：E009

### mine

mine_native 类数不变（324），仅指纹变化；mine_account_model 类数不变，仅指纹变化。两个调用边数两端完全一致（95 与 54），推断主要是 DEX 重排或混淆改名。MineVip、MineComponentFilter 对 account_model 有依赖关系，但本期方法级结构未见变化。

证据：E010

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类数不变，仅指纹变化，调用边95不变
- 可能影响：重排级差异，风险低
- 验证：真机打开我的页，确认 MineComponentFilter 仍生效
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数不变，仅指纹变化，调用边54不变
- 可能影响：模型类若被 Hook 需确认反射解析仍命中
- 验证：真机打开我的页，确认 MineVip 效果
- 证据：E010

### F001：多数家族规模守恒，指纹变化很可能是混淆/DEX 重排而非新样式
mine_native、mine_account_model、player_kotlin、home 等家族在 E003/E007/E010 中类数与外部调用边数基本不变，仅指纹差异。深挖 comment_native_legacy 类样本（E011，5 个类切片，不能代表全家族）显示其 holder 类混淆名/方法集保持熟悉形状。结合证书一致、规模守恒，推断差异主要来自混淆改名、DEX 重排或编译器产物差异，而非新样式。
反例与替代解释：若 method_bodies_sha256 大规模变化或具体方法签名出现新增/删除，该解释被推翻，需重新评估为新样式候选。
建议：复核阶段对 fingerprint 有差异但规模守恒的家族，用 family_evidence 双侧对比 method_bodies_sha256 分布；仅有重排时在矩阵标注为非语义变化。
证据：E003, E007, E010, E011

### F002：comment_kotlin_moss 协议签名双侧一致（130 定义/26 边，E012 vs E016），静态无回归；CommentKotlinPurifier 方法名反射锚点仍需真机验证不静默跳过
E012/E016 双侧独立读取并比对：comment_kotlin_moss 在 9150100 与 9150200 两侧均为 130 个定义、26 条实际调用边，签名集逐项一致，调用方均为 kntr/common/comment 下 card/data/f、common/api/g、page/data/PresetDetailPageRepo、imageviewer/data/e 等 Compose KMP 入口（doVote/userCallback/answerQuestion/translateReply/detailList/foldList/dialogList/pictureList）。协议签名与调用边数在两端一致，KReplyMoss 锚点形状静态无回归。风险集中在 CommentKotlinPurifier（E013，working_tree_dirty，按 sha256=4db3… 口径追溯）：依赖 protobuf 生成代码固定方法名反射并注释许诺'缺哪一项就跳过那一项'，解析失败会被缓存到进程结束，安装器侧可能仍报'新通道 3 项'形成静默失效。此为待真机验证项。
反例与替代解释：若真机日志显示 top-shape/links-shape 无 skip，则该风险仅是潜在项；若 KReplyMoss 签名后续出现字段丢失，风险坐实。
建议：真机开启评论净化后查看 logSkip 日志（top-shape/links-shape 前缀），确认 9.15.0 形状解析不缺项；同时回归净化三项开关。
证据：E001, E012, E013

### F003：search_native 边收缩 109 且部分样本方法体哈希变化（非纯重排，含纯改名证据），search_compose 扩 25 条，家族间迁移仍然是候选
E017/E018 双侧读取确认：search_native 两端类数均为 1674，样本类一一对应但存在改名——基线 result/p 在目标侧改名 result/n 而 method_bodies_sha256 完全相同（纯改名的直接证据）。但同名类 BaseSearchItem（51 字段/107 方法不变）method_bodies_sha256 两端不同，oversea/a 与 share/a 亦然，即确实存在方法体级变更，调用边 2898→2789 的收缩不是纯命名/重排。search_compose 反向扩 25 条边，家族间调用路径迁移仍是当前最经济的解释，但不能完全排除编译器变化。SearchPurifyFeatureInstaller 的 locator 命中面变化未知。
反例与替代解释：若扩展 class 样本显示方法体差异集中在无调用者方法（dead code/重排伪差），则仍可归类为编译器级变化而非功能迁移。
建议：对 method_bodies_sha256 两端不同的样本类逐方法比对外部调用去向（重点 BaseSearchItem 链路），确认是边迁移到 compose/KSearchMoss 而非局部功能删除；再按命中面复核 installer 定位。
证据：E004

### F004：未登记 Moss 协议家族成簇变化，需逐个核对是否影响安装器注册假设
changes 列出了多个 unregistered_protocol 的 K 系列（K 家族），但预取摘要未给出各自的签名差异与调用边数，无法判断是否对安装器可用性造成实际影响。与 CommentKotlinPurifier 强关联的 KReplyMoss 优先。
反例与替代解释：若 protocol_evidence 显示上述签名集一致，则仅为命名登记缺失，不构成适配风险。
建议：用 protocol_evidence 逐个读取 KReplyMoss、KHomeMoss、KViewMoss、KSearchMoss 双侧签名；一致则登记为非回归，不一致则升级为安装器改造项。
证据：E000

### F005：源码工作树不干净，CommentKotlinPurifier 的证据归属需一则哈希追溯注记
seed.source_dirty=true；module_source 读 CommentKotlinPurifier 时返回 working_tree_dirty=true。E013 的 sha256 属于截断视图的哈希，不是最终提交版本；同时基于该文件结论的真机验证方案也因此针对模糊版本。
反例与替代解释：若干净工作树读出的源码与 E013 一致，该问题仅是审阅口径，不构成模块风险。
建议：复核阶段在干净工作树下重读该文件，若与 E013 哈希一致则发现仍有效；若不一致需重新评估修正方案。
证据：E013

### F006：评审在 sample_limit=2 切片下的 comment 双侧对比不可回环验证
E001 的两侧样本限额均为 2 且注释明确"class samples omitted to retain both sides within size bound"，唯一深挖的 comment_native_legacy 也只有 5 个类。因此对 compose 家族两侧的指纹差异目前无法定位到具体类，仅能给出规模守恒的间接推断。
反例与替代解释：若扩展 sample_limit 后发现某类方法签名确实变化，需重新评估该家族的样式候选。
建议：扩展 sample_limit 或用 family_evidence 拉 comment_compose 双侧类样本逐类对照 method_bodies_sha256；仅名称或顺序变化则通过。
证据：E001, E011

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
comment 五个家族均被标记需要复核。legacy_v2 微漂移（576→581 类，739→734 边），native_legacy 收缩最大（173→156 类，209→177 边），E011 目标侧切片显示其为 comment3/ui/holder 下 RecyclerView holder 混淆类，收缩方向更像迁移/重排而非新样式，但该切片 5 类不能代表 156 类全家族。comment_kotlin_moss 双侧独立重读（E012/E016）签名集与 26 条调用边完全一致，静态无回归；130 定义仅 26 条有实际调用边，其余是否运行时激活未知。CommentKotlinPurifier（E013）依靠 protobuf 方法名反射并缺项即跳过、失败缓存到进程结束，本期 KReplyMoss 签名未变，静默失效风险待真机 logSkip 验证。
证据：E001, E011, E012, E013, E014, E016

### 复核页面：dynamic
dynamic 三家族全部变更。legacy 扩大（3221→3227 类，2092→2193 边），compose 扩大（947→956 类，161→170 边），opus 边收缩（219→190），可能是 opus 边向 legacy/compose 迁移。dynamic_kotlin_moss 双侧均为 382 定义/26 边，无协议结构变化。外围支撑域 dynamic_other:*（card/appointment/commonCore/commonPerf/commonUi/lightBrowser）也被标记，属并存栈支撑组件，本轮仅登记未逐个深挖。运行态选哪条栈未知，服务端世界开关的样式切换在本证据窗口不可见。
证据：E002, E015

### 复核页面：home
home_legacy 类 1008→1004、边 227→236；home_new_frame 类 197→196、边 48→46。两端规模守恒，指纹变化更可能来自 DEX 重排或混淆改名（与 search 双侧样本中看到的纯改名同类证据形状），但本期 home 家族未做双侧深挖，不能断言为非语义变化。本页 protocols 为空，首页 KHomeMoss 在 changes 中属 unregistered 家族，其签名变化未被读取，属登记外变化候选。
证据：E003

### 复核页面：search
search_native 类数不变（1674），边 2898→2789，收缩 109 条是登记页面里第二大降幅；search_compose 类数不变，边 591→616。双侧家族重读（E017/E018）确认：同名类一一对应，基线 result/p 在目标侧改名 result/n 而 method_bodies_sha256 完全相同（纯改名的直接证据）；但 BaseSearchItem 两侧 method_bodies_sha256 不同，说明存在真实方法体变更，边收缩不完全是重排。search_java_moss/search_kotlin_moss 双侧签名与边数一致（24/22 与 52/18）。SearchPurifyFeatureInstaller 是否仍定位到同一入口未知。
证据：E004, E017, E018

### 复核页面：detail
detail_legacy 两端均 absent（类 0、边 0、空集指纹相同），只能说明该路径在本矩阵下无可静态观测结构，不代表页面功能或 Hook 缺失。detail 变化集中在 Theseus 体系内：ugc 类 1951→1953、边 494→515；united 类 4589→4602、边 4167→4163。detail_kotlin_moss 双侧均 76 定义/10 边、detail_java_moss 双侧 32/35，无协议结构变化。
证据：E005

### 复核页面：pgc
pgc_legacy 类 352→353、compose_methods 1→0、边 302→401，是边增幅最大的登记路径之一；pgc_theseus 类 2241→2249、边 826→742。pgc_player_moss/pgc_view_moss 双侧签名与边数一致（12/3、14/7），无协议结构变化。compose 方法归 0 的原因（家族消重或 Compose 迁移）本期未做方法级排查。
证据：E006

### 复核页面：player
player_java 类 948→953、边 3223→3225，规模基本不变；player_kotlin 两端一致为 7 类/100 边，仅指纹变化，重排级解释为候选但方法体层面证据未读取，不能断言。player_java_moss/player_kotlin_moss 双侧签名与边数一致（18/2、34/3）。PlayerCapability/PlayerCodecForce/PlayerQuality/PlayerSpeed 等 installer 的实际命中未知。
证据：E007

### 复核页面：danmaku
danmaku_legacy 两端均 absent（类 0、边 0 且空集指纹相同），与 detail_legacy 同形，非本期才变空。danmaku_kotlin 类 57→56、边 10→9，是收紧而非消失。danmaku_java_moss 与 danmaku_kotlin_moss 双侧签名与边数完全一致（22/20、46/4），无协议结构变化。DanmakuPurifyFeatureInstaller 对该家族有依赖，本期未见协议级或家族级结构变化，风险较低但非零。
证据：E008

### 复核页面：story
story_native 类 2944→2958、边 1376→1380、compose_methods 44 两端一致，小幅扩张。story_kotlin 两端均 absent。本页 protocols 为空。相关 installer StoryPurify、StoryActionIcons、HomeVerticalDetailRouting 的实际命中未知。
证据：E009

### 复核页面：mine
mine_native 与 mine_account_model 两端类数、compose_methods、外部边数完全一致（324/7/95、132/0/54），仅指纹变化。未对 mine 做双侧深挖，但与 search 双侧读取发现的纯改名形态类似，指向重排/混淆改名，但不可断言为非语义变化。MineVip、MineComponentFilter 对 account_model 的实际命中未知。
证据：E010

- F001 / retained：mine_native/mine_account_model/player_kotlin/danmaku 等家族类数与调用边守恒，仅指纹变化；双侧深挖（E017/E018）证实同名类存在纯改名（search2 结果类改名而 method_bodies_sha256 完全相同），混淆改名/重排解释方向得到直接同类证据支持。保留，level 维持 static_evidence。（E001, E003, E007, E010, E011, E017, E018）
- F002 / revised：复核阶段双侧独立重读：comment_kotlin_moss 在 9150100 与 9150200 两侧均为 130 定义/26 边，签名集逐项一致，调用方均集中在 kntr/common/comment Compose KMP 入口。'协议结构两端一致'已从推断升级为静态事实，风险收窄为 CommentKotlinPurifier 反射锚点的运行时问题，故降级为 needs_runtime 并修订表述。（E012, E016, E001）
- F003 / revised：双侧家族深挖确认 search_native 同名类样本一一对应，且基线 result/p 在目标侧改名 result/n 而 method_bodies_sha256 完全相同（纯改名直接证据）；但 BaseSearchItem 两端方法体哈希不同，说明边收缩并非纯重排，'机器重排'的保守备选已被部分排除，家族间迁移候选被强化，修订分析以反映新证据。（E004, E017, E018）
- F004 / needs_more_evidence：本轮未逐个读取 unregistered K 系列协议的双侧签名（预算优先保证 comment/dynamic 复核与 KReplyMoss 关联项），草稿的 needs_runtime 判断本身无错，但没有新增证据升级，本轮降为 needs_more_evidence，缺口写入 remaining_gaps。（E000, E013）
- F005 / needs_more_evidence：source_dirty=true 事实成立，E013 归属注记必要。但'在干净工作树重读源码'属于流程待办而非真机验证，本轮未以干净树重读，降为 needs_more_evidence 并入 gaps。（E013）
- F006 / needs_more_evidence：复核阶段实际通过 H016、E017/E018 双面读取部分完成了该补证任务：comment_kotlin_moss 双侧全量签名比对已完成，search_native 提升到 5 类双侧样本。但 comment_compose 大家族（2417 类）的逐类 method_bodies 对比仍未执行，其指纹差异仍仅能给出规模守恒的间接解释，故保留为 needs_more_evidence。（E001, E011, E016, E017, E018）

### 尚未解决的证据缺口

- unregistered K 系列协议（KHomeMoss/KViewMoss/KSearchMoss/KOpusMoss/KFeedMoss/KMoreLiveMoss 等）的双侧签名与调用边未逐个读取，安装器层面是否受影响未核实（对应 F004）
- CommentKotlinPurifier 反射锚点在 91502 运行时是否静默 skip，未真机验证（对应 F002）
- CommentKotlinPurifier 源码未在干净工作树下重读，E013 的 sha256 归属仅为 working_tree_dirty 口径（对应 F005）
- comment_compose 家族逐类 method_bodies_sha256 双侧对比未执行，指纹差异仅有规模守恒间接解释（对应 F006）
- installer 侧 versionCode=91502 的命中分支未逐通道核对，矩阵 requires_installer_review 条目未读实
- 动态页并存栈（legacy/compose/opus）运行态选栈条件与 serving 端世界开关未读取，服务端 A/B 无结构变化的样式切换在静态证据窗口不可见
- 模块安装器依赖关系与本次变更的具体映射未逐文件读取，未对任何路径推断 Hook 覆盖

## 下一步

- 真机开启左右滑细条，确认 9.15.0 动态页运行态出栈家是 legacy 还是 compose，与世界开关（尤其 opus）匹配
- 抓 KReplyMoss 请求样本，人工比对净化后的响应与宿主不下传时的结构差异
- 打开 My/搜索/弓剧/播放器各自页面，确认是否触发 logSkip 日志（尤其是 CommentKotlinPurifier/其他 protobuf 形状解析）
- 构建干净工作树重跑指纹，剔除截断噪声；若仍有差异扩展 sample_limit 重拉
- 走 installer 代码逐通道核对 versionCode 分支为 91502 的命中情况