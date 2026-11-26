from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Query

from src.connections.postgresql import get_db
from src.api.dependencies import get_current_user
from src.models.user import User
from src.schemas.product import ProductCreate, ProductResponse
from src.services.product_service import (register_product , list_products , get_product_details)

router = APIRouter(
    tags=["Products"]
)

@router.post(
    "/vendors/{vendor_id}/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(
    vendor_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
        product = register_product(
            db=db,
            product_data=product_data,
            vendor_id=vendor_id,
            user_id=current_user.id
        )

        return product

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):

    return list_products(db, page=page, page_size=page_size)


@router.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db)
):

    try:
        return get_product_details(
            db,
            product_id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
