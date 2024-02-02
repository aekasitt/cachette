#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  examples/blacksheep_pickle.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from blacksheep import Application, FromJSON, get, post
from cachette import Cachette
from os import remove
from os.path import isfile
from pydantic import BaseModel
from typing import Optional


@Cachette.load_config
def get_cachette_config():
  return [("backend", "pickle"), ("pickle_path", "examples/cachette.pkl")]


### Schema ###
class Payload(BaseModel):
  key: str
  value: str


app: Application = Application()
app.services.add_scoped(Cachette)


### Routing ###


@post("/")
async def setter(body: FromJSON[Payload], cachette: Cachette) -> str:
  """
  Submit a new cache key-pair value
  """
  payload: Payload = body.value
  await cachette.put(payload.key, payload.value)
  return "OK"


@get("/{key}")
async def getter(cachette: Cachette, key: str) -> Optional[str]:
  """
  Returns key value
  """
  value: str = await cachette.fetch(key)
  return value


@app.lifespan
async def remove_pickle_after_shutdown() -> None:
  """
  Remove cachette pickle when App shuts down
  """
  yield
  if isfile("examples/cachette.pkl"):
    remove("examples/cachette.pkl")


if __name__ == "__main__":
  from uvicorn import run

  run(app, lifespan="on")


__all__ = ["app"]
