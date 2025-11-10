from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class Class(Base):
    __tablename__ = 'classes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True)