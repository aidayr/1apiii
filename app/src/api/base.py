# ruff: noqa: B008
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..domain.use_cases.categories import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetAllCategoriesUseCase,
    GetCategoryByIdUseCase,
)
from ..domain.use_cases.locations import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetAllLocationsUseCase,
    GetLocationByIdUseCase,
)
from ..domain.use_cases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
)
from ..infrastructure.sqlite.database import get_db
from ..schemas.categories import Category
from ..schemas.locations import Location
from ..schemas.users import LoginUserResponse, RegisterUserRequest

router = APIRouter()


@router.get("/users", response_model=list[LoginUserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    use_case = GetAllUsersUseCase()
    return await use_case.execute()


@router.get("/users/{user_id}", response_model=LoginUserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    use_case = GetUserByIdUseCase()
    return await use_case.execute(user_id)


@router.post("/users", response_model=LoginUserResponse, status_code=201)
async def create_user(user_data: RegisterUserRequest, db: Session = Depends(get_db)):
    use_case = CreateUserUseCase()
    return await use_case.execute(user_data)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    use_case = DeleteUserUseCase()
    await use_case.execute(user_id)
    return None


@router.get("/locations", response_model=list[Location])
async def get_all_locations(db: Session = Depends(get_db)):
    use_case = GetAllLocationsUseCase()
    return await use_case.execute()


@router.get("/locations/{location_id}", response_model=Location)
async def get_location_by_id(location_id: int, db: Session = Depends(get_db)):
    use_case = GetLocationByIdUseCase()
    return await use_case.execute(location_id)


@router.post("/locations", response_model=Location, status_code=201)
async def create_location(name: str, db: Session = Depends(get_db)):
    use_case = CreateLocationUseCase()
    return await use_case.execute(name)


@router.delete("/locations/{location_id}", status_code=204)
async def delete_location(location_id: int, db: Session = Depends(get_db)):
    use_case = DeleteLocationUseCase()
    await use_case.execute(location_id)
    return None


@router.get("/categories", response_model=list[Category])
async def get_all_categories(db: Session = Depends(get_db)):
    use_case = GetAllCategoriesUseCase()
    return await use_case.execute()


@router.get("/categories/{category_id}", response_model=Category)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    use_case = GetCategoryByIdUseCase()
    return await use_case.execute(category_id)


@router.post("/categories", response_model=Category, status_code=201)
async def create_category(
    title: str, description: str, slug: str, db: Session = Depends(get_db)
):
    use_case = CreateCategoryUseCase()
    return await use_case.execute(title, description, slug)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    use_case = DeleteCategoryUseCase()
    await use_case.execute(category_id)
    return None
