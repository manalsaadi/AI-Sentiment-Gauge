"""Tests for the analysis modules."""

import pytest
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.keyword_extractor import KeywordExtractor

@pytest.fixture
def sentiment_analyzer():
    """Create a SentimentAnalyzer instance for testing."""
    return SentimentAnalyzer()

@pytest.fixture
def keyword_extractor():
    """Create a KeywordExtractor instance for testing."""
    return KeywordExtractor()

# Sentiment Analysis Tests
def test_sentiment_empty_text(sentiment_analyzer):
    """Test sentiment analysis with empty text."""
    with pytest.raises(ValueError):
        sentiment_analyzer.analyze_sentiment("")

def test_sentiment_positive(sentiment_analyzer):
    """Test sentiment analysis with positive text."""
    text = "This product is excellent! I love it."
    result = sentiment_analyzer.analyze_sentiment(text)
    assert result['sentiment'] == 'positive'
    assert result['compound_score'] > 0

def test_sentiment_negative(sentiment_analyzer):
    """Test sentiment analysis with negative text."""
    text = "This is terrible. I hate it."
    result = sentiment_analyzer.analyze_sentiment(text)
    assert result['sentiment'] == 'negative'
    assert result['compound_score'] < 0

def test_sentiment_neutral(sentiment_analyzer):
    """Test sentiment analysis with neutral text."""
    text = "This is a product."
    result = sentiment_analyzer.analyze_sentiment(text)
    assert result['sentiment'] == 'neutral'

def test_batch_sentiment_analysis(sentiment_analyzer):
    """Test batch sentiment analysis."""
    texts = [
        "This is great!",
        "This is terrible.",
        "This is neutral.",
        ""  # Empty text
    ]
    results = sentiment_analyzer.batch_analyze(texts)
    assert len(results) == len(texts)
    assert results[0]['sentiment'] == 'positive'
    assert results[1]['sentiment'] == 'negative'
    assert results[-1] is None  # Empty text

def test_sentiment_distribution(sentiment_analyzer):
    """Test sentiment distribution calculation."""
    texts = [
        "Excellent product!",
        "Terrible service!",
        "Just okay.",
        "Amazing!",
        "Love it!"
    ]
    distribution = sentiment_analyzer.get_sentiment_distribution(texts)
    assert distribution['total'] == 5
    assert distribution['positive_count'] >= 3  # At least 3 positive
    assert distribution['negative_count'] >= 1  # At least 1 negative

# Keyword Extraction Tests
def test_keywords_empty_text(keyword_extractor):
    """Test keyword extraction with empty text."""
    with pytest.raises(ValueError):
        keyword_extractor.extract_keywords_frequency("")

def test_frequency_based_keywords(keyword_extractor):
    """Test frequency-based keyword extraction."""
    text = "This is a test. This is another test. Test is important."
    keywords = keyword_extractor.extract_keywords_frequency(text, top_k=2)
    assert len(keywords) <= 2
    assert any(kw['keyword'] == 'test' for kw in keywords)

def test_tfidf_keywords(keyword_extractor):
    """Test TF-IDF based keyword extraction."""
    texts = [
        "This is a test document about testing",
        "This document is about something else",
        "Another document with different content"
    ]
    keywords = keyword_extractor.extract_keywords_tfidf(texts)
    assert len(keywords) == len(texts)
    assert all(isinstance(kw_list, list) for kw_list in keywords)

def test_combined_keyword_extraction(keyword_extractor):
    """Test combined keyword extraction."""
    texts = [
        "Python is a great programming language",
        "Python is widely used in data science",
        "Programming in Python is fun"
    ]
    results = keyword_extractor.extract_keywords_combined(texts)
    assert len(results) == len(texts)
    assert all('frequency_based' in r for r in results)
    assert all('tfidf_based' in r for r in results)

def test_common_keywords(keyword_extractor):
    """Test common keyword extraction."""
    texts = [
        "Python programming is great",
        "I love Python programming",
        "Programming in Python is fun"
    ]
    results = keyword_extractor.get_common_keywords(texts)
    assert 'frequency_based' in results
    assert 'tfidf_based' in results
    # Check if 'python' and 'programming' are in top keywords
    freq_keywords = {kw['keyword'] for kw in results['frequency_based']}
    assert any('python' in kw.lower() for kw in freq_keywords)
    assert any('program' in kw.lower() for kw in freq_keywords)