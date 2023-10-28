from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
config = {
    "debug": True,
    "port": 5000,
    "host": "0.0.0.0"
}


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./database.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
