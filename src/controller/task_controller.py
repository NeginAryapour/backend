
from typing import List

import fastapi as _fastapi
import service.services as _services
from fastapi import APIRouter
from schema.task_time_schema import TaskTime
from schema.review_pattern_schema import ReviewPattern
# from model.review_pattern_model import ReviewPattern
from schema.tag_schema import Tag, TagCreate
from schema.task_schema import Task, TaskCreate
from schema.user_schema import User
from service.task_service import TaskService
from service.task_time_service import TaskTimeService

from controller.user_controller import get

_db = _services.get_db()


router = APIRouter(
    prefix="/tasks",
    # dependencies=[Depends(get_current_user)]
)
taskService = TaskService(_db)
taskTimeService = TaskTimeService(_db)


@router.post("/",response_model=Task)
async def create(task:TaskCreate, user: User = _fastapi.Depends(get)):
    return taskService.create(task=task, user_id=user.id)


@router.get("/", response_model=List[Task])
async def get_all(skip: int =0, limit:int = 10, user: User = _fastapi.Depends(get)):
    tasks = taskService.get_all(skip=skip, limit=limit, user_id= user.id)
    return tasks


@router.get("/{task_id}", response_model = Task)
async def get(task_id: int, user:User = _fastapi.Depends(get)):
    task =  taskService.get(task_id=task_id)
    if task is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task does not exist")
    return task


@router.delete("/{task_id}")
async def delete(task_id: int, user: User = _fastapi.Depends(get)):
    task =  taskService.get(task_id=task_id)
    if task is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task does not exist")
    else:
        taskService.delete(task_id=task_id)
        return {"message":"successfully deleted task with id : {task_id}"}


@router.put("/{task_id}", response_model=Task)
async def update(task_id: int,  task:TaskCreate, user: User = _fastapi.Depends(get)):
    return taskService.update(task=task,task_id=task_id)


@router.get("/{task_id}/tag", response_model = List[Tag])
async def get_tags(task_id: int, skip: int=0, limit:int=10 ,  user:User = _fastapi.Depends(get)):
    task = taskService.get(task_id=task_id)
    if task is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task does not exist")
    tags =  taskService.get_tags(skip=skip, limit=limit,task_id=task_id)
    return tags

@router.put("/{task_id}/tag", response_model=Task)
async def add_tag(task_id: int,  tag_id: int ,user: User = _fastapi.Depends(get)):
    return taskService.add_tag(task_id=task_id, tag_id=tag_id)  

@router.delete("/{task_id}/tag")
async def remove_tag(task_id: int, tag_id: int, user: User = _fastapi.Depends(get)):
    task =  taskService.get(task_id=task_id)
    if task is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task does not exist")

    taskService.remove_tag(task_id=task_id, tag_id=tag_id)
    return {"message":"successfully deleted task with id : {task_id}"}


@router.put("/{task_id}/start", response_model=TaskTime)
async def start_timer(task_id: int,  user: User = _fastapi.Depends(get)):
    return taskTimeService.start_timer(task_id=task_id)

@router.put("/{task_id}/stop", response_model=TaskTime)
async def stop_timer(task_id: int,  user: User = _fastapi.Depends(get)):
    return taskTimeService.stop_timer(task_id)
