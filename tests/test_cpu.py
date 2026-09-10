from framework.config import load_config
from framework.system_info import cpu_info


def test_cpu_validation(request):
    request.node.validation_area = "cpu"
    config = load_config()
    info = cpu_info()
    assert info["core_count"] > 0, "no logical CPU cores were detected"
    assert info["usage_percent"] <= config.cpu.max_usage_percent, (
        f"CPU usage {info['usage_percent']}% exceeds threshold {config.cpu.max_usage_percent}%"
    )
