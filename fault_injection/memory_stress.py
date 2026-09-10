from __future__ import annotations

import argparse
import time


def run(megabytes: int, duration: float) -> None:
    allocation = bytearray(megabytes * 1024 * 1024)
    allocation[::4096] = b"\x01" * len(allocation[::4096])
    try: time.sleep(duration)
    finally: del allocation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temporarily allocate memory; releases on exit.")
    parser.add_argument("--megabytes", type=int, required=True)
    parser.add_argument("--duration", type=float, default=10)
    args = parser.parse_args(); run(args.megabytes, args.duration)
