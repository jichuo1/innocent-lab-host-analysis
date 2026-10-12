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

复核后结论：目标与基线同版本号、签名一致，小步重构发布。评论区多家族存在真实收缩与合并（native_legacy 173→156 类、209→177 边），compose 编译产物稳定（compose 方法 274 保持）；动态页存在跨家族真实重构证据（FollowingList 相关类字段由 Function 回调改为 ViewModel+LazyListState+State，legacy 边 +101，参数型类 U2→X2、W→Z）。comment_kotlin_moss 双侧 summary 与采样 caller 完全一致，变化局限于未采样段。全路径 runtime_enabled=unknown，禁止宣称适配通过。基线 summary 缺失家族（pgc/danmaku/story/mine）须补证。22 条未登记 K* MOSS 协议触发变化，建议 installer registry 补位或显式排除。

## 各页面评估

### comment

评论区多家族真实变化：legacy_v2 576→581 类、739→734 边；native_legacy 173→156 类、209→177 边（收缩显著）；native_next 46→45 类、49→46 边；native_exp3 边 66→59；compose 类 2420→2417、边 938→918、compose 方法 274 不变，产物结构稳定。java_moss 50/50 稳定；kotlin_moss 双侧 summary 与 caller 样本一致但指纹变化。runtime 均未知。

证据：E000, E007

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类 +5 / 边 -5 / 指纹更新
- 可能影响：CommentPurify/CommentSection 类名定位需核对
- 验证：真机进入评论區启用过滤插件并抓取 Hook 日志
- 证据：E007

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类 -17 / 边 -32，收缩最显
- 可能影响：疑似代码迁移，Hook 定位可能失效
- 验证：双侧类级反编译比对确认缺失类去向
- 证据：E007

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类 46→45、边 49→46
- 可能影响：影响轻微
- 验证：真机触发新样式评论区
- 证据：E007

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：边 -7，实验分支收缩
- 可能影响：服务端开关触发条件未知
- 验证：真机结合服务端开关验证实验组路径是否被选中
- 证据：E007

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类 -3 / 边 -20 / compose 方法数 274 保持
- 可能影响：影响低
- 验证：真机 compose 评论样式下插件行为
- 证据：E007

### dynamic

dynamic_legacy 3221→3227 类、2092→2193 边；compose 947→956 类、161→170 边，FollowingList 相关字段由 Function 回调改为 ViewModel+LazyListState+State；dynamic_opus 1333→1341 类、219→190 边。dynamic_java_moss 134/134 稳定；kotlin_moss req 类型 x9→v9、wrapper e1→g1。runtime 未知。

证据：E000, E008

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类 +6 / 边 +101；U2→X2、W→Z
- 可能影响：DynamicTabs/DynamicPurify 需重新核对
- 验证：真机动态页 Tab 与过滤功能
- 证据：E008

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：FollowingListViewModel依赖字段重构
- 可能影响：compose Hook lambda 语义可能偏移
- 验证：反编译 followinglist 新链路并真机验证列表
- 证据：E008

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类 +8 / 边 -29，api/q→r
- 可能影响：Opus Hook 命中点可能迁移
- 验证：真机动态图文详情页
- 证据：E008

### home

legacy 1008→1004 类、227→236 边；userprotocol/n 方法 b5→c5，main2/A0(WatchLaterFragmentV2) 在 target 采样未见。new_frame 197→196 类、48→46 边，khome/widget/bubble 保持。runtime 未知。

证据：E000, E004

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类 -4 / 边 +9；b5→c5、A0 样本未见
- 可能影响：HomeTopBarInstaller 依赖或漂移
- 验证：真机顶栏定制与稍后再看入口
- 证据：E004

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类 -1 / 边 -2，bubble 样本保留
- 可能影响：影响轻微
- 验证：真机新框架气泡组件
- 证据：E004

### search

search_native 1674 类不变、边 2898→2789、result/n→p 平移；compose 3149 类/556 方法不变、边 591→616。协议 java_moss 24/22、kotlin_moss 52/18。runtime 未知。

证据：E000, E005

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：边 -109、n→p 类号平移
- 可能影响：SearchPurify 定位或需更新
- 验证：反编译确认 n/p 关系后真机验证
- 证据：E005

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：边 +25，类/方法数不变
- 可能影响：低风险
- 验证：真机搜索样式
- 证据：E005

### detail

detail_legacy 两侧均空指纹（absent，不等于功能消失）；theseus_ugc 1951→1953 类、494→515 边；theseus_united 4589→4602 类、4167→4163 边。MOSS caller 样本全为跨家族。runtime 未知。

证据：E000, E003

#### 路径：detail_legacy

- 状态：absent
- 变化：两侧均为空指纹
- 可能影响：不适用
- 验证：真机确认实际使用 theseus 路径
- 证据：E003

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 +2 / 边 +21
- 可能影响：DetailViewPurify 命中点需比对
- 验证：真机 UGC 详情页
- 证据：E003

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 +13 / 边 -4；OgvClipParams 保留
- 可能影响：影响低
- 验证：真机 united 详情页
- 证据：E003

### pgc

pgc_legacy 353 类/401 边、pgc_theseus 2249 类/742 边（target）；基线 summary 本轮未取得，变化幅度未知。协议 player_moss 3 边、view_moss 7 边稀疏。runtime 未知。

证据：E000

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：target 353/401，基线未取得
- 可能影响：未知
- 验证：补做基线 family_evidence
- 证据：E000

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：target 2249/742，基线未取得
- 可能影响：未知
- 验证：补做基线 family_evidence
- 证据：E000

### player

player_java 948→953 类、3223→3225 边；playerbizcommon input/panels b→c、features/background c→d 平移。player_kotlin 7/100 保持。runtime 未知。

证据：E000, E006

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类 +5 / 边 +2，两处类号平移
- 可能影响：Player 系列 Installer 或需改定位
- 验证：反编译比对并真机验证
- 证据：E006

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：7/100 保持、指纹更新
- 可能影响：低风险
- 验证：真机播放历史功能
- 证据：E006

### danmaku

danmaku_legacy 两侧 absent；kotlin target 56 类/9 边、基线缺；java_moss 22/20、kotlin_moss 46/4。runtime 未知。

证据：E000

#### 路径：danmaku_legacy

- 状态：absent
- 变化：两侧均空
- 可能影响：不适用
- 验证：真机确认实际使用 kotlin 路径
- 证据：E000

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：target 56/9，基线未取得
- 可能影响：未知
- 验证：补基线 family 查询 + 真机弹幕
- 证据：E000

### story

native target 2958 类/1380 边；基线未完整取得，变化幅度未知。kotlin 两侧 absent。runtime 未知。

证据：E000

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：target 2958/1380，基线未取得
- 可能影响：未知
- 验证：补基线 story_native family_evidence
- 证据：E000

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧均空
- 可能影响：不适用
- 验证：无需
- 证据：E000

### mine

native target 324 类/95 边；account_model 132 类/54 边；基线均未取得，命中面未知。runtime 未知。

证据：E000

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：target 324/95，基线未取得
- 可能影响：未知
- 验证：补基线 family_evidence
- 证据：E000

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：target 132/54，基线未取得
- 可能影响：未知
- 验证：补基线 family_evidence
- 证据：E000

### F001：comment_native_legacy 家族类数明显收缩，疑似代码迁移而非新样式
comment_native_legacy 173→156 类、209→177 边，收缩幅度远大于同期评论路径；推断为代码迁移而非新样式。
反例与替代解释：若反编译显示仅为包装类合并或 DEX 重排，则非迁移。
建议：双侧类级反编译比对确认缺失类去向，再更新 CommentPurify 定位。
证据：E007

### F002：search_native search2/result 类号平移 n→p 及边数 -109
result/n 与 result/p 同具 getUpMid/setIsFollow，边数 -109，指向真实重构。
反例与替代解释：若 n/p 并列角色非平移链，需反编译确认。
建议：SearchPurifyFeatureInstaller 定位由 result/n 检查并迁移到 result/p。
证据：E005

### F003：player playerbizcommon input/panels 与 features/background 类号平移
input/panels b→c、background c→d 双处平移，类数 +5。
反例与替代解释：若为并列 wrapper 非平移链，需反编译确认。
建议：Player 系列 Installer 核对类号平移。
证据：E006

### F004：home userprotocol/n 方法 b5→c5 及 A0(WatchLaterFragmentV2) 样本消失
方法改名与样本类消失，仍需真机验证，且样本每家族仅 2 个不能断言类消失。
反例与替代解释：若 A0 未抽中但仍存在，则无须改动。
建议：真机验证顶栏定制与稍后再看入口。
证据：E004

### F005：dynamic FollowingListViewModel 结构变化：Function lambda 变为 ViewModel+State
Target 中 FollowingList 相关类字段由 Function 回调变为 ViewModel+LazyListState+State，是跨家族真实重构证据。
反例与替代解释：若仅为 Kotlin lambda 重排风险较小。
建议：反编译 followinglist 新链路并更新 DynamicTabs/DynamicPurify 定位。
证据：E008

### F006：detail MOSS caller 全为 external_or_unknown，需要 Installer 覆盖审查
kotlin/java moss 调用边全为 external_or_unknown，需要 Installer 覆盖审查。
反例与替代解释：若 caller 使用包级 fallback，风险降低。
建议：真机验证历史/暂停页广告链路，并审查 Installer 兜底策略。
证据：E003

### F007：detail AdPausedPage caller 段变化 requestPausedPage→receivePausedPageResult
调用链不同可能为暂停页流程变化，需反编译确认。
反例与替代解释：若 requestPausedPage 段仍存在则无需变更。
建议：反编译 AdPausedPageApi 全流程比对应变。
证据：E003

### F008：comment_kotlin_moss 指纹变化但 caller 样本一致，签名差异需反编译定位
双侧 summary 与 caller 样本完全一致，但家族指纹变化，说明变化仅在未采样段。
反例与替代解释：若变化仅为 DEX 重排可排除。
建议：反编译 KReplyMoss 相关签名差异才能判断 KotlinReplyBridge 是否需更新。
证据：E007

### F009：22 条未登记 K* MOSS 协议触发变化，installer registry 需补位或显式排除
changes 中 22 条 unregistered_protocol K* MOSS 触发变化。
反例与替代解释：若与模块无关，属数据侧变化。
建议：registry 补充或显式排除。
证据：E000

### F010：pgc/danmaku/story/mine 家族基线数据未取得，需补证
pgc/danmaku/story/mine 双侧 summary 缺失，变化幅度未知。
反例与替代解释：若补证结果一致则可列为稳定。
建议：对上述家族补基线 family_evidence 后再判断。
证据：E000

### F011：home_new_frame 结构极小变化，可作为新框架稳定参考
home_new_frame 类-1/边-2，样本基本保留，属变化最小路径，作为新框架侧锚点。
反例与替代解释：若服务端降级则真机验证更重要。
建议：保留现有定位，真机观察。
证据：E004

### F012：comment_compose 编译产物结构稳定，是一个正面锚点
compose 类 -3/边 -20，方法数 274 保持，为评论区最稳定锚点。
反例与替代解释：若服务端样式切换则需真机验证。
建议：保留 comment_compose Hook。
证据：E007

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
覆盖完成，F008 修订说明
证据：E000, E007

### 复核页面：dynamic
覆盖完成，F005 证据已重建并复核
证据：E000, E008

### 复核页面：home
覆盖完成，样本受限
证据：E000, E004

### 复核页面：search
覆盖完成，类号平移仍需反编译确认
证据：E000, E005

### 复核页面：detail
覆盖完成
证据：E000, E003

### 复核页面：pgc
基线缺失
证据：E000

### 复核页面：player
覆盖完成
证据：E000, E006

### 复核页面：danmaku
基线缺失
证据：E000

### 复核页面：story
基线缺失
证据：E000

### 复核页面：mine
基线缺失
证据：E000

- F001 / retained：双侧证据支持收缩，反编译类比对定位（E007）
- F002 / retained：target 证据明显平移，字段一致（E005）
- F003 / retained：平移真实（E006）
- F004 / retained：方法改名确定，类消失仍需样本外验证（E004）
- F005 / retained：双侧样本真实差异且一致性说明（E008）
- F006 / retained：本轮未评估对象，仍按 needs_runtime 保留（E003）
- F007 / retained：参数等变化支持真实重构（E003）
- F008 / revised：双侧 summary 与 caller 样本完全一致，断定需反编译；定性为未采样段变化（E007）
- F009 / retained：22 条触发变化属实，registry 补位（E000）
- F010 / needs_more_evidence：缺口明确，需补基线数据（E000）
- F011 / retained：结构小变化锚点可信（E004）
- F012 / retained：compose 方法数一致支持锚点（E007）

### 尚未解决的证据缺口

- pgc_legacy/pgc_theseus/danmaku_kotlin/story_native/mine_native/mine_account_model 双侧基线 summary 缺失，变化幅度未定
- KReplyMoss、KDynamicMoss 签名差异定位（反编译未完成）
- comment_native_legacy 缺失类去向未确认（未完成反编译类比）
- search result/n 与 result/p 平移链关系未经反编译确认
- player playerbizcommon 平移链关系未经反编译确认
- 22 条未登记 K* MOSS 协议 registry 处理状态未动作
- 全部路径 runtime_enabled=unknown，需真机 A/B 验证

## 下一步

- 双侧类级反编译比对 comment_native_legacy（173→156）
- 验证 SearchPurify 引用的 result/n 与 result/p 并更新
- Player 系列 Installer 核对 playerbizcommon 类号平移
- 真机验证 home 顶栏、稍后再看入口功能
- 反编译 followinglist 新链路并更新 DynamicHooks 定位
- 反编译 KReplyMoss/KDynamicMoss 变化细节
- 补做 pgc/danmaku/story/mine 家族基线 family_evidence
- installer registry 处理 22 条未登记 K* MOSS 协议
- 逐真机消除全部路径 runtime_enabled=unknown