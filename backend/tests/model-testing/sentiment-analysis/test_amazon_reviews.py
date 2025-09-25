#!/usr/bin/env python3
"""
Amazon Reviews Sentiment Analysis Test
Test sentiment analysis on 10% of the Amazon reviews training dataset
"""

import sys
import os
import bz2
import random
import time
from collections import defaultdict, Counter

# Add the src directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from analysis.sentiment_analyzer import SentimentAnalyzer

def load_amazon_reviews_sample(dataset_path, num_samples=5000):
    """Load exactly 5,000 random samples from Amazon reviews training data"""
    
    train_file_path = os.path.join(dataset_path, 'train.ft.txt.bz2')
    
    print(f"📁 Loading Amazon reviews from: {train_file_path}")
    print(f"🎯 Target sample size: {num_samples:,} random reviews")
    
    if not os.path.exists(train_file_path):
        print(f"❌ Training file not found: {train_file_path}")
        return []
    
    # First pass: count total lines to calculate sampling probability
    print("🔍 First pass: counting total lines in dataset...")
    total_lines = 0
    
    try:
        with bz2.open(train_file_path, 'rt', encoding='utf-8') as file:
            for line in file:
                if line.strip().startswith('__label__'):
                    total_lines += 1
                
                # Progress indicator for counting
                if total_lines % 500000 == 0:
                    print(f"   📈 Counted {total_lines:,} valid lines...")
    
    except Exception as e:
        print(f"❌ Error counting lines: {e}")
        return []
    
    print(f"✅ Total valid lines in dataset: {total_lines:,}")
    
    # Calculate sampling probability to get approximately num_samples
    if total_lines <= num_samples:
        sampling_probability = 1.0
        print(f"📊 Using all available lines ({total_lines:,})")
    else:
        # Use slightly higher probability to account for parsing failures
        sampling_probability = (num_samples * 1.2) / total_lines
        print(f"📊 Sampling probability: {sampling_probability:.4f} ({sampling_probability*100:.2f}%)")
    
    # Second pass: collect samples
    print("🔍 Second pass: collecting random samples...")
    reviews = []
    lines_processed = 0
    
    try:
        with bz2.open(train_file_path, 'rt', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line.startswith('__label__'):
                    lines_processed += 1
                    
                    # Sample based on probability
                    if random.random() <= sampling_probability and len(reviews) < num_samples:
                        try:
                            # Split at the first space after label
                            label_end = line.find(' ')
                            if label_end != -1:
                                label = line[:label_end]
                                text = line[label_end + 1:].strip()
                                
                                # Convert fastText labels to sentiment
                                # __label__1 = negative, __label__2 = positive
                                if label == '__label__1':
                                    sentiment = 'negative'
                                elif label == '__label__2':
                                    sentiment = 'positive'
                                else:
                                    continue
                                
                                reviews.append({
                                    'text': text,
                                    'expected': sentiment,
                                    'original_label': label
                                })
                        except Exception as e:
                            continue
                
                # Progress indicator
                if lines_processed % 100000 == 0:
                    print(f"   📈 Processed {lines_processed:,} lines, collected {len(reviews):,} samples...")
                
                # Stop if we've collected enough samples
                if len(reviews) >= num_samples:
                    print(f"✅ Target sample size reached: {len(reviews):,} samples")
                    break
    
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
        return []
    
    print(f"✅ Dataset sampling completed!")
    print(f"   Lines processed: {lines_processed:,}")
    print(f"   Final sample size: {len(reviews):,} reviews")
    
    # Show distribution
    sentiment_counts = Counter(review['expected'] for review in reviews)
    print(f"   Sentiment distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(reviews)) * 100
        print(f"     {sentiment.capitalize()}: {count:,} ({percentage:.1f}%)")
    
    return reviews

def evaluate_amazon_reviews(reviews):
    """Evaluate sentiment analysis on Amazon reviews"""
    
    print(f"\n🚀 Initializing Sentiment Analyzer with ONNX optimization...")
    
    start_time = time.time()
    analyzer = SentimentAnalyzer()
    init_time = time.time() - start_time
    
    print(f"   ✅ Initialization completed in {init_time:.2f}s\n")
    
    results = []
    method_usage = Counter()
    processing_times = []
    sentiment_accuracy = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    total_samples = len(reviews)
    print(f"📊 Processing {total_samples:,} Amazon product reviews...")
    print("=" * 80)
    
    start_processing = time.time()
    
    for i, review in enumerate(reviews, 1):
        text = review['text']
        expected = review['expected']
        
        # Analyze sentiment
        start_time = time.time()
        try:
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
                
        except Exception as e:
            print(f"⚠️  Error processing review {i}: {e}")
            continue
        
        # Progress indicator
        if i % 1000 == 0 or i == total_samples:
            elapsed = time.time() - start_processing
            rate = i / elapsed if elapsed > 0 else 0
            eta = (total_samples - i) / rate if rate > 0 else 0
            current_accuracy = sum(1 for r in results if r['correct']) / len(results) * 100
            
            print(f"{i:6,}/{total_samples:,} ({i/total_samples*100:5.1f}%) | "
                  f"Accuracy: {current_accuracy:5.1f}% | "
                  f"Rate: {rate:6.1f}/s | "
                  f"ETA: {eta/60:4.1f}m")
    
    total_processing_time = time.time() - start_processing
    
    return results, method_usage, processing_times, sentiment_accuracy, total_processing_time

def generate_amazon_results_report(results, method_usage, processing_times, sentiment_accuracy, total_time):
    """Generate comprehensive test report for Amazon reviews"""
    
    total_tests = len(results)
    correct_predictions = sum(1 for r in results if r['correct'])
    overall_accuracy = (correct_predictions / total_tests) * 100
    
    print("\n" + "=" * 80)
    print("🛒 AMAZON REVIEWS SENTIMENT ANALYSIS RESULTS")
    print("=" * 80)
    
    # Overall Performance
    print(f"\n🎯 Overall Performance:")
    print(f"   Total Amazon Reviews Analyzed: {total_tests:,}")
    print(f"   Correct Predictions: {correct_predictions:,}")
    print(f"   Overall Accuracy: {overall_accuracy:.2f}%")
    print(f"   Total Processing Time: {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"   Average Processing Time: {sum(processing_times)/len(processing_times):.1f}ms")
    print(f"   Processing Rate: {total_tests/total_time:.1f} reviews/second")
    print(f"   Fastest Prediction: {min(processing_times):.1f}ms")
    print(f"   Slowest Prediction: {max(processing_times):.1f}ms")
    
    # Method Usage Analysis
    print(f"\n🔧 Analysis Method Usage:")
    total_method_usage = sum(method_usage.values())
    for method, count in method_usage.most_common():
        percentage = (count / total_method_usage) * 100
        avg_time = sum(r['time_ms'] for r in results if r['method'] == method) / count
        print(f"   {method:30s} {count:6,} tests ({percentage:5.1f}%) | Avg: {avg_time:5.1f}ms")
    
    # Sentiment-Specific Accuracy
    print(f"\n📊 Accuracy by Sentiment Type:")
    for sentiment, stats in sentiment_accuracy.items():
        accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        print(f"   {sentiment.capitalize():8s}: {stats['correct']:6,}/{stats['total']:6,} ({accuracy:6.2f}%)")
    
    # Performance Insights
    print(f"\n💡 Key Insights:")
    
    # ONNX usage
    onnx_methods = [method for method in method_usage.keys() if 'onnx' in method]
    onnx_usage = sum(method_usage[method] for method in onnx_methods)
    onnx_percentage = (onnx_usage / total_tests) * 100
    print(f"   • ONNX Optimization Active: {onnx_usage:,}/{total_tests:,} tests ({onnx_percentage:.1f}%)")
    
    # Translation usage
    translation_methods = [method for method in method_usage.keys() if 'translation' in method]
    translation_usage = sum(method_usage[method] for method in translation_methods)
    translation_percentage = (translation_usage / total_tests) * 100
    print(f"   • Translation-based Analysis: {translation_usage:,}/{total_tests:,} tests ({translation_percentage:.1f}%)")
    
    # Fallback usage
    fallback_methods = [method for method in method_usage.keys() if method in ['vader', 'pytorch_english', 'pytorch_multilingual']]
    fallback_usage = sum(method_usage[method] for method in fallback_methods)
    fallback_percentage = (fallback_usage / total_tests) * 100
    print(f"   • Fallback Methods Used: {fallback_usage:,}/{total_tests:,} tests ({fallback_percentage:.1f}%)")
    
    # Performance rating
    avg_time = sum(processing_times) / len(processing_times)
    processing_rate = total_tests / total_time
    
    if avg_time < 50 and processing_rate > 20:
        performance_rating = "Excellent"
    elif avg_time < 100 and processing_rate > 10:
        performance_rating = "Good"
    elif avg_time < 200 and processing_rate > 5:
        performance_rating = "Fair"
    else:
        performance_rating = "Needs Improvement"
    
    print(f"   • Processing Performance: {performance_rating}")
    print(f"   • Throughput: {processing_rate:.1f} reviews/second")
    
    # Accuracy rating
    if overall_accuracy >= 85:
        accuracy_rating = "Excellent"
    elif overall_accuracy >= 80:
        accuracy_rating = "Good"
    elif overall_accuracy >= 75:
        accuracy_rating = "Fair"
    else:
        accuracy_rating = "Needs Improvement"
    
    print(f"   • Accuracy Rating: {accuracy_rating}")
    
    # Show some examples
    print(f"\n📝 Sample Results (First 5 reviews):")
    for i, result in enumerate(results[:5], 1):
        status = "✅" if result['correct'] else "❌"
        print(f"   {i}. {status} Expected: {result['expected']:8s} | Predicted: {result['predicted']:8s}")
        print(f"      Text: {result['text']}")
        print(f"      Method: {result['method']} | Confidence: {result['confidence']:.3f} | Time: {result['time_ms']:.1f}ms")
        print()
    
    print(f"🎉 Amazon Reviews Analysis Complete!")
    return overall_accuracy, avg_time, processing_rate

def main():
    """Main test execution function"""
    print("=" * 80)
    print("🛒 AMAZON REVIEWS SENTIMENT ANALYSIS TEST")
    print("=" * 80)
    print("Testing sentiment analysis on 5,000 random Amazon product reviews")
    
    # Set random seed for reproducible sampling
    random.seed(42)
    
    # Dataset path from kagglehub download
    dataset_path = r"C:\Users\manal\.cache\kagglehub\datasets\bittlingmayer\amazonreviews\versions\7"
    
    # Load exactly 5,000 random Amazon reviews
    reviews = load_amazon_reviews_sample(dataset_path, num_samples=5000)
    
    if not reviews:
        print("❌ No reviews loaded. Exiting.")
        return
    
    # Run evaluation on all loaded reviews (already limited to 200k)
    results, method_usage, processing_times, sentiment_accuracy, total_time = evaluate_amazon_reviews(reviews)
    
    # Generate report
    overall_accuracy, avg_time, processing_rate = generate_amazon_results_report(
        results, method_usage, processing_times, sentiment_accuracy, total_time
    )
    
    # Final summary
    print(f"\n🏆 FINAL SUMMARY:")
    print(f"   Dataset: Amazon Product Reviews (sample of {len(results):,} reviews)")
    print(f"   Overall Accuracy: {overall_accuracy:.2f}%")
    print(f"   Average Response Time: {avg_time:.1f}ms")
    print(f"   Processing Rate: {processing_rate:.1f} reviews/second")
    print(f"   ONNX Optimization: {'🟢 Active' if any('onnx' in method for method in method_usage.keys()) else '🔴 Inactive'}")
    print(f"   System Status: {'🟢 Production Ready' if overall_accuracy >= 80 and avg_time < 100 else '🟡 Needs Optimization'}")

if __name__ == "__main__":
    main()