"""Tests for the preprocessing module."""

import pytest
from src.preprocessing.preprocessor import TextPreprocessor

@pytest.fixture
def preprocessor():
    """Create a TextPreprocessor instance for testing."""
    return TextPreprocessor()

def test_empty_text(preprocessor):
    """Test preprocessing empty text."""
    assert preprocessor.preprocess("") == ""
    assert preprocessor.preprocess("   ") == ""

def test_url_removal(preprocessor):
    """Test URL removal."""
    text = "Check out https://example.com and http://test.com/page"
    processed = preprocessor.preprocess(text)
    assert "http" not in processed
    assert "example.com" not in processed
    assert "test.com" not in processed

def test_mention_removal(preprocessor):
    """Test @mention removal."""
    text = "Hello @user1 and @user2!"
    processed = preprocessor.preprocess(text)
    assert "@user1" not in processed
    assert "@user2" not in processed
    assert "Hello" in processed

def test_hashtag_processing(preprocessor):
    """Test hashtag processing."""
    text = "Great #product with #amazing features"
    # Test with hashtag removal
    processed = preprocessor.preprocess(text, remove_hashtags=True)
    assert "#product" not in processed
    assert "product" in processed
    assert "#amazing" not in processed
    assert "amazing" in processed

def test_email_removal(preprocessor):
    """Test email address removal."""
    text = "Contact us at test@example.com or support@test.com"
    processed = preprocessor.preprocess(text)
    assert "test@example.com" not in processed
    assert "support@test.com" not in processed
    assert "Contact" in processed

def test_emoji_conversion(preprocessor):
    """Test emoji conversion."""
    text = "I love this product! 😊 It's amazing! 👍"
    processed = preprocessor.preprocess(text)
    assert "😊" not in processed
    assert "👍" not in processed
    assert "love" in processed
    assert "amazing" in processed

def test_stopword_removal(preprocessor):
    """Test stop word removal."""
    text = "This is a great product"
    processed = preprocessor.preprocess(text, remove_stopwords=True)
    assert "is" not in processed.split()
    assert "a" not in processed.split()
    assert "great" in processed
    assert "product" in processed

def test_punctuation_removal(preprocessor):
    """Test punctuation removal."""
    text = "Hello, world! How are you?"
    processed = preprocessor.preprocess(text)
    assert "," not in processed
    assert "!" not in processed
    assert "?" not in processed
    assert "Hello" in processed
    assert "world" in processed

def test_lemmatization(preprocessor):
    """Test word lemmatization."""
    text = "I am running and jumping"
    processed = preprocessor.preprocess(text, remove_stopwords=False)
    assert "running" not in processed
    assert "jumping" not in processed
    assert "run" in processed
    assert "jump" in processed

def test_contraction_expansion(preprocessor):
    """Test contraction expansion."""
    text = "I'm can't wouldn't"
    processed = preprocessor.preprocess(text, remove_stopwords=False)
    assert "I'm" not in processed
    assert "can't" not in processed
    assert "wouldn't" not in processed
    assert "am" in processed
    assert "cannot" in processed
    assert "would not" in processed

def test_batch_processing(preprocessor):
    """Test batch text preprocessing."""
    texts = [
        "Hello, world!",
        "Check https://example.com",
        "Contact @user",
        ""  # Empty text
    ]
    processed = preprocessor.batch_preprocess(texts)
    assert len(processed) == len(texts)
    assert all(isinstance(text, str) for text in processed)
    assert "https://example.com" not in processed[1]
    assert "@user" not in processed[2]

def test_batch_processing_empty_list(preprocessor):
    """Test batch processing with empty list."""
    with pytest.raises(ValueError):
        preprocessor.batch_preprocess([])