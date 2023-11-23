#!/usr/bin/env python3
# coding:utf-8
# Copyright (C) 2022-2023, All rights reserved.
# FILENAME:  config.py
# VERSION: 	 0.1.7
# CREATED: 	 2022-04-03 15:31
# AUTHOR: 	 Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""Module containing `CachetteConfig` class
"""

### Standard packages ###
from typing import Callable, List, Optional, Tuple

### Third-party packages ###
from pydantic import ValidationError

### Local modules ###
from cachette.load_config import LoadConfig


class CachetteConfig(object):
    ### Basics ###
    _backend: str = "inmemory"
    _codec: str = "vanilla"
    _ttl: int = 60

    ### Redis ###
    _redis_url: str

    ### Memcached ###
    _memcached_host: str

    ### AWS DynamoDB & MongoDB ###
    _table_name: str = "cachette"

    ### AWS DynamoDB ###
    _region: Optional[str]
    _dynamodb_url: Optional[str]

    ### MongoDB ###
    _database_name: str = "cachette-db"
    _mongodb_url: str

    ### Pickle ###
    _pickle_path: str

    @classmethod
    def load_config(cls, settings: Callable[..., List[Tuple]]) -> None:
        """
        Loads the Configuration from a Pydantic "BaseSettings" object or a List of parameter tuples.
        If not specified otherwise, each item should be provided as a string.

        ---
          backend -- optional; must be one of ["dynamodb", "inmemory", "memcached", "mongodb", "redis"];
            defaults to using inmemory option which required no extra package dependencies. To use other
            listed options; See installation guide on the README.md at
            [Repository Page](https://github.com/aekasitt/cachette).
          codec -- optional; serialization and de-serialization format to have cache values stored in
            the cache backend of choice as a string of selected encoding. once fetched, will have their
            decoded values returned of the same format. must be one of ["feather", "msgpack", "parquet",
            "pickle"]; if none is defined, will vanilla codec of basic string conversion will be used.
          ttl -- optional; the time-to-live or amount before this cache item expires within the cache;
            defaults to 60 (seconds) and must be between 1 second to 1 hour (3600 seconds).
          redis_url -- required when backend set to "redis"; the url set to redis-server instance with
            or without provided authentication in such formats "redis://user:password@host:port" and
            "redis://host:port" respectively.
          memcached_host -- required when backend set to "memcached"; the host endpoint to the memcached
            distributed memory caching system.
          table_name -- required when backend set to "dynamodb" or "mongodb"; name of the cache table or
            collection in case of "mongodb" backend to have key-value pairs stored; defaults to
            "cachette".
          region -- required when backend set to "dynamodb" and "dynamodb_url" not set; one of Amazon
            Web Services listed Regions which can be found on this Documentation
            [Page](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones)
          dynamodb_url -- required when backend set to "dynamodb" and "region" not set; this option is
            used when setting up your own DynamoDB Local instance according to this
            [Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal)
          database_name -- required when backend set to "mongodb"; the database name to be automatically
            created if not exists on the MongoDB instance and store the cache table; defaults to
            "cachette-db"
          mongodb_url -- required when backend set to "mongodb"; the url set to MongoDB database
            instance with or without provided authentication in such formats
            "mongodb://user:password@host:port" and "mongodb://host:port" respectively.
          pickle_path -- required when backend set to "pickle"; the file-system path to create local
            store using python pickling on local directory
        """
        try:
            config = LoadConfig(**{key.lower(): value for key, value in settings()})
            cls._backend = config.backend or cls._backend
            cls._codec = config.codec or cls._codec
            cls._ttl = config.ttl or cls._ttl
            cls._redis_url = config.redis_url or ""
            cls._memcached_host = config.memcached_host or ""
            cls._table_name = config.table_name or cls._table_name
            cls._region = config.region
            cls._dynamodb_url = config.dynamodb_url
            cls._database_name = config.database_name or cls._database_name
            cls._mongodb_url = config.mongodb_url or ""
            cls._pickle_path = config.pickle_path
        except ValidationError:
            raise
        except Exception:
            raise TypeError('CachetteConfig must be pydantic "BaseSettings" or list of tuples')


__all__ = ["CachetteConfig"]
