import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import UserAlreadyExists, UserNotFound
from src.infrastructure.sqlite.models.usersModel import User
from src.schemas.users import RegisterUserRequest

logger = logging.getLogger(__name__)

from src.core.utils.db_error import parse_integrity_error


class UserRepository:
    def __init__(self):
        self._model: type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> User:
        user = session.scalar(select(self._model).where(self._model.id == user_id))
        if not user:
            raise UserNotFound()
        return user

    def get_by_username(self, session: Session, username: str) -> User | None:
        return (
            session.query(self._model).filter(self._model.username == username).first()
        )

    def get_all(self, session: Session) -> list[User]:
        return list(session.scalars(select(self._model)).all())

    def create(self, session: Session, user_data: RegisterUserRequest) -> User:
        try:
            user = self._model(
                username=user_data.username,
                password=user_data.password,
            )
            session.add(user)
            session.flush()
            return user
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "username":
                raise UserAlreadyExists() from err

    def update(
        self, session: Session, user_id: int, user_data: RegisterUserRequest
    ) -> User:
        user = self.get_by_id(session, user_id)
        if user_data.username and user_data.username != user.username:
            existing = self.get_by_username(session, user_data.username)
            if existing:
                raise UserAlreadyExists()
            user.username = user_data.username
        if user_data.password:
            user.password = user_data.password
        session.commit()
        session.refresh(user)
        return user

    def delete(self, session: Session, user_id: int) -> None:
        user = self.get_by_id(session, user_id)
        session.delete(user)
        session.commit()
