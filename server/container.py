from repository.test_repository import TestRepository
from service.auth_service import AuthenticationService
from service.baby_service import BabyService
from enum import Enum
from main import db

Component = Enum('Component', [
    "BabyService",
    "TestRepository"
    "AuthenticationService"
])


container = {
    Component.BabyService: BabyService(),
    Component.TestRepository: TestRepository(),
    Component.AuthenticationService: AuthenticationService(db)
}
