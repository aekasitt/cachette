#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/mongodb.py
# VERSION: 	 0.1.2
# CREATED: 	 2022-04-05 14:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Any, Optional, Tuple
### Third-Party Packages ###
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
### Local Modules ###
from fastapi_cachette.backends import Backend
from fastapi_cachette.codecs import Codec

@dataclass
class MongoDBBackend(Backend):
  codec: Codec
  database_name: str
  table_name: str
  ttl: int
  url: str

  @property
  def db(self) -> AsyncIOMotorDatabase:
    return AsyncIOMotorClient(self.url)[self.database_name]

  @property
  def collection(self) -> AsyncIOMotorCollection:
    return AsyncIOMotorClient(self.url)[self.database_name][self.table_name]

  @classmethod
  async def init(
      cls, codec: Codec, database_name: str, table_name: str, ttl: int, url: str
    ) -> 'MongoDBBackend':
    client: AsyncIOMotorClient = AsyncIOMotorClient(url)
    ### Create Collection if None existed ###
    names: list = await client[database_name].list_collection_names(filter={ 'name': table_name })
    if len(names) == 0:
      await client[database_name].create_collection(table_name)
    return cls(codec, database_name, table_name, ttl, url)

  async def fetch(self, key: str) -> Any:
    document: dict = await self.collection.find_one({ 'key': key })
    if document and document.get('expires', 0) > self.now:
      value: str = document.get('value', None)
      return self.codec.loads(value)
    return None

  async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
    document: dict = await self.collection.find_one({ 'key': key })
    if document:
      value: str = document.get('value', None)
      ttl: int   = document.get('expires', 0) - self.now
      if ttl < 0: return 0, None
      return ttl, self.codec.loads(value)
    return -1, None

  async def put(self, key: str, value: Any, ttl: Optional[int] = None):
    ttl = ttl or self.ttl
    data: str = self.codec.dumps(value)
    item: dict = { 'key': key, 'value': data, 'expires': self.now + ttl }
    document: dict = await self.collection.find_one({ 'key': key })
    if document:
      await self.collection.update_one({'key': key}, {'$set': item })
    else:
      await self.collection.insert_one(item)

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    count: int = 0
    if namespace:
      raise NotImplementedError
    elif key:
      document: dict = await self.collection.find_one({ 'key': key })
      if document:
        exist: bool = document.get('expires', 0) > self.now
        result = await self.collection.delete_one({'key': key})
        count += (0, 1)[exist and result.deleted_count > 0]
    return count
