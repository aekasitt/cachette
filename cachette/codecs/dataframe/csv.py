#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/dataframe/csv.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-09 13:02
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining `CSVCodec` codec subclass used for decoding and encoding csv-formatted dataframes
"""

### Standard packages ###
from io import BytesIO, StringIO

### Third-party packages ###
from pandas import DataFrame, read_csv

### Local modules ##
from cachette.codecs import Codec


class CSVCodec(Codec):
    def dumps(self, df: DataFrame) -> bytes:
        bytes_io: BytesIO = BytesIO()
        df.to_csv(bytes_io)
        return bytes_io.getvalue()

    def loads(self, data: bytes) -> DataFrame:
        string_io: StringIO = StringIO(data.decode())
        return read_csv(string_io, index_col=0)


__all__ = ["CSVCodec"]
