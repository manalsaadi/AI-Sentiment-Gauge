
#!/usr/bin/env python3
"""
Language Detection and Extraction from Amazon Reviews Dataset
Analyze languages in the dataset and extract samples by language
"""

import sys
import os
import bz2
import random
import time
from collections import Counter, defaultdict
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException

def install_langdetect():
    """Install langdetect if not available"""
    try:
        import langdetect
        return True
    except ImportError:
        print("📦 Installing langdetect package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "langdetect"])
        return True

def detect_language_safely(text):
    """Safely detect language with error handling"""
    try:
        # Clean text for better detection
        text = text.strip()
        if len(text) < 10:  # Skip very short texts
            return None
        
        # Detect language
        lang = detect(text)
        return lang
    except LangDetectException:
        return None
    except Exception:
        return None

def analyze_dataset_languages(dataset_path, max_lines=50000):
    """Analyze languages in first 50,000 lines of Amazon reviews dataset"""
    
    train_file_path = os.path.join(dataset_path, 'train.ft.txt.bz2')
    
    print(f"📁 Analyzing languages in: {train_file_path}")
    print(f"🔍 Processing first {max_lines:,} lines for language detection")
    
    if not os.path.exists(train_file_path):
        print(f"❌ Training file not found: {train_file_path}")
        return {}, {}
    
    language_counts = Counter()
    language_samples = defaultdict(list)
    total_analyzed = 0
    total_lines = 0
    
    print("🌍 Detecting languages in dataset...")
    
    try:
        with bz2.open(train_file_path, 'rt', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line.startswith('__label__'):
                    total_lines += 1
                    
                    # Stop after max_lines
                    if total_lines > max_lines:
                        print(f"✅ Reached limit of {max_lines:,} lines")
                        break
                    
                    try:
                        # Parse fastText format
                        label_end = line.find(' ')
                        if label_end != -1:
                            label = line[:label_end]
                            text = line[label_end + 1:].strip()
                            
                            # Skip very short texts
                            if len(text) < 20:
                                continue
                            
                            # Detect language
                            detected_lang = detect_language_safely(text)
                            
                            if detected_lang:
                                language_counts[detected_lang] += 1
                                
                                # Store sample if we don't have many yet
                                if len(language_samples[detected_lang]) < 5:
                                    sentiment = 'negative' if label == '__label__1' else 'positive'
                                    language_samples[detected_lang].append({
                                        'text': text[:100] + '...' if len(text) > 100 else text,
                                        'sentiment': sentiment,
                                        'full_text': text
                                    })
                                
                                total_analyzed += 1
                    except Exception as e:
                        continue
                
                # Progress indicator
                if total_lines % 5000 == 0:
                    print(f"   📈 Processed {total_lines:,} lines, analyzed {total_analyzed:,} samples...")
    
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
        return {}, {}
    
    print(f"✅ Language analysis completed!")
    print(f"   Total lines processed: {total_lines:,}")
    print(f"   Total samples analyzed: {total_analyzed:,}")
    
    return language_counts, language_samples

def extract_language_samples(dataset_path, target_language='es', num_samples=2000):
    """Extract specific number of samples for a target language"""
    
    train_file_path = os.path.join(dataset_path, 'train.ft.txt.bz2')
    
    print(f"📁 Extracting {target_language} samples from: {train_file_path}")
    print(f"🎯 Target: {num_samples:,} samples in language '{target_language}'")
    
    language_samples = []
    total_lines = 0
    detected_count = 0
    
    try:
        with bz2.open(train_file_path, 'rt', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line.startswith('__label__'):
                    total_lines += 1
                    
                    try:
                        # Parse fastText format
                        label_end = line.find(' ')
                        if label_end != -1:
                            label = line[:label_end]
                            text = line[label_end + 1:].strip()
                            
                            # Skip very short texts
                            if len(text) < 30:
                                continue
                            
                            # Detect language
                            detected_lang = detect_language_safely(text)
                            
                            if detected_lang == target_language:
                                detected_count += 1
                                sentiment = 'negative' if label == '__label__1' else 'positive'
                                
                                language_samples.append({
                                    'text': text,
                                    'expected': sentiment,
                                    'original_label': label,
                                    'detected_language': detected_lang
                                })
                                
                                if len(language_samples) >= num_samples:
                                    print(f"✅ Target sample size reached: {len(language_samples):,} samples")
                                    break
                    except Exception as e:
                        continue
                
                # Progress indicator
                if total_lines % 50000 == 0:
                    print(f"   📈 Processed {total_lines:,} lines, found {detected_count:,} {target_language} texts, collected {len(language_samples):,} samples...")
    
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
        return []
    
    print(f"✅ Language extraction completed!")
    print(f"   Total lines processed: {total_lines:,}")
    print(f"   {target_language.upper()} texts found: {detected_count:,}")
    print(f"   Final sample size: {len(language_samples):,} reviews")
    
    # Show distribution
    sentiment_counts = Counter(sample['expected'] for sample in language_samples)
    print(f"   Sentiment distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(language_samples)) * 100
        print(f"     {sentiment.capitalize()}: {count:,} ({percentage:.1f}%)")
    
    return language_samples

def main():
    """Main analysis function"""
    print("=" * 80)
    print("🌍 AMAZON REVIEWS DATASET LANGUAGE ANALYSIS")
    print("=" * 80)
    
    # Install langdetect if needed
    install_langdetect()
    
    # Set random seed
    random.seed(42)
    
    # Dataset path
    dataset_path = r"C:\Users\manal\.cache\kagglehub\datasets\bittlingmayer\amazonreviews\versions\7"
    
    # Step 1: Analyze languages in dataset
    print("\n🔍 STEP 1: Analyzing languages in first 50,000 lines...")
    language_counts, language_samples = analyze_dataset_languages(dataset_path, max_lines=50000)
    
    if language_counts:
        print(f"\n📊 Languages detected in Amazon reviews:")
        print("-" * 50)
        total_detected = sum(language_counts.values())
        
        for lang, count in language_counts.most_common(15):
            percentage = (count / total_detected) * 100
            language_name = {
                'en': 'English',
                'es': 'Spanish', 
                'fr': 'French',
                'de': 'German',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ja': 'Japanese',
                'ko': 'Korean',
                'zh-cn': 'Chinese (Simplified)',
                'ru': 'Russian',
                'ar': 'Arabic',
                'hi': 'Hindi',
                'nl': 'Dutch',
                'pl': 'Polish',
                'tr': 'Turkish'
            }.get(lang, lang.upper())
            
            print(f"   {lang:6s} ({language_name:20s}): {count:4d} samples ({percentage:5.1f}%)")
        
        # Show samples for top languages
        print(f"\n📝 Sample texts by language:")
        for lang in list(language_counts.keys())[:5]:
            language_name = {
                'en': 'English',
                'es': 'Spanish', 
                'fr': 'French',
                'de': 'German',
                'it': 'Italian'
            }.get(lang, lang.upper())
            
            print(f"\n🔤 {language_name} ({lang}) samples:")
            for i, sample in enumerate(language_samples[lang][:2], 1):
                print(f"   {i}. [{sample['sentiment']}] {sample['text']}")
    
    # Step 2: Ask user which language to extract
    print(f"\n🎯 STEP 2: Language extraction options")
    print("Available for detailed extraction:")
    top_languages = list(language_counts.keys())[:10] if language_counts else ['es', 'fr', 'de', 'it']
    
    for i, lang in enumerate(top_languages, 1):
        language_name = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ja': 'Japanese',
            'ko': 'Korean'
        }.get(lang, lang.upper())
        print(f"   {i}. {lang} ({language_name})")
    
    # For demo, let's extract Spanish samples
    target_language = 'es'  # Spanish
    print(f"\n🚀 Extracting Spanish (es) samples for testing...")
    
    spanish_samples = extract_language_samples(dataset_path, target_language='es', num_samples=1000)
    
    if spanish_samples:
        print(f"\n✅ Successfully extracted {len(spanish_samples)} Spanish Amazon reviews!")
        print(f"📄 Sample Spanish reviews:")
        for i, sample in enumerate(spanish_samples[:3], 1):
            print(f"   {i}. [{sample['expected']}] {sample['text'][:100]}...")
    
    print(f"\n🎉 Language analysis complete!")
    print(f"💡 You can now run sentiment analysis tests on specific languages!")

if __name__ == "__main__":
    main()