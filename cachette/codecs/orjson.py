#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  codecs/json.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-07 12:23
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining `ORJSONCodec` codec subclass used for decoding and encoding json-formatted data
using `orjson` library
"""

### Standard packages ###
from typing import Any

### Third-party packages ###
from orjson import dumps, loads

### Local modules ##
from cachette.codecs import Codec


class ORJSONCodec(Codec):
  def dumps(self, obj: Any) -> bytes:
    return dumps(obj)

  def loads(self, data: bytes) -> Any:
    return loads(data)


__all__ = ["ORJSONCodec"]
