from main import db
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LoginDetail(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='children')
    password_hash: Mapped[str] = mapped_column(String)


class LoginSession(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='children')
    access_token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
