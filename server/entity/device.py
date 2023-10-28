from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

import config

db = config.db


class Device(db.Model):
    code: Mapped[str] = mapped_column(String, primary_key=True)
