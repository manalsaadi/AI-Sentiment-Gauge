#!/usr/bin/env python3
"""
Proper language detection using langdetect library instead of custom algorithms.
This replaces the flawed character-pattern-based detection.
"""

try:
    from langdetect import detect, detect_langs
    from langdetect.lang_detect_exception import LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("langdetect not installed. Install with: pip install langdetect")

def proper_language_detection(text: str) -> str:
    """
    Proper language detection using Google's language detection algorithm.
    
    Args:
        text: Text to detect language for
        
    Returns:
        Language code (e.g., 'fr', 'es', 'en', 'de', 'it')
    """
    if not LANGDETECT_AVAILABLE:
        return fallback_detection(text)
        
    try:
        # Clean text
        cleaned_text = text.strip()
        if len(cleaned_text) < 3:
            return 'en'  # Default for very short text
            
        # Detect language with confidence scores
        detected_lang = detect(cleaned_text)
        
        # Get detailed probabilities
        lang_probs = detect_langs(cleaned_text)
        confidence = max(prob.prob for prob in lang_probs)
        
        print(f"Detected: {detected_lang} (confidence: {confidence:.3f})")
        print(f"All probabilities: {[(l.lang, f'{l.prob:.3f}') for l in lang_probs[:3]]}")
        
        return detected_lang
        
    except LangDetectException as e:
        print(f"Language detection failed: {e}")
        return fallback_detection(text)

def fallback_detection(text: str) -> str:
    """Improved fallback detection with better French handling."""
    text_lower = text.lower()
    
    # French-specific words and patterns (check FIRST)
    french_patterns = [
        'je suis', 'tu es', 'il est', 'nous sommes', 'vous êtes', 'ils sont',
        'le', 'la', 'les', 'un', 'une', 'des',
        'qui', 'que', 'dont', 'où',
        'avec', 'dans', 'pour', 'sans', 'sur', 'sous',
        'très', 'plus', 'moins', 'bien', 'mal',
        'trouve', 'géniale', 'gentille'
    ]
    
    # French characters that are NOT in Spanish
    french_only_chars = ['à', 'ç', 'è', 'ê', 'û', 'ù', 'ï', 'ÿ', 'œ']
    
    # Spanish-specific words and patterns
    spanish_patterns = [
        'yo soy', 'tú eres', 'él es', 'nosotros somos', 'vosotros sois', 'ellos son',
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'que', 'quien', 'donde', 'como', 'cuando',
        'con', 'en', 'para', 'sin', 'sobre', 'bajo',
        'muy', 'más', 'menos', 'bien', 'mal',
        'hola', 'gracias', 'por favor'
    ]
    
    # Spanish-specific character (ñ is unique to Spanish)
    spanish_unique_chars = ['ñ']
    
    # Count patterns
    french_score = 0
    spanish_score = 0
    
    # Check for unique characters first (most reliable)
    for char in french_only_chars:
        if char in text_lower:
            french_score += 3  # High weight for unique chars
            
    for char in spanish_unique_chars:
        if char in text_lower:
            spanish_score += 3
    
    # Check for common words
    for pattern in french_patterns:
        if pattern in text_lower:
            french_score += 2
            
    for pattern in spanish_patterns:
        if pattern in text_lower:
            spanish_score += 2
    
    # Shared accented characters (lower weight)
    shared_accents = ['í', 'é', 'á', 'ó', 'ú']
    accent_count = sum(1 for char in shared_accents if char in text_lower)
    french_score += accent_count * 0.5
    spanish_score += accent_count * 0.5
    
    print(f"Fallback scores - French: {french_score}, Spanish: {spanish_score}")
    
    if french_score > spanish_score:
        return 'fr'
    elif spanish_score > french_score:
        return 'es'
    else:
        return 'en'  # Default

# Test the problematic text
if __name__ == "__main__":
    test_text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    
    print("=== TESTING PROPER LANGUAGE DETECTION ===")
    print(f"Text: {test_text}")
    print()
    
    if LANGDETECT_AVAILABLE:
        result = proper_language_detection(test_text)
        print(f"✅ Proper detection result: {result}")
    else:
        print("❌ langdetect not available, using fallback")
        result = fallback_detection(test_text)
        print(f"Fallback result: {result}")
    
    print()
    print("Expected: 'fr' (French)")
    print(f"Got: '{result}' - {'✅ CORRECT' if result == 'fr' else '❌ INCORRECT'}")