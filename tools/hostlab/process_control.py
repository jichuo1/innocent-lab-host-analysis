"""Bounded subprocesses with descendant cleanup and file-backed output."""
import os
from pathlib import Path
import signal
import subprocess


def terminate_tree(process):
    if os.name == "nt":
        # A timeout must also stop grandchildren (Python -> javac/java/workers).
        try:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=15, check=False)
        except (OSError, subprocess.TimeoutExpired):
            # Reap the direct process even if the platform's tree cleanup failed.
            # Report cleanup failure instead of presenting this as an ordinary timeout.
            process.kill()
            process.wait(timeout=15)
            raise RuntimeError("Process tree cleanup failed") from None
    else:
        # Nested managed commands have their own sessions. Include those sessions too.
        parents = {}
        for entry in Path("/proc").glob("[0-9]*/stat"):
            try:
                fields = entry.read_text().rsplit(")", 1)[1].split()
                parents[int(entry.parent.name)] = int(fields[1])
            except (OSError, ValueError, IndexError):
                continue
        descendants = {process.pid}
        while True:
            children = {pid for pid, parent in parents.items() if parent in descendants}
            if children <= descendants:
                break
            descendants.update(children)
        groups = {process.pid}
        for pid in descendants:
            try:
                groups.add(os.getpgid(pid))
            except ProcessLookupError:
                pass
        groups.discard(os.getpgrp())
        for group in groups:
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
    if process.poll() is None:
        process.kill()
    process.wait(timeout=15)


def run(command, *, stdout, stderr=subprocess.STDOUT, env=None, timeout):
    with subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env,
                          start_new_session=os.name != "nt") as process:
        try:
            return process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            terminate_tree(process)
            return 124
        except BaseException:
            terminate_tree(process)
            raise
