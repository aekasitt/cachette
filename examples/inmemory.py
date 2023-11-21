#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  examples/inmemory.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from fastapi_cachette import Cachette
from pydantic import BaseModel

app = FastAPI()


### Routing ###
class Payload(BaseModel):
    key: str
    value: str


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
