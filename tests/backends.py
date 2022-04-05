#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022 All rights reserved.
# FILENAME:  tests/basics.py
# VERSION: 	 0.1.0
# CREATED: 	 2022-04-03 21:08
# AUTHOR: 	 Sitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
'''
Test Suite containing different Backend implementations on TestClient
'''
### Standard Packages ###
from time import sleep
### Third-Party Packages ###
from fastapi.responses import Response
from fastapi.testclient import TestClient
from pytest import mark
### Local Modules ###
from tests import client, Payload

@mark.parametrize('client', [
  [('backend', 'dynamodb'), ('expire', 2), ('dynamodb_url', 'http://localhost:8000')],
  [('backend', 'inmemory'), ('expire', 2)],
  [('backend', 'memcached'), ('expire', 2), ('memcached_host', 'localhost')],
  [('backend', 'redis'), ('expire', 2), ('redis_url', 'redis://localhost:6379')]
], indirect=True)
def test_set_and_wait_til_expired(client: TestClient):
  ### Get key-value before setting anything ###
  response: Response = client.get('/cache')
  assert response.text == ''
  ### Setting key-value pair with Payload ###
  payload: Payload = Payload(key='cache', value='cachable')
  response = client.post('/', data=payload.json())
  assert response.text == 'OK'
  ### Getting cached value within TTL ###
  response = client.get('/cache')
  assert response.text == 'cachable'
  ### Sleeps on current thread until TTL expires ###
  sleep(3)
  ### Getting cached value after TTL expires ###
  response = client.get('/cache')
  assert response.text == ''
  ### Clear ###
  response = client.delete('/cache')
  assert response.text == '' ### Nothing to clear

@mark.parametrize('client', [
  [('backend', 'dynamodb'), ('dynamodb_url', 'http://localhost:8000')],
  [('backend', 'inmemory')],
  [('backend', 'memcached'), ('memcached_host', 'localhost')],
  [('backend', 'redis'), ('redis_url', 'redis://localhost:6379')]
], indirect=True)
def test_set_then_clear(client: TestClient):
  ### Get key-value before setting anything ###
  response: Response = client.get('/cache')
  assert response.text == ''
  ### Setting key-value pair with Payload ###
  payload: Payload = Payload(key='cache', value='cachable')
  response = client.post('/', data=payload.json())
  assert response.text == 'OK'
  ### Getting cached value within TTL ###
  response = client.get('/cache')
  assert response.text == 'cachable'
  ### Clear ###
  response = client.delete('/cache')
  assert response.text == 'OK'
