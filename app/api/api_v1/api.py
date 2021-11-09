from fastapi import APIRouter

from app.api.api_v1.endpoints import argowf, test

api_router = APIRouter()
api_router.include_router(argowf.router, tags=["argowf"])
api_router.include_router(test.router, tags=["test"])
