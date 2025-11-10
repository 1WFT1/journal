from sqlalchemy import select, update, and_

from database.database import db
from database.models.subject import Subject




async def new_subject(name: str) -> int:
    async with db.begin() as session:
        new_class_instance = Subject(name=name)
        session.add(new_class_instance)
        await session.flush()
        await session.commit()
        return new_class_instance.id


async def update_name(subject_id: int, name: str) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Subject)
            .where(Subject.id == subject_id)
            .values(name=name)
        )
        await session.commit()

async def get_by_name(name: str) -> Subject | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Subject)
            .where(Subject.name == name)
        )
        subject = result.scalar_one_or_none()
    return subject

async def get_by_id(subject_id: int) -> Subject | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Subject)
            .where(Subject.id == subject_id)
        )
        subject = result.scalar_one_or_none()
    return subject



async def get_all() -> list[Subject] | None:
    async with db.begin() as session:
        result = await session.scalars(select(Subject))
        return result.all()


# async def get_by_name(name: str) ->  Subject | None:
#     async with db.begin() as session:
#         result = await session.execute(
#             select(Subject)
#             .where(Subject.name == name)
#         )
#         subject = result.scalar_one_or_none()
#     return subject
