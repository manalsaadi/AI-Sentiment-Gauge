"""Shared test fixtures and configuration."""

import os
import sys
from pathlib import Path
import pytest
import nltk
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add src directory to Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

# Mock initialization functions before importing app
with patch('translation.translator.Translator._ensure_translation_packages'), \
     patch('translation.translator.Translator._get_supported_pairs', return_value={}), \
     patch('preprocessing.preprocessor.TextPreprocessor._ensure_nltk_resources'), \
     patch('analysis.sentiment_analyzer.SentimentAnalyzer._ensure_nltk_resources'):
    from main import app

def pytest_configure(config):
    """Configure pytest environment."""
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('vader_lexicon')

@pytest.fixture
def sample_texts():
    """Provide sample texts for testing."""
    return {
        'positive': [
            "This is excellent! Really amazing work.",
            "Great product, highly recommend it!",
            "Absolutely love this, best purchase ever."
        ],
        'negative': [
            "This is terrible. Very disappointed.",
            "Worst experience ever, do not buy.",
            "Complete waste of money, awful service."
        ],
        'neutral': [
            "This is a product.",
            "The item arrived yesterday.",
            "It comes in different colors."
        ]
    }

@pytest.fixture
def temp_report_dir(tmp_path):
    """Create a temporary directory for report files."""
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    return report_dir

@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def no_http_requests(monkeypatch):
    """Prevent actual HTTP requests during tests."""
    def urlopen_mock(self, method, url, *args, **kwargs):
        raise RuntimeError(
            f"The test tried to make an HTTP {method} request to {url}"
        )
    monkeypatch.setattr("urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock)