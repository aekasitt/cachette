#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  codecs/__init__.py
# VERSION: 	 0.1.4
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
### Standard Packages ###
from abc import abstractmethod
from typing import Any

class Codec:

  @abstractmethod
  def dumps(self, obj: Any) -> bytes:
    '''
    ...
    '''
    raise NotImplementedError

  @abstractmethod
  def loads(self, string: str) -> Any:
    '''
    ...
    '''
    raise NotImplementedError
