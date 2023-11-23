#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  codecs/__init__.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-06 15:38
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module defining `Codec` abstract class defining subclasses' method schemas
"""

### Standard packages ###
from abc import abstractmethod
from typing import Any


class Codec:
    @abstractmethod
    def dumps(self, obj: Any) -> bytes:
        """
        ...
        """
        raise NotImplementedError

    @abstractmethod
    def loads(self, data: bytes) -> Any:
        """
        ...
        """
        raise NotImplementedError


__all__ = ["Codec"]
