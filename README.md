# Cachette

[![Build status](https://travis-ci.com/aekasitt/cachette.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/cachette)
[![Package vesion](https://img.shields.io/pypi/v/cachette)](https://pypi.org/project/cachette)
[![Format](https://img.shields.io/pypi/format/cachette)](https://pypi.org/project/cachette)
[![Python version](https://img.shields.io/pypi/pyversions/cachette)](https://pypi.org/project/cachette)
[![License](https://img.shields.io/pypi/l/cachette)](https://pypi.org/project/cachette)

## Features

Opinionated cache extension for ASGI frameworks such as FastAPI, Quartz, Starlette and Unicorn;
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

    backend -- optional; must be one of ["dynamodb", "inmemory", "memcached", "mongodb", "redis"];
      defaults to using inmemory option which required no extra package dependencies. To use other
      listed options;
    codec -- optional; serialization and de-serialization format to have cache values stored in
      the cache backend of choice as a string of selected encoding. once fetched, will have their
      decoded values returned of the same format. must be one of ["feather", "msgpack", "parquet",
      "pickle"]; if none is defined, will vanilla codec of basic string conversion will be used.
    ttl -- optional; the time-to-live or amount before this cache item expires within the cache;
      defaults to 60 (seconds) and must be between 1 second to 1 hour (3600 seconds).
    redis_url -- required when backend set to "redis"; the url set to redis-server instance with
      or without provided authentication in such formats "redis://user:password@host:port" and
      "redis://host:port" respectively.
    memcached_host -- required when backend set to "memcached"; the host endpoint to the memcached
      distributed memory caching system.
    table_name -- required when backend set to "dynamodb" or "mongodb"; name of the cache table or
      collection in case of "mongodb" backend to have key-value pairs stored; defaults to
      "cachette".
    region -- required when backend set to "dynamodb" and "dynamodb_url" not set; one of Amazon
      Web Services listed Regions which can be found on this Documentation
      [Page](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones)
    dynamodb_url -- required when backend set to "dynamodb" and "region" not set; this option is
      used when setting up your own DynamoDB Local instance according to this
      [Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal)
    database_name -- required when backend set to "mongodb"; the database name to be automatically
      created if not exists on the MongoDB instance and store the cache table; defaults to
      "cachette-db"
    mongodb_url -- required when backend set to "mongodb"; the url set to MongoDB database
      instance with or without provided authentication in such formats
      "mongodb://user:password@host:port" and "mongodb://host:port" respectively.

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

## Upcoming Features (To-Do List)

1. Implement `flush` and `flush_expired` methods on individual backends 
(Not needed for Redis & Memcached backends)

2. Memcached Authentication ([No SASL Support](https://github.com/aio-libs/aiomcache/issues/12))
Change library?

3. DynamoDB Authentication (Add AWS Access Key ID and AWS Access Secret Key to configuration).

4. Boto3 Version Fix; Current version restrictions vulnerable to `aiohttp` bug.

5. Add behaviors responding to "Cache-Control" request header

6. More character validations for URLs and Database/Table/Collection names in configuration options

## Installation

The easiest way to start working with this extension with pip

```bash
pip install cachette
# or
poetry add cachette
```

When you familiarize with the basic structure of how to Dependency Inject Cachette within your
endpoints, please experiment more of using external backends with `extras` installations like

```bash
# Install FastAPI Cachette's extra requirements to Redis support
pip install cachette --install-option "--extras-require=redis"
# or Install FastAPI Cachette's support to Memcached
poetry add cachette[memcached]
# or Special JSON Codec written on Rust at lightning speed
poetry add cachette[orjson]
# or Include PyArrow package making DataFrame serialization much easier
pip install cachette --install-option "--extras-require=dataframe"
# or MongoDB and DynamoDB supports
poetry add cachette[mongodb]
pip install cachette --install-option "--extras-require=dynamodb"
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
pip install aiobotocore aiomcache motor uvicorn redis
# or
poetry install --extras examples
```

Do individual example with this command...

```bash
pip install redis
# or
poetry install --extras redis
```

## Contributions

See features and write tests I guess.

## Test Environment Setup

This project utilizes multiple external backend services namely AWS DynamoDB, Memcached, MongoDB and
Redis as backend service options as well as a possible internal option called InMemoryBackend. In
order to test viability, we must have specific instances of these set up in the background of our
testing environment 

### With Docker-Compose

Utilize orchestration file attached to reposity and `docker-compose` command to set up testing 
instances of backend services using the following command...

```bash
docker-compose up -d
```

When you are finished, you can stop and remove background running backend instances with the
following command...

```bash
docker-compose down
```

### Without Docker-Compose

If you are using `arm64` architecture on your local machine like I am with my fancy MacBook Pro, 
there is a chance that your `docker-compose` (V1) is not properly configured and have caused you 
many headaches. The following commands will allow you to replicate docker-compose orchestration
command given above.


1. AWS DynamoDB Local

    ```bash
    docker run --detach --rm -ti -p 8000:8000 --name cachette-dynamodb amazon/dynamodb-local:latest
    ```

2. Memcached

    ```bash
    docker run --detach --rm -ti -p 11211:11211 --name cachette-memcached memcached:bullseye
    ```

3. MongoDB

    ```bash
    docker run --detach --rm -ti -p 27017:27017 --name cachette-mongodb mongo:latest
    ```

4. Redis

    ```bash
    docker run --detach --rm -ti -p 6379:6379 --name cachette-redis redis:bullseye
    ```

And finally, to stop and remove running instances, run the following command

```bash
[ ! -z $(docker ps -f name="cachette-*" -q | tr -d '\n') ] \
  && docker kill $(docker ps -f name="cachette-*" -q)
```

## Tests

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