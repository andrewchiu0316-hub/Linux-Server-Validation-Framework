from framework.config import load_config
from framework.system_info import check_connectivity, network_interfaces_up


def test_network_interface_validation(request):
    request.node.validation_area = "network"
    interfaces = network_interfaces_up()
    assert interfaces, "no non-loopback network interface is UP"


def test_network_connectivity_validation(request):
    request.node.validation_area = "network"
    config = load_config().network
    healthy, reason = check_connectivity(config.target, config.port, config.timeout)
    assert healthy, reason
