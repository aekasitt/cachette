#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  examples/blacksheep_memcached.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from cachette import Cachette
from pydantic import BaseModel
from blacksheep import Application, FromJSON, get, post


@Cachette.load_config
def get_cachette_config():
  return [("backend", "memcached"), ("memcached_host", "localhost")]


### Schema ###
class Payload(BaseModel):
  key: str
  value: str


### Routing ###

app: Application = Application()

# async def syncs_cachette_instance_to_thread(app: Application):

app.services.add_scoped(Cachette)


@post("/")
async def setter(data: FromJSON[Payload], cachette: Cachette):
  """
  Submit a new cache key-pair value
  """
  payload: Payload = data.value
  await cachette.put(payload.key, payload.value)
  return "OK"


@get("/{key}")
async def getter(key: str, cachette: Cachette):
  """
  Returns key value
  """
  value: str = await cachette.fetch(key)
  return value


__all__ = ["app"]
