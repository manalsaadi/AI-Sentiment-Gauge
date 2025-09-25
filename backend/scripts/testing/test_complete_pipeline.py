#!/usr/bin/env python3
"""
Complete test of sentiment analysis and translation pipeline
for the French sentence: "je suis quelqu'un de gentille qui trouve la vie géniale"
"""

import sys
import os
from pathlib import Path

# Add backend src to Python path
backend_src = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_src))

def test_full_pipeline():
    """Test the complete sentiment analysis and translation pipeline."""
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    print("🧪 COMPLETE SENTIMENT ANALYSIS & TRANSLATION TEST")
    print("=" * 60)
    print(f"📝 Test text: '{test_text}'")
    print(f"🌐 Expected language: French (fr)")
    print(f"💭 Expected sentiment: Positive (géniale = awesome/great)")
    print()
    
    # Test 1: Language Detection Only
    print("1️⃣ TESTING LANGUAGE DETECTION")
    print("-" * 30)
    
    try:
        from langdetect import detect
        detected = detect(test_text)
        print(f"   langdetect result: {detected}")
        print(f"   ✅ {'CORRECT' if detected == 'fr' else 'INCORRECT'} - Expected 'fr'")
    except ImportError:
        print("   ❌ langdetect not available")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Translation Module
    print("2️⃣ TESTING TRANSLATION MODULE")
    print("-" * 30)
    
    try:
        from translation.translator import Translator, Language
        translator = Translator()
        
        # Test language detection
        detected_lang = translator.detect_language(test_text)
        print(f"   Detected language: {detected_lang.value}")
        print(f"   ✅ {'CORRECT' if detected_lang == Language.FRENCH else 'INCORRECT'}")
        
        # Test translation
        translated_result = translator.translate(test_text)
        print(f"   Translation: '{translated_result['translated_text']}'")
        print(f"   Source: {translated_result['source_language'].value}")
        print(f"   Target: {translated_result['target_language'].value}")
        print(f"   Method: {translated_result.get('method', 'unknown')}")
        
    except ImportError as e:
        print(f"   ❌ Translation import failed: {e}")
        print("   (This is expected if ML dependencies aren't installed)")
    except Exception as e:
        print(f"   ❌ Translation error: {e}")
    
    print()
    
    # Test 3: Sentiment Analysis
    print("3️⃣ TESTING SENTIMENT ANALYSIS")
    print("-" * 30)
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        analyzer = SentimentAnalyzer()
        
        # Test sentiment analysis with percentages
        result = analyzer.analyze_with_percentages(test_text)
        
        print(f"   Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"   Positive: {result.get('positive', 0):.1f}%")
        print(f"   Negative: {result.get('negative', 0):.1f}%")
        print(f"   Neutral: {result.get('neutral', 0):.1f}%")
        print(f"   Confidence: {result.get('confidence', 0):.3f}")
        print(f"   Method: {result.get('method', 'unknown')}")
        print(f"   Summary: {result.get('summary', 'No summary')}")
        
        # Check if result makes sense
        expected_positive = result.get('sentiment') == 'positive'
        print(f"   ✅ {'CORRECT' if expected_positive else 'NEEDS_REVIEW'} - Expected positive sentiment")
        
    except ImportError as e:
        print(f"   ❌ Sentiment analysis import failed: {e}")
        print("   (This is expected if ML dependencies aren't installed)")
    except Exception as e:
        print(f"   ❌ Sentiment analysis error: {e}")
    
    print()
    
    # Test 4: Complete API Integration
    print("4️⃣ TESTING COMPLETE API INTEGRATION")
    print("-" * 30)
    
    try:
        # Simulate what the main API would do
        from analysis.sentiment_analyzer import SentimentAnalyzer
        from translation.translator import Translator
        
        # Initialize components
        analyzer = SentimentAnalyzer()
        translator = Translator()
        
        # Step 1: Detect language
        detected_lang = translator.detect_language(test_text)
        print(f"   Step 1 - Language detected: {detected_lang.value}")
        
        # Step 2: Analyze sentiment (with potential translation)
        sentiment_result = analyzer.analyze_with_percentages(test_text, source_language=detected_lang.value)
        print(f"   Step 2 - Sentiment: {sentiment_result.get('sentiment')}")
        print(f"   Step 2 - Method: {sentiment_result.get('method')}")
        
        # Step 3: Translation if needed
        if detected_lang.value != 'en':
            translation_result = translator.translate(test_text)
            print(f"   Step 3 - Translation: '{translation_result['translated_text']}'")
            print(f"   Step 3 - Translation method: {translation_result.get('method')}")
        else:
            print(f"   Step 3 - No translation needed (already English)")
        
        print(f"   ✅ Complete pipeline executed successfully!")
        
    except Exception as e:
        print(f"   ❌ API integration error: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🏁 TEST COMPLETE")
    print("=" * 60)
    
    # Summary
    print("📊 EXPECTED RESULTS:")
    print("   • Language detection: French (fr) ✓")
    print("   • Sentiment: Positive ✓")
    print("   • Translation: 'I am someone nice who finds life awesome' ✓")
    print("   • Summary: Should mention positive sentiment ✓")

if __name__ == "__main__":
    test_full_pipeline()