#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  core.py
# VERSION: 	 0.1.2
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Module containing Core implementation for Cashette extension for FastAPI
'''
### Standard Packages ###
from asyncio import run
### Third-Party Packages ###
from fastapi.requests import Request
from fastapi.responses import Response
### Local Modules ###
from fastapi_cachette.backends import Backend
from fastapi_cachette.cachette_config import CachetteConfig
from fastapi_cachette.codecs import Codec

class Cachette(CachetteConfig):
  backend: Backend

  def __init__(self, request: Request, response: Response):
    '''
    Invoked by FastAPI Depends
    '''
    # TODO Check request headers if `Cache-Control`` is `no-store`

    ### Determine Encoding and Decoding Codec ###
    codec: Codec
    if self._codec == 'json':
      from fastapi_cachette.codecs.json import JSONCodec
      codec = JSONCodec()
    elif self._codec == 'msgpack':
      from fastapi_cachette.codecs.msgpack import MsgpackCodec
      codec = MsgpackCodec()
    if self._codec == 'orjson':
      from fastapi_cachette.codecs.orjson import ORJSONCodec
      codec = ORJSONCodec()
    elif self._codec == 'pickle':
      from fastapi_cachette.codecs.pickle import PickleCodec
      codec = PickleCodec()
    elif self._codec == 'vanilla':
      from fastapi_cachette.codecs.vanilla import VanillaCodec
      codec = VanillaCodec()

    if self._backend == 'dynamodb':
      from fastapi_cachette.backends.dynamodb import DynamoDBBackend
      self.backend = run(DynamoDBBackend.init(
        codec, self._table_name, self._ttl, self._region, self._dynamodb_url
      ))
    elif self._backend == 'inmemory':
      from fastapi_cachette.backends.inmemory import InMemoryBackend
      self.backend = InMemoryBackend(codec=codec, ttl=self._ttl)
    elif self._backend == 'memcached':
      from fastapi_cachette.backends.memcached import MemcachedBackend
      self.backend = run(MemcachedBackend.init(codec, self._memcached_host, self._ttl))
    elif self._backend == 'mongodb':
      from fastapi_cachette.backends.mongodb import MongoDBBackend
      self.backend = run(MongoDBBackend.init(
        codec, self._database_name, self._table_name, self._ttl, self._mongodb_url
      ))
    elif self._backend == 'redis':
      from fastapi_cachette.backends.redis import RedisBackend
      self.backend = run(RedisBackend.init(codec, self._redis_url, self._ttl))

  # When a method is not found, shortcuts it to instance's `backend` member method
  def __getattr__(self, name):
    return getattr(self.backend, name)
