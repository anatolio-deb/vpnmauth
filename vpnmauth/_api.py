"""Basic authentication logic for VPN Manager API
"""
from __future__ import annotations

import os
from typing import Dict

import requests


def _resolve_vpnm_api_response(json_response: Dict) -> Dict:
    """VPN Manager's API returns errors in the response data with status 200.
    To handle errors this function checks an error value in the response.

    Args:
        json_response (Dict): a response from VPN Manager API parsed as json

    Raises:
        requests.exceptions.HTTPError: when 'msg' key is not equals to 'ok'

    Returns:
        Dict: valid json response from VPN Manager API
    """
    if json_response["msg"] == "ok":
        return json_response
    raise requests.exceptions.HTTPError(json_response["msg"])


class VpnmApiClient:
    """Login, get account info and nodes from VPN Manager API."""

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

    def login(self) -> Dict:
        return _resolve_vpnm_api_response(
            requests.post(
                f"{self.api_url}/token", {"email": self.email, "passwd": self.password}
            ).json()
        )

    @property
    def account(self) -> Dict:
        return _resolve_vpnm_api_response(
            requests.get(
                f"{self.api_url}/user4/{self.user_id}", {"access_token": self.token}
            ).json()
        )

    @property
    def nodes(self) -> list:
        response = requests.get(
            f"{self.api_url}/node4", {"access_token": self.token}
        ).json()

        response = _resolve_vpnm_api_response(response)

        for node in response["data"]["node"]:
            server = node["server"].split(";")
            data = dict(value.split("=") for value in server[-1].split("|"))
            response["data"]["node"][response["data"]["node"].index(node)]["server"] = [
                server[:-1],
                data,
            ]

        return response
