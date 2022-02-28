
from typing import List

import pydantic as _pydantic

from schema.task_schema import Task


class _UserBase(_pydantic.BaseModel):
    email:str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id:int
    tasks : List[Task] = []

    class Config:
        orm_mode = True
