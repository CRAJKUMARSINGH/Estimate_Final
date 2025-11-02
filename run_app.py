#!/usr/bin/env python3
"""
Simple script to run the Construction Estimation Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    try:
        # Check if streamlit is installed
        subprocess.run([sys.executable, "-c", "import streamlit"], check=True, capture_output=True)
        
        # Run the app
        print("🏗️ Starting Construction Estimation System...")
        print("📱 The app will open in your default web browser")
        print("🔗 URL: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_estimation_app.py",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
        
    except subprocess.CalledProcessError:
        print("❌ Streamlit is not installed!")
        print("📦 Please install requirements first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()