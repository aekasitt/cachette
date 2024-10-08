#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:    ~~/tests/backends/__init__.py
# VERSION:     0.1.8
# CREATED:     2022-04-15 19:06
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining test methods to be used by different backend-specific tests"""

### Standard packages ###
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Tuple

### Third-party packages ###
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pytest_asyncio import fixture

### Local modules ###
from cachette import Cachette


class Payload(BaseModel):
  key: str
  value: str


@asynccontextmanager
@fixture(scope="function")
async def client(request) -> AsyncGenerator[TestClient, None]:
  assert isinstance(request.param, list)
  assert len(request.param) > 0
  configs: List[Tuple[str, Any]] = request.param

  app = FastAPI()

  @Cachette.load_config
  def get_cachette_config():
    return configs

  ### Routing ###
  @app.post("/", response_class=PlainTextResponse)
  async def setter(payload: Payload, cachette: Cachette = Depends()):
    """
    Submit a new cache key-pair value
    """
    await cachette.put(payload.key, payload.value)
    return "OK"

  @app.get("/{key}", response_class=PlainTextResponse, status_code=200)
  async def getter(key: str, cachette: Cachette = Depends()):
    """
    Returns key value
    """
    value: str = await cachette.fetch(key)
    return value

  @app.delete("/{key}", response_class=PlainTextResponse, status_code=200)
  async def destroy(key: str, cachette: Cachette = Depends()):
    """
    Clears cached value
    """
    cleared: int = await cachette.clear(key=key)
    return ("", "OK")[cleared > 0]

  with TestClient(app) as test_client:
    yield test_client
