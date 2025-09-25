#!/usr/bin/env python3
"""
Quick test of langdetect with the French sentence
"""

def test_langdetect_simple():
    """Simple test of langdetect library."""
    
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    print("🔍 QUICK LANGDETECT TEST")
    print("=" * 30)
    print(f"Text: '{test_text}'")
    print()
    
    try:
        from langdetect import detect, detect_langs
        
        # Simple detection
        detected = detect(test_text)
        print(f"Detected language: {detected}")
        
        # Detailed probabilities
        probs = detect_langs(test_text)
        print("Language probabilities:")
        for prob in probs:
            print(f"   {prob.lang}: {prob.prob:.4f}")
        
        print()
        print(f"Result: {'✅ CORRECT' if detected == 'fr' else '❌ INCORRECT'}")
        print("Expected: fr (French)")
        
        if detected == 'fr':
            print("🎉 French detection is working perfectly!")
        else:
            print("⚠️  There might be an issue with the text or langdetect")
            
    except ImportError:
        print("❌ langdetect not installed")
        print("Run: pip install langdetect")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_langdetect_simple()