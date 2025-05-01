from fastapi import APIRouter

router = APIRouter()

router.include_router(
    # {{app_name}}_router, tags=["{{app_name}}"], prefix="/{{lover_app_name}}"
)
