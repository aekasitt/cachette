#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/dynamodb.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Optional, Tuple
### Third-Party Packages ###
from aiobotocore.session import get_session, ClientCreatorContext
### Local Modules ###
from fastapi_cachette.backends import Backend

@dataclass
class DynamoDBBackend(Backend):
  table_name: str
  expire: int
  dynamodb: ClientCreatorContext
   
  @classmethod
  def init(cls,
    table_name: str, expire: Optional[int] = 60,            \
    region: Optional[str] = None, url: Optional[str] = None \
  ) -> 'DynamoDBBackend':
    return DynamoDBBackend(
      table_name=table_name, expire=expire,                                                    \
        dynamodb=get_session().create_client('dynamodb', region_name=region, endpoint_url=url) \
      )

  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    async with self.dynamodb as client:
      response = await client.get_item(TableName=self.table_name, Key={'key': {'S': key}})
      if 'Item' in response:
        value: str      = response['Item'].get('value', {}).get('S')
        created_at: int = int(response['Item'].get('created', {}).get('N', 0))
        if not created_at:
          return -1, value
        if created_at < self.now:
          return self.now - created_at, value
      return 0, None

  async def fetch(self, key: str) -> str:
    async with self.dynamodb as client:
      response = await client.get_item(TableName=self.table_name, Key={'key': {'S': key}})
      if 'Item' in response:
        value: str = response['Item'].get('value', {}).get('S')
        ttl: int   = int(response['Item'].get('ttl', {}).get('N', 0))
        if ttl < self.now: return None
        return value

  async def put(self, key: str, value: str, expire: Optional[int] = None):
    async with self.dynamodb as client:
      expire: int      = expire or self.expire
      created_at: dict = {
        'created': { 'N': f'{ self.now + expire }' }
      }
      await client.put_item(
        TableName=self.table_name,
        Item={ **{ 'key': { 'S': key }, 'value': { 'S': value }}, **created_at }
      )

  async def clear(self, namespace: str = None, key: str = None) -> int:
    count: int = 0
    if namespace:
      raise NotImplementedError
    elif key:
      async with self.dynamodb as client:
        ### Checks if previously existed ###
        response: dict = await client.get_item(TableName=self.table_name, Key={'key': {'S': key}})
        ### Calculate Time-to-live ###
        ttl: int = -1
        if 'Item' in response: ttl = int(response['Item'].get('created', {}).get('N', 0))-self.now
        ### Sends Delete Item Request ###
        resp = await client.delete_item(TableName=self.table_name, Key={'key': {'S': key}})
        count += (0, 1)[ttl > 0 and resp['ResponseMetadata']['HTTPStatusCode'] == 200]
    return count
