#!/usr/bin/env python3
"""
Simple script to start the Construction Estimation App
"""

import subprocess
import sys
import os

def main():
    print("🏗️ Starting Construction Estimation App...")
    print("=" * 50)
    
    # Try to run the app using streamlit
    try:
        print("🚀 Launching app with Streamlit...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py",
            "--server.port", "8501"
        ])
    except Exception as e:
        print(f"❌ Error running app: {e}")
        print("Trying alternative method...")
        
        # Alternative method
        try:
            # Try direct execution
            exec(open("app.py").read())
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")

if __name__ == "__main__":
    main()