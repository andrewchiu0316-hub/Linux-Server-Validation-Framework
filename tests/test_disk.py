from framework.config import load_config
from framework.system_info import disk_info


def test_disk_validation(request):
    request.node.validation_area = "disk"
    config = load_config()
    info = disk_info(config.disk_path)
    assert info["total_bytes"] > 0
    assert info["usage_percent"] <= config.disk.max_usage_percent, (
        f"disk usage for {config.disk_path} is {info['usage_percent']}%, above {config.disk.max_usage_percent}%"
    )
