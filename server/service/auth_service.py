from http import HTTPStatus
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Select

from entity.auth_entity import LoginDetail
from entity.user import User


class AuthenticationService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, email: str, password: str):
        detail: LoginDetail = LoginDetail.query.filter(
            LoginDetail.user.has(email=email)).filter_by(
                password_hash=password
        ).first()
        if detail == None:
            return None
