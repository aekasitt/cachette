#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/msgpack.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-07 2:08
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining `MsgpackCodec` codec subclass used for decoding and encoding msgpack-formatted data
"""

### Standard packages ###
from typing import Any

### Third-party packages ###
from msgpack import dumps, loads

### Local modules ##
from cachette.codecs import Codec


class MsgpackCodec(Codec):
    def dumps(self, obj: Any) -> bytes:
        return dumps(obj)

    def loads(self, data: bytes) -> Any:
        return loads(data)


__all__ = ["MsgpackCodec"]
