#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:    ~~/tests/codecs/unfrozen.py
# VERSION:     0.1.8
# CREATED:     2022-04-06 22:03
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Tests for codec implementations on TestClient which can encode/decode frozen objects fully"""

### Standard packages ###
from contextlib import asynccontextmanager
from datetime import date, datetime
from decimal import Decimal
from typing import Any, AsyncGenerator, List, Tuple

### Third-party packages ###
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient
from httpx import Response
from pytest import FixtureRequest, fixture, mark
from pytest_asyncio import fixture as asyncfixture

### Local modules ###
from cachette import Cachette


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
    {1, 2, 3},  # Set of numbers
    {"a", "b", "c"},  # Set of charstrings
    {b"a", b"b", b"c"},  # Set of charbytes
    Decimal(12345.67890),  # Decimal
    date.today(),  # Date
    datetime.now(),  # Datetime
  ]


@asynccontextmanager
@asyncfixture(scope="function")
async def client(items: List[Any], request: FixtureRequest) -> AsyncGenerator[TestClient, None]:
  configs: List[Tuple[str, Any]] = request.param

  app: FastAPI = FastAPI()

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
        ok = False
        break
    return ("", "OK")[ok]

  with TestClient(app) as test_client:
    yield test_client


@mark.parametrize(
  "client",
  [
    ### InMemory & Codecs ###
    [("backend", "inmemory"), ("codec", "pickle")],
    ### Memcached & Codecs ###
    [
      ("backend", "memcached"),
      ("codec", "pickle"),
      ("memcached_host", "localhost"),
    ],
    ### MongoDB & Codecs ###
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("codec", "pickle"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    ### Redis & Codecs ###
    [
      ("backend", "redis"),
      ("codec", "pickle"),
      ("redis_url", "redis://localhost:6379"),
    ],
  ],
  ids=[
    "inmemory-pickle",
    "memcached-pickle",
    "mongodb-pickle",
    "redis-pickle",
  ],
  indirect=True,
)
def test_every_backend_with_every_codec(client) -> None:
  response: Response = client.get("/put-items")
  assert response.text == "OK"
  response = client.get("/fetch-items")
  assert response.text == "OK"
