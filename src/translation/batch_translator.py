"""Batch processing module for translating multiple comments."""

import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .translator import Translator, Language

logger = logging.getLogger(__name__)

class BatchTranslator:
    """Handler for batch translation of comments."""
    
    def __init__(self, max_workers: int = 4):
        """Initialize the batch translator.
        
        Args:
            max_workers: Maximum number of parallel translation workers
        """
        self.translator = Translator()
        self.max_workers = max_workers
        
    def process_comments(
        self,
        comments: List[str],
        detect_languages: bool = True
    ) -> Dict[str, List[str]]:
        """Process and translate a batch of comments.
        
        Args:
            comments: List of comments to translate
            detect_languages: Whether to detect languages (True) or assume all need translation
            
        Returns:
            Dictionary with 'original' and 'translated' comment lists
            
        Raises:
            ValueError: If comments list is empty
        """
        if not comments:
            raise ValueError("Comments list cannot be empty")
            
        logger.info(f"Processing batch of {len(comments)} comments")
        results = {
            'original': comments,
            'translated': [],
            'languages': []
        }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # First detect languages if needed
            if detect_languages:
                future_to_comment = {
                    executor.submit(self.translator.detect_language, comment): comment
                    for comment in comments
                }
                
                detected_langs = []
                for future in as_completed(future_to_comment):
                    comment = future_to_comment[future]
                    try:
                        lang = future.result()
                        detected_langs.append(lang)
                    except Exception as e:
                        logger.error(f"Language detection failed for comment: {str(e)}")
                        # Default to English if detection fails
                        detected_langs.append(Language.ENGLISH)
                        
                results['languages'] = [lang.value for lang in detected_langs]
                
                # Now translate non-English comments
                future_to_comment = {
                    executor.submit(
                        self.translator.translate_to_english,
                        comment,
                        lang
                    ): comment
                    for comment, lang in zip(comments, detected_langs)
                }
                
            else:
                # Translate all comments without detection
                future_to_comment = {
                    executor.submit(
                        self.translator.translate_to_english,
                        comment
                    ): comment
                    for comment in comments
                }
                
            # Collect translations
            translations = []
            for future in as_completed(future_to_comment):
                comment = future_to_comment[future]
                try:
                    translated = future.result()
                    translations.append(translated)
                except Exception as e:
                    logger.error(f"Translation failed for comment: {str(e)}")
                    # Keep original if translation fails
                    translations.append(comment)
                    
            results['translated'] = translations
            
        logger.info("Batch processing completed")
        return results