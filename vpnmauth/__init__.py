from ._api import VpnmApiClient

__version__ = "0.1.0"


def get_hostname_or_address(node: dict):
    if node["server"][0][1] == "443":
        return node["server"][1]["host"]
    return node["server"][0][0]
