# 9150300 静态分析复核更正版 review1

**Codex 独立源码复核更正；新增模型请求 0。此文不是一次新的模型报告，也不代表安装、Hook 或设备效果验收。**

原报告：[38754554941-a1](https://github.com/jichuo1/innocent-lab-host-analysis/blob/reports/samples/9150300/c07cf0a3b838ecbc926d0a11c377e7fcb45c92b8aba7ee01d32cd2729b6a6110/runs/38754554941-a1/report.md)；[原 Release](https://github.com/jichuo1/innocent-lab-host-analysis/releases/tag/analysis-9150300-c07cf0a3b838-38754554941-a1) 保留不变。
本复核对应 APK SHA-256：`c07cf0a3b838ecbc926d0a11c377e7fcb45c92b8aba7ee01d32cd2729b6a6110`；应用源码快照 `2fa2d3b70f73fa431ed83267a9519c726a41b67de39eb7ee785813de39067120`，source head `5422fad1e3f798252619d610a0504573ff47211b`。

## 本次更正与证据边界

- 原模型账务完整保留：累计 19 次请求，本轮原生成新增 16 次，1 次补偿，累计 529.268020492 秒；未知计费仍未知。此次 Codex 复核新增 0 次模型请求。
- 覆盖 10 个已登记页面、25 条路径、12 条 finding；原 AI 独立 review 为 10 revised、2 retained。更正版对原文字与引用的修改由 Codex 标明，不归为新的模型输出。
- 689 是已验真固定源码清单，模型实际 module_source 正文调用为 0；安装器、定位器和 Hook 覆盖未知。dirty 是整体工作树状态，不能推出选中源码未提交或过期。
- 唯一变化资源文件为 resources.arsc；其内部 entry 与页面归属仍未解析。未登记 UI、服务端视觉变体、平板/宽屏路由和运行启用未穷尽。
- F004 的 52 条定义与 18 条边不能相减。E014 仅返回 12/18 样本；独立读取冻结全 18 边，确认来自 3 个 caller 类、涉及 9 种唯一 callee 签名，caller 均归类 search_compose；仍不证明运行消费或模块覆盖。
- revised finding 的最终引用采用已验证 review row；原草稿与 review 文件逐字保存。页级“0 Compose 即 View”“边数差即未调用/主通道”等表述改为限定的静态观察。

## 更正总览

本更正版由Codex基于冻结证据独立复核，不是一次新模型生成。目标9150300与基线9150200覆盖10个登记页面、25条路径；当前采集class_records与invoke_edges逐项一致，不能外推到未登记UI或服务端/运行状态。唯一资源文件变化已知为resources.arsc，其内部entry与页面归属尚未解析。原模型已完成12条finding的独立review（10 revised、2 retained），本更正版同步revised引用并纠正统计单位、样本范围与页级过度推断。源码为本次按SHA固定的689文件快照；dirty是整体状态，不能推出选中Hook文件均未提交或过期。本轮模型module_source正文读取为0，安装器/定位器覆盖与实际注入版本尚未验证，runtime_verified保持false，不宣称适配通过或样式穷尽。

## 全部页面与登记路径

### comment

本页登记静态摘要：comment_legacy_v2: 581类/0个Composer签名/734条外部invoke边；comment_native_legacy: 156类/0个Composer签名/177条外部invoke边；comment_native_next: 45类/0个Composer签名/46条外部invoke边；comment_native_exp3: 60类/0个Composer签名/59条外部invoke边；comment_compose: 2417类/274个Composer签名/918条外部invoke边。两版本当前登记采集记录一致；comment_java_moss: 50条定义/50条invoke边；comment_kotlin_moss: 130条定义/26条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### comment_legacy_v2 · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：581类、0个匹配Composer签名、734条外部invoke边，fingerprint=dc1ce6f264dcb03a41f07c9e62ab96960b84a44cfb4f08c86b2e303ddc49ee44；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E001

#### comment_native_legacy · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：156类、0个匹配Composer签名、177条外部invoke边，fingerprint=5f1a4dd53cbaae51fb45d984193742cedf07d76da36e3b4130d13addea0a330c；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E001

#### comment_native_next · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：45类、0个匹配Composer签名、46条外部invoke边，fingerprint=4f7755ff77b0b83cbe617afc6e39314ed234091c1a4098e850d3837a6562e8be；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E001

#### comment_native_exp3 · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：60类、0个匹配Composer签名、59条外部invoke边，fingerprint=d0a1de81d6ec335006536430c98e1c5eb255a1ad18180c7c52d9f6603374f370；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E001

#### comment_compose · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：2417类、274个匹配Composer签名、918条外部invoke边，fingerprint=b91f872535860e67b091dfa456d421e21d5d3c892b76ddedc9b5475a9ab32f58；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E001, E011

### dynamic

本页登记静态摘要：dynamic_legacy: 3227类/105个Composer签名/2193条外部invoke边；dynamic_compose: 956类/112个Composer签名/170条外部invoke边；dynamic_opus: 1341类/92个Composer签名/190条外部invoke边。两版本当前登记采集记录一致；dynamic_java_moss: 134条定义/134条invoke边；dynamic_kotlin_moss: 382条定义/26条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### dynamic_legacy · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：3227类、105个匹配Composer签名、2193条外部invoke边，fingerprint=d5217d0231ebb0b4a94090bd66a327cc2f0e8a8a9121a072c785b9dfe9ea93d5；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E002

#### dynamic_compose · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：956类、112个匹配Composer签名、170条外部invoke边，fingerprint=84a035d38f909be788d5247705201acb5c3b448b8600a2866ba23c786f064ba3；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E002

#### dynamic_opus · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：1341类、92个匹配Composer签名、190条外部invoke边，fingerprint=5f15905be8c735b1c22dfbd47211fdb23a9311aeec87e561902d7caadcacdd43；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E002, E012

### home

本页登记静态摘要：home_legacy: 1004类/128个Composer签名/236条外部invoke边；home_new_frame: 196类/33个Composer签名/46条外部invoke边。两版本当前登记采集记录一致；登记协议区为空，不能推出无实际协议消费。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### home_legacy · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：1004类、128个匹配Composer签名、236条外部invoke边，fingerprint=aa99feb80290f6630a8290088a4c9e74fada2a1efee9836aff429fb5e2cff4a9；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E003

#### home_new_frame · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：196类、33个匹配Composer签名、46条外部invoke边，fingerprint=e3ea685642f274af8aeca95d7b99c2c8d40c0bda3fc1d8344fbb49de4a55a3d4；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E003, E013

### search

本页登记静态摘要：search_native: 1674类/2个Composer签名/2789条外部invoke边；search_compose: 3149类/556个Composer签名/616条外部invoke边。两版本当前登记采集记录一致；search_java_moss: 24条定义/22条invoke边；search_kotlin_moss: 52条定义/18条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### search_native · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：1674类、2个匹配Composer签名、2789条外部invoke边，fingerprint=481dae5054c9577e9f646595bc406622f046f998f0cbfe1fbb6dd02b8444c740；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E004

#### search_compose · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：3149类、556个匹配Composer签名、616条外部invoke边，fingerprint=6c663f2d20fafc071e527b799390cfbdb79d250ff1b073fba495840a0ac786e1；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E004, E014

### detail

本页登记静态摘要：detail_legacy: 0类/0个Composer签名/0条外部invoke边；detail_theseus_ugc: 1953类/25个Composer签名/515条外部invoke边；detail_theseus_united: 4602类/98个Composer签名/4163条外部invoke边。两版本当前登记采集记录一致；detail_java_moss: 32条定义/35条invoke边；detail_kotlin_moss: 76条定义/10条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### detail_legacy · absent

- 变化：目标与基线当前登记摘要一致：0类、0个匹配Composer签名、0条外部invoke边，fingerprint=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945；status保持absent。
- 影响：当前规则没有匹配到该登记家族，不能推出页面功能消失、所有实际挂载点不存在或Hook必然无效；需区分规则边界与实际实现。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E005

#### detail_theseus_ugc · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：1953类、25个匹配Composer签名、515条外部invoke边，fingerprint=c36f2a42930dc4782361f39a8b58afc94a19649469b9b6797f8ad2138d4984cc；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E005, E012

#### detail_theseus_united · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：4602类、98个匹配Composer签名、4163条外部invoke边，fingerprint=83e1f0b1ede48a39a9bf5c8c7654481a5c08f067ddaacb373c21cf169b07f5fe；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E005

### pgc

本页登记静态摘要：pgc_legacy: 353类/0个Composer签名/401条外部invoke边；pgc_theseus: 2249类/131个Composer签名/742条外部invoke边。两版本当前登记采集记录一致；pgc_player_moss: 12条定义/3条invoke边；pgc_view_moss: 14条定义/7条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### pgc_legacy · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：353类、0个匹配Composer签名、401条外部invoke边，fingerprint=58516e1deb4e63124df153e402f253f340fbc9f99e34a43606ac4c176ebfebeb；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E006

#### pgc_theseus · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：2249类、131个匹配Composer签名、742条外部invoke边，fingerprint=e02d9f2747072662b44fd47822116e1d35c46efc5096dddedea9ee915428fe12；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E006

### player

本页登记静态摘要：player_java: 953类/0个Composer签名/3225条外部invoke边；player_kotlin: 7类/0个Composer签名/100条外部invoke边。两版本当前登记采集记录一致；player_java_moss: 18条定义/2条invoke边；player_kotlin_moss: 34条定义/3条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### player_java · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：953类、0个匹配Composer签名、3225条外部invoke边，fingerprint=4102698f3c1fdaab7ca6c3526b3d0ff77426ca433eaf8bd71fdde0d3824403bc；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E007, E011

#### player_kotlin · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：7类、0个匹配Composer签名、100条外部invoke边，fingerprint=b275709b530b2d285814f47291544549ad6ce5359fca2f93a8a7c5cc8a9d7edc；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E007

### danmaku

本页登记静态摘要：danmaku_legacy: 0类/0个Composer签名/0条外部invoke边；danmaku_kotlin: 56类/1个Composer签名/9条外部invoke边。两版本当前登记采集记录一致；danmaku_java_moss: 22条定义/20条invoke边；danmaku_kotlin_moss: 46条定义/4条invoke边。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### danmaku_legacy · absent

- 变化：目标与基线当前登记摘要一致：0类、0个匹配Composer签名、0条外部invoke边，fingerprint=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945；status保持absent。
- 影响：当前规则没有匹配到该登记家族，不能推出页面功能消失、所有实际挂载点不存在或Hook必然无效；需区分规则边界与实际实现。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E008

#### danmaku_kotlin · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：56类、1个匹配Composer签名、9条外部invoke边，fingerprint=f55e24e08dd891f8591d14fb9233e06a202bdfc5d566ed086334fa848bfab1cb；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E000, E008

### story

本页登记静态摘要：story_native: 2958类/44个Composer签名/1380条外部invoke边；story_kotlin: 0类/0个Composer签名/0条外部invoke边。两版本当前登记采集记录一致；登记协议区为空，不能推出无实际协议消费。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### story_native · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：2958类、44个匹配Composer签名、1380条外部invoke边，fingerprint=6b74bce42db028676a9b876d8f332257e2f9b8ad604dcfce1b0841742d483e99；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E009

#### story_kotlin · absent

- 变化：目标与基线当前登记摘要一致：0类、0个匹配Composer签名、0条外部invoke边，fingerprint=4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945；status保持absent。
- 影响：当前规则没有匹配到该登记家族，不能推出页面功能消失、所有实际挂载点不存在或Hook必然无效；需区分规则边界与实际实现。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E009

### mine

本页登记静态摘要：mine_native: 324类/7个Composer签名/95条外部invoke边；mine_account_model: 132类/0个Composer签名/54条外部invoke边。两版本当前登记采集记录一致；登记协议区为空，不能推出无实际协议消费。定义、类数和调用边属于不同单位，不能换算覆盖率、未调用数量或运行主通道。Composer签名匹配计数不是UI样式分类，普通数据类也不证明另一条渲染栈。runtime_enabled仍为unknown；源码快照已固定689文件，但本轮module_source调用为0，未完成定位器/安装器正文评审或设备验证。

#### mine_native · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：324类、7个匹配Composer签名、95条外部invoke边，fingerprint=cf69dfa72bd0aab4bb89f33ac7b5ad3e0483282d900389ec538da9133b8ae35d；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E010

#### mine_account_model · static_invoke_observed

- 变化：目标与基线当前登记摘要一致：132类、0个匹配Composer签名、54条外部invoke边，fingerprint=d5370d6ef7f86f092837bbc4aaa634512a18266f46db9e0eb8d7dcb03a011996；status保持static_invoke_observed。
- 影响：仅确认该登记家族在静态采集中可见。未读取对应模块绑定条件，不能确认定位器命中、安装覆盖、运行启用或策略效果；计数和命名均不能证明具体UI样式。
- 补证：先从精确pinned源码中读取本路径相关定位器/安装器及公共注册契约，核类/方法签名、版本门控、生命周期与fallback；已有调用边先按唯一签名和caller归属核对。随后在授权环境记录实际加载路径、Hook回调和用户可见效果；存在可控实验分支时再做分支对照。
- 证据：E010

## 全部 12 条 finding（Codex 校正后）

### F001 · 9150300 与 9150200 八条登记路径指纹逐字相同、changes 为空，不能推出“适配通过”

页面：`comment`；等级：`static_evidence`。

评论五条与动态三条登记路径的采集计数、指纹在目标9150300与基线9150200之间一致。独立复核冻结priority-target/baseline确认class_records及invoke_edges逐项相同。E015/E016属于每家族最多2类的页面预取；E017/E018分别提供comment_compose两侧各5类抽样（sample_limit=5），抽样类的方法体摘要与签名一致，不能代表整族2417类。指纹实际包括类名、DEX file_id、字段/方法签名及method_bodies_sha256，不能以改名或DEX调序“相互抵消”解释不变。上述观察只覆盖已登记抽取面，不证明模块安装、运行启用或服务端视觉变体相同。

建议：以 9150300 真机为基准，逐路径采集 Hook 安装与调用日志；对无变化路径仍按未知处理，不得默认沿用基线适配结论，也不得把指纹一致写成“已适配”。

替代解释与边界：变化可能位于未登记家族、资源表内部条目或运行/服务端配置；当前采集记录一致不能证明样式穷尽，也不能替代定位器、安装器和真机验证。

证据：E015, E016, E017, E018

### F002 · 评论与动态协议只到静态调用观测，module_coverage 均需安装器评审

页面：`comment`；等级：`needs_runtime`。

seed 中 comment_java_moss（50 定义/50 边）、comment_kotlin_moss（130 定义/26 边）、dynamic_java_moss（134/134）、dynamic_kotlin_moss（382/26）的 runtime_enabled 均为 unknown，且四条路径的 module_coverage 都是 requires_installer_review。定义数与调用边数单位不同，不能相除推导覆盖率；kotlin moss 定义多而边少，只能说明静态调用点稀疏，不能说明协议已被消费。共同协议是否有跨家族消费者、安装器/定位器是否有兜底，本轮均未读到。

建议：优先核 HookEntry/VersionAdapter/VersionAdapterContract 的安装分支：确认这些协议 stub 与评论/动态家族是否被同一安装器注册，以及未命中时的 fallback 行为。

替代解释与边界：若安装器日志显示某协议 stub 从未被注册，则“需安装器评审”可升级为明确缺口；若真机日志显示协议方法被调用且 Hook 生效，则当前保守结论可放宽。

证据：E001, E002

### F003 · Opus 家族静态同时存在 Compose 与普通类形态，是否并存渲染栈与覆盖归属均未确认

页面：`dynamic`；等级：`candidate`。

E012 抽样显示 dynamic_opus 家族中既有纯数据类（api/k、api/C、api/H），也有带 Compose 签名的方法（api/r.a(Modifier,Composer,int)V、api/i.d(Composer,int)V），说明该家族静态层面同时包含两类形态，可能对应多种渲染栈；但结果被截断、样本仅 5 个类，不能代表 1341 个类，也无法证明两条栈在真机并存或哪条被启用——未读方法体不能推断 Compose 调用点真正执行。E016 确认三条动态路径整体与基线同构且 runtime_enabled=unknown。OpusMoss/KOpusMoss 处于 unregistered_protocols，若模块依赖这些协议结构做定位，可能缺少对应消费者，跨家族消费者与兜底路径未验证。

建议：对 api/r、api/i 等类用 decompile_class 读取完整方法体，确认 compose 调用点与调用者；真机 Opus 详情页验证 DynamicPurifyFeatureInstaller 是否命中，并抓取 OpusMoss/KOpusMoss 的协议消费方。

替代解释与边界：若完整读取后发现这些 compose 方法属未启用的可选模块，则“并存栈”推断应降级为静态存在但运行不激活；若真机 Opus 页仅走 legacy 栈，则 Opus 覆盖问题转为冗余而非缺失；若确定无任何模块消费者依赖 OpusMoss/KOpusMoss，则协议未登记的缺口等级应下调。

证据：E012, E016

### F004 · search_kotlin_moss 已观测调用边全部落在 search_compose 聚合仓库层，跨家族覆盖边界未闭合

页面：`search`；等级：`static_evidence`。

E014摘要记录52条方法定义和18条外部invoke边，实际返回12/18条边样本（sample_limit=12），样本均标注search_compose，不是上限4，也不是返回全18条。定义条数与调用边数不是同一单位，不能用52−18推断34个未调用签名。Codex独立筛选冻结priority-target.json中的全部18条边，确认caller均归类search_compose，来自3个caller类、涉及9种唯一callee(owner,name,descriptor)；这仍不证明全部运行消费者或模块Hook覆盖。search_java_moss的静态消费者归属与模块共同通道需另核。

建议：用 module_source 读取 KotlinMossChannel.kt 与 KotlinMossReplyBridge.kt，确认其挂载类/方法与上述三个 repository 类及 KSearchMoss 成员的对应关系；若挂载点只覆盖 searchAll 或只覆盖 native 侧，则在 compose 渲染切换时可能漏净化。另用 protocol_evidence 展开 search_java_moss 的调用者家族，确认是否存在 native 侧消费者。真机对同一关键词分别以 compose/native 渲染抓取返回结构，比较净化前后差异。

替代解释与边界：静态图不解析所有接口分发、反射和动态代理；归为search_compose的仓库也可能被多个UI消费。即便完整18条已采集边都属该家族，也不能推出native页面没有运行消费者。

证据：E014, E004

### F005 · home_new_frame 的 HomeFrameViewModel 动作派发签名已观测，定位器覆盖与兜底仍未读取

页面：`home`；等级：`needs_runtime`。

E013(family_evidence, home_new_frame, target)给出类样本：tv.danmaku.bili.khome.widget.bubble.d/e/f/t 与 tv.danmaku.bili.khome.vm.HomeFrameViewModel$dispatchAction$1；后者 superclass 为 Lkotlin/coroutines/jvm/internal/SuspendLambda，fields 为 ["$action","LLo1/b;"]、["label","I"]、["this$0","Ltv/danmaku/bili/khome/vm/HomeFrameViewModel;"]，methods 为 <init>(HomeFrameViewModel;LLo1/b;Continuation)、create、invoke、invokeSuspend。由此可推断新框架通过 SuspendLambda 包装 action 对象派发，但这是对签名的语义推断，不是对 method body 的直读。E013 摘要 total_classes=196、fingerprint e3ea6856…a3d4，与 E003 基线侧同指纹，属既有实现延续，本区间无新增类或调用边。HomeFrameTabLocator.kt 与 HomeFrameListHook.kt 的匹配条件、命中日志与回落分支本轮均未读取，module_coverage=requires_installer_review、runtime_enabled=unknown 保持不变。

建议：用 module_source 读取 HomeFrameTabLocator.kt 与 HomeFrameListHook.kt，核对匹配条件是否包含 tv/danmaku/bili/khome/vm/HomeFrameViewModel 或 khome/widget/bubble 族，以及 $action:LLo1/b 是否被用作定位条件；同时读取 HookEntry.kt/VersionAdapter.kt 确认两家族是否经同一安装器注册。真机上(存在本地或服务端框架开关时)触发框架切换，记录定位器命中与未命中时的回落行为。

替代解释与边界：替代解释：(1) $action:LLo1/b 可能是被多个模块共享的通用 action 基类，不足以判定定位器脆弱；(2) 该 ViewModel 可能存在于 APK 但真机不加载(类计数包含未使用代码)，则 Hook 覆盖问题不成立；(3) 定位器若基于方法签名或注解而非类名，类名变更不影响命中。若真机日志显示稳定命中，本推断被推翻。

证据：E013, E003

### F006 · 登记家族采集记录未变，唯一资源文件变化为resources.arsc，内部页面归属未知

页面：`home`；等级：`candidate`。

home与search四条登记路径的计数与指纹在两版本间一致；独立核对冻结采集结果，class_records与invoke_edges均相同。priority-summary.json明确给出资源差异added=[]、removed=[]、changed=[resources.arsc]，scope为global_resources_not_yet_attributed_to_pages。外层文件路径及资源表类型已知，尚未解析的是资源表内部条目、含义和页面归属。不能据此认定新UI，也不能据登记家族不变认定所有样式已穷尽。

建议：如需继续补证，应先比较resources.arsc内部资源entry与页面引用，再核对精确pinned模块安装器/定位器；服务端和真实页面分流仍需另行授权运行验证。

替代解释与边界：变化可能仅涉及资源表元信息，也可能影响具体资源entry；当前资料未定位内部变化。未登记家族和服务端/运行状态仍不在本次结构一致结论之内。

证据：E003, E004, E000

### F007 · detail登记家族采集记录一致，模块安装器与实际注入版本尚未核对

页面：`detail`；等级：`candidate`。

E005中detail_legacy按当前规则匹配0类（absent），detail_theseus_ugc为1953类/25个Composer签名/515条外部边，detail_theseus_united为4602类/98个Composer签名/4163条边，目标与基线一致。absent不等于功能消失或所有实际挂载点不存在。detail_java_moss为32定义/35条边，detail_kotlin_moss为76定义/10条边，单位不能相减或换算覆盖率。源码快照已按SHA固定689文件；working_tree_dirty是整体工作树状态，不能推出选中Hook文件均未提交、过期或内容不可知。本轮模型没有调用module_source，因此未读取相关安装器/定位器正文，也未核对实际注入产物与快照的一致性，module_coverage继续requires_installer_review。

建议：从精确pinned快照读取Detail相关安装器/定位器及公共注册契约，核目标类/签名、版本门控与fallback；协议caller可先筛现有冻结invoke_edges，运行注入版本与Hook效果另验。

替代解释与边界：已登记抽取规则可能遗漏改名或未登记实现，服务端或运行选择也可能改变可见页面；冻结源码可验不等于已经逐文件审读，更不等于安装在设备上的产物。

证据：E005, E000

### F008 · PGC 两协议调用边少于定义数，消费者路径归属与模块定位器目标均未确认

页面：`pgc`；等级：`needs_runtime`。

E006记录pgc_legacy 353类/0个Composer签名/401条外部边、pgc_theseus 2249类/131个Composer签名/742条边，两侧计数和指纹一致。pgc_player_moss为12定义/3边，pgc_view_moss为14定义/7边；定义和边是不同单位，桥接方法影响定义集合，但不能推出定义数天然高于边数或业务入口未被消费。E006已保存pgc_player_moss的3/3 caller样本（external_or_unknown）及pgc_view_moss的4/7样本（pgc_theseus），不能说完全没有caller资料。0个匹配签名不证明纯View/Activity实现，131个也不证明整条路径只有Compose渲染。模块PgcAutoActivityPopupLocator等正文未读取，定位器目标和运行分支仍未知。

建议：1) 用 protocol_evidence 重读 pgc_player_moss 与 pgc_view_moss 的完整调用方列表（含 caller_samples），逐个标注所属家族与路径，并区分业务入口与桥接/序列化桩。2) 用 module_source 读取 PgcAutoActivityPopupLocator.kt 与 PgcAutoActivityPopupPolicy.kt，记录其类名/方法签名匹配条件与兜底分支，判断命中 legacy 还是 theseus。3) 真机上在番剧/影视详情与播放页抓取弹窗相关 Activity 与定位器日志，并做单路径置空对照（对其中一条路径强制关闭，观察是否仍命中）。4) 未读到运行条件前保持 runtime_enabled=unknown，不因页面可用而改写 status。

替代解释与边界：静态调用者可能位于其它或未登记家族；接口分发和反射不完全可见。两组类静态存在不证明两套运行渲染栈同时启用，需模块源码及运行路径另证。

证据：E006, E014

### F009 · player 页两条注册路径指纹与基线逐字节一致，本版本窗口内无可观测家族变化

页面：`player`；等级：`static_evidence`。

目标 9150300 与基线 9150200 的 player_java 指纹同为 4102698f3c1fdaab7ca6c3526b3d0ff77426ca433eaf8bd71fdde0d3824403bc（953 类 / 0 compose / 3225 外部调用边），player_kotlin 同为 b275709b530b2d285814f47291544549ad6ce5359fca2f93a8a7c5cc8a9d7edc（7 类 / 0 compose / 100 边）；changes 为空数组，resource_change_counts 仅 changed=1，未登记任何家族级增删。协议侧 player_java_moss 18 定义 / 2 实调用，player_kotlin_moss 34 定义 / 3 实调用，同样与基线一致。这说明该页没有结构级适配风险信号，但结构无变化也可能意味着变化发生在服务端开关控制的视觉层，静态不可见。

建议：（1）真机安装模块，抓取 Player*Locator 解析日志，记录命中类名/方法签名与未命中项；（2）对 player_kotlin_moss 的 3 条实调用边做宿主回溯，确认模块 Kotlin Moss 解析点是否落在其中；（3）若安装器日志显示遍历类数与 953/7 明显偏离，需排查混淆改名导致定位器按名匹配失效。

替代解释与边界：指纹一致也可能掩盖两类情形：一是 DEX 重排/编译参数变化但方法体哈希恰好稳定，二是家族类集合未变而内部实现被替换但抽取粒度未捕捉。若能取得目标 APK 中同一批类的方法体哈希并与基线逐一比对、或安装器日志显示定位器失败，则当前‘无变化’推断应被推翻。

证据：E000, E007

### F010 · danmaku登记家族格局未变，协议消费者与模块挂载点仍需核对

页面：`danmaku`；等级：`needs_runtime`。

E008显示danmaku_legacy按当前规则匹配0类，danmaku_kotlin为56类/1个Composer签名/9条外部边，目标和基线一致；这不是9150300新增的家族替换。danmaku_java_moss为22定义/20条invoke边，danmaku_kotlin_moss为46定义/4条边，不能由此计算覆盖率、未调用定义数或判定Java为运行主通道。1个Composer签名不足以量化Compose化程度；协议标识也不是已登记UI路径。模块安装器/策略正文没有被本轮模型读取，消费者归属、fallback和运行生效保持未知。

建议：（1）将 danmaku_kotlin 的 56 类清单与 DanmakuPurifyFeatureInstaller 的 hook 目标集合逐项比对，输出命中/缺失清单与绑定签名；（2）回溯 danmaku_java_moss 的 20 条实调用边宿主类，判定其归属家族（Kotlin 家族或未登记调用者）；（3）用同一静态抽取规则对 danmaku_legacy 已知类名前缀在目标 APK 做定向检索，区分真 absent 与抽取口径缺失；（4）真机弹幕页对净化开关做 A/B，记录 DanmakuPurifyPolicy 分支命中与未命中时的兜底日志；（5）核对未映射候选 KotlinMossChannel/KotlinMossReplyBridge/HookEntry 是否参与弹幕路径分发，避免漏算覆盖。

替代解释与边界：若真机日志显示净化策略分支正常命中且样式生效，则“挂载点存疑”推断被推翻；若定向检索能在目标 APK 中找到 legacy 家族类，则 absent 属抽取口径缺失而非家族消失；若安装器日志显示定位器遍历到的类名与静态家族不一致，则可能是混淆改名导致家族归并错误；若 danmaku_kotlin_moss 的 4 条实调用边宿主不在 56 类集合内，则 Kotlin Moss 消费者可能位于未登记家族。

证据：E000, E008

### F011 · story/mine 两侧登记家族摘要与指纹逐位相同，本版本差异在静态家族层不可见

页面：`story`；等级：`static_evidence`。

story_native、story_kotlin、mine_native、mine_account_model在两侧的登记家族摘要与指纹一致；独立核对当前冻结class_records和invoke_edges亦一致。story_kotlin的0类只表示当前登记规则未匹配，不证明功能或所有Kotlin实现消失。唯一资源文件变化已知为resources.arsc，内部entry和页面归属尚未解析。上述静态观察不能推出安装器匹配、运行适配通过或服务端样式相同。

建议：把本单元结论限定为“story/mine 登记家族静态层面未观测到变化”，不进入适配通过判定；后续版本对比优先按资源条目与模块解析点变化触发，而非仅靠家族指纹是否变化触发。

替代解释与边界：未登记家族、资源表内部变化和运行/服务端选择仍可能改变体验。当前登记采集记录一致不代表所有页面实现已枚举，也不证明已安装模块与冻结源码一致。

证据：E009, E010

### F012 · story/mine协议登记为空，相关未登记协议仍是待核caller候选

页面：`story`；等级：`candidate`。

E009/E010的story与mine登记protocol字典为空；未知协议名单中存在StoryMoss、KMineMoss、MineMoss、AccountInterfaceV1Moss等候选，但单凭名字不能证明其caller属于story/mine。应先核冻结caller归属再决定是否补登记或扩展Hook面。E011/E012/E013属于其它页家族，没有已证消费关系，不能充当本页协议或样式证据。story_kotlin的absent仅是登记规则下未观察到，保持candidate边界。

建议：先补登记 story/mine 侧 MOSS 协议清单并确认实际调用边归属路径，再决定是否把 Kotlin MOSS 通道纳入覆盖范围；在确认调用边归属前不新增针对 absent 族的 Hook 目标。

替代解释与边界：若 protocol_evidence 能证明 StoryMoss 或 KMineMoss 的调用边来自 story/mine 家族自身类，则当前“未登记缺口”可升级为已确认消费面；反之若确认调用边均来自其它家族，则本页协议面确为空而非漏登记。

证据：E009, E010

## 后续补证

- 优先用精确pinned源码补齐关键定位器/安装器与公共注册契约的正文证据；按文件SHA和选中行范围记录实际读取覆盖。
- 利用已有冻结invoke_edges按唯一方法签名和caller家族核对协议消费，禁止定义数减边数或相除推断覆盖率。
- 如需解释资源差异，继续定位resources.arsc内部变化entry与页面引用；外层文件路径已经明确。
- 未登记宿主UI、服务端视觉变体、宽屏/平板路由和运行启用仍是边界；在授权设备上分别核安装、调用与效果。

## 原始证据与账务

本附件只含更正文档、原公共 AI 记录和哈希来源，不含 APK、DEX 或私有源码正文。大静态证据不重复打包，沿用原 Release 的 evidence.zip；其 17 个成员 SHA 清单保存在 original-evidence-manifest.json。
- 原 evidence.zip SHA-256：`sha256:43565ce175e7bb3c6985f93fbcc010e8a75c735a2e1a2d6c899d93943b291e8f`。
- 逐条更正见 corrections.json；完整更正结果见 corrected-ai-analysis.json；原 draft/review/analysis/checkpoint/evidence 均在 original-ai/ 保留。
- 原始模型 review 的 remaining_gaps 为历史记录，未改写为 Codex 结论；本更正版当前边界以上文及 codex_review.remaining_boundaries 为准。
