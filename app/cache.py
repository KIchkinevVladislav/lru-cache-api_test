import time
from typing import Optional, Tuple
from collections import OrderedDict
import asyncio

from app.config import app_config


class LRUCache:
    def __init__(self):
        self.cache: OrderedDict[str, Tuple[Optional[str], Optional[int]]] = OrderedDict()
        self.capacity = abs(app_config.capacity_cache)
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> str | None:
        async with self.lock:
            if key not in self.cache:
                return False

            value, ttl = self.cache[key]
            if ttl and time.time() > ttl:
                del self.cache[key]
                return False

            self.cache.move_to_end(key, last=False)
            return value

    async def put(self, key: str, value: str, ttl: int = None) -> None:
        async with self.lock:
            if key in self.cache:
                _, old_ttl = self.cache[key]
                self.cache[key] = (value, time.time() + ttl if ttl else old_ttl)
                self.cache.move_to_end(key, last=False)

                return True
            else:
                if len(self.cache) == self.capacity:
                    self.cache.popitem()
                self.cache[key] = (value, time.time() + ttl if ttl else None)
                self.cache.move_to_end(key, last=False)


    async def delete(self, key: str):
        async with self.lock:
            if key not in self.cache:
                return False

            _, old_ttl = self.cache[key]
            self.cache[key] = (None, old_ttl)
            self.cache.move_to_end(key, last=False)
    
    async def cache_data(self):
        async with self.lock:

            cache_data = {"size": len(self.cache), 
                          "capacity": self.capacity,
                          "items": list(self.cache.keys())}
            return cache_data
