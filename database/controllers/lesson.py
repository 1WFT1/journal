from datetime import datetime

from sqlalchemy import select, update, and_, func

from database.database import db
from database.models import Class, Lesson
from database.models.student import Student

# __tablename__ = 'lessons'
#
# id: Mapped[int] = mapped_column(primary_key=True)
# subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
# teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
# class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
#
# theme: Mapped[str] = mapped_column(VARCHAR(500))
#
# present_students: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])
# late_students: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])
# not_student: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])
#
# start_date: Mapped[datetime] = mapped_column(DateTime)
# end_date: Mapped[datetime] = mapped_column(DateTime)
# mark_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


async def new_lesson(subject_id: int,
                     teacher_id: int,
                     class_id: int,
                     theme: str,
                     present_students=None,
                     late_students=None,
                     not_student=None,
                     start_date=None,
                     end_date=None,
                     mark_date=None
                     ) -> int:

    async with db.begin() as session:
        lesson_instance = Lesson(subject_id=subject_id,
                                    teacher_id=teacher_id,
                                    class_id=class_id,
                                    theme=theme,
                                    present_students=present_students,
                                    late_students=late_students,
                                    not_student=not_student,
                                    start_date=start_date,
                                    end_date=end_date,
                                    mark_date=mark_date
                                    )
        session.add(lesson_instance)
        await session.flush()
        await session.commit()
        return lesson_instance.id

async def get_by_id(lesson_id: int) -> Lesson | None:
    async with db.begin() as session:
        result = await session.execute(
            select(Lesson)
            .where(Lesson.id == lesson_id)
        )
        my_class = result.scalar_one_or_none()
    return my_class


async def update_mark_date(lesson_id: int) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(mark_date=datetime.now())
        )
        await session.commit()


async def update_theme(lesson_id: int, theme: str) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(theme=theme)
        )
        await session.commit()


async def update_present_students(lesson_id: int, student_id: int) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(present_students=func.array_append(Lesson.present_students, student_id))
        )
        await session.commit()

async def update_late_students(lesson_id: int, student_id: int) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(late_students =func.array_append(Lesson.late_students , student_id))
        )
        await session.commit()

async def update_not_student(lesson_id: int, student_id: int) -> None:
    async with db.begin() as session:
        await session.execute(
            update(Lesson)
            .where(Lesson.id == lesson_id)
            .values(not_student  =func.array_append(Lesson.not_student , student_id))
        )
        await session.commit()