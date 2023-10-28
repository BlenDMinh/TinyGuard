from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Select

from entity.auth_entity import LoginDetail
from entity.user import User


class AuthenticationService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, email: str, password: str):
        detail = LoginDetail.query.filter_by(User.user.has(email))
