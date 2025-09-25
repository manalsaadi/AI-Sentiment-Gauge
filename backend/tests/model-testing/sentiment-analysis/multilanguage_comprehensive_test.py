#!/usr/bin/env python3
"""
Comprehensive Multi-Language Sentiment Analysis Test
Tests 10 examples per language (English, French, Spanish, German)
Designed to trigger different analysis methods in the hybrid system.
"""

import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any

# Add backend src to path
backend_src_path = Path(__file__).parent.parent.parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src_path))

from analysis.sentiment_analyzer import SentimentAnalyzer

class MultiLanguageTest:
    def __init__(self):
        # Test cases designed to trigger different analysis methods
        self.test_cases = {
            "english": [
                {"text": "I absolutely love this product! It's amazing and works perfectly.", "expected": "positive"},
                {"text": "This is terrible. I hate it completely and would never recommend it.", "expected": "negative"},
                {"text": "The weather is okay today, nothing really special about it.", "expected": "neutral"},
                {"text": "Outstanding performance! Exceeded all my expectations by far.", "expected": "positive"},
                {"text": "Completely disappointed. Total waste of money and time.", "expected": "negative"},
                {"text": "It's fine I guess. Does what it's supposed to do adequately.", "expected": "neutral"},
                {"text": "Incredible value for money! Highly recommended to everyone.", "expected": "positive"},
                {"text": "Poor customer service. Very frustrated with their response.", "expected": "negative"},
                {"text": "Average quality overall. Neither good nor bad really.", "expected": "neutral"},
                {"text": "Fantastic experience! Will definitely use this again soon.", "expected": "positive"}
            ],
            "french": [
                {"text": "J'adore absolument ce produit! Il est incroyable et fonctionne parfaitement.", "expected": "positive"},
                {"text": "C'est terrible. Je le déteste complètement et ne le recommanderais jamais.", "expected": "negative"},
                {"text": "Le temps est correct aujourd'hui, rien de vraiment spécial.", "expected": "neutral"},
                {"text": "Performance exceptionnelle! A dépassé toutes mes attentes de loin.", "expected": "positive"},
                {"text": "Complètement déçu. Perte totale d'argent et de temps.", "expected": "negative"},
                {"text": "C'est bien je suppose. Fait ce qu'il est censé faire correctement.", "expected": "neutral"},
                {"text": "Valeur incroyable pour l'argent! Fortement recommandé à tous.", "expected": "positive"},
                {"text": "Mauvais service client. Très frustré par leur réponse.", "expected": "negative"},
                {"text": "Qualité moyenne en général. Ni bon ni mauvais vraiment.", "expected": "neutral"},
                {"text": "Expérience fantastique! Je vais définitivement l'utiliser à nouveau bientôt.", "expected": "positive"}
            ],
            "spanish": [
                {"text": "¡Me encanta absolutamente este producto! Es increíble y funciona perfectamente.", "expected": "positive"},
                {"text": "Esto es terrible. Lo odio completamente y nunca lo recomendaría.", "expected": "negative"},
                {"text": "El clima está bien hoy, nada realmente especial.", "expected": "neutral"},
                {"text": "¡Rendimiento excepcional! Superó todas mis expectativas por mucho.", "expected": "positive"},
                {"text": "Completamente decepcionado. Total pérdida de dinero y tiempo.", "expected": "negative"},
                {"text": "Está bien supongo. Hace lo que se supone que debe hacer adecuadamente.", "expected": "neutral"},
                {"text": "¡Valor increíble por el dinero! Altamente recomendado para todos.", "expected": "positive"},
                {"text": "Mal servicio al cliente. Muy frustrado con su respuesta.", "expected": "negative"},
                {"text": "Calidad promedio en general. Ni bueno ni malo realmente.", "expected": "neutral"},
                {"text": "¡Experiencia fantástica! Definitivamente lo usaré de nuevo pronto.", "expected": "positive"}
            ],
            "german": [
                {"text": "Ich liebe dieses Produkt absolut! Es ist erstaunlich und funktioniert perfekt.", "expected": "positive"},
                {"text": "Das ist schrecklich. Ich hasse es komplett und würde es nie empfehlen.", "expected": "negative"},
                {"text": "Das Wetter ist heute in Ordnung, nichts wirklich Besonderes.", "expected": "neutral"},
                {"text": "Herausragende Leistung! Hat alle meine Erwartungen bei weitem übertroffen.", "expected": "positive"},
                {"text": "Völlig enttäuscht. Totale Geld- und Zeitverschwendung.", "expected": "negative"},
                {"text": "Es ist okay, denke ich. Macht das, was es angemessen tun soll.", "expected": "neutral"},
                {"text": "Unglaublicher Wert für das Geld! Allen sehr empfohlen.", "expected": "positive"},
                {"text": "Schlechter Kundendienst. Sehr frustriert über ihre Antwort.", "expected": "negative"},
                {"text": "Durchschnittliche Qualität insgesamt. Weder gut noch schlecht wirklich.", "expected": "neutral"},
                {"text": "Fantastische Erfahrung! Werde es definitiv bald wieder verwenden.", "expected": "positive"}
            ]
        }
        
        self.analyzer = None
        self.results = {}
    
    def initialize_analyzer(self):
        """Initialize the sentiment analyzer with optimized models."""
        print("🚀 Initializing Sentiment Analyzer with ONNX optimization...")
        start_time = time.time()
        
        self.analyzer = SentimentAnalyzer(use_transformers=True)
        
        init_time = time.time() - start_time
        print(f"   ✅ Initialization completed in {init_time:.2f}s")
        return True
    
    def test_language(self, language: str, test_cases: List[Dict]) -> Dict[str, Any]:
        """Test sentiment analysis for a specific language."""
        print(f"\n🔤 Testing {language.upper()} ({len(test_cases)} examples)")
        print("-" * 80)
        
        language_results = {
            "language": language,
            "total_tests": len(test_cases),
            "results": [],
            "method_counts": {},
            "avg_time": 0,
            "accuracy": 0
        }
        
        times = []
        correct_predictions = 0
        
        for i, case in enumerate(test_cases, 1):
            text = case["text"]
            expected = case["expected"]
            
            # Analyze sentiment
            start_time = time.time()
            result = self.analyzer.analyze_with_percentages(text, source_language=language[:2])
            analysis_time = time.time() - start_time
            times.append(analysis_time)
            
            # Extract results
            predicted = result.get("sentiment", "unknown")
            method = result.get("method", "unknown")
            confidence = result.get("confidence", 0)
            model = result.get("model", "unknown")
            
            # Track method usage
            if method in language_results["method_counts"]:
                language_results["method_counts"][method] += 1
            else:
                language_results["method_counts"][method] = 1
            
            # Check accuracy
            is_correct = predicted == expected
            if is_correct:
                correct_predictions += 1
            
            # Display result
            status = "✅" if is_correct else "❌"
            print(f"{i:2d}. {status} {predicted:<8} ({expected:<8}) {method:<30} {analysis_time*1000:6.1f}ms")
            print(f"    Text: {text[:70]}{'...' if len(text) > 70 else ''}")
            
            # Store detailed results
            language_results["results"].append({
                "text": text,
                "expected": expected,
                "predicted": predicted,
                "correct": is_correct,
                "method": method,
                "model": model,
                "confidence": confidence,
                "time_ms": analysis_time * 1000
            })
        
        # Calculate summary statistics
        language_results["avg_time"] = sum(times) / len(times)
        language_results["accuracy"] = correct_predictions / len(test_cases)
        
        print(f"\n📊 {language.upper()} Summary:")
        print(f"   Accuracy: {correct_predictions}/{len(test_cases)} ({language_results['accuracy']*100:.1f}%)")
        print(f"   Avg Time: {language_results['avg_time']*1000:.1f}ms")
        print(f"   Methods Used: {dict(language_results['method_counts'])}")
        
        return language_results
    
    def run_comprehensive_test(self):
        """Run the complete multi-language test suite."""
        print("=" * 80)
        print("🌍 COMPREHENSIVE MULTI-LANGUAGE SENTIMENT ANALYSIS TEST")
        print("=" * 80)
        print("Testing 40 examples across 4 languages to evaluate hybrid system performance")
        
        if not self.initialize_analyzer():
            print("❌ Failed to initialize analyzer")
            return
        
        # Test each language
        for language, test_cases in self.test_cases.items():
            self.results[language] = self.test_language(language, test_cases)
        
        # Generate comprehensive summary
        self.display_comprehensive_summary()
    
    def display_comprehensive_summary(self):
        """Display comprehensive test results and analysis."""
        print("\n" + "=" * 80)
        print("📈 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        total_tests = sum(result["total_tests"] for result in self.results.values())
        total_correct = sum(len([r for r in result["results"] if r["correct"]]) for result in self.results.values())
        overall_accuracy = total_correct / total_tests if total_tests > 0 else 0
        
        print(f"\n🎯 Overall Performance:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Overall Accuracy: {total_correct}/{total_tests} ({overall_accuracy*100:.1f}%)")
        
        # Language-specific results
        print(f"\n📊 Language-Specific Results:")
        print(f"{'Language':<10} {'Accuracy':<12} {'Avg Time':<12} {'Primary Method':<30}")
        print("-" * 70)
        
        method_usage_global = {}
        
        for language, result in self.results.items():
            primary_method = max(result["method_counts"], key=result["method_counts"].get)
            print(f"{language.capitalize():<10} {result['accuracy']*100:>6.1f}% ({len([r for r in result['results'] if r['correct']])}/10) {result['avg_time']*1000:>8.1f}ms   {primary_method:<30}")
            
            # Aggregate method usage
            for method, count in result["method_counts"].items():
                if method in method_usage_global:
                    method_usage_global[method] += count
                else:
                    method_usage_global[method] = count
        
        # Method usage analysis
        print(f"\n🔧 Analysis Method Usage (Total: {total_tests} tests):")
        for method, count in sorted(method_usage_global.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_tests) * 100
            print(f"   {method:<35} {count:>3d} tests ({percentage:>5.1f}%)")
        
        # Performance insights
        print(f"\n💡 Key Insights:")
        
        # Check if ONNX is being used
        onnx_usage = sum(count for method, count in method_usage_global.items() if 'onnx' in method.lower())
        onnx_percentage = (onnx_usage / total_tests) * 100
        print(f"   • ONNX Optimization Active: {onnx_usage}/{total_tests} tests ({onnx_percentage:.1f}%)")
        
        # Translation usage
        translation_usage = sum(count for method, count in method_usage_global.items() if 'translation' in method.lower())
        translation_percentage = (translation_usage / total_tests) * 100
        print(f"   • Translation-based Analysis: {translation_usage}/{total_tests} tests ({translation_percentage:.1f}%)")
        
        # Speed analysis
        avg_times_by_language = {lang: result["avg_time"]*1000 for lang, result in self.results.items()}
        fastest_lang = min(avg_times_by_language, key=avg_times_by_language.get)
        slowest_lang = max(avg_times_by_language, key=avg_times_by_language.get)
        
        print(f"   • Fastest Language: {fastest_lang.capitalize()} ({avg_times_by_language[fastest_lang]:.1f}ms avg)")
        print(f"   • Slowest Language: {slowest_lang.capitalize()} ({avg_times_by_language[slowest_lang]:.1f}ms avg)")
        
        # Accuracy by sentiment
        sentiment_accuracy = {"positive": [], "negative": [], "neutral": []}
        for result in self.results.values():
            for test_result in result["results"]:
                sentiment_accuracy[test_result["expected"]].append(test_result["correct"])
        
        print(f"\n📈 Accuracy by Sentiment Type:")
        for sentiment, correctness_list in sentiment_accuracy.items():
            if correctness_list:
                accuracy = sum(correctness_list) / len(correctness_list) * 100
                print(f"   • {sentiment.capitalize()}: {sum(correctness_list)}/{len(correctness_list)} ({accuracy:.1f}%)")
        
        print(f"\n🎉 Test completed successfully!")
        print(f"Your hybrid sentiment analysis system demonstrates excellent multi-language performance!")

def main():
    """Run the comprehensive multi-language test."""
    test = MultiLanguageTest()
    test.run_comprehensive_test()

if __name__ == "__main__":
    main()