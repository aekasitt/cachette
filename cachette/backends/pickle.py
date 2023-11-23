#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  backends/pickle.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-11-22 23:29
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pickle import load, dump
from typing import Any, Dict, Optional, Tuple

### Third-party packages ###
from pydantic import BaseModel, StrictInt, StrictStr

### Local modules ###
from cachette.backends import Backend


class Value(BaseModel):
    data: Any
    expires: StrictInt


class PickleBackend(Backend, BaseModel):
    pickle_path: StrictStr
    ttl: StrictInt

    # def __init__(self, pickle_path: str, ttl: int) -> None:
    #     ### TODO: reimplement ###
    #     self.pickle_path = pickle_path
    #     self.ttl = ttl
    #     values: Dict[str, Value]
    #     try:
    #         with open(self.pickle_path, "rb") as f:
    #             values = load(f) or {}
    #     except FileNotFoundError:
    #         values = {}
    #     with open(self.pickle_path, "wb") as f:
    #         dump(values, f)

    async def fetch(self, key: str) -> Optional[Any]:
        values: Dict[str, Value]
        try:
            with open(self.pickle_path, "rb") as f:
                values = load(f) or {}
                value: Value = values.get(key, None)
                if value is not None and value.expires < self.now:
                    if key in values.keys():
                        values.pop(key)
                    with open(self.pickle_path, "wb") as f:
                        dump(values, f)
                    return None
                return value.data if value is not None else None
        except FileNotFoundError:
            pass

    async def fetch_with_ttl(self, key: str) -> Tuple[int, Any]:
        values: Dict[str, Value]
        try:
            with open(self.pickle_path, "rb") as f:
                values = load(f) or {}
                value: Value = values.get(key, None)
                if value is not None and value.expires < self.now:
                    if key in values.keys():
                        values.pop(key)
                    with open(self.pickle_path, "wb") as f:
                        dump(values, f)
                    return (0, None)
                return (value.expires, value.data) if value is not None else None
        except FileNotFoundError:
            return (0, None)

    async def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        values: Dict[str, Value]
        try:
            with open(self.pickle_path, "rb") as f:
                values = load(f)
        except FileNotFoundError:
            values = {}
        values[key] = Value(data=value, expires=self.now + (ttl or self.ttl))
        with open(self.pickle_path, "wb") as f:
            dump(values, f)

    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        if namespace is not None:
            raise NotImplemented
        elif key is not None:
            values: Dict[str, Value]
            try:
                with open(self.pickle_path, "rb") as f:
                    values = load(f)
            except FileNotFoundError:
                return 0
            cleared: int = 0
            if key in values.keys():
                value = values.pop(key)
                if value.expires >= self.now:
                    cleared = 1
            with open(self.pickle_path, "wb") as f:
                dump(values, f)
            return cleared
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
