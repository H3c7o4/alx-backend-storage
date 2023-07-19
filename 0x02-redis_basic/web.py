#!/usr/bin/env python3
"""
This module contains the function get_page(url)
"""
import redis
import requests
r = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """

    Args:
       url: link to the page

    Returns:
         HTML content
    """
    r.set(f'cached:{url}', count)
    resp = requests.get(url)
    r.incr(f'count:{url}')
    r.setex(f'cached:{url}', 10, r.get(f'cached:{url}'))
    return resp.text


if __name__ == "__main__":
    data = get_page('http://slowwly.robertomurray.co.uk')
    print(data)
