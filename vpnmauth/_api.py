"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request


class VpnmApiClient:

    _user_id = ""
    user_id = ""

    def __init__(
        self,
        api_url=os.getenv("VPNM_API_URL"),
        email=os.getenv("VPNM_EMAIL"),
        password=os.getenv("VPNM_PASSWORD"),
        token=os.getenv("VPNM_TOKEN"),
    ):
        self.api_url = api_url
        self.email = email
        self.password = password
        self.token = token

    def login(self) -> dict:
        _data: dict
        data = urllib.parse.urlencode({"email": self.email, "passwd": self.password})
        with urllib.request.urlopen(
            f"{self.api_url}/token", data.encode("ascii")
        ) as response:
            _data = json.loads(response.read().decode("utf-8")).get("data")

        if _data:
            self._user_id, self.token = _data["user_id"], _data["token"]
        return _data

    def logout(self) -> None:
        self._user_id, self.token = "", ""

    @property
    def is_logged_in(self) -> bool:
        return bool(self._user_id and self.token)

    @property
    def account(self) -> dict:
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(
            f"{self.api_url}/user4/{self._user_id}?{params}"
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
            else:
                data["address"] = server[0]
                data["network"] = server[3]
            response["node"][response["node"].index(node)]["server"] = data

        return response
