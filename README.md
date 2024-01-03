# HackCheck-py

Official python library for the [hackcheck.io](https://hackcheck.io) API

- [HackCheck-py](#hackcheck-py)
  - [Installation](#installation)
  - [Quick start](#quick-start)
  - [Methods](#methods)

## Installation

Install with pip

```sh
pip install hackcheck
```

## Quick start

Example usage

```py
from hackcheck import HackCheckClient, SearchFieldEmail, SearchOptions

with HackCheckClient("MY_API_KEY") as hc:
    resp = hc.search(
        SearchOptions(
            field=SearchFieldEmail,
            query="example@example.com",
        ),
    )

    print(resp.results)
```

## Getting your api key

1. Visit https://hackcheck.io/profile
2. Add your IP address in the "Authorized IP Addresses" text area and click Update
3. Copy your API key
