import database as _database
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


class ReviewPattern(_database.Base): #schemas
    __tablename__ = "review_pattern"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    pattern = _sql.Column(_sql.JSON)

    tasks = _orm.relationship("Task", back_populates="review_pattern")
