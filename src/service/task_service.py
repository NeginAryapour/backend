import fastapi as _fastapi
import sqlalchemy.orm as _orm
from model.review_pattern_model import ReviewPattern
from model.task_model import Tag, Task
from schema.tag_schema import TagCreate
from schema.task_schema import TaskCreate
from sqlalchemy import null
import datetime as _dt

from service.review_pattern_service import ReviewPatternService


class TaskService:
    def __init__(self, db: _orm.Session):
        self.db = db
        self.review_pattern_service = ReviewPatternService(db)

    def create(self, task: TaskCreate, user_id: int):
        task = Task(**task.dict(), owner_id=user_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        if task.review_pattern_id:
            review_pattern = self.review_pattern_service.get(
                task.review_pattern_id
            )  # task besazim say konm az front list begirm
            review_pattern_list = review_pattern.pattern
            print("*****************************")
            print(review_pattern_list)
            print("*****************************")
            for i in review_pattern_list:
                print(f"{type(i)}")
                task_i = TaskCreate(
                    title=task.title,
                    content=task.content,
                    priority=task.priority,
                    color=task.color,
                    is_done=task.is_done,
                    main_task_id=task.id,
                    tags=task.tags,
                    date=_dt.datetime.now()+_dt.timedelta(days=i))
                print("**********************")
                print(task_i)
            #     print("************************")
                self.create(task=task_i, user_id=user_id)
            
        return task

    def get_all(self, skip: int, limit: int, user_id: int):
        return (
            self.db.query(Task)
            .options(_orm.joinedload(Task.tags))
            .filter(Task.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )  # not good for pagination but people use it

    def get(self, task_id: int):
        return (
            self.db.query(Task)
            .options(_orm.joinedload(Task.tags))
            .filter(Task.id == task_id)
            .first()
        )

    def delete(self, task_id: int):
        self.db.query(Task).filter(Task.id == task_id).delete()  # message when it's not
        self.db.commit()

    def update(self, task: TaskCreate, task_id: int):
        db_task = self.get(task_id=task_id)
        if not db_task:
            raise _fastapi.HTTPException(
                status_code=404, detail="sorry this task does not exist"
            )
        db_task.title = task.title
        db_task.content = task.content
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def add_tag(self, task_id: int, tag_id: int):
        db_task = self.get(task_id=task_id)
        if not db_task:
            raise _fastapi.HTTPException(
                status_code=404, detail="sorry this task does not exist"
            )
        db_tag = self.get_tag(tag_id=tag_id)
        if not db_tag:
            raise _fastapi.HTTPException(
                status_code=404, detail="sorry this tag does not exist"
            )
        db_task.tags.append(db_tag)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_tags(self, skip: int, limit: int, task_id: int):
        tags = (
            self.db.query(Tag)
            .options(_orm.joinedload(Tag.tasks, innerjoin=True))
            .where(Task.id == task_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return tags

    def get_tag(self, tag_id: int):
        tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        return tag

    def remove_tag(self, task_id: int, tag_id: int):
        db_task = self.get(task_id=task_id)
        if not db_task:
            raise _fastapi.HTTPException(
                status_code=404, detail="sorry this task does not exist"
            )
        db_tag = self.get_tag(tag_id=tag_id)
        if not db_tag:
            raise _fastapi.HTTPException(
                status_code=404, detail="sorry this tag does not exist"
            )
        # self.db.query(Tag).filter(Tag.id == tag_id).delete() #message when it's not
        db_task.tags.remove(db_tag)
        self.db.commit()
