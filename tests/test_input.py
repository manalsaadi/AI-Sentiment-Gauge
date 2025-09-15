"""Tests for the input module."""

import pytest
from pathlib import Path
from src.input.comment_input import CommentInput
from src.input.web_scraper import WebScraper

def test_process_text_input_single_comment():
    """Test processing a single comment."""
    text = "This is a test comment"
    comments = CommentInput.process_text_input(text)
    assert len(comments) == 1
    assert comments[0] == text

def test_process_text_input_multiple_comments():
    """Test processing multiple comments."""
    text = "First comment\nSecond comment\nThird comment"
    comments = CommentInput.process_text_input(text)
    assert len(comments) == 3
    assert comments[0] == "First comment"
    assert comments[1] == "Second comment"
    assert comments[2] == "Third comment"

def test_process_text_input_empty():
    """Test processing empty input."""
    with pytest.raises(ValueError):
        CommentInput.process_text_input("")

def test_process_text_input_whitespace():
    """Test processing whitespace input."""
    with pytest.raises(ValueError):
        CommentInput.process_text_input("   \n   \t   ")

def test_validate_comment():
    """Test comment validation."""
    assert CommentInput.validate_comment("Valid comment")
    assert not CommentInput.validate_comment("")
    assert not CommentInput.validate_comment("   ")

# Web scraper tests would typically use mock responses
def test_web_scraper_invalid_url():
    """Test web scraper with invalid URL."""
    scraper = WebScraper()
    with pytest.raises(ValueError):
        scraper.scrape_comments("not-a-url")