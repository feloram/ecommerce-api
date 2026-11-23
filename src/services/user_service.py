
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from src.repositories.user_repository import (
    get_user_by_email,
    create_user
)


password_hash = PasswordHash.recommended()


def register_user(db: Session, user_data):
    existing_user = get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = password_hash.hash(
        user_data.password
    )

    new_user = create_user(
        db=db,
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return new_user
