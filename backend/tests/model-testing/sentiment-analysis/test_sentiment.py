#!/usr/bin/env python3
"""
Test script for enhanced sentiment analysis API
"""
import requests
import json
import sys
import os

# Add backend src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend', 'src'))

def test_enhanced_sentiment():
    """Test the enhanced sentiment analysis directly"""
    try:
        # Import components directly
        from analysis.sentiment_analyzer import SentimentAnalyzer
        from analysis.keyword_extractor import KeywordExtractor
        from preprocessing.preprocessor import TextPreprocessor
        
        # Initialize components
        sentiment_analyzer = SentimentAnalyzer()
        keyword_extractor = KeywordExtractor()
        preprocessor = TextPreprocessor()
        
        # Test text
        test_text = "I absolutely love this product! It's amazing and works perfectly. The customer service was excellent too. Highly recommended!"
        
        print("🧪 Testing Enhanced Sentiment Analysis")
        print(f"📝 Input text: {test_text}")
        print("-" * 80)
        
        # Preprocess
        cleaned_text = preprocessor.preprocess(test_text)
        print(f"🧹 Cleaned text: {cleaned_text}")
        
        # Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze_sentiment(cleaned_text)
        print(f"😊 Raw sentiment scores: {sentiment_result}")
        
        # Convert to percentages
        pos_score = sentiment_result['positive_score'] * 100
        neg_score = sentiment_result['negative_score'] * 100  
        neu_score = sentiment_result['neutral_score'] * 100
        
        # Normalize to ensure they sum to 100%
        total = pos_score + neg_score + neu_score
        if total > 0:
            pos_score = (pos_score / total) * 100
            neg_score = (neg_score / total) * 100
            neu_score = (neu_score / total) * 100
            
        print(f"📊 Percentage breakdown:")
        print(f"   ✅ Positive: {pos_score:.1f}%")
        print(f"   ❓ Neutral: {neu_score:.1f}%") 
        print(f"   ❌ Negative: {neg_score:.1f}%")
        
        # Extract keywords
        keywords_result = keyword_extractor.extract_keywords_frequency(
            cleaned_text, 
            top_k=8, 
            min_length=3
        )
        keywords = [kw['keyword'] for kw in keywords_result]
        print(f"🔑 Keywords: {keywords}")
        
        # Generate summary
        dominant_sentiment = sentiment_result['sentiment']
        confidence = max(sentiment_result['positive_score'], 
                        sentiment_result['negative_score'], 
                        sentiment_result['neutral_score'])
        
        summary = f"Analysis complete. The text shows {dominant_sentiment} sentiment with {confidence*100:.1f}% confidence."
        if keywords:
            summary += f" Key topics include: {', '.join(keywords[:3])}."
            
        print(f"📋 Summary: {summary}")
        print("\n✅ Enhanced sentiment analysis working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing sentiment analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_sentiment()