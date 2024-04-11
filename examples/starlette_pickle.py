#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:    ~~/examples/starlette_pickle.py
# VERSION:     0.1.8
# CREATED:     2024-02-02 22:27
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from cachette import Cachette
from os import remove
from os.path import isfile
from pydantic import BaseModel, ValidationError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from typing import List


@Cachette.load_config
def get_cachette_config():
  return [("backend", "pickle"), ("pickle_path", "examples/cachette.pkl")]


### Schema ###
class Payload(BaseModel):
  key: str
  value: str


### Routing ###
async def setter(request: Request):
  """
  Submit a new cache key-pair value
  """
  data = await request.json()
  try:
    payload: Payload = Payload(**data)
    cachette: Cachette = Cachette()
    await cachette.put(payload.key, payload.value)
  except ValidationError as err:
    return JSONResponse({"error": err.json()})
  return PlainTextResponse("OK")


async def getter(request: Request):
  """
  Returns key value
  """
  key: str = request.path_params["key"]
  if not key:
    return JSONResponse({"error": "Missing key"})
  cachette: Cachette = Cachette()
  value: str = await cachette.fetch(key)
  return PlainTextResponse(value)


def shutdown() -> None:
  """
  Remove cachette pickle when App shuts down
  """
  if isfile("examples/cachette.pkl"):
    remove("examples/cachette.pkl")


routes: List[Route] = []
routes.append(Route("/{key:str}", getter, methods=["GET"]))
routes.append(Route("/", setter, methods=["POST"]))
app: Starlette = Starlette(on_shutdown=[shutdown], routes=routes)


__all__ = ("app",)
