from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


app = Flask("Baby recognition")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    from config import config
    from route import route
    for url, handler in route.items():
        app.add_url_rule(
            url, endpoint=handler["endpoint"], view_func=handler["view"], methods=handler["methods"])

    app.run(
        debug=config["debug"],
        port=config["port"],
        host=config["host"]
    )
