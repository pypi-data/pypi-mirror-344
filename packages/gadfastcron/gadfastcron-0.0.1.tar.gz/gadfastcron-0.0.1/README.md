<p align="center">
  <a href="https://github.com/AlexDemure/gadfastcron">
    <a href="https://ibb.co/24XqKh3"><img src="https://i.ibb.co/rrnky02/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  Wrapper around APScheduler for managing scheduled tasks
</p>

---

## Installation

```
pip install gadfastcron
```

## Usage

```python
import contextlib

from fastapi import FastAPI

from gadfastcron import Cron
from gadfastcron import jobstores, triggers

def func():
    print('test')

cron = Cron(
    jobstores.Sqlalchemy(dsn).store,
    (func, triggers.cron.everyday()), 
)

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    cron.start()
    yield
    cron.shutdown()


app = FastAPI(lifespan=lifespan)
```
