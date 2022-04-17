#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  codecs/dataframe/csv.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-09 13:02
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from io import BytesIO, StringIO
### Third-Party Packages ###
from pandas import DataFrame, read_csv
### Local Modules ##
from fastapi_cachette.codecs import Codec

class CSVCodec(Codec):

  def dumps(self, df: DataFrame) -> bytes:
    bytes_io: BytesIO = BytesIO()
    df.to_csv(bytes_io)
    return bytes_io.getvalue()

  def loads(self, data: bytes) -> DataFrame:
    string_io: StringIO = StringIO(data.decode())
    return read_csv(string_io, index_col=0)
  