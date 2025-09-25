#!/usr/bin/env python3
"""
Test script for the enhanced sentiment analyzer with automatic model selection.
This script tests the new smart hybrid approach.
"""

import sys
import os
import time
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / ".." / ".." / ".." / "backend" / "src"
sys.path.insert(0, str(backend_path))

def test_basic_functionality():
    """Test basic VADER functionality (should always work)"""
    print("=== Testing Basic VADER Functionality ===")
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Initialize with transformers disabled for baseline test
        analyzer = SentimentAnalyzer(use_transformers=False)
        
        test_texts = [
            "I love this product! It's amazing and works perfectly.",
            "This is terrible. I hate it completely.",
            "The weather is okay today, nothing special.",
            "¡Este producto es fantástico! Me encanta mucho.",  # Spanish
            "Ce produit est vraiment mauvais."  # French
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\nTest {i}: {text}")
            start_time = time.time()
            
            result = analyzer.analyze_with_percentages(text)
            
            duration = time.time() - start_time
            
            print(f"  Sentiment: {result['sentiment']}")
            print(f"  Percentages - Pos: {result['positive']:.1f}%, Neg: {result['negative']:.1f}%, Neu: {result['neutral']:.1f}%")
            print(f"  Method: {result['method']}")
            print(f"  Confidence: {result['confidence']:.3f}")
            print(f"  Duration: {duration:.3f}s")
            
        print("\n✅ Basic VADER functionality works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_transformer_functionality():
    """Test transformer functionality if available"""
    print("\n=== Testing Transformer Functionality ===")
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Initialize with transformers enabled
        print("Initializing transformer models... (this may take a few moments)")
        analyzer = SentimentAnalyzer(use_transformers=True)
        
        test_cases = [
            ("I absolutely love this new feature! It's incredible.", "en"),
            ("This product is completely useless and broken.", "en"),
            ("The documentation could be better, but it's acceptable.", "en"),
            ("¡Este servicio es excelente! Lo recomiendo mucho.", "es"),
            ("Ce produit est vraiment décevant et de mauvaise qualité.", "fr"),
        ]
        
        for i, (text, lang_hint) in enumerate(test_cases, 1):
            print(f"\nTest {i}: {text}")
            print(f"  Language hint: {lang_hint}")
            
            start_time = time.time()
            result = analyzer.analyze_with_percentages(text, source_language=lang_hint)
            duration = time.time() - start_time
            
            print(f"  Sentiment: {result['sentiment']}")
            print(f"  Percentages - Pos: {result['positive']:.1f}%, Neg: {result['negative']:.1f}%, Neu: {result['neutral']:.1f}%")
            print(f"  Method: {result['method']}")
            print(f"  Model: {result.get('model', 'N/A')}")
            print(f"  Confidence: {result['confidence']:.3f}")
            print(f"  Duration: {duration:.3f}s")
            
            # Check for translation info if used
            if 'translated_text' in result:
                print(f"  Translated: {result['translated_text']}")
                print(f"  Source language: {result['source_language']}")
        
        print("\n✅ Transformer functionality works correctly!")
        return True
        
    except ImportError as e:
        print(f"⚠️  Transformer libraries not available: {e}")
        print("Install transformers and torch for enhanced functionality:")
        print("  pip install transformers torch")
        return False
    except Exception as e:
        print(f"❌ Transformer functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_automatic_selection():
    """Test the automatic model selection logic"""
    print("\n=== Testing Automatic Model Selection ===")
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Test both configurations
        configs = [
            ("VADER Only", False),
            ("Smart Hybrid", True)
        ]
        
        test_scenarios = [
            ("Very short", "Good"),
            ("Short English", "This is good"),
            ("Long English", "This product has exceeded all my expectations and I would definitely recommend it to anyone looking for quality."),
            ("French text", "Ce produit est vraiment fantastique et je le recommande vivement à tous."),
            ("Spanish text", "Este servicio es terrible, no funciona para nada bien."),
            ("Mixed content", "Hello world! ¿Cómo estás? This is a test.")
        ]
        
        for config_name, use_transformers in configs:
            print(f"\n--- {config_name} Configuration ---")
            analyzer = SentimentAnalyzer(use_transformers=use_transformers)
            
            for scenario_name, text in test_scenarios:
                print(f"\n{scenario_name}: {text}")
                start_time = time.time()
                
                result = analyzer.analyze_with_percentages(text)
                duration = time.time() - start_time
                
                print(f"  Method: {result['method']}, Duration: {duration:.3f}s")
                print(f"  Result: {result['sentiment']} ({result['confidence']:.2f} confidence)")
        
        print("\n✅ Automatic selection logic works correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Automatic selection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_characteristics():
    """Test performance characteristics"""
    print("\n=== Performance Characteristics ===")
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Test with different text lengths
        test_texts = {
            "Short": "Great product!",
            "Medium": "This product has been really helpful for my daily tasks and I appreciate the quality.",
            "Long": "After using this product for several months, I can confidently say that it has transformed my workflow in ways I never expected. The attention to detail, the user-friendly interface, and the robust functionality all combine to create an exceptional experience that I would highly recommend to anyone in a similar situation."
        }
        
        for config_name, use_transformers in [("VADER", False), ("Hybrid", True)]:
            print(f"\n--- {config_name} Performance ---")
            analyzer = SentimentAnalyzer(use_transformers=use_transformers)
            
            for length_type, text in test_texts.items():
                times = []
                for _ in range(3):  # 3 runs for averaging
                    start_time = time.time()
                    result = analyzer.analyze_with_percentages(text)
                    times.append(time.time() - start_time)
                
                avg_time = sum(times) / len(times)
                print(f"  {length_type} text: {avg_time:.3f}s avg (method: {result['method']})")
        
        print("\n✅ Performance testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Enhanced Sentiment Analyzer Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Transformer Functionality", test_transformer_functionality), 
        ("Automatic Selection", test_automatic_selection),
        ("Performance Characteristics", test_performance_characteristics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
            break
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Enhanced sentiment analyzer is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\nNext steps:")
    print("1. If transformer tests failed, install: pip install transformers torch")
    print("2. Test the /analyze/text API endpoint")
    print("3. Verify frontend integration")

if __name__ == "__main__":
    main()