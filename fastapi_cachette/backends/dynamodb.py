#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/dynamodb.py
# VERSION: 	 0.1.1
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
  region: str
  table_name: str
  ttl: int
  url: str

  @classmethod
  async def init(cls,
    table_name: str, ttl: int,                              \
    region: Optional[str] = None, url: Optional[str] = None \
  ) -> 'DynamoDBBackend':
    dynamodb: ClientCreatorContext = get_session() \
      .create_client('dynamodb', region_name=region, endpoint_url=url)
    async with dynamodb as client:
      ### Create Table if None Existed ###
      table_names: list = (await client.list_tables()).get('TableNames', [])
      if table_name not in table_names:
        table_definition: dict = {
          'AttributeDefinitions': [{
            'AttributeName': 'key',
            'AttributeType': 'S'
          }],
          'KeySchema': [{
            'AttributeName': 'key',
            'KeyType': 'HASH'
          }],
          'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
          }
        }
        await client.create_table(TableName=table_name, **table_definition)
    return cls(region=region, table_name=table_name, ttl=ttl, url=url)

  @property
  def dynamodb(self) -> ClientCreatorContext:
    return get_session().create_client('dynamodb', region_name=self.region, endpoint_url=self.url)

  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    async with self.dynamodb as client:
      response = await client.get_item(TableName=self.table_name, Key={'key': {'S': key}})
      if 'Item' in response:
        value: str = response['Item'].get('value', {}).get('S')
        ttl: int   = int(response['Item'].get('expires', {}).get('N', 0)) - self.now
        if ttl < 0:
          return 0, None
        return ttl, value

  async def fetch(self, key: str) -> str:
    async with self.dynamodb as client:
      response = await client.get_item(TableName=self.table_name, Key={'key': {'S': key}})
      if 'Item' in response:
        value: str = response['Item'].get('value', {}).get('S')
        ttl: int   = int(response['Item'].get('expires', {}).get('N', 0)) - self.now
        if ttl < 0: return None
        return value

  async def put(self, key: str, value: str, ttl: Optional[int] = None):
    ttl = ttl or self.ttl
    async with self.dynamodb as client:
      expires_at: dict = {
        'expires': { 'N': f'{ self.now + ttl }' }
      }
      await client.put_item(
        TableName=self.table_name,
        Item={ **{ 'key': { 'S': key }, 'value': { 'S': value }}, **expires_at }
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
        if 'Item' in response: ttl = int(response['Item'].get('expires', {}).get('N', 0)) - self.now
        ### Sends Delete Item Request ###
        resp = await client.delete_item(TableName=self.table_name, Key={'key': {'S': key}})
        count += (0, 1)[ttl > 0 and resp['ResponseMetadata']['HTTPStatusCode'] == 200]
    return count
