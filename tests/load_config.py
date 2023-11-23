#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  tests/load_config.py
# VERSION: 	 0.1.6
# CREATED: 	 2022-04-03 20:34
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Test suite containing configuration loading tests via `LoadConfig`
"""

### Standard packages ###
from typing import Any, List, Tuple

### Third-party packages ###
from pydantic import ValidationError
from pytest import mark, raises

### Local modules ###
from fastapi_cachette import Cachette


@mark.parametrize(
    "configs",
    [
        ### DynamoDB ###
        [("backend", "dynamodb"), ("region", "ap-southeast-1")],
        [("backend", "dynamodb"), ("dynamodb_url", "http://localhost:8000")],
        [("backend", "dynamodb"), ("region", "ap-southeast-1"), ("ttl", 1)],
        [("backend", "dynamodb"), ("region", "ap-southeast-1"), ("ttl", 3600)],
        [
            ("backend", "dynamodb"),
            ("dynamodb_url", "http://localhost:8000"),
            ("ttl", 1),
        ],
        [
            ("backend", "dynamodb"),
            ("dynamodb_url", "http://localhost:8000"),
            ("ttl", 3600),
        ],
        ### InMemory ###
        [("backend", "inmemory")],
        [("backend", "inmemory"), ("ttl", 1)],
        [("backend", "inmemory"), ("ttl", 3600)],
        [("backend", "inmemory"), ("table_name", None)],
        ### Memcached ###
        [("backend", "memcached"), ("memcached_host", "localhost")],
        [("backend", "memcached"), ("ttl", 1), ("memcached_host", "localhost")],
        [
            ("backend", "memcached"),
            ("memcached_host", "localhost"),
            ("table_name", None),
        ],
        ### MongoDB ###
        [
            ("backend", "mongodb"),
            ("database_name", "fastapi-cachette-database"),
            ("mongodb_url", "mongodb://localhost:27017"),
        ],
        [
            ("backend", "mongodb"),
            ("database_name", "fastapi-cachette-database"),
            ("ttl", 1),
            ("mongodb_url", "mongodb://localhost:27017"),
        ],
        [
            ("backend", "mongodb"),
            ("database_name", "fastapi-cachette-database"),
            ("ttl", 3600),
            ("mongodb_url", "mongodb://localhost:27017"),
        ],
        ### Redis ###
        [("backend", "redis"), ("redis_url", "redis://localhost:6379")],
        [("backend", "redis"), ("ttl", 1), ("redis_url", "redis://localhost:6379")],
        [("backend", "redis"), ("ttl", 3600), ("redis_url", "redis://localhost:6379")],
        [
            ("backend", "redis"),
            ("redis_url", "redis://localhost:6379"),
            ("table_name", None),
        ],
    ],
)
def test_load_valid_configs(configs: List[Tuple[str, Any]]) -> None:
    @Cachette.load_config
    def load_cachette_configs() -> List[Tuple[str, Any]]:
        return configs


@mark.parametrize(
    "invalid_configs, reason",
    [
        ### AWS DynamoDB ###
        (
            [("backend", "dynamodb")],
            'The "dynamodb_url" cannot be null when using DynamoDB as backend and no region defined.',
        ),
        (
            [("backend", "dynamodb"), ("region", "ap-southeast-1"), ("ttl", 0)],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [("backend", "dynamodb"), ("region", "ap-southeast-1"), ("ttl", 3601)],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [
                ("backend", "dynamodb"),
                ("dynamodb_url", "http://localhost:8000"),
                ("ttl", 0),
            ],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [
                ("backend", "dynamodb"),
                ("dynamodb_url", "http://localhost:8000"),
                ("ttl", 3601),
            ],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [("backend", "dynamodb"), ("region", "not-valid")],
            'The "region" provided does not exist under AWS Regions.',
        ),
        (
            [
                ("backend", "dynamodb"),
                ("region", "ap-southeast-1"),
                ("table_name", None),
            ],
            'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.',
        ),
        (
            [
                ("backend", "dynamodb"),
                ("dynamodb_url", "http://localhost:8000"),
                ("table_name", None),
            ],
            'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.',
        ),
        ### InMemory ###
        (
            [("backend", "inmemory"), ("ttl", 0)],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [("backend", "inmemory"), ("ttl", 3601)],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        ### Memcached ###
        (
            [("backend", "memcached")],
            'The "memcached_host" cannot be null when using memcached as backend.',
        ),
        (
            [("backend", "memcached"), ("ttl", 0), ("memcached_host", "localhost")],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [("backend", "memcached"), ("ttl", 3601), ("memcached_host", "localhost")],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        ### MongoDB ###
        (
            [("backend", "mongodb")],
            'The "mongodb_url" cannot be null when using MongoDB as backend.',
        ),
        (
            [("backend", "mongodb"), ("database_name", "customized-database-name")],
            'The "mongodb_url" cannot be null when using MongoDB as backend.',
        ),
        (
            [
                ("backend", "mongodb"),
                ("mongodb_url", "mongodb://localhost:27017"),
                ("database_name", None),
            ],
            'The "database_name" cannot be null when using MongoDB as backend.',
        ),
        (
            [
                ("backend", "mongodb"),
                ("database_name", "customized-database-name"),
                ("mongodb_url", "http://localhost:27017"),
                ("table_name", None),
            ],
            'The "table_name" cannot be null when using DynamoDB / MongoDB as backend.',
        ),
        ### Redis ###
        (
            [("backend", "redis")],
            'The "redis_url" cannot be null when using redis as backend.',
        ),
        (
            [("backend", "redis"), ("ttl", 0), ("redis_url", "redis://localhost:6379")],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        (
            [
                ("backend", "redis"),
                ("ttl", 3601),
                ("redis_url", "redis://localhost:6379"),
            ],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
        ### Pickle ###
        (
            [("backend", "pickle")],
            'The "pickle_path" cannot be null when using pickle as backend.'
        ),
        (
            [("backend", "pickle"), ("ttl", 0), ("pickle_path", "tests/cache.pkl")],
            'The "ttl" value must between 1 or 3600 seconds.',
        ),
    ],
)
def test_load_invalid_configs(
    invalid_configs: List[Tuple[str, Any]], reason: str
) -> None:
    with raises(ValidationError) as exc_info:

        @Cachette.load_config
        def load_cachette_configs():
            return invalid_configs

    assert exc_info.match(reason)
