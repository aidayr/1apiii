from app.src.domain.locations.use_cases.create_location import CreateLocationUseCase
from app.src.domain.locations.use_cases.delete_location import DeleteLocationUseCase
from app.src.domain.locations.use_cases.get_all_locations import GetAllLocationsUseCase
from app.src.domain.locations.use_cases.get_location_by_id import GetLocationByIdUseCase
from app.src.domain.users.use_cases.create_user import CreateUserUseCase
from app.src.domain.users.use_cases.delete_user import DeleteUserUseCase
from app.src.domain.users.use_cases.get_all_users import GetAllUsersUseCase
from app.src.domain.users.use_cases.get_user_by_id import GetUserByIdUseCase


async def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


async def get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()


async def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


async def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()


async def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


async def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


async def get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()


async def get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()
