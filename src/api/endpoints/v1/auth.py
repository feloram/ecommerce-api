
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.connections.postgresql import get_db
from src.schemas.user import UserRegister, UserResponse
from src.services.user_service import register_user
from src.schemas.auth import UserLogin, TokenResponse
from src.services.auth_service import login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, user_data)
        return user

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
    
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        access_token = login_user(db, user_data)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
