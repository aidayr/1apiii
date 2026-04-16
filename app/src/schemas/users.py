from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    SecretStr,
    field_validator,
    model_validator,
)


class RegisterUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: SecretStr

    @model_validator(mode="after")
    def validate_request(self) -> "RegisterUserRequest":
        if not self.username and not self.email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Необходимо ввести либо email, либо username",
            )
        return self

    @field_validator("password")
    @staticmethod
    def check_password(password: SecretStr) -> SecretStr:
        passw = password.get_secret_value()
        if len(passw) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Длина пароля должна быть как минимум 8 символов",
            )
        if not any(c.islower() for c in passw) or not any(c.isupper() for c in passw):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать и строчные, и заглавные буквы",
            )
        return password


class LoginUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str | None = None
    email: EmailStr | None = None
