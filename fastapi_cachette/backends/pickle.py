#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/pickle.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-11-22 23:29
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pickle import loads, dumps
from typing import Any, Dict, Optional, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr

### Local modules ###
from fastapi_cachette.backends import Backend


class Value(BaseModel):
    data: Any
    expires: StrictInt


class PickleBackend(Backend):
    pickle_path: StrictStr

    def __init__(self, pickle_path: str, ttl: int) -> None:
        ### TODO: reimplement ###
        self.pickle_path = pickle_path
        values: Dict[str, Value]
        with open(self.pickle_path, "wb") as f:
            values = loads(f.read()) or {}
            dumps(f, values)

    async def fetch(self, key: str) -> Optional[Any]:
        ### TODO: reimplement ###
        values: Dict[str, Value]
        with open(self.pickle_path, "rb") as f:
            values = loads(f.read()) or {}
            value: Value = values.get(key, None)
            return value.data if value is not None else None

    async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
        ### TODO: reimplement ###
        values: Dict[str, Value]
        with open(self.pickle_path, "rb") as f:
            values = f.read() or {}
            value: Value = values.get(key, None)
            return (value.expires, value.data) if value is not None else None

    async def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ### TODO: reimplement ###
        values: Dict[str, Value]

    async def clear(
        self, namespace: Optional[str] = None, key: Optional[str] = None
    ) -> int:
        if namespace is not None:
            raise NotImplemented
        elif key is not None:
            raise NotImplemented
        file_exists: bool = False
        try:
            with open(self.pickle_path, "rb") as _:
                file_exists = True
        except FileNotFoundError:
            pass
        if not file_exists:
            return 0
        # TODO: remove file
        # remove(pickle_path)


__all__ = ["PickleBackend"]
