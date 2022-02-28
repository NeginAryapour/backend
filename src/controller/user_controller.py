import fastapi as _fastapi
import fastapi.security as _security
import service.services as _services
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from schema.user_schema import User, UserCreate
from service.user_service import UserService

_db = _services.get_db()

userService = UserService(_db)

router = APIRouter(
    # dependencies=[Depends(get_current_user)]
    prefix="/users"
)

async def get(token: str = _fastapi.Depends(userService.oauth2schema)):
    db_user = await userService.get_current_user(token=token)
    return db_user


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    db_user = await userService.get_by_email(email=user.email)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="the email is in use")
    user = await userService.create(user=user)
    return user


@router.post("/token")
async def generate_token(form_data:_security.OAuth2PasswordRequestForm=_fastapi.Depends()):
    user = await userService.authenticate(form_data.username, form_data.password)
    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="invalid credentials")
    token = await userService.create_token(user=user)
    return token


@router.get("/me", response_model=User)
async def login(user:User = _fastapi.Depends(userService.get_current_user)):
    json_user = jsonable_encoder(user)
    if not user:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this user does not exist")
    return json_user
