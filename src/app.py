from fastapi import FastAPI

from src.connections.postgresql import Base, engine
from src.models.user import User
from src.api.endpoints.v1.auth import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Ecommerce API",
    description="Online Shopping Platform API",
    version="1.0.0"
)


app.include_router(
    auth_router,
    prefix="/api/v1"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Ecommerce API"
    }
