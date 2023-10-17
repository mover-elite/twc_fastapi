from fastapi import APIRouter
from app.api.view import router as view_router
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.plan import router as plan_router

router = APIRouter()

router.include_router(view_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(plan_router)
