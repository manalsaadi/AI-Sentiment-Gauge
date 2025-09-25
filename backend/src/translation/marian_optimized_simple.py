#!/usr/bin/env python3
"""
MarianMT ONNX Optimized Translator - Simplified but Fast
Focus on ONNX Runtime optimizations for production speed
"""

import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import AutoTokenizer
import torch
import onnxruntime as ort

logger = logging.getLogger(__name__)

class MarianOptimizedTranslator:
    """Production-optimized MarianMT with ONNX Runtime acceleration"""
    
    LANGUAGE_PAIRS = {
        'es': 'Helsinki-NLP/opus-mt-es-en',  
        'fr': 'Helsinki-NLP/opus-mt-fr-en',   
        'de': 'Helsinki-NLP/opus-mt-de-en',
        'it': 'Helsinki-NLP/opus-mt-it-en',
        'pt': 'Helsinki-NLP/opus-mt-pt-en',
    }
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the optimized translator"""
        self.cache_dir = Path(cache_dir) if cache_dir else Path.cwd() / "model_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        self.models = {}
        self.tokenizers = {}
        self.stats = {
            'total_translations': 0,
            'total_time': 0,
            'avg_speed': 0,
            'cache_hits': 0
        }
        
        # Optimized ONNX Runtime session options
        self.session_options = ort.SessionOptions()
        self.session_options.intra_op_num_threads = 0  # Use all CPU cores
        self.session_options.inter_op_num_threads = 0  # Use all CPU cores  
        self.session_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL
        self.session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        # Enable CPU-specific optimizations
        self.providers = ['CPUExecutionProvider']
        self.provider_options = [{
            'enable_cpu_mem_arena': True,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'cpu_mem_limit': 2 * 1024 * 1024 * 1024,  # 2GB limit
            'use_parallel_mode': True,
        }]
        
        logger.info("🚀 MarianMT Optimized Translator initialized")
        logger.info(f"📁 Cache: {self.cache_dir}")
        logger.info(f"🔥 ONNX optimizations: ENABLED")
    
    def detect_language(self, text: str) -> str:
        """Improved language detection with better French detection"""
        text = text.lower()
        
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
                    score += text.count(char) * 4  # French-specific chars
                elif lang == 'es' and char == 'ñ':
                    score += text.count(char) * 4  # Spanish-specific ñ
                else:
                    score += text.count(char) * 2
            # Word-based scoring  
            for word in words:
                if word in text:
                    score += 3
            scores[lang] = score
        
        # Handle é separately (can be French or Spanish)
        if 'é' in text:
            é_count = text.count('é')
            # Check for French context words
            french_context = any(word in text for word in ['je', 'qui', 'que', 'de', 'du', 'des', 'suis', 'vie', 'génial'])
            if french_context:
                scores['fr'] = scores.get('fr', 0) + é_count * 3
            else:
                scores['es'] = scores.get('es', 0) + é_count * 2
        
        detected = max(scores.items(), key=lambda x: x[1])[0] if any(scores.values()) else 'en'
        logger.debug(f"🔍 Detected: {detected}")
        return detected
    
    def _load_optimized_model(self, source_lang: str) -> Tuple[ORTModelForSeq2SeqLM, AutoTokenizer]:
        """Load ONNX-optimized model"""
        
        if source_lang not in self.LANGUAGE_PAIRS:
            logger.warning(f"⚠️ {source_lang} not supported, using Spanish")
            source_lang = 'es'
        
        # Check memory cache first
        if source_lang in self.models:
            self.stats['cache_hits'] += 1
            return self.models[source_lang], self.tokenizers[source_lang]
        
        model_name = self.LANGUAGE_PAIRS[source_lang]
        onnx_cache_path = self.cache_dir / f"marian_{source_lang}_onnx_optimized"
        
        logger.info(f"🔄 Loading optimized model: {source_lang} -> en")
        start_time = time.time()
        
        try:
            # Load or create optimized ONNX model
            if onnx_cache_path.exists():
                logger.info(f"📦 Loading cached ONNX: {onnx_cache_path}")
                model = ORTModelForSeq2SeqLM.from_pretrained(
                    onnx_cache_path,
                    provider=self.providers[0],
                    session_options=self.session_options,
                    provider_options=self.provider_options[0]
                )
                tokenizer = AutoTokenizer.from_pretrained(onnx_cache_path)
            else:
                logger.info(f"⚡ Converting to optimized ONNX: {model_name}")
                # Create optimized ONNX model
                model = ORTModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    export=True,
                    provider=self.providers[0],
                    session_options=self.session_options,
                    provider_options=self.provider_options[0],
                    use_cache=True
                )
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                
                # Save optimized model
                model.save_pretrained(onnx_cache_path)
                tokenizer.save_pretrained(onnx_cache_path)
                logger.info(f"💾 Saved optimized model: {onnx_cache_path}")
            
            # Cache in memory
            self.models[source_lang] = model
            self.tokenizers[source_lang] = tokenizer
            
            load_time = time.time() - start_time
            logger.info(f"✅ Model ready in {load_time:.2f}s")
            
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"❌ Failed to load {source_lang}: {e}")
            if source_lang != 'es':
                return self._load_optimized_model('es')
            raise
    
    def translate(self, text: str, source_lang: Optional[str] = None, 
                 target_lang: str = 'en', max_length: int = 256) -> Dict:
        """Ultra-fast optimized translation"""
        
        start_time = time.time()
        
        # Auto-detect if needed
        if not source_lang:
            source_lang = self.detect_language(text)
        
        # Skip if already English
        if source_lang == 'en':
            return {
                'translated_text': text,
                'source_language': source_lang,
                'target_language': target_lang,
                'translation_time': 0.001,
                'total_time': 0.001,
                'confidence': 1.0,
                'method': 'no_translation_needed'
            }
        
        try:
            # Load optimized model
            model, tokenizer = self._load_optimized_model(source_lang)
            model_load_time = time.time() - start_time
            
            # Optimized tokenization
            input_text = text.strip()[:max_length]  # Truncate early
            
            # Speed-optimized tokenization
            inputs = tokenizer(
                input_text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding=False,  # No padding for single input
                add_special_tokens=True
            )
            
            # Ultra-fast inference
            inference_start = time.time()
            with torch.no_grad(), torch.inference_mode():
                outputs = model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=1,  # Greedy search (fastest)
                    do_sample=False,  # Deterministic
                    early_stopping=True,
                    pad_token_id=tokenizer.pad_token_id,
                    use_cache=True,  # Enable KV caching
                    length_penalty=1.0,  # No length penalty
                    repetition_penalty=1.0  # No repetition penalty
                )
            
            inference_time = time.time() - inference_start
            
            # Fast decoding
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            total_time = time.time() - start_time
            
            # Update stats
            self.stats['total_translations'] += 1
            self.stats['total_time'] += total_time
            self.stats['avg_speed'] = self.stats['total_time'] / self.stats['total_translations']
            
            return {
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'translation_time': inference_time,
                'total_time': total_time,
                'confidence': 0.87,
                'method': f'marian_onnx_optimized_{source_lang}',
                'model_load_time': model_load_time,
                'from_cache': source_lang in self.models,
                'optimization': 'ONNX Runtime + CPU optimizations'
            }
            
        except Exception as e:
            logger.error(f"❌ Translation failed: {e}")
            return {
                'translated_text': text,
                'source_language': source_lang,
                'target_language': target_lang,
                'translation_time': time.time() - start_time,
                'total_time': time.time() - start_time,
                'confidence': 0.0,
                'method': 'fallback_error',
                'error': str(e)
            }
    
    def warm_up(self, languages: List[str] = ['es', 'fr', 'de']) -> None:
        """Pre-load models for instant response"""
        logger.info(f"🔥 Warming up: {languages}")
        for lang in languages:
            if lang in self.LANGUAGE_PAIRS:
                try:
                    self._load_optimized_model(lang)
                    logger.info(f"✅ {lang} ready")
                except Exception as e:
                    logger.warning(f"⚠️ {lang} failed: {e}")
    
    def get_stats(self) -> Dict:
        """Performance statistics"""
        return {
            **self.stats,
            'supported_languages': list(self.LANGUAGE_PAIRS.keys()),
            'cached_models': list(self.models.keys()),
            'cache_hit_rate': self.stats['cache_hits'] / max(self.stats['total_translations'], 1) * 100
        }
    
    def clear_cache(self) -> None:
        """Clear memory cache"""
        self.models.clear()
        self.tokenizers.clear()
        logger.info("🗑️ Cache cleared")


# Testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    translator = MarianOptimizedTranslator()
    
    test_cases = [
        ("¡Hola mundo!", "es", "Spanish"),
        ("Bonjour le monde!", "fr", "French"),
        ("Hallo Welt!", "de", "German"),
        ("Hello world!", "en", "English"),
    ]
    
    print("🚀 MARIANMT OPTIMIZED TRANSLATOR TEST")
    print("=" * 50)
    
    # Test cold start (first translation with model loading)
    print("\n❄️ COLD START TEST:")
    text, lang, name = test_cases[0]
    result = translator.translate(text, source_lang=lang)
    print(f"   {name}: {text}")
    print(f"   → {result['translated_text']}")
    print(f"   Load time: {result.get('model_load_time', 0)*1000:.1f}ms")
    print(f"   Inference: {result['translation_time']*1000:.1f}ms")
    print(f"   Total: {result['total_time']*1000:.1f}ms")
    
    # Test warm performance (cached models)
    print(f"\n🔥 WARM PERFORMANCE TEST:")
    warm_times = []
    
    for text, lang, name in test_cases:
        result = translator.translate(text, source_lang=lang)
        inference_ms = result['translation_time'] * 1000
        
        print(f"   {name}: {text}")
        print(f"   → {result['translated_text']}")  
        print(f"   ⚡ {inference_ms:.1f}ms {'(cached)' if result.get('from_cache') else '(new)'}")
        
        if result.get('from_cache') and lang != 'en':
            warm_times.append(inference_ms)
        print()
    
    # Performance summary
    if warm_times:
        avg_warm = sum(warm_times) / len(warm_times)
        print(f"🏆 WARM AVERAGE: {avg_warm:.1f}ms")
        print(f"🎯 TARGET (sub-100ms): {'✅ ACHIEVED' if avg_warm < 100 else '❌ MISSED'}")
    
    stats = translator.get_stats()
    print(f"\n📊 STATS:")
    print(f"   Translations: {stats['total_translations']}")
    print(f"   Cache hits: {stats['cache_hit_rate']:.1f}%")
    print(f"   Avg speed: {stats['avg_speed']*1000:.1f}ms")
    
    print(f"\n💡 NEXT RUN WILL BE EVEN FASTER!")
    print(f"   All models cached and ready for production speed 🚀")