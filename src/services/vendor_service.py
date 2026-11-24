
from sqlalchemy.orm import Session

from src.repositories.vendor_repository import (
    get_vendor_by_user_id,
    create_vendor
)


def register_vendor(db: Session, vendor_data, user_id: int):

    existing_vendor = get_vendor_by_user_id(
        db,
        user_id
    )

    if existing_vendor:
        raise ValueError("User already has a vendor")

    vendor = create_vendor(
        db=db,
        name=vendor_data.name,
        description=vendor_data.description,
        user_id=user_id
    )

    return vendor
