from fastapi import APIRouter, Depends

from api.schemas.user import UserCreate, UserPublic
from database.controllers import teacher as teacher_controller
from .session import get_current_user

router = APIRouter()


@router.post("/teacher/new", response_model=None, status_code=201)
async def create_user(payload: UserCreate):
    await teacher_controller.new_teacher(name=payload.name, username=payload.username, password=payload.password)
    return {"status": "created"}


@router.get("/teacher/me", response_model=UserPublic)
async def users_me(current_user=Depends(get_current_user)):
    user = await teacher_controller.get_by_id(current_user["id"])
    return UserPublic.model_validate(user)