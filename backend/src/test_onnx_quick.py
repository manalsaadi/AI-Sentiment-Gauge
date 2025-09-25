#!/usr/bin/env python3
"""
Quick ONNX integration test from backend/src directory.
"""

from analysis.sentiment_analyzer import SentimentAnalyzer
import time

def test_onnx():
    print("🧪 Testing ONNX Integration in Production Sentiment Analyzer")
    print("=" * 60)
    
    # Initialize analyzer
    print("\n1️⃣ Initializing analyzer...")
    analyzer = SentimentAnalyzer(use_transformers=True)
    
    # Test cases
    tests = [
        ("I absolutely love this product!", "en"),
        ("This is terrible and disappointing.", "en"),
        ("¡Este producto es fantástico!", "es"),
        ("C'est vraiment mauvais.", "fr")
    ]
    
    print("\n2️⃣ Running tests...")
    print(f"{'Text':<35} {'Sentiment':<10} {'Method':<25} {'Time'}")
    print("-" * 80)
    
    for text, lang in tests:
        start_time = time.time()
        result = analyzer.analyze_with_percentages(text, source_language=lang)
        duration = time.time() - start_time
        
        sentiment = result.get("sentiment", "unknown")
        method = result.get("method", "unknown")
        
        print(f"{text[:34]:<35} {sentiment:<10} {method:<25} {duration*1000:.1f}ms")
        
        if "onnx" in method.lower():
            print(f"   🚀 ONNX Active! Model: {result.get('model', 'unknown')}")
        
    print("\n✅ Integration test completed!")

if __name__ == "__main__":
    test_onnx()