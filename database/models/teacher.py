from sqlalchemy import VARCHAR
from . import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


class Teacher(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(64))
    username: Mapped[str] = mapped_column(VARCHAR(32))
    password: Mapped[str] = mapped_column(VARCHAR(64))
    create_date: Mapped[datetime] = mapped_column()
    active_date: Mapped[datetime] = mapped_column()
