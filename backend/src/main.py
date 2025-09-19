from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List

# Import existing functionality
from analysis.sentiment_analyzer import SentimentAnalyzer
from translation.translator import Translator
from preprocessing.preprocessor import TextPreprocessor
from input.web_scraper import WebScraper
from input.comment_input import CommentInput
from models import TextInput, UrlInput, SentimentResponse, TranslationResponse, ErrorResponse

app = FastAPI(
    title="AI Sentiment Gauge API",
    description="API for multilingual sentiment analysis and text processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
translator = Translator()
preprocessor = TextPreprocessor()
web_scraper = WebScraper()
comment_input = CommentInput()

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "Welcome to AI Sentiment Gauge API",
        "version": "1.0.0",
        "endpoints": [
            "/analyze/text",
            "/analyze/url",
            "/translate"
        ]
    }

@app.post("/analyze/text", response_model=SentimentResponse)
async def analyze_text(input_data: TextInput):
    """
    Analyze the sentiment of input text.
    If source_language is not provided, it will be auto-detected.
    Text will be translated to target_language before analysis if needed.
    """
    # Validate input
    if not input_data.text or not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Preprocess the text
        cleaned_text = preprocessor.preprocess(input_data.text)

        # Always auto-detect source language
        source_lang = translator.detect_language(cleaned_text)

        # Translate if needed
        translated_text = None
        if source_lang != input_data.target_language:
            translated_text = translator.translate_to_english(
                cleaned_text,
                source_lang=source_lang
            ) if input_data.target_language == "en" else None  # Currently only supporting translation to English
            text_to_analyze = translated_text
        else:
            text_to_analyze = cleaned_text

        # Analyze sentiment
        result = sentiment_analyzer.analyze_sentiment(text_to_analyze)

        return SentimentResponse(
            text=input_data.text,
            sentiment=result['sentiment'],
            score=result['compound_score'],
            translated_text=translated_text,
            source_language=getattr(source_lang, 'value', source_lang),
            confidence=max(result['positive_score'], result['negative_score'], result['neutral_score'])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/url", response_model=List[SentimentResponse])
async def analyze_url(input_data: UrlInput):
    """
    Scrape text content from a URL and analyze its sentiment.
    Returns sentiment analysis for each text block found.
    """
    try:
        # Scrape text from URL
        texts = web_scraper.scrape(str(input_data.url))
        results = []
        
        for text in texts:
            # Preprocess the text
            cleaned_text = preprocessor.preprocess(text)
            
            # Detect language
            source_lang = translator.detect_language(cleaned_text)
            
            # Translate if needed
            translated_text = None
            if source_lang != input_data.target_language:
                translated_text = translator.translate_to_english(
                    cleaned_text,
                    source_lang=source_lang
                ) if input_data.target_language == "en" else None  # Currently only supporting translation to English
                text_to_analyze = translated_text
            else:
                text_to_analyze = cleaned_text
            
            # Analyze sentiment
            result = sentiment_analyzer.analyze_sentiment(text_to_analyze)
            
            results.append(
                SentimentResponse(
                    text=text,
                    sentiment=result['sentiment'],
                    score=result['compound_score'],
                    translated_text=translated_text,
                    source_language=source_lang,
                    confidence=max(result['positive_score'], result['negative_score'], result['neutral_score'])
                )
            )
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(input_data: TextInput):
    """
    Translate text from source language to target language.
    If source_language is not provided, it will be auto-detected.
    """
    # Validate input text
    if not input_data.text or not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    # Validate target language first
    if input_data.target_language != "en":
        raise HTTPException(
            status_code=400,
            detail="Currently only supporting translation to English. Please set target_language to 'en'."
        )

    # Validate source language if provided
    source_lang = None
    if input_data.source_language:
        from translation.translator import Language
        try:
            source_lang = input_data.source_language
            # Check if it's a valid language code
            if source_lang not in [lang.value for lang in Language]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported language: {source_lang}"
                )
            source_lang = Language(source_lang)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {input_data.source_language}"
            )
    else:
        try:
            source_lang = translator.detect_language(input_data.text)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not detect language: {str(e)}"
            )

    # Attempt translation
    try:
        translated_text = translator.translate_to_english(
            input_data.text,
            source_lang=source_lang
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
    
    return TranslationResponse(
        original_text=input_data.text,
        translated_text=translated_text,
        source_language=source_lang.value if hasattr(source_lang, 'value') else source_lang,
        target_language=input_data.target_language
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)