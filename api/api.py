from fastapi import APIRouter, HTTPException, Response, status

from app.cache import LRUCache
from app.models import DataInCache, InfoAboutCache

cache_routers = APIRouter()


CACHE = LRUCache()


@cache_routers.get("/stats", response_model=InfoAboutCache)
async def get_cache_stats():
    data = await CACHE.cache_data()

    return InfoAboutCache.model_construct(**data)


@cache_routers.get("/{key}")
async def get_value_from_cache(key: str):

    value = await CACHE.get(key)

    if value is not None:
        return value

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")


@cache_routers.put(("/{key}"))
async def put_key_cache(key: str, body: DataInCache, response: Response):
    result = await CACHE.put(key=key,
                        value=body.value,
                        ttl=body.ttl)

    if not result:
        response.status_code = status.HTTP_201_CREATED


@cache_routers.delete(("/{key}"))
async def delete_key_in_cache(key: str, response: Response):
    result = await CACHE.delete(key=key)

    if result == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")
    
    response.status_code = status.HTTP_204_NO_CONTENT
