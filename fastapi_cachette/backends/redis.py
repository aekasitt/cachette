#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/redis.py
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
### Third-Party Pacakges ###
from redis.asyncio import Redis
### Local Modules ###
from fastapi_cachette.backends import Backend

@dataclass
class RedisBackend(Backend):
  redis: Redis
  expire: int

  @classmethod
  async def init(cls, redis_url: str, expire: Optional[int] = None) -> 'RedisBackend':
    return cls(Redis.from_url(url=redis_url), expire)

  async def fetch(self, key) -> str:
    return await self.redis.get(key)

  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    async with self.redis.pipeline(transaction=True) as pipe:
      return await (pipe.ttl(key).get(key).execute())

  async def put(self, key: str, value: str, expire: Optional[int] = None):
    return await self.redis.set(key, value, ex=expire or self.expire)

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    if namespace:
      lua = f"for i, name in ipairs(redis.call('KEYS', '{namespace}:*')) do redis.call('DEL', name); end"
      return await self.redis.eval(lua, numkeys=0)
    elif key:
      return await self.redis.delete(key)
