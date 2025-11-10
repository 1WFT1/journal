from sqlalchemy import VARCHAR, INTEGER, ForeignKey, ARRAY, DateTime
from sqlalchemy.sql import func
from . import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))

    theme: Mapped[str] = mapped_column(VARCHAR(500))

    present_students: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])
    late_students: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])
    not_student: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default=[])

    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    mark_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())