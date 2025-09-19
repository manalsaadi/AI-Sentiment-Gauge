from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class TextInput(BaseModel):
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"

class UrlInput(BaseModel):
    url: HttpUrl
    target_language: str = "en"

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    score: float
    translated_text: Optional[str] = None
    source_language: str
    confidence: float

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

class ErrorResponse(BaseModel):
    detail: str