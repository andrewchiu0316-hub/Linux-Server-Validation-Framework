import pytest

from framework.config import load_config
from framework.system_info import service_status, systemd_available


@pytest.mark.service
def test_configured_services_are_active(request):
    if not systemd_available():
        pytest.skip("systemd is unavailable; service validation requires a Linux systemd host")
    for service in load_config().services:
        request.node.validation_area = "service"
        request.node.service_name = service
        active, detail = service_status(service)
        assert active, f"{service} service is inactive: {detail}"
