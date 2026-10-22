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
| comment_compose | 2444 | 278 | 934 | static_invoke_observed |
| comment_legacy_v2 | 579 | 0 | 735 | static_invoke_observed |
| comment_native_exp3 | 58 | 0 | 62 | static_invoke_observed |
| comment_native_legacy | 172 | 0 | 211 | static_invoke_observed |
| comment_native_next | 45 | 0 | 50 | static_invoke_observed |
| comment_other_ui:(root) | 221 | 2 | 514 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 24 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 216 | 0 | 103 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 236 | 32 | 250 | static_invoke_observed |
| danmaku_kotlin | 57 | 1 | 8 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1946 | 25 | 510 | static_invoke_observed |
| detail_theseus_united | 4581 | 99 | 4257 | static_invoke_observed |
| dynamic_compose | 1136 | 127 | 221 | static_invoke_observed |
| dynamic_legacy | 3251 | 105 | 2151 | static_invoke_observed |
| dynamic_opus | 1352 | 92 | 186 | static_invoke_observed |
| dynamic_other:appointment | 25 | 3 | 18 | static_invoke_observed |
| dynamic_other:card | 423 | 87 | 306 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 60 | static_invoke_observed |
| dynamic_other:commonPerf | 11 | 1 | 4 | static_invoke_observed |
| dynamic_other:commonUi | 21 | 5 | 8 | static_invoke_observed |
| dynamic_other:lightBrowser | 80 | 19 | 27 | static_invoke_observed |
| dynamic_other_legacy | 2108 | 4 | 2152 | static_invoke_observed |
| home_legacy | 767 | 87 | 204 | static_invoke_observed |
| home_new_frame | 196 | 33 | 49 | static_invoke_observed |
| mine_account_model | 132 | 0 | 43 | static_invoke_observed |
| mine_native | 325 | 7 | 92 | static_invoke_observed |
| pgc_legacy | 354 | 0 | 399 | static_invoke_observed |
| pgc_theseus | 2265 | 131 | 782 | static_invoke_observed |
| player_java | 958 | 0 | 3222 | static_invoke_observed |
| player_kotlin | 7 | 0 | 100 | static_invoke_observed |
| search_compose | 3141 | 561 | 595 | static_invoke_observed |
| search_native | 1702 | 2 | 2859 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2924 | 44 | 1310 | static_invoke_observed |

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

本单元仅覆盖 comment（5 条路径）与 dynamic（3 条路径），目标 tv.danmaku.bili 9.16.1（vc9161100, sha256 41efb1c9…，E000）对比基线 9.16.0（vc9160200, a80c4e01…，E000）。八条登记路径的静态证据级别全部逐字为 static_invoke_observed，没有任何一条经安装器校验或真机验证，runtime_enabled 与 module_coverage 均为 unknown / requires_installer_review；因此本报告只能给出候选与待验证项，不能宣称适配通过。协议层两侧完全一致：comment_java_moss 50/50、comment_kotlin_moss 130 定义仅 26 条实际调用边、dynamic_java_moss 134/134、dynamic_kotlin_moss 382 定义仅 26 条实际调用边（E001/E002）。八个家族指纹全部变化，但类数与 compose 方法数基本持平：comment_compose 2446→2444（compose 方法恒为 278）、dynamic_legacy 3252→3251、dynamic_opus 1354→1352，其余家族类数不变，说明指纹漂移主要指向重排/编译器变化候选，而非可确认的新样式。深挖复核（E011/E012）显示 comment_compose 样本中多数方法体哈希两侧一致，仅 CardInteractionService 的方法体哈希发生分歧。源码快照为 published_unverified_worktree 且 working_tree_dirty=true（E000），本轮按限制未读取模块源码，模块 Hook 是否命中相关类不可推断。

本单元覆盖 home（home_legacy、home_new_frame）与 search（search_native、search_compose）四条登记路径，对比 9.16.1(9161100) 与 9.16.0(9160200)。四条路径两侧均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，故只能确认静态调用存在，不能确认样式启用或 Hook 生效。home_legacy 出现类数 767→769 之外的微差（769→767）、调用边 211→204 与样本内短名语义漂移；home_new_frame 类数与 Compose 方法数不变但哈希变化；search_native/search_compose 仅类数与调用边有 ±4/±8 级微动，search_java_moss(24/22)、search_kotlin_moss(52/18) 两侧完全一致。源码快照 working_tree_dirty=true，未在本次额度内读取模块源码，安装器与定位器覆盖仍为未知。

本单元仅覆盖 detail 与 pgc 两页共四条登记路径（detail_legacy 为 absent，其余三条 static_invoke_observed）。9.16.1 相对 9.16.0：detail_theseus_ugc 类 1947→1946、外部调用边 509→510、指纹变化；detail_theseus_united 类 4579→4581、compose 方法均 99、边 4312→4257；pgc_legacy 类 354 不变、compose 0、边 386→399；pgc_theseus 类 2264→2265、compose 131 不变、边 1328→782。四个已登记协议（detail_java_moss 32/35、detail_kotlin_moss 76/10、pgc_player_moss 12/3、pgc_view_moss 14/7）两侧定义数与调用边完全相同，资源侧仅 1 个 changed、0 增删。全部路径 runtime_enabled=unknown、module_coverage=requires_installer_review，源码工作树为 dirty 冻结快照，故本报告只给候选判断与待验证任务，不宣称适配通过。结构指纹变化不等于新样式，边数下降亦不等于功能消失。

本单元审计 player 与 danmaku 两页，样本 9.16.1(9161100) 对基线 9.16.0(9160200)，同包同证书（E000）。静态矩阵显示：player_java 957→958 类、外部调用边 3229→3222、指纹变；player_kotlin 7 类/0 Compose/100 边两侧完全一致，仅指纹变；danmaku_legacy 两侧均 absent；danmaku_kotlin 57 类/1 Compose/8 边两侧一致，仅指纹变。Moss 协议侧 player_java_moss(18/2)、player_kotlin_moss(34/3)、danmaku_java_moss(22/20)、danmaku_kotlin_moss(46/4) 两侧定义数与调用边数均未变。三处 change 均标 structure_or_call_path_changed，但计数未动者更符合 DEX 重排/混淆改名导致的指纹漂移，属候选而非确认新样式（E007、E008、E011、E012）。模块侧 689 文件源码为脏工作树冻结快照（source_dirty=true），未读模块解析点，hook 覆盖与安装器/定位器兜底一律未知；runtime_enabled 全为 unknown，不得宣称适配通过。

本单元覆盖 story 与 mine 两页共 4 条登记路径。9.16.1 相对 9.16.0：story_native 类数 2924→2925 下降 1、外部调用边 1310→1318 下降 8、Compose 方法 44 不变，指纹变化；story_kotlin 两侧均为空集（同一空指纹），属 absent 而非功能消失；mine_native 类数 325→328、边 92→91，mine_account_model 类数、边数、Compose 数完全一致（132/132、43/43、0）但指纹变化，更像方法体级改动或混淆/DEX 重排。四路径 evidence 与运行时启用均为 unknown，module_coverage 均为 requires_installer_review：静态调用存在不证明真机启用、也不证明模块 Hook 生效，本报告不宣称适配通过。源码快照 working_tree_dirty，需按文件哈希追溯；模块 installer 未读全文，Hook 覆盖不推测。未登记协议含 StoryMoss、MineMoss/KMineMoss、OpusMoss/KOpusMoss 等，跨家族消费者未登记，不得据协议名推断覆盖。

## 各页面评估

### comment

评论区共登记 5 条路径，全部为 static_invoke_observed，运行时启用状态未知。对比 9.16.0→9.16.1：comment_legacy_v2 类数 579 不变、外部调用边 735→743（+8）；comment_native_legacy 172→172、211→209（−2）；comment_native_next 45→45、50→49（−1）；comment_native_exp3 58→58、62→61（−1）；comment_compose 2446→2444（−2）、932→934（+2），且两侧 compose 方法数均为 278（E001）。五条路径指纹全部变化，但没有一条显示 compose 方法数或类规模的量级跳变，因此不能判定出现了新的评论样式。深挖对比（E011/E012）中，kntr/common/comment/common/service/b 与 h 的 method_bodies_sha256 两侧完全一致（ed8ead98…、990bc7a3…），kntr/common/comment/imageviewer/data/c 与 card/action/CardAction 两侧方法体均为空（e3b0c442…），唯一分歧在 CardInteractionService 的方法体哈希（基线 829a5c51… → 目标 6e3f9633…）。这提示 comment_compose 内存在个别方法体级改动候选，而非整套重写，但方法体哈希对混淆改名、DEX 重排、inline 与调试信息敏感，需按字节码复核。协议层 comment_java_moss 50/50、comment_kotlin_moss 130 定义仅 26 条实际调用边，两侧一致，说明评论共同协议本身未变；但 Kotlin Moss 的 104 条定义无静态调用边，接口分发或反射消费者无法解析。另需注意 ReplyMoss 与 KReplyMoss 出现在未登记协议列表中（E000），已登记的两个协议可能不是评论原生链路的全部消费者，跨家族实际调用边与安装器/定位器覆盖仍未核实，模块源码本轮未读，覆盖情况记未知。

证据：E000, E001, E011, E012

#### 路径：comment_legacy_v2

- 状态：static_invoke_observed
- 变化：类数 579 不变，外部调用边 735→743（+8），指纹 33676515…→8d381d51…；为本页路径中调用边漂移最大者。
- 可能影响：若 +8 条边来自新增调用者，legacy 评论区的类定位器与复制/净化桥可能需要在 9.16.1 上重新核对命中；若为识别信息漂移则影响有限，但仍属未知。
- 验证：对该家族取两侧类样本对比 method_bodies_sha256 与方法签名，定位新增的 8 条外部调用边归属类；真机 9.16.1 中确认 CommentClassicStyleLocator 是否命中并输出绑定日志。
- 证据：E001, E000

#### 路径：comment_native_legacy

- 状态：static_invoke_observed
- 变化：类数 172 不变，外部调用边 211→209（−2），指纹 3219e4f0…→e5428418…。
- 可能影响：−2 边可能是内联或包装层合并，也可能是某条原生绑定调用被移除；模块对该家族绑定目录的覆盖是否仍对齐未知。
- 验证：用 family_evidence 取两侧类样本比对方法体哈希与字段；对 CommentNativeBindingCatalog 的绑定项逐个在 9.16.1 中确认类/方法是否存在（仅静态存在性，不证明启用）。
- 证据：E001

#### 路径：comment_native_next

- 状态：static_invoke_observed
- 变化：类数 45 不变，外部调用边 50→49（−1），指纹 07ff5e26…→4a3fda7a…。
- 可能影响：规模极小且仅一条边差异，最可能来自编译器内联或重排；但若该边为宿主入口调用，则此家族在 9.16.1 是否仍被装载未知。
- 验证：定位这 1 条差异边的具体被调方，核对是否位于模块已登记的入口类/方法签名内；真机验证该家族页面样式是否切换（区分样式候选与已确认样式）。
- 证据：E001

#### 路径：comment_native_exp3

- 状态：static_invoke_observed
- 变化：类数 58 不变，外部调用边 62→61（−1），指纹 067a483c…→4ef234c4…。
- 可能影响：与 native_next 同类的小幅漂移，影响面取决于服务端是否把 exp3 样式当默认；静态结构无证据表明该实验样式被移除或新增。
- 验证：核对该 1 条边差异的方法是否被 CommentNativeSupplementBridge 引用；配合服务端开关抓包/日志确认 exp3 是否在目标版本仍被投放（服务端 A/B 静态不可见）。
- 证据：E001

#### 路径：comment_compose

- 状态：static_invoke_observed
- 变化：类数 2446→2444（−2），外部调用边 932→934（+2），compose 方法数两侧均为 278，指纹 1b4eddf5…→48046cbe…；深挖样本显示 CardInteractionService 方法体哈希由 829a5c51… 变为 6e3f9633…，其余抽样方法与空方法体类两侧一致。
- 可能影响：个别方法体改动可能影响 Compose 评论卡片交互（emoji、复制桥、净化桥、回复按钮）所依赖的签名；但不可据此断定 Compose 样式变更或 Hook 失效。
- 验证：对 CardInteractionService.d 两侧做 JADX 字节码比对并列出调用者；确认减少的 2 个类是否为匿名类/包装层合并；真机 9.16.1 打开视频评论区，记录 CommentComposeCopyBridge / CommentComposePurifyBridge / CommentReplyButtonCompose 的安装日志与命中情况。
- 证据：E011, E012, E001

### dynamic

动态页共登记 3 条路径，全部为 static_invoke_observed，运行时启用未知。对比 9.16.0→9.16.1：dynamic_legacy 类数 3252→3251（−1）、外部调用边 2152→2151（−1）、compose 方法 105 不变；dynamic_compose 类数 1136 不变、外部调用边 220→221（+1）、compose 方法 127 不变；dynamic_opus 类数 1354→1352（−2）、外部调用边 191→186（−5）、compose 方法 92 不变（E002）。三条路径指纹全部变化，但 compose 方法数三条路径两侧完全不变，且类数变动均在 ±2 以内，因此最可能的解释是 DEX 重排、混淆改名或少量包装层增减，而不是新增/删除一整套动态样式。唯一需要单列的是 dynamic_opus 的外部调用边相对收缩 −5（约 2.6%），是八条路径中调用边缩减比例最大者，若这 5 条边指向模块依赖的宿主入口，则 Opus 动态卡片的净化与标签 Hook 可能绑定到已变更的调用点；反之若差异来自内联，则静态边减少而功能保留。协议层 dynamic_java_moss 134/134、dynamic_kotlin_moss 382 定义仅 26 条实际调用边，两侧一致，说明共同协议未见变化，但 Kotlin Moss 有 356 条定义无静态调用边，接口分发与反射路径无法解析。未登记协议列表含 DynamicMoss、OpusMoss、KOpusMoss、KTribeeMoss、CampusMoss 等（E000），因此已登记的两条协议未必是动态页/Opus 家族的真实消费者，跨家族消费者与 DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller 的安装器覆盖、兜底逻辑本轮均未读取源码，记未知。

证据：E000, E002

#### 路径：dynamic_legacy

- 状态：static_invoke_observed
- 变化：类数 3252→3251（−1），外部调用边 2152→2151（−1），compose 方法 105 不变，指纹 e3738343…→a02ef6a4…。
- 可能影响：减 1 类 1 边属最小粒度漂移，可能是内部类合并或编译器变化；若被移除的类承载动态卡片绑定，则 legacy 动态列表的部分净化/标签逻辑可能失去锚点（未知）。
- 验证：用 family_evidence 拉取两侧类样本，比对 method_bodies_sha256 定位缺失类名；在 9.16.1 真机上确认 DynamicPurifyFeatureInstaller 与 DynamicTabsFeatureInstaller 是否安装成功并打印绑定类名。
- 证据：E002

#### 路径：dynamic_compose

- 状态：static_invoke_observed
- 变化：类数 1136 不变，外部调用边 220→221（+1），compose 方法 127 不变，指纹 3c0596bc…→a43e5e59…。
- 可能影响：结构规模与 compose 方法数均未变，仅 1 条新边；最可能为重排或内联差异，但新增边若来自新调用者，可能绕过现有 Compose 净化策略的作用点。
- 验证：定位这 1 条新增外部调用边的源类与被调方法，判断其是否为 Compose 组件的共同协议消费者；真机对比同一动态条目在纯净模式开关前后的渲染差异。
- 证据：E002

#### 路径：dynamic_opus

- 状态：static_invoke_observed
- 变化：类数 1354→1352（−2），外部调用边 191→186（−5，本页缩减最大），compose 方法 92 不变，指纹 008f9bfd…→70dd32b0…。
- 可能影响：Opus 家族调用边收缩可能意味着部分调用被内联、迁移到其他家族，或某条宿主入口被移除；若为后者，Opus 卡片上的净化与标签逻辑可能不再被触发，当前无证据判定。
- 验证：对两侧 Opus 家族类样本逐一比对方法体哈希，列出减少的 2 个类与 5 条边；核查这些边是否与 KotlinDynamicMossWatch / DynamicPurifyPolicy 使用的类名相关；真机进入动态页 Opus 图文条目验证 Hook 命中日志。
- 证据：E002, E000

### home

home 两条路径均在静态层观察到对宿主类的调用，但两侧 runtime_enabled 均为 unknown，module_coverage 均 requires_installer_review，无法据此判断首页新旧框架在真机哪条启用。home_legacy 目标侧 767 类/87 Compose 方法/204 调用边，基线 769/87/211，Compose 方法数持平而类数与调用边下降，fingerprint 由 8772cd… 变为 7a842b…。深挖样本 E013/E014 显示不能把哈希变化直接当作新样式：短名 Ltv/danmaku/bili/ui/main2/A0 在基线是 WatchLaterFragmentV2 的对话框 onClick 回调（字段为 WatchLaterFragmentV2、FragmentActivity），在目标侧变为接收 MenuItemBean 的消费者（字段为两个 Object），属典型的混淆短名复用/字母重排；而同名 A 类字段与方法签名完全一致但 method_bodies_sha256 由 156a32… 变为 9ce5e1…，AccountMineRequestResource 枚举方法集完全一致、方法体哈希由 e50c7b… 变为 0de665…，更像编译器/R8 产出差异或局部实现调整。home_new_frame 目标与基线均为 196 类、33 Compose 方法，调用边 48→49、fingerprint 由 086965… 变为 4a3e90…，本单元未取得该类家族的类级样本（深挖额度耗尽），变化性质未知。模块侧 HomeFrameListHook、HomeFrameTabLocator、HomeComponentFilterFeatureInstaller、HomeTopBarFeatureInstaller 等按类名/方法签名定位的实现未读取，其对 9.16.1 的命中与兜底不能推测。所有登记路径 status 逐字沿用 static_invoke_observed，不视为适配通过。

证据：E003, E013, E014

#### 路径：home_legacy

- 状态：static_invoke_observed
- 变化：类数 767（基线 769）、external_invoke_edges 204（基线 211）、compose_methods 双侧同为 87，fingerprint 7a842b… vs 8772cd…；样本内 A0 短名从 WatchLaterFragmentV2 回调变为 MenuItemBean 消费者，A 与 AccountMineRequestResource 方法体哈希变化。
- 可能影响：若 HomeFrameListHook/HomeFrameTabLocator 等定位器以类名+方法签名匹配，短名复用会使定位命中错误类或落空；但类数差 2 更可能来自裁剪/合并，不能认定首页旧框架样式消失。
- 验证：在 9.16.1 真机开启模块并抓取定位器命中/未命中日志，逐一比对 HomeFragmentV2 侧 Hook 入口是否被调用；用 JADX 读取 Ltv/danmaku/bili/ui/main2/A0 与 A 的实际调用点，确认短名映射是否只是字母重排。
- 证据：E003, E013, E014

#### 路径：home_new_frame

- 状态：static_invoke_observed
- 变化：类数 196 与 compose_methods 33 两侧一致，external_invoke_edges 48→49，fingerprint 4a3e90… vs 086965…；本单元未取得该家族类级样本。
- 可能影响：新增 1 条外部调用边与哈希变化的语义未知，可能影响新框架首页 Tab/列表侧 Hook 的定位假设，也可能仅为 DEX 重排。
- 验证：对 home_new_frame 双侧各取类级样本（family_evidence）比对方法体哈希分布，定位新增调用边的来源类；随后在真机 9.16.1 上确认该框架是否被首页实际加载。
- 证据：E003

### search

search 两条路径同样登记为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review。search_native 目标与基线类数完全一致（1702），compose_methods 均为 2，external_invoke_edges 由 2851 增至 2859（+8），fingerprint 由 bc8afd… 变为 28a11e…；search_compose 类数 3141（基线 3145，-4），compose_methods 双侧 561，调用边 594→595，fingerprint 由 e0ff41… 变为 fcde68…。两条协议侧统计在目标与基线完全一致：search_java_moss 定义 24、实际调用边 22；search_kotlin_moss 定义 52、实际调用边 18，说明搜索域 MOSS 协议面在本版本未见新增或删除，样式候选不能由协议计数确认。同时猎取列表外仍存在大量未登记协议（含 app/search/v2/SearchMoss、KSearchMoss、broadcast/message/search/SearchMoss 等），其消费者未纳入本单元登记路径。搜索模块侧 SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt 本次未读取（工具额度耗尽），因此首页推荐净化与默认词清理在新版是否仍有兜底路径属未知，不能写为无影响。类数与调用边的微差也可能来自 DEX 重排或 R8 裁剪，未取得 search 家族类级样本，故“是否有新样式”维持待查。

证据：E004

#### 路径：search_native

- 状态：static_invoke_observed
- 变化：类数 1702 两侧一致，compose_methods 2 一致，external_invoke_edges 2851→2859（+8），fingerprint bc8afd… → 28a11e…；未取得类级样本。
- 可能影响：调用边增加 8 条可能改变搜索原生页外部依赖面，进而影响以调用关系推断的 Hook 入口选择；类集合不变降低了“整族替换”的可能性，但无法排除新增样式类被并入同一家族。
- 验证：对 search_native 双侧各取类级样本比对新增边来源类与方法体哈希；真机 9.16.1 上进入搜索页抓取 SearchHomeRecommend 相关 Hook 是否命中及命中类名。
- 证据：E004

#### 路径：search_compose

- 状态：static_invoke_observed
- 变化：类数 3141（基线 3145，-4），compose_methods 561 两侧一致，external_invoke_edges 594→595，fingerprint e0ff41… → fcde68…；未取得类级样本。
- 可能影响：Compose 方法数不变而类数下降 4，可能为合并/裁剪而非样式删除；若 SearchHomeRecommendPolicy 依赖具体 Compose 类名或方法签名，需确认定位是否仍命中。
- 验证：定向读取 SearchHomeRecommendLocator.kt 与 SearchHomeRecommendPolicy.kt 的匹配条件，并在 9.16.1 上核对被匹配类是否存在；对 search_compose 做双侧类级样本比对确认减少的 4 个类身份。
- 证据：E004

### detail

detail 三个登记路径中，detail_legacy 两侧 classes/compose_methods/external_invoke_edges 均为 0、指纹完全相同（4f53cda1…，为空集合固定序列化值），因此 evidence 维持 absent——这是“两侧都未索引到该类家族”，不是本次被移除，推断由 statics 判定逻辑而非真实删除造成。两个 Theseus 家族都是 static_invoke_observed：ugc 类数 -1、外部调用边 +1，united 类数 +2、外部边 -55（4312→4257），compose 方法数两侧保持 25 与 99 不变。协议层 detail_java_moss（32 定义 / 35 实际边）与 detail_kotlin_moss（76 定义 / 10 实际边）两侧数字完全相同，提示共同协议接口面未变；注意定义数与调用边是不同单位，禁止相除推导覆盖率，且 76 定义仅 10 条边说明大量协议成员静态上无消费者，未解析接口派发。模块侧候选源码覆盖 DetailModulePurify*、DetailUnitedModulePurify*、DetailUnitedPresentationPurify*、DetailViewPurify*、DetailAppPromotion、HomeVerticalDetailRouting 等 Installer/Policy，但各 Installer 在 9.16.1 的版本适配、定位器命中与兜底均未核实（源码快照 working_tree_dirty=true，需按文件哈希追溯）。结论：结构有变动、影响面未知，需真机与安装器日志确认。

证据：E000, E005

#### 路径：detail_legacy

- 状态：absent
- 变化：两侧均为 0 类、0 compose 方法、0 外部调用边，指纹同为 4f53cda1…（空集合固定值），无相对变化。
- 可能影响：若 HomeVerticalDetailRouting/HomeVerticalDetailFeatureInstaller 或其他 Installer 仍按 legacy 类名定位，则该侧无静态锚点，Hook 可能静默不安装；但不能据此断言详情页功能缺失，可能统一走 Theseus 家族。
- 验证：在真机抓取详情页加载日志，确认模块 VersionAdapter/路由分支是否进入 legacy 分支；对 HomeVerticalDetailRouting 的判定条件按源码哈希复核；若确认走 Theseus，则记录 legacy 为“长期 absent、无需覆盖”而非回归。
- 证据：E000, E005

#### 路径：detail_theseus_ugc

- 状态：static_invoke_observed
- 变化：类 1947→1946、compose 方法 25→25 不变、外部调用边 509→510、结构指纹由 5cd2f7c7…变为 6725089730f0…。
- 可能影响：UGC 详情 Theseus 家族结构指纹变化而 compose 方法数不变，更像混淆改名/DEX 重排或包装层微调；若模块按类名/方法签名常量定位这些 Hook 点，则可能命中失败，涉及详情页模块净化与推广位屏蔽。
- 验证：对两侧 detail_theseus_ugc 类样本按 method_bodies_sha256 对齐，找出哈希变化的具体类；用 module_source 复核对应 Installer 的定位字符串是否仍存在；真机抓 Hook 安装日志与页面模块列表。
- 证据：E000, E005

#### 路径：detail_theseus_united

- 状态：static_invoke_observed
- 变化：类 4579→4581、compose 方法 99→99 不变、外部调用边 4312→4257（-55）、指纹由 519ae33f…变为 b0f0b041…。
- 可能影响：类数与 compose 数几乎不变而外部边明显减少，属于调用边层面的变动，可能来自内联/包装层合并或派发点被改写，而不是整块样式下线；若净化策略按调用边上下游定位，可能漏挂或误挂。
- 验证：用 family_evidence 分别重读两侧 detail_theseus_united，比对边下降集中在哪些调用者类；再对 DetailUnitedModulePurifyPolicy/DetailUnitedPresentationPurifyPolicy 的匹配条件做 module_source 复核；真机对比净化前后模块清单。
- 证据：E000, E005

### pgc

pgc 两条登记路径均为 static_invoke_observed。pgc_legacy：类 354→354 不变、compose 方法两侧为 0、外部调用边 386→399（+13）、指纹由 b77616da…变为 2c5cf1a4…；pgc_theseus：类 2264→2265、compose 方法两侧均 131 不变、外部调用边 1328→782（-546）、指纹由 ede5e8c1…变为 4df56dbb…。协议层 pgc_player_moss（12 定义 / 3 实际边）与 pgc_view_moss（14 定义 / 7 实际边）两侧完全一致，说明已在册的共同协议面没有新增/删除，PGV/PGC 播放与视图接口的静态消费者数量未变。关键反例：theseus 边数下降 41% 而类数与 compose 方法数基本不变，更符合调用边在被内联、包装层合并或 DEX 重排后无法解析到目标，而非页面样式减少；legacy 边数 +13 同理可能只是新增包装层。已知模块侧对应源码仅 PgcAutoActivityPopupFeatureInstaller/PgcAutoActivityPopupPolicy/PgcAutoActivityPopupLocator，其 Locator 在 9.16.1 是否命中、legacy 与 theseus 双栈切换条件、平板/宽屏布局与服务端开关均未读到运行条件，记为未知。不得由本次数字变化推断 PGC 自动弹窗抑制已失效或仍有效。

证据：E000, E006

#### 路径：pgc_legacy

- 状态：static_invoke_observed
- 变化：类数 354 两侧相同、compose 方法 0、外部调用边 386→399（+13）、指纹变化。
- 可能影响：legacy PGC 仍被静态索引，边数上升可能新增包装层或调用者；若 PgcAutoActivityPopupLocator 依赖 legacy 类名清单，新增调用者可能带来未被匹配的弹窗触发点，也可能完全无影响，当前未知。
- 验证：重读两侧 pgc_legacy 类样本，按方法体哈希定位新增/变化的调用者；module_source 读取 PgcAutoActivityPopupLocator 的候选类与兜底逻辑；真机在 legacy PGC 页（含平板宽屏）验证活动弹窗是否被抑制。
- 证据：E000, E006

#### 路径：pgc_theseus

- 状态：static_invoke_observed
- 变化：类 2264→2265、compose 方法 131 不变、外部调用边 1328→782（-546）、指纹变化。
- 可能影响：调用边大幅减少而结构规模不减，最可能是边解析失效（混淆/内联/接口派发未解析），其次是真实调用路径收敛；若模块按调用边或调用者签名定位 Theseus PGC 弹窗与播放层 Hook，可能出现匹配下降。
- 验证：对两侧 pgc_theseus 做类样本与方法体哈希对齐，确认是否有类整体消失；抽样反编译边减少最集中的类，检查是否方法体被内联/合并；真机 Theseus PGC 页验证 PgcAutoActivityPopup 行为并抓安装器日志。
- 证据：E000, E006

### player

player 两路径均为 static_invoke_observed，运行时启用未知。player_java 类数 957→958（+1）、外部调用边 3229→3222（-7），指纹由 f99b12… 变 2830ee…；量级变化很小且方向相反，无法直接判为新样式，需在全量家族视图里定位新增类与被移除的调用边（E007）。player_kotlin 类数 7、Compose 0、边 100 三项与基线逐字相同，仅指纹由 544b8d… 变 c20595…，这是“结构不变、指纹变”的典型形态，优先怀疑 DEX 重排/混淆改名或编译期布局变化，而不是新播放器样式（E007）。协议侧 player_java_moss 18 定义/2 实际调用边、player_kotlin_moss 34 定义/3 实际调用边，两侧完全相同，说明播放器相关共同协议的定义面与消费者边数未变，但这不等于模块 Hook 命中（定义数与调用边数单位不同，不可相除推覆盖率）。模块源码包含 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、SponsorPlayerLocator、PlayerCapabilityAccess 等按名/按签名定位的适配层，但这些文件的解析结果本轮未读，定位器命中与兜底策略保持未知；HookEntry、VersionAdapter、KotlinMossChannel、KotlinMossReplyBridge 被登记为 unmapped_multi_path_candidates，未映射到本页任一路径，属未归类调用者，需单列跟踪。结论：播放器页存在可复核的结构差异候选，但启用条件、安装器覆盖与真机效果均未知（E007、E000）。

证据：E000, E007, E011, E012

#### 路径：player_java

- 状态：static_invoke_observed
- 变化：类数 957→958（+1），外部调用边 3229→3222（-7），指纹 f99b12…→2830ee…，非等比变动，指向局部类增删与调用点迁移而非整体重写
- 可能影响：若被移除的 7 条边落在模块定位器所依赖的类/方法签名上，PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess 等按名解析可能退化到兜底分支；若新增类为包装层或重复层则影响可忽略
- 验证：对两侧家族做全量类清单与 body hash diff，定位新增类名与被删边的调用方/被调方，再用 decompile_class 读对应类确认是改名包装还是真实逻辑变化；真机侧打开模块自检日志比对定位器命中与回落
- 证据：E000, E007

#### 路径：player_kotlin

- 状态：static_invoke_observed
- 变化：类数 7、Compose 方法 0、外部调用边 100 三项与基线完全一致，仅指纹 544b8d…→c20595…，属结构不变型指纹漂移
- 可能影响：player_kotlin_moss 定义 34/实际调用边 3 也未变，故更可能是 DEX 重排或混淆改名；若模块以类名硬编码锚定 Kotlin 播放器侧实现，改名仍会打断解析，但当前无证据表明方法或边发生变化
- 验证：逐类比对 7 个 Kotlin 类的 full name 与 method_bodies_sha256；在真机对 KotlinMoss 通道打印解析到的定义者类与方法名，确认是否与快照中 KotlinMossChannel 的期望签名一致
- 证据：E007

### danmaku

danmaku_legacy 两侧 evidence 均为 absent、类数与边数为 0、指纹为同一空集指纹 4f53cd…，属一致的“未观测到”，不能推断该页面旧原生弹幕样式被删除或功能消失；absence 也可能来自家族登记口径或识别规则未覆盖（E008）。danmaku_kotlin 为 static_invoke_observed：57 类、1 个 Compose 方法、8 条外部调用边在两侧逐字相同，仅指纹由 7f0a50… 变 323c06…，与 player_kotlin 呈现同一模式，优先归因于 DEX 重排/改名或编译期变化，而不是新增弹幕样式（E008）。协议侧 danmaku_java_moss 为 22 定义/20 实际调用边，danmaku_kotlin_moss 为 46 定义/4 实际调用边，两侧未变：弹幕相关共同协议的实际消费者明显集中在 Java 侧，Kotlin 侧定义多而消费少，若净化逻辑只挂在 Kotlin 通道上，覆盖面会是问题，但这属于推断，需读模块源码确认（E008）。模块侧 DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy 等净化安装器/策略文件存在，但本轮未读取其目标类与失败兜底，因此不得声称弹幕净化 Hook 在新版本仍生效；1 个 Compose 方法的存在说明该家族含 Compose 成分，运行条件未读到，是否启用为未知。资源侧本次 changed=1、added/removed=0，不构成本页样式变化的证据。综上，danmaku 页无已确认样式变化，只有待复核候选与多处未知（E008、E000）。

证据：E000, E008

#### 路径：danmaku_legacy

- 状态：absent
- 变化：目标与基线均为 absent，类数 0、Compose 0、外部调用边 0，空集指纹 4f53cd… 两侧相同，无新增或消失的结构差异可复核
- 可能影响：无法据此判断旧原生弹幕实现是否仍存在；若模块曾针对 legacy 家族安装 Hook，该 Hook 在本版本的静态侧无锚点可验证，落空与否只能靠运行时观测
- 验证：在真机打开弹幕净化与相关开关，抓取模块日志确认是否出现 legacy 家族解析失败/跳过记录；同时用全量家族清单检索弹幕相关包路径，确认 absent 是识别口径问题还是实现确实不在此家族
- 证据：E008

#### 路径：danmaku_kotlin

- 状态：static_invoke_observed
- 变化：57 类、1 个 Compose 方法、8 条外部调用边两侧完全一致，仅指纹 7f0a50…→323c06…，判定为结构不变型指纹漂移候选
- 可能影响：danmaku_kotlin_moss 定义 46/调用边 4 未变，说明协议面稳定；风险集中在模块是否以硬编码类名/方法名解析该家族，若是，改名即失效且不体现在计数上
- 验证：比对两侧 57 类的方法体哈希与签名集合，确认是否存在仅改名不改结构；随后在真机开启弹幕净化，验证实际被拦截的弹幕元素与模块日志中的解析命中，并检查未归类调用者是否消费同一家族
- 证据：E008

### story

story_native 在 9.16.1 仍为 static_invoke_observed：2924 类、44 个 Compose 方法、1310 条外部调用边；基线为 2925/44/1318，指纹由 7fffa3be… 变为 b56b7342…。计数呈小幅下降，Compose 方法数不变，指向局部重构、类迁移或混淆改名，而非可确认的新样式；单条调用边/类减少也可能来自编译器与 DEX 重排。story_kotlin 两侧 total_classes=0 且空集指纹一致（4f53cda…），即该家族在快照中始终缺席，不能读作 Kotlin 侧样式被移除或页面功能消失。本页未登记任何协议（protocols 为空），unregistered_protocols 中的 StoryMoss、OpusMoss/KOpusMoss 等只能作为待查线索，共同协议是否有跨家族消费者、安装器/定位器是否覆盖均未知。模块侧存在 StoryPurifyFeatureInstaller、StoryActionIconsFeatureInstaller/Policy、HomeVerticalDetailFeatureInstaller/Routing 等文件，本轮未读取其目标描述符，故不能判断 Hook 点是否仍落在 story_native 现存类上。运行时启用状态与服务端开关导致的样式差异静态不可见，需真机验证。

证据：E009

#### 路径：story_native

- 状态：static_invoke_observed
- 变化：类数 2924（基线 2925，-1）、Compose 方法 44（不变）、外部调用边 1310（基线 1318，-8），家族指纹由 7fffa3be… 变为 b56b7342…；变化幅度小且以减少为主。
- 可能影响：若被移除的 1 个类或 8 条边端点涉及模块挂点（StoryPurify / StoryActionIcons 的目标方法），对应 Hook 在 9.16.1 可能静态不命中；也可能只是无关类裁剪或 DEX 重排，对模块零影响，当前无法区分。
- 验证：用 family_evidence 重读 story_native 两侧完整类级 method_bodies_sha256 清单做差集，定位消失类与 8 条边端点；将 StoryPurifyFeatureInstaller.kt、StoryActionIconsFeatureInstaller.kt 中的目标类描述符逐一比对 9.16.1 DEX；真机进入动态页抓 Xposed 日志确认命中与样式生效。
- 证据：E009

#### 路径：story_kotlin

- 状态：absent
- 变化：两侧均为空集：类数 0、Compose 方法 0、外部调用边 0，指纹同为 4f53cda…，无结构变化。
- 可能影响：表示快照中该家族选择器未匹配到任何类，既不能证明 Kotlin 侧 story 实现不存在（家族选择器可能不覆盖其包名/注解），也不能证明页面功能消失；若模块曾登记 Kotlin 侧 story Hook，其落点在静态证据中不可见。
- 验证：复核 story_kotlin 家族选择规则（包名前缀/注解）是否遗漏宿主 story 包；用 module_source 读 StoryActionIconsFeatureInstaller.kt、StoryPurifyFeatureInstaller.kt 的目标描述符并映射到实际 DEX 类，确认其是否归类到 story_native 而非 kotlin 家族。
- 证据：E009

### mine

mine_native 为 static_invoke_observed：325 类、7 个 Compose 方法、92 条外部调用边（基线 328/7/91），指纹 66c1fa8a… → 75f16dab…，类数减少 3、边数增加 1，属于小幅结构迁移，需先排除混淆改名与 DEX 重排。mine_account_model 更值得注意：类数 132/132、外部调用边 43/43、Compose 方法 0/0 完全一致，指纹仍由 ddcfc5ef… 变为 2b548e1a…，说明变化发生在方法体或边指向层面而非家族规模，可能是混淆重排、工具链差异或模型字段/方法体改写，不能直接判为新样式。两路径 runtime_enabled、module_coverage 均为 unknown/requires_installer_review。模块侧存在 MineComponentFilterFeatureInstaller、MineComponentSnapshot（含 HostBridge/QueryClient/QueryContract/Store）、MineVipFeatureInstaller、HostMineReadingCard 等文件，但本轮未读源码，组件过滤规则与快照键是否仍匹配宿主账户组件结构未知；mine 相关协议（MineMoss/KMineMoss）未登记，跨家族消费者与兜底策略无法从静态证据确认。

证据：E010, E011, E012

#### 路径：mine_native

- 状态：static_invoke_observed
- 变化：类数 325（基线 328，-3）、Compose 方法 7（不变）、外部调用边 92（基线 91，+1），指纹 66c1fa8a… → 75f16dab…；规模微降但边数微增，方向不一致。
- 可能影响：若减少的 3 个类属于“我的”页组件承载类，MineComponentFilterFeatureInstaller 的组件匹配/过滤可能漏项；新增 1 条边也可能引入未归类调用者，改变过滤入口。均为待验证推断。
- 验证：用 family_evidence 重读两侧 mine_native 类清单比对缺失类名与新增边端点；读 MineComponentFilterFeatureInstaller.kt 与 MineComponentSnapshot.kt 的匹配键，核对是否引用已消失类/方法；真机进入“我的”页对比组件快照输出。
- 证据：E010

#### 路径：mine_account_model

- 状态：static_invoke_observed
- 变化：类数 132/132、外部调用边 43/43、Compose 方法 0/0 与基线完全一致，但家族指纹由 ddcfc5ef… 变为 2b548e1a…，变化落在方法体哈希或边指向而非家族规模。
- 可能影响：若为模型字段/方法体改写，MineComponentSnapshotQueryContract/Store 的读取键或序列化契约可能失配；若仅为混淆重排，则模块无影响——当前无足够粒度证据区分。
- 验证：对两侧 mine_account_model 类级 method_bodies_sha256 逐一求交与差集，确认是整体体哈希漂移（混淆/编译器）还是少数类语义改动；再读 MineComponentSnapshotQueryContract.kt / MineComponentSnapshotStore.kt 核对字段名与契约版本号；真机抓快照查询返回校验。
- 证据：E010, E011, E012

### F001：comment_compose 样本内出现个别方法体级改动候选（CardInteractionService 哈希分歧），类数与 compose 方法数未变
事实：目标 9.16.1 相对基线 9.16.0，comment_compose 类数 2444/2446、外部调用边 934/932、compose 方法数两侧均 278（E001/E015）。family_evidence 各取 5 个类样本（E011 目标 / E012 基线）：kntr/common/comment/common/service/b 两侧方法体哈希同为 ed8ead98…，service/h 同为 990bc7a3…，kntr/common/comment/imageviewer/data/c 与 card/action/CardAction 两侧方法体均为空（e3b0c442…）；唯一分歧是 kntr/common/comment/common/service/CardInteractionService 的方法体哈希由 829a5c51… 变为 6e3f9633…，其方法列表仍为 d(LZe1/c;Lkotlin/coroutines/jvm/internal/ContinuationImpl;) 与 getPriority()，签名两侧一致。推断：样本内表现为“单个类的方法体被改写”，而不是整套 Compose 评论重写；但样本上限为 5 个类（共 2444 类），不能外推到其余类，也不能据此判断 Compose 样式变更。可能影响：CommentComposeCopyBridge、CommentComposePurifyBridge、CommentComposeViewAccess、CommentReplyButtonCompose、CommentEmojiAdapter 若以该类的方法体实现（而非签名）为语义依赖，可能出现行为漂移；模块源码本轮未读取（快照 working_tree_dirty=true），这些 Hook 是否以该类为注入点、注入方式是按类名+签名还是按字段/常量，均未知，故不能断言 Hook 仍命中或已失效。
反例与替代解释：可推翻当前推断的证据：(1) JADX 比对 CardInteractionService.d 两侧字节码，若仅指令重排、寄存器分配或调试信息差异而控制流等价，则该分歧属编译器变化而非逻辑改动；(2) 若把样本扩到全部同名类后发现 2442 个类哈希一致，则整体仍可判为重排主导；(3) 若减少的 2 个类经查为匿名类/重复包装层合并，则 −2 类不构成结构变化。反之，若 d 方法的优先级判定或协程竞态处理逻辑改变，则升级为真实调用路径变更。
建议：下一步：用 decompile_class 反编译两侧 kntr/common/comment/common/service/CardInteractionService 并列出其调用者，逐条比对 d 方法的控制流与返回语义；同时用 module_source 读取 CommentComposeCopyBridge、CommentComposePurifyBridge、CommentComposeViewAccess、CommentReplyButtonCompose，登记其目标类名/签名/字段锚点，判断是否与该类相关；最后在 9.16.1 真机打开视频评论区，记录上述安装器的安装返回值（成功/NULL/异常）与命中日志。
证据：E001, E011, E012

### F002：评论四条非 Compose 路径类数完全不变、外部调用边各漂移 1–8 条（legacy_v2 减少 8，native 三族各增 1–2），重排解释需以方法体哈希证伪
事实（目标 9.16.1 / 基线 9.16.0，E001/E015）：comment_legacy_v2 类数 579/579，外部调用边 735/743（目标少 8 条）；comment_native_legacy 172/172、211/209（目标多 2 条）；comment_native_next 45/45、50/49（多 1 条）；comment_native_exp3 58/58、62/61（多 1 条）；四条指纹全部变化。类数严格不变而调用边小幅漂移，是 DEX 重排、内联与包装层合并的常见特征，但两侧样本已给出反例：comment_legacy_v2 的 Lcom/bilibili/app/comm/comment2/comments/viewmodel/message/d; 方法体哈希由 1bec7f2e… 变为 8540eb05… 而方法签名 a(...)CharSequence 与 c(...)V 一致，同族 observable/LazyObservableBoolean$b、LazyObservableField$a、LazyObservableString$b、LazyObservableInt$b 两侧一致（E017/E018），说明至少一处方法体级改动存在，重排不足以解释全部差异。评论共同协议两侧一致（comment_java_moss 50/50；comment_kotlin_moss 130 定义、26 条实际调用边，E001），协议面未见变化，但定义数与边数之比不构成覆盖证明。可能影响：CommentClassicStyleLocator、CommentFilterFeatureInstaller、CommentKotlinPurifier、CommentNativeBindingCatalog 若以类名+签名为锚，样本内签名未见变化；若以调用边拓扑或 viewmodel 消息格式化实现为依赖，则 legacy_v2 的 8 条边减少与 message/d 的方法体改动构成待查点。模块源码未读取，覆盖情况不推断。
反例与替代解释：可推翻当前推断的证据：(1) 对四条路径取完整两侧类样本比对 method_bodies_sha256，若同名类几乎全等而仅边数变动，则回归重排/内联解释；(2) 若把 legacy_v2 减少的 8 条边逐一归属后发现无一边涉及模块登记类，则实际影响可降级；(3) 若 native 三族各新增的 1–2 条边指向 ReplyMoss/KReplyMoss 等未登记协议实现，则属于真实新增跨家族调用，结论升级；(4) 若 message/d 的差异仅来自编译器对同一逻辑的重写（如字符串拼接方式），则仍非语义变更。
建议：下一步：对 comment_legacy_v2 与三个 native 家族取两侧完整类样本（而非 5 类抽样）比对方法体哈希，输出差异类清单；把 legacy_v2 的 8 条消失边与 native 家族的 1–2 条新增边逐一归属到源类/被调方，与模块已登记类名求交集；用 decompile_class 反编译 comments/viewmodel/message/d 两侧确认差异语义；真机在 9.16.1 分别触发旧/新原生评论区并抓取定位器与安装器日志。
证据：E001, E015, E000, E017, E018

### F003：已登记 Moss 协议之外仍有 ReplyMoss/KReplyMoss、DynamicMoss、OpusMoss/KOpusMoss 等未登记协议，Kotlin Moss 多数定义无静态调用边，消费者归属未知
事实：协议统计两侧一致——comment_java_moss 50 定义/50 边、comment_kotlin_moss 130 定义/26 边、dynamic_java_moss 134 定义/134 边、dynamic_kotlin_moss 382 定义/26 边（E001/E002），且两侧数值没有版本间差异。未登记协议列表含 Lcom/bapis/bilibili/main/community/reply/v2/ReplyMoss 与 KReplyMoss、Lcom/bapis/bilibili/app/dynamic/v1/DynamicMoss、v2/OpusMoss 与 KOpusMoss、v2/KTribeeMoss、v2/CampusMoss 等（E000）。推断：java Moss 的定义数与调用边数在两侧相等，但这是计数事实，不能推出“所有调用点均已解析”；Kotlin Moss 大量定义（动态 356 条、评论 104 条）无实际调用边，符合接口分发、反射或跨 DEX 消费不可静态解析的解释，属于未知而非功能缺失。可能影响：若动态页或评论原生链路的真实消费者落在未登记协议（KOpusMoss、KReplyMoss 等），现有协议证据无法证明模块覆盖这些入口，dynamic_opus 的 −5 边与评论 native 家族 ±1–2 边的漂移也就缺少协议面解释；但同样没有证据表明模块依赖这些协议。
反例与替代解释：可推翻或支撑当前推断的证据：(1) 在 dex 中定位 KOpusMoss/KReplyMoss 的实现类并枚举实例化调用者，若存在非接口分发的真实调用边，则 26 边是解析缺口而非缺失；(2) 若模块源码注入点类名与未登记协议实现类无交集，则当前推断成立且需扩展协议登记；(3) 若服务端仅投放已登记协议对应样式，则未登记协议可能不参与本页渲染——但服务端 A/B 在静态侧不可见，无法据此排除。
建议：下一步：用 protocol_evidence 或 decompile_class 对 KOpusMoss、KReplyMoss、OpusMoss 的实现类做调用者枚举，区分接口分发与真实调用边；把结果与 module_source 中 DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller、KotlinDynamicMossWatch、CommentNativeBindingCatalog 引用的类名求交集；将确认的消费者补登为协议候选，并把“定义数/边数”明确标注为计数而非覆盖率。
证据：E000, E001, E002

### F004：home_legacy 短名复用致类名定位假设失效，样本内不能推及全族
事实（E003/E013/E014）：home_legacy 目标侧 767 类 / 87 Compose 方法 / 204 外部调用边，基线 769 / 87 / 211，fingerprint 7a842bb… vs 8772cd6…。可成对比较的样本只有 3 个类：A0 在基线是 WatchLaterFragmentV2 的 DialogInterface.OnClick 回调（字段 WatchLaterFragmentV2、FragmentActivity），在目标侧变为接收 MenuItemBean 的消费者（字段两个 Object）；A 类字段与方法签名逐项一致而 method_bodies_sha256 由 156a32… 变为 9ce5e1…；AccountMineRequestResource 字段前缀一致而方法体哈希由 e50c7b… 变为 0de665…。限制：E013/E014 均为有界摘录（truncated=true，每侧 5 类），且两侧样本集不一致（目标侧含 h0，基线侧无），因此缺失的 2 个类、7 条调用边端点以及其余 764/766 个类的哈希分布均未知，本发现不外推为全族结论。推断：指纹变化至少部分来自混淆短名复用与编译器/R8 产出差异，而非可确认的新首页样式；同时 A0 的语义变化说明“按短类名定位”的假设在 9.16.1 已不可靠。影响：模块侧 HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilterFeatureInstaller 若以短类名+方法签名匹配，可能在目标版本命中错误类或落空；runtime_enabled=unknown、module_coverage=requires_installer_review，Hook 是否真正生效未经任何验证。反例：若 JADX 调用点比对显示 A0 在 9.16.0 中也只被 MenuItemBean 路径使用，则“语义漂移”推断被推翻，应归为纯重排；若真机日志显示定位器按旧短名仍命中并生效，则影响等级应下调。
反例与替代解释：若 smali 调用点比对显示 A0 两版调用点一致，则属纯 DEX 重排；若真机日志显示旧短名仍命中且 Hook 生效，则本次变化无实际影响；若命中为空但安装器存在超类/接口兜底并成功，则降级为鲁棒性改进项；若命中为空且无兜底，则升级为需修复项。
建议：按以下顺序补证：1) 对 home_legacy 做 767 vs 769 类清单级 diff 与边端点 diff，而不是只依赖 5 类摘录；2) 对 Ltv/danmaku/bili/ui/main2/A0 与 A 做两侧完整 JADX 调用点比对，判定是短名重排还是实现迁移；3) 定向读取 HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeComponentFilterFeatureInstaller.kt，登记其匹配锚点（短名/签名/包前缀）与失败兜底分支，并按文件哈希追溯（source_tree_sha256=37745f8f…，working_tree_dirty=true）；4) 在 9.16.1 真机抓取定位器命中/未命中与安装器返回日志，确认是否触发兜底。
证据：E003, E013, E014

### F005：home_new_frame 结构与数量持平但哈希变化，语义待定
事实：home_new_frame 目标与基线均为 196 类、33 个 Compose 方法，external_invoke_edges 48→49，fingerprint 086965… → 4a3e90…；本单元未取得该家族的类级样本，也未读到 HomeFrameListHook/HomeExtraCardPolicy 中针对新框架的解析代码。因此“1 条新增调用边对应何种实现变更”及“新框架是否在 9.16.1 首页启用”均为未知，不能据哈希变化宣称新样式出现或模块适配通过。
反例与替代解释：若类级样本比对显示除新增一条边外方法体哈希全部一致，则本次变化可归为 DEX 重排/常量变化；若样本中出现新方法或新 Compose 签名，则需按新框架样式候选登记；若真机未加载该框架，则本次变化对本路径无运行时意义。
建议：补证顺序：先对 home_new_frame 双侧取类级样本，定位新增调用边的来源类与方法体差异；再在 9.16.1 真机确认该框架是否被首页加载并抓取对应 Hook 是否进入。
证据：E003

### F006：search 双路径静态微动，已登记协议计数不变但模块匹配与兜底未核实
事实（E004）：search_native 两侧类数均为 1702、compose_methods 均为 2、external_invoke_edges 2851→2859，fingerprint bc8afd… → 28a11e…；search_compose 类数 3145→3141、compose_methods 561 两侧一致、调用边 594→595，fingerprint e0ff41… → fcde68…。已登记协议计数两侧一致：search_java_moss 定义 24 / 实际调用边 22，search_kotlin_moss 定义 52 / 实际调用边 18；定义数与实际调用边数是不同单位，不能相除推导覆盖率，且该一致性只覆盖这两个已登记 MOSS 家族，不等于搜索域协议面全部未变。缺口：E004 未提供任何 search 家族类级样本，+8 条边、减少的 4 个类、+1 条边的来源类均为未知；未登记协议清单中仍列有 app/search/v2/SearchMoss、KSearchMoss、broadcast/message/search/SearchMoss 等条目，但消费者未读，不能据此断定搜索页另有并存样式栈。推断：类数与调用边的微动与“R8/DEX 重排或小范围实现调整”相容，也与“局部结构精简”相容，二者静态不可区分。影响：SearchHomeRecommendLocator、SearchHomeRecommendPolicy、SearchDefaultWordsCleaner 的匹配条件本轮未读，搜索首页推荐净化与默认词清理在 9.16.1 是否仍命中、是否存在兜底均为未知；两条路径 runtime_enabled=unknown、module_coverage=requires_installer_review。
反例与替代解释：若类级样本显示减少的 4 个类属推荐卡片容器且方法体差异集中于此，则可能对应真实结构精简而非裁剪；若方法体哈希除新增边外全一致，则归为 DEX 重排；若推荐区块实际走未登记 SearchMoss 消费者，则“已登记协议计数不变”不足以覆盖该路径，应重新登记家族。
建议：补证顺序：1) 对 search_native 与 search_compose 各做两侧类级样本比对，定位 8 条新增边、减少的 4 个类身份与新增 1 条边的端点；2) 读 SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt，登记类名/方法签名锚点、版本条件与失败兜底，并按文件哈希追溯（working_tree_dirty=true）；3) 排查询搜索页是否消费未登记的 app/search/v2/SearchMoss / KSearchMoss / broadcast/message/search/SearchMoss，若有则需重新划分路径；4) 真机 9.16.1 进入搜索页抓 Hook 命中与安装器返回日志，并在平板/宽屏与服务端开关两维度各做一次对照，静态不可见的变体记为未知。
证据：E004

### F007：pgc_theseus 外部调用边 1328→782 而类数与 compose 方法数不变，需区分边解析失效与新样式
事实：9.16.1 相对 9.16.0，pgc_theseus 类数 2265 vs 2264、compose 方法 131 vs 131 均基本不变，但 external_invoke_edges 由 1328 降至 782（-546），结构指纹由 ede5e8c1…变为 4df56dbb…；同期 pgc_player_moss（12 定义 / 3 边）与 pgc_view_moss（14 定义 / 7 边）两侧数字完全一致，共同协议接口面无增减。推断：在类集合与方法计数稳定的前提下，边数骤降通常指向调用边在混淆改名、DEX 重排、方法内联或包装层合并后无法解析到原目标，或接口派发未被解析，而不是 Theseus PGC 样式整体下线；legacy 侧边数反而 +13（386→399），也符合“调用被重新组织”的解释。影响面：PgcAutoActivityPopupFeatureInstaller 依赖 PgcAutoActivityPopupLocator 定位 PGC 页活动弹窗挂点，若这些挂点位于边减少的调用者集合中，静态上会表现为候选点变少；但边减少也可能完全不影响该 Locator（它可能按类名/接口而非调用边定位），当前无法区分。限制：本单元无 pgc_theseus 类级差异明细，runtime_enabled 全部为 unknown，module_coverage=requires_installer_review。
反例与替代解释：若类样本对齐后边减少集中类的方法体哈希与基线一致、且反编译显示同名方法仅换了调用者编号，则属混淆/DEX 重排，应改判为“无实质变化”；若这些类整体消失或方法体被重写为新的弹窗入口，则支持真实调用路径变更；若真机日志显示 PgcAutoActivityPopupLocator 命中且抑制生效，则当前“可能受影响”的推断被推翻；若协议侧出现新增 Moss 定义则需另立新协议消费者检查，但本次两侧协议数字一致，暂不成立。
建议：下一步固定动作：①用 family_evidence 重读 pgc_theseus 两侧，按 method_bodies_sha256 对齐类样本，列出边减少最集中的前若干个调用者；②对其中 1–2 个类用 decompile_class 检查是否被内联/合并或仅改名；③用 module_source 读 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupPolicy.kt，逐条比对定位常量是否仍存在于目标 APK；④真机在 Theseus PGC 页（含平板宽屏与服务端开关两种状态）抓安装器日志确认弹窗 Hook 是否挂上。
证据：E006, E000

### F008：detail 两个 Theseus 家族为类/调用边级微调，风险集中在按类名或签名定位的净化挂点
事实：detail_theseus_ugc 类 1947→1946、compose 方法 25→25、外部调用边 509→510；detail_theseus_united 类 4579→4581、compose 99→99、外部调用边 4312→4257（-55）；两家族结构指纹均变化。detail_java_moss（32 定义/35 条实际边）与 detail_kotlin_moss（76 定义/10 条实际边）两侧数字完全相同，已登记共同协议接口面无新增或删除消费者；定义数与调用边是不同单位，禁止相除推覆盖率，76 定义仅 10 条边说明大量协议成员静态上未解析到调用者。detail_legacy 两侧 classes/compose/edges 均 0、指纹同为 4f53cda1…（空集合固定值），属两侧同态。推断：类集合与 compose 方法计数稳定、调用边小幅波动，优先解释为混淆改名、DEX 重排、包装层合并或接口派发未解析，而不是详情页样式替换；本轮缺少两侧类级 method_bodies_sha256 差集，方法实现是否变化以及 united 55 条边减少的分布均未知。影响：若 DetailModulePurify*/DetailUnitedModulePurify*/DetailUnitedPresentationPurify*/DetailViewPurify*/DetailAppPromotion 的 Installer 或 Policy 按类名/签名/调用边精确定位挂点，理论上存在未命中或误挂风险；是否实际命中本轮未验证（模块源码未读，snapshot working_tree_dirty=true）。旁证（页外，不作结论）：E011/E012 中各限 5 类的 comment_compose 样本显示 Lkntr/common/comment/common/service/CardInteractionService; 的类级 method_bodies_sha256 由 829a5c51…变为 6e3f9633…，而 service/b（ed8ead98…）与 service/h（990bc7a3…）两侧一致；类级哈希是方法体聚合值，不能据此断定具体方法（如 getPriority）是否变化，且该类属评论页家族、不在本单元登记路径，不能外推为评论样式替换。
反例与替代解释：若类级差集显示 ugc/united 的变化类仅限于改名与常量池重排、方法体哈希一致，且真机各 Purify 挂点命中与基线一致，则本项应下调为噪声；若 united 边减少集中的类方法体被重写为新的模块入口或被删除，则支持真实调用路径变更、需按 Hook 未命中处理；若真机日志显示 Detail*Purify Installer 在 9.16.1 全部未命中，则“仅结构微调”的推断被推翻；若 detail_legacy 在真机构成实际页面栈（路由命中 legacy 分支），则两侧 absent 需升级为核心缺口而非长期状态；评论家族一侧 CardInteractionService 类级哈希变化是否为编译器/内联产物，须在 comment 单元以方法级反编译与控制流比对判定，本轮不作结论。
建议：①用 family_evidence 重读 detail_theseus_ugc 与 detail_theseus_united 的 target/baseline 两侧，做类级 method_bodies_sha256 差集，列出变化类并区分改名、常量池重排与实现改动，重点定位 united 边减少集中的调用者；②对其中 1–2 个类用 decompile_class 判定是方法内联、包装层合并还是接口派发未解析；③用 module_source 读取 DetailModulePurifyPolicy.kt、DetailUnitedModulePurifyPolicy.kt、DetailUnitedPresentationPurifyPolicy.kt、DetailViewPurifyPolicy.kt 与 HomeVerticalDetailRouting.kt，逐条比对定位常量在 9.16.1 中是否仍存在并记录未命中时的兜底分支；④用 module_source 或 decompile_class 核实 detail_kotlin_moss 76 定义中 10 条实际边的调用者身份，确认是否存在未登记的跨家族消费者；⑤真机进入 UGC 详情与 united 详情（含平板/宽屏、不同登录态）抓安装器与 Hook 命中日志，核对模块净化、推广位屏蔽与评论区交互项是否仍生效；⑥评论家族的方法级差异交 comment 单元以两侧完整类清单另行复核，不由本次 5 类样本外推。
证据：E005, E000, E011, E012

### F009：player 两路径计数不变/微变而指纹全变：待定位的结构差异候选，不足以判定新播放器样式
事实（E007）：player_java 在 9.16.1 类数 957→958（+1）、外部调用边 3229→3222（-7），指纹 f99b12…→2830ee…；player_kotlin 类数 7、Compose 方法 0、外部调用边 100 三项与基线逐字相同，仅指纹 544b8d…→c20595…。两侧协议 player_java_moss 18 定义/2 条实际调用边、player_kotlin_moss 34/3 完全一致，但定义数与调用边数单位不同，不能相除推覆盖率，调用边也不解析接口分发。跨家族参考（E011/E012，comment_compose）：同名样本中两个类的方法体哈希两侧一致，CardInteractionService 的方法体哈希不同，说明该类指纹会对方法体层面的差异敏感；因此对 player 家族不能仅凭计数不变就断定是重排，必须在 player 自己的类样本上做方法体哈希比对后才能定性。推断：player_kotlin 的“结构三项一致、指纹变”是重排/混淆改名/编译期变化的候选解释，player_java 的 +1 类与 −7 边才是需要定位的实质差异点；两者均为候选，未确认新样式。对模块的可能影响：源码文件清单中存在 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、SponsorPlayerLocator、PlayerCapabilityAccess 等适配层（E000），其命名暗示按名/按签名解析宿主类，但本轮未读取这些文件，锚点条件、失败分支与兜底均为未知，不能断言命中或落空。源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…，E000），后续结论须按文件哈希追溯。调用边存在不证明运行期启用，runtime_enabled 与 module_coverage 仍为 unknown / requires_installer_review。
反例与替代解释：若 player_kotlin 7 个类中存在方法体哈希变化的类，则不能只归因重排，应升级为真实实现变更候选；若 player_java 消失的 7 条边端点恰是模块定位器所锚定的类/方法，则属调用路径真实迁移而非噪声；若新增类为 Kotlin 合成/重复包装类且被删边全为埋点，则本次变化对适配可能无实质影响——但这些都需要类级 diff 才能判断，当前一律为未知。
建议：先用全量家族 diff 找出 player_java 新增的 1 个类与消失的 7 条边的端点类/方法，再用 decompile_class 读该新增类及其调用方，判断是重复包装层、埋点搬迁还是播放器逻辑迁移；对 player_kotlin 逐类比对 7 个类的 full name 与 method_bodies_sha256，若出现方法体哈希变化则升级为真实实现变更候选。随后用 module_source 读取 PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、SponsorPlayerLocator、PlayerCapabilityAccess，登记解析锚点、失败分支与兜底路径，并按文件哈希记录所读版本。真机侧开启模块自检，采集各定位器命中/回落日志与实际命中类名签名；另在宽屏/平板与不同服务端开关账号下各做一次对照，静态不可见的变体记为未知。
证据：E000, E007, E011, E012

### F010：danmaku 无新增家族证据：legacy 两侧 absent、kotlin 结构一致，但净化 Hook 覆盖面与兜底未知
事实：danmaku_legacy 在目标与基线两侧均为 absent（类数 0、Compose 方法 0、外部调用边 0、同一空集指纹 4f53cd…）；danmaku_kotlin 为 static_invoke_observed，57 类/1 个 Compose 方法/8 条外部调用边两侧完全一致，仅指纹 7f0a50…→323c06…（E008）。协议侧 danmaku_java_moss 22 定义/20 条实际调用边，danmaku_kotlin_moss 46 定义/4 条实际调用边，两侧未变；实际调用边不解析接口分发，故只能说本次解析到的边更多落在 Java 侧，不能据此认定 Kotlin 侧没有真实消费者，定义数与边数也不可相除推覆盖率。推断：本版本弹幕页静态侧没有可复核的样式新增或移除证据，danmaku_kotlin 的指纹变化属需逐类方法体比对后才能定性的漂移候选；absent 只表示该家族未被观测到，不等于旧原生弹幕功能消失，也可能是家族登记口径或识别规则未覆盖。对模块的可能影响：源码文件清单中存在 DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy（E000），但本轮未读取其目标类、安装失败分支与兜底逻辑，因此既不能确认净化对 danmaku_kotlin 家族生效，也不能排除只挂某一协议通道而漏掉其他消费者；1 个 Compose 方法的启用条件未读到，服务端开关可能在静态侧不可见，样式候选未穷尽。runtime_enabled 与 module_coverage 仍为 unknown / requires_installer_review。
反例与替代解释：若 DanmakuPurifyFeatureInstaller 的目标类落在 danmaku_kotlin 家族且解析成功，则“覆盖未知”可下调为静态候选命中；若 57 类的全量方法体 diff 出现签名或 body 变化，则 danmaku_kotlin 的指纹变化应升级为真实样式候选；若真机发现净化对某些弹幕场景无效，则应指向未归类调用者或跨家族消费者，而非本家族结构变化。
建议：先读 DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy，按文件哈希登记其解析锚点、家族区分逻辑与安装失败兜底；再对 danmaku_kotlin 57 类做两侧全量方法体哈希与签名集合 diff，判定指纹变化是改名重排还是实现变更。补证 absent 口径：用全量家族清单检索弹幕相关包路径，区分识别规则缺口与实现确不在该家族；枚举 danmaku_java_moss / danmaku_kotlin_moss 的实现类与实例化调用者，识别未归类消费者。真机对含大量弹幕的视频开启/关闭净化，对比实际渲染元素与模块日志中的命中记录，并覆盖宽屏/平板与不同服务端开关账号，记录未覆盖场景。
证据：E000, E008

### F011：story_native 指纹变化伴随类数 -1、调用边 -8、Compose 方法不变：属改名/重排候选，本轮不构成新样式
事实（E009）：9.16.1 story_native 为 2924 类 / 44 Compose 方法 / 1310 外部调用边，基线 2925 / 44 / 1318，家族指纹 b56b7342… 对 7fffa3be…，路径 evidence 仍逐字为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review。变化方向是“减少”，Compose 方法数完全不变，这与“新增一套原生/Compose 样式家族”不符，更像单类裁剪、类迁移或混淆改名引起的边重定向。限制：E009 是每家族有界类抽样，本轮未取得类级全量清单，也未取得 8 条调用边的起止端点，因此“哪些类/边发生变化”本身仍为未知，而不是已定位的差异。推断：若减少的类命中 StoryPurifyFeatureInstaller 或 StoryActionIconsFeatureInstaller 的目标描述符，模块在该版本会静默失去挂点；若无交集则对模块无语义影响——两者当前无法区分。story_kotlin 两侧为同一空集指纹 4f53cda…，说明本次没有 Kotlin 家族提供替代落点，任何 Kotlin 侧登记钩子都只能映射进 story_native。本结论不涉及运行时启用，不宣称适配通过。
反例与替代解释：可推翻当前推断的证据：①按名比对显示两侧同名类方法体哈希全部一致，仅类/边顺序不同，则为 DEX 重排或编译器差异，不构成样式变化；②清单中缺失类与模块 installer 目标类无交集，则本次变化对模块无语义影响；③真机日志显示原有 Hook 全部命中且按钮样式正常，则“潜在挂点丢失”假设不成立；④反向情况，日志显示 installer 返回 NULL 或目标类不存在，则应升级为运行时失效而非仅结构变化。注意“服务端投放的样式差异”和“平板/宽屏分支”在本轮静态证据中不可见，不能据此宣称已穷尽所有样式。
建议：分三步：①用 family_evidence 按名重读 story_native 两侧样本，逐类比对 method_bodies_sha256，凡两侧同名类哈希一致者记为“重排/编译器差异”候选，凡目标侧缺失或哈希分歧者进入清单；②对清单中的类用 decompile_class（JADX CLI）比对两侧方法体，判断是逻辑改动、内联还是匿名类合并，并用 module_source 读 StoryPurifyFeatureInstaller.kt、StoryActionIconsFeatureInstaller.kt、StoryActionIconsPolicy.kt 的目标类/方法描述符与清单求交；③在 9.16.1 真机进入动态页抓 Xposed 安装与命中日志并截图，记录安装器返回值与定位器是否回落。边级差集若确有必要，须先取得家族全量类与边清单，未取得前不得表述为已比对。
证据：E009

### F012：mine_account_model 规模完全一致而指纹变化、mine_native 类数 -3/边数 +1：属体级改动或重排候选，需按类级哈希定位
事实（E010）：mine_account_model 在 9.16.1 与 9.16.0 均为 132 类、43 条外部调用边、0 个 Compose 方法，家族指纹却由 ddcfc5ef… 变为 2b548e1a…；mine_native 由 328/91 变为 325/92（Compose 方法恒为 7），指纹 66c1fa8a… 对 75f16dab…。两侧 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review。相同规模＋不同指纹这一签名通常来自方法体哈希改写、边指向变化或混淆/DEX 重排，而非“新增一套样式”（新增样式应伴随类数或 Compose 方法数上升）；但 E010 为有界类抽样，本轮未能取得全量类级方法体哈希，故“整体漂移”与“少数类语义改动”两种解释都只能列为候选，不能择一。跨家族对照仅为方法学佐证、不是 mine 的直接证据：comment_compose 两侧 2444/2446 类、278 Compose 方法不变而指纹变化，样本中 CardInteractionService 的 d(...) 体哈希 829a5c51… 变为 6e3f9633…（E011/E012）；home_legacy 767/769 类、87 Compose 方法不变而指纹改变（E013/E014）。说明“指纹变≠新样式”在本样本重复出现，但不能据此推断 mine 侧具体变化位置。推断：mine 页风险更可能落在 MineComponentSnapshot 的契约/字段读取与 MineComponentFilter 的组件匹配上，而非页面家族消失；本轮未读这些源码，不能断言 Hook 覆盖。
反例与替代解释：可推翻当前推断的证据：①按名比对显示两侧同名类方法体哈希全部一致、仅类顺序不同，则为 DEX 重排/编译器差异，可排除语义变化；②清单中出现账户模型字段新增或删除，则属真实契约变更而非重排，且应优先排查快照读取失配；③mine_native 缺失的 3 个类正是 MineComponentFilter 引用的组件承载类，则应升级为较高优先级的过滤失效风险；④真机快照查询返回键名与旧契约一致、VIP/阅读卡显示正常，则契约失配与挂点丢失假设均不成立。E011–E014 为 comment/home 家族对照，只支持“指纹变化不等于新样式”的判断方法，不能作为 mine 路径的调用证据；服务端 A/B 变体在静态侧可能不可见，不得据此宣称所有样式已穷尽。
建议：①用 family_evidence 按名重读 mine_account_model 两侧类样本并逐类比对 method_bodies_sha256，凡同名类哈希一致者归为重排/编译器差异候选，分歧或缺失者形成待查清单；②对清单中代表类（如账户请求/响应模型、枚举类）用 decompile_class 比对字段与序列化相关方法，判断是否字段改名/新增；③用 module_source 读 MineComponentSnapshotQueryContract.kt、MineComponentSnapshotStore.kt、MineComponentSnapshotHostBridge.kt、MineComponentFilterFeatureInstaller.kt、MineVipFeatureInstaller.kt，登记快照键、契约版本与过滤匹配条件（按文件哈希追溯，工作树 dirty 不清理）；④真机进入“我的”页导出组件快照，对照 VIP 卡与阅读卡显示，并另做宽屏/服务端开关对照。全量类级哈希未取得前不得声称完成差集。
证据：E010, E011, E012, E013, E014

## 重点项独立复核

同一模型以独立上下文复核；不代表人工审查或真机验收。

### 复核页面：comment
复核后确认：评论区 5 条登记路径在 9.16.1（目标）与 9.16.0（基线）两侧的 evidence 均逐字为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，无任何安装器或真机证据，不能宣称适配通过或样式切换。需纠正草稿的方向标注：以目标/基线计，comment_legacy_v2 类数 579/579 不变、外部调用边 735/743（目标少 8 条，草稿写成“735→743(+8)”方向反了）；comment_native_legacy 172/172、211/209（目标多 2 条，草稿写成 −2）；comment_native_next 45/45、50/49（目标多 1）；comment_native_exp3 58/58、62/61（目标多 1）；comment_compose 2444/2446（−2 类）、934/932（+2 边）、compose 方法两侧均为 278（E001/E015）。五条指纹全部变化但无 compose 方法量级跳变，不能判定出现新评论样式。方法体层：E011/E012 显示 comment_compose 样本中 service/b、service/h 两侧哈希一致，imageviewer/data/c 与 card/action/CardAction 两侧均为空方法体（e3b0c442…），仅 CardInteractionService 分歧（829a5c51…→6e3f9633…），且签名不变；E017/E018 显示 comment_legacy_v2 样本中 observable 系列类两侧一致，仅 comments/viewmodel/message/d 的方法体哈希不同（1bec7f2e…→8540eb05…）而方法签名完全一致——故“纯 DEX 重排”解释已被部分削弱，至少存在两处方法体级改动，但样本仅 5 个类、不能外推到其余 574 类。协议层 comment_java_moss 50/50、comment_kotlin_moss 130 定义/26 边，两侧一致；104 条无静态边符合接口分发/反射不可解析，非功能缺失，但也构不成覆盖证明。未登记协议列表中含 ReplyMoss、KReplyMoss（E000），说明已登记协议未必覆盖评论原生链路全部消费者。模块源码本轮未读（快照 working_tree_dirty=true），CommentClassicStyleLocator、CommentNativeBindingCatalog、CommentComposeCopyBridge 等的命中与兜底仍为未知。
证据：E000, E001, E015, E011, E012, E017, E018

### 复核页面：dynamic
复核后确认：动态页 3 条登记路径两侧 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，静态调用存在不证明路径启用或 Hook 生效。目标/基线对比：dynamic_legacy 类数 3251/3252（−1）、外部调用边 2151/2152（−1）、compose 方法 105/105；dynamic_compose 1136/1136、221/220（+1）、127/127；dynamic_opus 1352/1354（−2）、186/191（−5）、compose 方法 92/92（E002/E016）。三条指纹全部变化，但 compose 方法数与类规模变动均在 ±2 内，最可能为 DEX 重排、混淆改名或包装层增减，不足以判定新增/删除整套动态样式；dynamic_opus 的 −5 边约为其基线的 2.6%，是本页最大收缩点，仍需逐边归属才能判断是内联还是宿主入口调用点迁移到其他家族（如 Kotlin 家族或未登记 Moss 消费者）。协议层 dynamic_java_moss 134/134、dynamic_kotlin_moss 382 定义/26 边，两侧一致；定义数与边数相等只是计数事实，不证明接口分发被完整解析，356 条无静态边的 Kotlin Moss 定义既不能解释为功能消失，也不能视为已覆盖。E000 未登记协议含 app/dynamic/v1/DynamicMoss、dynamic/v2/OpusMoss、KOpusMoss、KTribeeMoss、CampusMoss，故已登记两条协议未必是动态/Opus 家族真实消费者；DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller、DynamicPurifyPolicy、KotlinDynamicMossWatch 的定位锚点与兜底本轮未读源码，Hook 覆盖不可推断。平板/宽屏与服务端 A/B 维度亦无证据，样式候选未穷尽。
证据：E000, E002, E016

### 复核页面：home
本单元 home 的两条登记路径（home_legacy、home_new_frame）在目标 9.16.1(9161100) 与基线 9.16.0(9160200) 两侧的 evidence 值均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E003），逐字沿用，不视为适配通过。home_legacy：目标侧 767 类 / 87 Compose 方法 / 204 外部调用边，基线 769 / 87 / 211，fingerprint 7a842bb… vs 8772cd6…，可见差异集中在类数差 2 与调用边差 7，Compose 方法数持平。E013/E014 提供每侧 5 个类样本（均标记 truncated=true），可成对比较的仅 Ltv/danmaku/bili/ui/main2/A0、A、AccountMineRequestResource 三个类：A0 由 WatchLaterFragmentV2 的 DialogInterface.OnClick 回调（字段 WatchLaterFragmentV2、FragmentActivity）变为接收 MenuItemBean 的消费者（字段两个 Object）；A 字段与签名一致而方法体哈希 156a32…/9ce5e1… 不同；AccountMineRequestResource 字段前缀一致而方法体哈希 e50c7b…/0de665… 不同。两侧样本集本身不一致（目标侧含 h0、基线侧无），因此缺失的 2 个类与 7 条边端点无法从摘录枚举。home_new_frame：两侧均 196 类 / 33 Compose 方法，调用边 48→49，fingerprint 086965… → 4a3e90…，本单元无任何该类家族类级样本，新增 1 条边的来源类与语义未知。模块侧 HomeFrameTabLocator、HomeFrameListHook、HomeComponentFilterFeatureInstaller、HomeTopBarFeatureInstaller、HomeExtraCardPolicy 的匹配条件本轮未读取（源码快照 working_tree_dirty=true，E000），其对 9.16.1 的命中与兜底、以及首页新旧框架哪条在真机启用，均为未知；服务端投放的样式差异在静态侧可能不可见。
证据：E003, E013, E014

### 复核页面：search
search 两条登记路径 search_native、search_compose 两侧 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E004），不视为适配通过。search_native：类数 1702 两侧一致，compose_methods 均为 2，external_invoke_edges 2851→2859（+8），fingerprint bc8afd… → 28a11e…；类集合数量不变降低了“整族替换”的可能性，但把新增样式类并入同一家族的情形静态不可排除。search_compose：类数 3145→3141（−4），compose_methods 561 两侧一致，调用边 594→595（+1），fingerprint e0ff41… → fcde68…。两条已登记协议两侧计数一致：search_java_moss 定义 24 / 实际调用边 22，search_kotlin_moss 定义 52 / 实际调用边 18（定义数与调用边数单位不同，不能相除推导覆盖率，也不等于搜索域协议面全部未变）。E004 未提供任何 search 家族类级样本，因此 +8 边的来源类、减少的 4 个类身份、+1 边语义全部未知；由此既不能确认新样式，也不能确认旧样式消失，absent 未出现但计数微差同样不构成结论。样本的未登记协议清单中仍有 app/search/v2/SearchMoss、KSearchMoss、broadcast/message/search/SearchMoss 等条目，但其消费者本轮未读，不能据此断言搜索页另有一条并存样式栈。模块侧 SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt 未读取，故搜索首页推荐净化与默认词清理在 9.16.1 的匹配点与兜底路径为未知，不得写为无影响。平板/宽屏与服务端 A/B 开关两维度未做对照，若开关只改渲染不改结构，静态矩阵不可见。
证据：E004

### 复核页面：detail
三条登记路径与 E005 逐项一致：detail_legacy 两侧 classes/compose_methods/external_invoke_edges 均为 0、指纹同为 4f53cda1…（空集合固定值），evidence 逐字为 absent，说明两侧都未索引到该家族，属两侧同态而非本次被移除；成因为家族选择规则未覆盖还是实现确实不在该命名空间，尚未确认。detail_theseus_ugc 类 1947→1946、compose 25→25、外部边 509→510；detail_theseus_united 类 4579→4581、compose 99→99、外部边 4312→4257（-55），两家族指纹均变化，但类数与 compose 计数稳定，优先考虑混淆改名/DEX 重排/包装层合并，仅凭汇总数字无法排除局部实现改动。detail_java_moss（32 定义/35 边）与 detail_kotlin_moss（76 定义/10 边）两侧完全相同，已登记共同协议面无增减；定义数与调用边是不同单位，不得相除推覆盖率，76 定义仅 10 条边说明大量协议成员静态上未解析到消费者。所有路径 runtime_enabled=unknown、module_coverage=requires_installer_review；本轮未读模块源码（snapshot working_tree_dirty=true，需按文件哈希追溯），Detail*Purify 与 DetailAppPromotion Installer/Policy 的定位常量命中与兜底均未核实，不能宣称净化或推广屏蔽生效或失效，也不由 76/10 推断 Hook 覆盖。
证据：E000, E005

### 复核页面：pgc
两条登记路径与 E006 一致：pgc_legacy 类 354→354、compose 0、外部边 386→399（+13）；pgc_theseus 类 2264→2265、compose 131→131、外部边 1328→782（-546，约 -41%），两家族指纹均变化，evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review。类规模与 compose 方法数稳定而调用边大幅变动，更可能是混淆改名、DEX 重排、方法内联或接口派发未解析导致边不可见，也可能是真实调用路径收敛，两种解释静态不可区分，因此不能据此判断 PGC 页面样式增减或功能消失；legacy 侧 +13 同理可能只是新增包装层。pgc_player_moss（12 定义/3 边）与 pgc_view_moss（14 定义/7 边）两侧完全一致，共同协议面未变；定义数与边数单位不同，禁止相除推覆盖率。模块侧候选源码仅 PgcAutoActivityPopupFeatureInstaller/PgcAutoActivityPopupPolicy/PgcAutoActivityPopupLocator，其候选类清单、兜底分支、legacy/theseus 双栈切换条件、平板/宽屏与服务端开关条件本轮均未读取，记为未知，不宣称活动弹窗抑制有效或失效。
证据：E000, E006

### 复核页面：player
player 两条路径在 9.16.1(9161100) 与 9.16.0(9160200) 两侧均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review（E007）。player_java：类数 957→958（+1），外部调用边 3229→3222（-7），指纹 f99b12…→2830ee…；player_kotlin：类数 7、Compose 方法 0、外部调用边 100 三项逐字一致，仅指纹 544b8d…→c20595…（E007）。跨家族复核（E011/E012）显示，同类样本中部分同名类方法体哈希两侧一致、个别类不同，说明该类指纹可随方法体层面的差异变化，因此不能把结构哈希变化直接当作新样式，也不能在没有逐类方法体比对前假定 player 家族只是重排。协议侧 player_java_moss 18 定义/2 条实际调用边、player_kotlin_moss 34/3 两侧完全相同；定义数与调用边数单位不同，不可相除推覆盖率，且调用边不解析接口分发。本轮未读取 PlayerSpeedLocator、PlayerBufferLocator、PlayerCapabilityAccess 等模块文件（快照 working_tree_dirty=true，E000），定位器锚点与兜底保持未知；HookEntry、VersionAdapter、KotlinMossChannel 等未映射候选是否消费 player 家族亦未知。结论：本页只有待定位的结构差异候选，无已确认样式变化，不能宣称适配通过。
证据：E000, E007, E011, E012

### 复核页面：danmaku
danmaku_legacy 两侧 evidence 均为 absent，类数、Compose 方法数与外部调用边全为 0，空集指纹 4f53cd… 相同（E008）；这只说明该家族未被观测到，不证明旧原生弹幕实现消失或功能删除，也可能是家族登记口径或识别规则未覆盖。danmaku_kotlin 为 static_invoke_observed：57 类、1 个 Compose 方法、8 条外部调用边在两侧逐字相同，仅指纹由 7f0a50… 变为 323c06…，属需逐类比对方法体后才能定性的指纹漂移候选（E008）。协议侧 danmaku_java_moss 22 定义/20 条实际调用边、danmaku_kotlin_moss 46 定义/4 条实际调用边两侧未变；调用边不解析接口分发，“消费集中在 Java 侧”只是本次解析到的边分布，不能等同于真实消费者集合，定义数与边数也不可相除推覆盖率。净化安装器 DanmakuPurifyFeatureInstaller、DanmakuPurifyPolicy 本轮未读，目标类、失败兜底、是否区分新旧家族均未知；1 个 Compose 方法的启用条件与服务端开关静态不可见。资源变化 changed=1、added=removed=0 不构成本页样式变化证据（E000）。
证据：E000, E008

### 复核页面：story
复核 story 页两条登记路径，数据与 E009 一致：story_native 目标 2924 类 / 44 Compose 方法 / 1310 外部调用边（基线 2925 / 44 / 1318），家族指纹 b56b7342… 对 7fffa3be…，evidence 逐字仍为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review；story_kotlin 两侧 classes=0、compose=0、edges=0、指纹同为 4f53cda…，evidence=absent，空集两侧一致说明该家族在选择器口径下始终未匹配到类，不能读作 Kotlin 侧样式被移除或页面功能消失。story_native 的计数变化以“减少”为主且 Compose 方法数完全不变，属类裁剪/迁移/混淆改名候选，不构成“新增样式家族”；但 E009 为有界类抽样（每类家族仅少量类样本），消失类身份与 8 条调用边端点本轮无法定位，story_native 内部差异性质仍为未知。页内 protocols 为空，unregistered_protocols 里的 StoryMoss、OpusMoss/KOpusMoss 只能作为待查线索，是否存在跨家族消费者、安装器/定位器覆盖与兜底均未验证。本轮未读取 StoryPurifyFeatureInstaller / StoryActionIconsFeatureInstaller 的目标描述符，Hook 点是否仍落在现存 story_native 类上不可推断；服务端开关与平板/宽屏切换差异静态不可见，需真机验证。
证据：E009

### 复核页面：mine
复核 mine 页两条登记路径，数据与 E010 一致：mine_native 目标 325 类 / 7 Compose 方法 / 92 外部调用边（基线 328 / 7 / 91），指纹 75f16dab… 对 66c1fa8a…，类数 -3 而边数 +1，方向不一致；mine_account_model 类数 132/132、调用边 43/43、Compose 方法 0/0 完全一致，指纹却由 ddcfc5ef… 变为 2b548e1a…，差异只能落在方法体哈希或边指向层面。两路径 evidence 均为 static_invoke_observed，runtime_enabled=unknown、module_coverage=requires_installer_review，本页不存在任何通过结论。由于 E010 仅为有界类抽样，“整体体哈希漂移（混淆/编译器/DEX 重排）”与“少数类字段或方法体语义改动导致快照契约失配”两种解释并存，当前证据不能择一；相同规模＋不同指纹的签名本身不足以判为新样式。页内 protocols 为空，MineMoss/KMineMoss 仅出现在 unregistered_protocols，是否存在跨家族消费者、安装器/定位器覆盖与兜底未确认。本轮未读取 MineComponentSnapshot*（HostBridge/QueryClient/QueryContract/Store）、MineComponentFilterFeatureInstaller、MineVipFeatureInstaller、HostMineReadingCard 的匹配键与契约版本，且源码快照 working_tree_dirty=true，过滤/快照链路是否与 9.16.1 账户组件结构对齐仍为未知；真机“我的”页组件快照导出、VIP/阅读卡显示以及宽屏/服务端 A/B 差异均待实测。
证据：E010

- F001 / revised：事实部分与 E001/E015/E011/E012 一致：comment_compose 目标 2444 类/934 边、基线 2446 类/932 边，compose 方法两侧 278；样本 5 类中仅 CardInteractionService 的方法体哈希由 829a5c51… 变为 6e3f9633…，且 d 与 getPriority 签名不变，其余 4 类两侧一致或均为空方法体。缺陷是草稿据“签名不变”推断“现有按签名注入的 Hook 仍有静态锚点”，但本单元从未读取模块源码，无法得知 CommentComposeCopyBridge/PurifyBridge/ReplyButtonCompose 是否以该类的 d 方法为注入点，属于未读源码的 Hook 覆盖推测，需删除该推定并标注 module_source 未读；样本仅 5/2444 类，结论须限定为样本内观察。（E001, E011, E012）
- F002 / revised：核心判断（类数不变、调用边小幅漂移、优先按重排/内联解释并需方法体哈希证伪）成立，但草稿的漂移方向全部标反：以目标/基线计，comment_legacy_v2 为 735/743（目标少 8 条，而非“735→743 +8”），comment_native_legacy 211/209（目标多 2，而非 −2），comment_native_next 50/49（多 1），comment_native_exp3 62/61（多 1）（E001/E015）。方向反转会误导定位方向，必须修订。另外复核新取的两侧样本（E017/E018）显示 comment_legacy_v2 中 comments/viewmodel/message/d 的方法体哈希两侧不同（1bec7f2e…→8540eb05…）且签名一致，“纯重排”假设已被削弱，应在文中列为已知反例而不仅作为替代解释。（E001, E015, E000, E017, E018）
- F003 / revised：未登记协议清单与 Kotlin Moss 定义/边计数与证据一致（E000/E001/E002），但草稿把“java Moss 定义数与调用边数 1:1”写成“说明其调用点在本次静态图内可完整解析”，这是以计数相等替代解析完备性的过度推断；同样“非接口分发调用边即采样缺口”的替代解释也应标注为待验证而非已定。需保留事实、削弱结论，并明确列表/计数本身不含服务端投放信息。（E000, E001, E002）
- F004 / revised：E003/E013/E014 支持核心事实：home_legacy 767 类/204 边 vs 基线 769/211、Compose 方法同为 87、指纹变化；A0 短名在两侧承载完全不同语义（DialogInterface.OnClick 回调 → MenuItemBean 消费者），A 与 AccountMineRequestResource 签名/字段一致而方法体哈希不同。但草稿未说明两处限制：E013/E014 为有界摘录（truncated=true，每侧 5 类）且两侧样本集不同（目标侧含 h0、基线无），故“类数差 2 来自裁剪/合并”与“7 条边差异”都只是推断，不能由样本枚举；“混淆短名复用导致语义漂移”也只对已比较的 3 个类成立，不能外推到整套 767 类。据此修订分析以显式标注抽样边界，并调整结论措辞与补证顺序；level 保持 candidate（无真机与安装器证据）。（E003, E013, E014）
- F005 / retained：E003 支持全部事实：home_new_frame 两侧 196 类 / 33 Compose 方法，调用边 48→49，fingerprint 086965… → 4a3e90…。草稿结论严格限于“结构数量持平、1 条新增边与哈希变化的语义未知”，没有把哈希变化判为新样式，也没有宣称适配通过，符合证据边界；同时明确未取得该类家族类级样本、未读 HomeFrameListHook/HomeExtraCardPolicy，属如实的缺口声明而非推测。level=needs_runtime 可接受：静态侧已无更多在用证据，新框架是否被首页加载只能靠真机确认；但补证应先做静态类级抽样再上真机。（E003）
- F006 / revised：E004 支持全部数值：search_native 1702 类/2 Compose 方法/边 2851→2859，search_compose 3145→3141/561/594→595，两侧指纹变化；search_java_moss 24 定义 22 边、search_kotlin_moss 52 定义 18 边两侧一致。但草稿两处措辞需要收紧：标题“协议面稳定”超出证据，计数不变只覆盖两个已登记 MOSS 家族，注册表外仍有含 SearchMoss 的未登记协议；“类数微动更可能是 R8 合并/重排”与“局部结构精简”在静态上不可区分，应并列。据此修订标题与分析，level 保持 candidate（无类级样本、无真机、无安装器证据）。（E004）
- F007 / retained：数字与 E006 完全相符：pgc_theseus 类 2264→2265、compose 131→131 基本不变而外部调用边 1328→782（-546，约 -41%），legacy 侧 386→399（+13），pgc_player_moss（12/3）与 pgc_view_moss（14/7）两侧一致。草稿把“边骤降”明确列为边不可解析（混淆改名/内联/包装层合并/接口派发未解析）与真实调用路径收敛两种并列解释，未把低计数或指纹变化直接判为新样式或失效，也说明了 PgcAutoActivityPopupLocator 可能按类名/接口而非调用边定位这一反例；next_steps 覆盖两侧类级方法体哈希对齐、decompile_class 抽验与 module_source 核对定位常量，并保留 runtime_enabled=unknown、requires_installer_review 的限制。level 取 candidate 与仅静态汇总证据相符，无需修改。（E006, E000）
- F008 / revised：detail 侧核心事实经 E005 复核成立（ugc 1947→1946、compose 25→25、边 509→510；united 4579→4581、compose 99→99、边 4312→4257；两指纹变化；detail_java_moss 32/35 与 detail_kotlin_moss 76/10 两侧相同；detail_legacy 两侧 0/0/0 且指纹同为 4f53cda1…）。但草稿对评论家族样本的引用存在哈希误标：ed8ead98… 是 Lkntr/common/comment/common/service/b; 的类级哈希且两侧一致，CardInteractionService 的类级 method_bodies_sha256 实为 829a5c51…（基线）→6e3f9633…（目标）；E011/E012 只给类级聚合哈希（各限 5 类样本），无法支持“getPriority 等方法体哈希未变”的方法级断言；且 comment_compose 属评论页家族、不在本单元登记路径内，样本不可外推。故按补丁修正哈希归属、把评论部分降级为页外旁证并明确类级/方法级区分，detail 结论与 candidate 级别保持不变。（E005, E000, E011, E012）
- F009 / revised：核心事实经 E007 重新取证成立：player_java 957→958 类、3229→3222 边、指纹变化；player_kotlin 7 类/0 Compose 方法/100 边逐字一致仅指纹变。但草稿用 comment_compose（E011/E012）外推“指纹对结构性不敏感”，属跨家族类比，不能移到 player 家族；同时“各 Locator 均按名或按签名解析”是对未读源码的断言（快照 working_tree_dirty=true，E000），必须降级。修订保留候选级别与待定位项，删除确定化表述。（E000, E007, E011, E012）
- F010 / revised：absent 口径、两侧计数一致与指纹变化均有 E008 重新取证支持，needs_runtime 定级恰当；但“共同协议的消费集中在 Java 侧”由 actual_invoke_edges 推出，未解析接口分发，属过度外推，需改为“解析到的调用边分布”；同时补明 Compose 方法启用条件与服务端开关静态不可见。（E000, E008）
- F011 / revised：计数事实与 E009 完全一致（2924/44/1310 对 2925/44/1318，指纹 b56b7342… 对 7fffa3be…，evidence 仍为 static_invoke_observed），结论“先排除改名/重排、不构成新样式”成立，level=candidate 合适。但草稿的验证方案声称“以 family_evidence 重读两侧完整 method_bodies_sha256 清单，列出消失类与 8 条边的起止端点”，超出该证据的实际能力（E009 limits 标注为每家族有界类抽样，边级清单不在预取之中），若不修正会把不可执行步骤写成待办且可能被误读为已有全量差集。故修订 analysis/recommendation/alternatives，明确抽样限制与替代取证路径，标题与 level 调整表述方式，finding 归属页与 evidence_ids 不变。（E009）
- F012 / revised：核心事实与 E010 一致（mine_account_model 132/132、43/43、0/0 但指纹 ddcfc5ef…→2b548e1a…；mine_native 328/91→325/92 而 Compose 仍为 7），E011–E014 引用数据本身准确，且草稿已在 alternatives 中声明它们是方法学对照、不构成 mine/story 直接证据，因此引用不构成伪造。需修订之处：草稿把“对 mine_account_model 做类级 method_bodies_sha256 交集/差集”写成可直接执行步骤，但 E010 仅有有界类抽样，无法据此判定“整体漂移”还是“少数类语义改动”；且把 comment/home 家族对照放在 analysis 主体易被误读为 mine 的直接证据。故修订 analysis/recommendation/alternatives 以明确抽样限制与跨家族证据的类比地位，level 维持 candidate，finding 归属与 evidence_ids 不变。（E010, E011, E012, E013, E014）

### 尚未解决的证据缺口

- [1] 草稿 comment 页 5 条 path_reviews 的调用边方向标注与目标/基线数值相反（legacy_v2 实为 735/743 即目标少 8、native_legacy 211/209、native_next 50/49、native_exp3 62/61），复核已在校验记录中纠正，但 path_reviews 条目本身无法通过补丁修改，发布前需按正确方向重写。
[2] 草稿 overview 含未分配页面内容（home_legacy、home_new_frame、search_native、search_compose 段落，涉及 E013/E014）且以“search_ja”截断，属于跨单元串稿，overview 不在本单元可修订范围，需由汇总方删除该段并补全截断句。
[3] CardInteractionService.d 两侧未做 JADX 字节码比对，方法体哈希分歧属逻辑改动还是编译器重排仍未知；compare 结果需附偏差清单。
- [4] comment_legacy_v2 的 Lcom/bilibili/app/comm/comment2/comments/viewmodel/message/d; 方法体哈希两侧不同（1bec7f2e…→8540eb05…）而签名一致，其语义差异未确认，也未判断是否被模块任意 Hook 引用。
[5] 四条 comment 非 Compose 路径的完整类清单 diff（而非 5 类抽样）与 8 条消失/1–2 条新增调用边的端点归属均未产出，抽样不可外推。
[6] dynamic_opus 186/191 减少的 5 条调用边端点、以及三类 dynamic 家族减少的 1–2 个类的身份均未定位，是否与 DynamicPurifyPolicy/KotlinDynamicMossWatch 依赖类有交集未知。
- [7] KOpusMoss、OpusMoss、DynamicMoss、ReplyMoss、KReplyMoss 的实现类与实例化调用者未枚举，Kotlin Moss 无静态边的定义属接口分发、反射还是未使用无法区分。
[8] 模块源码（CommentClassicStyleLocator、CommentNativeBindingCatalog、CommentComposeViewAccess、CommentComposeCopyBridge/PurifyBridge、CommentReplyButtonCompose、CommentEmojiAdapter、DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller、DynamicPurifyPolicy）本轮未读取，仅凭类名推断覆盖不可行；source_tree_sha256=37745f8f…、repository_head=5422fad1…、working_tree_dirty=true，需按文件哈希追溯登记。
[9] 全部 8 条路径 runtime_enabled=unknown、module_coverage=requires_installer_review；缺 9.16.1 真机安装器返回值与定位器命中/兜底日志，静态调用存在不证明路径启用或 Hook 生效。
- [10] 评论旧/新原生（legacy/next/exp3）与 Compose 家族的切换条件、服务端开关投放规则未知；服务端 A/B 无结构变化在静态侧不可见，不能宣称样式候选已穷尽。
[11] 未验证平板/宽屏与登录态差异下 comment 与 dynamic 家族选择是否不同，多路径并存栈的切换条件尚无证据。
[12] unmapped_multi_path_candidates（HookEntry、VersionAdapter、KotlinMossChannel、KotlinMossReplyBridge、HostAgentWindow 等）是否消费 comment/dynamic 家族未核查，可能构成未归类调用者。
- [13] 本单元未执行任何字节码级方法语义读取（无 decompile_class/module_source 证据），结论级别仅到 candidate/needs_runtime，不能表述为适配结果或回归确认。
[14] home_legacy 767 vs 769 的类清单级 diff 与 204 vs 211 边端点 diff 未做；E013/E014 仅为每侧 5 类截断摘录且两侧样本集不同，缺失类身份与全族方法体哈希分布未知
[15] home_new_frame 无任何类级样本：48→49 新增调用边的来源类、方法体差异性质未知，该框架是否在 9.16.1 首页被实际加载亦未知
- [16] 模块侧 home 定位与兜底未读：HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeComponentFilterFeatureInstaller.kt、HomeTopBarFeatureInstaller.kt、HomeExtraCardPolicy.kt、HomeRecommendPurifyFeatureInstaller.kt 的匹配锚点（短名/签名/包前缀）与失败分支未核对，不能推断 9.16.1 命中情况
[17] 模块侧 search 定位与兜底未读：SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt、SearchPurifyFeatureInstaller.kt 未读取，搜索首页推荐净化与默认词清理在 9.16.1 是否命中、有无备用路径未知
[18] search_native 的 +8 条调用边与 search_compose 的 −4 类 / +1 条边来源类未定位；两条 search 路径均无类级样本，样式候选是新增、裁剪还是重排静态不可区分
- [19] 未登记协议中的 app/search/v2/SearchMoss、KSearchMoss、broadcast/message/search/SearchMoss 等在搜索页是否存在实际消费者未核实；若存在，当前 search 路径划分不完整（未归类调用者）
[20] home/search 四条路径的 runtime_enabled 全为 unknown、module_coverage 全为 requires_installer_review：缺少真机进入首页与搜索页时的定位器命中/未命中、安装器返回值与 Hook 进入日志
[21] 平板/宽屏与登录态、服务端 A/B 开关维度未做对照；服务端投放的视觉变体若无结构变化，静态矩阵不可见，不能宣称样式已穷尽
- [22] source_snapshot 为 published_unverified_worktree、working_tree_dirty=true（source_tree_sha256=37745f8f…，head 5422fad1…）：本轮未读取模块源码，若要引用须按文件哈希追溯具体版本，且不得据此清理工作树
[23] unmapped_multi_path_candidates 中的 HookEntry、VersionAdapter、KotlinMossChannel、HostAgentWindow 等是否消费 home/search 家族类，未评估，属潜在未归类调用者
[24] detail_theseus_ugc/united 缺少两侧类级 method_bodies_sha256 差集，方法实现是否变化、united 55 条边减少（4312→4257）集中在哪些调用者类均未知；需 family_evidence 两侧重读比对。
- [25] pgc_theseus 调用边 1328→782（-546）的成因（混淆改名/DEX 重排/内联/包装层合并 vs 真实路径收敛）未区分，需对边减少集中的类做 decompile_class 抽验。
[26] 模块源码未读：PgcAutoActivityPopupLocator/PgcAutoActivityPopupPolicy、DetailModulePurifyPolicy/DetailUnitedModulePurifyPolicy/DetailUnitedPresentationPurifyPolicy/DetailViewPurifyPolicy、HomeVerticalDetailRouting/HomeVerticalDetailFeatureInstaller 的定位常量、版本条件与兜底分支均未核实；source_snapshot working_tree_dirty=true（source_tree_sha256 37745f8f…），后续须按文件哈希追溯。
[27] detail 与 pgc 全部登记路径 runtime_enabled=unknown、module_coverage=requires_installer_review；Installer 返回值、定位器命中/兜底、真机样式启用均未验证，不能宣称适配通过。
- [28] detail_legacy 两侧 absent 的成因未确认（家族选择规则未覆盖该命名空间 vs 实现确实不存在）；需用全量家族清单检索 legacy 详情类路径并核对路由分支。
[29] detail_kotlin_moss 76 定义仅 10 条实际边的调用者身份与跨家族消费者未解析（含 ReplyMoss/KReplyMoss 等未登记协议在详情页的消费者），不得由定义/边数相除推覆盖率。
[30] 平板/宽屏与服务端 A/B 开关维度未做对照；服务端下发且无结构变化的样式差异在静态侧不可见，样式候选未被证明穷尽。
- [31] 草稿 F008 曾把 Lkntr/common/comment/common/service/b; 的类级哈希 ed8ead98… 误标为 CardInteractionService 目标哈希；已在修订中更正为 829a5c51…→6e3f9633…，评论家族的方法级差异仍需在 comment 单元复核。
[32] 草稿 overview 混入 comment、dynamic、home、search、player、story、mine 等其他页正文与本单元无关，全量合并时需按页拆分校正，避免跨页结论互串。
[33] player_java 新增的 1 个类与减少的 7 条外部调用边的端点类/方法尚未定位，无法区分重复包装层、埋点搬迁还是真实逻辑迁移（E007）。
- [34] player_kotlin 7 个类的 full name 与 method_bodies_sha256 未逐类比对，指纹 544b8d…→c20595… 是重排/改名还是实现变更仍未知（E007）。
[35] PlayerSpeedLocator、PlayerSpeedSessionLocator、PlayerBufferLocator、SponsorPlayerLocator、PlayerCapabilityAccess 未读取，解析锚点、失败分支与兜底路径均无证据；源码快照 working_tree_dirty=true，需按文件哈希追溯（E000）。
[36] DanmakuPurifyFeatureInstaller 与 DanmakuPurifyPolicy 未读取，净化 Hook 的目标类、家族区分与安装失败处理未知（E000）。
- [37] danmaku_legacy 两侧 absent 的判定口径未澄清：无法区分识别规则/家族登记缺口与实现确不在该家族（E008）。
[38] danmaku_kotlin 57 类未做逐类方法体哈希 diff，指纹变化仅为漂移候选（E008）。
[39] danmaku 家族中 1 个 Compose 方法的启用条件与服务端开关未读到，静态侧无法确认其是否投放。
- [40] HookEntry、VersionAdapter、KotlinMossChannel、KotlinMossReplyBridge 等 unmapped_multi_path_candidates 是否消费 player/danmaku 家族未核实，属未归类调用者（E000）。
[41] 两条路径的 runtime_enabled 与 module_coverage 仍为 unknown / requires_installer_review，所有结论均未获真机与安装器验证；宽屏/平板与服务端 A/B 变体未做对照。
[42] story_native 消失的 1 个类与 8 条外部调用边的端点未定位：E009 为有界类抽样，未提供类级全量清单与边级枚举，需按名重读完整证据或另行导出后再做差集。
- [43] StoryPurifyFeatureInstaller / StoryActionIconsFeatureInstaller / StoryActionIconsPolicy / StoryPurifyFeatureInstaller 的目标类与方法描述符本轮未读取（源码快照 working_tree_dirty=true，head 5422fad1），Hook 点是否仍命中 9.16.1 现存 story_native 类未知。
[44] story_kotlin 家族两侧 classes=0 的选择器口径（包名前缀/注解/superclass 规则）未复核，无法区分“该家族选择器不覆盖宿主 story 包”与“Kotlin 侧实现确实不存在”；同时 HomeVerticalDetailFeatureInstaller/Routing 是否归入 story 家族未核对。
[45] mine_account_model 132/132、43/43 不变而指纹变化的原因未定位：无全量类级 method_bodies_sha256，无法区分混淆/DEX 重排与少数类字段或方法体语义改动。
- [46] mine_native 减少的 3 个类与新增的 1 条调用边端点未识别，是否属于账户组件承载类或未归类调用者未知。
[47] MineComponentSnapshot 契约链路（QueryContract / QueryClient / Store / HostBridge）、MineComponentFilterFeatureInstaller 的匹配键、MineVipFeatureInstaller 与 HostMineReadingCard 的版本条件均未读源码，组件过滤与快照键是否失配未知。
[48] story 与 mine 页均无已登记协议（protocols 为空）；StoryMoss、MineMoss / KMineMoss、OpusMoss / KOpusMoss 等仅出现在 unregistered_protocols，其实现类、实例化调用者、是否存在跨家族消费者与兜底路径均未枚举。
- [49] 两页所有路径 runtime_enabled 均为 unknown、module_coverage 均为 requires_installer_review：未取得安装器返回值（安装成功/NULL/异常）、定位器命中或回落日志，任何“Hook 生效/失效”判断都缺证据。
[50] 服务端 A/B 投放与平板/宽屏分支造成的样式差异在静态侧可能不可见，本轮未做真机对照，不能宣称已穷尽 story/mine 的并存样式。
[51] tiny 计数差（如 story_native -1 类/-8 边、mine_native -3 类/+1 边）可能来自匿名类或重复包装层合并、DEX 重排，本轮无 JADX 类级反编译对照，尚不能排除工具链/混淆造成的伪差异。

## 下一步

- [1] JADX CLI 反编译 9.16.1 与 9.16.0 的 kntr/common/comment/common/service/CardInteractionService，逐方法比对 d(LZe1/c;Lkotlin/coroutines/jvm/internal/ContinuationImpl;) 的控制流与返回语义，判断是逻辑改动还是编译器/寄存器重排。
[2] 对 comment_legacy_v2、comment_native_legacy、comment_native_next、comment_native_exp3 取两侧类样本比对 method_bodies_sha256，并将 735→743 的新增 8 条边逐一归属到源类，确认是否指向未登记协议实现。
[3] 定位 comment_compose 减少的 2 个类与 dynamic_opus 减少的 2 个类的具体类名，判断是否为匿名类/重复包装层合并（重排解释）还是承载绑定逻辑的类被移除。
[4] 对 dynamic_opus 的 191→186 收缩列出被删除的 5 条调用边，核对是否与 KotlinDynamicMossWatch、DynamicPurifyPolicy、DynamicTabsFeatureInstaller 引用的类名存在交集。
[5] 枚举 ReplyMoss/KReplyMoss、DynamicMoss、OpusMoss/KOpusMoss 的实现类及其实例化调用者，区分接口分发与真实调用边，并登记为协议消费者候选。
- [6] 核对 modules 源码中 CommentClassicStyleLocator、CommentNativeBindingCatalog、CommentComposeViewAccess、DynamicPurifyFeatureInstaller、DynamicTabsFeatureInstaller 的定位条件（类名/签名/包前缀），逐条与 9.16.1 静态矩阵中的实际类名对齐，记录未命中项。
[7] 因源码快照 working_tree_dirty=true（source_tree_sha256 37745f8f…），按文件哈希追溯读取的模块源码版本，不清理工作树，并在报告中标注所引用文件的哈希。
[8] 真机（9.16.1 vc9161100）分场景验证：旧原生评论区、新原生评论区（legacy/next/exp3）、Compose 评论区、动态页 legacy/Compose/Opus 条目，各抓取安装器与 Hook 命中日志，标注样式是服务端投放还是本地结构决定。
[9] 对每个家族记录安装器返回值（安装成功/NULL/异常）与定位器兜底是否触发，补齐 module_coverage 从 requires_installer_review 到已核实的证据。
[10] 在宽屏/平板与服务端 A/B 开关两个维度各做一次对照，确认是否存在静态不可见的样式差异，并在报告中保留“样式候选未穷尽”的限制说明。
- [11] 对 home_legacy 的 Ltv/danmaku/bili/ui/main2/A0 与 A 在 9.16.0/9.16.1 做完整 JADX 调用点比对，判定是短名重排还是实现迁移
[12] 定向读取 HomeFrameTabLocator.kt、HomeFrameListHook.kt、HomeComponentFilterFeatureInstaller.kt，登记其类名/方法签名匹配条件与兜底分支
[13] 对 home_new_frame 双侧取类级样本，定位 48→49 新增调用边来源类与方法体哈希差异
[14] 在 9.16.1 真机分别进入首页与搜索页，抓取定位器命中/未命中及 Hook 进入日志，记录实际启用路径
[15] 对 search_compose 双侧做类级样本比对，确认 3145→3141 减少的 4 个类身份及 594→595 新增边来源
- [16] 读取 SearchHomeRecommendLocator.kt、SearchHomeRecommendPolicy.kt、SearchDefaultWordsCleaner.kt，核对搜索首页推荐与默认词清理的匹配点与兜底
[17] 检查未登记的 app/search/v2/SearchMoss、KSearchMoss 及 broadcast/message/search/SearchMoss 在 9.16.1 是否存在搜索页消费者
[18] 在 source_files working_tree_dirty=true 前提下按文件哈希追溯 SearchHomeRecommend 与 HomeFrame 相关文件版本，不用清理工作树
[19] 对 home_legacy 767/769 的类数差 2 与调用边差 7 做类清单级 diff，排除裁剪/合并与真机功能删除的区别
[20] 真机验证平板/宽屏与登录态差异下首页新旧框架、搜索双路径的切换条件是否触发不同家族
- [21] 用 family_evidence 重读 detail_theseus_ugc / detail_theseus_united / pgc_theseus 的 target 与 baseline 两侧类样本，按 method_bodies_sha256 对齐，输出方法体哈希变化的类清单（区分改名与实现变更）。
[22] 对 pgc_theseus 边减少最集中的 1–2 个类调用 decompile_class，判定是否方法内联/包装层合并/接口派发未解析。
[23] 用 module_source 读取 PgcAutoActivityPopupLocator.kt、PgcAutoActivityPopupPolicy.kt、DetailUnitedModulePurifyPolicy.kt、DetailViewPurifyPolicy.kt，逐条核对定位常量在 9.16.1 是否仍存在，并记录未命中时的兜底分支。
[24] 核实 HomeVerticalDetailRouting.kt 与 HomeVerticalDetailFeatureInstaller.kt 的版本/路由条件，确认 detail_legacy absent 是长期未使用还是回归。
[25] 用 module_source 或 decompile_class 复核 detail_kotlin_moss 76 定义中仅 10 条实际边的调用者身份，确认是否存在未登记的跨家族消费者（本单元未登记 detail 的 comment_compose 归属，需在下一次审计单元补登）。
- [26] 真机验证：UGC 详情、united 详情、legacy PGC、Theseus PGC 各页（含平板/宽屏）分别抓 Hook 安装日志与页面模块清单，确认 runtime_enabled 与 Installer 命中情况。
[27] 在有服务端开关的账号上重复 PGC 与详情页验证，记录开关前后是否出现结构性差异；静态不可见的 A/B 变体记为未知，不宣称穷尽。
[28] 按 source_tree_sha256=37745f8f…（working_tree_dirty=true）登记本次引用源码的文件哈希，后续复核以文件哈希追溯，不清理工作树。
[29] 对 player_java 做 9.16.0↔9.16.1 全量类清单与调用边 diff，定位新增的 1 个类与消失的 7 条边的端点类/方法
[30] 对 player_kotlin 的 7 个类逐类比对 full name 与方法体哈希，区分改名重排与真实实现变更
- [31] 读 PlayerSpeedLocator／PlayerSpeedSessionLocator／PlayerBufferLocator／SponsorPlayerLocator／PlayerCapabilityAccess 源码，登记解析锚点、失败分支与兜底路径
[32] 读 DanmakuPurifyFeatureInstaller／DanmakuPurifyPolicy，确认净化 Hook 的目标类、家族区分逻辑与安装失败处理
[33] 澄清 danmaku_legacy 两侧 absent 的判定口径：用全量家族清单检索弹幕相关包路径，区分识别规则缺口与实现缺失
[34] 在真机开启模块自检，采集 player 各定位器命中/回落日志，记录命中类名与方法签名
[35] 在真机对同一视频开启/关闭弹幕净化，对比实际渲染弹幕元素与模块日志，验证 Hook 命中与漏挂场景
- [36] 核查 HookEntry／VersionAdapter／KotlinMossChannel／KotlinMossReplyBridge 等 unmapped_multi_path_candidates 是否消费 player/danmaku 家族，补登为未归类调用者
[37] 复核 source_dirty=true 的冻结工作树中相关文件哈希，确保模块侧结论按文件哈希追溯而非按工作树状态推断
[38] 确认 1 个 danmaku Compose 方法的运行开关与启用条件（服务端开关可能在静态侧不可见）
[39] 用 family_evidence 重读 story_native 两侧完整类级 method_bodies_sha256 清单，产出消失类与 8 条边端点的差集。
[40] 读 module_source: StoryPurifyFeatureInstaller.kt / StoryActionIconsFeatureInstaller.kt，列出目标类描述符并与 story_native 差集比对。
- [41] 读 module_source: HomeVerticalDetailFeatureInstaller.kt / HomeVerticalDetailRouting.kt，确认其路由目标是否归入 story 家族。
[42] 复核 story_kotlin 家族选择器（包名前缀/注解），确认 total_classes=0 是否因选择规则遗漏而非实现不存在。
[43] 对 mine_account_model 做两侧类级 method_bodies_sha256 交集/差集，判定整体漂移还是局部语义改动。
[44] 用 family_evidence 定位 mine_native 缺失的 3 个类与新增 1 条边的端点。
[45] 读 module_source: MineComponentSnapshotQueryContract.kt / MineComponentSnapshotStore.kt / MineComponentSnapshotHostBridge.kt，核对快照键与契约版本。
- [46] 读 module_source: MineComponentFilterFeatureInstaller.kt / MineVipFeatureInstaller.kt，核对其匹配键是否引用已消失类或方法。
[47] 真机验证：进入动态页抓 Xposed 日志与界面截图，确认 story 相关 Hook 命中与样式生效（运行时状态目前 unknown）。
[48] 真机验证：进入“我的”页导出组件快照，对比 VIP 卡与阅读卡显示，确认 mine 侧过滤/快照链路。
[49] 按文件哈希追溯 source_snapshot（working_tree_dirty=true，head 5422fad1）中上述 installer 的改动，不清理工作树。
[50] 核对未登记协议 StoryMoss / MineMoss / KMineMoss / OpusMoss 的共同协议消费者与兜底路径，确认是否存在未归类调用者。