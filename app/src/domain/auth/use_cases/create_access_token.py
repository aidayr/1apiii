from datetime import UTC, datetime, timedelta

from jose import jwt

from src.services.auth import AUTH_ALGORITHM, SECRET_AUTH_KEY


class CreateAccessTokenUseCase:
    def __init__(self, token_expire_minutes: int = 10) -> None:
        self._ACCESS_TOKEN_EXPIRE_MINUTES = token_expire_minutes

    async def execute(
        self, username: str, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=SECRET_AUTH_KEY.get_secret_value(),
            algorithm=AUTH_ALGORITHM,
        )

        return encoded_jwt
