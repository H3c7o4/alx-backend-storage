#!/usr/bin/env python3
"""
Module that contains the class Cache
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def replay(function: Callable) -> None:
    """
    """
    key = function.__qualname__
    ins = key + ":inputs"
    outs = key + ":outputs"
    redis = function.__self__._redis
    count = redis.get(key).decode("utf-8")
    print(f"{key} was called {count} times")
    ins_list = redis.lrange(ins, 0, -1)
    outs_list = redis.lrange(outs, 0, -1)
    redis_zipped = list(zip(ins_list, outs_list))
    for a, b in redis_zipped:
        attr, data = a.decode("utf-8"), b.decode("utf-8")
        print(f"{key}(*{attr}) -> {data}")


def count_calls(method: Callable) -> Callable:
    """

    Args:
       method: method calls from cache object

    Returns:
         A callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """

    Args:
      method: A function

    Returns:
         A Callable
    """
    key = method.__qualname__
    ins = key + ":inputs"
    outs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapped function """
        self._redis.rpush(ins, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outs, str(data))
        return data
    return wrapper


class Cache(object):
    """ Caching object """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
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
