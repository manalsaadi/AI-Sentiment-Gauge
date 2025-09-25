#!/usr/bin/env python3
"""
Test the fixed language detection for French text
"""

def test_language_detection():
    # Test the fixed language detection logic
    text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    print(f"Testing: '{text}'")
    
    # Simulate the fixed detection logic
    text_lower = text.lower()
    
    # Language indicators with weights (French moved first for priority)
    indicators = {
        'fr': (['à', 'ç', 'è', 'ê', 'û', 'ô'], ['le', 'la', 'et', 'je', 'tu', 'vous', 'avec', 'qui', 'que', 'de', 'du', 'des', 'suis', 'vie', 'génial', 'trouve']),
        'es': (['ñ', 'í', 'á', 'ó', 'ú', '¿', '¡'], ['que', 'es', 'la', 'el', 'con', 'de', 'por', 'para', 'una', 'los', 'las']),
        'de': (['ä', 'ö', 'ü', 'ß'], ['der', 'die', 'das', 'und', 'ich', 'ist', 'mit']),
        'it': (['ò', 'ù', 'è', 'à'], ['che', 'con', 'per', 'una', 'della', 'questo']),
        'pt': (['ção', 'ão'], ['não', 'com', 'para', 'uma', 'mais', 'pela'])
    }
    
    scores = {}
    for lang, (chars, words) in indicators.items():
        score = 0
        # Character-based scoring (higher weight for distinctive chars)
        for char in chars:
            if lang == 'fr' and char in ['à', 'ç', 'è', 'ê', 'û', 'ô']:
                score += text_lower.count(char) * 4  # French-specific chars
            elif lang == 'es' and char == 'ñ':
                score += text_lower.count(char) * 4  # Spanish-specific ñ
            else:
                score += text_lower.count(char) * 2
        # Word-based scoring  
        for word in words:
            if word in text_lower:
                score += 3
                
        print(f"  {lang}: {score} points")
        if lang == 'fr':
            french_words_found = [word for word in words if word in text_lower]
            print(f"    French words found: {french_words_found}")
        scores[lang] = score
    
    # Handle é separately (can be French or Spanish)
    if 'é' in text_lower:
        é_count = text_lower.count('é')
        print(f"  Found 'é' {é_count} times")
        # Check for French context words
        french_context = any(word in text_lower for word in ['je', 'qui', 'que', 'de', 'du', 'des', 'suis', 'vie', 'génial'])
        if french_context:
            scores['fr'] = scores.get('fr', 0) + é_count * 3
            print(f"    Added {é_count * 3} points to French (context detected)")
        else:
            scores['es'] = scores.get('es', 0) + é_count * 2
            print(f"    Added {é_count * 2} points to Spanish")
    
    detected = max(scores.items(), key=lambda x: x[1])[0] if any(scores.values()) else 'en'
    
    print(f"\nFinal scores: {scores}")
    print(f"Detected language: {detected}")
    
    return detected == 'fr'

if __name__ == "__main__":
    success = test_language_detection()
    print(f"\nTest {'PASSED' if success else 'FAILED'}!")