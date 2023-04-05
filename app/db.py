from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from config import Settings

settings = Settings()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Movies(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(unique=True)
    vote_average: Mapped[float]
    quantity: Mapped[int]
