from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from main import db


class Device(db.Model):
    code: Mapped[str] = mapped_column(String, primary_key=True)
