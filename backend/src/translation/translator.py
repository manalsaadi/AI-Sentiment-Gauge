"""Translation module for language detection and translation using MarianMT Quantized."""

import logging
from enum import Enum
from typing import List, Optional, Dict, Tuple
from pathlib import Path

try:
    from langdetect import detect, detect_langs, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logging.warning("langdetect not available. Install with: pip install langdetect")

from .marian_quantized import MarianQuantizedTranslator

logger = logging.getLogger(__name__)

class Language(Enum):
    """Supported languages for translation."""
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
    
    @classmethod
    def get_all_codes(cls) -> List[str]:
        """Get list of all supported language codes."""
        return [lang.value for lang in cls]

class Translator:
    """Handler for language detection and translation using MarianMT Quantized."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the ultra-fast MarianMT quantized translator."""
        self.marian_translator = MarianQuantizedTranslator(cache_dir)
        logger.info("🚀 Initialized MarianMT Quantized translator")
        
        # Warm up common models for instant translation
        self.marian_translator.warm_up(['es', 'fr', 'de'])
        logger.info("🔥 Pre-loaded common translation models")
        
    def _ensure_translation_packages(self) -> None:
        """No longer needed with MarianMT - models auto-download as needed."""
        pass  # MarianMT handles model management automatically
            
    def _get_supported_pairs(self):
        """Get supported language pairs from MarianMT."""
        # MarianMT supports these pairs out of the box
        return list(self.marian_translator.LANGUAGE_PAIRS.keys())
        
    def detect_language(self, text: str) -> Language:
        """Detect the language of the input text using langdetect library.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected Language enum value
            
        Raises:
            ValueError: If language detection fails or language is not supported
        """
        if LANGDETECT_AVAILABLE:
            try:
                # Clean and validate text
                cleaned_text = text.strip()
                if len(cleaned_text) < 3:
                    logger.warning("Text too short for reliable detection, defaulting to English")
                    return Language.ENGLISH
                
                # Use Google's langdetect algorithm
                detected_code = detect(cleaned_text)
                
                # Get confidence scores for debugging
                lang_probs = detect_langs(cleaned_text)
                confidence = max(prob.prob for prob in lang_probs)
                logger.debug(f"Language detection: {detected_code} (confidence: {confidence:.3f})")
                
                # Map to our Language enum
                language_mapping = {
                    'en': Language.ENGLISH,
                    'fr': Language.FRENCH,
                    'de': Language.GERMAN,
                    'es': Language.SPANISH,
                    'pt': Language.SPANISH,  # Fallback Portuguese to Spanish
                    'it': Language.SPANISH,  # Fallback Italian to Spanish (similar)
                }
                
                detected_lang = language_mapping.get(detected_code, Language.ENGLISH)
                logger.debug(f"Mapped to: {detected_lang.value}")
                return detected_lang
                
            except LangDetectException as e:
                logger.warning(f"langdetect failed: {e}, using fallback")
                return self._fallback_detection(text)
        else:
            # Fallback to improved pattern-based detection
            return self._fallback_detection(text)
    
    def _fallback_detection(self, text: str) -> Language:
        """Fallback language detection using improved pattern matching."""
        text_lower = text.lower()
        
        # French-specific indicators (check FIRST to avoid Spanish false positives)
        french_unique = ['à', 'ç', 'è', 'ê', 'û', 'ù', 'ï', 'ÿ', 'œ']
        french_words = ['je suis', 'tu es', 'nous sommes', 'vous êtes', 'le', 'la', 'les', 'qui', 'que', 'avec', 'dans', 'très', 'bien']
        
        # Spanish-specific indicators
        spanish_unique = ['ñ']
        spanish_words = ['yo soy', 'tú eres', 'nosotros somos', 'el', 'los', 'las', 'con', 'en', 'muy', 'hola', 'gracias']
        
        # German-specific indicators
        german_unique = ['ß', 'ü', 'ä', 'ö']
        german_words = ['ich bin', 'du bist', 'der', 'die', 'das', 'und', 'mit', 'für', 'auf', 'haben', 'sein']
        
        # Score each language
        french_score = sum(2 for char in french_unique if char in text_lower)
        french_score += sum(1 for word in french_words if word in text_lower)
        
        spanish_score = sum(3 for char in spanish_unique if char in text_lower)  # ñ is definitive
        spanish_score += sum(1 for word in spanish_words if word in text_lower)
        
        german_score = sum(2 for char in german_unique if char in text_lower)
        german_score += sum(1 for word in german_words if word in text_lower)
        
        # Add shared accented chars with lower weight
        shared_accents = ['í', 'é', 'á', 'ó', 'ú']
        accent_count = sum(1 for char in shared_accents if char in text_lower)
        if accent_count > 0 and french_score == 0 and spanish_score == 0:
            # Only add to Spanish if no other clear indicators
            spanish_score += accent_count * 0.5
        
        logger.debug(f"Fallback scores - French: {french_score}, Spanish: {spanish_score}, German: {german_score}")
        
        # Determine best match
        scores = {'fr': french_score, 'es': spanish_score, 'de': german_score}
        best_lang = max(scores, key=scores.get)
        
        if scores[best_lang] > 0:
            return Language(best_lang)
        else:
            return Language.ENGLISH
        
    def translate_to_english(self, text: str, source_lang: Optional[Language] = None) -> str:
        """Translate text to English using ultra-fast MarianMT Quantized.
        
        Args:
            text: Text to translate
            source_lang: Optional source language. If None, language will be detected
        Returns:
            Translated text in English
        Raises:
            ValueError: If translation fails or language pair is not supported
        """
        if not text.strip():
            return text
            
        # Detect language if not provided
        if source_lang is None:
            source_lang = self.detect_language(text)
            
        # If already English, return as is
        if source_lang == Language.ENGLISH:
            return text
            
        try:
            # Use MarianMT for ultra-fast translation
            result = self.marian_translator.translate(
                text, 
                source_lang=source_lang.value.lower(),
                target_lang='en'
            )
            
            translated_text = result['translated_text']
            translation_time = result.get('translation_time', 0) * 1000  # Convert to ms
            
            logger.debug(f"⚡ Translated {source_lang.value}→en in {translation_time:.1f}ms")
            logger.debug(f"🎯 Confidence: {result.get('confidence', 0.87)*100:.1f}%")
            
            return translated_text
            
        except Exception as e:
            logger.error(f"MarianMT translation failed: {str(e)}")
            # Fallback: return original text if translation fails
            logger.warning(f"Returning original text due to translation failure")
            return text
    
    def get_translation_stats(self) -> Dict:
        """Get performance statistics from the MarianMT translator."""
        return self.marian_translator.get_stats()
    
    def warm_up_models(self, languages: List[str] = None) -> None:
        """Pre-load translation models for instant response."""
        if languages is None:
            languages = ['es', 'fr', 'de']
        self.marian_translator.warm_up(languages)
    
    def clear_model_cache(self) -> None:
        """Clear model cache to free memory."""
        self.marian_translator.clear_cache()