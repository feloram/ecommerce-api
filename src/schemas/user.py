from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
