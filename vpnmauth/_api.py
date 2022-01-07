"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from typing import Optional


class VpnmApiClient:
    user_id: str
    _token: str

    def __init__(
        self,
        api_url: Optional[str] = os.getenv("VPNM_API_URL"),
    ) -> None:
        self.api_url = api_url

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

    def login(
        self,
        email: Optional[str] = os.getenv("VPNM_EMAIL"),
        password: Optional[str] = os.getenv("VPNM_PASSWORD"),
    ) -> None:
        _data: dict
        data = urllib.parse.urlencode({"email": email, "passwd": password})
        with urllib.request.urlopen(
            f"{os.getenv('API_URL')}/token", data.encode("ascii")
        ) as response:
            _data = json.loads(response.read().decode("utf-8")).get("data")

        if _data:
            self.user_id, self.token = _data["user_id"], _data["token"]

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
        params = urllib.parse.urlencode({"access_token": self.token})

        with urllib.request.urlopen(
            f"{os.getenv('API_URL')}/node4?{params}"
        ) as response:
            return json.loads(response.read().decode("utf-8")).get("data").get("node")
