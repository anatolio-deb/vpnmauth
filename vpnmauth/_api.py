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
            server = node["server"].split(";")
            data = dict(value.split("=") for value in server[-1].split("|"))
            response["data"]["node"][response["data"]["node"].index(node)]["server"] = [
                server[:-1],
                data,
            ]

        return response
