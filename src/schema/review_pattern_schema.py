from typing import List

import pydantic as _pydantic

from schema.task_schema import Task


class _ReviewPatternBase(_pydantic.BaseModel):
    title : str
    pattern : str

class ReviewPatternCreate(_ReviewPatternBase):
    pass


class ReviewPattern(_ReviewPatternBase):
    id : int

    class Config:
        orm_mode = True #TODO
