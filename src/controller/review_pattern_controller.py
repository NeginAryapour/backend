from typing import List

import fastapi as _fastapi
import service.services as _services
from fastapi import APIRouter
from schema.review_pattern_schema import ReviewPattern, ReviewPatternCreate
from schema.user_schema import User
from service.review_pattern_service import ReviewPatternService

from controller.user_controller import get

_db = _services.get_db()


router = APIRouter(
    prefix="/review_patterns",
    # dependencies=[Depends(get_current_user)]
)
reviewPatternService = ReviewPatternService(_db)


@router.post("/", response_model=ReviewPattern)
async def create(
    review_pattern: ReviewPatternCreate, user: User = _fastapi.Depends(get)
):
    return reviewPatternService.create(review_pattern=review_pattern)


@router.get("/", response_model=List[ReviewPattern])
async def get_all(skip: int = 0, limit: int = 10, user: User = _fastapi.Depends(get)):
    review_patterns = reviewPatternService.get_all(skip=skip, limit=limit)
    return review_patterns


@router.get("/{review_pattern_id}", response_model=ReviewPattern)
async def get(review_pattern_id: int, user: User = _fastapi.Depends(get)):
    review_pattern = reviewPatternService.get(review_pattern_id=review_pattern_id)
    if review_pattern is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this review_pattern does not exist"
        )
    return review_pattern


@router.delete("/{review_pattern_id}")
async def delete(review_pattern_id: int, user: User = _fastapi.Depends(get)):
    review_pattern = reviewPatternService.get(review_pattern_id=review_pattern_id)
    if review_pattern is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this review_pattern does not exist"
        )
    else:
        reviewPatternService.delete(review_pattern_id=review_pattern_id)
        return {"message": "successfully deleted tag with id : {tag_id}"}


@router.put("/{review_pattern_id}", response_model=ReviewPattern)
async def update(
    review_pattern_id: int,
    review_pattern: ReviewPatternCreate,
    user: User = _fastapi.Depends(get),
):
    return reviewPatternService.update(
        review_pattern=review_pattern, review_pattern_id=review_pattern_id
    )
