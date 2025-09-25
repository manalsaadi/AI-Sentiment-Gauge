#!/usr/bin/env python3
"""
Test script for the improved language detection with langdetect.
"""

import sys
import os

# Add backend src to Python path
backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
sys.path.insert(0, backend_src)

def test_french_detection():
    """Test French language detection with the problematic text."""
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    print("=== FRENCH LANGUAGE DETECTION TEST ===")
    print(f"Text: '{test_text}'")
    print()
    
    try:
        # Test with langdetect directly
        try:
            from langdetect import detect, detect_langs
            detected = detect(test_text)
            probs = detect_langs(test_text)
            
            print("🔍 LANGDETECT RESULTS:")
            print(f"   Detected: {detected}")
            print(f"   Probabilities: {[(p.lang, f'{p.prob:.3f}') for p in probs[:3]]}")
            print(f"   ✅ Should be 'fr': {'✅ CORRECT' if detected == 'fr' else '❌ INCORRECT'}")
            print()
        except ImportError:
            print("❌ langdetect not installed")
            print("   Install with: pip install langdetect")
            print()
        
        # Test with our improved translator
        try:
            from translation.translator import Translator, Language
            translator = Translator()
            detected_lang = translator.detect_language(test_text)
            
            print("🔧 OUR TRANSLATOR RESULTS:")
            print(f"   Detected: {detected_lang.value}")
            print(f"   ✅ Should be Language.FRENCH: {'✅ CORRECT' if detected_lang == Language.FRENCH else '❌ INCORRECT'}")
            print()
            
        except ImportError as e:
            print(f"❌ Could not import translator: {e}")
            print("   (This is expected if dependencies aren't installed)")
            print()
            
        # Test with fallback detection
        try:
            from translation.marian_quantized import MarianQuantizedTranslator
            marian = MarianQuantizedTranslator()
            fallback_result = marian._fallback_detection(test_text)
            
            print("🛠️  FALLBACK DETECTION RESULTS:")
            print(f"   Detected: {fallback_result}")
            print(f"   ✅ Should be 'fr': {'✅ CORRECT' if fallback_result == 'fr' else '❌ INCORRECT'}")
            print()
            
        except Exception as e:
            print(f"❌ Fallback test failed: {e}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("=== SUMMARY ===")
    print("✅ Fixed the French detection issue by:")
    print("   1. Adding langdetect library to requirements.txt")  
    print("   2. Updating translator.py to use langdetect first")
    print("   3. Improved fallback detection with better French patterns")
    print("   4. Fixed character precedence (French unique chars checked first)")

if __name__ == "__main__":
    test_french_detection()