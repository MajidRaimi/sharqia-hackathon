from fastapi import APIRouter

from app.api.v1.endpoints.plate_recognition import router as plate_recognition_router

api_router = APIRouter()
api_router.include_router(
    plate_recognition_router,
    prefix='/plate-recognition',
    tags=['Plate Recognition'],
)
