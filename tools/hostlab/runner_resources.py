"""Dependency-free, bounded runner telemetry and conservative prefetch admission."""
from __future__ import annotations

import ctypes
import json
import math
import os
from pathlib import Path
import platform
import shutil
import threading
import time

PROC = Path("/proc")
CGROUP = Path("/sys/fs/cgroup")
MAX_RECORDS = 7200
MAX_BYTES = 1024 * 1024
GIB = 1024**3
FIELDS = (
    "cpu_usage_fraction", "cpu_iowait_fraction", "cpu_steal_fraction", "effective_cpus",
    "memory_available_bytes", "memory_limit_bytes", "cgroup_memory_current_bytes", "tree_rss_bytes",
    "psi_cpu_some_fraction", "psi_cpu_full_fraction", "psi_memory_some_fraction", "psi_memory_full_fraction",
    "psi_io_some_fraction", "psi_io_full_fraction", "cgroup_cpu_throttled_usec_delta",
    "cgroup_cpu_nr_throttled_delta", "cgroup_memory_high_delta", "cgroup_memory_max_delta",
    "cgroup_memory_oom_delta", "cgroup_memory_oom_kill_delta", "io_read_bytes_delta", "io_write_bytes_delta",
    "net_rx_bytes_delta", "net_tx_bytes_delta", "disk_free_bytes",
)


def text(path):
    try:
        with path.open(encoding="utf-8") as stream:
            value = stream.read(256 * 1024 + 1)
        return value if len(value) <= 256 * 1024 else None
    except (OSError, UnicodeError):
        return None


def number(value):
    try:
        result = int(value)
        return result if result >= 0 else None
    except (ValueError, TypeError):
        return None


def pairs(value):
    result = {}
    for line in (value or "").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            parsed = number(parts[1])
            if parsed is not None:
                result[parts[0].rstrip(":")] = parsed
    return result


def delta(current, previous):
    return current-previous if current is not None and previous is not None and current >= previous else None


def affinity_cpus():
    try:
        if hasattr(os, "sched_getaffinity"):
            return len(os.sched_getaffinity(0)) or None
        count = getattr(os, "process_cpu_count", os.cpu_count)()
        return count or None
    except (OSError, ValueError):
        return os.cpu_count() or None


def cgroup_directory():
    for line in (text(PROC / "self/cgroup") or "").splitlines():
        if line.startswith("0::"):
            relative = Path(line[3:].lstrip("/"))
            if ".." not in relative.parts:
                candidate = CGROUP / relative
                if (candidate / "cpu.stat").is_file():
                    return candidate
    return CGROUP if (CGROUP / "cgroup.controllers").is_file() else None


def tree_rss():
    """A bounded sample of this process and readable descendants, never a true peak."""
    pending, seen, total, threads_seen = [os.getpid()], set(), 0, 0
    while pending:
        pid = pending.pop()
        if pid in seen:
            continue
        seen.add(pid)
        if len(seen) > 128:
            return None
        root = PROC / str(pid)
        status = text(root / "status")
        if status is None:
            if not root.exists():  # A descendant may have exited between the two reads.
                continue
            return None
        rss = pairs(status).get("VmRSS")
        if rss is None:
            return None
        total += rss*1024
        try:
            tasks = list((root / "task").iterdir())
        except OSError:
            if not root.exists():
                continue
            return None
        for task in tasks:
            if not task.name.isdigit():
                continue
            threads_seen += 1
            if threads_seen > 256:
                return None
            children = text(task / "children")
            if children is None:
                if not task.exists():
                    continue
                return None
            try:
                pending.extend(int(value) for value in children.split())
            except ValueError:
                return None
    return total


def pressure(value):
    result = {}
    for line in (value or "").splitlines():
        words = line.split()
        if words and words[0] in {"some", "full"}:
            for word in words[1:]:
                if word.startswith("total="):
                    result[words[0]] = number(word[6:])
    return result


def linux_raw():
    result = {}
    cpus = affinity_cpus()
    group = cgroup_directory()
    cpu = pairs(text(group / "cpu.stat")) if group else {}
    quota = (text(group / "cpu.max") or "").split() if group else []
    if len(quota) == 2 and number(quota[0]) is not None and number(quota[1]):
        capacity = int(quota[0])/int(quota[1])
        cpus = min(cpus, capacity) if cpus is not None else capacity
    result.update(effective_cpus=cpus, cpu_usage_usec=cpu.get("usage_usec"),
                  throttled_usec=cpu.get("throttled_usec"), nr_throttled=cpu.get("nr_throttled"))
    for line in (text(PROC / "stat") or "").splitlines():
        if line.startswith("cpu "):
            values = [number(value) for value in line.split()[1:9]]
            if len(values) == 8 and all(value is not None for value in values):
                result.update(cpu_total=sum(values), cpu_idle=values[3], cpu_iowait=values[4], cpu_steal=values[7])
            break
    memory = pairs(text(PROC / "meminfo"))
    available = memory.get("MemAvailable")
    limit = memory.get("MemTotal")
    available = available*1024 if available is not None else None
    limit = limit*1024 if limit is not None else None
    current = number((text(group / "memory.current") or "").strip()) if group else None
    maximum = number((text(group / "memory.max") or "").strip()) if group else None
    if maximum is not None:
        limit = min(limit, maximum) if limit is not None else maximum
        if current is not None:
            remaining = max(0, maximum-current)
            available = min(available, remaining) if available is not None else remaining
    events = pairs(text(group / "memory.events")) if group else {}
    result.update(memory_available_bytes=available, memory_limit_bytes=limit,
                  cgroup_memory_current_bytes=current, tree_rss_bytes=tree_rss())
    for event in ("high", "max", "oom", "oom_kill"):
        result["memory_"+event] = events.get(event)
    for kind in ("cpu", "memory", "io"):
        psi = pressure(text(PROC / "pressure" / kind))
        for level in ("some", "full"):
            result[f"psi_{kind}_{level}"] = psi.get(level)
    io = {}
    for line in (text(group / "io.stat") or "").splitlines() if group else []:
        for word in line.split()[1:]:
            if "=" in word:
                key, value = word.split("=", 1)
                if key in {"rbytes", "wbytes"} and number(value) is not None:
                    io[key] = io.get(key, 0)+int(value)
    if io:
        result.update(io_read=io.get("rbytes"), io_write=io.get("wbytes"), io_counter_scope="cgroup")
    else:
        own = pairs(text(PROC / "self/io"))
        result.update(io_read=own.get("read_bytes"), io_write=own.get("write_bytes"), io_counter_scope="self")
    net_rx = net_tx = None
    for line in (text(PROC / "net/dev") or "").splitlines():
        if ":" not in line or line.split(":", 1)[0].strip() == "lo":
            continue
        values = line.split(":", 1)[1].split()
        if len(values) >= 9 and number(values[0]) is not None and number(values[8]) is not None:
            net_rx = (net_rx or 0)+int(values[0]); net_tx = (net_tx or 0)+int(values[8])
    result.update(net_rx=net_rx, net_tx=net_tx)
    return result


def windows_raw():
    result = {"effective_cpus": affinity_cpus()}
    try:
        class FileTime(ctypes.Structure):
            _fields_ = [("low", ctypes.c_uint32), ("high", ctypes.c_uint32)]

        class MemoryStatus(ctypes.Structure):
            _fields_ = [("length", ctypes.c_uint32), ("load", ctypes.c_uint32)] + [
                (name, ctypes.c_uint64) for name in ("total", "available", "page_total", "page_available",
                                                   "virtual_total", "virtual_available", "extended_available")]

        api = ctypes.windll.kernel32
        idle, kernel, user = FileTime(), FileTime(), FileTime()
        if api.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            value = lambda item: (item.high << 32) | item.low
            result.update(cpu_total=value(kernel)+value(user), cpu_idle=value(idle))
        memory = MemoryStatus(); memory.length = ctypes.sizeof(memory)
        if api.GlobalMemoryStatusEx(ctypes.byref(memory)):
            result.update(memory_limit_bytes=memory.total, memory_available_bytes=memory.available)
    except (AttributeError, OSError):
        pass
    return result


class Probe:
    def __init__(self, disk_path, *, system=None):
        self.disk_path = Path(disk_path)
        self.system = system or platform.system()
        self.previous = None
        self.previous_at = None

    def collect(self, now):
        raw = linux_raw() if self.system == "Linux" else windows_raw() if self.system == "Windows" else {}
        old = self.previous or {}
        elapsed = now-self.previous_at if self.previous_at is not None else None
        sample = {field: raw.get(field) for field in FIELDS}
        sample.update(cpu_counter_scope=None, io_counter_scope=raw.get("io_counter_scope"),
                      network_counter_scope="system_interfaces_excluding_loopback" if self.system == "Linux" else None)
        total = delta(raw.get("cpu_total"), old.get("cpu_total"))
        if total:
            idle = delta(raw.get("cpu_idle"), old.get("cpu_idle"))
            wait = delta(raw.get("cpu_iowait"), old.get("cpu_iowait"))
            steal = delta(raw.get("cpu_steal"), old.get("cpu_steal"))
            if idle is not None:
                sample["cpu_usage_fraction"] = max(0.0, min(1.0, (total-idle-(wait or 0)-(steal or 0))/total))
                sample["cpu_counter_scope"] = "system"
            sample["cpu_iowait_fraction"] = wait/total if wait is not None else None
            sample["cpu_steal_fraction"] = steal/total if steal is not None else None
        usage = delta(raw.get("cpu_usage_usec"), old.get("cpu_usage_usec"))
        cpus = raw.get("effective_cpus")
        if usage is not None and elapsed and cpus:
            sample["cpu_usage_fraction"] = max(0.0, min(1.0, usage/(elapsed*cpus*1000000)))
            sample["cpu_counter_scope"] = "cgroup"
        for kind in ("cpu", "memory", "io"):
            for level in ("some", "full"):
                value = delta(raw.get(f"psi_{kind}_{level}"), old.get(f"psi_{kind}_{level}"))
                sample[f"psi_{kind}_{level}_fraction"] = min(1.0, value/(elapsed*1000000)) if value is not None and elapsed else None
        for name, key in (("cgroup_cpu_throttled_usec_delta", "throttled_usec"),
                          ("cgroup_cpu_nr_throttled_delta", "nr_throttled"),
                          ("io_read_bytes_delta", "io_read"), ("io_write_bytes_delta", "io_write"),
                          ("net_rx_bytes_delta", "net_rx"), ("net_tx_bytes_delta", "net_tx")):
            sample[name] = delta(raw.get(key), old.get(key))
        if raw.get("io_counter_scope") != old.get("io_counter_scope"):
            sample["io_read_bytes_delta"] = sample["io_write_bytes_delta"] = None
        for event in ("high", "max", "oom", "oom_kill"):
            sample[f"cgroup_memory_{event}_delta"] = delta(raw.get("memory_"+event), old.get("memory_"+event))
        try:
            sample["disk_free_bytes"] = shutil.disk_usage(self.disk_path).free
        except OSError:
            sample["disk_free_bytes"] = None
        self.previous, self.previous_at = raw, now
        return sample


def rusage():
    try:
        import resource
        own, children = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
        return {"self_user": own.ru_utime, "self_system": own.ru_stime,
                "children_user": children.ru_utime, "children_system": children.ru_stime}
    except (ImportError, OSError, ValueError):
        return None


class Sampler:
    def __init__(self, *, origin=None, disk_path=".", interval=0.5, probe=None,
                 max_records=MAX_RECORDS, max_bytes=MAX_BYTES):
        self.origin = time.monotonic() if origin is None else origin
        self.interval = max(0.05, interval)
        self.probe = probe or Probe(disk_path)
        self.max_records = min(MAX_RECORDS, max_records)
        self.max_bytes = min(MAX_BYTES, max_bytes)
        self.samples = []; self.record_bytes = 0; self.count = 0; self.omitted = 0
        self.latest = {field: None for field in FIELDS}
        self.maxima = {}; self.totals = {}; self.phase = "preparing"
        self.lock = threading.Lock(); self.stopped = threading.Event(); self.thread = None
        self.initial_usage = None

    def set_phase(self, phase):
        with self.lock:
            self.phase = str(phase)[:32]

    def _sample(self):
        now = time.monotonic()
        try:
            value = self.probe.collect(now)
        except Exception:
            value = {field: None for field in FIELDS}
            value["probe_error"] = True
        with self.lock:
            value = {"ts_ms": (now-self.origin)*1000, "phase": self.phase, **value}
            self.latest = value; self.count += 1
            for key in ("tree_rss_bytes", "cgroup_memory_current_bytes"):
                if value.get(key) is not None:
                    self.maxima[key] = max(self.maxima.get(key, 0), value[key])
            for key in ("io_read_bytes_delta", "io_write_bytes_delta", "net_rx_bytes_delta", "net_tx_bytes_delta"):
                if value.get(key) is not None:
                    self.totals[key] = self.totals.get(key, 0)+value[key]
            size = len(json.dumps(value, separators=(",", ":")).encode())+1
            if len(self.samples) < self.max_records and self.record_bytes+size <= max(0, self.max_bytes-32768):
                self.samples.append(value); self.record_bytes += size
            else:
                self.omitted += 1

    def start(self):
        self.initial_usage = rusage()
        self._sample()

        def monitor():
            while not self.stopped.wait(self.interval):
                self._sample()

        self.thread = threading.Thread(target=monitor, name="hostlab-resources", daemon=True)
        self.thread.start()
        return self

    def snapshot(self):
        with self.lock:
            return dict(self.latest)

    def summary(self):
        current = rusage()
        cpu = {key+"_seconds": max(0.0, current[key]-self.initial_usage[key]) for key in current
               } if current is not None and self.initial_usage is not None else None
        with self.lock:
            return {"schema": 1, "interval_seconds": self.interval, "samples_seen": self.count,
                "samples_retained": len(self.samples), "samples_omitted": self.omitted,
                "sample_records_truncated": self.omitted > 0,
                "sampled_tree_rss_peak_bytes": self.maxima.get("tree_rss_bytes"),
                "sampled_cgroup_memory_peak_bytes": self.maxima.get("cgroup_memory_current_bytes"),
                "rss_scope": "sampled_self_and_readable_thread_children_not_true_peak",
                "rusage_cpu_delta": cpu, "observed_counter_deltas": dict(self.totals),
                "network_counter_scope": "system_interfaces_excluding_loopback",
                "latest": dict(self.latest)}

    def stop(self, output_path=None):
        self.stopped.set()
        if self.thread is not None:
            self.thread.join()
        self._sample()
        summary = self.summary()
        if output_path is not None:
            raw = json.dumps({"schema": 1, "summary": summary, "samples": self.samples},
                             separators=(",", ":"), ensure_ascii=False).encode()
            if len(raw) > self.max_bytes:
                raise RuntimeError("resource artifact exceeded its fixed budget")
            Path(output_path).write_bytes(raw)
        return summary


class SafeSampler:
    """Telemetry failures cannot change member results or strand a monitor thread."""
    def __init__(self, delegate, *, origin=None, error=None):
        self.delegate = delegate
        self.origin = time.monotonic() if origin is None else origin
        self.errors = [type(error).__name__] if error is not None else []
        self.started = False

    def _error(self, exc):
        name = type(exc).__name__
        if name not in self.errors and len(self.errors) < 8:
            self.errors.append(name)

    def _unknown(self):
        return {"ts_ms": (time.monotonic()-self.origin)*1000, "phase": "unknown", "probe_error": True,
                **{field: None for field in FIELDS}}

    def start(self):
        try:
            if self.delegate is not None:
                self.delegate.start()
                self.started = True
        except Exception as exc:
            self._error(exc)
        return self

    def set_phase(self, phase):
        try:
            if self.delegate is not None:
                self.delegate.set_phase(phase)
        except Exception as exc:
            self._error(exc)

    def snapshot(self):
        try:
            if self.started:
                return self.delegate.snapshot()
        except Exception as exc:
            self._error(exc)
        return self._unknown()

    def summary(self):
        try:
            value = self.delegate.summary() if self.delegate is not None else {}
        except Exception as exc:
            self._error(exc)
            value = {}
        return {**value, "available": self.started and not self.errors, "telemetry_errors": list(self.errors)}

    def stop(self, output_path=None):
        value = None
        try:
            if self.delegate is not None:
                value = self.delegate.stop(output_path)
        except Exception as exc:
            self._error(exc)
        finally:
            # This also handles start() raising after it launched the real monitor,
            # and a broken stop() that raised before setting its stop event.
            if self.delegate is not None:
                event = getattr(self.delegate, "stopped", None)
                thread = getattr(self.delegate, "thread", None)
                try:
                    if event is not None:
                        event.set()
                    if isinstance(thread, threading.Thread) and thread.ident is not None and thread is not threading.current_thread():
                        thread.join()
                except Exception as exc:
                    self._error(exc)
        summary = {**(value if isinstance(value, dict) else self.summary()),
                   "available": self.started and not self.errors, "telemetry_errors": list(self.errors)}
        if output_path is not None and self.errors:
            try:
                path = Path(output_path)
                document = json.loads(path.read_text(encoding="utf-8")) if path.is_file() and path.stat().st_size <= MAX_BYTES else {"schema": 1, "samples": []}
                document["summary"] = summary
                raw = json.dumps(document, separators=(",", ":")).encode()
                if len(raw) <= MAX_BYTES:
                    path.write_bytes(raw)
            except Exception as exc:
                self._error(exc)
                summary["telemetry_errors"] = list(self.errors)
        return summary


def make_sampler(**options):
    try:
        return SafeSampler(Sampler(**options), origin=options.get("origin"))
    except Exception as exc:
        return SafeSampler(None, origin=options.get("origin"), error=exc)


class AdaptivePrefetch:
    """AIMD-style 1..2 admission; existing transfers are drained, never cancelled."""
    def __init__(self, maximum=2):
        self.maximum = min(2, max(1, maximum))
        self.fetch_ms = self.processing_ms = self.ready_wait_ms = None
        self.cooldown = 0; self.low_samples = 0; self.last_ts = None

    def observe(self, *, fetch_ms, processing_ms, ready_wait_ms=0):
        for name, value in (("fetch_ms", fetch_ms), ("processing_ms", processing_ms), ("ready_wait_ms", ready_wait_ms)):
            if value is not None and value >= 0:
                old = getattr(self, name)
                setattr(self, name, value if old is None else 0.25*value+0.75*old)
        self.cooldown = max(0, self.cooldown-1)

    def decide(self, sample, *, phase, next_size, inflight=0):
        reasons = []
        cpu, available, limit = (sample.get(key) for key in
                                ("cpu_usage_fraction", "memory_available_bytes", "memory_limit_bytes"))
        floor = max(GIB, 0.20*limit) if limit is not None else GIB
        pressure_now = (cpu is not None and cpu >= 0.85) or (available is not None and available < floor)
        io = sample.get("psi_io_some_fraction")
        pressure_now = pressure_now or io is not None and io >= 0.10
        known = cpu is not None and available is not None and sample.get("disk_free_bytes") is not None
        fresh = sample.get("ts_ms") != self.last_ts
        if fresh:
            self.last_ts = sample.get("ts_ms")
            if pressure_now:
                self.cooldown = 2; self.low_samples = 0
            elif known and cpu < 0.70 and available >= floor:
                self.low_samples += 1
            else:
                self.low_samples = 0
        desired = min(self.maximum, max(1, math.ceil(self.fetch_ms/max(1.0, self.processing_ms)))) if (
            self.fetch_ms is not None and self.processing_ms is not None) else self.maximum
        if not known:
            desired = 1; reasons.append("pressure_unknown")
        if pressure_now:
            desired = 1; reasons.append("resource_pressure")
        if self.cooldown:
            desired = 1; reasons.append("cooldown")
        elif self.low_samples < 2:
            desired = 1; reasons.append("await_low_pressure_samples")
        if self.ready_wait_ms is not None and self.processing_ms is not None and self.ready_wait_ms > 1.5*self.processing_ms:
            desired = 1; reasons.append("ready_queue_backpressure")
        if phase == "processing":
            desired = 1; reasons.append("foreground_cap")
        free = sample.get("disk_free_bytes")
        required = 2*next_size+512*1024**2
        admitted = free is None or free >= required
        if not admitted:
            reasons.append("disk_capacity")
        return {"target": desired, "admit": admitted, "reason": reasons or ["latency_ratio"],
            "phase": phase, "effect": "drain_existing" if inflight > desired else "admission_only",
            "inputs": {"ts_ms": sample.get("ts_ms"), "cpu_usage_fraction": cpu,
                "memory_available_bytes": available, "memory_limit_bytes": limit,
                "psi_io_some_fraction": io, "disk_free_bytes": free, "next_sample_bytes": next_size},
            "ewma": {"fetch_ms": self.fetch_ms, "processing_ms": self.processing_ms, "ready_wait_ms": self.ready_wait_ms},
            "cooldown_samples": self.cooldown}
