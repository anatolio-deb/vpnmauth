"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import os

import requests


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
        return requests.post(
            f"{self.api_url}/token", {"email": self.email, "passwd": self.password}
        ).json()

    @property
    def account(self) -> dict:
        return requests.get(
            f"{self.api_url}/user4/{self.user_id}", {"access_token": self.token}
        ).json()

    @property
    def nodes(self) -> list:
        response = requests.get(
            f"{self.api_url}/node4", {"access_token": self.token}
        ).json()

        for node in response["data"]["node"]:
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
            response["data"]["node"][response["data"]["node"].index(node)][
                "server"
            ] = data

        return response
