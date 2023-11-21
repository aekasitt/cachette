#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  tests/codecs/primitives.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-06 3:27
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Tests for codec implementations on TestClient which can encode/decode primitives with correct types
"""
### Standard Packages ###
from typing import Any, List, Tuple

### Third-Party Packages ###
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse, Response
from fastapi.testclient import TestClient
from pytest import fixture, FixtureRequest, mark

### Local Modules ###
from fastapi_cachette import Cachette

### Fixtures ###


@fixture(scope="module")
def items() -> List[Any]:
    return [
        None,
        123,  # Integer
        123.45,  # Float
        "A",  # Charstring
        "Hello, World!",  # String
        "123",  # Alphanumeric String of an integer
        "123.45",  # Alphanumeric String of a float
        b"A",  # Charbytes
        b"Hello, World!",  # Bytes
        b"123",  # Alphanumeric Bytes of an integer
        b"123.45",  # Alphanumeric Bytes of a float
        {"a": "b", "c": "d"},  # Dictionary with String values
        {"a": b"b", "c": b"d"},  # Dictionary with Byte values
        {"a": 1, "b": 2},  # Dictionary with Integer values
        {"a": 1.2, "b": 3.4},  # Dictionary with Float values
        [1, 2, 3],  # List of numbers
        ["a", "b", "c"],  # List of charstrings
        [b"a", b"b", b"c"],  # List of charbytes
    ]


@fixture
def client(items: List[Any], request: FixtureRequest) -> TestClient:
    configs: List[Tuple[str, Any]] = request.param

    app = FastAPI()

    @Cachette.load_config
    def get_cachette_config():
        return configs

    ### Routing ###
    @app.get("/put-items", response_class=PlainTextResponse, status_code=200)
    async def put_items(cachette: Cachette = Depends()):
        """
        Puts a list of pre-determined items to cache
        """
        for i, item in enumerate(items):
            await cachette.put(f"{ i }", item)
        return "OK"

    @app.get("/fetch-items", response_class=PlainTextResponse, status_code=200)
    async def fetch_items(cachette: Cachette = Depends()):
        """
        Returns key value
        """
        ok: bool = True
        for i, item in enumerate(items):
            uncached: Any = await cachette.fetch(f"{ i }")
            if uncached != item:
                print(uncached)
                ok = False
                break
        return ("", "OK")[ok]

    return TestClient(app)


@mark.parametrize(
    "client",
    [
        ### DynamoDB & Codecs ###
        [
            ("backend", "dynamodb"),
            ("codec", "msgpack"),
            ("dynamodb_url", "http://localhost:8000"),
        ],
        ### InMemory & Codecs ###
        [("backend", "inmemory"), ("codec", "msgpack")],
        ### Memcached & Codecs ###
        [
            ("backend", "memcached"),
            ("codec", "msgpack"),
            ("memcached_host", "localhost"),
        ],
        ### MongoDB & Codecs ###
        [
            ("backend", "mongodb"),
            ("database_name", "fastapi-cachette-database"),
            ("codec", "msgpack"),
            ("mongodb_url", "mongodb://localhost:27017"),
        ],
        ### Redis & Codecs ###
        [
            ("backend", "redis"),
            ("codec", "msgpack"),
            ("redis_url", "redis://localhost:6379"),
        ],
    ],
    ids=[
        "dynamodb-msgpack",
        "inmemory-msgpack",
        "memcached-msgpack",
        "mongodb-msgpack",
        "redis-msgpack",
    ],
    indirect=True,
)
def test_every_backend_with_every_codec(client) -> None:
    response: Response = client.get("/put-items")
    assert response.text == "OK"
    response = client.get("/fetch-items")
    assert response.text == "OK"
