#!/usr/bin/env python3
"""
🏗️ CONSTRUCTION ESTIMATION SYSTEM - DEPLOYMENT ENTRY POINT
==========================================================
Entry point for production deployment (Heroku, Railway, Streamlit Cloud, etc.)
Points to the unified construction_estimation_app.py

Version: 3.0 (Unified)
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for deployment"""
    # Try multiple possible main app files in order of preference
    possible_files = [
        'construction_estimation_app.py',  # Primary unified app
        'streamlit_app.py',               # Streamlit Cloud standard
    ]
    
    for app_file in possible_files:
        if Path(app_file).exists():
            try:
                # Import and run the application
                with open(app_file, 'r', encoding='utf-8') as f:
                    exec(f.read())
                return
            except Exception as e:
                st.error(f"Error loading {app_file}: {str(e)}")
                continue
    
    # If no app file found, show error
    st.error("🚨 No main application file found!")
    st.error("Looking for one of:")
    for file in possible_files:
        st.write(f"- {file}")
    
    st.info("Available Python files:")
    current_dir = Path('.')
    for file in current_dir.glob('*.py'):
        st.write(f"- {file.name}")

if __name__ == "__main__":
    main()
