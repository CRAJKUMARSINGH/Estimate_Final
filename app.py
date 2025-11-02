#!/usr/bin/env python3
# Entry point for deployment
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
if __name__ == "__main__":
    # Import the optimized app
    exec(open('streamlit_estimation_app_optimized.py').read())
