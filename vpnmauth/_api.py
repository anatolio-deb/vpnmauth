"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request


class VpnmApiClient:
    user_id: str
    token: str

    def __init__(self) -> None:
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]
        self.api_url = os.environ["API_URL"]
        self._login()

    def _login(self) -> None:
        _data: dict
        data = urllib.parse.urlencode({"email": self.email, "passwd": self.password})
        with urllib.request.urlopen(
            f"{os.getenv('API_URL')}/token", data.encode("ascii")
        ) as response:
            _data = json.loads(response.read().decode("utf-8")).get("data")

        if _data:
            self.user_id, self.token = _data["user_id"], _data["token"]
            print("Successfully logged in")

    def logout(self) -> None:
        self.user_id, self.token = "", ""

    def is_logged_in(self) -> bool:
        return bool(self.user_id and self.token)

    def get_account(self) -> dict:
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(
            f"{os.getenv('API_URL')}/user4/{self.user_id}?{params}"
        ) as response:
            return json.loads(response.read().decode("utf-8")).get("data")

    def get_nodes(self) -> list:
        print("Requesting the node list")
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(
            f"{os.getenv('API_URL')}/node4?{params}"
        ) as response:
            nodes = json.loads(response.read().decode("utf-8")).get("data").get("node")
            print(f"{len(nodes)} nodes recieved")
            return nodes
