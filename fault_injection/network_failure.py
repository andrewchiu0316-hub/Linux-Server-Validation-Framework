"""Non-destructive network fault simulation using an intentionally invalid target."""
from __future__ import annotations

import argparse
from framework.system_info import check_connectivity


def simulate(target: str, timeout: float) -> tuple[bool, str]:
    return check_connectivity(target, 443, timeout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate network failure without altering interfaces.")
    parser.add_argument("--target", default="invalid.invalid")
    parser.add_argument("--timeout", type=float, default=2)
    args = parser.parse_args(); ok, message = simulate(args.target, args.timeout); print(f"simulated result: {ok}; {message}")
