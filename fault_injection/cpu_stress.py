from __future__ import annotations

import argparse
import multiprocessing as mp
import time


def _burn(stop: mp.Event) -> None:
    value = 1
    while not stop.is_set():
        value = (value * 1103515245 + 12345) % (2**31)


def run(duration: float, workers: int) -> None:
    stop = mp.Event()
    processes = [mp.Process(target=_burn, args=(stop,)) for _ in range(workers)]
    for process in processes: process.start()
    try: time.sleep(duration)
    finally:
        stop.set()
        for process in processes: process.join(timeout=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temporarily load CPU; workers exit automatically.")
    parser.add_argument("--duration", type=float, default=10)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(); run(args.duration, max(1, args.workers))
