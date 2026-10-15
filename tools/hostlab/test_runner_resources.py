"""Resource telemetry stays bounded and missing signals never masquerade as zero."""
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import runner_resources as resources


class LinuxResourceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.proc, self.group = self.root / "proc", self.root / "cgroup"
        self.addCleanup(patch.stopall)
        patch.object(resources, "PROC", self.proc).start()
        patch.object(resources, "CGROUP", self.group).start()
        patch.object(resources, "affinity_cpus", return_value=8).start()
        self.write(self.proc / "self/cgroup", "0::/\n")
        self.write(self.group / "cgroup.controllers", "cpu memory io")
        self.write(self.group / "cpu.max", "200000 100000")
        self.write(self.group / "cpu.stat", "usage_usec 1000000\nnr_throttled 2\nthrottled_usec 100\n")
        self.write(self.group / "memory.max", str(4*resources.GIB))
        self.write(self.group / "memory.current", str(resources.GIB))
        self.write(self.group / "memory.events", "high 1\nmax 0\noom 0\noom_kill 0\n")
        self.write(self.group / "io.stat", "8:0 rbytes=100 wbytes=200 rios=1 wios=2\n")
        self.write(self.proc / "stat", "cpu 100 0 100 800 50 0 0 10\n")
        self.write(self.proc / "meminfo", f"MemTotal: {8*1024**2} kB\nMemAvailable: {6*1024**2} kB\n")
        self.write(self.proc / "net/dev", "eth0: 1000 0 0 0 0 0 0 0 2000 0 0 0 0 0 0 0\nlo: 999 0 0 0 0 0 0 0 999 0 0 0 0 0 0 0\n")
        for kind, value in (("cpu", 10000), ("memory", 1000), ("io", 2000)):
            self.write(self.proc / "pressure" / kind, f"some avg10=0.00 total={value}\nfull total=0\n")
        pid = os.getpid()
        self.write(self.proc / str(pid) / "status", "VmRSS: 10 kB\n")
        self.write(self.proc / str(pid) / "task" / str(pid) / "children", "")
        self.write(self.proc / str(pid) / "task" / str(pid+1) / "children", "7")
        self.write(self.proc / "7/status", "VmRSS: 20 kB\n")
        self.write(self.proc / "7/task/7/children", "")

    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def test_cgroup_quota_memory_and_deltas_keep_their_scopes(self):
        probe = resources.Probe(self.root, system="Linux")
        first = probe.collect(1.0)
        self.assertIsNone(first["cpu_usage_fraction"])
        self.assertIsNone(first["io_read_bytes_delta"])
        self.assertEqual(first["effective_cpus"], 2)
        self.assertEqual(first["memory_available_bytes"], 3*resources.GIB)
        self.assertEqual(first["memory_limit_bytes"], 4*resources.GIB)
        self.assertEqual(first["tree_rss_bytes"], 30*1024)
        self.write(self.group / "cpu.stat", "usage_usec 1500000\nnr_throttled 3\nthrottled_usec 500\n")
        self.write(self.proc / "stat", "cpu 150 0 200 840 70 0 0 20\n")
        self.write(self.group / "memory.events", "high 3\nmax 1\noom 0\noom_kill 0\n")
        self.write(self.group / "io.stat", "8:0 rbytes=300 wbytes=260\n")
        self.write(self.proc / "net/dev", "eth0: 1500 0 0 0 0 0 0 0 2500 0 0 0 0 0 0 0\n")
        self.write(self.proc / "pressure/io", "some total=27000\nfull total=5000\n")
        second = probe.collect(1.5)
        self.assertAlmostEqual(second["cpu_usage_fraction"], 0.5)
        self.assertEqual(second["cpu_counter_scope"], "cgroup")
        self.assertAlmostEqual(second["cpu_iowait_fraction"], 20/220)
        self.assertAlmostEqual(second["cpu_steal_fraction"], 10/220)
        self.assertEqual(second["cgroup_cpu_throttled_usec_delta"], 400)
        self.assertEqual(second["cgroup_cpu_nr_throttled_delta"], 1)
        self.assertEqual(second["cgroup_memory_high_delta"], 2)
        self.assertEqual(second["io_read_bytes_delta"], 200)
        self.assertEqual(second["io_write_bytes_delta"], 60)
        self.assertEqual(second["io_counter_scope"], "cgroup")
        self.assertEqual(second["net_rx_bytes_delta"], 500)
        self.assertEqual(second["net_tx_bytes_delta"], 500)
        self.assertAlmostEqual(second["psi_io_some_fraction"], 0.05)
        self.assertAlmostEqual(second["psi_io_full_fraction"], 0.01)

    def test_thread_created_descendants_are_counted_without_double_counting(self):
        pid = os.getpid()
        self.write(self.proc / str(pid) / "task" / str(pid) / "children", "7")
        self.assertEqual(resources.tree_rss(), 30*1024)

    def test_unreadable_live_descendant_is_unknown_not_partial_rss(self):
        self.write(self.proc / "7/status", "Name: fixture\n")
        self.assertIsNone(resources.tree_rss())

    def test_thread_scan_is_bounded(self):
        pid = os.getpid()
        for index in range(256):
            self.write(self.proc / str(pid) / "task" / str(pid+100+index) / "children", "")
        self.assertIsNone(resources.tree_rss())

    def test_counter_reset_is_unknown_instead_of_a_negative_or_invented_zero(self):
        probe = resources.Probe(self.root, system="Linux")
        probe.collect(1)
        self.write(self.group / "cpu.stat", "usage_usec 1\n")
        self.write(self.group / "io.stat", "8:0 rbytes=1 wbytes=1\n")
        value = probe.collect(2)
        self.assertIsNone(value["io_read_bytes_delta"])
        self.assertIsNone(value["cgroup_cpu_throttled_usec_delta"])

    def test_missing_memory_and_psi_stay_unknown(self):
        with patch.object(resources, "linux_raw", return_value={}):
            value = resources.Probe(self.root, system="Linux").collect(1)
        for field in ("memory_available_bytes", "memory_limit_bytes", "tree_rss_bytes", "psi_io_some_fraction"):
            self.assertIsNone(value[field])

    def test_windows_unsupported_cpu_and_memory_are_unknown(self):
        with patch.object(resources, "windows_raw", return_value={}):
            value = resources.Probe(self.root, system="Windows").collect(1)
        self.assertIsNone(value["cpu_usage_fraction"])
        self.assertIsNone(value["cpu_iowait_fraction"])
        self.assertIsNone(value["tree_rss_bytes"])
        self.assertIsNone(value["memory_available_bytes"])

    def test_io_scope_change_does_not_subtract_cgroup_and_self_counters(self):
        values = [{"io_read": 100, "io_write": 200, "io_counter_scope": "cgroup"},
                  {"io_read": 10000, "io_write": 20000, "io_counter_scope": "self"}]
        with patch.object(resources, "linux_raw", side_effect=values):
            probe = resources.Probe(self.root, system="Linux")
            probe.collect(1)
            changed = probe.collect(2)
        self.assertEqual(changed["io_counter_scope"], "self")
        self.assertIsNone(changed["io_read_bytes_delta"])
        self.assertIsNone(changed["io_write_bytes_delta"])


class SamplerTest(unittest.TestCase):
    class FakeProbe:
        def __init__(self):
            self.calls = 0
            self.sampled = threading.Event()

        def collect(self, now):
            self.calls += 1
            if self.calls >= 3:
                self.sampled.set()
            return {**{field: None for field in resources.FIELDS}, "tree_rss_bytes": self.calls*100,
                    "cgroup_memory_current_bytes": self.calls*200, "cpu_usage_fraction": 0.5,
                    "memory_available_bytes": 4*resources.GIB, "memory_limit_bytes": 8*resources.GIB}

    def test_sampler_stops_joins_and_uses_common_monotonic_origin(self):
        probe = self.FakeProbe()
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "resources.json"
            sampler = resources.Sampler(origin=0, probe=probe, interval=0.05).start()
            try:
                self.assertTrue(probe.sampled.wait(2))
            finally:
                summary = sampler.stop(output)
            self.assertFalse(sampler.thread.is_alive())
            self.assertEqual(summary["sampled_tree_rss_peak_bytes"], probe.calls*100)
            self.assertEqual(summary["sampled_cgroup_memory_peak_bytes"], probe.calls*200)
            document = json.loads(output.read_text())
            self.assertGreater(document["samples"][0]["ts_ms"], 0)
            self.assertIn("not_true_peak", summary["rss_scope"])
            self.assertLessEqual(output.stat().st_size, resources.MAX_BYTES)

    def test_snapshot_does_not_take_unbounded_additional_samples(self):
        probe = self.FakeProbe()
        sampler = resources.Sampler(probe=probe)
        sampler._sample()
        for _ in range(100):
            sampler.snapshot()
        self.assertEqual(probe.calls, 1)

    def test_record_and_byte_budgets_retain_explicit_omission_count(self):
        for budget in ({"max_records": 2}, {"max_bytes": 4096}):
            with self.subTest(budget=budget), tempfile.TemporaryDirectory() as folder:
                sampler = resources.Sampler(probe=self.FakeProbe(), **budget)
                for _ in range(20):
                    sampler._sample()
                output = Path(folder) / "resources.json"
                summary = sampler.stop(output)
                self.assertTrue(summary["sample_records_truncated"])
                self.assertGreater(summary["samples_omitted"], 0)
                self.assertLessEqual(len(sampler.samples), budget.get("max_records", resources.MAX_RECORDS))
                self.assertLessEqual(output.stat().st_size, budget.get("max_bytes", resources.MAX_BYTES))

    def test_rusage_is_a_delta_and_is_not_mislabelled_process_memory(self):
        initial = {"self_user": 1, "self_system": 2, "children_user": 3, "children_system": 4}
        final = {"self_user": 3, "self_system": 5, "children_user": 7, "children_system": 9}
        with patch.object(resources, "rusage", side_effect=[initial, final]):
            sampler = resources.Sampler(probe=self.FakeProbe(), interval=60).start()
            summary = sampler.stop()
        self.assertEqual(summary["rusage_cpu_delta"], {"self_user_seconds": 2, "self_system_seconds": 3,
            "children_user_seconds": 4, "children_system_seconds": 5})
        self.assertNotIn("rss", str(summary["rusage_cpu_delta"]))

    def test_probe_failure_is_observable_and_does_not_kill_sampling(self):
        class Broken:
            def collect(self, now):
                raise OSError("private path must not be copied")

        sampler = resources.Sampler(probe=Broken())
        sampler._sample()
        snapshot = sampler.snapshot()
        self.assertTrue(snapshot["probe_error"])
        self.assertIsNone(snapshot["cpu_usage_fraction"])
        self.assertNotIn("private path", json.dumps(snapshot))


class AdaptivePrefetchTest(unittest.TestCase):
    def sample(self, **changes):
        return {"ts_ms": 0, "cpu_usage_fraction": 0.2, "memory_available_bytes": 4*resources.GIB,
            "memory_limit_bytes": 8*resources.GIB, "disk_free_bytes": 10*resources.GIB,
            "psi_io_some_fraction": 0.0, **changes}

    def decide(self, controller, sample=None, phase="waiting_inputs", inflight=0):
        return controller.decide(sample or self.sample(), phase=phase, next_size=200*1024**2, inflight=inflight)

    def test_unknown_pressure_starts_conservatively(self):
        controller = resources.AdaptivePrefetch()
        result = self.decide(controller, self.sample(cpu_usage_fraction=None))
        self.assertEqual(result["target"], 1)
        self.assertIn("pressure_unknown", result["reason"])

    def test_two_fresh_low_pressure_samples_allow_two_downloads(self):
        controller = resources.AdaptivePrefetch()
        self.assertEqual(self.decide(controller)["target"], 1)
        self.assertEqual(self.decide(controller, self.sample(ts_ms=1))["target"], 2)

    def test_repeated_reads_of_one_snapshot_do_not_fake_hysteresis_evidence(self):
        controller = resources.AdaptivePrefetch()
        for _ in range(10):
            self.assertEqual(self.decide(controller)["target"], 1)

    def test_foreground_cap_drains_existing_transfers_without_cancelling_them(self):
        controller = resources.AdaptivePrefetch()
        self.decide(controller)
        decision = self.decide(controller, self.sample(ts_ms=1), phase="processing", inflight=2)
        self.assertEqual(decision["target"], 1)
        self.assertEqual(decision["effect"], "drain_existing")
        self.assertIn("foreground_cap", decision["reason"])

    def test_pressure_contracts_and_requires_two_completed_members_to_recover(self):
        for changes in ({"cpu_usage_fraction": 0.9}, {"memory_available_bytes": 512*1024**2},
                        {"psi_io_some_fraction": 0.2}):
            with self.subTest(changes=changes):
                controller = resources.AdaptivePrefetch()
                self.decide(controller)
                self.decide(controller, self.sample(ts_ms=1))
                decision = self.decide(controller, self.sample(ts_ms=2, **changes))
                self.assertEqual(decision["target"], 1)
                self.assertIn("resource_pressure", decision["reason"])
                controller.observe(fetch_ms=3000, processing_ms=1000)
                self.assertEqual(self.decide(controller, self.sample(ts_ms=3))["target"], 1)
                controller.observe(fetch_ms=3000, processing_ms=1000)
                self.assertEqual(self.decide(controller, self.sample(ts_ms=4))["target"], 2)

    def test_fast_producer_or_long_ready_wait_limits_lookahead(self):
        controller = resources.AdaptivePrefetch()
        self.decide(controller)
        controller.observe(fetch_ms=10, processing_ms=1000)
        self.assertEqual(self.decide(controller, self.sample(ts_ms=1))["target"], 1)
        controller.observe(fetch_ms=4000, processing_ms=1000, ready_wait_ms=10000)
        decision = self.decide(controller, self.sample(ts_ms=2))
        self.assertEqual(decision["target"], 1)
        self.assertIn("ready_queue_backpressure", decision["reason"])

    def test_disk_capacity_blocks_admission_with_explicit_reason(self):
        result = self.decide(resources.AdaptivePrefetch(), self.sample(disk_free_bytes=100))
        self.assertFalse(result["admit"])
        self.assertIn("disk_capacity", result["reason"])


if __name__ == "__main__":
    unittest.main()
