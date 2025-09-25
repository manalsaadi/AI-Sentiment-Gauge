#!/usr/bin/env python3
"""
Start the enhanced sentiment analysis server for testing.
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Start the FastAPI server."""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend"
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return
    
    print("🚀 Starting Enhanced Sentiment Analysis Server...")
    print("=" * 50)
    print(f"📁 Working directory: {backend_dir.absolute()}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.main:app", 
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], cwd=backend_dir, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
    except FileNotFoundError:
        print("❌ uvicorn not found. Install it with: pip install uvicorn")

if __name__ == "__main__":
    main()