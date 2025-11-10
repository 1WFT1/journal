from datetime import datetime

from sqlalchemy import select, update, and_

from database.database import db
from database.models.mark import Mark


# получить все оценки ученика получить все оценки по предмету

#
# class Mark(Base):
#     __tablename__ = 'marks'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     student_id: Mapped[int] = mapped_column(ForeignKey("Student.id"))
#     teacher_id: Mapped[int] = mapped_column(ForeignKey("Teacher.id"))
#     subject_id: Mapped[int] = mapped_column(ForeignKey("Subject.id"))
#     mark: Mapped[int] = mapped_column(INTEGER)
#     create_date: Mapped[datetime] = mapped_column()




async def new_mark(student_id: int, teacher_id: int, subject_id: int,  mark: int) -> int:
    async with db.begin() as session:

        new_class_instance = Mark(student_id=student_id,
                               teacher_id=teacher_id,
                               subject_id=subject_id,
                               mark=mark,
                               create_date=datetime.now())
        session.add(new_class_instance)
        await session.flush()
        await session.commit()
        return new_class_instance.id


async def update_mark(mark_id: int, mark: str) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Mark)
            .where(Mark.id == mark_id)
            .values(mark=mark)
        )
        await session.commit()


async def get_all_by_student_id(student_id: int) -> list[Mark] | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Mark)
            .where(Mark.student_id == student_id)
        )
        marks = result.scalar_one_or_none()
    return marks



async def get_all_for_student_by_subject_id(student_id: int, subject_id: int) -> list[Mark] | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Mark)
            .where(and_(Mark.student_id == student_id, Mark.subject_id == subject_id))
        )
        marks = result.scalar_one_or_none()
    return marks


async def get_all() -> list[Mark] | None:
    async with db.begin() as session:
        result = await session.scalars(select(Mark))
        return result.all()


# async def get_by_id(mark_id: int) -> Mark | None:
#     async with db.begin() as session:
#         result = await session.execute(
#             select(Mark)
#             .where(Mark.id == mark_id)
#         )
#         subject = result.scalar_one_or_none()
#     return subject


# async def get_by_name(name: str) ->  Subject | None:
#     async with db.begin() as session:
#         result = await session.execute(
#             select(Subject)
#             .where(Subject.name == name)
#         )
#         subject = result.scalar_one_or_none()
#     return subject



# async def update_name(subject_id: int, name: str) -> None:
#     async with db.begin() as session:
#         await session.execute(
#             update(Subject)
#             .where(Subject.id == subject_id)
#             .values(name=name)
#         )
#         await session.commit()
