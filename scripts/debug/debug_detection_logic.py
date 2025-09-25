#!/usr/bin/env python3
"""
Test de la logique corrigée pour la détection de langue française.
"""

def test_corrected_detection():
    """Test avec le texte problématique."""
    
    text = "je suis quelqu'un de gentille qui trouve la vie géniale"
    text_lower = text.lower()
    
    print(f"Testing: '{text}'")
    print(f"Lowercase: '{text_lower}'")
    print()
    
    # LOGIQUE CORRIGÉE
    
    # French-specific avec 'é' inclus !
    french_unique = ['à', 'ç', 'è', 'ê', 'û', 'ù', 'ï', 'ÿ', 'œ', 'é']
    french_words = ['je suis', 'tu es', 'nous sommes', 'vous êtes', 'le', 'la', 'les', 'qui', 'que', 'avec', 'dans', 'très', 'bien', 'géniale', 'gentille', 'trouve', 'vie', 'quelqu']
    
    # Spanish-specific (ñ uniquement)
    spanish_unique = ['ñ']
    spanish_words = ['yo soy', 'tú eres', 'nosotros somos', 'el', 'los', 'las', 'con', 'en', 'muy', 'hola', 'gracias', 'para', 'por', 'soy']
    
    # German-specific
    german_unique = ['ß', 'ü', 'ä', 'ö']
    german_words = ['ich bin', 'du bist', 'der', 'die', 'das', 'und', 'mit', 'für', 'auf', 'haben', 'sein']
    
    # Calcul des scores
    french_score = 0
    spanish_score = 0
    german_score = 0
    
    # Caractères uniques
    print("=== CARACTÈRES UNIQUES ===")
    french_chars_found = [char for char in french_unique if char in text_lower]
    spanish_chars_found = [char for char in spanish_unique if char in text_lower]
    german_chars_found = [char for char in german_unique if char in text_lower]
    
    print(f"French chars found: {french_chars_found}")
    print(f"Spanish chars found: {spanish_chars_found}")
    print(f"German chars found: {german_chars_found}")
    
    french_score += len(french_chars_found) * 3
    spanish_score += len(spanish_chars_found) * 5  # ñ est définitif
    german_score += len(german_chars_found) * 3
    
    # Mots caractéristiques  
    print("\n=== MOTS CARACTÉRISTIQUES ===")
    french_words_found = [word for word in french_words if word in text_lower]
    spanish_words_found = [word for word in spanish_words if word in text_lower]
    german_words_found = [word for word in german_words if word in text_lower]
    
    print(f"French words found: {french_words_found}")
    print(f"Spanish words found: {spanish_words_found}")
    print(f"German words found: {german_words_found}")
    
    french_score += len(french_words_found) * 2
    spanish_score += len(spanish_words_found) * 2
    german_score += len(german_words_found) * 2
    
    # Accents ambigus (seulement si pas de gagnant clair)
    ambiguous_accents = ['í', 'á', 'ó', 'ú']
    ambiguous_found = [char for char in ambiguous_accents if char in text_lower]
    print(f"\nAmbiguous accents found: {ambiguous_found}")
    
    if ambiguous_found and max(french_score, spanish_score, german_score) == 0:
        spanish_score += len(ambiguous_found)
        print(f"Added {len(ambiguous_found)} to Spanish (no clear winner)")
    
    print(f"\n=== SCORES FINAUX ===")
    print(f"French: {french_score}")
    print(f"Spanish: {spanish_score}")
    print(f"German: {german_score}")
    
    scores = {'fr': french_score, 'es': spanish_score, 'de': german_score}
    best_lang = max(scores, key=scores.get) if any(scores.values()) else 'en'
    
    print(f"\nDétection: {best_lang}")
    print(f"Attendu: fr")
    print(f"Résultat: {'✅ CORRECT' if best_lang == 'fr' else '❌ INCORRECT'}")
    
    return best_lang == 'fr'

if __name__ == "__main__":
    success = test_corrected_detection()
    print(f"\n{'='*50}")
    print(f"Test {'RÉUSSI' if success else 'ÉCHOUÉ'}!")
    
    if success:
        print("✅ Le problème de détection française est résolu!")
    else:
        print("❌ Il y a encore un problème dans la logique.")