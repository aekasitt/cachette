#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  core.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing Core implementation for Cachette extension for FastAPI
"""

### Standard packages ###
from asyncio import run
from typing import Any, Optional, Tuple

### Local modules ###
from cachette.backends import Backend
from cachette.cachette_config import CachetteConfig
from cachette.codecs import Codec


class Cachette(CachetteConfig):
    backend: Backend

    def __init__(self):
        """
        Invoked by FastAPI Depends
        """
        # TODO Check request headers if `Cache-Control`` is `no-store`

        ### Determine Encoding and Decoding Codec ###
        codec: Codec
        if self._codec == "csv":
            from cachette.codecs.dataframe.csv import CSVCodec

            codec = CSVCodec()
        elif self._codec == "json":
            from cachette.codecs.json import JSONCodec

            codec = JSONCodec()
        elif self._codec == "feather":
            from cachette.codecs.dataframe.feather import FeatherCodec

            codec = FeatherCodec()
        elif self._codec == "msgpack":
            from cachette.codecs.msgpack import MsgpackCodec

            codec = MsgpackCodec()
        if self._codec == "orjson":
            from cachette.codecs.orjson import ORJSONCodec

            codec = ORJSONCodec()
        elif self._codec == "parquet":
            from cachette.codecs.dataframe.parquet import ParquetCodec

            codec = ParquetCodec()
        elif self._codec == "pickle":
            from cachette.codecs.pickle import PickleCodec

            codec = PickleCodec()
        elif self._codec == "vanilla":
            from cachette.codecs.vanilla import VanillaCodec

            codec = VanillaCodec()

        if self._backend == "dynamodb":
            from cachette.backends.dynamodb import DynamoDBBackend

            self.backend = run(
                DynamoDBBackend.init(
                    codec, self._table_name, self._ttl, self._region, self._dynamodb_url
                )
            )
        elif self._backend == "inmemory":
            from cachette.backends.inmemory import InMemoryBackend

            self.backend = InMemoryBackend(codec=codec, ttl=self._ttl)
        elif self._backend == "memcached":
            from cachette.backends.memcached import MemcachedBackend

            self.backend = run(MemcachedBackend.init(codec, self._memcached_host, self._ttl))
        elif self._backend == "mongodb":
            from cachette.backends.mongodb import MongoDBBackend

            self.backend = run(
                MongoDBBackend.init(
                    codec,
                    self._database_name,
                    self._table_name,
                    self._ttl,
                    self._mongodb_url,
                )
            )
        elif self._backend == "pickle":
            from cachette.backends.pickle import PickleBackend

            ### Ignore codec when pickle backend is chosen ###
            self.backend = PickleBackend(pickle_path=self._pickle_path, ttl=self._ttl)
        elif self._backend == "redis":
            from cachette.backends.redis import RedisBackend

            self.backend = run(RedisBackend.init(codec, self._redis_url, self._ttl))

    ### Override methods to initiated backend instance ###
    async def fetch(self, key: str) -> Any:
        """
        Fetches the value from cache

        ---
        :param:  key  `str` identifies key-value pair
        """
        return await self.backend.fetch(key)

    async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
        """
        Fetches the value from cache as well as remaining time to live.

        ---
        :param:  key  `str` identifies key-value pair
        :returns:  `Tuple[int, str]`  containing timetolive value (ttl) and value
        """
        return await self.backend.fetch_with_ttl(key)

    async def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Puts the value within the cache with key and assigned time-to-live value

        ---
        :param:  key  `str` identifies key-value pair
        :param:  value  `Any` value to have stored identified by key
        :param:  ttl  `int` time before value expires within cache; default: `None`
        """
        await self.backend.put(key, value, ttl)

    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        """
        Clears the cache identified by given `namespace` or `key`

        ---
        :param:  namespace  `str` identifies namespace to have entire cache cleared; default: `None`
        :param:  key  `str` identifies key-value pair to be cleared from cache; default: `None`
        :returns:  `int`  amount of items cleared
        """
        return await self.backend.clear(namespace, key)


__all__ = ["Cachette"]
