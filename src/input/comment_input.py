"""Module for handling text input from various sources."""

import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

class CommentInput:
    """Handler for processing text input from various sources."""
    
    @staticmethod
    def process_text_input(text: str) -> List[str]:
        """Process raw text input containing one or more comments.
        
        Args:
            text: Raw text input that may contain multiple comments
            
        Returns:
            List of individual comments
            
        Raises:
            ValueError: If the input text is empty
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        # Split text into individual comments
        # Assume comments are separated by newlines
        comments = [
            comment.strip()
            for comment in text.split('\n')
            if comment.strip()
        ]
        
        logger.info(f"Processed {len(comments)} comments from text input")
        return comments
    
    @staticmethod
    def process_file_input(file_path: Path) -> List[str]:
        """Process input from a text file containing comments.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            List of individual comments
            
        Raises:
            FileNotFoundError: If the input file doesn't exist
            ValueError: If the file is empty
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
            
        if not text:
            raise ValueError(f"Input file is empty: {file_path}")
            
        return CommentInput.process_text_input(text)
    
    @staticmethod
    def validate_comment(comment: str) -> bool:
        """Validate a single comment.
        
        Args:
            comment: The comment to validate
            
        Returns:
            True if the comment is valid, False otherwise
        """
        # Add validation rules as needed
        return bool(comment.strip())