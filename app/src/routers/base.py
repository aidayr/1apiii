from fastapi import status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..schemas.users import LoginUserRequest, LoginUserResponse


router = APIRouter(prefix='/users')


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[LoginUserResponse])
async def get_user_by_email(
    email: EmailStr,
    use_case: 
)