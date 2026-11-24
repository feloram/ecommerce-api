from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.repositories.user_repository import get_user_by_email
from src.utils.security import create_access_token


password_hash = PasswordHash.recommended()


def login_user(db: Session, user_data):

    user = get_user_by_email(
        db,
        user_data.email
    )

    if not user:
        raise ValueError("Invalid email or password")

    is_password_correct = password_hash.verify(
        user_data.password,
        user.hashed_password
    )

    if not is_password_correct:
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    access_token = create_access_token(user.id)

    return access_token