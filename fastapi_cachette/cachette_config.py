#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  config.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Module containing `CachetteConfig` class
'''
### Standard Packages ###
from typing import Callable, List, Tuple
### Third-Party Packages ###
from pydantic import ValidationError
### Local Modules ###
from fastapi_cachette.load_config import LoadConfig

class CachetteConfig(object):
  ### Basics ###
  _backend: str        = 'inmemory'
  _expire: int         = 60

  ### Redis ###
  _redis_url: str      = None

  ### Memcached ###
  _memcached_host: str = None

  ### AWS DynamoDB & MongoDB ###
  _table_name: str     = 'fastapi-cachette'

  ### AWS DynamoDB ###
  _region: str
  _dynamodb_url: str

  ### MongoDB ###
  _database_name: str
  _mongodb_url: str

  @classmethod
  def load_config(cls, settings: Callable[..., List[Tuple]]) -> 'CachetteConfig':
    try:
      config = LoadConfig(**{key.lower(): value for key, value in settings()})
      cls._backend        = config.backend or cls._backend
      cls._expire         = config.expire or cls._expire
      cls._redis_url      = config.redis_url
      cls._memcached_host = config.memcached_host
      cls._table_name     = config.table_name or cls._table_name
      cls._region         = config.region
      cls._dynamodb_url   = config.dynamodb_url
      cls._database_name  = config.database_name
      cls._mongodb_url    = config.mongodb_url
    except ValidationError: raise
    except Exception:
      raise TypeError('CachetteConfig must be pydantic "BaseSettings" or list of tuples')
