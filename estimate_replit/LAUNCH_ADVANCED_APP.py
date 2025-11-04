#!/usr/bin/env python3
"""
🚀 ADVANCED CONSTRUCTION ESTIMATION APP LAUNCHER
===============================================
This will launch your most advanced construction estimation app
with all the features you've been working on!
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_requirements():
    """Check and install required packages"""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'openpyxl'
    ]
    
    print("🔍 Checking required packages...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package, "--user"], 
                         capture_output=True)
            print(f"✅ {package} - INSTALLED")

def find_best_app():
    """Find the most advanced app file"""
    app_files = [
        'construction_estimation_app.py',  # Most advanced
        'streamlit_app.py',               # Comprehensive version
        'SIMPLE_APP.py',                  # Fallback
        'ULTRA_SIMPLE_APP.py'             # Last resort
    ]
    
    for app_file in app_files:
        if Path(app_file).exists():
            return app_file
    
    return None

def launch_app():
    """Launch the construction estimation app"""
    print("🏗️ ADVANCED CONSTRUCTION ESTIMATION SYSTEM")
    print("=" * 60)
    
    # Check requirements
    check_requirements()
    
    # Find best app
    app_file = find_best_app()
    
    if not app_file:
        print("❌ No app file found!")
        return
    
    print(f"🚀 Launching: {app_file}")
    print("📊 Features included:")
    
    if app_file == 'construction_estimation_app.py':
        print("   ✅ Enhanced Excel Import with Formula Preservation")
        print("   ✅ Real-time Calculations & Updates")
        print("   ✅ Database Persistence & Project Management")
        print("   ✅ Advanced Search & Filtering")
        print("   ✅ Visual Analytics & Reporting")
        print("   ✅ Template System")
        print("   ✅ Multi-user Collaboration")
        print("   ✅ Professional UI/UX")
    elif app_file == 'streamlit_app.py':
        print("   ✅ Comprehensive Estimation Features")
        print("   ✅ Excel Import/Export")
        print("   ✅ SSR Database")
        print("   ✅ Cost Calculations")
        print("   ✅ Professional Interface")
    else:
        print("   ✅ Basic Estimation Features")
        print("   ✅ Add/View Measurements")
        print("   ✅ Cost Summaries")
    
    print("\n🌐 Starting web server...")
    print("📱 The app will open automatically in your browser")
    print("🔗 URL: http://localhost:8508")
    print("\n⏹️  Press Ctrl+C to stop the app")
    print("=" * 60)
    
    # Launch streamlit
    try:
        # Open browser after a delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8508')
            except:
                pass
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Run streamlit
        result = subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_file,
            "--server.port", "8508",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ], capture_output=False, text=True)
        
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Python is installed")
        print("2. Try: pip install streamlit pandas numpy plotly openpyxl")
        print("3. Check if port 8508 is available")

if __name__ == "__main__":
    launch_app()