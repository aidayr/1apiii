from fastapi import HTTPException, status

from ...infrastructure.sqlite.database import database
from ...infrastructure.sqlite.repositories.users import UserRepository
from ...schemas.users import LoginUserResponse, RegisterUserRequest


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, ud: RegisterUserRequest) -> LoginUserResponse:
        with self._database.session() as session:
            if ud.email:
                existed = self._repo.get_by_email(session=session, email=ud.email)
                if existed:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Пользователь с таким email уже существует",
                    )
            if ud.username:
                existed2 = self._repo.get_by_username(
                    session=session, username=ud.username
                )
                if existed2:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Пользователь с таким username уже существует",
                    )
            user = self._repo.create(session=session, user_data=ud)
            response = LoginUserResponse.model_validate(obj=user)
            session.commit()
            session.refresh(user)
        return response
