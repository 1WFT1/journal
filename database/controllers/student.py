from datetime import datetime

from sqlalchemy import select, update, and_

from database.database import db
from database.models.student import Student




async def new_student(name: str, username: str, password: str, class_id: int) -> int:
    """Создает нового пользователя"""
    async with db.begin() as session:
        new_class_instance = Student(name=name,
                                  username=username,
                                  password=password,
                                  class_id = class_id,
                                  create_date=datetime.now(),
                                  active_date=datetime.now()
                                  )
        session.add(new_class_instance)
        await session.flush()
        await session.commit()
        return new_class_instance.id


async def update_class(user_id: int, class_id: int) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Student)
            .where(Student.id == user_id)
            .values(class_id=class_id)
        )
        await session.commit()


# async def update_active_date(user_id: int) -> None:
#     """Обновляет дату последней активности пользователя"""
#     async with db.begin() as session:
#         await session.execute(
#             update(Student)
#             .where(Student.id == user_id)
#             .values(active_date=datetime.now())
#         )
#         await session.commit()


# Дополнительные полезные методы

async def get_by_id(user_id: int) -> Student | None:
    """Получает пользователя по ID"""
    async with db.begin() as session:
        result = await session.execute(
            select(Student)
            .where(Student.id == user_id)
        )
        user = result.scalar_one_or_none()
    return user


async def get_by_username(username: str) -> Student:
    """Получает пользователя по имени пользователя"""
    async with db.begin() as session:
        result = await session.execute(
            select(Student)
            .where(Student.username == username)
        )
        user = result.scalar_one_or_none()
    return user


async def auth(username: str, password: str) -> Student:
    """Получает пользователя по имени пользователя и паролю"""
    async with db.begin() as session:
        result = await session.execute(
            select(Student)
            .where(and_(Student.username == username,
                        Student.password == password))
        )
        user = result.scalar_one_or_none()
    return user



async def get_all() -> list[Student] | None:
    async with db.begin() as session:
        result = await session.scalars(select(Student))
        return result.all()
