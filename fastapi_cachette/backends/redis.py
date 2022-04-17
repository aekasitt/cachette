#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/redis.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Any, Optional, Tuple
### Third-Party Pacakges ###
from redis.asyncio import Redis
### Local Modules ###
from fastapi_cachette.backends import Backend
from fastapi_cachette.codecs import Codec

@dataclass
class RedisBackend(Backend):
  codec: Codec
  redis: Redis
  ttl: int

  @classmethod
  async def init(cls, codec: Codec, redis_url: str, ttl: int) -> 'RedisBackend':
    return cls(codec=codec, redis=Redis.from_url(url=redis_url), ttl=ttl)

  async def fetch(self, key) -> Any:
    data: bytes = await self.redis.get(key)
    if data: return self.codec.loads(data)

  async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
    async with self.redis.pipeline(transaction=True) as pipe:
      data: bytes = await (pipe.ttl(key).get(key).execute())
      if data: return self.codec.loads(data)

  async def put(self, key: str, value: Any, ttl: Optional[int] = None):
    data: bytes = self.codec.dumps(value)
    return await self.redis.set(key, data, ex=(ttl or self.ttl))

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    if namespace:
      lua: str = \
        f'for i, key in ipairs(redis.call("KEYS", "{namespace}:*")) do redis.call("DEL", key); end'
      return await self.redis.eval(lua, numkeys=0)
    elif key:
      return await self.redis.delete(key)
