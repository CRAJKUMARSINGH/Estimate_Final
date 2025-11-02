#!/usr/bin/env python3
"""
Construction Estimation System Launcher
This script helps launch the Streamlit application with proper error handling
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_python():
    """Check if Python is available"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        print(f"✅ {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python not found: {e}")
        return False

def check_packages():
    """Check if required packages are installed"""
    required_packages = ["streamlit", "pandas", "numpy"]
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "streamlit":
                import streamlit
                print(f"✅ Streamlit version {streamlit.__version__}")
            elif package == "pandas":
                import pandas
                print(f"✅ Pandas version {pandas.__version__}")
            elif package == "numpy":
                import numpy
                print(f"✅ NumPy version {numpy.__version__}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not installed")
    
    return missing_packages

def install_packages():
    """Attempt to install missing packages"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True, timeout=300)
        print("✅ Packages installed successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    try:
        print("🚀 Launching Construction Estimation System...")
        print("📱 Opening browser at http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Launch the Streamlit app
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            "streamlit_estimation_app.py",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
        
        # Give the server a moment to start
        time.sleep(3)
        
        # Try to open the browser
        try:
            webbrowser.open("http://localhost:8501")
        except:
            print("⚠️  Could not automatically open browser. Please navigate to http://localhost:8501 manually")
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("🏗️ CONSTRUCTION ESTIMATION SYSTEM LAUNCHER")
    print("=" * 60)
    print()
    
    # Check Python
    print("🔍 Checking Python installation...")
    if not check_python():
        print("Please install Python 3.8 or higher and try again.")
        return
    
    # Check packages
    print("\n🔍 Checking required packages...")
    missing_packages = check_packages()
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        if not install_packages():
            print("Please manually install the required packages:")
            print("pip install -r requirements.txt")
            return
    
    print("\n" + "=" * 60)
    # Launch the application
    launch_app()

if __name__ == "__main__":
    main()