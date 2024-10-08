# Cachette

[![Package vesion](https://img.shields.io/pypi/v/cachette)](https://pypi.org/project/cachette)
[![Format](https://img.shields.io/pypi/format/cachette)](https://pypi.org/project/cachette)
[![Python version](https://img.shields.io/pypi/pyversions/cachette)](https://pypi.org/project/cachette)
[![License](https://img.shields.io/pypi/l/cachette)](https://pypi.org/project/cachette)
[![Top](https://img.shields.io/github/languages/top/aekasitt/cachette)](.)
[![Languages](https://img.shields.io/github/languages/count/aekasitt/cachette)](.)
[![Size](https://img.shields.io/github/repo-size/aekasitt/cachette)](.)
[![Last commit](https://img.shields.io/github/last-commit/aekasitt/cachette/master)](.)

![Cachette banner](static/cachette-banner.svg)

## Features

This is an extension aiming at making cache access on the server
By configuration at startup of the FastAPI App instance, you can set the backend and other 
configuration options and have it remain a class constant when using FastAPI's
intuitive [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/) system.

The design has built-in limitations like fixed codec and backend once the app has been launched and 
encourage developers to design their applications with this in mind.

Most of the Backend implementation is directly lifted from 
[fastapi-cache](https://github.com/long2ice/fastapi-cache) by 
[@long2ice](https://github.com/long2ice) excluding the MongoDB backend option.

## Configuration Options

The following are the current available configuration keys that can be set on this FastAPI extension
on startup either by using a method which returns a list of tuples or a Pydantic BaseSettings object
(See examples below or in `examples/` folder)

    backend -- optional; must be one of ["inmemory", "memcached", "mongodb", "pickle", "redis"];
      defaults to using inmemory option which required no extra package dependencies. To use
      other listed options; See installation guide on the README.md at
      [Repository Page](https://github.com/aekasitt/cachette).
    codec -- optional; serialization and de-serialization format to have cache values stored in
      the cache backend of choice as a string of selected encoding. once fetched, will have their
      decoded values returned of the same format. must be one of ["feather", "msgpack", "parquet",
      "pickle"]; if none is defined, will vanilla codec of basic string conversion will be used.
    database_name -- required when backend set to "mongodb"; the database name to be automatically
      created if not exists on the MongoDB instance and store the cache table; defaults to
      "cachette-db"
    memcached_host -- required when backend set to "memcached"; the host endpoint to the memcached
      distributed memory caching system.
    mongodb_url -- required when backend set to "mongodb"; the url set to MongoDB database
      instance with or without provided authentication in such formats
      "mongodb://user:password@host:port" and "mongodb://host:port" respectively.
    pickle_path -- required when backend set to "pickle"; the file-system path to create local
      store using python pickling on local directory
    redis_url -- required when backend set to "redis"; the url set to redis-server instance with
      or without provided authentication in such formats "redis://user:password@host:port" and
      "redis://host:port" respectively.
    table_name -- required when backend set to "mongodb"; name of the cache collection in case of
      "mongodb" backend to have key-value pairs stored; defaults to "cachette". 
    ttl -- optional; the time-to-live or amount before this cache item expires within the cache;
      defaults to 60 (seconds) and must be between 1 second to 1 hour (3600 seconds).
    valkey_url -- required when backend set to "valkey"; the url set to valkey-server instance
      with or without provided authentication in such formats "valkey://user:password@host:port"
      and "valkey://host:port" respectively.

## Examples

The following shows and example of setting up FastAPI Cachette in its default configuration, which
is an In-Memory cache implementation.

```py
from cachette import Cachette
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()

### Routing ###
class Payload(BaseModel):
  key: str
  value: str

@app.post('/', response_class=PlainTextResponse)
async def setter(payload: Payload, cachette: Cachette = Depends()):
  await cachette.put(payload.key, payload.value)
  return 'OK'

@app.get('/{key}', response_class=PlainTextResponse, status_code=200)
async def getter(key: str, cachette: Cachette = Depends()):
  value: str = await cachette.fetch(key)
  return value
```

And then this is how you set up a FastAPI Cachette with Redis support enabled.

```py
from cachette import Cachette
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()

@Cachette.load_config
def get_cachette_config():
  return [('backend', 'redis'), ('redis_url', 'redis://localhost:6379')]

class Payload(BaseModel):
  key: str
  value: str

@app.post('/', response_class=PlainTextResponse)
async def setter(payload: Payload, cachette: Cachette = Depends()):
  await cachette.put(payload.key, payload.value)
  return 'OK'

@app.get('/{key}', response_class=PlainTextResponse, status_code=200)
async def getter(key: str, cachette: Cachette = Depends()):
  value: str = await cachette.fetch(key)
  return value
```

## Roadmap

1. Implement `flush` and `flush_expired` methods on individual backends 
(Not needed for Redis & Memcached backends)

2. Memcached Authentication ([No SASL Support](https://github.com/aio-libs/aiomcache/issues/12))
Change library?

3. Add behaviors responding to "Cache-Control" request header

4. More character validations for URLs and Database/Table/Collection names in configuration options

## Installation

The easiest way to start working with this extension with pip

```bash
pip install cachette
# or
uv add cachette
```

When you familiarize with the basic structure of how to Dependency Inject Cachette within your
endpoints, please experiment more of using external backends with `extras` installations like

```bash
# Install FastAPI Cachette's extra requirements to Redis support
pip install cachette --install-option "--extras-require=redis"
# or Install FastAPI Cachette's support to Memcached
uv add cachette[memcached]
# or Special JSON Codec written on Rust at lightning speed
uv add cachette[orjson]
# or Include PyArrow package making DataFrame serialization much easier
pip install cachette --install-option "--extras-require=dataframe"
```

## Getting Started

This FastAPI extension utilizes "Dependency Injection" (To be continued)

Configuration of this FastAPI extension must be done at startup using "@Cachette.load_config" 
decorator (To be continued)

These are all available options with explanations and validation requirements (To be continued)

## Examples

The following examples show you how to integrate this extension to a FastAPI App (To be continued)

See "examples/" folders

To run examples, first you must install extra dependencies

Do all in one go with this command...

```bash
pip install aiomcache motor uvicorn redis
# or
uv sync --extra examples
# or
uv sync --all-extras
```

Do individual example with this command...

```bash
pip install redis
# or
uv sync --extra redis
```

## Contributions

### Prerequisites

- [python](https://www.python.org) version 3.9 or above
- [uv](https://docs.astral.sh/uv)

### Set up local environment

The following guide walks through setting up your local working environment using `pyenv`
as Python version manager and `uv` as Python package manager. If you do not have `pyenv`
installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>
  
  ```sh
  brew install pyenv --head
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>
  
  ```sh
  curl https://pyenv.run | bash
  ```
</details>

If you do not have `uv` installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>

  ```sh
  brew install uv
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>


Once you have `pyenv` Python version manager installed, you can
install any version of Python above version 3.9 for this project.
The following commands help you set up and activate a Python virtual
environment where `uv` can download project dependencies from the `PyPI`
open-sourced registry defined under `pyproject.toml` file.

<details>
  <summary> Set up environment and synchronize project dependencies </summary>

  ```sh
  pyenv install 3.9.19
  pyenv shell 3.9.19
  uv venv  --python-preference system
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

## Test Environment Setup

This project utilizes multiple external backend services namely AWS DynamoDB, Memcached, MongoDB and
Redis as backend service options as well as a possible internal option called InMemoryBackend. In
order to test viability, we must have specific instances of these set up in the background of our
testing environment. Utilize orchestration file attached to reposity and `docker-compose` command 
to set up testing instances of backend services using the following command...

```bash
docker-compose up --detach
```

When you are finished, you can stop and remove background running backend instances with the
following command...

```bash
docker-compose down
```

Now that you have background running backend instances, you can proceed with the tests by using
`pytest` command as such...

```bash
pytest
```

Or you can configure the command to run specific tests as such...

```bash
pytest -k test_load_invalid_configs
# or
pytest -k test_set_then_clear
```

All test suites must be placed under `tests/` folder or its subfolders.

## License

This project is licensed under the terms of the MIT license.
