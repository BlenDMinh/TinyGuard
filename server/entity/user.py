from dataclasses import dataclass
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import config

db = config.db


@dataclass
class User(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    phone_number: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    devices: Mapped[List["Device"]] = relationship(back_populates='user')
