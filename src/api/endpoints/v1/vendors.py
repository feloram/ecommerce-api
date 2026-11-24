
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.connections.postgresql import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.schemas.vendor import VendorCreate, VendorResponse
from src.services.vendor_service import register_vendor


router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)


@router.post(
    "",
    response_model=VendorResponse,
    status_code=status.HTTP_201_CREATED
)
def create_vendor_endpoint(
    vendor_data: VendorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        vendor = register_vendor(
            db=db,
            vendor_data=vendor_data,
            user_id=current_user.id
        )

        return vendor

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        )
