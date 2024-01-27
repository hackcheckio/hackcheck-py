import datetime
from typing import NamedTuple, Optional, NewType

from dataclasses import dataclass
from serde import serde


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
    next: PaginationData | None
    prev: PaginationData | None


@serde
@dataclass
class SearchResponse:
    databases: int
    results: list[SearchResult]
    pagination: SearchResponsePagination | None


SearchFilter = NewType("SearchFilter", str)
SearchFilterUse = SearchFilter("use")
SearchFilterIgnore = SearchFilter("ignore")


class SearchFilterOptions(NamedTuple):
    type: SearchFilter
    databases: list[str]


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
    filter: SearchFilterOptions | None = None
    pagination: SearchPaginationOptions | None = None


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
    asset_monitors: list[AssetMonitor]
    domain_monitors: list[DomainMonitor]


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
