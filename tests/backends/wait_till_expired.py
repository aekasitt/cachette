#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  tests/backends/wait_till_expired.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-15 19:06
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining a test case where a key-value is set with small ttl,
waited until expired, then have the same key-value fetched again
"""

### Standard packages ###
from time import sleep

### Third-party packages ###
from fastapi.responses import Response
from fastapi.testclient import TestClient
from pytest import mark

### Local modules ###
from tests import remove_pickles
from tests.backends import client, Payload


@mark.parametrize(
    "client",
    [
        [
            ("backend", "dynamodb"),
            ("ttl", 2),
            ("dynamodb_url", "http://localhost:8000"),
        ],
        [("backend", "inmemory"), ("ttl", 2)],
        [("backend", "memcached"), ("ttl", 2), ("memcached_host", "localhost")],
        [
            ("backend", "mongodb"),
            ("database_name", "cachette-db"),
            ("ttl", 2),
            ("mongodb_url", "mongodb://localhost:27017"),
        ],
        [("backend", "pickle"), ("ttl", 2), ("pickle_path", "tests/cachette.pkl")],
        [("backend", "redis"), ("ttl", 2), ("redis_url", "redis://localhost:6379")],
    ],
    ids=["dynamodb", "inmemory", "memcached", "mongodb", "pickle", "redis"],
    indirect=True,
)
def test_set_and_wait_til_expired(client: TestClient):
    ### Get key-value before setting anything ###
    response: Response = client.get("/cache")
    assert response.text == ""
    ### Setting key-value pair with Payload ###
    payload: Payload = Payload(key="cache", value="cachable")
    response = client.post("/", data=payload.json())
    assert response.text == "OK"
    ### Getting cached value within TTL ###
    response = client.get("/cache")
    assert response.text == "cachable"
    ### Sleeps on current thread until TTL ttls ###
    sleep(3)
    ### Getting cached value after TTL ttls ###
    response = client.get("/cache")
    assert response.text == ""
    ### Clear ###
    response = client.delete("/cache")
    assert response.text == ""  ### Nothing to clear
