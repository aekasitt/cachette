#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/mongodb.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-05 14:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Optional, Tuple
### Third-Party Packages ###
from motor.motor_asyncio import AsyncIOMotorClient
### Local Modules ###
from fastapi_cachette.backends import Backend

@dataclass
class MongoDBBackend(Backend):
  collection_name: str
  expire: int
  mongodb: AsyncIOMotorClient
  table_name: str

  @classmethod
  async def init(
      cls, collection_name: str, expire: int, table_name: str, url: str
    ) -> 'MongoDBBackend':
    mongodb: AsyncIOMotorClient = AsyncIOMotorClient(url)
    ### Create Collection if None existed ###
    names: list = await mongodb[table_name].list_collection_names(filter={'name': collection_name })
    if len(names) == 0:
      await mongodb[table_name].create_collection(collection_name)
    return cls(collection_name, expire, mongodb, table_name)

  async def fetch(self, key: str) -> str:
    pass

  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    pass

  async def put(self, key: str, value: str, expire: Optional[int] = None):
    pass

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    pass
