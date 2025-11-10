from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    name: str
    username: str
    create_date: datetime
    active_date: datetime

    class Config:
        from_attributes = True


