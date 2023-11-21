#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/inmemory.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

### Local Modules ###
from fastapi_cachette.backends import Backend
from fastapi_cachette.codecs import Codec


@dataclass
class Value:
    data: bytes
    expires: int


class InMemoryBackend(Backend):
    store: Dict[str, Value] = {}

    def __init__(self, codec: Codec, ttl: int):
        self.codec = codec
        self.ttl = ttl

    async def fetch(self, key: str) -> Any:
        value: Optional[Value] = self.store.get(key)
        if not value:
            return
        elif value.expires < self.now:
            del self.store[key]
        else:
            return self.codec.loads(value.data)

    async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
        value: Optional[Value] = self.store.get(key)
        if not value:
            return -1, None
        if value.expires < self.now:
            del self.store[key]
            return (0, None)
        else:
            return (value.expires - self.now, self.codec.loads(value.data))

    async def put(self, key: str, value: str, ttl: int = None) -> None:
        data: bytes = self.codec.dumps(value)
        expires: int = self.now + (ttl or self.ttl)
        self.store[key] = Value(data, expires)

    async def clear(
        self, namespace: Optional[str] = None, key: Optional[str] = None
    ) -> int:
        count: int = 0
        if namespace:
            keys: List[str] = list(
                filter(lambda key: key.startswith(namespace or ""), self.store.keys())
            )
            for key in keys:
                del self.store[key]
                count += 1
        elif key and self.store.get(key):
            del self.store[key]
            count += 1
        return count
