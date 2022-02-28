import datetime as _dt
from typing import List

import pydantic as _pydantic
from schema.task_time_schema import TaskTime


from schema.tag_schema import Tag


class _TaskBase(_pydantic.BaseModel):
    title : str
    content : str
    priority: int
    color : str
    is_done : bool
    main_task_id : int = None
    tags : List[Tag] = []
    task_times: List[TaskTime] = []
    review_pattern_id : int = None

    def __str__(self) :
        return self.title , self.content

    


class TaskCreate(_TaskBase):
    pass

    

class Task(_TaskBase):
    id: int
    owner_id: int
    date: _dt.datetime
    

    class Config:
        orm_mode = True #TODO
