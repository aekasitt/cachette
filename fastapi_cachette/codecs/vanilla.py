#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  codecs/vanilla.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from typing import Any
### Local Modules ##
from fastapi_cachette.codecs import Codec

class VanillaCodec(Codec):

  def dumps(self, obj: Any) -> bytes:
    return str(obj).encode('utf-8')

  def loads(self, data: bytes) -> Any:
    return data.decode('utf-8')
  