# Installation Guide

## Quick Start

### Option 1: One-Click Windows Batch File (Recommended)
Double-click `run_app.bat` - This will automatically:
- Check if Python is installed
- Install all required dependencies
- Start the application

### Option 2: Quick Start (For already installed systems)
Double-click `quick_start.bat` - This will:
- Check if dependencies are installed
- Start the application directly

### Option 3: Using Python Script
```bash
python run_app.py
```

### Option 4: Using Streamlit Directly
```bash
streamlit run streamlit_estimation_app.py
```


## Prerequisites

1. **Python 3.8+** - Download from [python.org](https://python.org)
2. **pip** - Usually comes with Python

## Installation Steps

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python run_app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Port already in use
```bash
streamlit run streamlit_estimation_app.py --server.port 8502
```

### Permission errors on Windows
Run Command Prompt as Administrator

## Features Available

- ✅ Measurement Sheets for different work types
- ✅ SSR (Standard Schedule of Rates) database
- ✅ Cost abstracts with automatic calculations
- ✅ Export to CSV functionality
- ✅ Professional dashboard with metrics

## System Requirements

- **OS:** Windows, macOS, or Linux
- **RAM:** 2GB minimum, 4GB recommended
- **Storage:** 100MB free space
- **Browser:** Chrome, Firefox, Safari, or Edge