#!/usr/bin/env python3
"""
Module that contains the class Cache
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any


class Cache(object):
    """ Caching object """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """

        Args:
           data: string, bytes, int or float

        Returns:
             A string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
