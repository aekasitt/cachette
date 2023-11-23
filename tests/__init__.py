#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  tests/__init__.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-03 21:08
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Previous implementations moved to tests/backends/__init__.py
"""

### Standard packages ###
from os import remove

### Third-party packages ###
from pytest import fixture


@fixture(autouse=True, scope="session")
def remove_pickles() -> None:
    """Fixture to be called after test session is over for cleaning up local pickle files"""
    yield
    file_exists: bool = False
    try:
        with open("tests/cachette.pkl", "rb"):
            file_exists = True
    except FileNotFoundError:
        pass
    if file_exists:
        remove("tests/cachette.pkl")


__all__ = ["remove_pickles"]
