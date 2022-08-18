# Hackcheck-py
A python wrapper for [hackcheck.io](https://hackcheck.io)'s API

## Installation

Install with pip

```sh
pip install -U git+https://github.com/hackcheckio/hackcheck-py
```

## Usage

```py
from hackcheck import Hackcheck

hc = Hackcheck("your hackcheck api key")

# Returns a list of Result objects
result = hc.lookup_email("your@email.com")

for r in result:
    print(f"{r.email}:{r.password}")
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
