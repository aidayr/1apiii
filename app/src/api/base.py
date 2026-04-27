# ruff: noqa: B008
from fastapi import APIRouter, Depends, status

from api.depends import (
    create_location_use_case,
    create_user_use_case,
    delete_location_use_case,
    delete_user_use_case,
    get_all_locations_use_case,
    get_all_users_use_case,
    get_location_by_id_use_case,
    get_user_by_id_use_case,
)
from app.src.domain.locations.use_cases import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetAllLocationsUseCase,
    GetLocationByIdUseCase,
)
from app.src.domain.users.use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
)
from src.schemas.locations import Location
from src.schemas.users import LoginUserResponse, RegisterUserRequest

router = APIRouter()


@router.get("/users", response_model=list[LoginUserResponse], status=status.HTTP_200_OK)
async def get_all_users(use_case: GetAllUsersUseCase = Depends(get_all_users_use_case)):
    return await use_case.execute()


@router.get(
    "/users/{user_id}",
    response_model=list[LoginUserResponse],
    status=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
    status=status.HTTP_200_OK,
):
    return await use_case.execute(user_id)


@router.post(
    "/users", response_model=LoginUserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: RegisterUserRequest,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
):
    return await use_case.execute(user_data)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, use_case: DeleteUserUseCase = Depends(delete_user_use_case)
):
    await use_case.execute(user_id)
    return None


@router.get(
    "/locations/{location_id}", response_model=Location, status_code=status.HTTP_200_OK
)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(get_location_by_id_use_case),
):
    return await use_case.execute(location_id)


@router.post("/locations", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    name: str,
    use_case: CreateLocationUseCase = Depends(create_location_use_case),
):
    return await use_case.execute(name)


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    use_case: DeleteLocationUseCase = Depends(delete_location_use_case),
):
    await use_case.execute(location_id)
    return None


@router.get("/locations", response_model=list[Location], status_code=status.HTTP_200_OK)
async def get_all_locations(
    use_case: GetAllLocationsUseCase = Depends(get_all_locations_use_case),
):
    return await use_case.execute()
