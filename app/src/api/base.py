# ruff: noqa: B008
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..domain.use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
)
from ..infrastructure.sqlite.database import get_db
from ..schemas.users import LoginUserResponse, RegisterUserRequest

router = APIRouter()


@router.get("/", response_model=list[LoginUserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    use_case = GetAllUsersUseCase()
    return await use_case.execute()


@router.get("/{user_id}", response_model=LoginUserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    use_case = GetUserByIdUseCase()
    return await use_case.execute(user_id)


@router.post("/", response_model=LoginUserResponse, status_code=201)
async def create_user(user_data: RegisterUserRequest, db: Session = Depends(get_db)):
    use_case = CreateUserUseCase()
    return await use_case.execute(user_data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    use_case = DeleteUserUseCase()
    await use_case.execute(user_id)
    return None
