"""Collect failure evidence without raising additional test errors."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from framework.system_info import run_command


def _commands_for(area: str, service: str | None = None) -> list[list[str]]:
    commands = {
        "cpu": [["uptime"], ["ps", "-eo", "pid,comm,%cpu", "--sort=-%cpu"]],
        "memory": [["free", "-h"], ["ps", "-eo", "pid,comm,%mem", "--sort=-%mem"]],
        "disk": [["df", "-h"]],
        "network": [["ip", "addr"], ["ip", "route"]],
    }
    if area == "service" and service:
        return [["systemctl", "status", service, "--no-pager"], ["journalctl", "-u", service, "-n", "50", "--no-pager"]]
    return commands.get(area, [])


def collect_diagnostics(area: str, reason: str, service: str | None = None) -> Path:
    """Write failure reason and best-effort command outputs to a unique report directory."""
    root = Path(__file__).resolve().parents[1] / "reports" / "logs" / datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    root.mkdir(parents=True, exist_ok=True)
    lines = [f"area: {area}", f"reason: {reason}", ""]
    for command in _commands_for(area, service):
        result = run_command(command)
        lines.append(f"$ {' '.join(command)}")
        lines.append(result.stdout or result.stderr or result.error or f"exit {result.returncode}")
        lines.append("")
    output = root / "diagnostics.txt"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
