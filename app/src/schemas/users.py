from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException, status
from datetime import datetime


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @staticmethod
    def check_password(password: str) -> str:
        if (len(password) < 8):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITYT,
                detail="Длина пароля должна быть как минимум 8 символов"
            )
        if not any(c.islower() for c in password) \
                or not any(c.isupper() for c in password):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать и строчные, и заглавные буквы"
            )
        return password


class LoginUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created: datetime
    active: bool

    class Config:
        from_attributes = True
