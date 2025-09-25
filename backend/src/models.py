from typing import List, Optional, Dict, Any
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

class EnhancedSentimentResponse(BaseModel):
    """Enhanced sentiment response with percentage breakdown and keywords"""
    text: str
    sentiment: Dict[str, float]  # {positive: 65.0, neutral: 25.0, negative: 10.0}
    keywords: List[str]
    summary: str
    translated_text: Optional[str] = None
    source_language: str
    confidence: float
    metadata: Optional[Dict[str, Any]] = None

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

class ErrorResponse(BaseModel):
    detail: str