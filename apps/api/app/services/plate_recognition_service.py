import base64
import json

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.plate import (
    ARABIC_TO_ENGLISH,
    ENGLISH_TO_ARABIC,
    Plate,
    PlateAR,
    PlateEN,
    PlateRecognitionResponse,
)

SYSTEM_PROMPT = """You are a Saudi Arabia license plate recognition system.
Analyze the provided image and identify all Saudi license plates visible.

Saudi plates have 3 Arabic letters and up to 4 numbers.

Valid Arabic letters and their English equivalents:
ا=A, ب=B, ح=J, د=D, ر=R, س=S, ص=X, ط=T, ع=E, ق=G, ك=K, ل=L, م=Z, ن=N, هـ=H, و=U, ى=V

Return a JSON object with this exact structure:
{
  "plates": [
    {
      "en": {"characters": ["A", "B", "D"], "numbers": [1, 2, 3, 4]},
      "ar": {"characters": ["ا", "ب", "د"], "numbers": [1, 2, 3, 4]}
    }
  ]
}

Rules:
- characters must be exactly 3 valid letters from the mapping above
- numbers is a list of individual digits (up to 4)
- Both en and ar representations must match (same plate, different scripts)
- If no plates are found, return {"plates": []}
- Only return the JSON object, nothing else"""


async def recognize_plates(image_bytes: bytes, content_type: str) -> PlateRecognitionResponse:
    settings = get_settings()
    client = AsyncOpenAI(
        base_url='https://api.groq.com/openai/v1',
        api_key=settings.GROQ_API_KEY,
    )

    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    data_uri = f'data:{content_type};base64,{encoded_image}'

    response = await client.chat.completions.create(
        model='meta-llama/llama-4-scout-17b-16e-instruct',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': 'Identify all Saudi license plates in this image.',
                    },
                    {
                        'type': 'image_url',
                        'image_url': {'url': data_uri},
                    },
                ],
            },
        ],
        response_format={
            'type': 'json_schema',
            'json_schema': {
                'name': 'plate_recognition_response',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'plates': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'en': {
                                        'type': 'object',
                                        'properties': {
                                            'characters': {
                                                'type': 'array',
                                                'items': {'type': 'string'},
                                            },
                                            'numbers': {
                                                'type': 'array',
                                                'items': {'type': 'integer'},
                                            },
                                        },
                                        'required': ['characters', 'numbers'],
                                        'additionalProperties': False,
                                    },
                                    'ar': {
                                        'type': 'object',
                                        'properties': {
                                            'characters': {
                                                'type': 'array',
                                                'items': {'type': 'string'},
                                            },
                                            'numbers': {
                                                'type': 'array',
                                                'items': {'type': 'integer'},
                                            },
                                        },
                                        'required': ['characters', 'numbers'],
                                        'additionalProperties': False,
                                    },
                                },
                                'required': ['en', 'ar'],
                                'additionalProperties': False,
                            },
                        },
                    },
                    'required': ['plates'],
                    'additionalProperties': False,
                },
                'strict': True,
            },
        },
        temperature=0,
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    plates: list[Plate] = []
    for plate_data in data.get('plates', []):
        en_chars = plate_data.get('en', {}).get('characters', [])
        en_nums = plate_data.get('en', {}).get('numbers', [])
        ar_chars = plate_data.get('ar', {}).get('characters', [])
        ar_nums = plate_data.get('ar', {}).get('numbers', [])

        if en_chars and not ar_chars:
            ar_chars = [ENGLISH_TO_ARABIC.get(c, c) for c in en_chars]
        elif ar_chars and not en_chars:
            en_chars = [ARABIC_TO_ENGLISH.get(c, c) for c in ar_chars]

        numbers = en_nums or ar_nums

        plates.append(
            Plate(
                en=PlateEN(characters=en_chars, numbers=numbers),
                ar=PlateAR(characters=ar_chars, numbers=numbers),
            )
        )

    return PlateRecognitionResponse(plates=plates)
