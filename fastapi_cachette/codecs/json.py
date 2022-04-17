#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  codecs/json.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-07 12:23
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import Any
### Third-Party Packages ###
from json import dumps, loads
### Local Modules ##
from fastapi_cachette.codecs import Codec

class JSONCodec(Codec):

  def dumps(self, obj: Any) -> bytes:
    return dumps(obj).encode()

  def loads(self, data: bytes) -> Any:
    return loads(data)
  