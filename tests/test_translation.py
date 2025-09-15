"""Tests for the translation module."""

import pytest
from src.translation.translator import Translator, Language
from src.translation.batch_translator import BatchTranslator

def test_language_detection():
    """Test language detection for supported languages."""
    translator = Translator()
    
    # Test English
    assert translator.detect_language("Hello, how are you?") == Language.ENGLISH
    
    # Test French
    assert translator.detect_language("Bonjour, comment allez-vous?") == Language.FRENCH
    
    # Test German
    assert translator.detect_language("Guten Tag, wie geht es Ihnen?") == Language.GERMAN
    
    # Test Spanish
    assert translator.detect_language("¡Hola! ¿Cómo estás?") == Language.SPANISH

def test_translation_to_english():
    """Test translation to English from supported languages."""
    translator = Translator()
    
    # Test French to English
    french_text = "Bonjour le monde"
    english = translator.translate_to_english(french_text, Language.FRENCH)
    assert english.lower() != french_text.lower()
    assert "hello" in english.lower() or "world" in english.lower()
    
    # Test German to English
    german_text = "Guten Morgen"
    english = translator.translate_to_english(german_text, Language.GERMAN)
    assert english.lower() != german_text.lower()
    assert "good" in english.lower() or "morning" in english.lower()
    
    # Test Spanish to English
    spanish_text = "Buenos días"
    english = translator.translate_to_english(spanish_text, Language.SPANISH)
    assert english.lower() != spanish_text.lower()
    assert "good" in english.lower() or "morning" in english.lower()

def test_empty_text_translation():
    """Test translation of empty text."""
    translator = Translator()
    assert translator.translate_to_english("") == ""
    assert translator.translate_to_english("   ") == "   "

def test_batch_translation():
    """Test batch translation of multiple comments."""
    batch_translator = BatchTranslator()
    comments = [
        "Hello world",  # English
        "Bonjour le monde",  # French
        "Hallo Welt",  # German
        "¡Hola mundo!"  # Spanish
    ]
    
    results = batch_translator.process_comments(comments)
    
    assert len(results['original']) == len(comments)
    assert len(results['translated']) == len(comments)
    assert len(results['languages']) == len(comments)
    
    # Check that English text remains unchanged
    assert results['translated'][0] == comments[0]
    
    # Check that non-English text is translated
    for i in range(1, len(comments)):
        assert results['translated'][i] != comments[i]
        assert results['translated'][i].strip()  # Not empty

def test_batch_translation_empty_list():
    """Test batch translation with empty input."""
    batch_translator = BatchTranslator()
    with pytest.raises(ValueError):
        batch_translator.process_comments([])

def test_batch_translation_single_comment():
    """Test batch translation with a single comment."""
    batch_translator = BatchTranslator()
    comment = "Bonjour!"
    results = batch_translator.process_comments([comment])
    assert len(results['translated']) == 1
    assert results['translated'][0] != comment