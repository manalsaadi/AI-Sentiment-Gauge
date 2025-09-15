"""Sentiment analysis module for analyzing comment sentiment."""

import logging
from enum import Enum
from typing import List, Dict, Any, Union
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

class Sentiment(Enum):
    """Sentiment categories for classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class SentimentAnalyzer:
    """Analyzer for determining comment sentiment."""
    
    def __init__(self):
        """Initialize the sentiment analyzer with required NLTK resources."""
        self._ensure_nltk_resources()
        self.analyzer = SentimentIntensityAnalyzer()
        
    def _ensure_nltk_resources(self) -> None:
        """Download required NLTK resources if not present."""
        try:
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                logger.info("Downloading NLTK vader_lexicon")
                nltk.download('vader_lexicon', quiet=True)
        except Exception as e:
            logger.error(f"Error downloading NLTK resources: {str(e)}")
            raise
            
    def analyze_sentiment(
        self,
        text: str,
        threshold: float = 0.05
    ) -> Dict[str, Any]:
        """Analyze the sentiment of a text.
        
        Args:
            text: Text to analyze
            threshold: Threshold for neutral sentiment (-threshold to +threshold)
            
        Returns:
            Dictionary containing sentiment scores and category
            
        Raises:
            ValueError: If input text is empty
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        try:
            # Get sentiment scores
            scores = self.analyzer.polarity_scores(text)
            compound = scores['compound']
            
            # Determine sentiment category
            if compound >= threshold:
                sentiment = Sentiment.POSITIVE
            elif compound <= -threshold:
                sentiment = Sentiment.NEGATIVE
            else:
                sentiment = Sentiment.NEUTRAL
                
            return {
                'sentiment': sentiment.value,
                'compound_score': compound,
                'positive_score': scores['pos'],
                'negative_score': scores['neg'],
                'neutral_score': scores['neu']
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            raise
            
    def batch_analyze(
        self,
        texts: List[str],
        threshold: float = 0.05
    ) -> List[Dict[str, Any]]:
        """Analyze sentiment for multiple texts.
        
        Args:
            texts: List of texts to analyze
            threshold: Threshold for neutral sentiment
            
        Returns:
            List of sentiment analysis results
            
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
            
        logger.info(f"Analyzing sentiment for {len(texts)} texts")
        results = []
        
        for text in texts:
            try:
                result = self.analyze_sentiment(text, threshold)
                results.append(result)
            except ValueError:
                # For empty texts, add None result
                results.append(None)
            except Exception as e:
                logger.error(f"Error analyzing text: {str(e)}")
                results.append(None)
                
        return results
        
    def get_sentiment_distribution(
        self,
        texts: List[str],
        threshold: float = 0.05
    ) -> Dict[str, Union[int, float]]:
        """Calculate sentiment distribution across texts.
        
        Args:
            texts: List of texts to analyze
            threshold: Threshold for neutral sentiment
            
        Returns:
            Dictionary with sentiment counts and percentages
            
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
            
        results = self.batch_analyze(texts, threshold)
        valid_results = [r for r in results if r is not None]
        
        if not valid_results:
            return {
                'total': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'positive_percent': 0.0,
                'negative_percent': 0.0,
                'neutral_percent': 0.0
            }
            
        # Count sentiments
        sentiment_counts = {
            'positive': sum(1 for r in valid_results if r['sentiment'] == 'positive'),
            'negative': sum(1 for r in valid_results if r['sentiment'] == 'negative'),
            'neutral': sum(1 for r in valid_results if r['sentiment'] == 'neutral')
        }
        
        total = len(valid_results)
        
        return {
            'total': total,
            'positive_count': sentiment_counts['positive'],
            'negative_count': sentiment_counts['negative'],
            'neutral_count': sentiment_counts['neutral'],
            'positive_percent': (sentiment_counts['positive'] / total) * 100,
            'negative_percent': (sentiment_counts['negative'] / total) * 100,
            'neutral_percent': (sentiment_counts['neutral'] / total) * 100
        }