import database as _database
import passlib.hash as _hash
import sqlalchemy as _sql
import sqlalchemy.orm as _orm


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    
    tasks = _orm.relationship("Task", back_populates="owner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

    def __str__(self) -> str:
        user_str = f"id = {self.id}\nemail = {self.email}\n tasks = {self.tasks}"
        return user_str
