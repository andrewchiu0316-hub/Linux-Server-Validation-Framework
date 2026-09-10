"""Explicit, reversible systemd service stop helper for disposable hosts."""
from __future__ import annotations

import argparse
import platform
from framework.system_info import run_command, systemd_available


def change_service(service: str, action: str, confirm: bool) -> None:
    if not confirm: raise RuntimeError("refusing service change without --confirm")
    if platform.system() != "Linux" or not systemd_available(): raise RuntimeError("a Linux host with systemd is required")
    result = run_command(["systemctl", action, service])
    if result.error or result.returncode != 0: raise RuntimeError(result.error or result.stderr or "systemctl failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stop or recover a service; requires explicit confirmation.")
    parser.add_argument("service"); parser.add_argument("--recover", action="store_true"); parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args(); action = "start" if args.recover else "stop"; change_service(args.service, action, args.confirm)
    print(f"{args.service} {action} succeeded. Recovery: python -m fault_injection.service_failure {args.service} --recover --confirm")
