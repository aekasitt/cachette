#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  __init__.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""FastAPI extension that provides Cache Implementation Support
"""

__version__ = "0.1.7"

from .core import Cachette

__all__ = ["Cachette"]
