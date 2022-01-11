import json

from . import templates
from ._api import VpnmApiClient


def set_config(node: dict, user_id: str):
    if node["server"][0][1] == "443":
        config = templates.PORT_443
        config["outbounds"][0]["settings"]["vnext"][0]["address"] = node["server"][1][
            "server"
        ]
    else:
        config = templates.PORT_NON_443
        config["outbounds"][0]["settings"]["vnext"][0]["address"] = node["server"][0][0]

    config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = user_id
    config["inbound"] = {
        "port": 1080,
        "listen": "127.0.0.1",
        "protocol": "socks",
    }

    with open(
        "-".join(node["name"].split()) + ".json", "w", encoding="utf-8"
    ) as config_file:
        json.dump(config, config_file, indent=4)


def set_configs():
    client = VpnmApiClient()
    response = client.nodes
    for node in response["data"]["node"]:
        set_config(node, response["data"]["user_id"])
