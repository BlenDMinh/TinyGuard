from dataclasses import dataclass
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entity.user import User
import config

db = config.db


@dataclass
class LoginDetail(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped['User'] = relationship()
    password_hash: Mapped[str] = mapped_column(String)


@dataclass
class LoginSession(db.Model):
    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped['User'] = relationship()
    access_token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
