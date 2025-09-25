#!/usr/bin/env python3
"""
Quick test to debug transformer model outputs.
"""

import sys
import logging
from pathlib import Path

# Set up debug logging
logging.basicConfig(level=logging.DEBUG)

# Add backend to path
backend_path = Path(__file__).parent / "backend" / "src"
sys.path.insert(0, str(backend_path))

def test_transformer_debug():
    """Test transformer models with debug output."""
    print("🔍 Debugging Transformer Model Outputs")
    print("=" * 50)
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        # Initialize with transformers
        analyzer = SentimentAnalyzer(use_transformers=True)
        
        test_texts = [
            "I love this product!",
            "This is terrible.",
            "It's okay."
        ]
        
        for text in test_texts:
            print(f"\n📝 Testing: '{text}'")
            result = analyzer.analyze_with_percentages(text, source_language="en")
            
            print(f"  Result: {result['sentiment']}")
            print(f"  Method: {result.get('method', 'N/A')}")
            print(f"  Raw label: {result.get('raw_label', 'N/A')}")
            print(f"  Raw score: {result.get('raw_score', 'N/A')}")
            print(f"  Percentages: {result['positive']:.1f}% pos, {result['negative']:.1f}% neg, {result['neutral']:.1f}% neu")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_transformer_debug()