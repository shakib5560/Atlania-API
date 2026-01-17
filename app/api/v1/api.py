from fastapi import APIRouter
from app.api.v1.endpoints import posts, categories, auth, upload, admin, interactions

api_router = APIRouter()
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])

