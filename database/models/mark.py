from sqlalchemy import VARCHAR, INTEGER, ForeignKey
from . import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Mark(Base):
    __tablename__ = 'marks'

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    mark: Mapped[int] = mapped_column(INTEGER)
    create_date: Mapped[datetime] = mapped_column()

