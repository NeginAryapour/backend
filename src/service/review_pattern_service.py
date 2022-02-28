import fastapi as _fastapi
import sqlalchemy.orm as _orm
from model.review_pattern_model import ReviewPattern
from schema.review_pattern_schema import ReviewPatternCreate


class ReviewPatternService:
    def __init__(self, db: _orm.Session):
        self.db = db
    
    def create(self, review_pattern: ReviewPatternCreate):
        reviewPattern =ReviewPattern(**review_pattern.dict())
        self.db.add(reviewPattern)
        self.db.commit()
        self.db.refresh(reviewPattern)
        return reviewPattern
    

    def get_all(self, skip:int, limit:int):
        return self.db.query(ReviewPattern).offset(skip).limit(limit).all() #not good for pagination but people use it 
    
    def get(self, review_pattern_id:int): #?
        return self.db.query(ReviewPattern).filter(ReviewPattern.id == review_pattern_id).first()

    def delete(self, review_pattern_id:int): 
        self.db.query(ReviewPattern).filter(ReviewPattern.id == review_pattern_id).delete() #message when it's not 
        self.db.commit()

    def update(self, review_pattern: ReviewPatternCreate,review_pattern_id:int):
        db_reviw_pattern =  self.get(review_pattern_id=review_pattern_id)
        if not db_reviw_pattern:
            raise _fastapi.HTTPException(status_code=404, detail="sorry this reviw pattern does not exist")
        db_reviw_pattern.title = review_pattern.title
        db_reviw_pattern.pattern = review_pattern.pattern
        self.db.commit()
        self.db.refresh(db_reviw_pattern)
        return db_reviw_pattern
