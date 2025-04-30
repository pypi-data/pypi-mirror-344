<p align="center">
  <a href="https://github.com/AlexDemure/gadfastrouter">
    <a href="https://ibb.co/TBqwVMMp"><img src="https://i.ibb.co/ccXyGhhM/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A FastAPI routing extension that provides detailed request/response logging
</p>

---

## Installation

```
pip install gadfastrouter
```


## Usage

```python
# global override

import fastapi

from gadfastrouter import APIRoute
from sgadfastrouter import APIRouter

fastapi.routing.APIRoute = APIRoute
fastapi.APIRouter = APIRouter

from endpoints import router

app.include_router(router)
```
