#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  examples/pickle_xpresso.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from cachette import Cachette
from pydantic import BaseModel
from xpresso import App, Depends, FromJson, FromPath, Path
from xpresso.typing import Annotated


@Cachette.load_config
def get_cachette_config():
    return [("backend", "pickle"), ("pickle_path", "examples/cachette.pkl")]


### Schema ###
class Payload(BaseModel):
    key: str
    value: str


### Routing ###


async def setter(payload: FromJson[Payload], cachette: Annotated[Cachette, Depends(Cachette)]):
    """
    Submit a new cache key-pair value
    """
    await cachette.put(payload.key, payload.value)
    return "OK"


async def getter(key: FromPath[str], cachette: Annotated[Cachette, Depends(Cachette)]):
    """
    Returns key value
    """
    value: str = await cachette.fetch(key)
    return value


app = App(routes=[Path("/{key}", get=getter), Path("/", post=setter)])


__all__ = ["app"]
