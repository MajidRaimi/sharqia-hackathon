from fastapi import APIRouter, UploadFile

from app.schemas.plate import PlateRecognitionResponse
from app.services.plate_recognition_service import recognize_plates

router = APIRouter()


@router.post('/recognize', response_model=PlateRecognitionResponse)
async def recognize_plate(file: UploadFile):
    image_bytes = await file.read()
    return await recognize_plates(image_bytes, file.content_type)
