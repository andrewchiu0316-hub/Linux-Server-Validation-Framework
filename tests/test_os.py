from framework.system_info import os_info


def test_os_inventory_validation():
    info = os_info()
    assert info["hostname"]
    assert info["kernel_version"]
    assert float(info["uptime_seconds"]) >= 0
