#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  tests/codecs/none.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-06 3:27
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Tests for codec implementations on TestClient which serializes, deserializes in JSON format"""

### Standard packages ###
from contextlib import asynccontextmanager
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
    {"a": "b", "c": "d"},  # Dictionary with String values
    {"a": 1, "b": 2},  # Dictionary with Integer values
    {"a": 1.2, "b": 3.4},  # Dictionary with Float values
    [1, 2, 3],  # List of integers
    [1.1, 2.2, 3.3],  # List of floats
    ["a", "b", "c"],  # List of charstrings
  ]


@asynccontextmanager
@asyncfixture(scope="function")
async def client(items: List[Any], request: FixtureRequest) -> AsyncGenerator[TestClient, None]:
  """
  Sets up a FastAPI TestClient wrapped around test application with Cachette

  ---
  :return: instance of Cachette api service for testing
  :rtype: TestClient
  """
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
      uncached: str = await cachette.fetch(f"{ i }")
      if uncached != item:
        ok = False
        break
    return ("", "OK")[ok]

  with TestClient(app) as test_client:
    yield test_client


@mark.parametrize(
  "client",
  [
    ### InMemory & JSON Codecs ###
    [("backend", "inmemory"), ("codec", "json")],
    [("backend", "inmemory"), ("codec", "orjson")],
    ### Memcached & JSON Codecs ###
    [("backend", "memcached"), ("codec", "json"), ("memcached_host", "localhost")],
    [
      ("backend", "memcached"),
      ("codec", "orjson"),
      ("memcached_host", "localhost"),
    ],
    ### MongoDB & JSON Codecs ###
    [
      ("backend", "mongodb"),
      ("codec", "json"),
      ("database_name", "cachette-db"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    [
      ("backend", "mongodb"),
      ("codec", "orjson"),
      ("database_name", "cachette-db"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    ### Redis & JSON Codecs ###
    [
      ("backend", "redis"),
      ("codec", "json"),
      ("redis_url", "redis://localhost:6379"),
    ],
    [
      ("backend", "redis"),
      ("codec", "orjson"),
      ("redis_url", "redis://localhost:6379"),
    ],
  ],
  ids=[
    "inmemory-json",
    "inmemory-orjson",
    "memcached-json",
    "memcached-orjson",
    "mongodb-json",
    "mongodb-orjson",
    "redis-json",
    "redis-orjson",
  ],
  indirect=True,
)
def test_every_backend_with_every_codec(client: TestClient) -> None:
  response: Response = client.get("/put-items")
  assert response.text == "OK"
  response = client.get("/fetch-items")
  assert response.text == "OK"
