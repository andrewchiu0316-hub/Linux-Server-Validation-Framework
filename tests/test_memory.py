from framework.config import load_config
from framework.system_info import memory_info


def test_memory_validation(request):
    request.node.validation_area = "memory"
    config = load_config()
    info = memory_info()
    assert info["total_bytes"] > 0 and info["available_bytes"] >= 0
    assert info["usage_percent"] <= config.memory.max_usage_percent, (
        f"memory usage {info['usage_percent']}% exceeds threshold {config.memory.max_usage_percent}%"
    )
