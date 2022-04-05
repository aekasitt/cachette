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
  [('backend', 'inmemory'), ('expire', 60)],                                       \
  [('backend', 'redis'), ('expire', 60), ('redis_url', 'redis://localhost:6379')], \
  [('backend', 'memcached'), ('expire', 60), ('memcached_host', 'localhost')],     \
])
def test_load_valid_configs(configs: List[Tuple[str, Any]]) -> NoReturn:
  @Cachette.load_config
  def load_cachette_configs() -> List[Tuple[str, Any]]:
    return configs

@mark.parametrize('configs, reason', [
  (
    [('backend', 'dynamodb'), ('expire', 0), ('region', 'us-east-1')], \
    'The "expire" value must between 1 or 3600 seconds.'               \
  ),
  (
    [('backend', 'dynamodb'), ('expire', 0), ('dynamodb_url', 'http://localhost:8000')], \
    'The "expire" value must between 1 or 3600 seconds.'                                 \
  ),
  (
    [('backend', 'inmemory'), ('expire', 0)],            \
    'The "expire" value must between 1 or 3600 seconds.' \
  ),
  (
    [('backend', 'redis'), ('expire', 0), ('redis_url', 'redis://localhost:6379')], \
    'The "expire" value must between 1 or 3600 seconds.'                            \
  ),
  (
    [('backend', 'memcached'), ('expire', 0), ('memcached_host', 'localhost')], \
    'The "expire" value must between 1 or 3600 seconds.'                        \
  ),
  (
    [('backend', 'dynamodb'), ('region', 'not-valid')],       \
    'The `region` provided does not exist under AWS Regions.' \
  ),
  (
    [('backend', 'redis')],                                       \
    'The `redis_url` cannot be null when using redis as backend.' \
  ),
  (
    [('backend', 'memcached')],                                            \
    'The `memcached_host` cannot be null when using memcached as backend.' \
  )
])
def test_load_invalid_configs(configs: List[Tuple[str, Any]], reason: str) -> NoReturn:
  with raises(ValidationError) as err:
    @Cachette.load_config
    def load_cachette_configs():
      return configs
  exc_info: str = str(err)
  assert set(reason).issubset(set(exc_info))
