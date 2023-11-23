#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/inmemory.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining backend subclass used with In-memory key-value store
"""

### Standard packages ###
from typing import Any, Dict, List, Optional, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictBytes, StrictInt, StrictStr

### Local modules ###
from cachette.backends import Backend
from cachette.codecs import Codec


class Value(BaseModel):
    data: StrictBytes
    expires: StrictInt


class InMemoryBackend(Backend):
    store: Dict[str, Value] = {}

    def __init__(self, codec: Codec, ttl: StrictInt):
        self.codec = codec
        self.ttl = ttl

    async def fetch(self, key: StrictStr) -> Any:
        value: Optional[Value] = self.store.get(key)
        if not value:
            return
        elif value.expires < self.now:
            del self.store[key]
        else:
            return self.codec.loads(value.data)

    async def fetch_with_ttl(self, key: StrictStr) -> Tuple[int, Any]:
        value: Optional[Value] = self.store.get(key)
        if not value:
            return -1, None
        if value.expires < self.now:
            del self.store[key]
            return (0, None)
        else:
            return (value.expires - self.now, self.codec.loads(value.data))

    async def put(self, key: StrictStr, value: StrictStr, ttl: Optional[StrictInt] = None) -> None:
        data: bytes = self.codec.dumps(value)
        expires: int = self.now + (ttl or self.ttl)
        self.store[key] = Value(data=data, expires=expires)

    async def clear(
        self, namespace: Optional[StrictStr] = None, key: Optional[StrictStr] = None
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


__all__ = ["InMemoryBackend"]
