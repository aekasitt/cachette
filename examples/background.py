#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  examples/background.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-12 11:25
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Example for using FastAPI Cachette extension in tandem with BackgroundTasks
"""
from asyncio import run
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import PlainTextResponse
from fastapi_cachette import Cachette
from pydantic import BaseModel

app = FastAPI()


### Cachette Configurations ###
@Cachette.load_config
def get_cachette_config():
    return [("backend", "memcached"), ("memcached_host", "localhost")]


### Routing ###
class Payload(BaseModel):
    key: str
    value: str


@app.post("/", response_class=PlainTextResponse)
def setter(
    payload: Payload, background_tasks: BackgroundTasks, cachette: Cachette = Depends()
):
    """
    Submit a new cache key-pair value
    """
    background_tasks.add_task(cachette.put, payload.key, payload.value)
    return "OK"


@app.get("/{key}", response_class=PlainTextResponse, status_code=200)
def getter(key: str, cachette: Cachette = Depends()):
    """
    Returns key value
    """
    value: str = run(cachette.fetch(key))
    return value
