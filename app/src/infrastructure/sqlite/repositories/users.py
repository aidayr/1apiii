import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import UserAlreadyExists, UserNotFound
from src.infrastructure.sqlite.models.usersModel import User
from src.schemas.users import RegisterUserRequest

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self):
        self._model: type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> User:
        user = session.scalar(select(self._model).where(self._model.id == user_id))
        if not user:
            raise UserNotFound()
        return user

    def get_all(self, session: Session) -> list[User]:
        return list(session.scalars(select(self._model)).all())

    def get_by_email(self, session: Session, email: str) -> User | None:
        user = session.query(User).filter(User.username == email).first()
        return user

    def get_by_username(self, session: Session, username: str) -> User | None:
        user = session.query(User).filter(User.username == username).first()
        return user

    def create(self, session: Session, user_data: RegisterUserRequest) -> User:
        try:
            user = self._model(
                username=user_data.username,
                email=user_data.email,
                password=user_data.password.get_secret_value(),
            )
            session.add(user)
            session.flush()
            return user
        except IntegrityError as err:
            raise UserAlreadyExists() from err

    """def update(self, session: Session, user_id, user_data: RegisterUserRequest) -> User:
        user = self.get_by_id(session, user_id)
        if user_data.username and user_data.username != user.username:
            existing = self.get_by_username(session, user_data.username)
            if existing:
                raise UsernameIsOccupied()

        if user_data.email and user_data.email != user.email:
            existing = self.get_by_email(session, user_data.email)
            if existing:
                raise EmailIsOccupied()
        user.username = user_data.username
        user.email = user_data.email
        user.password = user_data.password.get_secret_value()
        session.commit()
        session.refresh(user)

        return user """

    def delete(self, session: Session, user_id: int) -> None:
        try:
            user = self.get_by_id(session, user_id)
            session.delete(user)
            session.commit()
        except IntegrityError as err:
            raise UserNotFound() from err


""" def create(self, session: Session, user_data: RegisterUserRequest) -> User:
        query = (
            insert(self._model).values(user_data.model_dump()).returning(self._model)
        )
        try:
            user = session.scalar(query)
        except IntegrityError as err:
            # e.__cause__
            raise AlreadyExists() from err
        return user
"""
