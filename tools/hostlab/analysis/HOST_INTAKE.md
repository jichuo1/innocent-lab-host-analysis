# 宿主升版接入清单

接到新的官方 `tv.danmaku.bili` APK 时按本文执行。目标不是「把 APK 反编译一遍」，而是用固定步骤判断：

1. 现有定位规则还能不能命中；
2. 要不要改候选表 / DexKit / JSON；
3. 要不要加 `ADAPTER_RULE_VERSION` 或 `SCHEMA_VERSION`；
4. 哪些域静态 FOUND 仍必须进真机。

工具与产物都在本目录，已被仓库根 `.gitignore` 的 `Temp/` 排除。可复用结论必须回填 `docs/development_experience.md`，不要把 TSV 或反编译当唯一档案。

当前 Adapter 版本（动手前从源码复核，不要抄旧条目）：

- `SCHEMA_VERSION`（JSON 字段形状）= `VersionAdapter.kt` 的 `sv`
- `ADAPTER_RULE_VERSION`（定位规则）= 同文件的 `rule`，并写入宿主指纹

2026-09-04 历史快照：`sv=48`，`rule=42`。2026-09-05 的 9.11.0 接入复核为
`sv=53`、`rule=48`；本轮只改候选顺序，schema 沿用 PGC 活动半屏接入后的 53。

---

## 0. 这次失败过的模式（先读，再跑）

这些已经在真机或离线审计上付出过学费，清单就是为了不再用聊天记录拼步骤。

| 失败 | 证据 | 清单里对应哪一步 |
| --- | --- | --- |
| 按混淆单字母写死候选 → 静默不装 | 脉络 mapper：9.6.0 / 9.10.0 漂到 `...v1.b`；相关游戏组件 8 个本地宿主全程未安装 | §2 字母表漂移；禁止再往运行时名单里加短名 |
| 离线审计域不全 → 「26 域全部 FOUND」被误读 | 09-02 的 9.10 审计不含 `comment_topology` / `home_vertical_detail` / `mine_account_mine` / `detail_app_promotion` 组件层 | §3 覆盖表；§5 缺口必须单独勾 |
| 快路径不看 topology | `ensureAdapted` 只要求 `commentHigh` 或当前无 high 候选；topology 规则变了若不加 `rule`，旧缓存会永远跳过重定位 | §6 版本号决策 |
| 类还在 ≠ 入口还对 | 画质同时存在 `getDefaultQuality()` 与 `getSettingsQuality()`；阻止更新旧混淆 owner 会残留 | §3 命中必须是「精确签名 ∩ 方法体语义」 |
| jadx 重定位包写进运行时候选 | `com.bilibili.p4439app.*` 运行时不存在；展开成字母表等于给 `quickLocate` 加必失败 `loadClass` | §6 禁止项 |
| 静默门禁误拒自己的目标 | Story URI 35,657 字符被 `length <= 4096` 丢掉，日志还是 `status=success` | 真机阶段看诊断 id，不看「像没装」 |

`FOUND` 只证明 APK 里有满足当前结构规则的成员。不证明 Hook 装上、页面渲染、点击路径或空位消除。

---

## 1. 收样与身份

```text
APK 放置：Temp/host-compat/apks/bili-<versionName>.apk
审计输出：Temp/host-compat/fixed-audits/<versionName>.tsv
表面探针：Temp/host-compat/surfaces/<versionName>.tsv   （可选）
```

核对（缺一项就停）：

- 包名必须是 `tv.danmaku.bili`（HD `android_hd` 不做）
- 文件名版本与 APK 内部 `versionName` / `versionCode` 一致
- 签名证书 SHA-256 与上一版对照：变了要当「不同发行渠道」，不要直接当补丁
- 未提供的相邻小版本（历史上是 8.85.x、9.0.x）**不准外推为已验证**

本机可用：

```powershell
$env:PYTHONIOENCODING = "utf-8"
python Temp/host-compat/run_intake.py path\to\bili.apk
```

`aapt` 默认找 `%LOCALAPPDATA%\Android\Sdk\build-tools\36.0.0\aapt.exe`。没有 aapt 时脚本只打印文件名，身份必须改用 Android SDK 或设备 `dumpsys package tv.danmaku.bili` 补齐。

Windows 的 `aapt`/`ziparchive` **打不开路径里有非 ASCII 的 APK**（工程目录里那份 `哔哩哔哩-9.10.0(9100200).apk` 会直接 `Illegal byte sequence`）。`run_intake.py` 会拷到临时英文名再 dump；手跑 aapt 时自己先拷一份。Git Bash 控制台请设 `PYTHONIOENCODING=utf-8`，否则缺口说明会乱码。

建议把新 APK 放到 `Temp/host-compat/apks/bili-<versionName>.apk`（纯 ASCII），不要长期放在 Gradle 工程目录里用中文文件名。

---

## 2. 字母表漂移（无 jadx，必跑）

```powershell
python Temp/host-compat/obfuscated_owner_drift.py Temp/host-compat/apks/bili-<ver>.apk
```

一次核对三处「稳定包 + 单字母类名」：

| 点 | 稳定包 | 运行时候选策略 |
| --- | --- | --- |
| 脉络 `ReplyInfo → CommentItem` mapper | `com.bilibili.app.comment3.data.source.v1` | `('a'..'z')`，结构过滤；禁止 jadx `p4439` 包 |
| 相关游戏推广组件 | `com.bilibili.ship.theseus.united.page.intro.module.relate.game` | 字母表 + 未混淆 `RelateGameComponent` |
| gemini 绑定基类 | `com.bilibili.app.gemini.ui` | 显式优先顺序，再追加字母表；必须排除 interface |

退出码非 0，或 mapper owner 多于一个：先当 MISSING，不要猜。8.63.0–8.88.0 无 gemini 框架时该行是 `n/a`，不算漂移。

2026-09-03 已在 26 个本地宿主上跑过，0 越界。新 APK 只要再跑这一个文件。

---

## 3. 结构审计（需要 jadx）

`HostCompatibilityAudit.java` 用 jadx API 只读 DEX，规则刻意对齐 `VersionAdapter` 的保守结构，不反编译源码、不开混淆还原。

本机 jadx：`C:\Users\Administrator\jadx\lib\jadx-1.5.6-all.jar`（1.5.6）。09-03 条目写「本机没有 jadx jar」已经过时。

```powershell
python Temp/host-compat/run_intake.py path\to\bili.apk --audit --prev Temp/host-compat/fixed-audits/<上一版>.tsv
```

或手编：

```powershell
$jadx = "C:\Users\Administrator\jadx\lib\jadx-1.5.6-all.jar"
$out  = "Temp\host-compat\audit-classes"
javac -encoding UTF-8 -cp $jadx -d $out Temp\host-compat\HostCompatibilityAudit.java
java  -cp "$out;$jadx" HostCompatibilityAudit path\to\bili.apk Temp\host-compat\fixed-audits\<ver>.tsv
```

9.10.0 量级约 29 万类，单线程跑完要几分钟。`fixed-audits/9.10.0.tsv` **不含** `comment_topology`（审计器后补的），不能当当前覆盖基线；换版后应重新产出。

画质列可加第三参 `quality-all` 做全类扫描，只在候选表全部落空时用，很慢。

### 3.1 审计 FEATURE id ↔ 安装器

当前 `HostCompatibilityAudit.run()` 会写出这些 `FEATURE` 行。安装器 id 以源码 `*FeatureInstaller.ID` 为准。

| 审计 FEATURE | 安装器 ID | 说明 |
| --- | --- | --- |
| `block_update` | `block_app_update` | 候选表仍是混淆短名，新 owner 要**前置** |
| `player_default_quality` | `player_default_quality` | 必须语义常量 ∩ 无参 `()I`；拒绝 `getSettingsQuality()` |
| `comment_free_copy` | （HookEntry 自由复制） | high handler 结构命中即可，low 可空 |
| `description_free_copy` | （HookEntry 简介复制） | ExpandableTextView + 官方复制方法精确签名 |
| `home_top_bar` | `home_top_bar_purify` | |
| `mine_entry` | （漫游入口 / 适配锚点） | `HomeUserCenterFragment` 构建方法 |
| `mine_vip` | `mine_vip_purify` | |
| `dynamic_tabs` | `dynamic_tabs_purify` | |
| `full_number` | `full_number_display` | |
| `player_portrait` | `player_portrait_control` | |
| `player_status_bar` | `player_status_bar` | |
| `home_recommend` | `home_recommend_purify` | 只证明 holder/items/uri，**不含**时长/类型过滤语义 |
| `video_relate` | `video_relate_filter` | 只证明 list/cardCase，**不含**理由/强力模式 |
| `home_tabs` | `home_tab_filter` | |
| `mine_components` | `mine_component_filter` | 只覆盖 MenuGroup getter/legacy，**不含** `AccountMine.sectionListV2` |
| `story_purify` | `story_purify` | |
| `splash_ads` | `splash_ad_purify` | |
| `bottom_bar` | `bottom_bar` | |
| `teenagers_mode` | `teenagers_mode_prompt` | |
| `comment_filter` | `comment_filter` | |
| `comment_purify` | `comment_purify` | |
| `comment_topology` | `comment_topology` | 结构规则，不按 facade 短名 |
| `comment_section` | `comment_section` | |
| `paused_ad` | `paused_ad` | |
| `home_banner` | `home_banner` | |
| `merchandise` | `merchandise` | |
| `game_promotion` | `game_mentioned_promotion` | mention 协议，**不是** RelateGameComponent |

`MISSING` / `PARTIAL` 必须记下 owner 集合，不要只记状态。`DISCOVERY` 行是新混淆 owner 的来源，阻止更新 / 画质换版时抄这里，不要抄 jadx GUI 里看到的第一个类。

---

## 4. 审计覆盖缺口（静态 FOUND 也救不了）

这些安装器 **不在** `HostCompatibilityAudit` 的 FEATURE 集合里。每次升版必须单独勾，不能因为「其余 26 项 FOUND」就宣称全功能可用。这正是 09-02 → 09-03 的教训。

| 缺口 | 安装器 / 定位入口 | 怎么查 |
| --- | --- | --- |
| 竖屏进普通详情 | `home_vertical_detail` / `locateHomeRecommendFeed` + 启动边界 | 真机 + 抓包；改 cid 前必须有设备证据。长期文档 2026-09-02 |
| 首页子组件隐藏 | `home_component_filter` / `locateHomeComponents` | 结构：父 Fragment 链属于首页容器 |
| 「我的」数据层剪枝 | `locateMineAccountMinePoints`（`AccountMine.sectionListV2`） | `mine_components` FOUND 不够；9.9.x 主路径是 V1 字段不是 V2 getter |
| 详情页相关游戏组件 | `detail_app_promotion` 的 RelateGame 字母表 | **只认** §2 漂移脚本，不认 `game_promotion` FEATURE |
| 话题/GAd 播放器下方卡片 | 同安装器的 `IAdUnderPlayer` 运行时实现 | 离线很难证；真机看诊断 |
| 播放器互动层 | `locatePlayerInteractiveOverlays` | 两个 Guide 家族、DmResource 第二载体、三个 Moss 边界、DmViewReply.activityMeta；默认实例保护和章节点保留必须完整 |
| 影视大会员自动半屏 | `PgcAutoActivityPopupLocator` | 不仅要 constructWith 签名，还要安装期校验 play_half_container 的参数顺序、类型和可空性，并验证真实模型过滤 |
| 新首页框架（平板/宽屏）的底栏与顶栏 Tab | `HomeFrameTabLocator`（`bottom_bar` / `home_tab_filter` 的 `frame` 层） | `python Temp/host-compat/home_frame_audit.py <apk>`：序列化名、元素顺序（按 iput 源寄存器实证）、ViewModel 签名两跳、Companion `serializer()` 都要过；`new_frame_probe.py` 看新旧框架标记。长期文档 2026-09-23（六） |

可选：`HostSurfaceProbe.java` 扫模块源码里的类名在 APK 中是否还在。噪音大（android.*、占位符会 MISSING），只在「某个写死全限定名突然 404」时用。

---

## 5. 对照上一版

有上一版 `fixed-audits/<prev>.tsv` 时：

```powershell
python Temp/host-compat/run_intake.py path\to\new.apk --prev Temp/host-compat/fixed-audits/<prev>.tsv
```

关注：

- 上一版 `FOUND`、本版 `MISSING` / `PARTIAL` 的域
- `block_update` / `player_default_quality` 的 DISCOVERY owner 是否换了（通常要前置到候选表）
- `comment_topology` 的 `mapperOwners=` 是否仍是单字母且落在 `v1` 包

不要对 DISCOVERY 里出现的旧 owner 做删除。新版 DEX 会保留旧混淆类；运行时按新→旧探测，每个候选仍要精确签名。

---

## 6. 决定改什么代码

### 6.1 候选表

| 情况 | 做法 | bump |
| --- | --- | --- |
| 阻止更新 / 默认画质 DISCOVERY 出了新 owner，结构与语义仍对 | 把新 owner **前置**进 `BLOCK_UPDATE_OWNER_CANDIDATES` / `PLAYER_DEFAULT_QUALITY_CLASS_CANDIDATES`，保留旧项 | 只加 `ADAPTER_RULE_VERSION` |
| mapper / RelateGame / gemini 仍在字母表内 | **不改**候选，不写死这次的短名 | 不 bump |
| mapper 漂到多字母或离开稳定包 | 先靠 `DexAssistQuery.COMMENT_REPLY_MAPPER`；仍失败再考虑扩查询，不要写死新短名 | 视 JSON 是否变化 |
| JSON `AdaptResult` 增删改字段 | 改 `toJson`/`fromJson`，两边一起 bump | `SCHEMA_VERSION` **和** `ADAPTER_RULE_VERSION` |
| 只改定位规则、JSON 形状不变 | 例：topology 结构过滤、字母表生成 | **只**加 `ADAPTER_RULE_VERSION` |
| 快路径目前不检查的点（topology）规则变了 | 必须加 `ADAPTER_RULE_VERSION`，否则已适配设备永不重定位 | 只加 rule |

`ensureAdapted` 快路径有效性（2026-09-04 源码）：

```text
cached != null
&& versionCode 匹配
&& fingerprint 匹配（指纹含 ADAPTER_RULE_VERSION）
&& (cached.commentHigh != null || 当前 ClassLoader 没有 high 候选类)
```

它**不**看 `commentTopology`。topology 相关改动只加 schema、不加 rule，等于没改。

### 6.2 DexKit

当前目录只有两点，语义不可互换：

| 查询 | 选择器 | 诊断 id | 何时触发 |
| --- | --- | --- | --- |
| `BLOCK_UPDATE` | `selectUniqueLeaf` | `dex.assist` | 常规定位落空 |
| `COMMENT_REPLY_MAPPER` | `selectSingleOwnerGroup` | `dex.assist.comment_topology` | 字母表 + 结构过滤落空 |

硬限制：

- 只允许后台适配线程创建桥；`quickLocate` / Hook 回调禁止
- 必须 `searchPackages`；8.90.2 无包约束会 59 命中撞 `MAX_MATCHES`
- 结果必须经宿主 ClassLoader 二次验真；多 owner / 多叶子按缺失
- 不要给 `()I` 画质或 `comment_low` 加 DexKit，特征不够强

### 6.3 明确禁止

- 按 jadx 短名或 GUI 第一个类写死运行时候选
- 把 `com.bilibili.pNNNN.*` 重定位名写进 `quickLocate` 会走到的名单
- 在 Hook 回调前置门禁上叠长度/格式（只做归属判断）
- 用 debug APK 当「该宿主版本已支持」的发布证据
- 把本次 TSV 的 FOUND 写进 README「已验证客户端」——那一列需要真机

---

## 7. 单测与门禁

改了候选表或定位器，至少：

- `VersionAdapterTest` 里「最新 owner 优先、隐藏最新后回退上一版」
- 涉及 mapper 时：`ReplyTopologyLocateRoute` 相关桩 + `DexAssistCandidateSelectorTest`
- 涉及装箱/原始类型反射时：`ReflectAccessPrimitiveArgTest` / `MineComponentHiddenFlagWriterTest`

然后从 Gradle 工程目录：

```powershell
cd Bilibili_Innocent_Lab
.\gradlew.bat assembleDebug testDebugUnitTest lintDebug minifyReleaseWithR8 --console=plain --no-daemon
```

核对 `app/build/outputs/apk/debug/app-debug.apk` 的 mtime。宣称某宿主可用还要真机，不能在这里停。

### 7.1 未升级宿主时的 Android APK 契约验证

2026-09-05 新增 `HostApkCompatibilityInstrumentedTest`，直接运行生产 VersionAdapter，补足
离线 Java 审计器与实际 Android 反射可能不一致的盲区。先核对宿主签名和哈希，再把只读 APK 放入
模块私有 `cache/host-compat/`；测试不安装该 APK、不挂 Hook、不打开宿主、不改开关。
需额外构建 `assembleDebugAndroidTest`。参数、两个方法和报告范围见 `docs/verification.md`
的 Host APK intake 小节。模块与测试包按相同签名覆盖安装，不用会卸载模块的自动设备测试任务。

- 新版本和上一版运行 `verifyHostApkContracts`，检查完整定位签名、缓存序列化、互动层及 PGC
  真实模型过滤。报告保留原始诊断；新版 high 已就绪时，残留旧评论 low 不应单独判整轮失败。
- 出现同名类的旧版本运行 `verifyVersionAnchors`，只验证更新/画质入口选择，不能宣称旧宿主
  全功能通过。9.11 新增 mq1.c 在 8.84/8.86/8.90.2/8.92.1 同名，es1.i 在 8.84 同名，
  但旧类没有目标签名；因此“类存在即命中”必错。所有新增混淆候选都要对旧 APK 集查碰撞。
- 只读 APK 是动态代码装载的要求；父加载器只用系统加载器，避免混入模块的 AndroidX/Kotlin。
  卸载本次临时测试应用并清理专用目录内本次复制的 APK，保留本地报告。
- 原始 FEATURE 审计当前共 27 项，仍须单独核对 §4 缺口。APK 契约通过不能取代下节的宿主
  实际页面与 LSPosed/NPatch 验收，不能据此扩大 README 的“已验证客户端”范围。

---

## 8. 真机最低集

静态全部 FOUND 之后，至少：

1. 冷启动出现适配 toast；第二次启动走快路径（无「正在适配」）
2. 首页推荐过滤、底栏、顶栏
3. 动态 tab
4. 「我的」：大会员卡 + 组件勾选（走 `sectionListV2` 的版本要点进「我的」再回模块看快照）
5. 评论 / 简介自由复制
6. 有回复的一级评论操作栏出现「脉络」；诊断 `comment.topology` 不是 `MISSING`；正常情况 `dex.assist.comment_topology` 应为 `not-required`
7. 视频详情：相关推荐 / 游戏提及 / 暂停广告
8. 竖屏视频进普通详情（失败时看诊断放行原因，不要先改 cid）
9. 对应开关关闭后宿主原行为恢复

设备日志：`adb shell su -c`（Git Bash 先 `export MSYS_NO_PATHCONV=1`）。LSPosed 看 `/data/adb/lspd/log/verbose_*.log`。诊断中心导出优先于截图口述。

NPatch 路径另走免 Root 契约，不在本清单里用「LSPosed 上 FOUND」代替。

---

## 9. 回填档案

设备或规则有结论时，在 `docs/development_experience.md` 追加日期条目，至少写：

- 宿主 `versionName` / `versionCode` / 证书 SHA-256
- 哪些 FEATURE 变了，候选表是否前置
- `sv` / `rule` 是否 bump，以及**为什么**（尤其是「JSON 没变但必须加 rule」）
- 真机做了哪些、明确没做哪些
- 失败方案（猜短名、扩 DexKit、不 bump 等）

只有会改变多数任务决策的结论才浓缩进 `AGENTS.md`。TSV 留在 `Temp/host-compat/`，不进公开仓库。

---

## 10. 一页命令

```powershell
# 身份 + 字母表漂移 + 与上一版 TSV 对照（无 jadx）
python Temp/host-compat/run_intake.py Temp/host-compat/apks/bili-9.11.0.apk `
    --prev Temp/host-compat/fixed-audits/9.10.0.tsv

# 加上 jadx 结构审计（慢）
python Temp/host-compat/run_intake.py Temp/host-compat/apks/bili-9.11.0.apk `
    --audit --prev Temp/host-compat/fixed-audits/9.10.0.tsv
```

跑完先看脚本打印的「缺口」和「rule/schema 决策」，再打开 TSV。
