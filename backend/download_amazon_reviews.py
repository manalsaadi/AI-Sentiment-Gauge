#!/usr/bin/env python3
"""
Download Amazon Reviews Dataset from Kaggle
"""

import kagglehub
import os
import time

def download_amazon_reviews():
    """Download the Amazon reviews dataset using kagglehub"""
    
    print("🚀 Downloading Amazon Reviews Dataset from Kaggle...")
    print("Dataset: bittlingmayer/amazonreviews")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        # Download the dataset
        path = kagglehub.dataset_download("bittlingmayer/amazonreviews")
        
        download_time = time.time() - start_time
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Download path: {path}")
        print(f"⏱️  Download time: {download_time:.2f} seconds")
        
        # List files in the downloaded directory
        print("\n📂 Dataset contents:")
        if os.path.exists(path):
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    file_size_mb = file_size / (1024 * 1024)
                    print(f"   📄 {file} ({file_size_mb:.2f} MB)")
        
        return path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    dataset_path = download_amazon_reviews()
    
    if dataset_path:
        print(f"\n🎉 Dataset ready for use at: {dataset_path}")
        print("You can now load and analyze the Amazon reviews data!")
    else:
        print("\n💥 Failed to download dataset")