import datetime

from sqlalchemy import String, Float, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class ArticleRequest(Base):
    __tablename__ = "article_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    article: Mapped[str] = mapped_column(String(length=9), nullable=False)
    request_datetime: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now())
