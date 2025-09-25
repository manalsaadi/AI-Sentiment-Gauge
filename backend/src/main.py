from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from typing import List

# Import existing functionality
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.keyword_extractor import KeywordExtractor
from translation.translator import Translator
from preprocessing.preprocessor import TextPreprocessor
from input.web_scraper import WebScraper
from input.comment_input import CommentInput
from models import TextInput, UrlInput, SentimentResponse, EnhancedSentimentResponse, TranslationResponse, ErrorResponse

# Setup logging
logger = logging.getLogger(__name__)

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
keyword_extractor = KeywordExtractor()
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

@app.post("/analyze/text", response_model=EnhancedSentimentResponse)
async def analyze_text(input_data: TextInput):
    """
    Analyze the sentiment of input text with enhanced AI-powered features.
    Uses automatic model selection for optimal accuracy.
    """
    # Validate input
    if not input_data.text or not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Initialize enhanced sentiment analyzer
        enhanced_analyzer = SentimentAnalyzer()
        
        # Preprocess the text
        cleaned_text = preprocessor.preprocess(input_data.text)

        # Auto-detect source language for smart routing
        source_lang = translator.detect_language(cleaned_text)
        
        # Get enhanced sentiment analysis with automatic model selection
        sentiment_result = enhanced_analyzer.analyze_with_percentages(
            cleaned_text,
            source_language=getattr(source_lang, 'value', str(source_lang)) if hasattr(source_lang, 'value') else str(source_lang)
        )
        
        # Handle translation if requested and needed
        translated_text = None
        if source_lang != input_data.target_language and input_data.target_language == "en":
            try:
                translated_text = translator.translate_to_english(
                    cleaned_text,
                    source_lang=source_lang
                )
            except Exception as e:
                logger.warning(f"Translation failed: {e}")
        
        # Extract keywords using enhanced extractor
        keywords_result = keyword_extractor.extract_keywords_frequency(
            cleaned_text, 
            top_k=10, 
            min_length=3
        )
        keywords = [kw['keyword'] for kw in keywords_result]

        # Enhanced summary with method information
        method_used = sentiment_result.get('method', 'unknown')
        confidence = sentiment_result.get('confidence', 0)
        dominant_sentiment = sentiment_result.get('sentiment', 'neutral')
        
        if confidence > 0.8:
            confidence_level = "very high"
        elif confidence > 0.6:
            confidence_level = "high"
        elif confidence > 0.4:
            confidence_level = "moderate" 
        else:
            confidence_level = "low"
            
        summary = f"AI analysis shows {dominant_sentiment} sentiment with {confidence_level} confidence using {method_used}."
        
        if translated_text:
            summary += f" Original text was in {source_lang}."
        if keywords:
            summary += f" Key topics: {', '.join(keywords[:3])}."

        return EnhancedSentimentResponse(
            text=input_data.text,
            sentiment={
                "positive": sentiment_result.get("positive", 0),
                "negative": sentiment_result.get("negative", 0),
                "neutral": sentiment_result.get("neutral", 0)
            },
            keywords=keywords,
            summary=summary,
            translated_text=translated_text,
            source_language=getattr(source_lang, 'value', str(source_lang)) if hasattr(source_lang, 'value') else str(source_lang),
            confidence=round(confidence * 100, 1),
            metadata={
                "method": method_used,
                "model": sentiment_result.get("model", "unknown"),
                "compound_score": sentiment_result.get("compound_score", 0),
                "text_length": len(cleaned_text),
                "word_count": len(cleaned_text.split())
            }
        )
        
    except Exception as e:
        logger.error(f"Error in enhanced analyze_text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/url")
async def analyze_url(input_data: UrlInput):
    """
    Scrape text content from a URL and analyze its sentiment.
    Returns aggregated sentiment analysis matching frontend expectations.
    """
    try:
        # Scrape text from URL
        texts = web_scraper.scrape(str(input_data.url))
        
        if not texts:
            raise HTTPException(status_code=404, detail="No text content found on the page")
        
        # Analyze all texts and aggregate results
        all_sentiments = []
        all_keywords = []
        
        for text in texts:
            # Preprocess the text
            cleaned_text = preprocessor.preprocess(text)
            
            if len(cleaned_text.strip()) < 10:  # Skip very short texts
                continue
            
            # Detect language
            source_lang = translator.detect_language(cleaned_text)
            
            # Translate if needed
            text_to_analyze = cleaned_text
            if source_lang != input_data.target_language and input_data.target_language == "en":
                try:
                    text_to_analyze = translator.translate_to_english(
                        cleaned_text,
                        source_lang=source_lang
                    )
                except Exception as e:
                    logger.warning(f"Translation failed for text: {e}")
            
            # Get enhanced sentiment analysis
            enhanced_analyzer = SentimentAnalyzer()
            sentiment_result = enhanced_analyzer.analyze_with_percentages(text_to_analyze)
            all_sentiments.append(sentiment_result)
            
            # Extract keywords
            keywords_result = keyword_extractor.extract_keywords_frequency(
                text_to_analyze, 
                top_k=5, 
                min_length=3
            )
            for kw in keywords_result:
                all_keywords.append(kw['keyword'])
        
        if not all_sentiments:
            raise HTTPException(status_code=404, detail="No analyzable content found")
        
        # Aggregate sentiment percentages
        total_positive = sum(s.get('positive', 0) for s in all_sentiments)
        total_neutral = sum(s.get('neutral', 0) for s in all_sentiments)
        total_negative = sum(s.get('negative', 0) for s in all_sentiments)
        
        # Calculate averages
        count = len(all_sentiments)
        avg_positive = round(total_positive / count, 1)
        avg_neutral = round(total_neutral / count, 1)
        avg_negative = round(total_negative / count, 1)
        
        # Get top unique keywords
        unique_keywords = list(dict.fromkeys(all_keywords))[:10]  # Remove duplicates, keep order
        
        # Return format matching frontend expectations
        return {
            "comments_found": len(texts),
            "sentiment": {
                "positive": avg_positive,
                "neutral": avg_neutral,
                "negative": avg_negative
            },
            "keywords": unique_keywords,
            "url": str(input_data.url)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analyze_url: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze URL: {str(e)}")

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