#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/redis.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `RedisBackend` backend subclass used with Redis key-value store
"""

### Standard packages ###
from typing import Any, Optional, Tuple

### Third-party packages ###
from pydantic import BaseModel
from redis.asyncio import Redis

### Local modules ###
from cachette.backends import Backend
from cachette.codecs import Codec


class RedisBackend(Backend, BaseModel):
    class Config:
        arbitrary_types_allowed: bool = True

    codec: Codec
    redis: Redis
    ttl: int

    @classmethod
    async def init(
        cls,
        codec: Codec,
        ttl: int,
        redis_url: str = None,
        redis_host: str = None,
        redis_port: int = None,
        redis_password: str = None,
        redis_username: str = None,
        redis_ssl: bool = False,
        redis_ssl_keyfile: str = None,
        redis_ssl_certfile: str = None,
        redis_ssl_ca_certs: str = None,
    ) -> "RedisBackend":
        if redis_url:
            return cls(codec=codec, redis=Redis.from_url(url=redis_url), ttl=ttl)
        else:
            redis_obj = Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                username=redis_username,
                ssl=redis_ssl,
                ssl_keyfile=redis_ssl_keyfile,
                ssl_certfile=redis_ssl_certfile,
                ssl_ca_certs=redis_ssl_ca_certs,
            )

            return cls(codec=codec, redis=redis_obj, ttl=ttl)

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
            lua: str = f'for i, key in ipairs(redis.call("KEYS", "{namespace}:*")) do redis.call("DEL", key); end'
            return await self.redis.eval(lua, numkeys=0)
        elif key:
            return await self.redis.delete(key)
        return 0


__all__ = ["RedisBackend"]
