from typing import List, Dict
from pydantic import SecretStr, EmailStr
from fastapi import status, HTTPException, APIRouter, Body

from ..schemas.users import RegisterUserRequest, LoginUserResponse


router = APIRouter()

users: Dict[int, RegisterUserRequest] = {
    1: RegisterUserRequest(
        email="abc@gmail.com",
        username="popi",
        password=SecretStr("Asdfghj12")
    ),
    2: RegisterUserRequest(
        email="bebeb@gmail.com",
        password=SecretStr("5G123asd")
    )
}

@router.get("/users", status_code=status.HTTP_200_OK, response_model=LoginUserResponse)
async def get_user_by_email(email: EmailStr):
    for uid, user in users.items():
        if user.email == email:
            return LoginUserResponse(
                id=uid,
                username=user.username,
                email=user.email
            )
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Такого пользователя не существует"
    )


@router.get("/users/all", status_code=status.HTTP_200_OK, response_model=List[LoginUserResponse])
async def get_all_users():
    response = []
    for uid, user in users.items():
        response.append(
            LoginUserResponse(
                id=uid,
                username=user.username,
                email=user.email
            )
        )
    return response


@router.delete("/users/{uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    uid: int,
    password: SecretStr):
    if uid not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такого пользователя не существует"
        )
    
    user = users[uid]
    if user.password.get_secret_value() != password.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )
    
    users.pop(uid)
    return