from typing import List

from sqlalchemy.orm import Session

from ....infrastructure.sqlite.repositories.users import UserRepository
from ...schemas.users import LoginUserRequest, LoginUserResponse


class UserUseCase:
    def __init__(self):
        self._repo = UserRepository()