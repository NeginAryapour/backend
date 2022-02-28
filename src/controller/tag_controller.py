
from typing import List

import fastapi as _fastapi
import service.services as _services
from fastapi import APIRouter
from schema.tag_schema import Tag, TagCreate
from schema.user_schema import User
from service.tag_service import TagService

from controller.user_controller import get

_db = _services.get_db()


router = APIRouter(
    prefix="/tags",
    # dependencies=[Depends(get_current_user)]
)
tagService = TagService(_db)



@router.post("/",response_model=Tag)
async def create(tag:TagCreate, user: User = _fastapi.Depends(get)):
    return tagService.create(tag=tag)


@router.get("/", response_model=List[Tag])
async def get_all(skip: int =0, limit:int = 10, user: User = _fastapi.Depends(get)):
    tags = tagService.get_all(skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model = Tag)
async def get(tag_id: int, user:User = _fastapi.Depends(get)):
    tag =  tagService.get(tag_id=tag_id)
    if tag is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this tag does not exist")
    return tag


@router.delete("/{tag_id}")
async def delete(tag_id: int, user: User = _fastapi.Depends(get)):
    tag =  tagService.get(tag_id=tag_id)
    if tag is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this tag does not exist")
    else:
        tagService.delete(tag_id=tag_id)
        return {"message":"successfully deleted tag with id : {tag_id}"}


@router.put("/{tag_id}", response_model=Tag)
async def update(tag_id: int,  tag:TagCreate, user: User = _fastapi.Depends(get)):
    return tagService.update(tag=tag,tag_id=tag_id)
        
