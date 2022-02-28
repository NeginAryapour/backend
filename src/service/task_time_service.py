import fastapi as _fastapi
import sqlalchemy.orm as _orm
from model.task_time_model import TaskTime
from schema.task_time_schema import TaskTimeCreate
import datetime as _dt


class TaskTimeService:
    def __init__(self, db: _orm.Session):
        self.db = db

    def create(self, task_time: TaskTimeCreate):
        task_time = TaskTime(**task_time.dict())
        self.db.add(task_time)
        self.db.commit()
        self.db.refresh(task_time)
        return task_time

    def get(self, task_time_id: int):
        return self.db.query(TaskTime).filter(TaskTime.id == task_time_id).first()

    def get_active_timer(self, task_id: int):
        return (
            self.db.query(TaskTime)
            .filter(TaskTime.task_id == task_id)
            .filter(TaskTime.start_date != None)
            .filter(TaskTime.end_date == None)
            .first()
        )

    def start_timer(self, task_id: int):
        active_timer = self.get_active_timer(task_id)
        if active_timer:
            raise _fastapi.HTTPException(
                status_code=400, detail="This task already has an active timer"
            )
        task_timer = TaskTimeCreate(task_id=task_id, start_date=_dt.datetime.utcnow())
        return self.create(task_time=task_timer)

    def stop_timer(self, task_id: int):
        active_timer = self.get_active_timer(task_id)
        if not active_timer:
            raise _fastapi.HTTPException(
                status_code=400, detail="There is no active timer for this task"
            )
        active_timer.end_date = _dt.datetime.utcnow()
        self.db.commit()
        return active_timer

    def delete(self, task_time_id: int):
        self.db.query(TaskTime).filter(TaskTime.id == task_time_id).delete()
        self.db.commit()
