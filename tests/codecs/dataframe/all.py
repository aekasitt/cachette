#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  tests/codecs/dataframe/all.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-06 22:03
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Tests for codec implementations on TestClient which can serializ/de-serialize DataFrame objects"""

### Standard packages ###
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Tuple

### Third-party packages ###
from fastapi import Depends, FastAPI
from fastapi.responses import PlainTextResponse, Response
from fastapi.testclient import TestClient
from pytest import FixtureRequest, mark
from pytest_asyncio import fixture

try:
  from pandas import DataFrame, get_dummies, Series
  from pandas.testing import assert_frame_equal
except ImportError:
  ### Assume skipped by conftest "skip_all_if_pandas_not_installed" fixture ###
  pass
### Local modules ###
from cachette import Cachette


@asynccontextmanager
@fixture(scope="function")
async def client(request: FixtureRequest) -> AsyncGenerator[TestClient, None]:
  app: FastAPI = FastAPI()
  configs: List[Tuple[str, Any]] = request.param
  items: List[DataFrame] = [get_dummies(Series(["income", "age", "gender", "education"]))]

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
      uncached: DataFrame = await cachette.fetch(f"{ i }")
      try:
        assert_frame_equal(uncached, item, check_dtype=False)  # dtypes sometimes get changed
      except AssertionError:
        ok = False
        break
    return ("", "OK")[ok]

  with TestClient(app) as test_client:
    yield test_client


@mark.parametrize(
  "client",
  [
    ### InMemory & Codecs ###
    [("backend", "inmemory"), ("codec", "csv")],
    [("backend", "inmemory"), ("codec", "feather")],
    [("backend", "inmemory"), ("codec", "parquet")],
    [("backend", "inmemory"), ("codec", "pickle")],
    ### Memcached & Codecs ###
    [("backend", "memcached"), ("codec", "csv"), ("memcached_host", "localhost")],
    [
      ("backend", "memcached"),
      ("codec", "feather"),
      ("memcached_host", "localhost"),
    ],
    [
      ("backend", "memcached"),
      ("codec", "parquet"),
      ("memcached_host", "localhost"),
    ],
    [
      ("backend", "memcached"),
      ("codec", "pickle"),
      ("memcached_host", "localhost"),
    ],
    ### MongoDB & Codecs ###
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("codec", "csv"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("codec", "feather"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("codec", "parquet"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("codec", "pickle"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    ### Redis & Codecs ###
    [
      ("backend", "redis"),
      ("codec", "csv"),
      ("redis_url", "redis://localhost:6379"),
    ],
    [
      ("backend", "redis"),
      ("codec", "feather"),
      ("redis_url", "redis://localhost:6379"),
    ],
    [
      ("backend", "redis"),
      ("codec", "parquet"),
      ("redis_url", "redis://localhost:6379"),
    ],
    [
      ("backend", "redis"),
      ("codec", "pickle"),
      ("redis_url", "redis://localhost:6379"),
    ],
  ],
  ids=[
    "inmemory-csv",
    "inmemory-feather",
    "inmemory-parquet",
    "inmemory-pickle",
    "memcached-csv",
    "memcached-feather",
    "memcached-parquet",
    "memcached-pickle",
    "mongodb-csv",
    "mongodb-feather",
    "mongodb-parquet",
    "mongodb-pickle",
    "redis-csv",
    "redis-feather",
    "redis-parquet",
    "redis-pickle",
  ],
  indirect=True,
)
def test_every_backend_with_every_dataframe_codec(client) -> None:
  response: Response = client.get("/put-items")
  assert response.text == "OK"
  response = client.get("/fetch-items")
  assert response.text == "OK"
