#!/usr/bin/env python3
"""
Script to run the consolidated Construction Estimation App
"""

import subprocess
import sys
import os

def run_streamlit_app():
    """Run the Streamlit app"""
    print("🏗️ Starting Consolidated Construction Estimation App...")
    print("=" * 50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "consolidated_app.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    run_streamlit_app()