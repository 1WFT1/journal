from datetime import datetime

from sqlalchemy import select, update, and_

from database.database import db
from database.models import Class
from database.models.student import Student



async def new_class(name: str) -> int:
    async with db.begin() as session:
        new_class_instance = Class(name=name)
        session.add(new_class_instance)
        await session.flush()
        await session.commit()
        return new_class_instance.id

async def get_by_name(name: str) -> Class | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Class)
            .where(Class.name == name)
        )
        my_class = result.scalar_one_or_none()
    return my_class
