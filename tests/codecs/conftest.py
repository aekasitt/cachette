#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  tests/codecs/conftest.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-15 23:02
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `pytest` config overrides regarding codec tests"""

### Standard packages ###
from typing import Any, List, Optional, Tuple

### Third-party packages ###
from pytest import fixture, FixtureRequest, skip


def get_config_value_from_client_configs(key: str, request: FixtureRequest) -> Optional[str]:
  configs: List[Tuple[str, Any]] = request.node.callspec.params.get("client", [])
  if len(configs) == 0:
    return
  try:
    backend_tuple: Tuple[str, str] = list(filter(lambda item: item[0] == key, configs))[0]
  except IndexError:
    return  # no backend set
  if len(backend_tuple) != 2:
    return
  return backend_tuple[1]


@fixture(autouse=True)
def skip_if_backend_dependency_is_not_installed(request: FixtureRequest):
  """
  Skip test with "dynamodb" backend in the case that "aiobotocore" is not installed;
  Skip test with "memcached" backend in the case that "aiomcache" is not installed;
  Skip test with "mongodb" backend in the case that "motor" is not installed;
  Skip test with "redis" backend in the case that "redis" is not installed.
  Skip test with "valkey" backend in the case that "redis" is not installed.

  ---
  :param:  request  `FixtureRequest`
  """
  backend: str = get_config_value_from_client_configs("backend", request)
  if backend == "dynamodb":
    try:
      import aiobotocore as _
    except ImportError:
      skip(reason='"aiobotocore" dependency is required for "dynamodb" backend test.')
  elif backend == "memcached":
    try:
      import aiomcache as _
    except ImportError:
      skip(reason='"aiomcache" dependency is required for "memcached" backend test.')
  elif backend == "mongodb":
    try:
      import motor as _
    except ImportError:
      skip(reason='"motor" dependency is required for "mongodb" backend test.')
  elif backend == "redis":
    try:
      import redis as _
    except ImportError:
      skip(reason='"redis" dependency is required for "redis" backend test.')
  elif backend == "valkey":
    try:
      import redis as _
    except ImportError:
      skip(reason='"redis" dependency is required for "valkey" backend test.')


@fixture(autouse=True)
def skip_if_codec_dependency_is_not_installed(request: FixtureRequest):
  """
  Skip test with "msgpack" codec in the case that "msgpack" is not installed;
  Skip test with "orjson" codec in the case that "orjson" is not installed;

  ---
  :param:  request  `FixtureRequest`
  """
  codec: str = get_config_value_from_client_configs("codec", request)
  if codec == "msgpack":
    try:
      import msgpack as _
    except ImportError:
      skip(reason='"msgpack" dependency is not installed in this test environment.')
  elif codec == "orjson":
    try:
      import orjson as _
    except ImportError:
      skip(reason='"orjson" dependency is not installed in this test environment.')


@fixture(autouse=True)
def skip_if_dynamodb_server_cannot_be_reached(request: FixtureRequest):
  """
  Skip test with "dynamodb" backend in all cases as of now.

  ---
  :param:  request  `FixtureRequest`
  """
  backend: str = get_config_value_from_client_configs("backend", request)
  if backend == "dynamodb":
    skip(reason="DynamoDB tests are disabled in version 0.1.8")


@fixture(autouse=True)
def skip_if_memcached_server_cannot_be_reached(request: FixtureRequest):
  """
  Skip test with "memcached" backend in the case that Memcached server defined by "memcached_host"
  cannot be reached.

  ---
  :param:  request  `FixtureRequest`
  """
  memcached_host: str = get_config_value_from_client_configs("memcached_host", request)
  if memcached_host is not None:
    from asyncio import BaseEventLoop, set_event_loop, get_event_loop
    from aiomcache import Client

    client: Client = Client(memcached_host)
    loop: BaseEventLoop = get_event_loop()
    try:
      loop.run_until_complete(client.get(b"test"))
    except OSError:
      skip(reason="Memcached Server cannot be reached.")
    finally:
      loop.run_until_complete(client.close())
      set_event_loop(loop)


@fixture(autouse=True)
def skip_if_mongodb_server_cannot_be_reached(request: FixtureRequest):
  """
  Skip test with "mongodb" backend in the case that MongoDB server defined by "mongodb_url"
  cannot be reached.

  ---
  :param:  request  `FixtureRequest`
  """
  mongodb_url: str = get_config_value_from_client_configs("mongodb_url", request)
  if mongodb_url is not None:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError

    try:
      client: MongoClient = MongoClient(mongodb_url, serverSelectionTimeoutMS=1)
      client["test"].list_collection_names(filter={"name": "test"})
    except ServerSelectionTimeoutError:
      skip(reason="MongoDB Server cannot be reached.")


@fixture(autouse=True)
def skip_if_redis_server_cannot_be_reached(request: FixtureRequest):
  """
  Skip test with "redis" backend in the case that Redis server defined by "redis_url"
  cannot be reached.

  ---
  :param:  request  `FixtureRequest`
  """
  redis_url: str = get_config_value_from_client_configs("redis_url", request)
  if redis_url is not None:
    from redis import Redis
    from redis.exceptions import ConnectionError

    try:
      Redis.from_url(redis_url).get("test")
    except ConnectionError:
      skip(reason="Redis Server cannot be reached.")


@fixture(autouse=True)
def skip_if_valkey_server_cannot_be_reached(request: FixtureRequest):
  """
  Skip test with "valkey" backend in the case that Valkey server defined by "valkey_url"
  cannot be reached.

  ---
  :param:  request  `FixtureRequest`
  """
  valkey_url: str = get_config_value_from_client_configs("valkey_url", request)
  if valkey_url is not None:
    from redis import Redis
    from redis.exceptions import ConnectionError

    valkey_url = valkey_url.replace("valkey://", "redis://")
    try:
      Redis.from_url(valkey_url).get("test")
    except ConnectionError:
      skip(reason="Valkey Server cannot be reached.")
