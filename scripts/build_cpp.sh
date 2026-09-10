#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cmake -S "$ROOT/cpp_diag" -B "$ROOT/cpp_diag/build"
cmake --build "$ROOT/cpp_diag/build"
