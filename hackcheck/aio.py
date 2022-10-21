import aiohttp

from .errors import InvalidApiKey
from .types import Result, Source

BASE_URL = "https://api.hackcheck.io/v3/lookup"

_without = lambda d, w: {k: v for k, v in d.items() if k != w}


class AIOHackcheck:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.allowed_rate_limit = 0
        self.current_rate_limit = 0

        self._session = aiohttp.ClientSession()

        assert self.api_key != ""

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def _lookup_request(self, q: str, inp: str) -> list[Result]:
        async with self._session.get(
            f"{BASE_URL}/{self.api_key}/{q}/{inp}"
        ) as response:
            if response.status == 401:
                raise InvalidApiKey(
                    "failed to lookup, this may be to your IP address not being linked, or your api key is invalid"
                )

            self.allowed_rate_limit = int(response.headers["hc-allowed-rate"])
            self.current_rate_limit = int(response.headers["hc-current-rate"])

            data = await response.json()

            if not data["success"]:
                raise Exception(data["message"])

            return [
                Result(**_without(x, "source"), source=Source(**x["source"]))
                for x in data["results"]
            ]

    async def lookup_email(self, email: str) -> list[Result]:
        return await self._lookup_request("email", email)

    async def lookup_username(self, username: str) -> list[Result]:
        return await self._lookup_request("username", username)

    async def lookup_name(self, name: str) -> list[Result]:
        return await self._lookup_request("name", name)

    async def lookup_ip(self, ip: str) -> list[Result]:
        return await self._lookup_request("ip", ip)

    async def lookup_password(self, password: str) -> list[Result]:
        return await self._lookup_request("password", password)

    async def lookup_phone(self, phone: str) -> list[Result]:
        return await self._lookup_request("phone", phone)

    async def lookup_domain(self, domain: str) -> list[Result]:
        return await self._lookup_request("domain", domain)
