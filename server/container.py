from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from repository.test_repository import TestRepository
from service.user_service import UserService
from service.auth_service import AuthenticationService
from service.baby_service import BabyService
from enum import Enum

import config

db = config.db

Component = Enum('Component', [
    "App",
    "Db",
    "BabyService",
    "UserService",
    "TestRepository",
    "AuthenticationService"
])

_userService = UserService(db=db)

container = {
    Component.BabyService: BabyService(),
    Component.UserService: _userService,
    Component.TestRepository: TestRepository(),
    Component.AuthenticationService: AuthenticationService(db, _userService)
}
