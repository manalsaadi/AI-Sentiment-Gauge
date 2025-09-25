#!/usr/bin/env python3
"""
Test pour identifier la source du problème de boucle infinie.
"""

def test_imports():
    """Test les imports pour voir s'il y a un problème."""
    
    print("=== TEST DES IMPORTS ===")
    
    try:
        print("1. Test langdetect...")
        from langdetect import detect
        text = "hello world"
        result = detect(text)
        print(f"   ✅ langdetect OK: {result}")
    except Exception as e:
        print(f"   ❌ langdetect FAIL: {e}")
    
    try:
        print("2. Test import backend modules...")
        import sys
        import os
        backend_src = os.path.join(os.path.dirname(__file__), 'backend', 'src')
        sys.path.insert(0, backend_src)
        
        print("   2a. Import marian_quantized...")
        from translation.marian_quantized import MarianQuantizedTranslator
        print("   ✅ marian_quantized OK")
        
        print("   2b. Test création MarianQuantizedTranslator...")
        # NE PAS créer l'instance pour éviter le chargement de modèles
        print("   ✅ Prêt pour création (pas créé)")
        
    except Exception as e:
        print(f"   ❌ Backend imports FAIL: {e}")
        import traceback
        traceback.print_exc()

def test_langdetect_problem():
    """Test si langdetect cause le problème."""
    
    print("\n=== TEST LANGDETECT EN ISOLATION ===")
    
    test_texts = [
        "hello world",
        "je suis quelqu'un de gentille qui trouve la vie géniale",
        "hola mundo",
        "hallo welt"
    ]
    
    try:
        from langdetect import detect, detect_langs
        
        for text in test_texts:
            print(f"Testing: '{text[:30]}...'")
            try:
                # Test avec timeout implicite
                result = detect(text)
                probs = detect_langs(text)
                print(f"   ✅ Detected: {result} (probs: {len(probs)})")
            except Exception as e:
                print(f"   ❌ FAILED on this text: {e}")
                
    except ImportError:
        print("❌ langdetect not available")

def test_simple_detection():
    """Test la détection simple sans langdetect."""
    
    print("\n=== TEST DÉTECTION SIMPLE ===")
    
    text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    text_lower = text.lower()
    
    print(f"Text: {text}")
    
    # Test pattern simple
    french_patterns = ['je suis', 'géniale', 'gentille', 'trouve', 'la vie']
    spanish_patterns = ['yo soy', 'hola', 'muy', 'para', 'con']
    
    french_score = sum(1 for pattern in french_patterns if pattern in text_lower)
    spanish_score = sum(1 for pattern in spanish_patterns if pattern in text_lower)
    
    print(f"French score: {french_score}")
    print(f"Spanish score: {spanish_score}")
    print(f"Should detect: {'French' if french_score > spanish_score else 'Spanish'}")

if __name__ == "__main__":
    test_imports()
    test_langdetect_problem()
    test_simple_detection()
    print("\n=== DIAGNOSTIC TERMINÉ ===")
    print("Si ça s'affiche, il n'y a pas de boucle infinie dans ce test !")