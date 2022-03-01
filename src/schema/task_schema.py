import datetime as _dt
from typing import List

import pydantic as _pydantic
from schema.task_time_schema import TaskTime


from schema.tag_schema import Tag


class _TaskBase(_pydantic.BaseModel):
    title: str
    content: str
    priority: int
    color: str
    is_done: bool = False
    main_task_id: int = None
    tags: List[Tag] = []
    task_times: List[TaskTime] = []
    review_pattern_id: int = None
    date: _dt.datetime

    def __str__(self):
        task_str = f"title={self.title}\n\
            content={self.content}\n\
                priority={self.priority}\n\
                    color={self.color}\n\
                        isdone={self.is_done}\n\
                            date={self.date}\n\
                                task_times={self.task_times}\n\
                                    review_pattern_id={self.review_pattern_id}\n\
                                        tags={self.tags}\n\
                                            main_task_id={self.main_task_id}"
        return task_str


class TaskCreate(_TaskBase):
    pass

    def __str__(self):
        return super().__str__()


class Task(_TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True  # TODO
