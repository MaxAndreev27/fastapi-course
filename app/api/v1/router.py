from fastapi import APIRouter

from app.api.v1.endpoints import auth, heroes, root, users

v1_router = APIRouter()

v1_router.include_router(root.router, tags=["System"])
v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication V1"])
v1_router.include_router(users.router, prefix="/users", tags=["Users V1"])
v1_router.include_router(heroes.router, prefix="/heroes", tags=["Heroes V1"])
