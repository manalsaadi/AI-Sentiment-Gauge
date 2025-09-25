#!/usr/bin/env python3
"""
Comprehensive comparison test: ONNX RoBERTa vs PyTorch RoBERTa for Sentiment Analysis
Tests speed, memory usage, and accuracy for both English and Multilingual models.
"""

import sys
import os
import time
import psutil
import gc
import json
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

# Add backend to path
backend_path = Path(__file__).parent / ".." / ".." / ".." / "backend" / "src"
sys.path.insert(0, str(backend_path))

class RoBERTaComparisonTest:
    def __init__(self):
        self.test_texts = [
            # English texts (various sentiment levels)
            "I absolutely love this product! It's amazing and works perfectly.",
            "This is terrible. I hate it completely and would never recommend it.",
            "The weather is okay today, nothing really special about it.",
            "Outstanding performance! Exceeded all my expectations.",
            "Completely disappointed. Waste of money and time.",
            "Not bad, but could be better. Average quality overall.",
            "Fantastic experience! Will definitely use again.",
            "Poor customer service. Very frustrated with the response.",
            "It's fine I guess. Does what it's supposed to do.",
            "Incredible value for money! Highly recommended.",
            
            # Multilingual texts (same sentiments in different languages)
            "¡Este producto es fantástico! Me encanta mucho.",  # Spanish - positive
            "C'est vraiment mauvais. Je le déteste complètement.",  # French - negative  
            "Das Wetter ist heute in Ordnung, nichts Besonderes.",  # German - neutral
            "Prestazione eccezionale! Ha superato tutte le aspettative.",  # Italian - positive
            "Muito decepcionado. Perda de dinheiro e tempo.",  # Portuguese - negative
            "Niet slecht, maar kan beter. Gemiddelde kwaliteit.",  # Dutch - neutral
            "¡Experiencia fantástica! Definitivamente lo usaré de nuevo.",  # Spanish - positive
            "Mauvais service client. Très frustré par la réponse.",  # French - negative
            "È okay, immagino. Fa quello che dovrebbe fare.",  # Italian - neutral
            "Valor increíble por el dinero! Muy recomendado."  # Spanish - positive
        ]
        
        self.pytorch_english_pipeline = None
        self.pytorch_multilingual_pipeline = None
        self.onnx_english_pipeline = None
        self.onnx_multilingual_pipeline = None
        
    def measure_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    
    def initialize_pytorch_models(self) -> Dict[str, Any]:
        """Initialize PyTorch RoBERTa models."""
        print("\n🔥 Initializing PyTorch RoBERTa Models...")
        
        try:
            from transformers import pipeline
            
            start_memory = self.measure_memory_usage()
            start_time = time.time()
            
            # English model
            print("Loading English PyTorch model...")
            self.pytorch_english_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=-1  # CPU
            )
            
            # Multilingual model  
            print("Loading Multilingual PyTorch model...")
            self.pytorch_multilingual_pipeline = pipeline(
                "sentiment-analysis", 
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                device=-1  # CPU
            )
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            return {
                "initialization_time": end_time - start_time,
                "memory_usage": end_memory - start_memory,
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Error initializing PyTorch models: {e}")
            return {
                "initialization_time": 0,
                "memory_usage": 0,
                "success": False,
                "error": str(e)
            }
    
    def initialize_onnx_models(self) -> Dict[str, Any]:
        """Initialize ONNX RoBERTa models."""
        print("\n⚡ Initializing ONNX RoBERTa Models...")
        
        try:
            from optimum.onnxruntime import ORTModelForSequenceClassification
            from transformers import AutoTokenizer, pipeline
            
            start_memory = self.measure_memory_usage()
            start_time = time.time()
            
            # Create cache directory
            cache_dir = Path("../../../../model_cache")
            cache_dir.mkdir(exist_ok=True)
            
            # English ONNX model
            english_onnx_path = cache_dir / "roberta_english_onnx"
            print(f"Setting up English ONNX model at: {english_onnx_path}")
            
            if english_onnx_path.exists():
                print("📦 Loading cached English ONNX model...")
                english_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    english_onnx_path,
                    provider="CPUExecutionProvider"
                )
                english_tokenizer = AutoTokenizer.from_pretrained(english_onnx_path)
            else:
                print("⚡ Converting English model to ONNX...")
                english_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    "cardiffnlp/twitter-roberta-base-sentiment-latest",
                    export=True,
                    provider="CPUExecutionProvider"
                )
                english_tokenizer = AutoTokenizer.from_pretrained(
                    "cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
                
                # Save for future use
                english_onnx_model.save_pretrained(english_onnx_path)
                english_tokenizer.save_pretrained(english_onnx_path)
                print(f"💾 Saved English ONNX model: {english_onnx_path}")
            
            # Create pipeline
            self.onnx_english_pipeline = pipeline(
                "sentiment-analysis",
                model=english_onnx_model,
                tokenizer=english_tokenizer,
                device=-1
            )
            
            # Multilingual ONNX model
            multilingual_onnx_path = cache_dir / "roberta_multilingual_onnx"
            print(f"Setting up Multilingual ONNX model at: {multilingual_onnx_path}")
            
            if multilingual_onnx_path.exists():
                print("📦 Loading cached Multilingual ONNX model...")
                multilingual_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    multilingual_onnx_path,
                    provider="CPUExecutionProvider"
                )
                multilingual_tokenizer = AutoTokenizer.from_pretrained(multilingual_onnx_path)
            else:
                print("⚡ Converting Multilingual model to ONNX...")
                multilingual_onnx_model = ORTModelForSequenceClassification.from_pretrained(
                    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
                    export=True,
                    provider="CPUExecutionProvider"
                )
                multilingual_tokenizer = AutoTokenizer.from_pretrained(
                    "cardiffnlp/twitter-xlm-roberta-base-sentiment"
                )
                
                # Save for future use
                multilingual_onnx_model.save_pretrained(multilingual_onnx_path)
                multilingual_tokenizer.save_pretrained(multilingual_onnx_path)
                print(f"💾 Saved Multilingual ONNX model: {multilingual_onnx_path}")
            
            # Create pipeline
            self.onnx_multilingual_pipeline = pipeline(
                "sentiment-analysis",
                model=multilingual_onnx_model,
                tokenizer=multilingual_tokenizer,
                device=-1
            )
            
            end_time = time.time()
            end_memory = self.measure_memory_usage()
            
            return {
                "initialization_time": end_time - start_time,
                "memory_usage": end_memory - start_memory,
                "success": True
            }
            
        except Exception as e:
            print(f"❌ Error initializing ONNX models: {e}")
            import traceback
            traceback.print_exc()
            return {
                "initialization_time": 0,
                "memory_usage": 0,
                "success": False,
                "error": str(e)
            }
    
    def run_performance_test(self, pipeline, texts: List[str], model_name: str, num_runs: int = 5) -> Dict[str, Any]:
        """Run performance test on a pipeline."""
        print(f"\n🏃 Testing {model_name} performance...")
        
        if pipeline is None:
            return {
                "model_name": model_name,
                "success": False,
                "error": "Pipeline not initialized"
            }
        
        try:
            # Warmup run
            pipeline(texts[0])
            gc.collect()
            
            # Measure baseline memory
            baseline_memory = self.measure_memory_usage()
            
            # Performance testing
            times = []
            results = []
            
            for run in range(num_runs):
                start_time = time.time()
                
                run_results = []
                for text in texts:
                    result = pipeline(text)
                    run_results.append(result)
                
                end_time = time.time()
                times.append(end_time - start_time)
                
                if run == 0:  # Save results from first run for accuracy comparison
                    results = run_results
            
            # Memory after processing
            peak_memory = self.measure_memory_usage()
            
            # Calculate statistics
            avg_time = np.mean(times)
            std_time = np.std(times)
            min_time = np.min(times)
            max_time = np.max(times)
            avg_time_per_text = avg_time / len(texts)
            
            return {
                "model_name": model_name,
                "success": True,
                "avg_total_time": avg_time,
                "std_time": std_time,
                "min_time": min_time,
                "max_time": max_time,
                "avg_time_per_text": avg_time_per_text,
                "memory_usage": peak_memory - baseline_memory,
                "peak_memory": peak_memory,
                "results": results,
                "num_texts": len(texts),
                "num_runs": num_runs
            }
            
        except Exception as e:
            print(f"❌ Error testing {model_name}: {e}")
            return {
                "model_name": model_name,
                "success": False,
                "error": str(e)
            }
    
    def calculate_accuracy_similarity(self, pytorch_results: List, onnx_results: List) -> Dict[str, Any]:
        """Compare accuracy between PyTorch and ONNX results."""
        if not pytorch_results or not onnx_results or len(pytorch_results) != len(onnx_results):
            return {"similarity": 0.0, "identical_predictions": 0, "score_difference": 1.0}
        
        identical_predictions = 0
        score_differences = []
        
        for pt_result, onnx_result in zip(pytorch_results, onnx_results):
            # Handle both single result and list formats
            pt_item = pt_result[0] if isinstance(pt_result, list) else pt_result
            onnx_item = onnx_result[0] if isinstance(onnx_result, list) else onnx_result
            
            pt_label = pt_item.get('label', '')
            onnx_label = onnx_item.get('label', '')
            pt_score = pt_item.get('score', 0.0)
            onnx_score = onnx_item.get('score', 0.0)
            
            # Check if predictions are identical
            if pt_label == onnx_label:
                identical_predictions += 1
            
            # Calculate score difference
            score_diff = abs(pt_score - onnx_score)
            score_differences.append(score_diff)
        
        similarity = identical_predictions / len(pytorch_results)
        avg_score_difference = np.mean(score_differences) if score_differences else 1.0
        
        return {
            "similarity": similarity,
            "identical_predictions": identical_predictions,
            "total_predictions": len(pytorch_results),
            "avg_score_difference": avg_score_difference,
            "max_score_difference": np.max(score_differences) if score_differences else 1.0
        }
    
    def run_comparison_test(self):
        """Run the complete comparison test."""
        print("=" * 80)
        print("🤖 ONNX RoBERTa vs PyTorch RoBERTa - Comprehensive Comparison")
        print("=" * 80)
        
        # Initialize models
        pytorch_init = self.initialize_pytorch_models()
        onnx_init = self.initialize_onnx_models()
        
        if not pytorch_init["success"] or not onnx_init["success"]:
            print("❌ Model initialization failed. Cannot proceed with comparison.")
            return
        
        print(f"\n📊 Initialization Results:")
        print(f"PyTorch - Time: {pytorch_init['initialization_time']:.2f}s, Memory: {pytorch_init['memory_usage']:.1f}MB")
        print(f"ONNX    - Time: {onnx_init['initialization_time']:.2f}s, Memory: {onnx_init['memory_usage']:.1f}MB")
        
        # Test English models
        english_texts = [text for text in self.test_texts if not any(char in text for char in 'àáäâèéëêìíïîòóöôùúüûñç¿¡')]
        multilingual_texts = [text for text in self.test_texts if any(char in text for char in 'àáäâèéëêìíïîòóöôùúüûñç¿¡')]
        
        print(f"\n🔤 Testing with {len(english_texts)} English texts and {len(multilingual_texts)} multilingual texts...")
        
        # English model comparison
        pytorch_english_results = self.run_performance_test(
            self.pytorch_english_pipeline, english_texts, "PyTorch English RoBERTa"
        )
        
        onnx_english_results = self.run_performance_test(
            self.onnx_english_pipeline, english_texts, "ONNX English RoBERTa"
        )
        
        # Multilingual model comparison  
        pytorch_multilingual_results = self.run_performance_test(
            self.pytorch_multilingual_pipeline, multilingual_texts, "PyTorch Multilingual RoBERTa"
        )
        
        onnx_multilingual_results = self.run_performance_test(
            self.onnx_multilingual_pipeline, multilingual_texts, "ONNX Multilingual RoBERTa"
        )
        
        # Calculate accuracy comparisons
        english_accuracy = self.calculate_accuracy_similarity(
            pytorch_english_results.get("results", []),
            onnx_english_results.get("results", [])
        )
        
        multilingual_accuracy = self.calculate_accuracy_similarity(
            pytorch_multilingual_results.get("results", []),
            onnx_multilingual_results.get("results", [])
        )
        
        # Display comprehensive results
        self.display_results(
            pytorch_english_results, onnx_english_results, english_accuracy,
            pytorch_multilingual_results, onnx_multilingual_results, multilingual_accuracy,
            pytorch_init, onnx_init
        )
    
    def display_results(self, pytorch_en, onnx_en, en_accuracy, pytorch_multi, onnx_multi, multi_accuracy, pytorch_init, onnx_init):
        """Display comprehensive comparison results."""
        
        print("\n" + "=" * 80)
        print("📈 COMPREHENSIVE RESULTS SUMMARY")
        print("=" * 80)
        
        # Performance comparison table
        print(f"\n{'Metric':<25} {'PyTorch EN':<15} {'ONNX EN':<15} {'PyTorch Multi':<15} {'ONNX Multi':<15}")
        print("-" * 90)
        
        if pytorch_en["success"] and onnx_en["success"]:
            print(f"{'Avg Time per Text (ms)':<25} {pytorch_en['avg_time_per_text']*1000:<15.1f} {onnx_en['avg_time_per_text']*1000:<15.1f} {pytorch_multi['avg_time_per_text']*1000:<15.1f} {onnx_multi['avg_time_per_text']*1000:<15.1f}")
            print(f"{'Memory Usage (MB)':<25} {pytorch_en['memory_usage']:<15.1f} {onnx_en['memory_usage']:<15.1f} {pytorch_multi['memory_usage']:<15.1f} {onnx_multi['memory_usage']:<15.1f}")
        
        # Speed improvement calculations
        if pytorch_en["success"] and onnx_en["success"]:
            en_speed_improvement = ((pytorch_en['avg_time_per_text'] - onnx_en['avg_time_per_text']) / pytorch_en['avg_time_per_text']) * 100
            multi_speed_improvement = ((pytorch_multi['avg_time_per_text'] - onnx_multi['avg_time_per_text']) / pytorch_multi['avg_time_per_text']) * 100
            
            print(f"\n🚀 SPEED IMPROVEMENTS:")
            print(f"English Model: {en_speed_improvement:.1f}% faster with ONNX")
            print(f"Multilingual Model: {multi_speed_improvement:.1f}% faster with ONNX")
        
        # Memory improvement calculations
        if pytorch_en["success"] and onnx_en["success"]:
            en_memory_improvement = ((pytorch_en['memory_usage'] - onnx_en['memory_usage']) / pytorch_en['memory_usage']) * 100
            multi_memory_improvement = ((pytorch_multi['memory_usage'] - onnx_multi['memory_usage']) / pytorch_multi['memory_usage']) * 100
            
            print(f"\n💾 MEMORY IMPROVEMENTS:")
            print(f"English Model: {en_memory_improvement:.1f}% less memory with ONNX")
            print(f"Multilingual Model: {multi_memory_improvement:.1f}% less memory with ONNX")
        
        # Accuracy comparison
        print(f"\n🎯 ACCURACY COMPARISON:")
        print(f"English Model - Identical Predictions: {en_accuracy['identical_predictions']}/{en_accuracy['total_predictions']} ({en_accuracy['similarity']*100:.1f}%)")
        print(f"English Model - Avg Score Difference: {en_accuracy['avg_score_difference']:.4f}")
        print(f"Multilingual Model - Identical Predictions: {multi_accuracy['identical_predictions']}/{multi_accuracy['total_predictions']} ({multi_accuracy['similarity']*100:.1f}%)")  
        print(f"Multilingual Model - Avg Score Difference: {multi_accuracy['avg_score_difference']:.4f}")
        
        # Overall recommendation
        print(f"\n" + "=" * 80)
        print("🏆 RECOMMENDATION")
        print("=" * 80)
        
        if en_speed_improvement > 0 and multi_speed_improvement > 0:
            print(f"✅ ONNX optimization is HIGHLY RECOMMENDED!")
            print(f"   • Speed: {en_speed_improvement:.1f}% - {multi_speed_improvement:.1f}% faster")
            print(f"   • Memory: {en_memory_improvement:.1f}% - {multi_memory_improvement:.1f}% less usage")
            print(f"   • Accuracy: {en_accuracy['similarity']*100:.1f}% - {multi_accuracy['similarity']*100:.1f}% identical predictions")
            print(f"   • Quality loss: Minimal ({en_accuracy['avg_score_difference']:.4f} - {multi_accuracy['avg_score_difference']:.4f} avg difference)")
        else:
            print(f"⚠️  Mixed results - review individual metrics above")

def main():
    """Run the comparison test."""
    test = RoBERTaComparisonTest()
    
    try:
        test.run_comparison_test()
    except Exception as e:
        print(f"❌ Error during comparison test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()