#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/mongodb.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-05 14:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining backend subclass used with MongoDB key-value database
"""

### Standard packages ###
from typing import Any, Optional, Tuple

### Third-party packages ###
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel, StrictInt, StrictStr, validate_arguments

### Local modules ###
from cachette.backends import Backend
from cachette.codecs import Codec


class MongoDBBackend(Backend, BaseModel):
    codec: Codec
    database_name: StrictStr
    table_name: StrictStr
    ttl: StrictInt
    url: StrictStr

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return AsyncIOMotorClient(self.url)[self.database_name]

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return AsyncIOMotorClient(self.url)[self.database_name][self.table_name]

    @classmethod
    @validate_arguments
    async def init(
        cls,
        codec: Codec,
        database_name: StrictStr,
        table_name: StrictStr,
        ttl: StrictInt,
        url: StrictStr,
    ) -> "MongoDBBackend":
        client: AsyncIOMotorClient = AsyncIOMotorClient(url)
        ### Create Collection if None existed ###
        names: list = await client[database_name].list_collection_names(filter={"name": table_name})
        if len(names) == 0:
            await client[database_name].create_collection(table_name)
        return cls(codec, database_name, table_name, ttl, url)

    @validate_arguments
    async def fetch(self, key: StrictStr) -> Any:
        document: dict = await self.collection.find_one({"key": key})
        if document and document.get("expires", 0) > self.now:
            value: bytes = document.get("value", None)
            return self.codec.loads(value)
        return None

    @validate_arguments
    async def fetch_with_ttl(self, key: StrictStr) -> Tuple[int, Any]:
        document: dict = await self.collection.find_one({"key": key})
        if document:
            value: bytes = document.get("value", None)
            ttl: int = document.get("expires", 0) - self.now
            if ttl < 0:
                return 0, None
            return ttl, self.codec.loads(value)
        return -1, None

    @validate_arguments
    async def put(self, key: StrictStr, value: Any, ttl: Optional[StrictInt] = None) -> None:
        ttl = ttl or self.ttl
        data: bytes = self.codec.dumps(value)
        item: dict = {"key": key, "value": data, "expires": self.now + ttl}
        document: dict = await self.collection.find_one({"key": key})
        if document:
            await self.collection.update_one({"key": key}, {"$set": item})
        else:
            await self.collection.insert_one(item)

    @validate_arguments
    async def clear(
        self, namespace: Optional[StrictStr] = None, key: Optional[StrictStr] = None
    ) -> int:
        count: int = 0
        if namespace:
            raise NotImplementedError
        elif key:
            document: dict = await self.collection.find_one({"key": key})
            if document:
                exist: bool = document.get("expires", 0) > self.now
                result = await self.collection.delete_one({"key": key})
                count += (0, 1)[exist and result.deleted_count > 0]
        return count


__all__ = ["MongoDBBackend"]
