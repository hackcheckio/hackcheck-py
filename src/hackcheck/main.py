import datetime
from typing import NamedTuple, Optional, NewType, List, Union
import httpx
from dataclasses import dataclass
from serde import serde, from_dict, to_dict


# Exception classes
class RateLimitError(Exception):
    def __init__(self, limit: int, remaining_requests: int):
        self.limit = limit
        self.remaining_requests = remaining_requests
        super().__init__(f"Rate limit reached: {limit} requests allowed, {remaining_requests} remaining.")

class UnauthorizedIPAddressError(Exception):
    pass

class InvalidAPIKeyError(Exception):
    pass

class ServerError(Exception):
    pass


# API URL
API_BASE_URL = "https://api.hackcheck.io"


# API Data Structures
@serde
@dataclass
class ErrorResponse:
    error: str

@serde
@dataclass
class CheckResponse:
    found: bool

MonitorStatus = NewType("MonitorStatus", int)
MonitorStatusRunning = 0
MonitorStatusPaused = 1
MonitorStatusExpired = 2

@serde
@dataclass
class Source:
    name: str
    date: str

@serde
@dataclass
class SearchResult:
    email: str
    password: str
    username: str
    full_name: str
    ip_address: str
    phone_number: str
    hash: str
    source: Source

@serde
@dataclass
class PaginationData:
    offset: int
    limit: int

@serde
@dataclass
class SearchResponsePagination:
    document_count: int
    next: Optional[PaginationData]
    prev: Optional[PaginationData]

@serde
@dataclass
class SearchResponse:
    databases: int
    results: List[SearchResult]
    pagination: Optional[SearchResponsePagination]
    first_seen: str
    last_seen: str

SearchFilter = NewType("SearchFilter", str)
SearchFilterUse = SearchFilter("use")
SearchFilterIgnore = SearchFilter("ignore")

class SearchFilterOptions(NamedTuple):
    type: SearchFilter
    databases: List[str]

class SearchPaginationOptions(NamedTuple):
    offset: int
    limit: int

SearchField = NewType("SearchField", str)
SearchFieldEmail = SearchField("email")
SearchFieldUsername = SearchField("username")
SearchFieldFullName = SearchField("full_name")
SearchFieldPassword = SearchField("password")
SearchFieldIPAddress = SearchField("ip_address")
SearchFieldPhoneNumber = SearchField("phone_number")
SearchFieldDomain = SearchField("domain")
SearchFieldHash = SearchField("hash")

class SearchOptions(NamedTuple):
    field: SearchField
    query: str
    filter: Optional[SearchFilterOptions] = None
    pagination: Optional[SearchPaginationOptions] = None

class CheckOptions(NamedTuple):
    field: SearchField
    query: str

@serde
@dataclass
class AssetMonitor:
    id: str
    status: MonitorStatus
    type: SearchField
    asset: str
    notification_email: str
    expires_soon: bool
    created_at: datetime.datetime
    ends_at: datetime.datetime

@serde
@dataclass
class DomainMonitor:
    id: str
    status: MonitorStatus
    domain: str
    notification_email: str
    expires_soon: bool
    created_at: datetime.datetime
    ends_at: datetime.datetime

@serde
@dataclass
class GetMonitorsResponse:
    asset_monitors: List[AssetMonitor]
    domain_monitors: List[DomainMonitor]

@serde
@dataclass
class UpdateAssetMonitorParams:
    asset_type: SearchField
    asset: str
    notification_email: str

@serde
@dataclass
class UpdateDomainMonitorParams:
    domain: str
    notification_email: str


# Client Class
class HackCheckClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._http = httpx.AsyncClient()

    async def _request(self, method: str, url: str, body: Optional[dict] = None) -> dict:
        headers = {"Authorization": f"Bearer {self._api_key}"}
        response = await self._http.request(method, url, json=body, headers=headers)

        if response.status_code == 401:
            data = from_dict(ErrorResponse, response.json())
            if data.error == "Invalid API key.":
                raise InvalidAPIKeyError("The provided API key is invalid.")
            elif data.error == "Unauthorized IP address.":
                raise UnauthorizedIPAddressError("The request is coming from an unauthorized IP address.")
            else:
                raise ServerError("An unknown server error occurred.")
        elif response.status_code == 429:
            limit = int(response.headers.get("X-HackCheck-Limit", 0))
            remaining = int(response.headers.get("X-HackCheck-Remaining", 0))
            raise RateLimitError(limit, remaining)
        elif response.status_code in {400, 404}:
            data = from_dict(ErrorResponse, response.json())
            raise Exception(data.error)

        return response.json()

    async def search(self, options: SearchOptions) -> SearchResponse:
        url = self._generate_search_url(options)
        resp = await self._request("GET", url)
        return from_dict(SearchResponse, resp)

    async def check(self, options: CheckOptions) -> bool:
        url = f"{API_BASE_URL}/check"
        body = to_dict(options)
        resp = await self._request("POST", url, body)
        return from_dict(CheckResponse, resp).found

    async def get_monitors(self) -> GetMonitorsResponse:
        url = f"{API_BASE_URL}/monitors"
        resp = await self._request("GET", url)
        return from_dict(GetMonitorsResponse, resp)

    async def update_asset_monitor(
        self, monitor_id: str, params: UpdateAssetMonitorParams
    ) -> AssetMonitor:
        url = f"{API_BASE_URL}/monitors/asset/{monitor_id}"
        resp = await self._request("PUT", url, to_dict(params))
        return from_dict(AssetMonitor, resp)

    async def update_domain_monitor(
        self, monitor_id: str, params: UpdateDomainMonitorParams
    ) -> DomainMonitor:
        url = f"{API_BASE_URL}/monitors/domain/{monitor_id}"
        resp = await self._request("PUT", url, to_dict(params))
        return from_dict(DomainMonitor, resp)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "HackCheckClient":
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    def _generate_search_url(self, options: SearchOptions) -> str:
        url = f"{API_BASE_URL}/search/{options.field}/{options.query}"

        params = []
        if options.filter:
            params.append(f"filter={options.filter.type}")
            params.append(f"databases={','.join(options.filter.databases)}")
        if options.pagination:
            params.append(f"offset={options.pagination.offset}")
            params.append(f"limit={options.pagination.limit}")

        if params:
            url += "?" + "&".join(params)

        return url


# Example Usage
async def main():
    # Print the ASCII art on execution
    ascii_art = r"""
    ██   ██  █████   ██████ ██   ██      ██████ ██   ██ ███████  ██████ ██   ██    
    ██   ██ ██   ██ ██      ██  ██      ██      ██   ██ ██      ██      ██  ██     
    ███████ ███████ ██      █████       ██      ███████ █████   ██      █████      
    ██   ██ ██   ██ ██      ██  ██      ██      ██   ██ ██      ██      ██  ██     
    ██   ██ ██   ██  ██████ ██   ██      ██████ ██   ██ ███████  ██████ ██   ██    
                                                                                   

 █████  ██████  ██     ███████  ██████  █████  ███    ██ ███    ██ ███████ ██████  
██   ██ ██   ██ ██     ██      ██      ██   ██ ████   ██ ████   ██ ██      ██   ██ 
███████ ██████  ██     ███████ ██      ███████ ██ ██  ██ ██ ██  ██ █████   ██████  
██   ██ ██      ██          ██ ██      ██   ██ ██  ██ ██ ██  ██ ██ ██      ██   ██ 
██   ██ ██      ██     ███████  ██████ ██   ██ ██   ████ ██   ████ ███████ ██   ██ 
    """
    print(ascii_art)

    api_key = "YOUR_API_KEY"  # Replace with your actual API key

    async with HackCheckClient(api_key) as client:
        # Search example
        search_options = SearchOptions(
            field=SearchFieldEmail,
            query="example@example.com",
            pagination=SearchPaginationOptions(offset=0, limit=10)
        )
        search_results = await client.search(search_options)
        print(search_results)

        # Check example
        check_options = CheckOptions(field=SearchFieldEmail, query="check@example.com")
        found = await client.check(check_options)
        print(f"Email found: {found}")

        # Get monitors
        monitors = await client.get_monitors()
        print(monitors)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
