#!/usr/bin/env python3
"""
Simple script to run the Construction Estimation App
"""

import subprocess
import sys
import os

def run_streamlit_app():
    """Run the Streamlit app"""
    print("🏗️ Starting Construction Estimation App...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print(f"✅ Streamlit version: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Check if pandas is installed
    try:
        import pandas
        print(f"✅ Pandas version: {pandas.__version__}")
    except ImportError:
        print("❌ Pandas not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pandas"])
    
    # Run the app
    print("\n🚀 Launching Construction Estimation App...")
    print("📱 The app will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("\n⏹️  Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_estimation_app.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    run_streamlit_app()