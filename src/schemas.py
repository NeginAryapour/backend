import datetime as _dt
from tkinter.tix import Tree
from typing import List
import pydantic as _pydantic

class _TaskBase(_pydantic.BaseModel):
    title : str
    content : str

# {
#     "titile": "first task title",
#     "content": "first task content"
# }

class TaskCreate(_TaskBase):
    pass

# {
#     "id":1,
#     "owner_id":12,
#     "titile": "first task title",
#     "content": "first task content",
#     "date_created":"12-12-12"
# }
class Task(_TaskBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    #TODO

    class Config:
        orm_mode = True

class _UserBase(_pydantic.BaseModel):
    email:str

class UserCreate(_UserBase):
    password: str

class User(_UserBase):
    id:int
    tasks : List[Task] = []

    class Config:
        orm_mode = True

