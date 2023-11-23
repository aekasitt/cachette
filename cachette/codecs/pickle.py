#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/pickle.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `PickleCodec` codec subclass used for decoding and encoding pickled data
"""

### Standard packages ###
from pickle import dumps, loads
from typing import Any

### Local modules ###
from cachette.codecs import Codec


class PickleCodec(Codec):
    def dumps(self, obj: Any) -> bytes:
        return dumps(obj)

    def loads(self, data: bytes) -> Any:
        return loads(data)


__all__ = ["PickleCodec"]
