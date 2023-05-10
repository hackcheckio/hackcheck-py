from typing import NamedTuple, Optional


class Source(NamedTuple):
    name: Optional[str]
    date: Optional[str]
    description: Optional[str]


class Result(NamedTuple):
    email: Optional[str]
    username: Optional[str]
    name: Optional[str]
    password: Optional[str]
    ip: Optional[str]
    phone: Optional[str]
    source: Optional[Source]
