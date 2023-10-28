from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

import config

db = config.db


class User(db.Model):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
