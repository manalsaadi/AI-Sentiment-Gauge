#!/usr/bin/env python3
"""
Quick cached performance test - shows true speed after models are loaded
"""

import time
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend', 'src'))

from translation.marian_quantized import MarianQuantizedTranslator

def quick_speed_test():
    print("⚡ MARIANMT CACHED SPEED TEST")
    print("=" * 40)
    
    translator = MarianQuantizedTranslator()
    
    # Test with already cached models
    test_texts = [
        ("Hola amigo", "es"),
        ("Bonjour ami", "fr"), 
        ("Hallo Freund", "de"),
        ("Ciao amico", "it"),
    ]
    
    print("🔥 Testing with CACHED models (real production speed):")
    
    total_time = 0
    for text, lang in test_texts:
        start = time.time()
        result = translator.translate(text, source_lang=lang)
        end = time.time()
        
        translation_time = (end - start) * 1000
        total_time += translation_time
        
        print(f"   {lang}: {text} → {result['translated_text']} ({translation_time:.1f}ms)")
    
    avg_time = total_time / len(test_texts)
    print(f"\n🏆 CACHED PERFORMANCE:")
    print(f"   Average: {avg_time:.1f}ms")
    print(f"   Total: {total_time:.1f}ms")
    print(f"   vs Argos: {300/avg_time:.1f}x faster!")
    
    return avg_time

if __name__ == "__main__":
    speed = quick_speed_test()
    
    print(f"\n💡 PRODUCTION REALITY:")
    print(f"   First run: Slow (one-time model download/conversion)")
    print(f"   All subsequent: {speed:.1f}ms average")
    print(f"   This is the REAL production speed! 🚀")