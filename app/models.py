from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String,ForeignKey,Text
from sqlalchemy.orm import Mapped, mapped_column,relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    blogs: Mapped[list["Blog"]] = relationship(
    back_populates="owner",
    )

    comments: Mapped[list["Comment"]] = relationship(
    back_populates="user",
    )

class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
    back_populates="blogs",
    )

    comments: Mapped[list["Comment"]] = relationship(
    back_populates="blog",
    )

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    blog_id: Mapped[int] = mapped_column(
        ForeignKey("blogs.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="comments",
    )

    blog: Mapped["Blog"] = relationship(
        back_populates="comments",
    )