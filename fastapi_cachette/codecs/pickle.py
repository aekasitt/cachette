#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  codecs/pickle.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from pickle import dumps, loads
from typing import Any
### Local Modules ###
from fastapi_cachette.codecs import Codec

class PickleCodec(Codec):

  def dumps(self, obj: Any) -> bytes:
    return dumps(obj)
  
  def loads(self, string: str) -> Any:
    return loads(string)
