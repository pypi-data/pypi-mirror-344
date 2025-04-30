# security.dev Python Client (`securitydev`)

[![PyPI version](https://badge.fury.io/py/securitydev.svg)](https://badge.fury.io/py/securitydev)

A modern Python client for the [security.dev API](https://docs.security.dev/), built using `httpx` and `pydantic`. Supports both **synchronous** (default) and **asynchronous** usage.

## Features

*   Synchronous and Asynchronous interfaces.
*   Data validation using `pydantic`.
*   Simple and intuitive interface.
*   Type-hinted.

## Installation

Install using `pip` (or any other manager):

```bash
pip install securitydev
```

## Requirements

- Python 3.8+
- A security.dev API key, available from security.dev. 


## Quick Examples

### Synchronous Usage

```python 
import os
from securitydev import SecurityClient

key = os.getenv("SECURITYDEV_KEY")

with SecurityClient(key=key) as client:
    reputation = client.ip_intel.reputation("8.8.8.8")
    print(f"8.8.8.8 - Is Abuser: {reputation.is_abuser}")
```

You don't necessarily need to use the context manager.

```python
import os
from securitydev import SecurityClient

key = os.getenv("SECURITYDEV_KEY")

client = SecurityClient(key=key)
ip = "1.1.1.1"
rep = client.ip_intel.reputation(ip)
if rep.is_tor_exit:
    print(f"{ip} is a Tor exit.")
```

### Asynchronous Usage

```python
import os
import asyncio
from securitydev import AsyncSecurityClient

async def main():
    async with AsyncSecurityClient(key=os.getenv("SECURITYDEV_KEY")) as client:
        geoip = await client.ip_intel.geolocate("1.1.1.1")
        print(f"1.1.1.1 - Country: {geoip.country.name}")

asyncio.run(main())
```
