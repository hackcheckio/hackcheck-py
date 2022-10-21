import requests

from .errors import InvalidApiKey
from .types import Result, Source

BASE_URL = "https://api.hackcheck.io/v3/lookup"

_without = lambda d, w: {k: v for k, v in d.items() if k != w}


class Hackcheck:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.allowed_rate_limit = 0
        self.current_rate_limit = 0

        assert self.api_key != ""

    def _lookup_request(self, q: str, inp: str) -> list[Result]:
        response = requests.get(f"{BASE_URL}/{self.api_key}/{q}/{inp}")

        if response.status_code == 401:
            raise InvalidApiKey(
                "failed to lookup, this may be to your IP address not being linked, or your api key is invalid"
            )

        self.allowed_rate_limit = int(response.headers["hc-allowed-rate"])
        self.current_rate_limit = int(response.headers["hc-current-rate"])

        data = response.json()

        if not data["success"]:
            raise Exception(data["message"])

        return [
            Result(**_without(x, "source"), source=Source(**x["source"]))
            for x in data["results"]
        ]

    def lookup_email(self, email: str) -> list[Result]:
        return self._lookup_request("email", email)

    def lookup_username(self, username: str) -> list[Result]:
        return self._lookup_request("username", username)

    def lookup_name(self, name: str) -> list[Result]:
        return self._lookup_request("name", name)

    def lookup_ip(self, ip: str) -> list[Result]:
        return self._lookup_request("ip", ip)

    def lookup_password(self, password: str) -> list[Result]:
        return self._lookup_request("password", password)

    def lookup_phone(self, phone: str) -> list[Result]:
        return self._lookup_request("phone", phone)

    def lookup_domain(self, domain: str) -> list[Result]:
        return self._lookup_request("domain", domain)
