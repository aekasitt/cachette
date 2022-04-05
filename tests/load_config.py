#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  tests/load_config.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-03 20:34
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Test Suite containing Configuration Loading tests
'''
### Standard Packages ###
from typing import Any, List, NoReturn, Tuple
### Third-Party Packages ###
from pydantic import ValidationError
from pytest import mark, raises
### Local Modules ###
from fastapi_cachette import Cachette

@mark.parametrize('configs', [
  ### DynamoDB ###
  [('backend', 'dynamodb'), ('region', 'ap-southeast-1')],                                \
  [('backend', 'dynamodb'), ('dynamodb_url', 'http://localhost:8000')],                   \
  [('backend', 'dynamodb'), ('region', 'ap-southeast-1'), ('expire', 1)],                 \
  [('backend', 'dynamodb'), ('region', 'ap-southeast-1'), ('expire', 3600)],              \
  [('backend', 'dynamodb'), ('dynamodb_url', 'http://localhost:8000'), ('expire', 1)],    \
  [('backend', 'dynamodb'), ('dynamodb_url', 'http://localhost:8000'), ('expire', 3600)], \

  ### InMemory ###
  [('backend', 'inmemory')],                       \
  [('backend', 'inmemory'), ('expire', 1)],        \
  [('backend', 'inmemory'), ('expire', 3600)],     \
  [('backend', 'inmemory'), ('table_name', None)], \

  ### Memcached ###
  [('backend', 'memcached'), ('memcached_host', 'localhost')],                       \
  [('backend', 'memcached'), ('expire', 1), ('memcached_host', 'localhost')],        \
  [('backend', 'memcached'), ('memcached_host', 'localhost'), ('table_name', None)], \

  ### MongoDB ###
  [
    ('backend', 'mongodb'), ('database_name', 'fastapi-cachette-database'), \
    ('mongodb_url', 'mongodb://localhost:27017')                            \
  ],                     \
  [
    ('backend', 'mongodb'), ('database_name', 'fastapi-cachette-database'), \
    ('expire', 1), ('mongodb_url', 'mongodb://localhost:27017')             \
  ],
  [
    ('backend', 'mongodb'), ('database_name', 'fastapi-cachette-database'), \
    ('expire', 3600), ('mongodb_url', 'mongodb://localhost:27017')          \
  ],

  ### Redis ###
  [('backend', 'redis'), ('redis_url', 'redis://localhost:6379')],                       \
  [('backend', 'redis'), ('expire', 1), ('redis_url', 'redis://localhost:6379')],        \
  [('backend', 'redis'), ('expire', 3600), ('redis_url', 'redis://localhost:6379')],     \
  [('backend', 'redis'), ('redis_url', 'redis://localhost:6379'), ('table_name', None)], \
])
def test_load_valid_configs(configs: List[Tuple[str, Any]]) -> NoReturn:
  @Cachette.load_config
  def load_cachette_configs() -> List[Tuple[str, Any]]:
    return configs

@mark.parametrize('invalid_configs, reason', [
  ### AWS DynamoDB ###
  (
    [('backend', 'dynamodb')],                                                                \
    'The "dynamodb_url" cannot be null when using DynamoDB as backend and no region defined.' \
  ),
  (
    [('backend', 'dynamodb'), ('region', 'ap-southeast-1'), ('expire', 0)], \
    'The "expire" value must between 1 or 3600 seconds.'                    \
  ),
  (
    [('backend', 'dynamodb'), ('expire', 3601)],          \
    'The "expire" value must between 1 or 3600 seconds.'  \
  ),
  # (
  #   [('backend', 'dynamodb'), ('region', 'not-valid')],       \
  #   'The "region" provided does not exist under AWS Regions.' \
  # ),
  (
    [('backend', 'dynamodb'), ('region', 'ap-southeast-1'), ('table_name', None)], \
    'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.'    \
  ),
  (
    [('backend', 'dynamodb'), ('dynamodb_url', 'http://localhost:8000'), ('table_name', None)], \
    'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.'                 \
  ),

  ### InMemory ###
  (
    [('backend', 'inmemory'), ('expire', 0)],            \
    'The "expire" value must between 1 or 3600 seconds.' \
  ),
  (
    [('backend', 'inmemory'), ('expire', 3601)],         \
    'The "expire" value must between 1 or 3600 seconds.' \
  ),

  ### Memcached ###
  (
    [('backend', 'memcached')],                                            \
    'The "memcached_host" cannot be null when using memcached as backend.' \
  ),
  (
    [('backend', 'memcached'), ('expire', 0), ('memcached_host', 'localhost')], \
    'The "expire" value must between 1 or 3600 seconds.'                        \
  ),
  (
    [('backend', 'memcached'), ('expire', 3601), ('memcached_host', 'localhost')], \
    'The "expire" value must between 1 or 3600 seconds.'                           \
  ),

  ### MongoDB ###
  (
    [('backend', 'mongodb')],                                           \
    'The "database_name" cannot be null when using MongoDB as backend.' \
    
  ),
  (
    [('backend', 'mongodb'), ('database_name', 'cachette-collection')], \
    'The "mongodb_url" cannot be null when using MongoDB as backend.'   \
  ),
  (
    [('backend', 'mongodb'), ('database_name', 'cachette-collection'),           \
      ('mongodb_url', 'http://localhost:27017'), ('table_name', None)],          \
    'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.'  \
  ),

  ### Redis ###
  (
    [('backend', 'redis')],                                       \
    'The "redis_url" cannot be null when using redis as backend.' \
  ),
  (
    [('backend', 'redis'), ('expire', 0), ('redis_url', 'redis://localhost:6379')], \
    'The "expire" value must between 1 or 3600 seconds.'                            \
  ),
  (
    [('backend', 'redis'), ('expire', 3601), ('redis_url', 'redis://localhost:6379')], \
    'The "expire" value must between 1 or 3600 seconds.'                               \
  ),
])
def test_load_invalid_configs(invalid_configs: List[Tuple[str, Any]], reason: str) -> NoReturn:
  with raises(ValidationError) as err:
    @Cachette.load_config
    def load_cachette_configs():
      return invalid_configs
  exc_info: str = str(err)
  assert set(reason).issubset(set(exc_info))
