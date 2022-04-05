#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  backends/__init__.py
# VERSION: 	 0.1.1
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Module containing `Backend` abstract class to be inherited by implementation-specific backends
'''
### Standard Packages ###
from abc import abstractmethod
from time import time
from typing import Optional, Tuple

class Backend:

  @property
  def now(self) -> int:
    return int(time())

  @abstractmethod
  async def fetch(self, key: str) -> str:
    '''
    Fetches the value from cache  

    ---
    :param:  key  `str` identifies key-value pair
    '''
    raise NotImplementedError

  @abstractmethod
  async def fetch_with_ttl(self, key: str) -> Tuple[int, str]:
    '''
    Fetches the value from cache as well as remaining time to live.

    ---
    :param:  key  `str` identifies key-value pair  
    :returns:  `Tuple[int, str]`  containing timetolive value (ttl) and value
    '''
    raise NotImplementedError

  @abstractmethod
  async def put(self, key: str, value: str, ttl: Optional[int] = None):
    '''
    Puts the value within the cache with key and assigned time-to-live value

    ---
    :param:  key  `str` identifies key-value pair  
    :param:  value  `str` value to have stored identified by key  
    :param:  ttl  `int` time before value expires within cache; default: `None`
    '''
    raise NotImplementedError

  @abstractmethod
  async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
    '''
    Clears the cache identified by given `namespace` or `key`  

    ---
    :param:  namespace  `str` identifies namespace to have entire cache cleared; default: `None`  
    :param:  key  `str` identifies key-value pair to be cleared from cache; default: `None`  
    :returns:  `int`  amount of items cleared
    '''
    raise NotImplementedError
