from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from entity.auth_entity import *
from entity.device import *
from entity.user import *
from container import Component, container
import config

app = config.app
db = config.db

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    config = config.config
    from route import route
    for url, handler in route.items():
        app.add_url_rule(
            url, endpoint=handler["endpoint"], view_func=handler["view"], methods=handler["methods"])

    app.run(
        debug=config["debug"],
        port=config["port"],
        host=config["host"]
    )
