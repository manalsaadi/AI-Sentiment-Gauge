"""Keyword extraction module for identifying important terms in comments."""

import logging
from collections import Counter
from typing import List, Dict, Union, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)

class KeywordExtractor:
    """Extractor for identifying important keywords in text."""
    
    def __init__(self):
        """Initialize the keyword extractor."""
        # These are defaults; may be overridden for small input
        self.tfidf_vectorizer = None
        
    def extract_keywords_frequency(
        self,
        text: str,
        top_k: int = 10,
        min_length: int = 3
    ) -> List[Dict[str, Union[str, int]]]:
        """Extract keywords using frequency-based approach.
        
        Args:
            text: Text to analyze
            top_k: Number of top keywords to return
            min_length: Minimum keyword length
            
        Returns:
            List of dictionaries with keywords and their frequencies
            
        Raises:
            ValueError: If input text is empty
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        # Split into words and count frequencies
        words = [
            word.lower() for word in text.split()
            if len(word) >= min_length
        ]
        word_freq = Counter(words)
        
        # Get top k keywords
        keywords = word_freq.most_common(top_k)
        return [
            {'keyword': word, 'frequency': freq}
            for word, freq in keywords
        ]
        
    def extract_keywords_tfidf(
        self,
        texts: List[str],
        top_k: int = 10
    ) -> List[List[Dict[str, Union[str, float]]]]:
        """Extract keywords using TF-IDF approach.
        
        Args:
            texts: List of texts to analyze
            top_k: Number of top keywords to return per text
        
        Returns:
            List of keyword lists for each text
        
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
        try:
            n_docs = len(texts)
            # Ensure min_df and max_df are valid for the number of documents
            if n_docs < 2:
                min_df = 1
                max_df = 1.0
            else:
                min_df = 2
                max_df = 0.95
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                max_df=max_df,
                min_df=min_df,
                stop_words='english'
            )
            # Fit and transform the texts
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            feature_names = np.array(self.tfidf_vectorizer.get_feature_names_out())
            # Extract top keywords for each text
            results = []
            for i in range(tfidf_matrix.shape[0]):
                # Get scores for current text
                scores = tfidf_matrix[i].toarray()[0]
                # Get indices of top k scores
                top_indices = np.argsort(scores)[-top_k:][::-1]
                # Get keywords and scores
                keywords = [
                    {
                        'keyword': feature_names[idx],
                        'tfidf_score': float(scores[idx])
                    }
                    for idx in top_indices
                    if scores[idx] > 0
                ]
                results.append(keywords)
            return results
        except Exception as e:
            logger.error(f"Error extracting TF-IDF keywords: {str(e)}")
            raise
            
    def extract_keywords_combined(
        self,
        texts: List[str],
        top_k: int = 10,
        min_length: int = 3
    ) -> List[Dict[str, List[Dict[str, Union[str, float, int]]]]]:
        """Extract keywords using both frequency and TF-IDF approaches.
        
        Args:
            texts: List of texts to analyze
            top_k: Number of top keywords to return
            min_length: Minimum keyword length
            
        Returns:
            List of dictionaries containing both frequency and TF-IDF keywords
            
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
            
        logger.info(f"Extracting keywords from {len(texts)} texts")
        
        # Get TF-IDF keywords
        tfidf_keywords = self.extract_keywords_tfidf(texts, top_k)
        
        # Get frequency-based keywords for each text
        freq_keywords = [
            self.extract_keywords_frequency(text, top_k, min_length)
            for text in texts
        ]
        
        # Combine results
        results = []
        for freq_kw, tfidf_kw in zip(freq_keywords, tfidf_keywords):
            results.append({
                'frequency_based': freq_kw,
                'tfidf_based': tfidf_kw
            })
            
        return results
        
    def get_common_keywords(
        self,
        texts: List[str],
        top_k: int = 10,
        min_length: int = 3
    ) -> Dict[str, List[Dict[str, Union[str, int, float]]]]:
        """Get common keywords across all texts.
        
        Args:
            texts: List of texts to analyze
            top_k: Number of top keywords to return
            min_length: Minimum keyword length
            
        Returns:
            Dictionary containing common keywords by both methods
            
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
            
        # Combine all texts for frequency analysis
        combined_text = " ".join(texts)
        freq_keywords = self.extract_keywords_frequency(
            combined_text,
            top_k,
            min_length
        )
        
        # Get TF-IDF keywords
        tfidf_keywords = self.extract_keywords_tfidf([combined_text], top_k)[0]
        
        return {
            'frequency_based': freq_keywords,
            'tfidf_based': tfidf_keywords
        }