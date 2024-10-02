#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:    ~~/src/cachette/load_config.py
# VERSION:     0.1.8
# CREATED:     2022-04-03 15:31
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing `LoadConfig` Pydantic model"""

### Standard packages ###
from typing import Optional

### Third-party packages ###
from pydantic import BaseModel, validator, StrictInt, StrictStr


class LoadConfig(BaseModel):
  backend: Optional[StrictStr] = None
  codec: Optional[StrictStr] = None
  ttl: Optional[StrictInt] = None

  ### Memcached ###
  memcached_host: Optional[StrictStr] = None

  ### MongoDB ###
  database_name: Optional[StrictStr] = None
  mongodb_url: Optional[StrictStr] = None
  table_name: Optional[StrictStr] = None

  ### Pickle ###
  pickle_path: Optional[StrictStr] = None

  ### Redis ###
  redis_url: Optional[StrictStr] = None

  ### Valkey ###
  valkey_url: Optional[StrictStr] = None

  @validator("backend")
  def validate_backend(cls, value: str) -> str:
    if value.lower() not in {
      "inmemory",
      "memcached",
      "mongodb",
      "pickle",
      "redis",
      "valkey",
    }:
      raise ValueError(
        'The "backend" value must be one of "inmemory", "memcached", "pickle", "redis" or "valkey".'
      )
    return value.lower()

  @validator("ttl")
  def validate_time_to_live(cls, value: int) -> int:
    if value <= 0 or value > 3600:
      raise ValueError('The "ttl" value must between 1 or 3600 seconds.')
    return value

  @validator("codec")
  def validate_codec(cls, value: str) -> str:
    if value.lower() not in {
      "csv",
      "feather",
      "json",
      "msgpack",
      "orjson",
      "parquet",
      "pickle",
    }:
      raise ValueError(
        'The "codec" value must be one of "csv", "feather", "json", "msgpack", "orjson", '
        '"parquet", or "pickle".'
      )
      ### TODO: validation when using DataFrame Codecs (csv, sql, feather, parquet) have pandas? ###
    return value

  @validator("redis_url", always=True)
  def validate_redis_url(cls, value: str, values: dict) -> str:
    if values["backend"].lower() == "redis" and not value:
      raise ValueError('The "redis_url" cannot be null when using redis as backend.')
    ### TODO: More validations ###
    return value

  @validator("memcached_host", always=True)
  def validate_memcached_host(cls, value: str, values: dict) -> str:
    if values["backend"].lower() == "memcached" and not value:
      raise ValueError('The "memcached_host" cannot be null when using memcached as backend.')
    ### TODO: More validations ###
    return value

  @validator("table_name")
  def validate_table_name(cls, value: str, values: dict) -> str:
    backend: str = values["backend"].lower()
    if backend == "mongodb" and not value:
      raise ValueError('The "table_name" cannot be null when using MongoDB as backend.')
    ### TODO: More validations ###
    return value

  @validator("database_name")
  def validate_database_name(cls, value: str, values: dict) -> str:
    backend: str = values["backend"].lower()
    if backend == "mongodb" and not value:
      raise ValueError('The "database_name" cannot be null when using MongoDB as backend.')
    ### TODO: More validations ###
    return value

  @validator("mongodb_url", always=True)
  def validate_mongodb_url(cls, value: str, values: dict) -> str:
    backend: str = values["backend"].lower()
    if backend == "mongodb" and not value:
      raise ValueError('The "mongodb_url" cannot be null when using MongoDB as backend.')
    ### TODO: More validations ###
    return value

  @validator("pickle_path", always=True)
  def validate_pickle_path(cls, value: str, values: dict) -> str:
    backend: str = values["backend"].lower()
    if backend == "pickle" and not value:
      raise ValueError('The "pickle_path" cannot be null when using pickle as backend.')
    ### TODO: More validations ###
    return value

  @validator("valkey_url", always=True)
  def validate_valkey_url(cls, value: str, values: dict) -> str:
    if values["backend"].lower() == "valkey" and not value:
      raise ValueError('The "valkey_url" cannot be null when using valkey as backend.')
    ### TODO: More validations ###
    return value


__all__ = ("LoadConfig",)
