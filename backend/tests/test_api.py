"""Unit tests for the FastAPI endpoints."""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from typing import Generator

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the Language enum before we patch anything
from translation.translator import Language

# Patch the component initialization before importing app
patches = [
    patch('translation.translator.Translator._ensure_translation_packages'),
    patch('translation.translator.Translator._get_supported_pairs', return_value={}),
    patch('preprocessing.preprocessor.TextPreprocessor._ensure_nltk_resources'),
    patch('analysis.sentiment_analyzer.SentimentAnalyzer._ensure_nltk_resources'),
]

# Apply all patches
for p in patches:
    p.start()

# Now import the app
from main import app

# Create test client
client = TestClient(app)

# Stop all patches when the module is unloaded
for p in patches:
    p.stop()

# Mock responses
MOCK_SENTIMENT_RESPONSE = {
    'sentiment': 'positive',
    'compound_score': 0.8,
    'positive_score': 0.8,
    'negative_score': 0.0,
    'neutral_score': 0.2
}

MOCK_TRANSLATION = "Hello world"

# Test data
TEST_CASES = [
    {
        'text': 'Bonjour le monde',
        'source_language': 'fr',
        'target_language': 'en',
        'expected_translation': 'Hello world'
    },
    {
        'text': 'This is great!',
        'source_language': 'en',
        'target_language': 'en',
        'expected_sentiment': 'positive'
    }
]

@pytest.fixture
def mock_dependencies():
    """Create mock objects for all dependencies."""
    patches = [
        # Mock the class methods to prevent initialization issues
        patch('translation.translator.Translator._ensure_translation_packages'),
        patch('translation.translator.Translator._get_supported_pairs', return_value={}),
        patch('preprocessing.preprocessor.TextPreprocessor._ensure_nltk_resources'),
        patch('analysis.sentiment_analyzer.SentimentAnalyzer._ensure_nltk_resources'),
        
        # Mock the actual component instances
        patch('main.sentiment_analyzer', **{
            'analyze_sentiment.return_value': MOCK_SENTIMENT_RESPONSE
        }),
        patch('main.translator', **{
            'detect_language.return_value': Language.FRENCH,
            'translate_to_english.return_value': MOCK_TRANSLATION,
            'Language': Language,  # Ensure proper enum handling
        }),
        patch('main.preprocessor', **{
            'preprocess.side_effect': lambda text: text if text.strip() else ValueError("Empty text")
        }),
        patch('main.web_scraper', **{
            'scrape.return_value': ["Sample text 1", "Sample text 2"]
        })
    ]
    
    # Start all patches
    mocks = [p.start() for p in patches]
    
    yield {
        'sentiment': mocks[4],  # sentiment_analyzer mock
        'translator': mocks[5],  # translator mock
        'preprocessor': mocks[6],  # preprocessor mock
        'scraper': mocks[7]  # web_scraper mock
    }
    
    # Stop all patches
    for p in patches:
        p.stop()

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to AI Sentiment Gauge API"
    assert "version" in data
    assert "endpoints" in data
    assert len(data["endpoints"]) == 3

def test_analyze_text_english(mock_dependencies):
    """Test sentiment analysis for English text."""
    input_data = {
        "text": "This is great!",
        "source_language": "en",
        "target_language": "en"
    }
    
    response = client.post("/analyze/text", json=input_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["text"] == input_data["text"]
    assert data["sentiment"] == MOCK_SENTIMENT_RESPONSE["sentiment"]
    assert data["score"] == MOCK_SENTIMENT_RESPONSE["compound_score"]
    assert data["source_language"] == "en"
    assert data["translated_text"] is None

def test_analyze_text_french(mock_dependencies):
    """Test sentiment analysis with translation from French."""
    input_data = {
        "text": "Bonjour le monde",
        "source_language": "fr",
        "target_language": "en"
    }
    
    response = client.post("/analyze/text", json=input_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["text"] == input_data["text"]
    assert data["sentiment"] == MOCK_SENTIMENT_RESPONSE["sentiment"]
    assert data["translated_text"] == MOCK_TRANSLATION
    assert data["source_language"] == "fr"

def test_analyze_text_auto_detect(mock_dependencies):
    """Test sentiment analysis with language auto-detection."""
    input_data = {
        "text": "Some text",
        "target_language": "en"
    }
    
    response = client.post("/analyze/text", json=input_data)
    assert response.status_code == 200
    data = response.json()
    
    assert mock_dependencies['translator'].detect_language.called
    assert data["source_language"] == "fr"  # Based on our mock

def test_analyze_url(mock_dependencies):
    """Test URL content analysis."""
    input_data = {
        "url": "https://example.com",
        "target_language": "en"
    }
    
    response = client.post("/analyze/url", json=input_data)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2  # Two sample texts from mock
    for result in data:
        assert "sentiment" in result
        assert "score" in result
        assert "confidence" in result

def test_translate(mock_dependencies):
    """Test text translation."""
    input_data = {
        "text": "Bonjour le monde",
        "source_language": "fr",
        "target_language": "en"
    }
    
    response = client.post("/translate", json=input_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["original_text"] == input_data["text"]
    assert data["translated_text"] == MOCK_TRANSLATION
    assert data["source_language"] == "fr"
    assert data["target_language"] == "en"

@pytest.mark.parametrize("invalid_lang", ["invalid", "xx", "zz"])
def test_translate_unsupported_language(invalid_lang, mock_dependencies):
    """Test translation with unsupported language."""
    input_data = {
        "text": "Text",
        "source_language": invalid_lang,
        "target_language": "en"
    }
    
    response = client.post("/translate", json=input_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert f"Unsupported language: {invalid_lang}" in data["detail"]

def test_translate_target_not_english(mock_dependencies):
    """Test translation with non-English target language."""
    input_data = {
        "text": "Hello",
        "source_language": Language.ENGLISH.value,  # Use enum value
        "target_language": Language.FRENCH.value  # Use enum value
    }
    
    response = client.post("/translate", json=input_data)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Currently only supporting translation to English" in data["detail"]

# Error cases
def test_analyze_text_empty():
    """Test sentiment analysis with empty text."""
    input_data = {
        "text": "",
        "source_language": "en",
        "target_language": "en"
    }
    
    response = client.post("/analyze/text", json=input_data)
    assert response.status_code == 400  # Bad Request for empty text
    data = response.json()
    assert "detail" in data
    assert "Text cannot be empty" in data["detail"]

def test_analyze_url_invalid():
    """Test URL analysis with invalid URL."""
    input_data = {
        "url": "not_a_url",
        "target_language": "en"
    }
    
    response = client.post("/analyze/url", json=input_data)
    assert response.status_code == 422  # FastAPI validation error