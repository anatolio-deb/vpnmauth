"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request


class VpnmApiClient:
    api_url = os.getenv("VPNM_API_URL")
    email = os.getenv("VPNM_EMAIL")
    password = os.getenv("VPNM_PASSWORD")
    _user_id = ""
    _token = ""

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value

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
            return json.loads(response.read().decode("utf-8")).get("data").get("node")
