"""Shared test fixtures and configuration."""

import pytest
from pathlib import Path
import nltk

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