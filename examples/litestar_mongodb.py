#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  examples/litestar_mongodb.py
# VERSION: 	 0.1.8
# CREATED: 	 2024-02-02 23:51
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
  return [("backend", "mongodb"), ("mongodb_url", "mongodb://localhost:27017")]


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
