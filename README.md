# FastAPI Cachette

[![Build Status](https://travis-ci.com/aekasitt/fastapi-cachette.svg?branch=master)](https://app.travis-ci.com/github/aekasitt/fastapi-cachette)
[![Package Vesion](https://img.shields.io/pypi/v/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)
[![Format](https://img.shields.io/pypi/format/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)
[![License](https://img.shields.io/pypi/l/fastapi-cachette)](https://pypi.org/project/fastapi-cachette)

## Features

Cache Extension for FastAPI Asynchronous Web Framework
Most of the Backend implementation is directly lifted from 
[fastapi-cache](https://github.com/long2ice/fastapi-cache) by 
[@long2ice](https://github.com/long2ice) excluding the MongoDB backend option.

## Upcoming Features (To-Do List)

1. Implement `flush` and `flush_expired` methods on individual backends 
(Not needed for Redis & Memcached backends)

2. Implement options for encoding/decoding cache data using built-in protocols such as pickle, json
or third-party protocol such as msgpack, parquet, feather, hdf5

3. Write more examples

## Installation

The easiest way to start working with this extension with pip

```bash
pip install fastapi-cachette
# or
poetry add fastapi-cachette
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
# or
poetry install --extras `<example-name>`
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
[ -n $(docker ps -f name="cachette-*" -q) ] && docker kill $(docker ps -f name="cachette-*" -q)
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