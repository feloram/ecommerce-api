from sqlalchemy.orm import Session

from src.repositories.product_repository import ( create_product,get_all_products,get_product_by_id )
from src.repositories.vendor_repository import get_vendor_by_user_id

def register_product(db: Session , product_data , vendor_id: int , user_id: int):
     vendor = get_vendor_by_user_id(db , user_id)

     if not vendor or vendor.id != vendor_id:
        raise ValueError("Vendor not found or access denied")

     if not vendor.is_active:
        raise ValueError("Vendor is inactive")

     return create_product(db=db , product_data=product_data , vendor_id=vendor_id)

def list_products(db: Session):

    return get_all_products(db)


def get_product_details(db: Session, product_id: int):

    product = get_product_by_id(db , product_id)

    if not product:
        raise ValueError("Product not found")

    return product

