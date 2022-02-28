import datetime as _dt

import database as _database
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


class TaskTime(_database.Base):
    __tablename__ = "task_time"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    task_id = _sql.Column(_sql.Integer, _sql.ForeignKey("tasks.id"))

    start_date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    end_date = _sql.Column(_sql.DateTime)

    task = _orm.relationship("Task", back_populates="task_times")

    def __str__(self) -> str:
        timer_str = f"id={self.id}\ntask_id={self.task_id}\nstart_date={self.start_date}\nend_date={self.end_date}"
        return timer_str
