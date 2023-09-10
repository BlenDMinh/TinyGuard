from repository.test_repository import TestRepository
from service.baby_service import BabyService
from enum import Enum

Component = Enum('Component', [
    "BabyService",
    "TestRepository"
])


container = {
    Component.BabyService: BabyService(),
    Component.TestRepository: TestRepository()
}
