#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/memcached.py
# VERSION: 	 0.1.1
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Any, Optional, Tuple
### Third-Party Packages ###
from aiomcache import Client
### Local Modules ###
from fastapi_cachette.backends import Backend
from fastapi_cachette.codecs import Codec

@dataclass
class MemcachedBackend(Backend):
  codec: Codec
  mcache: Client
  ttl: int

  @classmethod
  async def init(cls, codec: Codec, memcached_host: str, ttl: int) -> 'MemcachedBackend':
    return MemcachedBackend(codec=codec, mcache=Client(host=memcached_host), ttl=ttl)

  async def fetch(self, key: str) -> Any:
    return self.codec.loads(await self.mcache.get(key.encode()))

  async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
    return 3600, self.codec.loads(await self.mcache.get(key.encode()))

  async def put(self, key: str, value: Any, ttl: Optional[int] = None):
    data: str = self.codec.dumps(value)
    return await self.mcache.set(key.encode(), data.encode(), exptime=ttl or self.ttl)

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None):
    count: int = 0
    if namespace:
      raise NotImplementedError
    elif key:
      count += (0, 1)[await self.mcache.delete(key.encode())]      
    return count
