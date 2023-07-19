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

    def get(self, key: str,
            fn: Optional[Callable]) -> Union[str, bytes, int, float]:
        """

        Args:
           key: string argument
           fn: Callable argument

        Returns:
             None
        """
        data = self._redis.get(key)

        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """

        Args:
           key: string argument

        Returns:
             A string
        """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """

        Args:
           key: string argument

        Returns:
              An integer
        """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data
