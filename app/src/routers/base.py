from typing import List, Dict
from pydantic import SecretStr, EmailStr
from fastapi import status, HTTPException, APIRouter

from ..schemas.users import RegisterUserRequest, LoginUserResponse


router = APIRouter()

users: Dict[int, RegisterUserRequest] = {
    1: RegisterUserRequest(
        email="abc@gmail.com",
        username="appok",
        password=SecretStr("Asdfghj12")
    ),
    2: RegisterUserRequest(
        email="bebeb@gmail.com",
        password=SecretStr("5G123asd")
    )
}

nid = 3

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

@router.post("/users", status_code=status.HTTP_201_CREATED,
             response_model=LoginUserResponse)
async def create_user(user_data: RegisterUserRequest):
    global nid
    
    emails = {user.email for user in users.values() if user.email}
    usernames = {user.username for user in users.values() if user.username}
    
    if user_data.email and user_data.email in emails:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email уже существует"
                            )
    
    if user_data.username and user_data.username in usernames:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким username уже существует"
                            )
    users[nid] = user_data
    nid += 1
    
    return LoginUserResponse(
        id=(nid - 1),
        username=user_data.username,
        email=user_data.email
    )
       