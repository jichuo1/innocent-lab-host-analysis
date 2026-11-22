# HostLab `advanced` — MeguvizDexDash 1.2.2 Integration & Remote CI Quantitative Benchmark

## 1. Overview & Pinned Provenance

The `advanced` branch of `jichuo1/innocent-lab-host-analysis` (branched cleanly from `origin/main` `d872f2faf5d61e70b422231803884b47670595da`) replaces legacy DEX/APK analysis dependencies across standard batch, single-command query/decode/refs/info, and full static audit workflows with **MeguvizDexDash `1.2.2`** while keeping `origin/main` untouched and preserving rule identity (`tools/hostlab/surface_workers.py` remains byte-identical to `d872f2faf5d61e70b422231803884b47670595da`).

| Component | Pinned Reference / Identity | Verification Status |
|---|---|---|
| Engine source | `https://github.com/Meguvizarchic/MeguvizDexDash.git` @ `6f0d5ce47680628ee9c51bfcc8a9157d9641c0ec` (`1.2.2`, dialect `dexsql-0.1.0`) | `Native build and conformance` Run [`45035735613`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/45035735613) (Ubuntu 3m54s, Windows 7m43s) & `Desktop workbench` Run [`45035735618`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/45035735618) (Ubuntu 8m47s, Windows 16m0s) — all green |
| Linux `x86_64` `build_id` | `source-sha256:d10a00fb9fa5ea1db35e15d3e4b6410cbd67cfb7fb2b99bb0f60855212e28164` | Verified in binary `version` + `capabilities` checks in CI (binary SHA-256 `0d1a03bf130c47e06e342c01b8fb9ee0321e3c3a7b6807008ab1f4c2c3a76973`) |
| Windows `AMD64` `build_id` | `source-sha256:77040b4091ab6f0c0fc0742962bef24219354305344cb12364af7241c6f6c450` | Deterministic `build.rs` LF digest verified for pinned commit `6f0d5ce47680` |
| Darwin `arm64` `build_id` | `source-sha256:f337ed538e72e6e601bf282e1ad3df5102b824395010f27b847abfcae0ad9252` | Deterministic `build.rs` LF digest verified for pinned commit `6f0d5ce47680` |
| HostLab `advanced` code SHA | `92730af035bc0e90490f1e1facdee253f7942189` (base `d872f2faf5d61e70b422231803884b47670595da`) | `Analysis tooling tests` Run [`45037458245`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45037458245) — 54s green |
| Reference audit baseline | `d872f2faf5d61e70b422231803884b47670595da` (`dexsql 0.1.0` + `run_intake.py` + `home_frame_audit.py`) | Executed side-by-side in fresh serial processes on Ubuntu 24.04 (`Linux-7.0.0-1014-aws-x86_64-with-glibc2.39`, 4 vCPU) |

---

## 2. Dependency Replacement Summary

| Path / Workflow | Legacy Dependencies (`main`) | `advanced` Replacement |
|---|---|---|
| Full audit (`audit`, `multipath_audit`) structural + surface extraction | External `dexsql 0.1.0` binary + `native_cli.py` interactive sentinel text protocol | `meguvizdexdash serve --dialect dexsql-0.1.0 --non-scalar-text lossy-replacement` via `mdd_session.py` (`mdd.cli-stream.v1` JSONL + typed B1 batches, persistent writer thread, `struct.pack` UTF-16 decode) |
| Full audit intake & home-frame gates | Redundant full-archive pure-Python DEX parsing in `analysis/run_intake.py` + `analysis/home_frame_audit.py` subprocesses | `mdd_gates.py` (`gate_mode: "mdd_fact_reuse"`), reusing the open verified `B1Session`, stat-verified single-slot `ZipArchiveSliceReader`, and combined `TAB_DATA`/`TAB_ITEM` probe query |
| Structural & surface rule queries (`native_graph.py`, `native_surface.py`) | 5×38-DEX `per_file` query loops (`lower(...)`, `JOIN class_methods`, small chunks) | Cross-DEX `all_files` queries for `classes`/protocol defs, descriptor-chunked `IN` scans for `class_fields`/`class_methods`, widened graph chunks (`400`), `methods` `method_kind IS NOT NULL` direct projection, while keeping `method_calls` streaming `per_file` to cap peak RSS |
| Full audit Java / JDK / JADX requirement | `plan_ci.py` provisioned JDK 17 + `install_jadx.py` even for native audits | `plan_ci.py` sets `needs_java=false` for `audit`, `multipath_audit`, `batch`, `batch_group`, and `backend_validation` with `native_reference` or `jadx=false`; JADX/Java only prepared for `decompile` or legacy fallback |
| Batch & single-command MCP (`analysis_batch.py`, `dexq_cli.py`, `remote_job.py`, `remote_mcp.py`, `host-analysis.yml`) | `dexsql 0.1.0` (`--threads` + MCP) or `dexq/server.py` (`androguard 4.1.4` + SQLite) | Defaults to `meguvizdexdash mcp --dialect dexsql-0.1.0 --non-scalar-text lossy-replacement`; legacy `"dexsql"` request specs map onto `"meguvizdexdash"` while `"sqlite"` remains available for explicit equivalence/legacy checks |
| Query-only runtime isolation (`dexq/server.py`) | Top-level `from loguru import logger` failed when `requirements-query.txt` excluded `androguard`/`loguru` | Optional `loguru` import at module load (`try/except ModuleNotFoundError`), allowing `requirements-query.txt` validation runs with zero `androguard` installed |

> [!NOTE]
> While validating Experiment 2 on real host APK `9200300` (~257 MiB), `mdd-mcp` uncovered a real non-scalar UTF-16 literal in `method_strings.value` (`non_scalar_UTF16_cannot_be_plain_UTF8`). We resolved the root cause in `MeguvizDexDash` commit `0ecc13aa96514f8517729551a6978390dd9b56b9` by adding `--non-scalar-text` policy plumbing (default `reject`, opt-in `lossy-replacement`) to `mdd-mcp` and `mdd-cli mcp`.

---

## 3. Experiment 1: Full Audit Equivalence & Performance (`reference_native` vs `meguvizdexdash 1.2.2`)

- **Workflow Run**: [`45038632260`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45038632260) (`hostlab-5ee04d66ab834a27a63a6e3f205c6e24`, 7m56s, zero Java, zero Androguard (`requirements-query.txt`), warm `MeguvizDexDash 1.2.2` cache `hostlab-mdd-v1-Linux-X64-1.2.2-6f0d5ce47680`, runner `Linux-7.0.0-1014-aws-x86_64-with-glibc2.39`)
- **Samples**:
  - Target (`9200300`): SHA-256 `609003767fbbfe4870d6bcbd8cea0292833327c4eef6513eb7388852be070bcc` (257,273,718 bytes)
  - Baseline (`9200200`): SHA-256 `47cd74d4a709baa903a3716d7708fe2a6bf85d6b29224c6c93cfacb77b7c314b` (257,286,006 bytes)
- **Methodology**: 2 rounds × 2 samples = 4 paired serial comparisons in alternating execution order (`reference_native` vs `meguvizdexdash`), fresh processes per worker, shared fetched APKs on runner.

### 3.1 Equivalence Verification

- `complete`: `true`
- `tools_reverified`: `true`, `reference_reverified`: `true`
- **All 4 round comparisons**: `all_equal = true` across all **20 / 20** evidence groups per sample (`home_probe_sha256`, 27 `features`, `discoveries`, `gates`, `class_records` 21,842, `invoke_edges` 109,493, `protocol_definitions` 5,926, `protocol_twins` 47, `unclassified_protocol_callers` 1,668, `resource_fingerprints` 17,754, etc.).
- **All 3 `pair_checks`** (`9200200` -> `9200300` diff & verdict):
  - `changes`: `equal = true`, `count = 105`, SHA-256 `eb5c988dd8837fd85715f0bb2726192ad43094785e32159ddc82c50d65f71404`
  - `resource_changes`: `equal = true`, `count = 4`, SHA-256 `230b721a58d70b3370e5ed352f2ea080c92595b361ebcf1e36ca2d62746d7f0d`
  - `verdict`: `equal = true`, `count = 2`, SHA-256 `2f8990c0025706d9470e82fb01764868369e69b49400d611faf0f8f4f4156953`

### 3.2 Per-Run Latency, Phase Breakdown, CPU & Memory Footprint

| Round & Sample | Engine | Elapsed (ms) | `prepare_ms` | `structural_ms` | `surface_ms` | `gate_ms` | Total CPU (s) | Tree RSS Peak (MiB) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| R1 target (`9200300`) | `reference_native` | 76,317.45 | 1,327.27 | 11,821.54 | 46,395.15 | *(16,434.51 residual)* | 103.77 | 1,246.62 |
| R1 target (`9200300`) | `meguvizdexdash` | 29,946.37 | 13,508.30 | 1,060.67 | 8,146.89 | 6,226.08 | 51.08 | 1,730.08 |
| R1 baseline (`9200200`) | `meguvizdexdash` | 29,620.07 | 13,425.45 | 1,036.44 | 7,984.68 | 6,169.29 | 50.72 | 1,700.39 |
| R1 baseline (`9200200`) | `reference_native` | 75,911.56 | 1,336.81 | 11,450.24 | 46,593.91 | *(16,186.09 residual)* | 103.22 | 1,245.60 |
| R2 target (`9200300`) | `meguvizdexdash` | 29,556.36 | 13,320.75 | 1,017.52 | 8,006.72 | 6,207.16 | 50.30 | 1,759.13 |
| R2 target (`9200300`) | `reference_native` | 77,279.08 | 1,346.14 | 12,374.13 | 46,885.32 | *(16,322.85 residual)* | 105.55 | 1,252.96 |
| R2 baseline (`9200200`) | `reference_native` | 75,814.02 | 1,347.69 | 11,519.81 | 46,535.03 | *(16,063.21 residual)* | 103.21 | 1,261.25 |
| R2 baseline (`9200200`) | `meguvizdexdash` | 29,936.33 | 13,608.09 | 1,041.00 | 8,052.85 | 6,233.84 | 51.10 | 1,709.79 |

> *(Reference residual gate cost = `audit_and_shared_scan_ms - prepare_ms - structural_ms - surface_ms`, representing standalone `run_intake.py` + `home_frame_audit.py` execution and subprocess teardown.)*

### 3.3 Experiment 1 Aggregated Comparison (4-Run Means)

| Metric | `reference_native` (`dexsql 0.1.0`) Mean | `meguvizdexdash 1.2.2` (`6f0d5ce4`) Mean | Delta / Speedup |
|---|---:|---:|---|
| Total worker `elapsed_ms` | 76,330.53 ms (76.33 s) | **29,764.78 ms (29.76 s)** | **2.56x faster (-61.0%)** |
| Snapshot `prepare_ms` | 1,339.48 ms | 13,465.65 ms | Eager parallel table + Bloom build upfront |
| Structural rules `structural_ms` | 11,791.43 ms | **1,038.91 ms** | **11.35x faster (-91.2%)** |
| Surface scan `surface_ms` | 46,602.35 ms | **8,047.79 ms** | **5.79x faster (-82.7%)** |
| Intake + Home gates | ~16,251.66 ms (`run_intake` + `home_frame_audit`) | **6,209.09 ms** (`mdd_gates`) | **2.62x faster (-61.8%)** |
| Total CPU time (`user + sys`) | 103.94 s | **50.80 s** | **2.05x less CPU (-51.1%)** |
| Process tree RSS peak | **1,251.61 MiB** | **1,724.85 MiB** | **-120.98 MiB vs `0ecc13aa` AWS** / **-775.35 MiB (-31.0%) vs `55957094`** |

### 3.4 Experiment 1 Multi-Stage Progression & Memory Recovery

| Metric (4-Run Mean) | `0ecc13aa` AWS ([`44987139478`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44987139478)) | `e0358934` Azure ([`45017371825`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45017371825)) | `55957094` AWS ([`45032244408`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45032244408)) | `6f0d5ce4` AWS ([`45038632260`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45038632260)) | Net Change (`0ecc13aa` -> `6f0d5ce4` AWS / `55957094` -> `6f0d5ce4`) |
|---|---:|---:|---:|---:|---|
| Total `elapsed_ms` | 30,352.61 ms (2.43x) | 40,507.56 ms (2.42x) | 30,102.25 ms (2.56x) | **29,764.78 ms (2.56x)** | **-587.83 ms (-1.9%)** / **-337.47 ms (-1.1%)** |
| `structural_ms` | 1,415.76 ms (7.89x) | 1,332.98 ms (10.46x) | 1,078.47 ms (11.22x) | **1,038.91 ms (11.35x)** | **-376.85 ms (-26.6%)** / **-39.56 ms (-3.7%)** |
| `surface_ms` | 8,486.24 ms (5.27x) | 11,992.27 ms (4.80x) | 8,511.45 ms (5.52x) | **8,047.79 ms (5.79x)** | **-438.45 ms (-5.2%)** / **-463.66 ms (-5.4%)** |
| `gate_ms` | 6,194.52 ms (2.59x) | 9,390.51 ms (2.61x) | 5,989.47 ms (2.72x) | **6,209.09 ms (2.62x)** | **+14.57 ms (+0.2%)** |
| Tree RSS peak | 1,845.83 MiB | 1,967.62 MiB | 2,500.20 MiB | **1,724.85 MiB** | **-120.98 MiB (-6.6%)** / **-775.35 MiB (-31.0%)** |

> [!IMPORTANT]
> Comparing `55957094` against `6f0d5ce4` on identical `Linux-7.0.0-1014-aws-x86_64` hardware highlights why memory-path verification matters: `55957094` spiked `tree_rss_peak_mib` to `2,500.20 MiB` (+654 MiB over `0ecc13aa`) because `SelectedScope` still called `source.lease()` (materializing the 257 MiB spilled APK back into heap RAM), `lazy.rs` spawned a 3-worker reorder buffer (~10 concurrent threads + 3 in-flight DEX builds), `reset_sqlite_connection` omitted `PRAGMA shrink_memory;`, `ValueIndex` LRU cached 192 MiB, and `method_calls` aggregated 109,493 rows across all 38 DEXes in one response. Fixing all four in `6f0d5ce4` / `92730af` recovered **775.35 MiB (-31.0%)** to **1,724.85 MiB** while simultaneously setting the fastest wall clock yet (**29.76 s**, `structural` **11.35x**, `surface` **5.79x**).

*(Note: `sampled_cgroup_memory_peak_bytes` is container-lifetime monotonic on Linux cgroup v2 and therefore rises across sequential runs from 3,238 MiB to 4,018 MiB for `reference_native` and 4,476 MiB to 5,224 MiB for `meguvizdexdash`; process-tree `sampled_tree_rss_peak_bytes` measures each fresh isolated worker tree accurately.)*

---

## 4. Experiment 2: MCP Query / Decode / Refs / Manifest Equivalence & Performance (`sqlite / Androguard 4.1.4` vs `meguvizdexdash 1.2.2 mcp`)

- **Latest Workflow Run (`6f0d5ce4`)**: [`45037625807`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45037625807) (`hostlab-c7e2a05063904039b479c981dd25eead`, 10m12s, `jadx: false`)
- **Intermediate 3-Wave Run (`55957094`)**: [`45031466279`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45031466279) (`hostlab-ed0979115f444805842bfda5b9818fd0`, 8m9s, AWS-class fast runner)
- **Sample**: `9200300` (`609003767fbbfe4870d6bcbd8cea0292833327c4eef6513eb7388852be070bcc`, 257,273,718 bytes)
- **Methodology**: 2 alternating serial MCP sessions (`meguvizdexdash` vs `sqlite`) covering class/method/field lookup, string literal references (`method_strings`), duplicate-task memoization (`string_reused`), caller refs (`method_calls`), field access refs (`method_field_accesses`), type usage refs (`method_used_types`), method Smali decode, and AndroidManifest summary.

### 4.1 Equivalence Verification

- `result_multisets_equal`: **`true`**
- Identical canonical row counts & SHA-256 digests across all 4 sessions (`class`: 1 row `25d7a991...`, `methods`: 3 rows `1e977f92...`, `fields`: 1 row `1793dd85...`, `string`: 1 row `bbecf37f...`, `callers`: 19 rows / 12 distinct `86b4276f...`, `field_refs`: 6 rows / 3 distinct `29cb3d66...`, `type_refs`: 109 rows / 107 distinct `9a1ba53d...`, `string_reused`: 1 row `reused_from="string"`), plus verified `smali` body (`internalGetUrls` / `unmodifiableMap`) and `manifest` identity (`tv.danmaku.bili`, `9200300`).

### 4.2 Latency Breakdown Across Cold & Warm Sessions (`6f0d5ce4` in Run `45037625807`)

| Phase / Task | SQLite R1 Cold Build (ms) | SQLite R2 Cache Hit (ms) | MeguvizDexDash R1 (ms) | MeguvizDexDash R2 (ms) | Speedup (MDD Avg vs Cold / Warm SQLite) |
|---|---:|---:|---:|---:|---|
| Session `prepare_ms` | 92,812.35 | 48.80 *(disk hit)* | 16,048.61 *(memory)* | 15,880.33 *(memory)* | **5.81x faster** vs cold build |
| `class` (`classes`) | 3.21 | 2.91 | **1.76** | **2.00** | **1.71x / 1.55x faster (avg 1.88 vs 3.06 ms)** |
| `methods` (`class_methods`) | 1.84 | 1.87 | **2.53** | **2.64** | **0.71x / 0.72x** (within 0.72 ms of SQLite; **9.1x vs `0ecc13aa`**) |
| `fields` (`class_fields`) | 1.82 | 1.78 | **1.55** | **1.59** | **1.16x / 1.13x faster (avg 1.57 vs 1.80 ms)** |
| `string` (`method_strings`) | 9,026.76 | 8,904.63 | **1.70** | **1.71** | **5,287x / 5,216x faster** |
| `callers` (`method_calls`) | 6,058.60 | 6,138.83 | **10.00** | **9.46** | **623x / 631x faster** |
| `field_refs` (`method_field_accesses`) | 3,779.22 | 3,915.23 | **3.85** | **4.32** | **925x / 958x faster** |
| `type_refs` (`method_used_types`) | 121,726.55 | 121,822.53 | **46.97** | **46.95** | **2,592x / 2,594x faster** |
| `smali` (`decode`) | 2,042.81 | 2,152.39 | **119.15** | **114.44** | **17.49x / 18.43x faster** (**44.8x vs `0ecc13aa`**) |
| `manifest` (`get_manifest`) | 503.01 | 510.43 | **5.97** | **5.63** | **86.7x / 88.0x faster** |
| `string_reused` | 0.03 | 0.03 | 0.04 | 0.04 | Semantic memo reuse |
| **Total `total_ms`** | **237,643.45 (237.64 s)** | **145,148.34 (145.15 s)** | **16,546.37 (16.55 s)** | **16,371.02 (16.37 s)** | **14.44x vs cold SQLite / 8.82x vs warm SQLite** |

*(Note: `verify_backends.py` does not attach `runner_resources` RSS telemetry to `verification.json` in Experiment 2. Because `45037625807` ran on a slower VM than `45031466279` where same-run cold SQLite took `237.64 s` vs `178.03 s` [+33.5%], normalized speedup vs SQLite is the consistent cross-run metric while absolute latencies from AWS-class `45031466279` are also listed below.)*

---

## 5. Multi-Stage Optimization Progression (`0ecc13aa` -> `5c2df441` -> `e0358934` -> `55957094` -> `6f0d5ce4`)

Across four follow-up optimization cycles after initial Experiment 2 baseline `0ecc13aa`, all three targeted optimization waves plus the memory-recovery pass delivered cumulative gains:

1. **Wave 1 — Streaming & spilled APK snapshot (`crates/mdd-input`)**: Streamed archives >16 MiB to unlinked/private temporary files with direct range reads, avoiding holding a full 257 MiB APK heap buffer, and fixed `SelectedScope` to hold `RetainedLease::Source(CapturedSource)` so spilled snapshots are never materialized back into RAM on `Dataset::open`.
2. **Wave 2 — Columnar & SQL fast paths (`crates/mdd-dex`, `mdd-facts`, `mdd-sql`, `mdd-wire`, `mdd-service`)**:
   - `RefTable` direct `LIKE` fast path + `Chunk` bitset min/max pruning + per-DEX blocked `U32Bloom` filters + direct `AND` predicate pushdown expansion;
   - `TextDict` `ValueIndex` LRU (bounded to `96 MiB`) with `IndexSlice` lifetime safety;
   - `SqlBridge` cached `PreparedSchema` & reusable SQLite connection (`PRAGMA shrink_memory;` on recycle), direct `COUNT(*) GROUP BY` & equality/`IN`/`ORDER BY`, zero-TEMP expansion bypass;
   - Single-pass `non_scalar_text_gap`, `for_each_annotation*` zero-Vec scans, `ValidatedCodeMeta` `Arc<[u32]>` sharing, and single-pass UTF-8 `BatchStreamEncoder` escaping;
   - Single-loader `sync_channel(0)` + `lazy.dict.shrink_to_fit()` pipeline avoiding 4-vCPU oversubscription.
3. **Wave 3 — Decode & MCP latency (`crates/mdd-service`, `crates/mdd-mcp`)**: `SingleMethodDecoder` lazy single-DEX fast path + zero-annotation skip (`decode.rs`), spill-safe `input_bytes`, and persistent pooled deadline worker (`mdd-mcp`).

| Experiment 2 Task (R1 / R2 ms) | Baseline `0ecc13aa` ([`44986457292`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44986457292)) | Round 1 `5c2df441` ([`45009513926`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45009513926)) | Round 2 `e0358934` ([`45016455209`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45016455209)) | Wave 1–3 AWS `55957094` ([`45031466279`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45031466279)) | Final + Mem Fix `6f0d5ce4` ([`45037625807`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/45037625807)) |
|---|---:|---:|---:|---:|---|
| `class` (`classes`) | 6.79 / 6.53 | 2.76 / 3.07 | 2.74 / 2.07 | **1.83 / 1.57** *(1.58x vs SQLite)* | **1.76 / 2.00** (**1.71x / 1.55x vs SQLite**) |
| `methods` (`class_methods`) | 23.63 / 23.31 | 4.07 / 3.85 | 2.24 / 2.03 | **1.80 / 1.72** *(0.94x vs SQLite)* | **2.53 / 2.64** (9.1x vs `0ecc13aa`) |
| `fields` (`class_fields`) | 30.99 / 29.72 | 2.09 / 2.19 | 2.05 / 1.14 | **1.01 / 0.96** *(1.50x vs SQLite)* | **1.55 / 1.59** (**1.16x / 1.13x vs SQLite**) |
| `string` (`method_strings`) | 9.18 / 8.89 | 3.11 / 2.99 | 2.62 / 1.95 | **1.29 / 1.37** *(4,945x vs SQLite)* | **1.70 / 1.71** (**5,287x vs SQLite**) |
| `callers` (`method_calls`) | 99.94 / 98.67 | 8.46 / 7.94 | 6.82 / 6.35 | **6.42 / 6.01** *(696x vs SQLite)* | **10.00 / 9.46** (**623x vs SQLite**) |
| `field_refs` (`method_field_accesses`) | 59.62 / 53.29 | 4.27 / 4.37 | 3.03 / 2.97 | **2.65 / 2.77** *(1,016x vs SQLite)* | **3.85 / 4.32** (**925x vs SQLite**) |
| `type_refs` (`method_used_types`) | 52.90 / 51.97 | 29.81 / 30.32 | 29.46 / 29.19 | **28.23 / 29.30** *(3,240x vs SQLite)* | **46.97 / 46.95** (**2,592x vs SQLite**) |
| `smali` (`decode`) | 5,287.57 / 5,168.07 | 96.83 / 100.11 | 101.70 / 102.12 | **128.73 / 104.84** *(12.5x / 13.7x)* | **119.15 / 114.44** (**17.5x / 18.4x vs SQLite**) |
| `manifest` (`get_manifest`) | 6.81 / 6.76 | 4.97 / 6.41 | 6.98 / 5.30 | **6.74 / 5.49** *(55.1x / 55.6x)* | **5.97 / 5.63** (**86.7x / 88.0x vs SQLite**) |
| **Session `total_ms`** | 21,589.26 / 21,037.03 | 13,836.26 / 14,200.96 | 14,562.22 / 13,985.03 | **13,915.53 / 13,585.01** *(12.95x / 8.06x)* | **16,546.37 / 16,371.02** (**14.44x / 8.82x vs SQLite**) |
