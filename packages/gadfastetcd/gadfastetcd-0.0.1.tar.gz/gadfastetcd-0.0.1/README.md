<p align="center">
  <a href="https://github.com/AlexDemure/gadfastetcd">
    <a href="https://ibb.co/ZzpzbS7g"><img src="https://i.ibb.co/pjBjkQ5K/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A FastAPI integration with Etcd for managing configuration settings via a RESTful API
</p>

---

### Installation

```
pip install gadfastetcd
```

### Usage

#### API
Set
```curl
curl -X 'PUT' \
  'http://127.0.0.1:8000/-/etcd' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "test": 1
}
```
Get
```
curl -X 'GET' \
  'http://127.0.0.1:8000/-/etcd' \
  -H 'accept: application/json'

{
  "test": 1
}
```

#### Code
```python
import pydantic

import fastapi

from gadfastetcd import Etcd

class Settings(pydantic.BaseModel):
    class Config:
        extra = "allow"

settings = Settings()

etcd = Etcd(url="localhost:2379", storage="/{service_name}/{environment}", settings=settings)

app = fastapi.FastAPI()

app.include_router(etcd.router)

>>> settings.test
```
