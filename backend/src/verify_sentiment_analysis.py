#!/usr/bin/env python3
"""
Quick ONNX integration test from backend/src directory.
"""
import sys
from pathlib import Path

# Add backend src to path
backend_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(backend_src_path))


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
    print(f"{'Text':<35} {'Sentiment':<10} {'Method':<30} {'Time'}")
    print("-" * 85)
    
    for text, lang in tests:
        start_time = time.time()
        result = analyzer.analyze_with_percentages(text, source_language=lang)
        duration = time.time() - start_time
        
        sentiment = result.get("sentiment", "unknown")
        method = result.get("method", "unknown")
        
        print(f"{text[:34]:<35} {sentiment:<10} {method:<30} {duration*1000:.1f}ms")
        
        if "onnx" in method.lower():
            print(f"   🚀 ONNX Active! Model: {result.get('model', 'unknown')}")
        
    print("\n✅ Integration test completed!")

if __name__ == "__main__":
    # This is a simplified path correction for running the script directly
    # In a real app, this would be handled by the application's entry point
    current_dir = Path(__file__).parent
    if current_dir.name == 'src':
         # If running from backend/src, we need to adjust the path for model cache
         import os
         os.chdir(current_dir.parent.parent) # Go up to project root
         print(f"Changed directory to: {os.getcwd()}")


    test_onnx()