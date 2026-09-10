import json
import subprocess
from pathlib import Path

import pytest


def test_cpp_system_probe():
    executable = Path(__file__).resolve().parents[1] / "cpp_diag" / "build" / "server_diag"
    if not executable.exists():
        pytest.skip("C++ probe is not built; run ./scripts/build_cpp.sh")
    completed = subprocess.run([str(executable)], capture_output=True, text=True, timeout=5, check=False)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["cpu_cores"] > 0
    assert payload["memory_total_kb"] > 0
    assert "load_average" in payload
