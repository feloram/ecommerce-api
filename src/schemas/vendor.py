
from pydantic import BaseModel, Field, ConfigDict


class VendorCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class VendorResponse(BaseModel):
    id: int
    name: str
    description: str | None
    user_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
