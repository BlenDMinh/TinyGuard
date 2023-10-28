from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import config

db = config.db


@dataclass
class Device(db.Model):
    code: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="devices")
