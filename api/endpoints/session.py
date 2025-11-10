import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Header
from starlette import status

from database.cache import cache
from database.controllers import teacher as teacher_controller
from api.schemas.session import LoginRequest, TokenResponse
router = APIRouter()


@router.post("/session/teacher/auth", response_model=TokenResponse)
async def auth(payload: LoginRequest):
    user = await teacher_controller.auth(payload.username, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = secrets.token_urlsafe(32)
    await cache.set_token(token, {"id": user.id, "username": user.username, "name": user.name, "role": "teacher"}, expire_seconds=int(timedelta(hours=2).total_seconds()))
    return TokenResponse(access_token=token)

@router.post("/session/user/auth", response_model=TokenResponse)
async def auth(payload: LoginRequest):
    pass


async def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    user_data = await cache.get_user_by_token(token)
    if user_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user_data
