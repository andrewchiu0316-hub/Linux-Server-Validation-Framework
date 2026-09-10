"""Host inspection and safe command-execution primitives."""
from __future__ import annotations

import platform
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    stdout: str
    stderr: str
    returncode: int | None
    error: str | None = None


def run_command(command: list[str], timeout: float = 10) -> CommandResult:
    """Run a command without a shell and convert common execution errors to data."""
    if not command:
        return CommandResult((), "", "", None, "empty command")
    if shutil.which(command[0]) is None:
        return CommandResult(tuple(command), "", "", None, f"command not found: {command[0]}")
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)
        return CommandResult(tuple(command), completed.stdout, completed.stderr, completed.returncode)
    except subprocess.TimeoutExpired:
        return CommandResult(tuple(command), "", "", None, f"command timed out after {timeout}s")
    except PermissionError:
        return CommandResult(tuple(command), "", "", None, "permission denied")
    except OSError as exc:
        return CommandResult(tuple(command), "", "", None, str(exc))


def cpu_info(sample_seconds: float = 0.2) -> dict[str, Any]:
    return {"usage_percent": psutil.cpu_percent(interval=sample_seconds), "core_count": psutil.cpu_count(logical=True) or 0,
            "load_average": list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else []}


def memory_info() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    return {"total_bytes": memory.total, "available_bytes": memory.available, "usage_percent": memory.percent}


def disk_info(path: str) -> dict[str, Any]:
    usage = psutil.disk_usage(path)
    return {"path": path, "total_bytes": usage.total, "used_bytes": usage.used, "free_bytes": usage.free, "usage_percent": usage.percent}


def network_interfaces_up() -> list[str]:
    return [name for name, stats in psutil.net_if_stats().items() if stats.isup and name.lower() not in {"lo", "loopback"}]


def check_connectivity(target: str, port: int, timeout: float) -> tuple[bool, str]:
    """Resolve and connect; port 0 means only name-resolution is required."""
    try:
        socket.getaddrinfo(target, None)
    except socket.gaierror as exc:
        return False, f"DNS resolution failed for {target}: {exc}"
    if port == 0:
        return True, f"resolved {target} (port probe disabled)"
    try:
        with socket.create_connection((target, port), timeout=timeout):
            return True, f"TCP connection to {target}:{port} succeeded"
    except socket.timeout:
        return False, f"connection to {target}:{port} timed out after {timeout}s"
    except OSError as exc:
        return False, f"connection to {target}:{port} failed: {exc}"


def os_info() -> dict[str, str | float]:
    boot_time = psutil.boot_time()
    return {"distribution": platform.platform(), "kernel_version": platform.release(), "hostname": socket.gethostname(),
            "architecture": platform.machine(), "uptime_seconds": round(time.time() - boot_time, 1)}


def systemd_available() -> bool:
    return platform.system() == "Linux" and Path("/run/systemd/system").exists() and shutil.which("systemctl") is not None


def service_status(service: str) -> tuple[bool, str]:
    result = run_command(["systemctl", "is-active", service], timeout=5)
    if result.error:
        return False, result.error
    status = result.stdout.strip()
    return status == "active", status or result.stderr.strip() or f"exit {result.returncode}"
