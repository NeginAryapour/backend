import fastapi as _fastapi
import sqlalchemy.orm as _orm
from model.task_model import Tag
from schema.tag_schema import TagCreate


class TagService:
    def __init__(self, db: _orm.Session):
        self.db = db
    
    def create(self, tag: TagCreate): 
        tag = Tag(**tag.dict()) 
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    

    def get_all(self, skip:int, limit:int):  #?
        return self.db.query(Tag).options(_orm.joinedload(Tag.tasks)).offset(skip).limit(limit).all() 
    
    def get(self, tag_id:int):
        return self.db.query(Tag).options(_orm.joinedload(Tag.tasks)).filter(Tag.id == tag_id).first()

    def delete(self, tag_id:int):
        self.db.query(Tag).filter(Tag.id == tag_id).delete() 
        self.db.commit()

    def update(self, tag: TagCreate,tag_id:int):
        db_tag =  self.get(tag_id=tag_id)
        if not db_tag:
            raise _fastapi.HTTPException(status_code=404, detail="sorry this tag does not exist")
        db_tag.title = tag.title
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag
