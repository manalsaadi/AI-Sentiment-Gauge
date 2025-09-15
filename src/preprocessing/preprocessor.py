"""Text preprocessing module for cleaning and normalizing comments."""

import logging
import re
import string
from typing import List, Set, Optional
import emoji
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Handler for text cleaning and normalization."""
    
    def __init__(self):
        """Initialize the text preprocessor with required NLTK resources."""
        self._ensure_nltk_resources()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Common contractions mapping
        self.contractions = {
            "ain't": "is not", "aren't": "are not", "can't": "cannot",
            "could've": "could have", "couldn't": "could not", 
            "didn't": "did not", "doesn't": "does not", "don't": "do not",
            "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
            "he'd": "he would", "he'll": "he will", "he's": "he is",
            "how'd": "how did", "how'll": "how will", "how's": "how is",
            "i'd": "i would", "i'll": "i will", "i'm": "i am",
            "i've": "i have", "isn't": "is not", "it'd": "it would",
            "it'll": "it will", "it's": "it is", "let's": "let us",
            "might've": "might have", "mightn't": "might not",
            "must've": "must have", "mustn't": "must not",
            "should've": "should have", "shouldn't": "should not",
            "that'll": "that will", "that's": "that is",
            "there'd": "there would", "there's": "there is",
            "they'd": "they would", "they'll": "they will",
            "they're": "they are", "they've": "they have",
            "wasn't": "was not", "we'd": "we would", "we'll": "we will",
            "we're": "we are", "we've": "we have", "weren't": "were not",
            "what'd": "what did", "what's": "what is",
            "when'd": "when did", "when'll": "when will",
            "when's": "when is", "where'd": "where did",
            "where's": "where is", "who'd": "who would",
            "who'll": "who will", "who's": "who is",
            "why'd": "why did", "why'll": "why will",
            "why's": "why is", "won't": "will not", "would've": "would have",
            "wouldn't": "would not", "you'd": "you would",
            "you'll": "you will", "you're": "you are", "you've": "you have"
        }
        
        # Compile regex patterns for efficiency
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        self.mention_pattern = re.compile(r'@[\w_]+')
        self.hashtag_pattern = re.compile(r'#[\w_]+')
        self.email_pattern = re.compile(r'\S+@\S+')
        self.multiple_spaces = re.compile(r'\s+')
        
    def _ensure_nltk_resources(self) -> None:
        """Download required NLTK resources if not present."""
        try:
            required_resources = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
            for resource in required_resources:
                try:
                    nltk.data.find(f'tokenizers/{resource}')
                except LookupError:
                    logger.info(f"Downloading NLTK resource: {resource}")
                    nltk.download(resource, quiet=True)
        except Exception as e:
            logger.error(f"Error downloading NLTK resources: {str(e)}")
            raise
            
    def preprocess(
        self,
        text: str,
        remove_urls: bool = True,
        remove_mentions: bool = True,
        remove_hashtags: bool = False,
        remove_emails: bool = True,
        remove_stopwords: bool = True,
        remove_punctuation: bool = True,
        convert_emojis: bool = True,
        lemmatize: bool = True,
        lowercase: bool = True
    ) -> str:
        """Preprocess text with specified options.
        
        Args:
            text: Input text to preprocess
            remove_urls: Whether to remove URLs
            remove_mentions: Whether to remove @mentions
            remove_hashtags: Whether to remove #hashtags
            remove_emails: Whether to remove email addresses
            remove_stopwords: Whether to remove stop words
            remove_punctuation: Whether to remove punctuation
            convert_emojis: Whether to convert emojis to text
            lemmatize: Whether to lemmatize words
            lowercase: Whether to convert to lowercase
            
        Returns:
            Preprocessed text
            
        Raises:
            ValueError: If input text is empty
        """
        if not text.strip():
            return text
            
        logger.debug(f"Preprocessing text: {text[:50]}...")
        
        # Convert to lowercase if requested
        if lowercase:
            text = text.lower()
            
        # Replace contractions
        for contraction, expansion in self.contractions.items():
            if lowercase:
                text = re.sub(r'\b' + contraction + r'\b', expansion, text)
            else:
                text = re.sub(
                    r'\b' + contraction + r'\b',
                    expansion,
                    text,
                    flags=re.IGNORECASE
                )
                
        # Remove URLs
        if remove_urls:
            text = self.url_pattern.sub(' ', text)
            
        # Remove @mentions
        if remove_mentions:
            text = self.mention_pattern.sub(' ', text)
            
        # Remove #hashtags (preserve text without #)
        if remove_hashtags:
            text = self.hashtag_pattern.sub(lambda m: m.group(0)[1:], text)
            
        # Remove emails
        if remove_emails:
            text = self.email_pattern.sub(' ', text)
            
        # Convert emojis to text
        if convert_emojis:
            text = emoji.demojize(text)
            text = text.replace(':', ' ').replace('_', ' ')
            
        # Tokenize
        tokens = word_tokenize(text)
        
        # Process tokens
        processed_tokens = []
        for token in tokens:
            # Skip stop words if requested
            if remove_stopwords and token.lower() in self.stop_words:
                continue
                
            # Remove punctuation if requested
            if remove_punctuation and token in string.punctuation:
                continue
                
            # Lemmatize if requested
            if lemmatize:
                token = self.lemmatizer.lemmatize(token)
                
            processed_tokens.append(token)
            
        # Join tokens and clean up spaces
        text = ' '.join(processed_tokens)
        text = self.multiple_spaces.sub(' ', text).strip()
        
        logger.debug(f"Preprocessing complete: {text[:50]}...")
        return text
        
    def batch_preprocess(
        self,
        texts: List[str],
        **kwargs
    ) -> List[str]:
        """Preprocess a batch of texts with the same settings.
        
        Args:
            texts: List of texts to preprocess
            **kwargs: Preprocessing options to pass to preprocess()
            
        Returns:
            List of preprocessed texts
            
        Raises:
            ValueError: If input list is empty
        """
        if not texts:
            raise ValueError("Input text list cannot be empty")
            
        logger.info(f"Batch preprocessing {len(texts)} texts")
        return [self.preprocess(text, **kwargs) for text in texts]