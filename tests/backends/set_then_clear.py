#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2024, All rights reserved.
# FILENAME:  tests/backends/set_then_clear.py
# VERSION: 	 0.1.8
# CREATED: 	 2022-04-15 19:06
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Module defining a test case where a key-value is set and then cleared
before fetching the same key-value pair again
"""

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
    [("backend", "dynamodb"), ("dynamodb_url", "http://localhost:8000")],
    [("backend", "inmemory")],
    [("backend", "memcached"), ("memcached_host", "localhost")],
    [
      ("backend", "mongodb"),
      ("database_name", "cachette-db"),
      ("mongodb_url", "mongodb://localhost:27017"),
    ],
    [("backend", "pickle"), ("pickle_path", "tests/cachette.pkl")],
    [("backend", "redis"), ("redis_url", "redis://localhost:6379")],
  ],
  ids=["dynamodb", "inmemory", "memcached", "mongodb", "pickle", "redis"],
  indirect=True,
)
def test_set_then_clear(client: TestClient):
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
  ### Clear ###
  response = client.delete("/cache")
  assert response.text == "OK"
