#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/vanilla.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining `VanillaCodec` codec subclass used as default for decoding and encoding
basic data string-casted for storage
"""

### Standard packages ###
from typing import Any

### Local modules ##
from cachette.codecs import Codec


class VanillaCodec(Codec):
    def dumps(self, obj: Any) -> bytes:
        return str(obj).encode("utf-8")

    def loads(self, data: bytes) -> Any:
        return data.decode("utf-8")


__all__ = ["VanillaCodec"]
