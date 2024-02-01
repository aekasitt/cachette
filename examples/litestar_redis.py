#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  examples/litestar_redis.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from cachette import Cachette
from litestar import Litestar, get, post
from litestar.di import Provide
from pydantic import BaseModel


### Cachette Configurations ###
@Cachette.load_config
def get_cachette_config():
  return [("backend", "redis"), ("redis_url", "redis://localhost:6379")]


### Schema ###


class Payload(BaseModel):
  key: str
  value: str


### Routing ###


@get(
  "/{key:str}",
)
async def getter(key: str, cachette: Cachette) -> str:
  """
  Returns key value
  """
  value: str = await cachette.fetch(key)
  return value


@post("/", tags=["Payload"])
async def setter(data: Payload, cachette: Cachette) -> str:
  """
  Submit a new cache key-pair value
  """
  await cachette.put(data.key, data.value)
  return "OK"


app: Litestar = Litestar(
  route_handlers=[getter, setter],
  dependencies={"cachette": Provide(Cachette, sync_to_thread=True)},
)


__all__ = ["app"]
