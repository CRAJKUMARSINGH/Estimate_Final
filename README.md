# Construction Estimation System

A professional Streamlit-based construction cost estimation application focused on measurement sheets, SSR database, and cost abstracts.

## Features

- **📝 Measurement Sheets**: Create detailed measurement sheets for different work types
- **📚 SSR Database**: Manage Standard Schedule of Rates with search and filtering
- **💰 Abstract of Cost**: Generate cost abstracts with automatic calculations
- **📊 Dashboard**: Overview of project metrics and recent activity

## Installation

1. Install Python 3.8 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Windows Users (Recommended)
Double-click `run_app.bat` for full setup or `quick_start.bat` for quick launch

### Manual Method
Run the Streamlit app:
```bash
streamlit run streamlit_estimation_app.py
```

The app will open in your default web browser at `http://localhost:8501`


## Work Types Supported

- 🏗️ Civil Work
- 🚰 Sanitary Work  
- ⚡ Electrical Work
- 🌳 Landscape Work

## Units Supported

- RM (Running Meter)
- Cum (Cubic Meter)
- Sqm (Square Meter)
- Nos (Numbers)
- Kg (Kilogram)
- Ton
- Ltr (Liter)
- LS (Lump Sum)

## Cost Calculations

The system automatically calculates:
- Subtotal from abstract items
- Electrification charges (7% on Civil Work)
- Prorata charges (13% on total)
- Grand total with all charges

## Export Features

- Export measurements to CSV
- Export SSR database to CSV
- Export cost abstracts to CSV
- Export detailed cost breakdown