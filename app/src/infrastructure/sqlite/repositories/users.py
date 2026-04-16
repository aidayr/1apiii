from sqlalchemy.orm import Session

from src.infrastructure.sqlite.models.usersModel import User
from src.schemas.users import RegisterUserRequest


class UserRepository:
    def __init__(self):
        self._model: type[User] = User

    def get_by_id(self, session: Session, user_id: int) -> User | None:
        query = session.query(self._model).where(self._model.id == user_id)

        return query.scalar()

    def get_all(self, session: Session) -> list[User]:
        return session.query(User).all()

    def get_by_email(self, session: Session, email: str) -> User | None:
        query = session.query(self._model).where(self._model.email == email)
        return query.scalar()

    def get_by_username(self, session: Session, username: str) -> User | None:
        query = session.query(self._model).where(self._model.username == username)
        return query.scalar()

    def create(self, session: Session, user_data: RegisterUserRequest) -> User:
        user = self._model(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password.get_secret_value(),
        )
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user_id, user_data: RegisterUserRequest) -> User:
        user = self.get_by_id(session, user_id)
        if user:
            user.username = user_data.username
            user.email = user_data.email
            user.password = user_data.password.get_secret_value()
            session.flush()
            session.refresh(user)

        return user

    def delete(self, session: Session, user: User) -> None:
        session.delete(user)
        session.flush()
