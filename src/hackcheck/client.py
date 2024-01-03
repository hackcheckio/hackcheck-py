import httpx
from .types import (
    SearchOptions,
    SearchResponse,
    SearchResult,
    Source,
    SearchResponsePagination,
)
from .errors import (
    InvalidAPIKeyError,
    ServerError,
    UnauthorizedIPAddressError,
    RateLimitError,
)
from serde import from_dict

search_url = "https://api.hackcheck.io/search"


def _handle_error(response: httpx.Response, data: dict) -> Exception:
    if response.status_code == 401:
        if data["error"] == "Invalid API key.":
            return InvalidAPIKeyError
        elif data["error"] == "Unauthorized IP address.":
            return UnauthorizedIPAddressError
    elif response.status_code == 429:
        limit = int(response.headers.get("X-HackCheck-Limit", 0))
        remaining = int(response.headers.get("X-HackCheck-Remaining", 0))
        return RateLimitError(limit, remaining)

    return ServerError


def _generate_url(api_key: str, options: SearchOptions) -> str:
    thy_url = f"{search_url}/{api_key}/{options.field}/{options.query}"

    query = {}

    if options.filter is not None:
        query["filter"] = options.filter.type
        query["databases"] = ",".join(options.filter.databases)

    if options.pagination is not None:
        query["offset"] = str(options.pagination.offset)
        query["limit"] = str(options.pagination.limit)

    if query:
        thy_url += "?" + "&".join(f"{k}={v}" for k, v in query.items())

    return thy_url


class HackCheckClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._http = httpx.Client()

    def search(self, options: SearchOptions) -> SearchResponse:
        response = self._http.get(_generate_url(self._api_key, options))

        data = response.json()

        if response.status_code != 200:
            raise _handle_error(response, data)

        return from_dict(SearchResponse, data)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "HackCheckClient":
        return self

    def __exit__(self, *_) -> None:
        self.close()


class AsyncHackCheckClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._http = httpx.AsyncClient()

    async def search(self, options: SearchOptions) -> SearchResponse:
        response = await self._http.get(_generate_url(self._api_key, options))

        data = response.json()

        if response.status_code != 200:
            raise _handle_error(response, data)

        return from_dict(SearchResponse, data)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncHackCheckClient":
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()
