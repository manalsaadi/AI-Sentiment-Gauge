"""Sentiment analysis module for analyzing comment sentiment."""

import logging
from enum import Enum
from typing import List, Dict, Any, Union, Optional
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

class Sentiment(Enum):
    """Sentiment categories for classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class AnalysisMethod(Enum):
    """Methods used for sentiment analysis."""
    VADER = "vader"
    MULTILINGUAL_TRANSFORMER = "multilingual_transformer"
    TRANSLATION_BASED = "translation_based"

class SentimentAnalyzer:
    """Smart hybrid analyzer that automatically chooses the best approach."""
    
    def __init__(self, use_transformers: bool = True):
        """Initialize the sentiment analyzer.
        
        Args:
            use_transformers: Whether to use transformer models (requires transformers library)
        """
        self.use_transformers = use_transformers
        self._init_vader()
        
        if self.use_transformers:
            self._init_transformer_models()
        
    def _init_vader(self) -> None:
        """Initialize VADER as fallback option."""
        try:
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                logger.info("Downloading NLTK vader_lexicon")
                nltk.download('vader_lexicon', quiet=True)
            self.vader_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            logger.error(f"Error initializing VADER: {str(e)}")
            raise
            
    def _init_transformer_models(self) -> None:
        """Initialize transformer models for hybrid analysis with ONNX optimization."""
        try:
            # Try ONNX-optimized models first for best performance (50-60% faster)
            if self._init_onnx_models():
                logger.info("🚀 ONNX-optimized RoBERTa models initialized successfully")
                return
            else:
                logger.warning("ONNX models failed, falling back to PyTorch models")
                self._init_pytorch_models()
                
        except Exception as e:
            logger.error(f"Error initializing transformer models: {str(e)}")
            self.use_transformers = False
            self.multilingual_pipeline = None
            self.english_pipeline = None

    def _init_onnx_models(self) -> bool:
        """Initialize ONNX-optimized RoBERTa models for maximum performance."""
        try:
            from optimum.onnxruntime import ORTModelForSequenceClassification
            from transformers import AutoTokenizer, pipeline
            from pathlib import Path
            
            # Model cache directory
            cache_dir = Path(__file__).parent.parent.parent.parent / "model_cache"
            cache_dir.mkdir(exist_ok=True)
            
            # English ONNX model path
            english_onnx_path = cache_dir / "roberta_english_onnx"
            multilingual_onnx_path = cache_dir / "roberta_multilingual_onnx"
            
            # Initialize English ONNX model
            if english_onnx_path.exists():
                logger.info("📦 Loading cached English ONNX RoBERTa model...")
                english_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    english_onnx_path,
                    provider="CPUExecutionProvider"
                )
                english_tokenizer = AutoTokenizer.from_pretrained(english_onnx_path)
            else:
                logger.info("⚡ Converting English RoBERTa to ONNX (one-time process)...")
                english_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    "cardiffnlp/twitter-roberta-base-sentiment-latest",
                    export=True,
                    provider="CPUExecutionProvider"
                )
                english_tokenizer = AutoTokenizer.from_pretrained(
                    "cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
                
                # Save for future use
                english_onnx_model.save_pretrained(english_onnx_path)
                english_tokenizer.save_pretrained(english_onnx_path)
                logger.info(f"💾 Saved English ONNX model: {english_onnx_path}")
            
            # Initialize Multilingual ONNX model
            if multilingual_onnx_path.exists():
                logger.info("📦 Loading cached Multilingual ONNX RoBERTa model...")
                multilingual_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    multilingual_onnx_path,
                    provider="CPUExecutionProvider"
                )
                multilingual_tokenizer = AutoTokenizer.from_pretrained(multilingual_onnx_path)
            else:
                logger.info("⚡ Converting Multilingual RoBERTa to ONNX (one-time process)...")
                multilingual_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
                    export=True,
                    provider="CPUExecutionProvider"
                )
                multilingual_tokenizer = AutoTokenizer.from_pretrained(
                    "cardiffnlp/twitter-xlm-roberta-base-sentiment"
                )
                
                # Save for future use
                multilingual_onnx_model.save_pretrained(multilingual_onnx_path)
                multilingual_tokenizer.save_pretrained(multilingual_onnx_path)
                logger.info(f"💾 Saved Multilingual ONNX model: {multilingual_onnx_path}")
            
            # Create optimized pipelines
            self.english_pipeline = pipeline(
                "sentiment-analysis",
                model=english_onnx_model,
                tokenizer=english_tokenizer,
                device=-1
            )
            
            self.multilingual_pipeline = pipeline(
                "sentiment-analysis",
                model=multilingual_onnx_model,
                tokenizer=multilingual_tokenizer,
                device=-1
            )
            
            return True
            
        except ImportError as e:
            logger.info(f"ONNX dependencies not available: {e}")
            return False
        except Exception as e:
            logger.warning(f"Failed to initialize ONNX models: {e}")
            return False
    
    def _init_pytorch_models(self) -> None:
        """Initialize standard PyTorch models as fallback."""
        try:
            from transformers import pipeline
            
            logger.info("Loading PyTorch RoBERTa models (fallback mode)...")
            
            # Multilingual model for direct analysis (fast, 90-93% accuracy)
            self.multilingual_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                device=-1  # CPU inference
            )
            
            # English-specific model for high accuracy (95-97% accuracy)  
            self.english_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest", 
                device=-1  # CPU inference
            )
            
            logger.info("PyTorch transformer models initialized successfully")
            
        except ImportError:
            logger.warning("Transformers library not available, falling back to VADER only")
            self.use_transformers = False
            self.multilingual_pipeline = None
            self.english_pipeline = None
        except Exception as e:
            logger.error(f"Error initializing PyTorch models: {str(e)}")
            self.use_transformers = False
            self.multilingual_pipeline = None
            self.english_pipeline = None
            
    def analyze_sentiment(
        self,
        text: str,
        threshold: float = 0.05,
        source_language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Smart sentiment analysis that automatically chooses the best approach.
        
        Args:
            text: Text to analyze
            threshold: Threshold for neutral sentiment (used for VADER fallback)
            source_language: Optional source language hint
            
        Returns:
            Dictionary containing sentiment scores, method used, and metadata
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty")
            
        try:
            # Auto-select the best analysis method
            result = self._smart_analyze(text, source_language)
            return result
            
        except Exception as e:
            logger.error(f"Error in smart analysis: {str(e)}")
            # Fallback to VADER
            return self._analyze_with_vader(text, threshold)
    
    def _smart_analyze(self, text: str, source_language: Optional[str] = None) -> Dict[str, Any]:
        """Automatically choose the best analysis method based on text characteristics."""
        
        if not self.use_transformers:
            return self._analyze_with_vader(text, 0.05)
        
        # Detect characteristics for smart routing
        text_length = len(text.split())
        
        # Language detection (simple heuristic for now)
        detected_lang = self._simple_language_detection(text) if not source_language else source_language
        
        # Decision logic for method selection
        if detected_lang == "en" and text_length > 3:
            # English text with sufficient length → Use English-specific model
            return self._analyze_with_english_transformer(text)
            
        elif detected_lang in ["es", "fr", "de", "it", "pt", "nl"] and text_length > 2:
            # Major European languages → Multilingual model works well
            result = self._analyze_with_multilingual_transformer(text)
            
            # If confidence is low, try translation approach
            if result.get("confidence", 0) < 0.8:
                logger.info("Low confidence on multilingual, trying translation approach")
                translation_result = self._analyze_with_translation(text, detected_lang)
                
                # Use the result with higher confidence
                if translation_result.get("confidence", 0) > result.get("confidence", 0):
                    return translation_result
            
            return result
            
        elif text_length > 2:
            # Other languages or uncertain cases → Try multilingual first, fallback to translation
            try:
                multilingual_result = self._analyze_with_multilingual_transformer(text)
                
                # If very low confidence, try translation
                if multilingual_result.get("confidence", 0) < 0.7:
                    try:
                        translation_result = self._analyze_with_translation(text, detected_lang)
                        if translation_result.get("confidence", 0) > multilingual_result.get("confidence", 0):
                            return translation_result
                    except Exception as e:
                        logger.warning(f"Translation fallback failed: {e}")
                
                return multilingual_result
                
            except Exception as e:
                logger.warning(f"Multilingual analysis failed: {e}")
                return self._analyze_with_translation(text, detected_lang)
        
        else:
            # Very short text or other edge cases → Use VADER
            return self._analyze_with_vader(text, 0.05)
    
    def _simple_language_detection(self, text: str) -> str:
        """Simple language detection based on character patterns."""
        # This is a basic implementation - in production you might want to use langdetect
        text_lower = text.lower()
        
        # English indicators
        english_words = ["the", "and", "is", "it", "to", "of", "a", "in", "that", "this", "for"]
        english_score = sum(1 for word in english_words if word in text_lower)
        
        # French indicators  
        french_words = ["le", "la", "les", "de", "et", "est", "ce", "un", "une", "je", "du"]
        french_score = sum(1 for word in french_words if word in text_lower)
        
        # Spanish indicators
        spanish_words = ["el", "la", "los", "las", "de", "y", "es", "en", "un", "una", "que"]
        spanish_score = sum(1 for word in spanish_words if word in text_lower)
        
        # German indicators
        german_words = ["der", "die", "das", "und", "ist", "ich", "ein", "eine", "zu", "den"]
        german_score = sum(1 for word in german_words if word in text_lower)
        
        # Choose language with highest score
        scores = {
            "en": english_score,
            "fr": french_score, 
            "es": spanish_score,
            "de": german_score
        }
        
        detected_lang = max(scores, key=scores.get)
        return detected_lang if scores[detected_lang] > 0 else "unknown"
    
    def _is_onnx_model(self, pipeline) -> bool:
        """Check if a pipeline is using an ONNX model."""
        if pipeline is None:
            return False
        try:
            # Check if the model is an ONNX model by looking at the class name
            model = getattr(pipeline, 'model', None)
            if model is None:
                return False
            return 'ORTModel' in str(type(model))
        except Exception:
            return False
    
    def _analyze_with_english_transformer(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using English-specific transformer model."""
        try:
            if self.english_pipeline is None:
                raise ValueError("English pipeline not initialized")
                
            result = self.english_pipeline(text)
            
            # Debug output to understand the structure
            logger.debug(f"English transformer raw result: {result}")
            
            # Convert transformer output to our format
            # Handle both single result and list of results
            if isinstance(result, list) and len(result) > 0:
                result_item = result[0]
            else:
                result_item = result
                
            label = result_item.get('label', '').upper()
            score = result_item.get('score', 0.0)
            
            # Map labels to our sentiment categories
            positive = 0
            negative = 0
            neutral = 0
            
            if label in ['POSITIVE', 'POS', 'LABEL_2']:
                positive = score
                sentiment = Sentiment.POSITIVE
            elif label in ['NEGATIVE', 'NEG', 'LABEL_0']:
                negative = score
                sentiment = Sentiment.NEGATIVE
            else:  # NEUTRAL, NEU, LABEL_1, or unknown
                neutral = score
                sentiment = Sentiment.NEUTRAL
                
            # Calculate compound score
            compound = positive - negative
            
            return {
                'sentiment': sentiment.value,
                'compound_score': compound,
                'positive_score': positive,
                'negative_score': negative,
                'neutral_score': neutral,
                'confidence': score,
                'method': 'english_transformer_onnx' if self._is_onnx_model(self.english_pipeline) else 'english_transformer',
                'model': 'cardiffnlp/twitter-roberta-base-sentiment-latest (ONNX)' if self._is_onnx_model(self.english_pipeline) else 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                'raw_label': label,
                'raw_score': score
            }
            
        except Exception as e:
            logger.warning(f"English transformer analysis failed: {e}")
            return self._analyze_with_vader(text, 0.05)
    
    def _analyze_with_multilingual_transformer(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using multilingual transformer model."""
        try:
            if self.multilingual_pipeline is None:
                raise ValueError("Multilingual pipeline not initialized")
                
            result = self.multilingual_pipeline(text)
            
            # Debug output to understand the structure
            logger.debug(f"Multilingual transformer raw result: {result}")
            
            # Convert transformer output to our format
            # Handle both single result and list of results
            if isinstance(result, list) and len(result) > 0:
                result_item = result[0]
            else:
                result_item = result
                
            label = result_item.get('label', '').upper()
            score = result_item.get('score', 0.0)
            
            # Map labels to our sentiment categories
            positive = 0
            negative = 0
            neutral = 0
            
            if label in ['POSITIVE', 'POS', 'LABEL_2']:
                positive = score
                sentiment = Sentiment.POSITIVE
            elif label in ['NEGATIVE', 'NEG', 'LABEL_0']:
                negative = score
                sentiment = Sentiment.NEGATIVE
            else:  # NEUTRAL, NEU, LABEL_1, or unknown
                neutral = score
                sentiment = Sentiment.NEUTRAL
                
            # Calculate compound score
            compound = positive - negative
            
            return {
                'sentiment': sentiment.value,
                'compound_score': compound,
                'positive_score': positive,
                'negative_score': negative,
                'neutral_score': neutral,
                'confidence': score,
                'method': 'multilingual_transformer_onnx' if self._is_onnx_model(self.multilingual_pipeline) else 'multilingual_transformer',
                'model': 'cardiffnlp/twitter-xlm-roberta-base-sentiment (ONNX)' if self._is_onnx_model(self.multilingual_pipeline) else 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
                'raw_label': label,
                'raw_score': score
            }
            
        except Exception as e:
            logger.warning(f"Multilingual transformer analysis failed: {e}")
            return self._analyze_with_vader(text, 0.05)
    
    def _analyze_with_translation(self, text: str, source_language: str) -> Dict[str, Any]:
        """Analyze sentiment by translating to English first."""
        try:
            # Import translator here to avoid circular imports
            from ..translation.translator import Translator
            
            translator = Translator()
            
            # Translate to English
            translated_text = translator.translate(text, source_language, 'en')
            
            # Analyze translated text with English model
            if self.english_pipeline:
                result = self._analyze_with_english_transformer(translated_text)
                result['method'] = 'translation_then_english'
                result['translated_text'] = translated_text
                result['source_language'] = source_language
                return result
            else:
                # Fallback to VADER on translated text
                result = self._analyze_with_vader(translated_text, 0.05)
                result['method'] = 'translation_then_vader'
                result['translated_text'] = translated_text
                result['source_language'] = source_language
                return result
                
        except Exception as e:
            logger.warning(f"Translation analysis failed: {e}")
            return self._analyze_with_vader(text, 0.05)
    
    def _analyze_with_vader(self, text: str, threshold: float) -> Dict[str, Any]:
        """Fallback sentiment analysis using VADER."""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
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
                'neutral_score': scores['neu'],
                'confidence': abs(compound),
                'method': 'vader',
                'model': 'nltk_vader'
            }
            
        except Exception as e:
            logger.error(f"Error in VADER analysis: {str(e)}")
            raise
    
    def get_percentage_breakdown(self, analysis_result: Dict[str, Any]) -> Dict[str, float]:
        """Convert analysis result to percentage breakdown expected by frontend.
        
        Args:
            analysis_result: Result from analyze_sentiment method
            
        Returns:
            Dictionary with positive, negative, neutral percentages (0-100)
        """
        positive = analysis_result.get('positive_score', 0)
        negative = analysis_result.get('negative_score', 0) 
        neutral = analysis_result.get('neutral_score', 0)
        
        # Ensure scores sum to 1 for percentage calculation
        total = positive + negative + neutral
        if total == 0:
            total = 1
            
        return {
            'positive': round((positive / total) * 100, 1),
            'negative': round((negative / total) * 100, 1),
            'neutral': round((neutral / total) * 100, 1)
        }
    
    def analyze_with_percentages(self, text: str, source_language: Optional[str] = None) -> Dict[str, Any]:
        """Complete analysis with percentage breakdown for frontend compatibility.
        
        Args:
            text: Text to analyze
            source_language: Optional language hint
            
        Returns:
            Enhanced result with percentage breakdown
        """
        # Get base analysis
        result = self.analyze_sentiment(text, source_language=source_language)
        
        # Add percentage breakdown
        percentages = self.get_percentage_breakdown(result)
        result.update(percentages)
        
        # Add summary text based on primary sentiment
        primary_sentiment = result.get('sentiment', 'neutral')
        confidence = result.get('confidence', 0)
        method = result.get('method', 'unknown')
        
        if confidence > 0.8:
            confidence_text = "very confident"
        elif confidence > 0.6:
            confidence_text = "confident"
        elif confidence > 0.4:
            confidence_text = "somewhat confident"
        else:
            confidence_text = "less confident"
            
        result['summary'] = f"Analysis is {confidence_text} that this text is {primary_sentiment} (using {method})"
        
        return result
            
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