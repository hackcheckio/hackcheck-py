# HackCheck-py

Official python library for the [hackcheck.io](https://hackcheck.io) API

- [HackCheck-py](#hackcheck-py)
  - [Installation](#installation)
  - [Quick start](#quick-start)
  - [Getting your api key](#getting-your-api-key)
  - [Other examples](#other-examples)

## Installation

Install with pip

```sh
pip install hackcheck
```

## Quick start

Example usage

```py
import asyncio

from hackcheck import (
    HackCheckClient,
    SearchFieldEmail,
    SearchOptions,
)


async def main() -> None:
    async with HackCheckClient("MY_API_KEY") as hc:
        breaches = await hc.search(
            SearchOptions(
                field=SearchFieldEmail,
                query="hello@gmail.com",
            )
        )

        print(breaches.results)


asyncio.run(main())
```

## Getting your api key

1. Visit https://hackcheck.io/profile
2. Add your IP address in the "Authorized IP Addresses" text area and click Update
3. Copy your API key

## Other examples

<details>
<summary>Breach Monitors</summary>

```py
import asyncio

from hackcheck import HackCheckClient, UpdateDomainMonitorParams


async def main() -> None:
    async with HackCheckClient("MY_API_KEY") as hc:
        monitors = await hc.get_monitors()

        print(monitors.asset_monitors)
        print(monitors.domain_monitors)

        my_asset_monitor = await hc.get_asset_monitor("...")  # or hc.get_domain_monitor

        print(my_asset_monitor.status)
        print(my_asset_monitor.asset)

        # Updating a monitor
        domain_monitor = await hc.update_domain_monitor(
            "id123123123",
            UpdateDomainMonitorParams(
                domain="website.com",
                notification_email="notifications@example.com",
            ),
        )

        print(domain_monitor.domain)


asyncio.run(main())
```

</details>

<details>
<summary>Filtering databases</summary>

```py
import asyncio

from hackcheck import (
    HackCheckClient,
    SearchFieldEmail,
    SearchFilterOptions,
    SearchFilterUse,
    SearchOptions,
)


async def main() -> None:
    async with HackCheckClient("MY_API_KEY") as hc:
        # This will only yield results from "website.com" and "website.org"
        breaches = await hc.search(
            SearchOptions(
                field=SearchFieldEmail,
                query="example@example.com",
                filter=SearchFilterOptions(
                    type=SearchFilterUse, databases=["website.com", "other.com"]
                ),
            )
        )

        print(breaches.results)


asyncio.run(main())
```

</details>

<details>
<summary>Checking if a query exists</summary>

```py
import asyncio

from hackcheck import (
    CheckOptions,
    SearchFieldEmail,
    HackCheckClient,
)


async def main() -> None:
    async with HackCheckClient("MY_API_KEY") as hc:
        exists = await hc.check(
            CheckOptions(
                field=SearchFieldEmail,
                query="example@example.com",
            )
        )

        print(exists)


asyncio.run(main())
```

</details>
