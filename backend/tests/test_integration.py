"""Integration tests for the complete comment analysis pipeline."""

import pytest
import time
from pathlib import Path
from typing import List

from src.input.comment_input import CommentInput
from src.translation.translator import Translator
from src.preprocessing.preprocessor import TextPreprocessor
from src.analysis.sentiment_analyzer import SentimentAnalyzer
from src.analysis.keyword_extractor import KeywordExtractor
from src.reporting.report_generator import ReportGenerator

# Test data
SAMPLE_COMMENTS = {
    'english': [
        "This product is amazing! Really love it.",
        "Not happy with the service, terrible experience.",
        "The quality is okay, nothing special."
    ],
    'french': [
        "Ce produit est incroyable! Je l'adore.",
        "Pas content du service, expérience terrible.",
        "La qualité est correcte, rien de spécial."
    ],
    'german': [
        "Dieses Produkt ist fantastisch! Ich liebe es.",
        "Nicht zufrieden mit dem Service, schreckliche Erfahrung.",
        "Die Qualität ist okay, nichts Besonderes."
    ],
    'spanish': [
        "¡Este producto es increíble! Me encanta.",
        "No estoy contento con el servicio, experiencia terrible.",
        "La calidad está bien, nada especial."
    ]
}

@pytest.fixture
def pipeline_components():
    """Create instances of all pipeline components."""
    return {
        'translator': Translator(),
        'preprocessor': TextPreprocessor(),
        'sentiment_analyzer': SentimentAnalyzer(),
        'keyword_extractor': KeywordExtractor(),
        'report_generator': ReportGenerator()
    }

def test_full_pipeline_english(pipeline_components, tmp_path):
    """Test complete pipeline with English comments."""
    comments = SAMPLE_COMMENTS['english']
    
    # Process through pipeline
    preprocessed = pipeline_components['preprocessor'].batch_preprocess(comments)
    sentiment_results = pipeline_components['sentiment_analyzer'].batch_analyze(preprocessed)
    sentiment_dist = pipeline_components['sentiment_analyzer'].get_sentiment_distribution(preprocessed)
    keyword_results = pipeline_components['keyword_extractor'].get_common_keywords(preprocessed)
    
    # Generate report
    output_file = tmp_path / "report_english.md"
    report = pipeline_components['report_generator'].generate_report(
        comments,
        sentiment_results,
        keyword_results,
        sentiment_dist,
        output_file
    )
    
    # Verify outputs
    assert output_file.exists()
    assert len(sentiment_results) == len(comments)
    assert all(result['sentiment'] in ['positive', 'negative', 'neutral']
              for result in sentiment_results if result)
    assert 'frequency_based' in keyword_results
    assert 'tfidf_based' in keyword_results

def test_full_pipeline_multilingual(pipeline_components, tmp_path):
    """Test complete pipeline with multilingual comments."""
    # Combine comments from all languages
    all_comments = []
    for lang_comments in SAMPLE_COMMENTS.values():
        all_comments.extend(lang_comments)
    
    # Translate non-English comments
    translated = []
    for comment in all_comments:
        try:
            translated_text = pipeline_components['translator'].translate_to_english(comment)
            translated.append(translated_text)
        except Exception as e:
            pytest.fail(f"Translation failed: {str(e)}")
    
    # Continue with pipeline
    preprocessed = pipeline_components['preprocessor'].batch_preprocess(translated)
    sentiment_results = pipeline_components['sentiment_analyzer'].batch_analyze(preprocessed)
    sentiment_dist = pipeline_components['sentiment_analyzer'].get_sentiment_distribution(preprocessed)
    keyword_results = pipeline_components['keyword_extractor'].get_common_keywords(preprocessed)
    
    # Generate report
    output_file = tmp_path / "report_multilingual.md"
    report = pipeline_components['report_generator'].generate_report(
        all_comments,
        sentiment_results,
        keyword_results,
        sentiment_dist,
        output_file
    )
    
    # Verify outputs
    assert output_file.exists()
    assert len(sentiment_results) == len(all_comments)
    assert all(result['sentiment'] in ['positive', 'negative', 'neutral']
              for result in sentiment_results if result)

def test_performance_benchmark(pipeline_components):
    """Test performance with larger dataset (500 comments)."""
    # Generate test dataset
    large_dataset = []
    for _ in range(167):  # Will give us 501 comments
        large_dataset.extend(SAMPLE_COMMENTS['english'])
    large_dataset = large_dataset[:500]  # Ensure exactly 500
    
    # Measure processing time
    start_time = time.time()
    
    # Run pipeline
    preprocessed = pipeline_components['preprocessor'].batch_preprocess(large_dataset)
    sentiment_results = pipeline_components['sentiment_analyzer'].batch_analyze(preprocessed)
    sentiment_dist = pipeline_components['sentiment_analyzer'].get_sentiment_distribution(preprocessed)
    keyword_results = pipeline_components['keyword_extractor'].get_common_keywords(preprocessed)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Verify performance requirement (15 seconds)
    assert processing_time <= 15, f"Processing took {processing_time:.2f} seconds"
    
def test_error_handling(pipeline_components):
    """Test error handling in the pipeline."""
    # Test with empty input
    with pytest.raises(ValueError):
        pipeline_components['preprocessor'].batch_preprocess([])
    
    # Test with None values
    with pytest.raises(ValueError):
        pipeline_components['sentiment_analyzer'].analyze_sentiment(None)
    
    # Test with invalid language
    with pytest.raises(Exception):
        pipeline_components['translator'].translate_to_english("こんにちは")  # Japanese
        
def test_input_formats(pipeline_components, tmp_path):
    """Test different input formats."""
    # Test file input
    test_file = tmp_path / "comments.txt"
    test_file.write_text("\n".join(SAMPLE_COMMENTS['english']))
    file_comments = CommentInput.process_file_input(test_file)
    assert len(file_comments) == len(SAMPLE_COMMENTS['english'])
    
    # Test batch text input
    batch_text = "\n---\n".join(SAMPLE_COMMENTS['english'])
    batch_comments = CommentInput.process_text_input(batch_text)
    assert len(batch_comments) == len(SAMPLE_COMMENTS['english'])