
from sqlalchemy.orm import Session

from src.models.vendor import Vendor


def get_vendor_by_user_id(db: Session, user_id: int):

    return db.query(Vendor).filter(
        Vendor.user_id == user_id
    ).first()


def create_vendor(
    db: Session,
    name: str,
    description: str | None,
    user_id: int
):

    vendor = Vendor(
        name=name,
        description=description,
        user_id=user_id
    )

    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    return vendor
