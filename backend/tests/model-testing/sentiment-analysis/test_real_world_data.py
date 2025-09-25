#!/usr/bin/env python3
"""
Real-World Sentiment Analysis Test
Using test_output.txt dataset to evaluate sentiment analysis performance
"""

import sys
import os
import csv
import time
from collections import defaultdict, Counter

# Add the src directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analysis.sentiment_analyzer import SentimentAnalyzer

def load_test_data(file_path):
    """Load test data from tab-separated file"""
    test_cases = []
    
    print(f"📁 Loading test data from: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                text = row['text'].strip()
                expected_sentiment = row['sentiment'].strip().lower()
                
                # Skip empty lines or invalid data
                if text and expected_sentiment in ['positive', 'negative', 'neutral']:
                    test_cases.append({
                        'text': text,
                        'expected': expected_sentiment
                    })
        
        print(f"✅ Loaded {len(test_cases)} test cases")
        return test_cases
    
    except Exception as e:
        print(f"❌ Error loading test data: {e}")
        return []

def evaluate_sentiment_analysis(test_cases):
    """Evaluate sentiment analysis on test cases"""
    print("\n🚀 Initializing Sentiment Analyzer with ONNX optimization...")
    
    start_time = time.time()
    analyzer = SentimentAnalyzer()
    init_time = time.time() - start_time
    
    print(f"   ✅ Initialization completed in {init_time:.2f}s\n")
    
    results = []
    method_usage = Counter()
    processing_times = []
    sentiment_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    print("📊 Processing test cases...")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        text = test_case['text']
        expected = test_case['expected']
        
        # Analyze sentiment
        start_time = time.time()
        result = analyzer.analyze_sentiment(text)
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        predicted = result['sentiment'].lower()
        method = result['method']
        confidence = result['confidence']
        
        # Track results
        is_correct = predicted == expected
        results.append({
            'text': text[:50] + '...' if len(text) > 50 else text,
            'expected': expected,
            'predicted': predicted,
            'correct': is_correct,
            'method': method,
            'confidence': confidence,
            'time_ms': processing_time
        })
        
        method_usage[method] += 1
        processing_times.append(processing_time)
        sentiment_accuracy[expected]['total'] += 1
        if is_correct:
            sentiment_accuracy[expected]['correct'] += 1
        
        # Print progress every 10 tests or if incorrect
        if i % 10 == 0 or not is_correct:
            status = "✅" if is_correct else "❌"
            print(f"{i:3d}. {status} {expected:8s} ({predicted:8s}) {method:25s} {processing_time:6.1f}ms")
            if not is_correct:
                print(f"     Text: {text[:60]}{'...' if len(text) > 60 else ''}")
    
    return results, method_usage, processing_times, sentiment_accuracy

def generate_detailed_report(results, method_usage, processing_times, sentiment_accuracy):
    """Generate comprehensive test report"""
    total_tests = len(results)
    correct_predictions = sum(1 for r in results if r['correct'])
    overall_accuracy = (correct_predictions / total_tests) * 100
    
    print("\n" + "=" * 80)
    print("📈 REAL-WORLD SENTIMENT ANALYSIS TEST RESULTS")
    print("=" * 80)
    
    # Overall Performance
    print(f"\n🎯 Overall Performance:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Correct Predictions: {correct_predictions}")
    print(f"   Overall Accuracy: {overall_accuracy:.1f}%")
    print(f"   Average Processing Time: {sum(processing_times)/len(processing_times):.1f}ms")
    print(f"   Fastest Prediction: {min(processing_times):.1f}ms")
    print(f"   Slowest Prediction: {max(processing_times):.1f}ms")
    
    # Method Usage Analysis
    print(f"\n🔧 Analysis Method Usage:")
    total_method_usage = sum(method_usage.values())
    for method, count in method_usage.most_common():
        percentage = (count / total_method_usage) * 100
        print(f"   {method:30s} {count:3d} tests ({percentage:5.1f}%)")
    
    # Sentiment-Specific Accuracy
    print(f"\n📊 Accuracy by Sentiment Type:")
    for sentiment, stats in sentiment_accuracy.items():
        accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"   {sentiment.capitalize():8s}: {stats['correct']:2d}/{stats['total']:2d} ({accuracy:5.1f}%)")
    
    # Most Challenging Cases (incorrect predictions)
    print(f"\n❌ Most Challenging Cases:")
    incorrect_cases = [r for r in results if not r['correct']]
    
    if incorrect_cases:
        # Show up to 10 most challenging cases
        for i, case in enumerate(incorrect_cases[:10], 1):
            print(f"   {i:2d}. Expected: {case['expected']:8s} | Predicted: {case['predicted']:8s}")
            print(f"       Text: {case['text']}")
            print(f"       Method: {case['method']} | Confidence: {case['confidence']:.3f}")
            print()
    else:
        print("   🎉 No incorrect predictions! Perfect performance!")
    
    # Performance Insights
    print(f"\n💡 Key Insights:")
    
    # ONNX usage
    onnx_methods = [method for method in method_usage.keys() if 'onnx' in method]
    onnx_usage = sum(method_usage[method] for method in onnx_methods)
    onnx_percentage = (onnx_usage / total_tests) * 100
    print(f"   • ONNX Optimization Active: {onnx_usage}/{total_tests} tests ({onnx_percentage:.1f}%)")
    
    # Translation usage
    translation_methods = [method for method in method_usage.keys() if 'translation' in method]
    translation_usage = sum(method_usage[method] for method in translation_methods)
    translation_percentage = (translation_usage / total_tests) * 100
    print(f"   • Translation-based Analysis: {translation_usage}/{total_tests} tests ({translation_percentage:.1f}%)")
    
    # Fallback usage
    fallback_methods = [method for method in method_usage.keys() if method in ['vader', 'pytorch_english', 'pytorch_multilingual']]
    fallback_usage = sum(method_usage[method] for method in fallback_methods)
    fallback_percentage = (fallback_usage / total_tests) * 100
    print(f"   • Fallback Methods Used: {fallback_usage}/{total_tests} tests ({fallback_percentage:.1f}%)")
    
    # Performance comparison
    avg_time = sum(processing_times) / len(processing_times)
    if avg_time < 50:
        performance_rating = "Excellent"
    elif avg_time < 100:
        performance_rating = "Good"
    elif avg_time < 200:
        performance_rating = "Fair"
    else:
        performance_rating = "Needs Improvement"
    
    print(f"   • Average Response Time: {avg_time:.1f}ms ({performance_rating})")
    
    if overall_accuracy >= 90:
        accuracy_rating = "Excellent"
    elif overall_accuracy >= 80:
        accuracy_rating = "Good"
    elif overall_accuracy >= 70:
        accuracy_rating = "Fair"
    else:
        accuracy_rating = "Needs Improvement"
    
    print(f"   • Overall Accuracy Rating: {accuracy_rating}")
    
    print(f"\n🎉 Test completed successfully!")
    return overall_accuracy, avg_time

def main():
    """Main test execution function"""
    print("=" * 80)
    print("🌟 REAL-WORLD SENTIMENT ANALYSIS EVALUATION")
    print("=" * 80)
    print("Testing against real Twitter/social media data from test_output.txt")
    
    # Load test data
    test_file = os.path.join(os.path.dirname(__file__), 'test_output.txt')
    test_cases = load_test_data(test_file)
    
    if not test_cases:
        print("❌ No test cases loaded. Exiting.")
        return
    
    # Run evaluation
    results, method_usage, processing_times, sentiment_accuracy = evaluate_sentiment_analysis(test_cases)
    
    # Generate report
    overall_accuracy, avg_time = generate_detailed_report(results, method_usage, processing_times, sentiment_accuracy)
    
    # Final summary
    print(f"\n🏆 FINAL SUMMARY:")
    print(f"   Dataset: Real-world social media text ({len(test_cases)} samples)")
    print(f"   Overall Accuracy: {overall_accuracy:.1f}%")
    print(f"   Average Response Time: {avg_time:.1f}ms")
    print(f"   System Status: {'🟢 Production Ready' if overall_accuracy >= 75 and avg_time < 100 else '🟡 Needs Optimization'}")

if __name__ == "__main__":
    main()