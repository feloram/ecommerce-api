from sqlalchemy.orm import Session

from src.models.product import Product
from src.models.vendor import Vendor

def create_product(db:Session , product_data , vendor_id:int):

    product=Product(
    name= product_data.name,
    description= product_data.description,
    price= product_data.price,
    stock= product_data.stock,
    vendor_id=vendor_id,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def  get_all_products(db: Session, page: int = 1, page_size: int = 20):
    return(
        db.query(Product).join(Vendor,Product.vendor_id == Vendor.id)
        # .filter(Vendor.is_active == True , Product.is_active == True).all()
        .filter(Vendor.is_active == True , Product.is_active == True)
        .order_by(Product.id).offset((page - 1) * page_size).limit(page_size).all()
    )

def get_product_by_id(db: Session , Product_id:int):
    return(
        db.query(Product).join(Vendor , Product.vendor_id == Vendor.id)
        .filter(Product.id == Product_id , Vendor.is_active == True , Product.is_active == True).first()
    )

    