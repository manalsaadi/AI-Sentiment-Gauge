"""Translation module for language detection and translation using Argos Translate."""

import logging
from enum import Enum
from typing import List, Optional, Dict, Tuple


import argostranslate.package
import argostranslate.translate

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
    """Handler for language detection and translation."""
    
    def __init__(self):
        """Initialize the translator and ensure required packages are installed."""
        self._ensure_translation_packages()
        self.supported_pairs = self._get_supported_pairs()
        logger.info(f"Initialized translator with {len(self.supported_pairs)} language pairs")
        
    def _ensure_translation_packages(self) -> None:
        """Check and install required Argos Translate language packages."""
        try:
            import argostranslate.settings
            import argostranslate.package
            
            # Download and install package index
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            
            # Install required language pairs
            required_pairs = [("fr", "en"), ("de", "en"), ("es", "en")]
            for from_code, to_code in required_pairs:
                # Find package for this language pair
                package = next(
                    (pkg for pkg in available_packages 
                     if pkg.from_code == from_code and pkg.to_code == to_code),
                    None
                )
                
                if package:
                    logger.info(f"Installing translation package for {from_code}->{to_code}")
                    argostranslate.package.install_from_path(package.download())
                else:
                    logger.error(f"Could not find translation package for {from_code}->{to_code}")
                    
        except Exception as e:
            logger.error(f"Error installing translation packages: {str(e)}")
            raise ValueError(
                "Failed to install translation packages. Please ensure you have internet "
                "connection and try again. Error: " + str(e)
            )
            
    def _get_supported_pairs(self):
        """Get dictionary of supported translation language pairs."""
        pairs = {}
        installed_languages = argostranslate.translate.get_installed_languages()

        # Create mapping from language codes to argostranslate Language objects
        lang_map = {lang.code: lang for lang in installed_languages}

        # Build pairs using Argos Translate API; avoid relying on private attrs
        for from_code, from_lang_obj in lang_map.items():
            if from_code not in Language.get_all_codes():
                continue
            for to_code, to_lang_obj in lang_map.items():
                if to_code not in Language.get_all_codes():
                    continue
                try:
                    translation = from_lang_obj.get_translation(to_lang_obj)
                    # If no translation exists, Argos may raise; guard by checking attribute
                    if translation:
                        pairs[(from_code, to_code)] = translation
                except Exception:
                    # No available translation for this pair; skip
                    continue
        return pairs
        
    def detect_language(self, text: str) -> Language:
        """Detect the language of the input text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Detected Language enum value
            
        Raises:
            ValueError: If language detection fails or language is not supported
        """
        # Note: For V1, using a simple character frequency approach
        # TODO: Implement more sophisticated language detection in V2
        
        # Common character patterns for each language
        patterns = {
            Language.FRENCH: ['é', 'è', 'ê', 'ç', 'à', 'ù'],
            Language.GERMAN: ['ä', 'ö', 'ü', 'ß'],
            Language.SPANISH: ['ñ', 'á', 'é', 'í', 'ó', 'ú', '¿', '¡'],
            Language.ENGLISH: []  # Default if no special characters found
        }
        
        text_lower = text.lower()
        scores = {lang: 0 for lang in Language}
        
        # Score based on character patterns
        for lang, chars in patterns.items():
            for char in chars:
                if char in text_lower:
                    scores[lang] += text_lower.count(char)
                    
        # If no special characters found, attempt to detect based on common words
        if all(score == 0 for score in scores.values()):
            common_words = {
                Language.FRENCH: ['le', 'la', 'les', 'et', 'je', 'tu', 'il', 'nous'],
                Language.GERMAN: ['der', 'die', 'das', 'und', 'ich', 'sie', 'ist'],
                Language.SPANISH: ['el', 'la', 'los', 'las', 'y', 'yo', 'tu', 'es'],
                Language.ENGLISH: ['the', 'and', 'is', 'in', 'to', 'it', 'of']
            }
            
            words = text_lower.split()
            for lang, word_list in common_words.items():
                scores[lang] = sum(1 for word in words if word in word_list)
                
        # Get language with highest score
        detected_lang = max(scores.items(), key=lambda x: x[1])[0]
        logger.debug(f"Detected language: {detected_lang.value}")
        return detected_lang
        
    def translate_to_english(self, text: str, source_lang: Optional[Language] = None) -> str:
        """Translate text to English.
        
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
        # Get translation pair
        pair = (source_lang.value, Language.ENGLISH.value)
        if pair not in self.supported_pairs:
            raise ValueError(f"Translation not supported for language pair: {pair}")
        try:
            translation = self.supported_pairs[pair]
            translated = translation.translate(text)
            logger.debug(f"Translated text from {source_lang.value} to English")
            return translated
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise