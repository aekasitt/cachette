#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  core.py
# VERSION: 	 0.1.0
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

class Cachette(CachetteConfig):
  backend: Backend

  def __init__(self, request: Request, response: Response):
    '''
    Invoked by FastAPI Depends
    '''
    # TODO Check request headers if `Cache-Control`` is `no-store`
    if self._backend == 'dynamodb':
      from fastapi_cachette.backends.dynamodb import DynamoDBBackend
      self.backend = DynamoDBBackend.init(self._table_name, self._expire, self._region, self._dynamodb_url)
    elif self._backend == 'inmemory':
      from fastapi_cachette.backends.inmemory import InMemoryBackend
      self.backend = InMemoryBackend(self._expire)
    elif self._backend == 'redis':
      from fastapi_cachette.backends.redis import RedisBackend
      self.backend = run(RedisBackend.init(self._redis_url, self._expire))
    elif self._backend == 'memcached':
      from fastapi_cachette.backends.memcached import MemcachedBackend
      self.backend = run(MemcachedBackend.init(self._memcached_host, self._expire))

  # When a method is not found, shortcuts it to instance's `backend` member method
  def __getattr__(self, name):
    return getattr(self.backend, name)
