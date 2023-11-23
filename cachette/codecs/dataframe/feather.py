#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/dataframe/feather.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-09 13:02
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `FeatherCodec` codec subclass used for decoding and encoding feather dataframes
"""

### Standard packages ###
from io import BytesIO

### Third-party packages ###
from pandas import DataFrame, read_feather

### Local modules ##
from cachette.codecs import Codec


class FeatherCodec(Codec):
    def dumps(self, df: DataFrame) -> bytes:
        bytes_io: BytesIO = BytesIO()
        df.to_feather(bytes_io)
        return bytes_io.getvalue()

    def loads(self, data: bytes) -> DataFrame:
        bytes_io: BytesIO = BytesIO(data)
        return read_feather(bytes_io)


__all__ = ["FeatherCodec"]
