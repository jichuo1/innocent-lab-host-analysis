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

本报告基于预取证据（E000–E010）+ 深挖证据（E011–E014，覆盖评论 Kotlin MOSS 协议调用方、CommentKotlinPurifier 源码解析点、comment 家族双侧类样本），对 9.15.0（9150100→9150200）宿主做静态适配审计。所有登记页面已分别分析，每条登记路径均给出状态（逐字沿用静态矩阵值）、与基线的变化、对模块影响、验证方法与证据编号。指纹变化量整体小（类数±数个、边数±几十至百余、compose_methods 多数不变），配合 E013 类样本形态，倾向为混淆改名/编译器差异/代码迁移而非确认的新样式；unregistered_protocol 清单在基线中同样存在，属登记缺口而非本次新增风险。所有路径 evidence 均为 static_invoke_observed 或 absent，runtime_enabled unknown，模块覆盖 requires_installer_review，未宣称任何 Hook 生效或适配通过。草稿未经复核。

## 各页面评估

### comment

评论区为本次重点。五个登记路径（legacy_v2/native_legacy/native_next/native_exp3/compose）均为 static_invoke_observed，需安装器与真机验证。comment_compose 类 2420→2417、边 938→918、compose_methods 274 不变；comment_native_legacy 类 173→156、边 209→177；native_next 边 49→46；native_exp3 边 66→59；legacy_v2 类 576→581、边 739→734。协议层不变：comment_java_moss 50/50，comment_kotlin_moss 130 定义/26 边与基线完全一致。深挖 E011 显示 KReplyMoss 的 26 条真实调用边集中在 comment_compose 家族（kntr/common/comment/...）的 detailList/foldList/addReply/userCallback 等 suspend 方法。深挖 E012（CommentKotlinPurifier 源码）表明该模块走 Protobuf 形状反射（getContent/getUrlsMap/clearUrls/putAllUrls/clearQoe/clearOperation/setSubjectControl 等），形状解析失败会静默 logSkip 跳过，且对 Moss 顶层方法签名变化不敏感——因此协议调用边变化主要影响 ReplyBridge/Channel 桥接类是否补齐，而非净化本身。风险集中在形状反射解析：若类名或字段名迁移，净化会静默失效。

证据：E000, E001, E011, E012, E013, E014

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 576→581，边 739→734，fingerprint 变化
- 可能影响：Java getter 净化链路的入口结构小变；主要影响 CommentPurify 的 legacy 通道锚点
- 验证：真机开启评论 Java 净化，检查 evidence(APPLIED) 计数与日志
- 证据：E000, E001

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 173→156，边 209→177
- 可能影响：旧原生 View 评论（comment3 holder 家族）类数下降较多，CommentSection/CommentTopology 若按类名锚点定位可能失配
- 验证：真机切旧原生评论样式，开启分区/拓扑功能看是否 OBSERVED+APPLIED
- 证据：E000, E001, E014

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 46→45，边 49→46
- 可能影响：新原生通道锚点小幅变化；类数仅减 1，倾向代码迁移
- 验证：真机切换 next 样式并验证 Hook 定位日志
- 证据：E000, E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类 60 不变，边 66→59
- 可能影响：实验通道调用边减少；无类数变化，推断为方法合并/内联
- 验证：真机在实验评论区触发净化功能验证
- 证据：E000, E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 2420→2417，边 938→918，compose_methods 不变
- 可能影响：Compose 评论页为 CommentKotlinPurifier 与 ReplyTopologyComposeMenu 主目标；调用边为 26 条（E011），样式反射解析点如保持（E012 所列固定 protobuf 方法名）则净化可用
- 验证：真机开启评论净化+摘搜索跳转，抓 logSkip 是否出现 top-shape/links-shape 跳过
- 证据：E000, E001, E011, E012, E013

### dynamic

dynamic_legacy 类 3221→3227、边 2092→2193，dynamic_compose 类 947→956、边 161→170，dynamic_opus 类 1333→1341、边 219→190。协议层不变：dynamic_java_moss 134/134，dynamic_kotlin_moss 382/26 与基线完全一致。另有 dynamic_other:*（appointment/card/commonCore/commonPerf/commonUi/lightBrowser）与 dynamic_other_legacy 多个子家族需要复核；模块侧 DynamicPurifyFeatureInstaller/DynamicTabsFeatureInstaller 与 KotlinDynamicMossWatch 主要工作在该页。KOpusMoss/KTribeeMoss 属未注册协议，Opus 图文动态存在未覆盖调用面（需 runtime 确认）。整体变化小，静态层面 Hook 路径风险偏低，但动态 Tab 切换/服务端样式是否生效需真机。

证据：E000, E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 3221→3227，边 2092→2193，compose_methods 105 不变
- 可能影响：DynamicPurify 主入口路径；数值漂移幅度小，推断为内联/合并
- 验证：真机动态页开启净化，检查 OBSERVED/APPLIED 计数
- 证据：E000, E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类 947→956，边 161→170，compose_methods 112 不变
- 可能影响：Compose 动态卡片若新增类（+9），模块按类名定位有失配可能
- 验证：真机在 Compose 动态卡片上触发净化
- 证据：E000, E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 1333→1341，边 219→190
- 可能影响：Opus 图文动态调用边减少 29；叠加 KOpusMoss 未注册，Opus 相关净化覆盖需重点验证
- 验证：打开图文动态验证 Opus 净化是否产生日志
- 证据：E000, E002

### home

home_legacy 类 1008→1004、边 227→236，compose_methods 128 不变；home_new_frame 类 197→196、边 48→46，compose_methods 33 不变。两路径均需安装器复核。模块侧 HomeBanner/ComponentFilter/RecommendPurify/TabFilter/TopBar/VerticalDetail 等大量功能锚点位于该页；变化幅度小但均为 fingerprint 变化，无法静态区分重命名与新组件。

证据：E000, E003

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 1008→1004，边 227→236
- 可能影响：HomeTabFilter/ComponentFilter 落点，需验证锚点稳定
- 验证：真机开启首页组件过滤并查 applied 计数
- 证据：E000, E003

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类 197→196，边 48→46
- 可能影响：新框架顶部/底部条 Hook 锚点可能漂移
- 验证：真机启用 BottomBar/HomeTopBar 看日志
- 证据：E000, E003

### search

search_native 类 1674 不变、边 2898→2789（-109），compose_methods 2 不变；search_compose 类 3149 与 compose 556 不变、边 591→616。协议层不变：search_java_moss 24/22，search_kotlin_moss 52/18 与基线一致。边数减少但类数不变，倾向方法内联/调用集中化而非功能移除（推断）。

证据：E000, E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：注射边 2898→2789，其他不变
- 可能影响：SearchPurify/SearchHomeRecommend 的 Hook 调用点减少，需真机确认净化是否失效
- 验证：真机搜索页开启 SearchPurify，比对 applied 计数
- 证据：E000, E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：边 591→616，其他不变
- 可能影响：Compose 搜索页 Hook 分支变化小
- 验证：真机在 Compose 搜索 UI 验证净化结果
- 证据：E000, E004

### detail

detail_legacy 在两版均 absent（0/0/0），非异常。detail_theseus_ugc 类 1951→1953、边 494→515；detail_theseus_united 类 4589→4602、边 4167→4163。模块侧 DetailAppPromotion/DetailModulePurify/DetailUnitedModulePurify/DetailUnitedPresentationPurify/DetailViewPurify 分布于 theseus 家族，任何结构变化都可能影响多个功能，但变化幅度小。

证据：E000, E005

#### 路径：detail_legacy

- 状态：absent
- 变化：两版一致（0/0/0）
- 可能影响：无需 Hook；仅登记核对
- 验证：无静态动作，若真机出现 legacy 详情页需重新登记
- 证据：E000, E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 +2，边 494→515
- 可能影响：UGC 详情页净化/推广屏蔽锚点小幅变化
- 验证：打开 UGC 详情页验证 DetailAppPromotion/DetailViewPurify
- 证据：E000, E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 +13，边 4167→4163
- 可能影响：United 详情页存在可能的新子组件或合并
- 验证：打开 United 详情页验证两个 Purify 模块 applied
- 证据：E000, E005

### pgc

pgc_legacy 类 352→353、compose_methods 1→0、边 302→401（+99）；pgc_theseus 类 2241→2249、边 826→742（-84）。两路径变化幅度均在指纹差异范围内但 compose_methods 1→0 值得关注（推断为其占位 compile 差异或迁移）。模块侧 PgcAutoActivityPopupFeatureInstaller 等需要此页 Hook。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类 +1，compose 1→0，边 302→401
- 可能影响：PGC legacy 内部调用链显著扩张（+99）或为合并，需要运行确认
- 验证：真机番剧页验证 PgcAutoActivityPopup 是否命中
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 +8，边 826→742
- 可能影响：PGC Theseus 主路径，方法合并风险
- 验证：真机 Check PGC Theseus Purify applied 计数
- 证据：E000, E006

### player

player_java 类 948→953、边 3223→3225；player_kotlin 类 7/边 100 不变但 fingerprint 变。协议层不变：player_java_moss 18/2，player_kotlin_moss 34/3 与基线一致。模块侧 PlayerCodecForce/PlayerQuality/PlayerSpeed/PlayerStatusBar/PausedAd 等大量播放页功能集中于 player_java。

证据：E000, E007

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类 +5，边 +2
- 可能影响：播放页新句柄点可能；视内联判定
- 验证：真机按 PlayerCodecForce/PlayerQuality 逐项验证
- 证据：E000, E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类/边不变，fingerprint 变
- 可能影响：若为方法体内部变化，对 Hook 无影响；重命名则失效
- 验证：真机使用 PlayerPortrait 等验证
- 证据：E000, E007

### danmaku

danmaku_legacy 两版均 absent，非异常。danmaku_kotlin 类 57→56、边 10→9，compose_methods 1 不变。danmaku_java_moss 22/20，danmaku_kotlin_moss 46/4 协议双边数不变。模块 DanmakuPurifyFeatureInstaller 覆盖弹幕净化（弹幕是种子中需重点验证的页面之一）。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：两版一致
- 可能影响：无
- 验证：无需
- 证据：E000, E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：类 -1，边 -1
- 可能影响：轻微，需真机确认弹幕净化
- 验证：真机开弹幕屏启用 DanmakuPurify 看是否 applied
- 证据：E000, E008

### story

story_native 类 2944→2958、边 1376→1380、compose_methods 44 不变；story_kotlin 两版均 absent。模块侧 StoryPurify/StoryActionIcons 落在 native 家族。Kotlin moss 协议在另一路径存在（story 无协议登记）。

证据：E000, E009

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类 +14，边 +4
- 可能影响：Story 净化与动作图标判断逻辑需真机确认
- 验证：真机在 story 页打开进度条与评论判分模块确认 applied
- 证据：E000, E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两版一致
- 可能影响：无
- 验证：无需
- 证据：E000, E009

### mine

mine_native 类 324、边 95 与基线完全一致，仅 fingerprint 变；mine_account_model 类 132、边 54 同样一致。这类'数字完全一致但指纹改变'的情况，几乎可以确定是方法体内部变化或 R8 混淆名变更（推断），对按类名+方法名 Hook 的模块干扰低，但安全提示不能排除。

证据：E000, E010

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：数量全一致，fingerprint 变
- 可能影响：MineComponentFilter/MineVip 锚点在类名层面稳定
- 验证：真机打开 Mine 页并启用过滤功能
- 证据：E000, E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：数量全一致，fingerprint 变
- 可能影响：Account Model 字段名重命名的低概率风险
- 验证：真机 MineVip 判定/势力值逻辑验证
- 证据：E000, E010

### F001：comment_compose 与 comment_kotlin_moss 协议调用路径变化对 CommentKotlinPurifier 形状解析的影响
【事实】E011 深挖显示 comment_kotlin_moss 的 26 条调用边全部集中于 comment_compose 家族（kntr/common/comment/...），KReplyMoss 顶层方法签名与 9.15.0 基线一致（130 定义/26 边不变）。【事实】CommentKotlinPurifier（E012）通过 ProtobufBuilderPlan.resolve 反射固定形状名（getContent/getUrlsMap/clearUrls/putAllUrls/N 等），解析不出就静默 logSkip 跳过；其对 Moss 顶层方法名不敏感。【推断】本次 comment 家族指纹与边数变化（compose 938→918，native_legacy 209→177 等）不精确指向新增样式，更倾向于混淆/编译器行为，但存在真实样式迁移可能。模块侧风险：形状反射固定名若被重命名则净化静默跳过。【候选】仍需真机确认 logSkip 无 top-shape:*/links-shape:* 跳过日志。
反例与替代解释：若真机验证显示这些字段名在 9150200 下仍存在，则本条降级为正常非干扰；如确认重命名，则需替换形状解析名，本条升级为静态证据级问题。
建议：在真机开启评论净化与摘搜索跳转，抓取 Xposed 日志确认无 top-shape / links-shape 类 logSkip；用 Family 深挖重读 comment_compose 全类清单与含 KReplyMoss 引用的类名集合对比基线。
证据：E011, E012, E013

### F002：comment 家族五路径（含 comment_other_ui:*）跨版本指纹、类数、边数一致变化是否为混淆改名而非新样式
【事实】E000/E001 显示 comment 五个家族全部变化，且 comment_other_ui 六个分支同时变化；E013 类样本显示 comment_compose 家族内多为 object 模式 service（CardInteractionService、getLogger 等），样本形态与基线差别小。【推断】此类同步小规模变化倾向指向统一编译优化/混淆重命名/DEX 重排，而非每家族独立的新样式演进。不能据此断言样式换新或模块覆盖通过。【候选】
反例与替代解释：若深挖发现真实新增顶层 Compose UI 类或被O̶̶̶̶̶统一识别为全新样式路径，本条升级并需为新家族登记路径与 Hook 覆盖评估。
建议：用 family_evidence 重读 comment_native_legacy 与 comment_compose 双侧完整类名集，检测是否存在 kntr ↔ comment3 的同包迁移或仅 target 侧出现的全新顶层 UI 类；若无独立新类，归并为同一混淆/迁移事件。
证据：E000, E013, E014

### F003：大量 unregistered_protocol 变化（KReplyMoss/KOpusMoss/KFeedMoss/KViewMoss 等）是否真正影响本模块 Hook 覆盖
【事实】Seed E000 列出约 25 个 unregistered_protocol 变化条目，但这些条目同时存在于 baseline 与 target 的未注册协议清单中，并非本次新增。【推断】unregistered ≠ 不存在，只是登记缺失；模块目前未对这些协议建立 Hook path。主要风险：KReplyMoss（评论区数据）、KOpusMoss（图文动态）、KFeedMoss（动态 feed）、KViewMoss（详情页）等核心数据协议若仓内调用边被调用，缺 Hook path 可能导致部分净化能力静默失效。【needs_runtime】
反例与替代解释：若深挖显示这些协议 caller 均未挂接登记家族，则影响为 0，本条关闭；若 caller 挂接登记路径（如 comment_compose、dynamic_opus），则需为对应路径补充 Hook 配置。
建议：用 protocol_evidence 对 KReplyMoss、KOpusMoss、KFeedMoss、KViewMoss 逐条采样 target 侧，确认 caller 家族归属与调用边数，判断是否有未被覆盖的用户侧影响面。
证据：E000, E011

### F004：home/dynamic/search 多路径同时需要 installer 复核，模块安装器/定位器的覆盖一致性风险
【事实】所有 18 个登记路径均 requires_installer_review，且 installer_and_runtime_validation_required，无任何路径被登记为已适配。【推断】确认模块 Hook 生效需真机验证 + evidence 采样（operator 迹金 APPLIED / OBSERVED）。一种朴素风险是：static_invoke_observed 的调用边不等于运行时开启；服务端开关/AB 情境下样式可能被关闭而静态矩阵不表现出差异。【候选】
反例与替代解释：若真机验证全部路径的 installer 与 runtime 验证均到位，则本条降级为合规性确认项，不视为风险。
建议：在真机 9150200 上跑一轮 installer 采样，对每个 FeatureInstaller 记录 applied 计数，与各路径登记状态差异做对比，确认每个登记路径是否真的存在运行时 Hook 必要性。
证据：E000

### F005：search_native 边数减少 109 但类数/compose_methods 不变（2898→2789）
【事实】E000/E004 显示 search_native 两版类数同 1674，compose_methods 同 2，边数差 109。【推断】在类数与 compose 不变的条件下，纯边数下降指向方法级内联/调用合并，而非搜索功能消失；类结构骨架不动，模块按类锚点 Hook的风险低，按方法锚点 Hook 的风险中等。【候选】
反例与替代解释：若深挖显示减少的边集中在模块 Hook 的目标方法，则本条升级为真实适配问题；若分散在公共支撑层则视为轻微风险。
建议：真机开启 SearchPurify 抓运行日，检查是否有 method_not_found/family Resolution 警告。
证据：E000, E004

### F006：pgc_legacy compose_methods 1→0、边数 302→401 的形状变化
【事实】E000/E006 显示 pgc_legacy 类基本不变（352→353）但 compose 从 1 变 0，边数扩张 99 条；pgc_theseus 边数收缩 84 条。【推断】这部分可能涉及 build 时的方法迁移与调用重合，非确定性新样式；compose 归 0 属于编译产物差异，也可能为类从 legacy 迁至 theseus（推断）。【候选】
反例与替代解释：若确认 compose 方法的类完整迁移到 PGC Theseus 分组，则本条解释为代码迁移并关闭；若有新 Compose UI 出现则需样式候选登记。
建议：用 family_evidence 重读 PGC theseus 双侧样本，确认 compose_methods 从 1→0 是否伴随类扩张；同时真机开启 PgcAutoActivityPopup 看是否命中 Hook。
证据：E000, E006

### F007：mine_native / mine_account_model 数值全同但 fingerprint 变化——低概率字段重命名风险
【事实】E000/E010 两版类数/边数/compose 数值完全一致但 fingerprint 变。【推断】描述为方法体内部变更或 R8 名值变化，不影响类名/方法名锚点，风险低。【候选】
反例与替代解释：若真机验证 discovered R8 renaming 涉及被 Hook 的字段，需替换 lookup 名，本条升级。
建议：真机开启 MineComponentFilter/MineVip 看是否 applied；无需深挖。
证据：E000, E010

### F008：story_native 类 +14（2944→2958）来源未定
【事实】story_native 类 2944→2958、边 1376→1380、compose 44 不变；story_kotlin 双侧同指纹一致 absent（非本次变化）。【未知】+14 类来源未验证：UI 子组件新增、类拆分、公共层类归入（common class grouping 归并）、混淆改名均可产生同信号，静态不能区分。【待验证】双侧类名集比对 + 真机 StoryPurify applied 计数。story 页无协议登记，草稿中'Kotlin moss 协议在另一路径存在'与页面证据冲突，应删除。
反例与替代解释：若补证显示新增类归属公共层或为拆分产物则降为非问题；若出现 UI 组件层级则需新样式候选登记
建议：双侧 story_native 各抽样 ≥10 类并比对类名集合；真机 StoryPurify/StoryActionIcons 验证 applied；不能据有界抽样外推整套实现。
证据：E000, E009

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
已用 E015 复核五条登记路径。legacy_v2 类 576→581、边 739→734；native_legacy 类 173→156、边 209→177；native_next 类 46→45、边 49→46；native_exp3 边 66→59；compose 类 2420→2417、边 938→918、compose 274 不变。协议层双侧一致：java_moss 50/50，kotlin_moss 130/26（E011 vs E018，caller 集合一致）。所有路径 evidence 逐字 static_invoke_observed，runtime unknown，requires_installer_review；未宣称样式变更或 Hook 生效。E013/E014/E017/E018 均为有界抽样（各侧 5 类），不能外推到全家族（共 2417/156 等）——这个对于 comment_native_legacy 的 target 侧样本缺口是主要复核不完整点。
证据：E000, E001, E011, E012, E013, E014, E015, E017, E018

### 复核页面：dynamic
已用 E016 复核。dynamic_legacy 类 3221→3227、边 2092→2193、compose 103→105（草稿误写为 105 不变，已更正）；dynamic_compose 类 947→956、边 161→170、compose 112 不变；dynamic_opus 类 1333→1341、边 219→190、compose 92 不变。legacy/compose 样本（followinglist playable holder 含 HistoryPlugin 引用、kntr/app/following Compose 类）双侧同名，但各仅 2 类有界抽样。dynamic_other:* 六个分支与 dynamic_other_legacy（旧/新并存栈、切换条件、宽屏分支）未做调用方级核对，列入缺口。协议 java_moss 134/134、kotlin_moss 382/26 双侧一致。KOpusMoss/KTribeeMoss 未注册协议影响需补协议证据。
证据：E000, E002, E016

### 复核页面：home
home_legacy 类 1008→1004、边 227→236、compose 128 不变；home_new_frame 类 197→196、边 48→46、compose 33 不变。数值核对成立。evidence 逐字沿用 static_invoke_observed；home tab 并存栈与宽屏/平板分支待确认。模块 HomeBanner/TabFilter/ComponentFilter/TopBar/VerticalDetail 锚点需真机采样，静态无法证明 Hook 生效。
证据：E000, E003

### 复核页面：search
search_native 类 1674、compose 2 不变，边 2898→2789；search_compose 类 3149、compose 556 不变，边 591→616。协议 java_moss 24/22、kotlin_moss 52/18 双侧一致。边数减少但类数不变与调用合并同信号混淆，需运行级证据判定对 SearchPurify 的影响。
证据：E000, E004

### 复核页面：detail
detail_legacy 双侧均 0/0/0 且指纹一致，属登记 absent 而非本次变化。theseus_ugc 类 1951→1953、边 494→515、compose 25 不变；theseus_united 类 4589→4602、边 4167→4163、compose 98 不变。数值核对成立，+13 类来源属于统计未知。KViewMoss/KLegacyViewMoss 未注册协议归属待核查。
证据：E000, E005

### 复核页面：pgc
pgc_legacy 类 352→353、compose 1→0、边 302→401；pgc_theseus 类 2241→2249、边 826→742、compose 131 不变。协议 pgc_player_moss 12/3、pgc_view_moss 14/7 双侧一致。compose_methods 1→0 属统计归属差异，不据此断言样式消失或迁移。
证据：E000, E006

### 复核页面：player
player_java 类 948→953、边 3223→3225；player_kotlin 类 7、边 100 不变仅 fingerprint 变。协议 player_java_moss 18/2、player_kotlin_moss 34/3 双侧一致。'fingerprint-only 变化倾向方法体内部变动'为推断，不可轻定——player_kotlin 类数少边数多，需方法级比对才能判定锚点稳健性。
证据：E000, E007

### 复核页面：danmaku
danmaku_legacy 双侧均 0/0/0；danmaku_kotlin 类 57→56、边 10→9、compose 1 不变。协议 danmaku_java_moss 22/20、danmaku_kotlin_moss 46/4 双侧一致。数值核对成立，evidence 逐字沿用。
证据：E000, E008

### 复核页面：story
story_native 类 2944→2958、边 1376→1380、compose 44 不变；story_kotlin 双侧 absent。数值核对成立。+14 类来源未验证；草稿'Kotlin moss 协议在另一路径存在'与 story 页无协议登记事实冲突，不应作推论保留（已通过 F008 revision 修正）。
证据：E000, E009

### 复核页面：mine
mine_native 类 324、边 95、compose 7 全一致仅 fingerprint 变；mine_account_model 类 132、边 54 全一致仅 fingerprint 变。数值核对成立。低风险判断保守合理，但字段/方法级重命名可能性待真机验证。
证据：E000, E010

- F001 / needs_more_evidence：E011/E018 双侧对比显示 comment_kotlin_moss 130 定义/26 调用边不变，caller 集合相同，Moss 顶层方法签名稳态。CommentKotlinPurifier 形状反射（getContent/getUrlsMap/clearUrls/putAllUrls/clearQoe/clearOperation/setSubjectControl）失败会 logSkip 静默跳过，是真实风险但只能 runtime 验证；静态证据不足以判定形状字段名是否被重命名。降级为 needs_runtime 并留补证缺口：真机 logSkip 日志 + 形状名与 9150200 反编译 protobuf 生成类对照。草稿把 comment 家族外部 invoke 边变化与形状解析风险混为一谈也无依据。（E011, E012, E018）
- F002 / needs_more_evidence：E013/E017 对比（comment_compose 双侧五类同名、方法集归一，仅个别 method_bodies 哈希不同）与 E014 支持'同包同名、倾向混淆/编译器差异'的推断方向，但 sample_limit 有界，不能外推到 2417 类的全家族；comment_other_ui 六个分支无类名证据。降级：需读取 comment_native_legacy target 侧与 comment_other_ui:adapter/view 双侧类名集后才能判定是否归并为同一混淆/迁移事件。（E000, E013, E014, E017）
- F003 / needs_more_evidence：草稿断言'unregistered_protocol 条目同时存在于基线'没有基线侧清单证据支持，E000 仅有 target 侧清单；'模块未对这些协议建立 Hook path'也未从模块源码核验。降级为 needs_more_evidence：需对 KOpusMoss、KFeedMoss、KViewMoss 等逐条 protocol_evidence 采样 caller 家族，并核查模块源码是否消费这些协议。KReplyMoss 已由 E011/E018 证实与 registered comment_kotlin_moss 一致，无需重复。（E000, E011）
- F004 / needs_more_evidence：发现中所写'18 个登记路径'计数错误，实际为 25 条（comment 5 + dynamic 3 + home 2 + search 2 + detail 3 + pgc 2 + player 2 + danmaku 2 + story 2 + mine 2）；'evidence 采样 operator 迹金 APPLIED/OBSERVED'为笔误级表述需在最终报告中剔除。核心主张（25 条均 requires_installer_review、无已适配登记、静态调用不等于运行时启用）与 E000 一致，保留为 needs_runtime 待真机采样验证。（E000）
- F005 / needs_more_evidence：数值核对成立（类 1674、compose 2 不变，边 2898→2789；search_compose 边 591→616；协议双侧一致）。但'纯边数下降指向方法级内联/调用合并'的断言缺乏证明——同一信号可由混淆改名或 DEX 重排产生。降级：需补证边数减少是否命中 SearchPurify Hook 目标方法，以及真机查 method_not_found/解析警告。（E000, E004）
- F006 / needs_more_evidence：数值核对成立（pgc_legacy 类 352→353、compose 1→0、边 302→401；pgc_theseus 类 2241→2249、边 826→742、compose 131 不变；协议双侧一致）。但'类从 legacy 迁至 theseus'缺乏类级证据——侧数增量并非简单迁移。降级：需 family_evidence 双侧样本判定 compose 方法归属变化与边数增减来源；真机验证 PgcAutoActivityPopup。（E000, E006）
- F007 / retained：数值核对成立：mine_native（324/7/95）与 mine_account_model（132/0/54）双侧全一致仅 fingerprint 变。对按类名+方法名锚点功能低风险、字段级重命名待真机排除的判断与证据相符，作为 candidate 保留合理。（E000, E010）
- F008 / revised：数值核对成立（story_native 类 2944→2958、边 1376→1380、compose 44 不变；story_kotlin 双侧 consistent absent）。修正：+14 类不能断言为'新子组件或类拆分'——有界抽样下来源未知；删除草稿中'Kotlin moss 协议在另一路径存在'这一与 story 页无协议登记事实冲突的表述。（E000, E009）

### 尚未解决的证据缺口

- ["全部 25 条登记路径的真机 installer 采样与 runtime Hook 生效验证均未完成，runtime_enabled 全部 unknown；安装器/定位器覆盖一致性属待补证据", "dynamic_other:* 六个子家族与 dynamic_other_legacy 未调用方级核对（旧/新原生、Compose、Opus 并存栈与切换条件、平板/宽屏分支、服务端开关）", "KOpusMoss/KFeedMoss/KViewMoss/KWatchInterfaceMoss 等未注册核心协议 caller 家族归属与模块 Hook 覆盖差未逐条采样", "unregistered_protocols 清单未做基线对比，不能断言'非本次新增'", "comment_native_legacy target 侧类样本在深挖预算耗尽前未读取；E014 仅为 baseline 侧有界抽样", "comment_other_ui:* 六分支和 story_native +14 类需双侧完整类名集比对以区分混淆/迁移与新样式", "服务端 A/B 无结构变化时静态不可见，不宣称样式穷尽或适配通过", "source_dirty=true 时的源码修订哈希追踪与 CommentKotlinPurifier\<其他模块清单>全量清单轮补证（含 E012 截断处的 ProtobufReplyTreeRewriter）"]

## 下一步

- 在真机 9150200 上复验 CommentKotlinPurifier，抓 logSkip 排查 top-shape/links-shape 静默跳过
- 用 protocol_evidence 对 unregistered 核心协议（KReplyMoss/KOpusMoss/KFeedMoss/KViewMoss）采样 caller 家族，判断 Hook 未配置覆盖影响
- 对 comment 家族执行双侧全类清单比对，判定指纹变化是否为混淆/迁移而非新样式
- 真机复验所有 18 条登记路径的 installer 覆盖与 runtime Hook 生效，将结果回填运行时证据字段