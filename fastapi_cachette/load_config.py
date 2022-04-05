#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  load_config.py
# VERSION: 	 0.1.1
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Module containing `LoadConfig` Pydantic model
'''
### Standard Packages ###
from typing import Optional
### Third-Party Packages ###
from pydantic import BaseModel, validator, StrictInt, StrictStr

class LoadConfig(BaseModel):
  backend: Optional[StrictStr] = 'inmemory'
  ttl: Optional[StrictInt]     = 60 # seconds

  ### Redis ###
  redis_url: Optional[StrictStr]

  ### Memcached ###
  memcached_host: Optional[StrictStr]

  ### AWS DynamoDB & MongoDB ###
  table_name: Optional[StrictStr]

  ### AWS DynamoDB ###
  region: Optional[StrictStr]
  dynamodb_url: Optional[StrictStr]

  ### MongoDB ###
  database_name: Optional[StrictStr]
  mongodb_url: Optional[StrictStr]

  @validator('backend')
  def validate_backend(cls, value: str):
    if value.lower() not in { 'dynamodb', 'inmemory', 'memcached', 'redis', 'mongodb' }:
      raise ValueError(
        'The "backend" value must be one of "dynamodb", "inmemory", "memcached", or "redis".'
      )
    return value.lower()

  @validator('ttl')
  def validate_time_to_live(cls, value: str):
    if value <= 0 or value > 3600:
      raise ValueError('The "ttl" value must between 1 or 3600 seconds.')
    return value

  @validator('redis_url', always=True)
  def validate_redis_url(cls, value: str, values: dict):
    if values['backend'].lower() == 'redis' and not value:
      raise ValueError('The "redis_url" cannot be null when using redis as backend.')
    ### TODO More Validations ###
    return value

  @validator('memcached_host', always=True)
  def validate_memcached_host(cls, value: str, values: dict):
    if values['backend'].lower() == 'memcached' and not value:
      raise ValueError('The "memcached_host" cannot be null when using memcached as backend.')
    ### TODO More Validations ###
    return value

  @validator('table_name')
  def validate_table_name(cls, value: str, values: dict):
    backend: str = values['backend'].lower()
    if backend in ('dynamodb', 'mongodb') and not value:
      raise ValueError('The "table_name" cannot be null when using DynamoDB / MongoDB as backend.')
    ### TODO More Validations ###
    return value

  @validator('region')
  def validate_region(cls, value: str, values: dict):
    backend: str      = values['backend'].lower()
    dynamodb_url: str = values.get('dynamodb_url', None)
    if backend == 'dynamodb' and not dynamodb_url and not value:
      raise ValueError(
        'The "region" cannot be null when using DynamoDB as backend and no "dynamodb_url" defined.'
      )
    if value.lower() not in {
      'us-east-1', 'us-west-2', 'us-west-1', 'eu-west-1',   \
        'eu-central-1', 'ap-southeast-1', 'ap-southeast-2', \
          'ap-northeast-1', 'ap-northeast-2', 'sa-east-1',  \
            'cn-north-1', 'ap-south-1'                      \
    }:
      raise ValueError('The "region" provided does not exist under AWS Regions.')
    return value.lower()

  @validator('dynamodb_url', always=True)
  def validate_dynamodb_url(cls, value: str, values: dict):
    backend: str = values['backend'].lower()
    region: str  = values.get('region', None)
    if backend == 'dynamodb' and not region and not value:
      raise ValueError(
        'The "dynamodb_url" cannot be null when using DynamoDB as backend and no region defined.'
      )
    ### TODO More Validations ###
    return value

  @validator('database_name')
  def validate_database_name(cls, value: str, values: dict):
    backend: str = values['backend'].lower()
    if backend == 'mongodb' and not value:
      raise ValueError('The "database_name" cannot be null when using MongoDB as backend.')
    ### TODO More Validations ###
    return value

  @validator('mongodb_url', always=True)
  def validate_mongodb_url(cls, value: str, values: dict):
    backend: str = values['backend'].lower()
    if backend == 'mongodb' and not value:
      raise ValueError('The "mongodb_url" cannot be null when using MongoDB as backend.')
    ### TODO More Validations ###
    return value
