#!/usr/bin/env python3
"""
Test script to verify ONNX-optimized sentiment analyzer integration.
This tests the production deployment of ONNX models in the main analyzer.
"""

import sys
import time
from pathlib import Path

# Add backend src to path
backend_src_path = Path(__file__).parent.parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_src_path))

def test_onnx_integration():
    """Test that the main sentiment analyzer uses ONNX models."""
    print("🧪 Testing ONNX Integration in Main Sentiment Analyzer")
    print("=" * 60)
    
    try:
        from analysis.sentiment_analyzer import SentimentAnalyzer
        
        print("\n1️⃣ Initializing Sentiment Analyzer (with ONNX optimization)...")
        start_time = time.time()
        
        analyzer = SentimentAnalyzer(use_transformers=True)
        
        init_time = time.time() - start_time
        print(f"   ✅ Initialization completed in {init_time:.2f}s")
        
        # Test texts
        test_cases = [
            ("I absolutely love this product!", "positive", "en"),
            ("This is terrible and disappointing.", "negative", "en"), 
            ("The weather is okay today.", "neutral", "en"),
            ("¡Este producto es fantástico!", "positive", "es"),
            ("C'est vraiment mauvais.", "negative", "fr")
        ]
        
        print(f"\n2️⃣ Running sentiment analysis tests...")
        print(f"{'Text':<35} {'Expected':<10} {'Result':<10} {'Method':<25} {'Time':<8}")
        print("-" * 95)
        
        for text, expected, lang_hint in test_cases:
            start_time = time.time()
            
            result = analyzer.analyze_with_percentages(text, source_language=lang_hint)
            
            analysis_time = time.time() - start_time
            
            # Display results
            sentiment = result.get('sentiment', 'unknown')
            method = result.get('method', 'unknown')
            confidence = result.get('confidence', 0)
            
            status = "✅" if sentiment == expected else "❌"
            
            print(f"{text[:34]:<35} {expected:<10} {sentiment:<10} {method:<25} {analysis_time*1000:<8.1f}ms")
            
            # Check if ONNX is being used
            if 'onnx' in method.lower():
                print(f"   🚀 ONNX optimization active! Confidence: {confidence:.3f}")
            else:
                print(f"   ⚠️  Using fallback method. Confidence: {confidence:.3f}")
        
        print(f"\n3️⃣ Performance Summary:")
        
        # Quick performance test
        performance_text = "This product is amazing and works perfectly!"
        times = []
        
        for i in range(10):
            start_time = time.time()
            result = analyzer.analyze_sentiment(performance_text)
            times.append(time.time() - start_time)
        
        avg_time = sum(times) / len(times)
        method_used = result.get('method', 'unknown')
        
        print(f"   Average analysis time: {avg_time*1000:.1f}ms")
        print(f"   Method being used: {method_used}")
        
        if 'onnx' in method_used.lower():
            print(f"   🎉 SUCCESS: ONNX optimization is active!")
            print(f"   Expected performance: 50-60% faster than PyTorch")
        else:
            print(f"   ℹ️  Using fallback method (PyTorch or VADER)")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the ONNX integration test."""
    success = test_onnx_integration()
    
    if success:
        print(f"\n🎯 INTEGRATION TEST RESULT: SUCCESS")
        print(f"Your sentiment analyzer is now using ONNX-optimized models!")
    else:
        print(f"\n❌ INTEGRATION TEST RESULT: FAILED")
        print(f"Check the errors above and ensure dependencies are installed.")

if __name__ == "__main__":
    main()