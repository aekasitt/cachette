#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/inmemory.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from time import time
from typing import Dict, List, Optional, Tuple
### Local Modules ###
from fastapi_cachette.backends import Backend

@dataclass
class Value:
  data: str
  ttl: int

class InMemoryBackend(Backend):
  store: Dict[str, Value] = {}

  def __init__(self, expire: Optional[int] = None):
    self.expire = expire
  
  async def fetch(self, key: str) -> str:
    value: Value = self.store.get(key)
    if not value: return
    elif value.ttl < self.now: del self.store[key]
    else: return value.data
  
  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    value: Value = self.store.get(key)
    if value.ttl < self.now:
      del self.store[key]
      return (0, None)
    else:
      return (value.ttl - self.now, value.data)
  
  async def put(self, key: str, value: str, expire: int = None):
    self.store[key] = Value(value, self.now + (expire or self.expire))

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    count: int = 0
    if namespace:
      keys: List[str] = filter(lambda key: key.startswith(namespace), self.store.keys())
      for key in keys:
        del self.store[key]
        count += 1
    elif key and self.store.get(key):
      del self.store[key]
      count += 1
    return count
