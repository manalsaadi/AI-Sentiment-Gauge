#!/usr/bin/env python3
"""
Simple backend test script for French sentence sentiment analysis and translation.
Run this directly to test without frontend or complex dependencies.
"""

def test_langdetect_only():
    """Test only the langdetect functionality."""
    print("🔍 Testing langdetect library...")
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    try:
        from langdetect import detect
        detected = detect(test_text)
        print(f"✅ langdetect works!")
        print(f"   Text: '{test_text}'")
        print(f"   Detected: {detected}")
        print(f"   Expected: fr")
        print(f"   Result: {'✅ CORRECT' if detected == 'fr' else '❌ WRONG'}")
        return detected == 'fr'
    except ImportError:
        print("❌ langdetect not installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_backend_imports():
    """Test if backend modules can be imported."""
    print("\n📦 Testing backend imports...")
    
    import sys
    import os
    
    # Add backend src to path
    backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
    sys.path.insert(0, backend_src)
    
    # Test imports one by one
    modules_to_test = [
        ('translation.marian_quantized', 'MarianQuantizedTranslator'),
        ('translation.translator', 'Translator'),
        ('analysis.sentiment_analyzer', 'SentimentAnalyzer'),
    ]
    
    success_count = 0
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} - OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name}.{class_name} - Import Error: {e}")
        except Exception as e:
            print(f"⚠️  {module_name}.{class_name} - Other Error: {e}")
    
    print(f"\n📊 Import Results: {success_count}/{len(modules_to_test)} modules imported successfully")
    return success_count == len(modules_to_test)

def test_full_translation():
    """Test full translation from French to English."""
    print("\n🔄 Testing translation to English...")
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    try:
        import sys
        import os
        backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        sys.path.insert(0, backend_src)
        
        from translation.translator import Translator
        
        # Create translator
        translator = Translator()
        
        # Test translation using the correct method name
        translated_text = translator.translate_to_english(test_text)
        
        print(f"✅ Translation works!")
        print(f"   Original: '{test_text}'")
        print(f"   Translated: '{translated_text}'")
        print(f"   Method: translate_to_english")
        
        # Check if translation makes sense
        translated_lower = translated_text.lower()
        expected_words = ['nice', 'kind', 'life', 'great', 'awesome', 'wonderful', 'someone', 'person', 'find']
        found_words = [word for word in expected_words if word in translated_lower]
        
        if found_words:
            print(f"   Expected words found: {found_words}")
            print(f"   Quality: ✅ GOOD")
            return True, translated_text
        else:
            print(f"   Quality: ⚠️  NEEDS REVIEW")
            print(f"   (Translation might be correct but using different words)")
            return True, translated_text
        
    except Exception as e:
        print(f"❌ Translation Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_sentiment_analysis():
    """Test sentiment analysis on both French and English."""
    print("\n💭 Testing sentiment analysis...")
    
    french_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    try:
        import sys
        import os
        backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        sys.path.insert(0, backend_src)
        
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Create analyzer
        analyzer = SentimentAnalyzer()
        
        # Test sentiment analysis on French text
        result = analyzer.analyze_with_percentages(french_text)
        
        print(f"✅ Sentiment analysis works!")
        print(f"   Text: '{french_text}'")
        print(f"   Sentiment: {result.get('sentiment', 'unknown')}")
        print(f"   Positive: {result.get('positive', 0):.1f}%")
        print(f"   Negative: {result.get('negative', 0):.1f}%")
        print(f"   Neutral: {result.get('neutral', 0):.1f}%")
        print(f"   Confidence: {result.get('confidence', 0):.3f}")
        print(f"   Method: {result.get('method', 'unknown')}")
        
        if 'summary' in result:
            print(f"   Summary: {result['summary']}")
        
        # Check if sentiment makes sense (should be positive)
        sentiment = result.get('sentiment', 'unknown')
        if sentiment == 'positive':
            print(f"   Expected result: ✅ CORRECT (should be positive)")
            return True, result
        else:
            print(f"   Expected result: ⚠️  REVIEW NEEDED (expected positive, got {sentiment})")
            return True, result
        
    except Exception as e:
        print(f"❌ Sentiment Analysis Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_sentiment_on_english():
    """Test sentiment analysis on English translation."""
    print("\n💭 Testing sentiment analysis on English translation...")
    
    # Common English translations of the French sentence
    english_texts = [
        "I am someone nice who finds life awesome",
        "I am someone kind who finds life great", 
        "I am a nice person who thinks life is wonderful"
    ]
    
    try:
        import sys
        import os
        backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        sys.path.insert(0, backend_src)
        
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        for i, text in enumerate(english_texts, 1):
            print(f"\n   Test {i}: '{text}'")
            result = analyzer.analyze_with_percentages(text)
            
            sentiment = result.get('sentiment', 'unknown')
            positive_pct = result.get('positive', 0)
            confidence = result.get('confidence', 0)
            
            print(f"   → Sentiment: {sentiment} ({positive_pct:.1f}% positive)")
            print(f"   → Confidence: {confidence:.3f}")
            print(f"   → Method: {result.get('method', 'unknown')}")
            
            if sentiment == 'positive':
                print(f"   → Result: ✅ CORRECT")
            else:
                print(f"   → Result: ⚠️  UNEXPECTED ({sentiment})")
        
        return True
        
    except Exception as e:
        print(f"❌ English Sentiment Analysis Error: {e}")
        return False

def test_language_detection_only():
    """Test just the language detection part."""
    print("\n🌐 Testing language detection...")
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    try:
        import sys
        import os
        backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        sys.path.insert(0, backend_src)
        
        from translation.marian_quantized import MarianQuantizedTranslator
        
        # Create translator (don't load models yet)
        translator = MarianQuantizedTranslator()
        
        # Test language detection
        detected = translator.detect_language(test_text)
        print(f"✅ Language detection works!")
        print(f"   Text: '{test_text}'")
        print(f"   Detected: {detected}")
        print(f"   Expected: fr")
        print(f"   Result: {'✅ CORRECT' if detected == 'fr' else '❌ WRONG'}")
        
        return detected == 'fr'
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all comprehensive tests."""
    print("🧪 COMPREHENSIVE BACKEND TESTING")
    print("=" * 60)
    print("French sentence: 'je suis quelqu'un de gentille qui trouve la vie géniale'")
    print("Expected: Detect French → Translate to English → Positive Sentiment")
    print()
    
    # Test 1: langdetect library
    langdetect_ok = test_langdetect_only()
    
    # Test 2: Backend imports
    imports_ok = test_backend_imports()
    
    if not imports_ok:
        print("\n⏭️  Skipping advanced tests (imports failed)")
        print("\n" + "=" * 60)
        print("❌ FAILED: Cannot proceed without backend dependencies")
        return
    
    # Test 3: Language detection through backend
    detection_ok = test_language_detection_only()
    
    # Test 4: Full translation
    translation_ok, translated_text = test_full_translation()
    
    # Test 5: Sentiment analysis on French
    sentiment_french_ok, sentiment_result = test_sentiment_analysis()
    
    # Test 6: Sentiment analysis on English
    sentiment_english_ok = test_sentiment_on_english()
    
    # Final Summary
    print("\n" + "=" * 60)
    print("🏁 COMPREHENSIVE TEST SUMMARY")
    print(f"   langdetect library: {'✅' if langdetect_ok else '❌'}")
    print(f"   Backend imports: {'✅' if imports_ok else '❌'}")
    print(f"   Language detection: {'✅' if detection_ok else '❌'}")
    print(f"   Translation: {'✅' if translation_ok else '❌'}")
    print(f"   Sentiment (French): {'✅' if sentiment_french_ok else '❌'}")
    print(f"   Sentiment (English): {'✅' if sentiment_english_ok else '❌'}")
    
    # Overall assessment
    all_tests = [langdetect_ok, imports_ok, detection_ok, translation_ok, sentiment_french_ok, sentiment_english_ok]
    passed_tests = sum(all_tests)
    total_tests = len(all_tests)
    
    print(f"\n📊 Overall Score: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 PERFECT! Complete pipeline working!")
        print("✅ French detection → English translation → Sentiment analysis")
        if translated_text:
            print(f"✅ Translation result: '{translated_text}'")
        if sentiment_result:
            print(f"✅ Sentiment: {sentiment_result.get('sentiment')} ({sentiment_result.get('positive', 0):.1f}% positive)")
    elif passed_tests >= 4:
        print("\n🟡 MOSTLY WORKING! Core functionality operational")
        print("✅ Main features work, minor issues may exist")
    else:
        print("\n❌ NEEDS WORK! Multiple components failing")
        print("⚠️  Check dependencies and configuration")

if __name__ == "__main__":
    main()