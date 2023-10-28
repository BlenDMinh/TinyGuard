import time
from flask_sqlalchemy import SQLAlchemy

from entity.auth_entity import LoginDetail, LoginSession
import random

from model.auth_model import LoginInfo, RegisterInfo


class AuthenticationService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, login_info: LoginInfo):
        if login_info.type == 0:
            email = login_info.email
            password = login_info.password
            detail: LoginDetail = LoginDetail.query.filter(
                LoginDetail.user.has(email=email)).filter_by(
                    password_hash=password
            ).first()
            if detail == None:
                return None

            session: LoginSession = LoginSession.query.filter(
                LoginSession.id == detail.id).first()
            if session != None:
                return session

            random.seed(time.now())
            refresh_token = random.getrandbits(128)
            access_token = random.getrandbits(128)

            session = LoginSession(
                id=detail.id, refresh_token=refresh_token, access_token=access_token)

            self.db.session.add(session)
            self.db.session.commit()

            return session
        elif login_info.type == 1:
            session = LoginSession.query.filter_by(
                access_token=login_info.access_token).first_or_404()
            return session

    def register(self, register_info: RegisterInfo):
        pass
