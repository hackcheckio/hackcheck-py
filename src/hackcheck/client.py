import httpx
from .types import (
    AssetMonitor,
    CheckOptions,
    CheckResponse,
    DomainMonitor,
    ErrorResponse,
    GetMonitorsResponse,
    SearchOptions,
    SearchResponse,
    Source,
    UpdateAssetMonitorParams,
    UpdateDomainMonitorParams,
)
from .endpoints import (
    EndpointCheck,
    EndpointGetAssetMonitorSources,
    EndpointGetDomainMonitorSources,
    EndpointGetAssetMonitor,
    EndpointGetDomainMonitor,
    EndpointGetMonitors,
    EndpointSearch,
    EndpointTogglePauseAssetMonitor,
    EndpointTogglePauseDomainMonitor,
    EndpointUpdateAssetMonitor,
    EndpointUpdateDomainMonitor,
)
from .errors import (
    InvalidAPIKeyError,
    ServerError,
    UnauthorizedIPAddressError,
    RateLimitError,
)
from serde import from_dict, to_dict


search_url = "https://api.hackcheck.io/search"


def _generate_search_url(api_key: str, options: SearchOptions) -> str:
    thy_url = EndpointSearch(api_key, options.field, options.query)

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
        self._http = httpx.AsyncClient()

    async def _request(self, method: str, url: str, body: dict | None) -> dict:
        response = await self._http.request(method, url, json=body)

        if response.status_code == 401:
            data = from_dict(ErrorResponse, response.json())
            if data.error == "Invalid API key.":
                raise InvalidAPIKeyError
            elif data.error == "Unauthorized IP address.":
                raise UnauthorizedIPAddressError
            else:
                raise ServerError
        elif response.status_code == 429:
            limit = int(response.headers.get("X-HackCheck-Limit", 0))
            remaining = int(response.headers.get("X-HackCheck-Remaining", 0))
            raise RateLimitError(limit, remaining)
        elif response.status_code == 400:
            data = from_dict(ErrorResponse, response.json())
            raise Exception(data.error)
        elif response.status_code == 404:
            raise Exception("endpoint not found")

        return response.json()

    async def search(self, options: SearchOptions) -> SearchResponse:
        resp = await self._request(
            "get", _generate_search_url(self._api_key, options), None
        )

        return from_dict(SearchResponse, resp)

    async def check(self, options: CheckOptions) -> bool:
        resp = await self._request(
            "get", EndpointCheck(self._api_key, options.field, options.query), None
        )

        return from_dict(CheckResponse, resp).found

    async def get_monitors(self) -> GetMonitorsResponse:
        resp = await self._request("get", EndpointGetMonitors(self._api_key), None)

        return from_dict(GetMonitorsResponse, resp)

    async def get_asset_monitor(self, monitor_id: str) -> AssetMonitor:
        resp = await self._request(
            "get", EndpointGetAssetMonitor(self._api_key, monitor_id), None
        )

        return from_dict(AssetMonitor, resp)

    async def get_domain_monitor(self, monitor_id: str) -> DomainMonitor:
        resp = await self._request(
            "get", EndpointGetDomainMonitor(self._api_key, monitor_id), None
        )

        return from_dict(DomainMonitor, resp)

    async def get_asset_monitor_sources(self, monitor_id: str) -> list[Source]:
        resp = await self._request(
            "get", EndpointGetAssetMonitorSources(self._api_key, monitor_id), None
        )

        return from_dict(list[Source], resp)

    async def get_domain_monitor_sources(self, monitor_id: str) -> list[Source]:
        resp = await self._request(
            "get", EndpointGetDomainMonitorSources(self._api_key, monitor_id), None
        )

        return from_dict(list[Source], resp)

    async def toggle_pause_assset_monitor(self, monitor_id: str) -> AssetMonitor:
        resp = await self._request(
            "post", EndpointTogglePauseAssetMonitor(self._api_key, monitor_id), None
        )

        return from_dict(AssetMonitor, resp)

    async def toggle_pause_domain_monitor(self, monitor_id: str) -> DomainMonitor:
        resp = await self._request(
            "post", EndpointTogglePauseDomainMonitor(self._api_key, monitor_id), None
        )

        return from_dict(DomainMonitor, resp)

    async def update_asset_monitor(
        self, monitor_id: str, params: UpdateAssetMonitorParams
    ) -> AssetMonitor:
        resp = await self._request(
            "put",
            EndpointUpdateAssetMonitor(self._api_key, monitor_id),
            to_dict(params),
        )

        return from_dict(AssetMonitor, resp)

    async def update_domain_monitor(
        self, monitor_id: str, params: UpdateDomainMonitorParams
    ) -> DomainMonitor:
        resp = await self._request(
            "put",
            EndpointUpdateDomainMonitor(self._api_key, monitor_id),
            to_dict(params),
        )

        return from_dict(DomainMonitor, resp)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "HackCheckClient":
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()
