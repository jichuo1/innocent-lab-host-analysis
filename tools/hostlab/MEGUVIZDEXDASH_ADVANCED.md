# HostLab `advanced` — MeguvizDexDash 1.2.2 Integration & Remote CI Quantitative Benchmark

## 1. Overview & Pinned Provenance

The `advanced` branch of `jichuo1/innocent-lab-host-analysis` (branched cleanly from `origin/main` `d872f2faf5d61e70b422231803884b47670595da`) replaces legacy DEX/APK analysis dependencies across standard batch, single-command query/decode/refs/info, and full static audit workflows with **MeguvizDexDash `1.2.2`** while keeping `origin/main` untouched and preserving rule identity (`tools/hostlab/surface_workers.py` remains byte-identical to `d872f2faf5d61e70b422231803884b47670595da`).

| Component | Pinned Reference / Identity | Verification Status |
|---|---|---|
| Engine source | `https://github.com/Meguvizarchic/MeguvizDexDash.git` @ `e0358934620aa82091178febb1a2ce6c7abad9db` (`1.2.2`, dialect `dexsql-0.1.0`) | `Native build and conformance` Run [`45014820025`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/45014820025) (Ubuntu 4m45s, Windows 7m2s) & `Desktop workbench` Run [`45014820019`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/45014820019) (Ubuntu 8m52s, Windows 16m24s) — all green |
| Linux `x86_64` `build_id` | `source-sha256:cc96e38c446778ad931f730b8cb18e8751126ff3cf1348a047f58a233d517c76` | Verified in binary `version` + `capabilities` checks in CI (binary SHA-256 `a4466f6e8c964e9a4d54157db56139bf2ac55e140d54a09b00a4d6731a7afe51`) |
| Windows `AMD64` `build_id` | `source-sha256:6e956db9b5a919f28b2d96d66c5aead58974fdc7dc62f3cb63ad007e8581ca70` | Deterministic `build.rs` LF digest verified for pinned commit `e0358934620a` |
| Darwin `arm64` `build_id` | `source-sha256:17d8c8191bfead3921753400316a8b0bb4c60abe09d9ca0160683012877d02a5` | Deterministic `build.rs` LF digest verified for pinned commit `e0358934620a` |
| HostLab `advanced` code SHA | `01f20f981ff0fb3c9b1731013ec5fb854b57d9c2` (base `d872f2faf5d61e70b422231803884b47670595da`) | `Analysis tooling tests` Run [`45016305114`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45016305114) — 47s green |
| Reference audit baseline | `d872f2faf5d61e70b422231803884b47670595da` (`dexsql 0.1.0` + `run_intake.py` + `home_frame_audit.py`) | Executed side-by-side in fresh serial processes on Ubuntu 24.04 (`Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`, 4 vCPU; initial `0ecc13aa` Experiment 1 run [`44987139478`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44987139478) ran on `Linux-7.0.0-1014-aws-x86_64-with-glibc2.39`) |

---

## 2. Dependency Replacement Summary

| Path / Workflow | Legacy Dependencies (`main`) | `advanced` Replacement |
|---|---|---|
| Full audit (`audit`, `multipath_audit`) structural + surface extraction | External `dexsql 0.1.0` binary + `native_cli.py` interactive sentinel text protocol | `meguvizdexdash serve --dialect dexsql-0.1.0 --non-scalar-text lossy-replacement` via `mdd_session.py` (`mdd.cli-stream.v1` JSONL + typed B1 batches) |
| Full audit intake & home-frame gates | Redundant full-archive pure-Python DEX parsing in `analysis/run_intake.py` + `analysis/home_frame_audit.py` subprocesses | `mdd_gates.py` (`gate_mode: "mdd_fact_reuse"`), reusing the already-open verified `B1Session` + bounded central-directory slice reads (`ZipArchiveSliceReader`) |
| Full audit Java / JDK / JADX requirement | `plan_ci.py` provisioned JDK 17 + `install_jadx.py` even for native audits | `plan_ci.py` sets `needs_java=false` for `audit`, `multipath_audit`, `batch`, `batch_group`, and `backend_validation` with `native_reference` or `jadx=false`; JADX/Java only prepared for `decompile` or legacy fallback |
| Batch & single-command MCP (`analysis_batch.py`, `dexq_cli.py`, `remote_job.py`, `remote_mcp.py`, `host-analysis.yml`) | `dexsql 0.1.0` (`--threads` + MCP) or `dexq/server.py` (`androguard 4.1.4` + SQLite) | Defaults to `meguvizdexdash mcp --dialect dexsql-0.1.0 --non-scalar-text lossy-replacement`; legacy `"dexsql"` request specs map onto the canonical `"meguvizdexdash"` native engine while `"sqlite"` stays available for explicit equivalence/legacy calls |
| Query-only runtime isolation (`dexq/server.py`) | Top-level `from loguru import logger` failed when `requirements-query.txt` excluded `androguard`/`loguru` | Optional `loguru` import at module load (`try/except ModuleNotFoundError`), allowing `requirements-query.txt` validation runs with zero `androguard` installed |

> [!NOTE]
> While validating Experiment 2 on real host APK `9200300` (~257 MiB), `mdd-mcp` uncovered a real non-scalar UTF-16 literal in `method_strings.value` (`non_scalar_UTF16_cannot_be_plain_UTF8`). We resolved the root cause in `MeguvizDexDash` commit `0ecc13aa96514f8517729551a6978390dd9b56b9` by adding `--non-scalar-text` policy plumbing (default `reject`, opt-in `lossy-replacement`) to `mdd-mcp` and `mdd-cli mcp`.

---

## 3. Experiment 1: Full Audit Equivalence & Performance (`reference_native` vs `meguvizdexdash 1.2.2`)

- **Workflow Run**: [`45017371825`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45017371825) (`hostlab-e9e0ddaf6cdb4b17931c0ddbc527918a`, 10m22s, zero Java, zero Androguard (`requirements-query.txt`), warm `MeguvizDexDash 1.2.2` cache `hostlab-mdd-v1-Linux-X64-1.2.2-e0358934620a`, runner `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`)
- **Samples**:
  - Target (`9200300`): SHA-256 `609003767fbbfe4870d6bcbd8cea0292833327c4eef6513eb7388852be070bcc` (257,273,718 bytes)
  - Baseline (`9200200`): SHA-256 `47cd74d4a709baa903a3716d7708fe2a6bf85d6b29224c6c93cfacb77b7c314b` (257,286,006 bytes)
- **Methodology**: 2 rounds × 2 samples = 4 paired serial comparisons in alternating execution order (`reference_native` vs `meguvizdexdash`), fresh processes per worker, shared fetched APKs on runner.

### 3.1 Equivalence Verification

- `complete`: `true`
- `tools_reverified`: `true`, `reference_reverified`: `true`
- **All 4 round comparisons**: `all_equal = true` across all **20 / 20** evidence groups per sample (`home_probe_sha256`, 27 `features`, `discoveries`, `gates`, `class_records`, `invoke_edges`, `protocol_definitions`, `protocol_twins`, `unclassified_protocol_callers`, resource fingerprints, etc.).
- **All 3 `pair_checks`** (`9200200` -> `9200300` diff & verdict):
  - `changes`: `equal = true`, `count = 105`, SHA-256 `eb5c988dd8837fd85715f0bb2726192ad43094785e32159ddc82c50d65f71404`
  - `resource_changes`: `equal = true`, `count = 4`, SHA-256 `230b721a58d70b3370e5ed352f2ea080c92595b361ebcf1e36ca2d62746d7f0d`
  - `verdict`: `equal = true`, `count = 2`, SHA-256 `2f8990c0025706d9470e82fb01764868369e69b49400d611faf0f8f4f4156953`

### 3.2 Per-Run Latency, Phase Breakdown, CPU & Memory Footprint

| Round & Sample | Engine | Elapsed (ms) | `prepare_ms` | `structural_ms` | `surface_ms` | `gate_ms` | Total CPU (s) | Tree RSS Peak (MiB) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| R1 target (`9200300`) | `reference_native` | 97,413.54 | 1,737.04 | 14,133.75 | 57,295.98 | *(23,781.68 residual)* | 134.47 | 1,256.86 |
| R1 target (`9200300`) | `meguvizdexdash` | 40,468.92 | 16,238.75 | 1,335.30 | 11,997.48 | 9,330.07 | 65.96 | 1,899.08 |
| R1 baseline (`9200200`) | `meguvizdexdash` | 40,384.79 | 16,148.53 | 1,328.14 | 11,914.51 | 9,459.46 | 66.03 | 1,929.64 |
| R1 baseline (`9200200`) | `reference_native` | 99,491.96 | 1,745.55 | 14,202.09 | 58,618.59 | *(24,455.74 residual)* | 136.83 | 1,237.99 |
| R2 target (`9200300`) | `meguvizdexdash` | 40,621.45 | 16,121.46 | 1,339.39 | 12,123.49 | 9,399.69 | 66.07 | 2,011.71 |
| R2 target (`9200300`) | `reference_native` | 96,723.19 | 1,759.24 | 13,918.07 | 57,129.06 | *(23,449.63 residual)* | 133.20 | 1,252.58 |
| R2 baseline (`9200200`) | `reference_native` | 99,133.01 | 1,728.46 | 13,529.09 | 57,224.47 | *(26,177.22 residual)* | 135.64 | 1,242.19 |
| R2 baseline (`9200200`) | `meguvizdexdash` | 40,555.06 | 16,367.08 | 1,329.10 | 11,933.61 | 9,372.82 | 66.05 | 2,030.05 |

> *(Reference residual gate cost = `audit_and_shared_scan_ms - prepare_ms - structural_ms - surface_ms`, representing standalone `run_intake.py` + `home_frame_audit.py` execution and subprocess teardown.)*

### 3.3 Experiment 1 Aggregated Comparison (4-Run Means)

| Metric | `reference_native` (`dexsql 0.1.0`) Mean | `meguvizdexdash 1.2.2` (`e0358934`) Mean | Delta / Speedup |
|---|---:|---:|---|
| Total worker `elapsed_ms` | 98,190.42 ms (98.19 s) | **40,507.56 ms (40.51 s)** | **2.42x faster (-58.7%)** |
| Snapshot `prepare_ms` | 1,742.57 ms | 16,218.96 ms | Eager parallel table + Bloom build upfront |
| Structural rules `structural_ms` | 13,945.75 ms | **1,332.98 ms** | **10.46x faster (-90.4%)** |
| Surface scan `surface_ms` | 57,567.03 ms | **11,992.27 ms** | **4.80x faster (-79.2%)** |
| Intake + Home gates | ~24,466.07 ms (`run_intake` + `home_frame_audit`) | **9,390.51 ms** (`mdd_gates`) | **2.61x faster (-61.6%)** |
| Total CPU time (`user + sys`) | 135.04 s | **66.03 s** | **2.05x less CPU (-51.1%)** |
| Process tree RSS peak | **1,247.40 MiB** | 1,967.62 MiB | +720.22 MiB (+57.7%) in-memory SoA + Bloom tradeoff within 16 GiB CI RAM |

> [!NOTE]
> Initial `0ecc13aa` Experiment 1 (Run [`44987139478`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44987139478)) ran on faster AWS VM hardware (`Linux-7.0.0-1014-aws-x86_64`, where `reference_native` averaged `73,625.04 ms` and `0ecc13aa` averaged `30,352.61 ms` / `1,845.83 MiB` RSS peak). On the `1017-azure` runner of Run `45017371825`, the immutable `reference_native` baseline slowed by +33.4% to `98,190.42 ms`, while `e0358934` kept the same `2.42x` overall speedup (`40,507.56 ms`), improved `structural_ms` even in absolute ms (`1,332.98 ms` vs AWS `1,415.76 ms`, expanding from `7.89x` to `10.46x` faster than `reference_native`), reduced relative CPU ratio further (`1.98x` -> `2.05x`), and increased tree RSS peak by `+121.79 MiB (+6.6%)` (`1,967.62 MiB` vs `1,845.83 MiB`) to hold `RefTable` + per-DEX Bloom filters + cached bridge schemas.

*(Note: `sampled_cgroup_memory_peak_bytes` is container-lifetime monotonic on Linux cgroup v2 and therefore rises across sequential runs from 3,139 MiB to 3,919 MiB for `reference_native` and 4,276 MiB to 5,271 MiB for `meguvizdexdash`; process-tree `sampled_tree_rss_peak_bytes` measures each fresh isolated worker tree accurately.)*

---

## 4. Experiment 2: MCP Query / Decode / Refs / Manifest Equivalence & Performance (`sqlite / Androguard 4.1.4` vs `meguvizdexdash 1.2.2 mcp`)

- **Workflow Run**: [`45016455209`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45016455209) (`hostlab-ffec9ac6c9264c33a52f2c350583e6dc`, 8m17s, `jadx: false`)
- **Sample**: `9200300` (`609003767fbbfe4870d6bcbd8cea0292833327c4eef6513eb7388852be070bcc`, 257,273,718 bytes)
- **Methodology**: 2 alternating serial MCP sessions (`meguvizdexdash` vs `sqlite`) covering class/method/field lookup, string literal references (`method_strings`), duplicate-task memoization (`string_reused`), caller refs (`method_calls`), field access refs (`method_field_accesses`), type usage refs (`method_used_types`), method Smali decode, and AndroidManifest summary.

### 4.1 Equivalence Verification

- `result_multisets_equal`: **`true`**
- Identical canonical row counts & SHA-256 digests across all 4 sessions (`class`: 1 row `25d7a991...`, `methods`: 3 rows `1e977f92...`, `fields`: 1 row `1793dd85...`, `string`: 1 row `bbecf37f...`, `callers`: 19 rows / 12 distinct `86b4276f...`, `field_refs`: 6 rows / 3 distinct `29cb3d66...`, `type_refs`: 109 rows / 107 distinct `9a1ba53d...`, `string_reused`: 1 row `reused_from="string"`), plus verified `smali` body (`internalGetUrls` / `unmodifiableMap`) and `manifest` identity (`tv.danmaku.bili`, `9200300`).

### 4.2 Latency Breakdown Across Cold & Warm Sessions (`e0358934` in Run `45016455209`)

| Phase / Task | SQLite R1 Cold Build (ms) | SQLite R2 Cache Hit (ms) | MeguvizDexDash R1 (ms) | MeguvizDexDash R2 (ms) | Speedup (MDD Avg vs Cold / Warm SQLite) |
|---|---:|---:|---:|---:|---|
| Session `prepare_ms` | 68,698.95 | 36.47 *(disk hit)* | 14,180.75 *(memory)* | 13,634.72 *(memory)* | **4.94x faster** vs cold build |
| `class` (`classes`) | 2.50 | 2.44 | **2.74** | **2.07** | **1.04x / 1.01x faster (avg 2.40 vs 2.47 ms)** |
| `methods` (`class_methods`) | 1.47 | 1.51 | **2.24** | **2.03** | **0.69x / 0.71x** (within 0.65 ms of SQLite; **11.0x vs `0ecc13aa`**) |
| `fields` (`class_fields`) | 1.35 | 1.42 | **2.05** | **1.14** | **0.85x / 0.89x** (R2 beats SQLite; **19.0x vs `0ecc13aa`**) |
| `string` (`method_strings`) | 6,621.13 | 6,433.97 | **2.62** | **1.95** | **2,896x / 2,814x faster** |
| `callers` (`method_calls`) | 4,378.14 | 4,481.39 | **6.82** | **6.35** | **665x / 681x faster** |
| `field_refs` (`method_field_accesses`) | 2,784.08 | 2,926.62 | **3.03** | **2.97** | **929x / 976x faster** |
| `type_refs` (`method_used_types`) | 94,534.28 | 94,773.35 | **29.46** | **29.19** | **3,223x / 3,232x faster** |
| `smali` (`decode`) | 1,510.25 | 1,556.03 | **101.70** | **102.12** | **14.8x / 15.3x faster** (**51.3x vs `0ecc13aa`**) |
| `manifest` (`get_manifest`) | 331.65 | 338.00 | **6.98** | **5.30** | **54.0x / 55.0x faster** |
| `string_reused` | 0.02 | 0.02 | 0.04 | 0.04 | Semantic memo reuse |
| **Total `total_ms`** | **180,259.04 (180.26 s)** | **111,822.98 (111.82 s)** | **14,562.22 (14.56 s)** | **13,985.03 (13.99 s)** | **12.63x vs cold SQLite / 7.83x vs warm SQLite** |

*(Note: `verify_backends.py` does not attach `runner_resources` RSS telemetry to `verification.json` in Experiment 2.)*

---

## 5. Optimization Progression (`0ecc13aa` -> `5c2df441` -> `e0358934`)

Following Experiment 2 baseline analysis (`44986457292`), two targeted optimization rounds eliminated both bottlenecks where `MeguvizDexDash 1.2.2` initially trailed `SQLite / Androguard`:

1. **Single-DEX lazy Smali decode + zero-annotation skip** (`crates/mdd-service/src/decode.rs`): Instead of decoding the entire archive or building full-DEX `DexDecode` tables/annotations on a single-method `decode`, locate the target method/class across DEX headers, lazily parse only the matching DEX's `CodeItem` (reusing cached annotation stores and skipping annotation decoding entirely when a DEX/method has zero annotations), while preserving all MDD-042/071 structural decode semantics.
2. **Direct filtered columnar projection & SoA `RefTable`** (`crates/mdd-sql/src/column_store.rs`, `dialects/pushdown.rs`, `provider/hostlab/lazy.rs`): Answer single-table Equality/`IN`/`AND`/`ORDER BY` queries directly over compressed columnar + SoA `RefTable` slices without spawning per-query in-memory SQLite virtual-table connections.
3. **Per-DEX blocked 64-bit-word Bloom filters & `SqlBridge` schema cache** (`crates/mdd-sql/src/column_store.rs`, `bridge.rs`, `dialects/ast.rs`, `dialects/ast/rewrite.rs`, `temp.rs`): Attach compact 64-bit-word `U32Bloom` filters to each DEX's `RefTable` (skipping non-matching DEX partitions in ~1 cache-line load instead of scanning ~2.1M `method_name` / ~570K `type_desc` `u32` entries), cache validated `PreparedSchema` on `SqlBridge` (keyed by binding + relation visibility with deferred commit on valid prepare), and bypass `TempSqlSession` expansion overhead when zero TEMP definitions are active.

| Experiment 2 Task (R1 / R2 ms) | Baseline `0ecc13aa` ([`44986457292`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44986457292)) | Round 1 `5c2df441` ([`45009513926`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45009513926)) | Final `e0358934` ([`45016455209`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45016455209)) | Same-Run SQLite (`45016455209`) | Net Improvement (`0ecc13aa` -> `e0358934`) |
|---|---:|---:|---:|---:|---|
| `class` (`classes`) | 6.79 / 6.53 | 2.76 / 3.07 | **2.74 / 2.07** | 2.50 / 2.44 | **2.77x faster (-63.9%, beats SQLite avg)** |
| `methods` (`class_methods`) | 23.63 / 23.31 | 4.07 / 3.85 | **2.24 / 2.03** | 1.47 / 1.51 | **10.99x faster (-90.9%)** |
| `fields` (`class_fields`) | 30.99 / 29.72 | 2.09 / 2.19 | **2.05 / 1.14** | 1.35 / 1.42 | **19.03x faster (-94.7%, R2 beats SQLite)** |
| `string` (`method_strings`) | 9.18 / 8.89 | 3.11 / 2.99 | **2.62 / 1.95** | 6,621.13 / 6,433.97 | **3.95x faster (-74.7%)** |
| `callers` (`method_calls`) | 99.94 / 98.67 | 8.46 / 7.94 | **6.82 / 6.35** | 4,378.14 / 4,481.39 | **15.08x faster (-93.4%)** |
| `field_refs` (`method_field_accesses`) | 59.62 / 53.29 | 4.27 / 4.37 | **3.03 / 2.97** | 2,784.08 / 2,926.62 | **18.82x faster (-94.7%)** |
| `type_refs` (`method_used_types`) | 52.90 / 51.97 | 29.81 / 30.32 | **29.46 / 29.19** | 94,534.28 / 94,773.35 | **1.79x faster (-44.1%)** |
| `smali` (`decode`) | 5,287.57 / 5,168.07 | 96.83 / 100.11 | **101.70 / 102.12** | 1,510.25 / 1,556.03 | **51.30x faster (-98.1%, 15.0x vs SQLite)** |
| `manifest` (`get_manifest`) | 6.81 / 6.76 | 4.97 / 6.41 | **6.98 / 5.30** | 331.65 / 338.00 | **1.11x faster (-9.5%)** |
| **Session `total_ms`** | 21,589.26 / 21,037.03 | 13,836.26 / 14,200.96 | **14,562.22 / 13,985.03** | 180,259.04 / 111,822.98 | **1.49x faster (-33.0%, 12.6x / 7.8x vs SQLite)** |
