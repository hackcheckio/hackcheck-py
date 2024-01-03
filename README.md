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

```py
from hackcheck import Hackcheck

# Get an api key by purchasing a developer plan https://hackcheck.io/plans
hc = Hackcheck("MY_API_KEY")

result = hc.lookup_email("your@email.com")

for r in result:
    print(f"Database: {r.source.name}")
    print(f"Date: {r.source.date}")
    print(f"Password: {r.password}")
    print(f"Username: {r.username}")
    print(f"IP: {r.ip}")
    print("------")

# Check your ratelimits
print(f"Current rate limit: {hc.current_rate_limit}")
print(f"Allowed rate limit: {hc.allowed_rate_limit}")
```

## Methods

```py
hc.lookup_email("your@email.com")
hc.lookup_username("username")
hc.lookup_password("password")
hc.lookup_name("Full Name")
hc.lookup_ip("8.8.8.8")
hc.lookup_phone("1234567890")
hc.lookup_domain("hackcheck.io")
```

## Getting your api key

1. Visit https://hackcheck.io/profile
2. Add your IP address in the "Authorized IP Addresses" text area and click Update
3. Copy your API key
