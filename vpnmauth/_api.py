"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request


class VpnmApiClient:
    def __init__(
        self,
        api_url=os.getenv("VPNM_API_URL"),
        email=os.getenv("VPNM_EMAIL"),
        password=os.getenv("VPNM_PASSWORD"),
        token=os.getenv("VPNM_TOKEN"),
        user_id="",
    ):
        self.api_url = api_url
        self.email = email
        self.password = password
        self.token = token
        self.user_id = user_id

    def login(self) -> dict:
        data = urllib.parse.urlencode({"email": self.email, "passwd": self.password})
        with urllib.request.urlopen(
            f"{self.api_url}/token", data.encode("ascii")
        ) as response:
            return json.loads(response.read().decode("utf-8")).get("data")

    @property
    def account(self) -> dict:
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(
            f"{self.api_url}/user4/{self.user_id}?{params}"
        ) as response:
            return json.loads(response.read().decode("utf-8")).get("data")

    @property
    def nodes(self) -> list:
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(f"{self.api_url}/node4?{params}") as response:
            response = json.loads(response.read().decode("utf-8")).get("data")

        for node in response["node"]:
            data = {}
            server = node["server"].split(";")
            data["port"] = server[1]
            data["alterId"] = server[2]
            data.update(value.split("=") for value in server[-1].split("|"))
            data.setdefault("server")
            if server[1] == "443":
                data["security"] = server[3]
                data["address"] = data.pop("server")
                data["network"] = server[4]
            else:
                data["address"] = server[0]
                data["network"] = server[3]
            response["node"][response["node"].index(node)]["server"] = data

        return response
