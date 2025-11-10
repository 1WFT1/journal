from sqlalchemy import VARCHAR, ForeignKey
from . import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    name: Mapped[str] = mapped_column(VARCHAR(64))
    username: Mapped[str] = mapped_column(VARCHAR(32))
    password: Mapped[str] = mapped_column(VARCHAR(64))
    present_lessons:Mapped[int] = 0
    late_lessons: Mapped[int] = 0
    not_lessons: Mapped[int] = 0
    create_date: Mapped[datetime] = mapped_column()
    active_date: Mapped[datetime] = mapped_column()
