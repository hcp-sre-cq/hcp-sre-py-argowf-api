from fastapi.routing import APIRouter
from typing import Optional
from app.core.config import settings

router = APIRouter()

@router.get("/")
def read_root():
    return {"app_env": settings.APP_ENV, "project_name": settings.PROJECT_NAME}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
