# How to Run the Construction Estimation System

## Overview
The Construction Estimation System is a Streamlit-based web application that provides professional construction cost estimation capabilities. This document provides instructions on how to run the application.

## Prerequisites
1. Python 3.8 or higher installed on your system
2. pip package manager (usually comes with Python)
3. Web browser (Chrome, Firefox, Edge, Safari, etc.)

## Installation Steps

### 1. Install Required Packages
Open a command prompt or terminal and navigate to the project directory, then run:

```bash
pip install -r requirements.txt
```

If you encounter permission issues, try:

```bash
python -m pip install --user streamlit pandas numpy openpyxl
```

### 2. Verify Installation
Check that all packages are installed correctly:

```bash
python -c "import streamlit as st; import pandas as pd; import numpy as np; print('All packages imported successfully')"
```

## Running the Application

### Option 1: Using the Provided Batch Files
Double-click on one of these batch files:
- `run_app.bat` - Full setup with dependency installation
- `quick_start.bat` - Quick launch if dependencies are already installed
- `run_streamlit.bat` - Direct launch of the Streamlit app

### Option 2: Manual Launch
Open a command prompt or terminal, navigate to the project directory, and run:

```bash
streamlit run streamlit_estimation_app.py
```

Or alternatively:

```bash
python -m streamlit run streamlit_estimation_app.py
```

### Option 3: Specifying Custom Port
To run the app on a specific port:

```bash
streamlit run streamlit_estimation_app.py --server.port 8501
```

## Accessing the Application
Once the application is running, it will automatically open in your default web browser at:
- http://localhost:8501

If it doesn't open automatically, manually navigate to this URL in your browser.

## Application Features
The Construction Estimation System includes:

1. **Dashboard** - Overview of project metrics and recent activity
2. **Measurement Sheets** - Create detailed measurement sheets for different work types
3. **SSR Database** - Manage Standard Schedule of Rates with search and filtering
4. **Abstract of Cost** - Generate cost abstracts with automatic calculations

## Troubleshooting

### Common Issues and Solutions

1. **"Module not found" errors**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Port already in use**
   ```bash
   streamlit run streamlit_estimation_app.py --server.port 8502
   ```

3. **Permission errors on Windows**
   - Run Command Prompt as Administrator
   - Or use the `--user` flag when installing packages

4. **Application doesn't open in browser**
   - Manually navigate to http://localhost:8501 in your browser
   - Check firewall settings

5. **Streamlit not recognized**
   ```bash
   python -m streamlit run streamlit_estimation_app.py
   ```

## Stopping the Application
To stop the application, go to the command prompt/terminal where it's running and press `Ctrl+C`.

## System Requirements
- **OS:** Windows, macOS, or Linux
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 100MB free space
- **Browser:** Chrome, Firefox, Safari, or Edge

## Support
For issues or questions, please refer to the documentation or contact technical support.