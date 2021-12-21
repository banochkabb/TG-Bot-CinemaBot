from functools import lru_cache

from sqlmodel import Field, SQLModel, create_engine
from typing import Optional


class Cinema(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    req_name: str
    actual_ru_name: str


@lru_cache
def get_engine():
    return create_engine("sqlite:///database.db")
