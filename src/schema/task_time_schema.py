import datetime as _dt

import pydantic as _pydantic

from schema.association_schema import Association
from schema.tag_schema import Tag


class _TaskTimeBase(_pydantic.BaseModel):
    task_id: int = None
    start_date: _dt.datetime
    end_date: _dt.datetime = None
    def __str__(self) :
        pass

    


class TaskTimeCreate(_TaskTimeBase):
    pass

    

class TaskTime(_TaskTimeBase):
    id: int
    
    

    class Config:
        orm_mode = True #TODO
