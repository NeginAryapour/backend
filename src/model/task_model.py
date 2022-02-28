import datetime as _dt

import database as _database
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

association_table = _sql.Table('tag_and_task',_database.Base.metadata,
    _sql.Column('task_id', _sql.ForeignKey('tasks.id'), primary_key=True),
    _sql.Column('tag_id', _sql.ForeignKey('tags.id'), primary_key=True)
)


class Task(_database.Base): #schemas #TODO
    __tablename__ = "tasks"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    content = _sql.Column(_sql.String, index=True, nullable=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    priority = _sql.Column(_sql.Integer, nullable=True)
    color = _sql.Column(_sql.String, nullable=True)
    main_task_id = _sql.Column(_sql.Integer, _sql.ForeignKey("tasks.id"), nullable=True)
    is_done = _sql.Column(_sql.Boolean, default=False)
    review_pattern_id = _sql.Column(_sql.Integer, _sql.ForeignKey("review_pattern.id"), nullable=True)

    #TODO cycle
    owner = _orm.relationship("User", back_populates="tasks")
    main_task = _orm.relationship("Task") #bekhunam
    tags = _orm.relationship("Tag", 
                              secondary= association_table,
                              back_populates="tasks")

    review_pattern = _orm.relationship("ReviewPattern", back_populates="tasks")

    task_times = _orm.relationship("TaskTime",  back_populates="task")
    
 
    def __str__(self):
        task_str = f"id = {self.id}\ntitle = {self.title}\ncontent = {self.content}\nowner_id = {self.owner_id}\n date = {self.date}"
        return task_str


class Tag(_database.Base):
    __tablename__ = "tags"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)

    tasks = _orm.relationship("Task", 
                              secondary= association_table,
                              back_populates="tags")

    def __str__(self) -> str:
        tag_str = f"id={self.id}\ntitle={self.title}"
        return tag_str

    


