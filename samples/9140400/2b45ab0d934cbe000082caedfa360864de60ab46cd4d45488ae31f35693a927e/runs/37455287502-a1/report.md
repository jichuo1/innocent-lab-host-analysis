# 页面多路径覆盖与样式变化审计

分析结果：REVIEW_REQUIRED

任务执行成功不等于模块适配通过。评论区、动态页最高优先级；所有登记路径分别核对。静态证据；AI 未接入，运行期样式启用未知。

| 家族 | 类数 | Compose 方法 | 外部 invoke 边 | 证据 |
|---|---:|---:|---:|---|
| comment_compose | 2378 | 274 | 939 | static_invoke_observed |
| comment_legacy_v2 | 586 | 0 | 761 | static_invoke_observed |
| comment_native_exp3 | 67 | 0 | 84 | static_invoke_observed |
| comment_native_legacy | 181 | 0 | 243 | static_invoke_observed |
| comment_native_next | 47 | 0 | 64 | static_invoke_observed |
| comment_other_ui:(root) | 188 | 2 | 492 | static_invoke_observed |
| comment_other_ui:adapter | 8 | 0 | 22 | static_invoke_observed |
| comment_other_ui:nextwidget | 15 | 0 | 12 | static_invoke_observed |
| comment_other_ui:span | 15 | 0 | 13 | static_invoke_observed |
| comment_other_ui:view | 191 | 0 | 119 | static_invoke_observed |
| comment_other_ui:webview | 3 | 0 | 1 | static_invoke_observed |
| comment_other_ui:widget | 238 | 32 | 298 | static_invoke_observed |
| danmaku_kotlin | 57 | 1 | 8 | static_invoke_observed |
| danmaku_legacy | 0 | 0 | 0 | absent |
| detail_legacy | 0 | 0 | 0 | absent |
| detail_theseus_ugc | 1906 | 25 | 499 | static_invoke_observed |
| detail_theseus_united | 4485 | 98 | 4140 | static_invoke_observed |
| dynamic_compose | 953 | 112 | 143 | static_invoke_observed |
| dynamic_legacy | 3193 | 104 | 2143 | static_invoke_observed |
| dynamic_opus | 1313 | 92 | 195 | static_invoke_observed |
| dynamic_other:appointment | 26 | 3 | 18 | static_invoke_observed |
| dynamic_other:card | 412 | 82 | 287 | static_invoke_observed |
| dynamic_other:commonCore | 24 | 0 | 58 | static_invoke_observed |
| dynamic_other:commonPerf | 13 | 1 | 2 | static_invoke_observed |
| dynamic_other:commonUi | 21 | 5 | 9 | static_invoke_observed |
| dynamic_other:lightBrowser | 71 | 18 | 29 | static_invoke_observed |
| dynamic_other_legacy | 2063 | 4 | 2145 | static_invoke_observed |
| home_legacy | 1031 | 128 | 222 | static_invoke_observed |
| home_new_frame | 182 | 33 | 53 | static_invoke_observed |
| mine_account_model | 132 | 0 | 54 | static_invoke_observed |
| mine_native | 318 | 7 | 98 | static_invoke_observed |
| pgc_legacy | 357 | 0 | 397 | static_invoke_observed |
| pgc_theseus | 2194 | 131 | 4407 | static_invoke_observed |
| player_java | 962 | 0 | 3235 | static_invoke_observed |
| player_kotlin | 8 | 0 | 150 | static_invoke_observed |
| search_compose | 3147 | 556 | 594 | static_invoke_observed |
| search_native | 1625 | 2 | 2760 | static_invoke_observed |
| story_kotlin | 0 | 0 | 0 | absent |
| story_native | 2884 | 44 | 1389 | static_invoke_observed |

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
