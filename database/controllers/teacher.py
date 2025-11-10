from datetime import datetime

from sqlalchemy import select, update, and_

from database.database import db
from database.models.teacher import Teacher





async def new_teacher(name: str, username: str, password: str) -> int:
    """Создает нового пользователя"""
    async with db.begin() as session:
        new_class_instance = Teacher(name=name,
                                  username=username,
                                  password=password,
                                  create_date=datetime.now(),
                                  active_date=datetime.now()
                                  )
        session.add(new_class_instance)
        await session.commit()
        return new_class_instance.id




async def update_active_date(user_id: int) -> None:
    """Обновляет дату последней активности пользователя"""
    async with db.begin() as session:
        await session.execute(
            update(Teacher)
            .where(Teacher.id == user_id)
            .values(active_date=datetime.now())
        )
        await session.commit()


# Дополнительные полезные методы

async def get_by_id(user_id: int) -> Teacher | None:
    """Получает пользователя по ID"""
    async with db.begin() as session:
        result = await session.execute(
            select(Teacher)
            .where(Teacher.id == user_id)
        )
        user = result.scalar_one_or_none()
    return user


async def get_by_username(user_name: str) -> Teacher:
    """Получает пользователя по имени пользователя"""
    async with db.begin() as session:
        result = await session.execute(
            select(Teacher)
            .where(Teacher.username == user_name)
        )
        user = result.scalar_one_or_none()
    return user


async def auth(username: str, password: str) -> Teacher | None:
    """Получает пользователя по имени пользователя и паролю"""
    async with db.begin() as session:
        result = await session.execute(
            select(Teacher)
            .where(and_(Teacher.username == username,
                        Teacher.password == password))
        )
        user = result.scalar_one_or_none()
    return user



async def get_all() -> list[Teacher] | None:
    async with db.begin() as session:
        result = await session.scalars(select(Teacher))
        return result.all()
