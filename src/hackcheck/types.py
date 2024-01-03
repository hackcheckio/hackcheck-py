from typing import NamedTuple, Optional, NewType

from dataclasses import dataclass
from serde import serde


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
    error: str | None


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
