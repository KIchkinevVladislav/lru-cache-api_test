from typing import Optional

from pydantic import BaseModel, Field


class DataInCache(BaseModel):
    value: str
    ttl: Optional[int] = Field(default=None, gt=0)


class InfoAboutCache(BaseModel):
    size: int
    capacity: int
    items: list
