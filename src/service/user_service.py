import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import passlib.hash as _hash
import sqlalchemy.orm as _orm
from fastapi.encoders import jsonable_encoder
from model.user_model import User as _User
from schema.user_schema import User, UserCreate

JWT_SECRET = "myjwtsecret"

class UserService:
    
    oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/users/token")
    
    def __init__(self, db: _orm.Session ):
        self.db = db
    
    async def get_by_email(self, email: str): 
        return self.db.query(_User).filter(_User.email == email).first()
        
    
    async def authenticate(self, email: str, password: str ): 
        user = await self.get_by_email(email=email) 
        if not user:
            return None 
        if not user.verify_password(password=password):
            return None 
        return user

    async def create_token(self, user: _User):
        user_obj = User.from_orm(user)
        user_json = jsonable_encoder(user_obj)
        token = _jwt.encode(user_json, JWT_SECRET)
        return dict(access_token=token, token_type="bearer")

    
    async def create(self, user:UserCreate):
        hashed_password = _hash.bcrypt.hash(user.password)
        db_user  = _User(email=user.email, hashed_password=hashed_password)
        self.db.add(db_user) #transaction
        self.db.commit() #actual work with db
        self.db.refresh(db_user) #give new id to db_user
        return db_user
    
    async def get_current_user(self, token: str = _fastapi.Depends(oauth2schema)):
        try:
            
            payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user = self.db.query(_User).get(payload["id"])
        except:
            raise _fastapi.HTTPException(status_code=401, detail= "Authentication Error")
        return User.from_orm(user)
    
