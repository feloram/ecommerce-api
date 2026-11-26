from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict

class ProductCreate(BaseModel):

    name:str = Field(min_length=2,max_length=150)

    description:str | None = Field(default=None ,  max_length=1000)

    price:Decimal = Field(gt=0 , max_digits=12 , decimal_places=2 )

    stock:int = Field(ge=0)


class ProductResponse(BaseModel):
    id:int
    name:str
    description: str | None
    price:Decimal
    stock:int
    vendor_id:int
    is_active:bool

    model_config = ConfigDict(from_attributes=True)