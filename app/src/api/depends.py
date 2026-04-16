# ruff: noqa: B008
from fastapi import Depends
from sqlalchemy.orm import Session

from ..domain.use_cases.users.create_user import CreateUserUseCase
from ..domain.use_cases.users.delete_user import DeleteUserUseCase
from ..domain.use_cases.users.get_all_users import GetAllUsersUseCase
from ..domain.use_cases.users.get_user_by_id import GetUserByIdUseCase
from ..infrastructure.sqlite.database import get_db


async def gett_user_by_id_use_case(db: Session = Depends(get_db)) -> GetUserByIdUseCase:
    return GetUserByIdUseCase(db)


async def get_all_users_use_case(db: Session = Depends(get_db)) -> GetAllUsersUseCase:
    return GetAllUsersUseCase()


async def get_create_user_use_case(db: Session = Depends(get_db)) -> CreateUserUseCase:
    return CreateUserUseCase()


async def get_delete_user_use_case(db: Session = Depends(get_db)) -> DeleteUserUseCase:
    return DeleteUserUseCase()
