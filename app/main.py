from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import urllib3
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.log import logger

urllib3.disable_warnings()

app = FastAPI(
    title = settings.PROJECT_NAME
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.API_V1_STR)
