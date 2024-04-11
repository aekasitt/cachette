#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:    backends/valkey.py
# VERSION:     0.1.8
# CREATED:     2024-04-10 22:06
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `ValkeyBackend` backend subclass used with Valkey key-value store"""

### Standard packages ###
from typing import Any, Optional, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictStr
from redis.asyncio import Redis

### Local modules ###
from cachette.backends import Backend
from cachette.codecs import Codec


class ValkeyBackend(Backend, BaseModel):
  class Config:
    arbitrary_types_allowed: bool = True

  codec: Codec
  ttl: int
  valkey_url: StrictStr

  async def fetch(self, key: str) -> Any:
    data: bytes = await self.redis.get(key)
    if data:
      return self.codec.loads(data)

  async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
    async with self.redis.pipeline(transaction=True) as pipe:
      data: bytes = await pipe.ttl(key).get(key).execute()
      if data:
        return self.codec.loads(data)
    return -1, None

  async def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
    data: bytes = self.codec.dumps(value)
    await self.redis.set(key, data, ex=(ttl or self.ttl))

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    if namespace:
      lua: str = (
        f'for i, key in ipairs(redis.call("KEYS", "{namespace}:*")) do redis.call("DEL", key); end'
      )
      return await self.redis.eval(lua, numkeys=0)
    elif key:
      return await self.redis.delete(key)
    return 0

  @property
  def redis(self) -> Redis:
    return Redis.from_url(url=self.valkey_url.replace("valkey://", "redis://"))


__all__ = ("ValkeyBackend",)
