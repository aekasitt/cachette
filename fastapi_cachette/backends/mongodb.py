#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/mongodb.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-05 14:14
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from dataclasses import dataclass
from typing import Optional, Tuple
### Third-Party Packages ###
from motor.motor_asyncio import AsyncIOMotorClient
### Local Modules ###
from fastapi_cachette.backends import Backend

@dataclass
class MongoDBBackend(Backend):
  mongodb: AsyncIOMotorClient
  def __init__(self):
    pass

  async def fetch(self, key: str) -> str:
    pass

  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    pass

  async def put(self, key: str, value: str, expire: Optional[int] = None):
    pass

  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    pass
