#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/memcached.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `MemcachedBackend` backend subclass used with Memcached key-value store
"""

### Standard packages ###
from typing import Any, Optional, Tuple

### Third-party packages ###
from aiomcache import Client
from pydantic import BaseModel

### Local modules ###
from cachette.backends import Backend
from cachette.codecs import Codec


class MemcachedBackend(Backend, BaseModel):
    class Config:
        arbitrary_types_allowed: bool = True

    ### member vars ###
    codec: Codec
    mcache: Client
    ttl: int

    @classmethod
    async def init(cls, codec: Codec, memcached_host: str, ttl: int) -> "MemcachedBackend":
        return cls(codec=codec, mcache=Client(host=memcached_host), ttl=ttl)

    async def fetch(self, key: str) -> Any:
        data: Optional[bytes] = await self.mcache.get(key.encode())
        if data:
            return self.codec.loads(data)

    async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
        data: Optional[bytes] = await self.mcache.get(key.encode())
        if data:
            return 3600, self.codec.loads(data)
        return 0, None

    async def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        data: bytes = self.codec.dumps(value)
        await self.mcache.set(key.encode(), data, exptime=ttl or self.ttl)

    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        count: int = 0
        if namespace:
            raise NotImplementedError
        elif key:
            count += (0, 1)[await self.mcache.delete(key.encode())]
        return count


__all__ = ["MemcachedBackend"]
