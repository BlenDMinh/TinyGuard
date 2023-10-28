import datetime
from flask_sqlalchemy import SQLAlchemy

from entity.auth_entity import LoginDetail, LoginSession
import random

from model.auth_model import LoginInfo, RegisterInfo
from service.user_service import UserService


class AuthenticationService:
    def __init__(self, db: SQLAlchemy, user_service: UserService):
        self.db = db
        self.user_service = user_service

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

            random.seed(datetime.datetime.now().microsecond)
            refresh_token = random.getrandbits(16)
            access_token = random.getrandbits(16)

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
        user = self.user_service.create(
            register_info.username, register_info.age, register_info.email, register_info.phone_number)
        login_detail = LoginDetail(
            id=user.id,
            password_hash=register_info.password
        )
        self.db.session.add(login_detail)
        self.db.session.commit()
        return user
