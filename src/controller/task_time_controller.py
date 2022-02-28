
from typing import List

import fastapi as _fastapi
import service.services as _services
from fastapi import APIRouter
from schema.task_time_schema import TaskTime, TaskTimeCreate
from schema.user_schema import User
from service.task_time_service import TaskTimeService

from controller.user_controller import get

_db = _services.get_db()


router = APIRouter(
    prefix="/task_time",
    # dependencies=[Depends(get_current_user)]
)
taskTimeService = TaskTimeService(_db)



@router.post("/",response_model=TaskTime)
async def create(task_time:TaskTimeCreate, user: User = _fastapi.Depends(get)):
    return taskTimeService.create(task_time=task_time)

@router.get("/{task_time_id}", response_model = TaskTime)
async def get(task_time_id: int, user:User = _fastapi.Depends(get)):
    task_time =  taskTimeService.get(task_time_id=task_time_id)
    if task_time is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task time does not exist")
    return task_time


@router.delete("/{task_time_id}")
async def delete(task_time_id: int, user: User = _fastapi.Depends(get)):
    task_time =  taskTimeService.get(task_time_id=task_time_id)
    if task_time is None:
        raise _fastapi.HTTPException(status_code=404, detail="sorry this task time does not exist")
    else:
        taskTimeService.delete(task_time_id=task_time_id)
        return {"message":"successfully deleted task time with id : {task_time_id}"}


@router.put("/{task_time_id}/stop", response_model=TaskTime)
async def stop_timer(task_time_id: int,  user: User = _fastapi.Depends(get)):
    return taskTimeService.stop_timer(task_time_id=task_time_id)


        
