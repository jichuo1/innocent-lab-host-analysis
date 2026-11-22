# HostLab `advanced` — MeguvizDexDash 1.2.2 Integration & Remote CI Quantitative Benchmark

## 1. Overview & Pinned Provenance

The `advanced` branch of `jichuo1/innocent-lab-host-analysis` (branched cleanly from `origin/main` `d872f2faf5d61e70b422231803884b47670595da`) replaces legacy DEX/APK analysis dependencies across standard batch, single-command query/decode/refs/info, and full static audit workflows with **MeguvizDexDash `1.2.2`** while keeping `origin/main` untouched and preserving rule identity (`tools/hostlab/surface_workers.py` remains byte-identical to `d872f2faf5d61e70b422231803884b47670595da`).

| Component | Pinned Reference / Identity | Verification Status |
|---|---|---|
| Engine source | `https://github.com/Meguvizarchic/MeguvizDexDash.git` @ `0ecc13aa96514f8517729551a6978390dd9b56b9` (`1.2.2`, dialect `dexsql-0.1.0`) | `Native build and conformance` Run [`44985652932`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/44985652932) (Ubuntu 5m18s, Windows 9m20s) & `Desktop workbench` Run [`44985652863`](https://github.com/Meguvizarchic/MeguvizDexDash/actions/runs/44985652863) — all green |
| Linux `x86_64` `build_id` | `source-sha256:b1f590b763871e2ffe7a9080954981cb035cf40f05f2744a5a8d5cfcef782c1c` | Verified in binary `version` + `capabilities` checks in CI (`0dbf5203151b642840dd5eaad48375d007d87f7bf4b50393253db5df9abbcde2`) |
| Windows `AMD64` `build_id` | `source-sha256:8127c890e2071069b50a619fd87a8a7768732f909d1c559d9aff1d8ecd4ed402` | Deterministic `build.rs` digest verified against CI baseline |
| Darwin `arm64` `build_id` | `source-sha256:2400df1920e55b8a89c6ce3269fda28623aeed6bb046e6c2fb488b42202f1dd1` | Deterministic `build.rs` digest verified against CI baseline |
| HostLab `advanced` code SHA | `e9624de311e2b39e401605e7bd70f1ca13a70a06` (base `d872f2faf5d61e70b422231803884b47670595da`) | `Analysis tooling tests` Run [`44986363105`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44986363105) — 49s green |
| Reference audit baseline | `d872f2faf5d61e70b422231803884b47670595da` (`dexsql 0.1.0` + `run_intake.py` + `home_frame_audit.py`) | Executed side-by-side in fresh serial processes on Ubuntu 24.04 (`Linux-7.0.0-1014-aws-x86_64-with-glibc2.39`, 4 vCPU) |

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

- **Workflow Run**: [`44987139478`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44987139478) (`hostlab-5e908cc60cf34283a1433ede7c3bae4a`, 10m2s, zero Java, zero Androguard (`requirements-query.txt`), warm `MeguvizDexDash 1.2.2` cache)
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
| R1 target (`9200300`) | `reference_native` | 72,828.07 | 1,284.17 | 10,703.79 | 44,294.25 | *(16,212.85 residual)* | 98.49 | 1,252.25 |
| R1 target (`9200300`) | `meguvizdexdash` | 30,386.73 | 13,319.84 | 1,383.46 | 8,480.83 | 6,179.51 | 50.23 | 1,835.41 |
| R1 baseline (`9200200`) | `meguvizdexdash` | 30,675.37 | 13,406.19 | 1,471.56 | 8,550.65 | 6,218.47 | 51.16 | 1,849.26 |
| R1 baseline (`9200200`) | `reference_native` | 74,125.09 | 1,286.16 | 11,246.54 | 45,255.49 | *(15,999.85 residual)* | 100.81 | 1,249.82 |
| R2 target (`9200300`) | `meguvizdexdash` | 30,189.25 | 13,194.72 | 1,392.95 | 8,396.38 | 6,199.80 | 50.35 | 1,901.54 |
| R2 target (`9200300`) | `reference_native` | 73,085.28 | 1,289.87 | 10,956.09 | 44,505.03 | *(15,996.68 residual)* | 99.47 | 1,238.43 |
| R2 baseline (`9200200`) | `reference_native` | 74,461.71 | 1,284.86 | 11,790.60 | 45,002.80 | *(16,043.78 residual)* | 101.56 | 1,244.04 |
| R2 baseline (`9200200`) | `meguvizdexdash` | 30,159.11 | 13,045.90 | 1,415.06 | 8,517.09 | 6,180.28 | 50.19 | 1,797.11 |

> *(Reference residual gate cost = `audit_and_shared_scan_ms - prepare_ms - structural_ms - surface_ms`, representing standalone `run_intake.py` + `home_frame_audit.py` execution and subprocess teardown.)*

### 3.3 Experiment 1 Aggregated Comparison (4-Run Means)

| Metric | `reference_native` (`dexsql 0.1.0`) Mean | `meguvizdexdash 1.2.2` Mean | Delta / Speedup |
|---|---:|---:|---|
| Total worker `elapsed_ms` | 73,625.04 ms (73.63 s) | **30,352.61 ms (30.35 s)** | **2.43x faster (-58.8%)** |
| Snapshot `prepare_ms` | 1,286.27 ms | 13,241.66 ms | Eager parallel table build upfront |
| Structural rules `structural_ms` | 11,174.25 ms | **1,415.76 ms** | **7.89x faster (-87.3%)** |
| Surface scan `surface_ms` | 44,764.39 ms | **8,486.24 ms** | **5.27x faster (-81.0%)** |
| Intake + Home gates | ~16,063 ms (`run_intake` + `home_frame_audit`) | **6,194.52 ms** (`mdd_gates`) | **2.59x faster (-61.4%)** |
| Total CPU time (`user + sys`) | 100.08 s | **50.48 s** | **1.98x less CPU (-49.6%)** |
| Process tree RSS peak | **1,246.13 MiB** | 1,845.83 MiB | +599.70 MiB (+48.1%) in-memory snapshot tradeoff within 16 GiB CI RAM |

*(Note: `sampled_cgroup_memory_peak_bytes` is container-lifetime monotonic on Linux cgroup v2 and therefore rises across sequential runs from 3,191 MiB to 3,990 MiB for `reference_native` and 4,276 MiB to 5,066 MiB for `meguvizdexdash`; process-tree `sampled_tree_rss_peak_bytes` measures each fresh isolated worker tree accurately.)*

---

## 4. Experiment 2: MCP Query / Decode / Refs / Manifest Equivalence & Performance (`sqlite / Androguard 4.1.4` vs `meguvizdexdash 1.2.2 mcp`)

- **Workflow Run**: [`44986457292`](https://github.com/jichuo1/innocent-lab-host-analysis/actions/runs/44986457292) (`hostlab-3641e832e9d144319cd949f9eafb4d00`, 9m13s, `jadx: false`)
- **Sample**: `9200300` (`609003767fbbfe4870d6bcbd8cea0292833327c4eef6513eb7388852be070bcc`, 257,273,718 bytes)
- **Methodology**: 2 alternating serial MCP sessions (`meguvizdexdash` vs `sqlite`) covering class/method/field lookup, string literal references (`method_strings`), duplicate-task memoization (`string_reused`), caller refs (`method_calls`), field access refs (`method_field_accesses`), type usage refs (`method_used_types`), method Smali decode, and AndroidManifest summary.

### 4.1 Equivalence Verification

- `result_multisets_equal`: **`true`**
- Identical canonical row counts & SHA-256 digests across all 4 sessions (`class`: 1 row `25d7a991...`, `methods`: 3 rows `1e977f92...`, `fields`: 1 row `1793dd85...`, `string`: 1 row `bbecf37f...`, `callers`: 19 rows / 12 distinct `86b4276f...`, `field_refs`: 6 rows / 3 distinct `29cb3d66...`, `type_refs`: 109 rows / 107 distinct `9a1ba53d...`, `string_reused`: 1 row `reused_from="string"`), plus verified `smali` body (`internalGetUrls` / `unmodifiableMap`) and `manifest` identity (`tv.danmaku.bili`, `9200300`).

### 4.2 Latency Breakdown Across Cold & Warm Sessions

| Phase / Task | SQLite R1 Cold Build (ms) | SQLite R2 Cache Hit (ms) | MeguvizDexDash R1 (ms) | MeguvizDexDash R2 (ms) | Speedup (MDD Avg vs Cold / Warm SQLite) |
|---|---:|---:|---:|---:|---|
| Session `prepare_ms` | 65,350.54 | 35.29 *(disk hit)* | 13,783.34 *(memory)* | 13,445.64 *(memory)* | 4.80x faster vs cold build |
| `class` (`classes`) | 2.79 | 2.82 | 6.79 | 6.53 | — |
| `methods` (`class_methods`) | 1.79 | 1.63 | 23.63 | 23.31 | — |
| `fields` (`class_fields`) | 1.52 | 1.39 | 30.99 | 29.72 | — |
| `string` (`method_strings`) | 6,327.69 | 6,106.69 | **9.18** | **8.89** | **700x / 676x faster** |
| `callers` (`method_calls`) | 4,119.81 | 4,291.88 | **99.94** | **98.67** | **41.5x / 43.2x faster** |
| `field_refs` (`method_field_accesses`) | 2,540.43 | 2,653.94 | **59.62** | **53.29** | **45.0x / 47.0x faster** |
| `type_refs` (`method_used_types`) | 88,653.52 | 90,011.75 | **52.90** | **51.97** | **1,691x / 1,717x faster** |
| `smali` (`decode`) | 1,360.42 | 1,447.66 | 5,287.57 | 5,168.07 | 0.26x *(fresh on-demand decode without pre-saved APK index)* |
| `manifest` (`get_manifest`) | 323.99 | 329.82 | **6.81** | **6.76** | **47.8x / 48.6x faster** |
| `string_reused` | 0.02 | 0.02 | 0.04 | 0.04 | Semantic memo reuse |
| **Total `total_ms`** | **169,814.46 (169.81 s)** | **105,983.87 (105.98 s)** | **21,589.26 (21.59 s)** | **21,037.03 (21.04 s)** | **7.97x vs cold SQLite / 4.97x vs warm SQLite** |

*(Note: `verify_backends.py` does not attach `runner_resources` RSS telemetry to `verification.json` in Experiment 2.)*
