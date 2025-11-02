import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import json
import os
import glob
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Construction Estimation App",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for measurements
if 'measurements' not in st.session_state:
    st.session_state.measurements = pd.DataFrame(columns=MEASUREMENT_COLUMNS)
    st.session_state.counter = 1

# Initialize SSR database
if 'ssr_items' not in st.session_state:
    st.session_state.ssr_items = pd.DataFrame([
        # Earth Work
        {"code": "1.1.1", "description": "Earth work excavation in foundation by manual means", "category": "Earth Work", "unit": "cum", "rate": 245.50},
        {"code": "1.1.2", "description": "Earth work excavation by mechanical means", "category": "Earth Work", "unit": "cum", "rate": 185.00},
        {"code": "1.2.1", "description": "Earth work in backfilling", "category": "Earth Work", "unit": "cum", "rate": 125.00},
        {"code": "1.3.1", "description": "Disposal of excavated earth", "category": "Earth Work", "unit": "cum", "rate": 85.00},
        
        # Concrete Work
        {"code": "2.1.1", "description": "Cement concrete 1:2:4 using 20mm aggregate", "category": "Concrete Work", "unit": "cum", "rate": 4850.00},
        {"code": "2.1.2", "description": "Cement concrete 1:3:6 using 40mm aggregate", "category": "Concrete Work", "unit": "cum", "rate": 4200.00},
        {"code": "2.2.1", "description": "RCC work using HYSD bars", "category": "Concrete Work", "unit": "cum", "rate": 6200.00},
        {"code": "2.3.1", "description": "Precast concrete blocks", "category": "Concrete Work", "unit": "cum", "rate": 3800.00},
        
        # Masonry Work
        {"code": "3.1.1", "description": "Brick work in superstructure using common burnt clay bricks", "category": "Masonry Work", "unit": "cum", "rate": 5200.00},
        {"code": "3.1.2", "description": "Brick work in foundation using first class bricks", "category": "Masonry Work", "unit": "cum", "rate": 4800.00},
        {"code": "3.2.1", "description": "Stone masonry in cement mortar", "category": "Masonry Work", "unit": "cum", "rate": 3500.00},
        {"code": "3.3.1", "description": "Hollow concrete block masonry", "category": "Masonry Work", "unit": "cum", "rate": 2800.00},
        
        # Plastering
        {"code": "4.1.1", "description": "12mm thick cement plaster 1:4", "category": "Plastering", "unit": "sqm", "rate": 125.00},
        {"code": "4.1.2", "description": "15mm thick cement plaster 1:3", "category": "Plastering", "unit": "sqm", "rate": 145.00},
        {"code": "4.2.1", "description": "Lime plaster 12mm thick", "category": "Plastering", "unit": "sqm", "rate": 95.00},
        {"code": "4.3.1", "description": "Gypsum plaster 6mm thick", "category": "Plastering", "unit": "sqm", "rate": 85.00},
        
        # Painting
        {"code": "5.1.1", "description": "Painting with acrylic emulsion paint", "category": "Painting", "unit": "sqm", "rate": 45.00},
        {"code": "5.1.2", "description": "Painting with oil bound distemper", "category": "Painting", "unit": "sqm", "rate": 35.00},
        {"code": "5.2.1", "description": "Enamel painting on steel work", "category": "Painting", "unit": "sqm", "rate": 125.00},
        {"code": "5.3.1", "description": "Primer coat on steel work", "category": "Painting", "unit": "sqm", "rate": 65.00},
        
        # Plumbing
        {"code": "6.1.1", "description": "PVC pipes 110mm dia for drainage", "category": "Plumbing", "unit": "m", "rate": 285.00},
        {"code": "6.1.2", "description": "PVC pipes 75mm dia for drainage", "category": "Plumbing", "unit": "m", "rate": 185.00},
        {"code": "6.2.1", "description": "GI pipes 25mm dia for water supply", "category": "Plumbing", "unit": "m", "rate": 325.00},
        {"code": "6.3.1", "description": "Sanitary fittings - WC pan", "category": "Plumbing", "unit": "nos", "rate": 4500.00},
        
        # Steel Work
        {"code": "7.1.1", "description": "Steel reinforcement bars", "category": "Steel Work", "unit": "kg", "rate": 65.00},
        {"code": "7.2.1", "description": "Structural steel work", "category": "Steel Work", "unit": "kg", "rate": 85.00},
        {"code": "7.3.1", "description": "MS angles and channels", "category": "Steel Work", "unit": "kg", "rate": 75.00},
        
        # Waterproofing
        {"code": "8.1.1", "description": "Waterproofing membrane", "category": "Waterproofing", "unit": "sqm", "rate": 180.00},
        {"code": "8.2.1", "description": "Bituminous waterproofing", "category": "Waterproofing", "unit": "sqm", "rate": 125.00},
        
        # Flooring
        {"code": "9.1.1", "description": "Flooring tiles 600x600mm", "category": "Flooring", "unit": "sqm", "rate": 320.00},
        {"code": "9.1.2", "description": "Marble flooring 20mm thick", "category": "Flooring", "unit": "sqm", "rate": 850.00},
        {"code": "9.2.1", "description": "Cement concrete flooring", "category": "Flooring", "unit": "sqm", "rate": 185.00},
        
        # Roofing
        {"code": "10.1.1", "description": "AC sheet roofing", "category": "Roofing", "unit": "sqm", "rate": 285.00},
        {"code": "10.2.1", "description": "Clay tile roofing", "category": "Roofing", "unit": "sqm", "rate": 425.00}
    ])

# Initialize abstract items (linked from measurements)
if 'abstract_items' not in st.session_state:
    st.session_state.abstract_items = pd.DataFrame(columns=ABSTRACT_COLUMNS)

# Initialize General Abstract settings
if 'general_abstract_settings' not in st.session_state:
    st.session_state.general_abstract_settings = {
        'project_name': 'CONSTRUCTION OF COMMERCIAL COMPLEX FOR PANCHAYAT SAMITI GIRWA, UDAIPUR',
        'project_location': 'GIRWA, UDAIPUR',
        'engineer_name': 'CHARTERED ENGINEER, TEJHANS INVESTMENTS, UDAIPUR',
        'sanitary_work_amount': 81418.00,
        'electric_work_percentage': 12.0,
        'electric_fixtures_percentage': 5.0
    }

# Initialize separate sheets for different work types with enhanced columns
if 'measurement_sheets' not in st.session_state:
    st.session_state.measurement_sheets = {
        'Ground Floor': pd.DataFrame(columns=MEASUREMENT_COLUMNS),
        'First Floor': pd.DataFrame(columns=MEASUREMENT_COLUMNS),
        'Basement': pd.DataFrame(columns=MEASUREMENT_COLUMNS),
        'Civil Work': pd.DataFrame(columns=MEASUREMENT_COLUMNS),
        'Structural Work': pd.DataFrame(columns=MEASUREMENT_COLUMNS),
        'Finishing Work': pd.DataFrame(columns=MEASUREMENT_COLUMNS)
    }

if 'abstract_sheets' not in st.session_state:
    st.session_state.abstract_sheets = {
        'Ground Floor': pd.DataFrame(columns=ABSTRACT_COLUMNS),
        'First Floor': pd.DataFrame(columns=ABSTRACT_COLUMNS),
        'Basement': pd.DataFrame(columns=ABSTRACT_COLUMNS),
        'Civil Work': pd.DataFrame(columns=ABSTRACT_COLUMNS),
        'Structural Work': pd.DataFrame(columns=ABSTRACT_COLUMNS),
        'Finishing Work': pd.DataFrame(columns=ABSTRACT_COLUMNS)
    }

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1f4e79;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #f0f2f6;
            border-radius: 4px 4px 0 0;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff;
        }
        .total-row {
            background-color: #e3f2fd !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Constants
WORK_TYPES = {
    "Civil Work": "🏗️",
    "Sanitary Work": "🚰", 
    "Electrical Work": "⚡",
    "Landscape Work": "🌳"
}

UNITS = ["RM", "Cum", "Sqm", "Nos", "Kg", "Ton", "Ltr", "LS", "Meter", "Feet", "Inch"]

# Measurement Types for different calculation methods
MEASUREMENT_TYPES = {
    "Standard": "Nos × Length × Breadth × Height",
    "Linear": "Nos × Length", 
    "Area": "Nos × Length × Breadth",
    "Volume": "Nos × Length × Breadth × Height",
    "Circular Area": "Nos × π × (Diameter/2)²",
    "Circular Volume": "Nos × π × (Diameter/2)² × Height",
    "Deduction": "Gross - Deductions",
    "Weight": "Nos × Length × Unit Weight",
    "Custom Formula": "User Defined"
}

# Enhanced DataFrame Schemas for Complex Measurements
MEASUREMENT_COLUMNS = [
    'id', 'ssr_code', 'item_no', 'description', 'specification', 'location',
    'quantity', 'length', 'breadth', 'height', 'diameter', 'thickness', 
    'unit', 'total', 'deduction', 'net_total', 'remarks'
]

ABSTRACT_COLUMNS = [
    'id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount'
]

SSR_COLUMNS = [
    'code', 'description', 'category', 'unit', 'rate'
]

# Main App Header
st.markdown("""
    <div class="main-header">
        <h1>🏗️ Construction Estimation System</h1>
        <p>Professional Construction Cost Estimation Tool</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.selectbox("Select Module", [
    "📊 Dashboard", 
    "📋 General Abstract",
    "💰 Abstract of Cost",
    "📝 Measurement Sheets",
    "📊 Technical Report",
    "📚 SSR Database",
    "📥 Import Excel Data",
    "🔧 System Tools"
])

# Enhanced Helper Functions
def calculate_total(quantity, length, breadth, height, diameter=0, thickness=0, measurement_type="Standard"):
    """Enhanced calculation function supporting multiple measurement types"""
    import math
    
    if measurement_type == "Linear":
        return quantity * max(1, length)
    elif measurement_type == "Area":
        return quantity * max(1, length) * max(1, breadth)
    elif measurement_type == "Volume":
        return quantity * max(1, length) * max(1, breadth) * max(1, height)
    elif measurement_type == "Circular Area":
        if diameter > 0:
            return quantity * math.pi * (diameter/2)**2
        return 0
    elif measurement_type == "Circular Volume":
        if diameter > 0:
            return quantity * math.pi * (diameter/2)**2 * max(1, height)
        return 0
    elif measurement_type == "Weight":
        # For steel/reinforcement calculations
        unit_weight = 7.85 if thickness > 0 else 1  # kg/m³ for steel
        return quantity * max(1, length) * thickness * unit_weight
    else:  # Standard
        return quantity * max(1, length) * max(1, breadth) * max(1, height)

def calculate_deduction_total(gross_total, deduction_items):
    """Calculate net total after deductions"""
    total_deductions = sum(item.get('total', 0) for item in deduction_items)
    return max(0, gross_total - total_deductions)

def export_to_csv(dataframe, filename):
    return dataframe.to_csv(index=False).encode('utf-8')

def get_default_unit_rates():
    """Get default unit rates for auto-generation"""
    return {
        'cum': 3500.0,
        'sqm': 150.0,
        'rm': 100.0,
        'nos': 500.0,
        'kg': 60.0,
        'ton': 60000.0,
        'ltr': 50.0,
        'ls': 50000.0
    }

def clear_dataframe(df_type, sheet_name=None):
    """Centralized function to clear DataFrames with proper schema"""
    if df_type == 'measurements':
        if sheet_name:
            st.session_state.measurement_sheets[sheet_name] = pd.DataFrame(columns=MEASUREMENT_COLUMNS)
        else:
            st.session_state.measurements = pd.DataFrame(columns=MEASUREMENT_COLUMNS)
            st.session_state.counter = 1
    elif df_type == 'abstracts':
        if sheet_name:
            st.session_state.abstract_sheets[sheet_name] = pd.DataFrame(columns=ABSTRACT_COLUMNS)
        else:
            st.session_state.abstract_items = pd.DataFrame(columns=ABSTRACT_COLUMNS)

def create_export_button(data, filename, button_text, file_prefix="export"):
    """Centralized export button creation"""
    if isinstance(data, pd.DataFrame):
        csv_data = export_to_csv(data, filename)
    else:
        csv_data = data
    
    return st.download_button(
        button_text,
        data=csv_data,
        file_name=f"{file_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

def get_next_id(df_type, sheet_name=None):
    """Get the next available ID for a DataFrame"""
    if df_type == 'measurement':
        if sheet_name:
            return len(st.session_state.measurement_sheets[sheet_name]) + 1
        else:
            return len(st.session_state.measurements) + 1
    elif df_type == 'abstract':
        if sheet_name:
            return len(st.session_state.abstract_sheets[sheet_name]) + 1
        else:
            return len(st.session_state.abstract_items) + 1
    elif df_type == 'ssr':
        return len(st.session_state.ssr_items) + 1
    return 1

def validate_and_strip(text):
    """Validate and strip text input"""
    return text.strip() if text else ""

# UI Standardization Constants
BUTTON_TYPES = {
    'primary': 'primary',      # Main actions (Add, Generate, Import)
    'secondary': 'secondary',  # Secondary actions (Clear, Reset)
    'danger': 'secondary',     # Destructive actions (Delete, Clear)
    'neutral': None           # Neutral actions (Export, View)
}

COLUMN_LAYOUTS = {
    'metrics': [1, 1, 1, 1],           # 4 equal columns for metrics
    'form_basic': [1, 2],              # Basic form layout
    'form_detailed': [1, 2],           # Detailed form layout  
    'actions': [1, 1, 1],              # 3 equal columns for actions
    'search': [2, 1, 1],               # Search with 2 filters
    'cost_calc': [2, 1],               # Cost calculation layout
    'export': [1, 1],                  # Export options
    'stats': [1, 1]                    # Statistics display
}

def create_standardized_button(label, button_type='neutral', key=None, help_text=None):
    """Create standardized button with consistent styling"""
    button_params = {'label': label}
    
    if BUTTON_TYPES[button_type] is not None:
        button_params['type'] = BUTTON_TYPES[button_type]
    
    if key:
        button_params['key'] = key
    
    if help_text:
        button_params['help'] = help_text
    
    return st.button(**button_params)

def create_standardized_form_button(label, button_type='primary', key=None):
    """Create standardized form submit button"""
    button_params = {'label': label}
    
    if BUTTON_TYPES[button_type] is not None:
        button_params['type'] = BUTTON_TYPES[button_type]
    
    if key:
        button_params['key'] = key
    
    return st.form_submit_button(**button_params)

def create_standardized_columns(layout_type):
    """Create standardized column layouts"""
    if layout_type in COLUMN_LAYOUTS:
        return st.columns(COLUMN_LAYOUTS[layout_type])
    else:
        return st.columns([1, 1])  # Default to 2 equal columns

def create_ssr_selection_section(key_prefix="ssr"):
    """Standardized SSR code selection UI component"""
    st.subheader("🔍 SSR Code Selection")
    
    col1, col2 = create_standardized_columns('form_basic')
    
    with col1:
        ssr_codes = ["Select SSR Code..."] + st.session_state.ssr_items['code'].tolist()
        selected_ssr = st.selectbox("SSR Item Code", ssr_codes, key=f"{key_prefix}_selector")
    
    with col2:
        if selected_ssr != "Select SSR Code...":
            ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr].iloc[0]
            st.success(f"**📋 Description:** {ssr_item['description']}")
            st.info(f"**📂 Category:** {ssr_item['category']} | **📏 Unit:** {ssr_item['unit']} | **💰 Rate:** ₹{ssr_item['rate']:,.2f}")
            return selected_ssr, ssr_item
        else:
            st.info("Select an SSR code to auto-populate description and rate")
            return selected_ssr, None

def create_import_section(title, file_type, import_function, file_pattern="*.xlsx"):
    """Standardized import section UI component"""
    st.subheader(title)
    
    # Check for files in attached_assets
    files = find_estimate_files(file_pattern)
    if files:
        selected_file = st.selectbox(f"Select {file_type} file:", files, 
                                   format_func=lambda x: os.path.basename(x))
        if create_standardized_button(f"Import Selected {file_type} File", 'primary'):
            if import_function(selected_file):
                st.success(f"✅ {file_type} imported successfully from: {os.path.basename(selected_file)}")
                st.rerun()
            else:
                st.error(f"❌ Failed to import {file_type} from: {os.path.basename(selected_file)}")
    else:
        st.info("No Excel files found in attached_assets folder")
    
    # Manual file upload
    uploaded_file = st.file_uploader(f"Or upload {file_type} file", type=['xlsx', 'xls'])
    if uploaded_file is not None:
        if create_standardized_button(f"Import Uploaded {file_type} File", 'primary'):
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            if import_function(tmp_path):
                st.success(f"✅ {file_type} imported successfully from: {uploaded_file.name}")
                os.unlink(tmp_path)
                st.rerun()
            else:
                st.error(f"❌ Failed to import {file_type} from: {uploaded_file.name}")
                os.unlink(tmp_path)

def auto_generate_abstracts_from_measurements():
    """Centralized auto-generation logic for creating abstracts from measurements"""
    if st.session_state.measurements.empty or st.session_state.ssr_items.empty:
        return False, "No measurements or SSR items available"
    
    # Clear existing abstract items
    clear_dataframe('abstracts')
    
    # Group measurements by work type/category
    measurements_df = st.session_state.measurements.copy()
    ssr_df = st.session_state.ssr_items.copy()
    unit_rates = get_default_unit_rates()
    
    # Try to match measurements with SSR items
    abstract_counter = 1
    
    for _, measurement in measurements_df.iterrows():
        # Find matching SSR item by description keywords or unit
        measurement_desc = measurement['description'].lower()
        measurement_unit = measurement['unit'].lower()
        
        # Look for SSR matches
        matching_ssr = ssr_df[
            (ssr_df['unit'].str.lower() == measurement_unit) |
            (ssr_df['description'].str.lower().str.contains(
                measurement_desc.split()[0] if measurement_desc else '', 
                case=False, na=False
            ))
        ]
        
        if not matching_ssr.empty:
            # Use the first matching SSR item
            ssr_item = matching_ssr.iloc[0]
            rate = ssr_item['rate']
        else:
            # Use default rate based on unit
            rate = unit_rates.get(measurement_unit, 1000.0)
        
        # Create abstract item
        amount = measurement['total'] * rate
        
        new_abstract_item = {
            "id": str(abstract_counter),
            "ssr_code": measurement.get('ssr_code', ''),
            "description": measurement['description'],
            "unit": measurement['unit'],
            "quantity": measurement['total'],
            "rate": rate,
            "amount": amount
        }
        
        st.session_state.abstract_items = pd.concat([
            st.session_state.abstract_items,
            pd.DataFrame([new_abstract_item])
        ], ignore_index=True)
        
        abstract_counter += 1
    
    return True, f"Generated {len(st.session_state.abstract_items)} abstract items from measurements"

def find_estimate_files(pattern="att*.xlsx"):
    """Find estimate files in attached_assets folder matching pattern"""
    attached_assets_path = os.path.join(os.path.dirname(__file__), "attached_assets")
    if not os.path.exists(attached_assets_path):
        return []
    
    import glob
    search_pattern = os.path.join(attached_assets_path, pattern)
    files = list(glob.glob(search_pattern))
    return sorted(files)

def import_excel_measurements(file_path):
    """Import measurements from Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ['item_no', 'description', 'unit', 'quantity', 'length', 'breadth', 'height']
        if not all(col in df.columns for col in required_columns):
            st.warning("Excel file missing required columns. Expected: item_no, description, unit, quantity, length, breadth, height")
            return False
        
        # Calculate totals
        df['total'] = df['quantity'] * df['length'] * df['breadth'] * df['height']
        df['id'] = range(1, len(df) + 1)
        df['ssr_code'] = ""
        
        # Update session state
        st.session_state.measurements = df[st.session_state.measurements.columns]
        st.session_state.counter = len(df) + 1
        
        st.success(f"✅ Imported {len(df)} measurements from {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        st.error(f"❌ Error importing Excel file: {str(e)}")
        return False

def import_ssr_from_excel(file_path):
    """Import SSR data from Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Validate required columns
        required_columns = ['code', 'description', 'category', 'unit', 'rate']
        if not all(col in df.columns for col in required_columns):
            st.warning("Excel file missing required columns. Expected: code, description, category, unit, rate")
            return False
        
        # Update session state
        st.session_state.ssr_items = df
        
        st.success(f"✅ Imported {len(df)} SSR items from {os.path.basename(file_path)}")
        return True
        
    except Exception as e:
        st.error(f"❌ Error importing SSR Excel file: {str(e)}")
        return False

def import_complete_estimate(file_path):
    """Import complete estimate from Excel file with all sheets and data"""
    try:
        # Read all sheets from Excel file
        all_sheets = pd.read_excel(file_path, sheet_name=None)
        
        # Process each sheet based on its name
        measurement_data = []
        abstract_data = []
        ssr_data = []
        
        for sheet_name, df in all_sheets.items():
            if 'measurement' in sheet_name.lower():
                # Process measurement sheet
                if not df.empty:
                    # Extract relevant columns for measurements
                    required_columns = ['item_no', 'description', 'unit', 'quantity', 'length', 'breadth', 'height']
                    available_columns = [col for col in required_columns if col in df.columns]
                    if available_columns:
                        measurement_df = df[available_columns].copy()
                        # Calculate totals if all dimension columns exist
                        if all(col in measurement_df.columns for col in ['quantity', 'length', 'breadth', 'height']):
                            measurement_df['total'] = (
                                measurement_df['quantity'] * 
                                measurement_df['length'] * 
                                measurement_df['breadth'] * 
                                measurement_df['height']
                            )
                        elif 'quantity' in measurement_df.columns:
                            measurement_df['total'] = measurement_df['quantity']
                        else:
                            measurement_df['total'] = 1
                        
                        # Add to measurements
                        measurement_data.append(measurement_df)
            
            elif 'abstract' in sheet_name.lower() and 'general' not in sheet_name.lower():
                # Process abstract sheet
                if not df.empty:
                    # Extract relevant columns for abstract
                    required_columns = ['description', 'unit', 'quantity', 'rate', 'amount']
                    available_columns = [col for col in required_columns if col in df.columns]
                    if available_columns:
                        abstract_df = df[available_columns].copy()
                        abstract_data.append(abstract_df)
            
            elif 'ssr' in sheet_name.lower() or 'schedule' in sheet_name.lower():
                # Process SSR sheet
                if not df.empty:
                    # Extract relevant columns for SSR
                    required_columns = ['code', 'description', 'category', 'unit', 'rate']
                    available_columns = [col for col in required_columns if col in df.columns]
                    if available_columns:
                        ssr_df = df[available_columns].copy()
                        ssr_data.append(ssr_df)
        
        # Update session state with imported data
        if measurement_data:
            # Combine all measurement data
            combined_measurements = pd.concat(measurement_data, ignore_index=True)
            # Add missing columns if needed
            for col in ['id', 'item_no', 'description', 'quantity', 'length', 'breadth', 'height', 'unit', 'total', 'ssr_code']:
                if col not in combined_measurements.columns:
                    if col == 'id':
                        combined_measurements[col] = range(1, len(combined_measurements) + 1)
                    elif col in ['quantity', 'length', 'breadth', 'height', 'total']:
                        combined_measurements[col] = 0.0
                    else:
                        combined_measurements[col] = ''
            st.session_state.measurements = combined_measurements[st.session_state.measurements.columns]
            st.session_state.counter = len(combined_measurements) + 1
        
        if abstract_data:
            # Combine all abstract data
            combined_abstracts = pd.concat(abstract_data, ignore_index=True)
            # Add missing columns if needed
            for col in ['id', 'description', 'quantity', 'unit', 'rate', 'amount']:
                if col not in combined_abstracts.columns:
                    if col == 'id':
                        combined_abstracts[col] = [str(i) for i in range(1, len(combined_abstracts) + 1)]
                    elif col in ['quantity', 'rate', 'amount']:
                        combined_abstracts[col] = 0.0
                    else:
                        combined_abstracts[col] = ''
            st.session_state.abstract_items = combined_abstracts[st.session_state.abstract_items.columns]
        
        if ssr_data:
            # Combine all SSR data
            combined_ssr = pd.concat(ssr_data, ignore_index=True)
            # Add missing columns if needed
            for col in ['code', 'description', 'category', 'unit', 'rate']:
                if col not in combined_ssr.columns:
                    if col in ['rate']:
                        combined_ssr[col] = 0.0
                    else:
                        combined_ssr[col] = ''
            st.session_state.ssr_items = combined_ssr
        
        return True
        
    except Exception as e:
        st.error(f"Error importing complete estimate: {str(e)}")
        return False

def auto_create_abstract_item(sheet_name, measurement_data, rate):
    """Automatically create abstract item from measurement"""
    abstract_item = {
        'id': get_next_id('abstract', sheet_name),
        'ssr_code': measurement_data['ssr_code'],
        'description': measurement_data['description'],
        'unit': measurement_data['unit'],
        'quantity': measurement_data['total'],  # Total from measurement
        'rate': rate,
        'amount': measurement_data['total'] * rate
    }
    
    st.session_state.abstract_sheets[sheet_name] = pd.concat([
        st.session_state.abstract_sheets[sheet_name],
        pd.DataFrame([abstract_item])
    ], ignore_index=True)

def auto_create_measurement_lines(sheet_name, abstract_item):
    """Create measurement lines with SAME DESCRIPTION as in estimate based on unit type"""
    unit = abstract_item['unit'].lower()
    description = abstract_item['description']  # Use EXACT same description as in estimate
    ssr_code = abstract_item['ssr_code']
    
    # Create measurement lines based on unit type with SAME DESCRIPTION
    lines_created = 0
    
    if unit in ['cum', 'cubic meter']:
        # For cubic units: create 3 blank formulated measurement lines
        measurement_templates = [
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0}   # Same description
        ]
    elif unit in ['sqm', 'square meter']:
        # For square units: create 2 blank formulated measurement lines
        measurement_templates = [
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 1},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 1}   # Same description
        ]
    elif unit in ['rm', 'meter', 'm']:
        # For linear units: create 2 blank formulated measurement lines
        measurement_templates = [
            {"desc": description, "qty": 1, "l": 0, "b": 1, "h": 1},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 1, "h": 1}   # Same description
        ]
    elif unit in ['nos', 'numbers']:
        # For numbers: create 2 blank formulated measurement lines
        measurement_templates = [
            {"desc": description, "qty": 0, "l": 1, "b": 1, "h": 1},  # Same description
            {"desc": description, "qty": 0, "l": 1, "b": 1, "h": 1}   # Same description
        ]
    else:
        # Default: create 3 blank formulated measurement lines
        measurement_templates = [
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0},  # Same description
            {"desc": description, "qty": 1, "l": 0, "b": 0, "h": 0}   # Same description
        ]
    
    # Create the blank formulated measurement lines with SAME DESCRIPTION and enhanced fields
    for i, template in enumerate(measurement_templates):
        measurement_line = {
            'id': get_next_id('measurement', sheet_name),
            'ssr_code': ssr_code,
            'item_no': f"{abstract_item['id']}.{i+1}",
            'description': template['desc'],  # EXACT SAME DESCRIPTION as in estimate
            'specification': '',  # Blank for user to fill
            'location': '',  # Blank for user to fill
            'quantity': template['qty'],
            'length': template['l'],
            'breadth': template['b'], 
            'height': template['h'],
            'diameter': 0,
            'thickness': 0,
            'unit': abstract_item['unit'],
            'total': template['qty'] * max(1, template['l']) * max(1, template['b']) * max(1, template['h']),
            'deduction': 0,
            'net_total': template['qty'] * max(1, template['l']) * max(1, template['b']) * max(1, template['h']),
            'remarks': ''
        }
        
        st.session_state.measurement_sheets[sheet_name] = pd.concat([
            st.session_state.measurement_sheets[sheet_name],
            pd.DataFrame([measurement_line])
        ], ignore_index=True)
        
        lines_created += 1
    
    return lines_created

def update_abstract_quantities_from_measurements(sheet_name):
    """Update abstract quantities from measurement totals"""
    if sheet_name not in st.session_state.abstract_sheets or sheet_name not in st.session_state.measurement_sheets:
        return
    
    abstracts = st.session_state.abstract_sheets[sheet_name].copy()
    measurements = st.session_state.measurement_sheets[sheet_name]
    
    # Update quantities for each abstract item
    for idx, abstract_row in abstracts.iterrows():
        # Find matching measurements by SSR code or description
        if abstract_row['ssr_code']:
            matching_measurements = measurements[
                (measurements['ssr_code'] == abstract_row['ssr_code']) & 
                (~measurements['description'].str.contains('SPECIFICATION:', case=False, na=False))
            ]
        else:
            # Match by description keywords
            desc_keywords = abstract_row['description'].lower().split()[:2]  # First 2 words
            matching_measurements = measurements[
                measurements['description'].str.lower().str.contains('|'.join(desc_keywords), case=False, na=False) &
                (~measurements['description'].str.contains('SPECIFICATION:', case=False, na=False))
            ]
        
        # Sum up the total quantities
        total_quantity = matching_measurements['total'].sum() if not matching_measurements.empty else 0
        
        # Update abstract item
        abstracts.loc[idx, 'quantity'] = total_quantity
        abstracts.loc[idx, 'amount'] = total_quantity * abstract_row['rate']
    
    # Update the session state
    st.session_state.abstract_sheets[sheet_name] = abstracts

def update_abstract_from_measurements():
    """Update all abstract sheets from measurement changes"""
    for sheet_name in st.session_state.measurement_sheets.keys():
        # Clear existing abstract items for this sheet
        clear_dataframe('abstracts', sheet_name)
        
        # Recreate abstract items from measurements
        measurements = st.session_state.measurement_sheets[sheet_name]
        for _, measurement in measurements.iterrows():
            if measurement['ssr_code']:
                ssr_item = st.session_state.ssr_items[
                    st.session_state.ssr_items['code'] == measurement['ssr_code']
                ]
                if not ssr_item.empty:
                    rate = ssr_item.iloc[0]['rate']
                    auto_create_abstract_item(sheet_name, measurement, rate)

def calculate_general_abstract_totals():
    """Calculate totals for General Abstract"""
    # Calculate civil work total from all abstract sheets
    civil_work_total = 0
    for sheet_name, abstracts in st.session_state.abstract_sheets.items():
        if not abstracts.empty:
            update_abstract_quantities_from_measurements(sheet_name)
            updated_abstracts = st.session_state.abstract_sheets[sheet_name]
            sheet_total = updated_abstracts['amount'].sum()
            civil_work_total += sheet_total
    
    # Get settings
    settings = st.session_state.general_abstract_settings
    
    # Calculate other parts
    sanitary_work_total = settings['sanitary_work_amount']
    electric_work_total = civil_work_total * (settings['electric_work_percentage'] / 100)
    electric_fixtures = civil_work_total * (settings['electric_fixtures_percentage'] / 100)
    
    # Calculate totals
    subtotal = civil_work_total + sanitary_work_total + electric_work_total
    grand_total = subtotal + electric_fixtures
    
    return {
        'civil_work': civil_work_total,
        'sanitary_work': sanitary_work_total,
        'electric_work': electric_work_total,
        'electric_fixtures': electric_fixtures,
        'subtotal': subtotal,
        'grand_total': grand_total
    }

# Dashboard Page
if page == "📊 Dashboard":
    st.title("📊 Project Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = create_standardized_columns('metrics')
    
    with col1:
        st.metric(
            "Total Measurements", 
            len(st.session_state.measurements),
            delta=None
        )
    
    with col2:
        st.metric(
            "SSR Items Available", 
            len(st.session_state.ssr_items),
            delta=None
        )
    
    with col3:
        st.metric(
            "Abstract Items", 
            len(st.session_state.abstract_items),
            delta=None
        )
    
    with col4:
        # Calculate total from General Abstract
        ga_totals = calculate_general_abstract_totals()
        total_cost = ga_totals['grand_total']
        st.metric(
            "Grand Total (General Abstract)", 
            f"₹{total_cost:,.0f}",
            delta=f"₹{ga_totals['civil_work']:,.0f} Civil Work"
        )
    
    # Recent Activity
    st.subheader("📈 Recent Measurements")
    if not st.session_state.measurements.empty:
        recent_measurements = st.session_state.measurements.tail(5)[
            ['item_no', 'description', 'unit', 'total']
        ].copy()
        recent_measurements['total'] = recent_measurements['total'].round(2)
        st.dataframe(recent_measurements, use_container_width=True, hide_index=True)
    else:
        st.info("No measurements added yet. Start by adding measurements in the Measurement Sheets section.")
    
    # Quick Stats
    st.subheader("📊 Quick Statistics")
    if not st.session_state.measurements.empty:
        col1, col2 = create_standardized_columns('stats')
        
        with col1:
            # Most used units
            unit_counts = st.session_state.measurements['unit'].value_counts()
            st.write("**Most Used Units:**")
            for unit, count in unit_counts.head(3).items():
                st.write(f"• {unit}: {count} items")
        
        with col2:
            # Total quantities by unit
            total_by_unit = st.session_state.measurements.groupby('unit')['total'].sum()
            st.write("**Total Quantities:**")
            for unit, total in total_by_unit.head(3).items():
                st.write(f"• {unit}: {total:.2f}")
    
    # General Abstract Quick Summary
    st.subheader("📋 General Abstract Summary")
    ga_totals = calculate_general_abstract_totals()
    
    if ga_totals['grand_total'] > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Civil Work", f"₹{ga_totals['civil_work']:,.0f}")
        with col2:
            st.metric("Sanitary Work", f"₹{ga_totals['sanitary_work']:,.0f}")
        with col3:
            st.metric("Electric Work", f"₹{ga_totals['electric_work']:,.0f}")
        with col4:
            st.metric("Grand Total", f"₹{ga_totals['grand_total']:,.0f}")
        
        # Progress indicator
        if ga_totals['civil_work'] > 0:
            progress = min(1.0, ga_totals['civil_work'] / 1000000)  # Assuming 10 lacs target
            st.progress(progress, text=f"Project Progress: ₹{ga_totals['civil_work']:,.0f} / ₹10,00,000 (estimated)")
        
        st.info("💡 **Tip:** Visit the 'General Abstract' section for detailed cost breakdown and export options.")
    else:
        st.info("📋 **General Abstract will show here once you add measurements and abstract items.**")
        st.write("**Quick Start:**")
        st.write("1. Go to 'Measurement Sheets' to add measurements")
        st.write("2. Go to 'Abstract of Cost' to create cost items") 
        st.write("3. View 'General Abstract' for complete project summary")

# General Abstract Page
elif page == "📋 General Abstract":
    st.title("📋 General Abstract of Cost")
    
    # Project Information Section
    with st.expander("🏗️ Project Information", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", 
                value="CONSTRUCTION OF COMMERCIAL COMPLEX FOR PANCHAYAT SAMITI GIRWA, UDAIPUR",
                help="Enter the complete project name")
            
            project_location = st.text_input("Location", 
                value="GIRWA, UDAIPUR",
                help="Project location")
        
        with col2:
            project_date = st.date_input("Estimate Date", value=datetime.now().date())
            
            engineer_name = st.text_input("Engineer Name", 
                value="CHARTERED ENGINEER, TEJHANS INVESTMENTS, UDAIPUR",
                help="Name and designation of the engineer")
    
    st.divider()
    
    # Calculate totals from all abstract sheets
    part_totals = {}
    grand_total = 0
    
    # Part A - Civil Work (from all measurement sheets)
    civil_work_total = 0
    for sheet_name, abstracts in st.session_state.abstract_sheets.items():
        if not abstracts.empty:
            # Update quantities from measurements first
            update_abstract_quantities_from_measurements(sheet_name)
            updated_abstracts = st.session_state.abstract_sheets[sheet_name]
            sheet_total = updated_abstracts['amount'].sum()
            civil_work_total += sheet_total
    
    part_totals['PART A - CIVIL WORK (BASEMENT, GROUND FLOOR AND FIRST FLOOR)'] = civil_work_total
    
    # Part B - Sanitary & Water Supply Work (fixed amount from ga.txt)
    sanitary_work_total = 81418.00
    part_totals['PART B - SANITARY & WATER SUPPLY WORK'] = sanitary_work_total
    
    # Part C - Electric Work (12% of Civil Work)
    electric_work_total = civil_work_total * 0.12
    part_totals['PART C - ELECTRIC WORK @ 12% OF Civil Work'] = electric_work_total
    
    # Subtotal
    subtotal = civil_work_total + sanitary_work_total + electric_work_total
    
    # Electric Fixtures (5% of Civil Work Part A)
    electric_fixtures = civil_work_total * 0.05
    
    # Grand Total
    grand_total = subtotal + electric_fixtures
    
    # Display General Abstract Table
    st.subheader("💰 General Abstract Summary")
    
    # Create the general abstract dataframe
    general_abstract_data = []
    
    for part_name, amount in part_totals.items():
        general_abstract_data.append({
            'S.No.': len(general_abstract_data) + 1,
            'Description': part_name,
            'Amount (Rs.)': amount
        })
    
    # Add subtotal
    general_abstract_data.append({
        'S.No.': '',
        'Description': 'TOTAL',
        'Amount (Rs.)': subtotal
    })
    
    # Add electric fixtures
    general_abstract_data.append({
        'S.No.': len(general_abstract_data),
        'Description': f'Add @ 5% for Electric Fixtures On Civil Work Part A (i.e. on Rs. {civil_work_total:,.2f})',
        'Amount (Rs.)': electric_fixtures
    })
    
    # Add grand total
    general_abstract_data.append({
        'S.No.': '',
        'Description': 'GRAND TOTAL',
        'Amount (Rs.)': grand_total
    })
    
    # Convert to DataFrame and display
    general_df = pd.DataFrame(general_abstract_data)
    
    # Custom styling for the table
    st.dataframe(
        general_df,
        column_config={
            "S.No.": st.column_config.TextColumn("S.No.", width="small"),
            "Description": st.column_config.TextColumn("Description", width="large"),
            "Amount (Rs.)": st.column_config.NumberColumn("Amount (Rs.)", format="₹%.2f", width="medium")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Summary Cards
    st.subheader("📊 Cost Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Civil Work (Part A)", 
            f"₹{civil_work_total:,.0f}",
            delta=f"{(civil_work_total/grand_total*100):.1f}% of total" if grand_total > 0 else None
        )
    
    with col2:
        st.metric(
            "Sanitary Work (Part B)", 
            f"₹{sanitary_work_total:,.0f}",
            delta=f"{(sanitary_work_total/grand_total*100):.1f}% of total" if grand_total > 0 else None
        )
    
    with col3:
        st.metric(
            "Electric Work (Part C)", 
            f"₹{electric_work_total:,.0f}",
            delta="12% of Civil Work"
        )
    
    with col4:
        st.metric(
            "Electric Fixtures", 
            f"₹{electric_fixtures:,.0f}",
            delta="5% of Civil Work"
        )
    
    # Grand Total Display
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #1f77b4;">
            <h2 style="color: #1f77b4; margin: 0;">GRAND TOTAL</h2>
            <h1 style="color: #1f77b4; margin: 10px 0;">₹{grand_total:,.2f}</h1>
            <p style="margin: 0; color: #666;">SAY ₹{round(grand_total):,}</p>
            <p style="margin: 0; color: #666;">{grand_total/100000:.2f} Lacs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Breakdown
    with st.expander("📋 Detailed Part-wise Breakdown"):
        st.subheader("Part A - Civil Work Breakdown")
        
        if civil_work_total > 0:
            # Show breakdown by measurement sheets
            civil_breakdown = []
            for sheet_name, abstracts in st.session_state.abstract_sheets.items():
                if not abstracts.empty:
                    update_abstract_quantities_from_measurements(sheet_name)
                    updated_abstracts = st.session_state.abstract_sheets[sheet_name]
                    sheet_total = updated_abstracts['amount'].sum()
                    if sheet_total > 0:
                        civil_breakdown.append({
                            'Floor/Part': sheet_name,
                            'Amount (Rs.)': sheet_total,
                            'Percentage': f"{(sheet_total/civil_work_total*100):.1f}%"
                        })
            
            if civil_breakdown:
                civil_df = pd.DataFrame(civil_breakdown)
                st.dataframe(
                    civil_df,
                    column_config={
                        "Floor/Part": "Floor/Part",
                        "Amount (Rs.)": st.column_config.NumberColumn("Amount (Rs.)", format="₹%.2f"),
                        "Percentage": "% of Civil Work"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No civil work data available. Add measurements and abstract items to see breakdown.")
        else:
            st.info("No civil work costs calculated yet. Add measurements and abstract items to see costs.")
        
        st.subheader("Part B - Sanitary & Water Supply Work")
        st.info(f"Fixed amount as per estimate: ₹{sanitary_work_total:,.2f}")
        
        st.subheader("Part C - Electric Work")
        st.info(f"Calculated as 12% of Civil Work: ₹{civil_work_total:,.2f} × 12% = ₹{electric_work_total:,.2f}")
        
        st.subheader("Electric Fixtures")
        st.info(f"Calculated as 5% of Civil Work: ₹{civil_work_total:,.2f} × 5% = ₹{electric_fixtures:,.2f}")
    
    # Export Options
    st.subheader("📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export General Abstract
        if st.button("📄 Export General Abstract CSV"):
            csv_data = general_df.to_csv(index=False)
            st.download_button(
                "📥 Download General Abstract CSV",
                data=csv_data,
                file_name=f"general_abstract_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    with col2:
        # Export Detailed Breakdown
        if civil_work_total > 0:
            if st.button("📊 Export Detailed Breakdown"):
                breakdown_data = {
                    'Project': [project_name] * 4,
                    'Part': ['Civil Work', 'Sanitary Work', 'Electric Work', 'Electric Fixtures'],
                    'Amount': [civil_work_total, sanitary_work_total, electric_work_total, electric_fixtures],
                    'Percentage': [
                        f"{(civil_work_total/grand_total*100):.1f}%",
                        f"{(sanitary_work_total/grand_total*100):.1f}%", 
                        f"{(electric_work_total/grand_total*100):.1f}%",
                        f"{(electric_fixtures/grand_total*100):.1f}%"
                    ]
                }
                breakdown_df = pd.DataFrame(breakdown_data)
                csv_breakdown = breakdown_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Breakdown CSV",
                    data=csv_breakdown,
                    file_name=f"cost_breakdown_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
    with col3:
        # Print-ready format
        if st.button("🖨️ Generate Print Format"):
            print_data = f"""
{project_name}

GENERAL ABSTRACT OF COST

PART 'A'  CIVIL WORK BASEMENT, GROUND FLOOR AND FIRST FLOOR    Rs. {civil_work_total:,.2f}

PART 'B'  SANITARY & WATER SUPPLY WORK                         Rs. {sanitary_work_total:,.2f}

PART 'C'  ELECTRIC WORK @ 12% OF Civil Work                    Rs. {electric_work_total:,.2f}

                                                    TOTAL Rs. {subtotal:,.2f}

Add @ 5% for Electric Fixtures On Civil Work Part 'A'
    i.e. on Rs. {civil_work_total:,.2f}                        Rs. {electric_fixtures:,.2f}
                                            GRAND TOTAL Rs. {grand_total:,.2f}

                                                SAY Rs. {round(grand_total):,}
                                                    {grand_total/100000:.2f} Lacs.

                        {engineer_name}
            """
            
            st.download_button(
                "📥 Download Print Format",
                data=print_data,
                file_name=f"general_abstract_print_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    # Notes and Instructions
    with st.expander("ℹ️ Notes and Instructions"):
        st.markdown("""
        **General Abstract Calculation Logic:**
        
        1. **Part A - Civil Work**: Automatically calculated from all measurement sheets and abstract items
        2. **Part B - Sanitary Work**: Fixed amount (₹81,418.00) as per original estimate
        3. **Part C - Electric Work**: Calculated as 12% of Civil Work (Part A)
        4. **Electric Fixtures**: Additional 5% of Civil Work (Part A)
        
        **To Update Costs:**
        - Add measurements in the "Measurement Sheets" section
        - Create abstract items in the "Abstract of Cost" section
        - The General Abstract will automatically update with real-time calculations
        
        **Export Options:**
        - **CSV Format**: For spreadsheet analysis
        - **Print Format**: Ready for official documentation
        - **Detailed Breakdown**: For cost analysis and reporting
        """)

# Abstract of Cost Page
elif page == "💰 Abstract of Cost":
    st.title("💰 Abstract of Cost")
    
    # Sheet selector (different floors/parts)
    available_abstract_sheets = list(st.session_state.abstract_sheets.keys())
    selected_abstract_sheet = st.selectbox("Select Abstract Sheet", available_abstract_sheets)
    st.write(f"**Current Sheet:** 💰 Abstract of Cost {selected_abstract_sheet}")
    
    # Show linkage info
    st.info(f"🔗 **Auto-Linkage:** Items in this sheet are linked to quantities from 'Measurement {selected_abstract_sheet}' sheet")
    
    # Add new abstract item form
    with st.expander("➕ Add New Abstract Item", expanded=True):
        # SSR Code Selection Section
        selected_ssr_abstract, ssr_item = create_ssr_selection_section("abstract")
        
        if ssr_item is not None:
            auto_description = ssr_item['description']
            auto_unit = ssr_item['unit'].title()
            auto_rate = ssr_item['rate']
        else:
            auto_description = ""
            auto_unit = "Cum"
            auto_rate = 0
        
        st.divider()
        
        with st.form("add_abstract_item"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                abs_item_no = st.text_input("Item No.", placeholder="1, 2, 3...")
                
                # Auto-select unit based on SSR or allow manual selection
                if selected_ssr_abstract != "Select SSR Code..." and auto_unit in UNITS:
                    unit_index = UNITS.index(auto_unit)
                    abs_unit = st.selectbox("Unit", UNITS, index=unit_index)
                else:
                    abs_unit = st.selectbox("Unit", UNITS)
                
                abs_rate = st.number_input("Rate (₹)", min_value=0.0, step=0.01, 
                                         value=auto_rate if selected_ssr_abstract != "Select SSR Code..." else 0.0)
            
            with col2:
                # Auto-populate description or allow manual entry
                if selected_ssr_abstract != "Select SSR Code...":
                    abs_description = st.text_area("Description", value=auto_description, 
                                                 help="Description auto-populated from SSR. You can modify if needed.")
                else:
                    abs_description = st.text_area("Description", placeholder="Enter detailed description of work item...")
                
                # Show measurement template based on unit
                st.write("**📏 Blank Measurement Lines (will be created automatically):**")
                if abs_unit.lower() in ['cum', 'cubic meter']:
                    st.caption("📐 Will create 3 blank lines with SAME DESCRIPTION: Nos × Length × Breadth × Height")
                elif abs_unit.lower() in ['sqm', 'square meter']:
                    st.caption("📐 Will create 2 blank lines with SAME DESCRIPTION: Nos × Length × Breadth")
                elif abs_unit.lower() in ['rm', 'meter', 'm']:
                    st.caption("📐 Will create 2 blank lines with SAME DESCRIPTION: Nos × Length")
                elif abs_unit.lower() in ['nos', 'numbers']:
                    st.caption("📐 Will create 2 blank lines with SAME DESCRIPTION: Nos (quantity only)")
                else:
                    st.caption("📐 Will create 3 blank lines with SAME DESCRIPTION: Nos × Length × Breadth × Height (default)")
            
            submitted_abstract = create_standardized_form_button("➕ Add Abstract Item & Create Measurement Lines", 'primary')
            
            if submitted_abstract and abs_description.strip():
                # Create abstract item
                new_abstract_item = {
                    'id': get_next_id('abstract', selected_abstract_sheet),
                    'ssr_code': selected_ssr_abstract if selected_ssr_abstract != "Select SSR Code..." else "",
                    'description': validate_and_strip(abs_description),
                    'unit': abs_unit,
                    'quantity': 0,  # Will be linked from measurement
                    'rate': abs_rate,
                    'amount': 0  # Will be calculated when measurement is added
                }
                
                # Add to abstract sheet
                st.session_state.abstract_sheets[selected_abstract_sheet] = pd.concat([
                    st.session_state.abstract_sheets[selected_abstract_sheet],
                    pd.DataFrame([new_abstract_item])
                ], ignore_index=True)
                
                # Auto-create corresponding measurement lines based on unit
                lines_created = auto_create_measurement_lines(selected_abstract_sheet, new_abstract_item)
                
                st.success(f"✅ Abstract item added to **{selected_abstract_sheet}** sheet!")
                st.success(f"📏 **Auto-created {lines_created} blank formulated measurement lines** with SAME DESCRIPTION in 'Measurement {selected_abstract_sheet}' sheet")
                if selected_ssr_abstract != "Select SSR Code...":
                    st.info(f"🏷️ **SSR Code:** {selected_ssr_abstract} linked to both sheets")
                st.rerun()
            elif submitted_abstract:
                st.error("Please enter a description for the abstract item.")
    
    # Display abstract items for selected sheet
    current_abstracts = st.session_state.abstract_sheets[selected_abstract_sheet]
    if not current_abstracts.empty:
        st.subheader(f"📋 Abstract of Cost {selected_abstract_sheet}")
        
        # Update quantities from measurements before displaying
        update_abstract_quantities_from_measurements(selected_abstract_sheet)
        
        # Display updated abstracts
        updated_abstracts = st.session_state.abstract_sheets[selected_abstract_sheet]
        
        # Add total row
        if len(updated_abstracts) > 0:
            subtotal = updated_abstracts['amount'].sum()
            total_row = pd.DataFrame([{
                'id': '',
                'ssr_code': '',
                'description': f'TOTAL {selected_abstract_sheet.upper()}',
                'unit': '',
                'quantity': '',
                'rate': '',
                'amount': subtotal
            }])
            display_abstracts = pd.concat([updated_abstracts, total_row], ignore_index=True)
        else:
            display_abstracts = updated_abstracts
        
        st.dataframe(
            display_abstracts,
            column_config={
                "id": "S.No.",
                "ssr_code": "SSR Code",
                "description": st.column_config.TextColumn("Description", width="large"),
                "unit": "Unit",
                "quantity": st.column_config.NumberColumn("Quantity", format="%.2f"),
                "rate": st.column_config.NumberColumn("Rate (₹)", format="%.2f"),
                "amount": st.column_config.NumberColumn("Amount (₹)", format="%.2f")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Show measurement linkage info
        st.info(f"💡 **Quantities auto-update** from Measurement {selected_abstract_sheet} sheet. Go to Measurement Sheets to enter dimensions.")
        
        # Cost summary for this sheet
        if len(updated_abstracts) > 0:
            col1, col2, col3 = create_standardized_columns('actions')
            with col1:
                st.metric("Items", len(updated_abstracts))
            with col2:
                total_qty = updated_abstracts['quantity'].sum()
                st.metric("Total Quantity", f"{total_qty:.2f}")
            with col3:
                total_amount = updated_abstracts['amount'].sum()
                st.metric("Total Amount", f"₹{total_amount:,.2f}")
    
    else:
        st.info(f"No abstract items in {selected_abstract_sheet} sheet yet. Add items using the form above.")
        
        # Show sample measurement structure
        st.subheader("📏 How it Works:")
        st.write("**When you add an Abstract item, the system automatically creates:**")
        st.write("1. **2-3 Blank formulated measurement lines** with SAME DESCRIPTION as in estimate")
        st.write("2. **Unit-based formula structure** - Based on unit type:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**📐 Cum (Cubic):** 3 blank lines")
            st.caption("- Formula: Nos × Length × Breadth × Height")
            st.write("**📐 Sqm (Square):** 2 blank lines") 
            st.caption("- Formula: Nos × Length × Breadth")
        with col2:
            st.write("**📐 RM/Meter (Linear):** 2 blank lines")
            st.caption("- Formula: Nos × Length")
            st.write("**📐 Nos (Numbers):** 2 blank lines")
            st.caption("- Formula: Nos (quantity only)")
        
        st.write("3. **Same item description** - All measurement lines use exact same description as Abstract item")
        st.write("4. **Auto-linked totals** - Measurements feed into Abstract quantities")
        st.write("5. **Real-time updates** - Change measurements, see instant cost updates")

    # General Abstract Summary (combining all sheets)
    st.divider()
    st.subheader("📊 General Abstract Summary")
    
    # Calculate totals from all abstract sheets
    all_sheet_totals = []
    grand_total = 0
    
    for sheet_name, abstracts in st.session_state.abstract_sheets.items():
        if not abstracts.empty:
            # Update quantities first
            update_abstract_quantities_from_measurements(sheet_name)
            updated_abstracts = st.session_state.abstract_sheets[sheet_name]
            sheet_total = updated_abstracts['amount'].sum()
            all_sheet_totals.append({
                'Sheet': sheet_name,
                'Amount': sheet_total
            })
            grand_total += sheet_total
    
    if all_sheet_totals:
        # Display sheet totals
        totals_df = pd.DataFrame(all_sheet_totals)
        
        # Add grand total row
        grand_total_row = pd.DataFrame([{
            'Sheet': 'GRAND TOTAL',
            'Amount': grand_total
        }])
        totals_display = pd.concat([totals_df, grand_total_row], ignore_index=True)
        
        st.dataframe(
            totals_display,
            column_config={
                "Sheet": st.column_config.TextColumn("Part/Floor", width="medium"),
                "Amount": st.column_config.NumberColumn("Amount (₹)", format="%.2f")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Additional charges calculation
        st.subheader("💹 Final Cost Calculation")
        
        col1, col2 = create_standardized_columns('cost_calc')
        with col1:
            st.write("**Subtotal (All Parts):**")
            st.write("**Add 7% Electrification:**")
            st.write("**Total after Electrification:**")
            st.write("**Add 13% Prorata Charges:**")
            st.write("---")
            st.write("**FINAL TOTAL:**")
        
        with col2:
            electrification = grand_total * 0.07
            after_electrification = grand_total + electrification
            prorata = after_electrification * 0.13
            final_total = after_electrification + prorata
            
            st.write(f"₹{grand_total:,.2f}")
            st.write(f"₹{electrification:,.2f}")
            st.write(f"₹{after_electrification:,.2f}")
            st.write(f"₹{prorata:,.2f}")
            st.write("---")
            st.write(f"**₹{final_total:,.2f}**")
        
        # Export options
        col1, col2 = create_standardized_columns('export')
        
        with col1:
            # Export all abstract sheets combined
            all_abstracts = []
            for sheet_name, abstracts in st.session_state.abstract_sheets.items():
                if not abstracts.empty:
                    sheet_abstracts = abstracts.copy()
                    sheet_abstracts['Sheet'] = sheet_name
                    all_abstracts.append(sheet_abstracts)
            
            if all_abstracts:
                combined_abstracts = pd.concat(all_abstracts, ignore_index=True)
                create_export_button(
                    combined_abstracts,
                    "combined_abstract",
                    "📥 Export Combined Abstract CSV",
                    "combined_abstract"
                )
        
        with col2:
            # Cost breakdown
            breakdown_data = {
                'Category': ['Subtotal', 'Electrification (7%)', 'Prorata Charges (13%)', 'FINAL TOTAL'],
                'Amount': [grand_total, electrification, prorata, final_total]
            }
            breakdown_df = pd.DataFrame(breakdown_data)
            create_export_button(
                breakdown_df,
                "cost_breakdown", 
                "📥 Export Cost Breakdown",
                "cost_breakdown"
            )
    
    else:
        st.info("No abstract items available. Add items to individual sheets to see the General Abstract summary.")
        
        # Auto-generate functionality for legacy measurements
        if not st.session_state.measurements.empty and not st.session_state.ssr_items.empty:
            st.subheader("🔄 Auto-Generate from Legacy Measurements")
            col1, col2 = create_standardized_columns('cost_calc')
            
            with col1:
                st.info("💡 You can auto-generate abstract items by matching measurements with SSR rates")
            
            with col2:
                if create_standardized_button("🔄 Auto-Generate Abstract", 'primary'):
                    success, message = auto_generate_abstracts_from_measurements()
                    if success:
                        st.success(f"✅ {message}")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

# Measurement Sheets Page
elif page == "📝 Measurement Sheets":
    st.title("📝 Measurement Sheets")
    
    # Sheet selector (different floors/parts)
    available_sheets = list(st.session_state.measurement_sheets.keys())
    selected_sheet = st.selectbox("Select Measurement Sheet", available_sheets)
    st.write(f"**Current Sheet:** 📏 Measurement {selected_sheet}")
    
    # Show linkage info
    st.info(f"💡 **Auto-Linkage:** Measurements in this sheet automatically feed quantities into 'Abstract of Cost {selected_sheet}' sheet")
    
    # Enhanced measurement form with complex measurement support
    with st.expander("➕ Add New Measurement", expanded=True):
        # SSR Code Selection Section
        selected_ssr, ssr_item = create_ssr_selection_section("measurement")
        
        if ssr_item is not None:
            auto_description = ssr_item['description']
            auto_unit = ssr_item['unit'].title()
            auto_rate = ssr_item['rate']
        else:
            auto_description = ""
            auto_unit = "Cum"
            auto_rate = 0
        
        st.divider()
        
        with st.form("add_measurement"):
            # Basic Item Information
            col1, col2 = st.columns([1, 2])
            
            with col1:
                item_no = st.text_input("Item No.", placeholder="1, 2, 3...")
                
                # Auto-select unit based on SSR or allow manual selection
                if selected_ssr != "Select SSR Code..." and auto_unit in UNITS:
                    unit_index = UNITS.index(auto_unit)
                    unit = st.selectbox("Unit", UNITS, index=unit_index)
                else:
                    unit = st.selectbox("Unit", UNITS)
                
                # Measurement type selection
                measurement_type = st.selectbox("Calculation Type", list(MEASUREMENT_TYPES.keys()))
                st.caption(f"Formula: {MEASUREMENT_TYPES[measurement_type]}")
            
            with col2:
                # Auto-populate description or allow manual entry
                if selected_ssr != "Select SSR Code...":
                    description = st.text_area("Description", value=auto_description, 
                                             help="Description auto-populated from SSR. You can modify if needed.")
                else:
                    description = st.text_area("Description", placeholder="Enter detailed description of work item...")
                
                # Additional fields for complex measurements
                col2a, col2b = st.columns(2)
                with col2a:
                    specification = st.text_input("Specification", placeholder="e.g., M25 grade, 230mm thick")
                with col2b:
                    location = st.text_input("Location", placeholder="e.g., Ground Floor, Back Side")
            
            # Dynamic measurement inputs based on type
            st.subheader("📐 Measurement Dimensions")
            
            if measurement_type in ["Standard", "Volume"]:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    breadth = st.number_input("Breadth (m)", min_value=0.0, step=0.01, value=0.0)
                with col4:
                    height = st.number_input("Height (m)", min_value=0.0, step=0.01, value=0.0)
                diameter = thickness = 0
                
            elif measurement_type == "Linear":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    st.write("*Not applicable*")
                    breadth = 1.0
                with col4:
                    st.write("*Not applicable*")
                    height = 1.0
                diameter = thickness = 0
                
            elif measurement_type == "Area":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    breadth = st.number_input("Breadth (m)", min_value=0.0, step=0.01, value=0.0)
                with col4:
                    st.write("*Not applicable*")
                    height = 1.0
                diameter = thickness = 0
                
            elif measurement_type in ["Circular Area", "Circular Volume"]:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    diameter = st.number_input("Diameter (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    if measurement_type == "Circular Volume":
                        height = st.number_input("Height (m)", min_value=0.0, step=0.01, value=0.0)
                    else:
                        st.write("*Not applicable*")
                        height = 1.0
                with col4:
                    thickness = st.number_input("Thickness (m)", min_value=0.0, step=0.01, value=0.0)
                length = breadth = 1.0
                
            elif measurement_type == "Weight":
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    thickness = st.number_input("Thickness/Cross-section (m²)", min_value=0.0, step=0.001, value=0.0)
                with col4:
                    st.caption("Unit Weight: 7.85 kg/m³ (Steel)")
                breadth = height = diameter = 1.0
                
            else:  # Custom or other types
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    quantity = st.number_input("Quantity/Nos", min_value=0.0, step=0.01, value=1.0)
                with col2:
                    length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
                with col3:
                    breadth = st.number_input("Breadth (m)", min_value=0.0, step=0.01, value=0.0)
                with col4:
                    height = st.number_input("Height (m)", min_value=0.0, step=0.01, value=0.0)
                
                # Additional dimensions for complex calculations
                col5, col6 = st.columns(2)
                with col5:
                    diameter = st.number_input("Diameter (m)", min_value=0.0, step=0.01, value=0.0)
                with col6:
                    thickness = st.number_input("Thickness (m)", min_value=0.0, step=0.01, value=0.0)
            
            # Deduction section
            st.subheader("➖ Deductions (Optional)")
            col1, col2 = st.columns(2)
            with col1:
                deduction = st.number_input("Deduction Quantity", min_value=0.0, step=0.01, value=0.0)
            with col2:
                remarks = st.text_input("Remarks", placeholder="Additional notes or calculations")
            
            # Calculate and display total
            gross_total = calculate_total(quantity, length, breadth, height, diameter, thickness, measurement_type)
            net_total = max(0, gross_total - deduction)
            
            # Show calculation breakdown
            st.subheader("📊 Calculation Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Gross Total", f"{gross_total:.3f} {unit}")
                if measurement_type == "Circular Area" and diameter > 0:
                    st.caption(f"π × ({diameter/2:.2f})² × {quantity:.0f} = {gross_total:.3f}")
                elif measurement_type == "Circular Volume" and diameter > 0:
                    st.caption(f"π × ({diameter/2:.2f})² × {height:.2f} × {quantity:.0f} = {gross_total:.3f}")
                elif measurement_type == "Linear":
                    st.caption(f"{quantity:.2f} × {length:.2f} = {gross_total:.3f}")
                elif measurement_type == "Area":
                    st.caption(f"{quantity:.2f} × {length:.2f} × {breadth:.2f} = {gross_total:.3f}")
                else:
                    st.caption(f"{quantity:.2f} × {length:.2f} × {breadth:.2f} × {height:.2f} = {gross_total:.3f}")
            
            with col2:
                if deduction > 0:
                    st.metric("Deductions", f"{deduction:.3f} {unit}", delta=f"-{deduction:.3f}")
                else:
                    st.metric("Deductions", "0.00", delta="None")
            
            with col3:
                st.metric("Net Total", f"{net_total:.3f} {unit}", delta=f"{net_total-gross_total:.3f}" if deduction > 0 else None)
                
                # Show estimated cost if SSR is selected
                if selected_ssr != "Select SSR Code..." and net_total > 0:
                    estimated_cost = net_total * auto_rate
                    st.metric("Estimated Cost", f"₹{estimated_cost:,.2f}")
            
            submitted = create_standardized_form_button("➕ Add Measurement", 'primary')
            
            if submitted and description.strip():
                new_measurement = {
                    'id': get_next_id('measurement', selected_sheet),
                    'ssr_code': selected_ssr if selected_ssr != "Select SSR Code..." else "",
                    'item_no': item_no,
                    'description': validate_and_strip(description),
                    'specification': validate_and_strip(specification),
                    'location': validate_and_strip(location),
                    'quantity': quantity,
                    'length': length,
                    'breadth': breadth,
                    'height': height,
                    'diameter': diameter,
                    'thickness': thickness,
                    'unit': unit,
                    'total': net_total,
                    'deduction': deduction,
                    'net_total': net_total,
                    'remarks': validate_and_strip(remarks)
                }
                
                # Add to selected measurement sheet
                st.session_state.measurement_sheets[selected_sheet] = pd.concat([
                    st.session_state.measurement_sheets[selected_sheet],
                    pd.DataFrame([new_measurement])
                ], ignore_index=True)
                
                # Auto-create corresponding abstract item if SSR code is selected
                if selected_ssr != "Select SSR Code...":
                    auto_create_abstract_item(selected_sheet, new_measurement, auto_rate)
                    st.success(f"✅ Measurement added to **{selected_sheet}** sheet with SSR Code: **{selected_ssr}**")
                    st.success(f"🔗 **Auto-linked** to Abstract of Cost {selected_sheet} | Estimated Cost: **₹{net_total * auto_rate:,.2f}**")
                else:
                    st.success(f"✅ Measurement added to **{selected_sheet}** sheet!")
                st.rerun()
            elif submitted:
                st.error("Please enter a description for the measurement.")
    
    # Display measurements for selected sheet
    current_measurements = st.session_state.measurement_sheets[selected_sheet]
    if not current_measurements.empty:
        st.subheader(f"📋 Measurement {selected_sheet}")
        
        # Create display dataframe
        display_df = current_measurements.copy()
        
        # Add total row with enhanced columns
        if len(display_df) > 0:
            total_gross = display_df['total'].sum() if 'total' in display_df.columns else 0
            total_deductions = display_df['deduction'].sum() if 'deduction' in display_df.columns else 0
            total_net = display_df['net_total'].sum() if 'net_total' in display_df.columns else total_gross
            
            total_row = pd.DataFrame([{
                'id': '',
                'ssr_code': '',
                'item_no': 'TOTAL',
                'description': f'Total {selected_sheet}',
                'specification': '',
                'location': '',
                'quantity': '',
                'length': '',
                'breadth': '',
                'height': '',
                'diameter': '',
                'thickness': '',
                'unit': display_df.iloc[0]['unit'] if len(display_df) > 0 else '',
                'total': total_gross,
                'deduction': total_deductions,
                'net_total': total_net,
                'remarks': f'{len(display_df)} items'
            }])
            display_df = pd.concat([display_df, total_row], ignore_index=True)
        
        # Enhanced display table with all measurement fields
        display_columns = {
            "id": None,
            "item_no": "Item No.",
            "description": st.column_config.TextColumn("Description", width="large"),
            "specification": st.column_config.TextColumn("Specification", width="medium"),
            "location": st.column_config.TextColumn("Location", width="medium"),
            "quantity": st.column_config.NumberColumn("Qty", format="%.2f"),
            "length": st.column_config.NumberColumn("Length", format="%.3f"),
            "breadth": st.column_config.NumberColumn("Breadth", format="%.3f"),
            "height": st.column_config.NumberColumn("Height", format="%.3f"),
            "diameter": st.column_config.NumberColumn("Diameter", format="%.3f"),
            "thickness": st.column_config.NumberColumn("Thickness", format="%.3f"),
            "unit": "Unit",
            "total": st.column_config.NumberColumn("Gross Total", format="%.3f"),
            "deduction": st.column_config.NumberColumn("Deductions", format="%.3f"),
            "net_total": st.column_config.NumberColumn("Net Total", format="%.3f"),
            "remarks": st.column_config.TextColumn("Remarks", width="medium")
        }
        
        # Add SSR code column
        if 'ssr_code' in display_df.columns:
            display_columns["ssr_code"] = "SSR Code"
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Complete View", "📏 Dimensions Only", "📊 Summary View"])
        
        with tab1:
            # Show all columns
            st.dataframe(
                display_df,
                column_config=display_columns,
                hide_index=True,
                use_container_width=True
            )
        
        with tab2:
            # Show only dimension-related columns
            dimension_columns = {
                "item_no": "Item No.",
                "description": st.column_config.TextColumn("Description", width="large"),
                "quantity": st.column_config.NumberColumn("Qty", format="%.2f"),
                "length": st.column_config.NumberColumn("Length", format="%.3f"),
                "breadth": st.column_config.NumberColumn("Breadth", format="%.3f"),
                "height": st.column_config.NumberColumn("Height", format="%.3f"),
                "unit": "Unit",
                "net_total": st.column_config.NumberColumn("Net Total", format="%.3f")
            }
            st.dataframe(
                display_df[list(dimension_columns.keys())],
                column_config=dimension_columns,
                hide_index=True,
                use_container_width=True
            )
        
        with tab3:
            # Show summary view
            summary_columns = {
                "item_no": "Item No.",
                "description": st.column_config.TextColumn("Description", width="large"),
                "specification": st.column_config.TextColumn("Specification", width="medium"),
                "unit": "Unit",
                "net_total": st.column_config.NumberColumn("Net Total", format="%.3f"),
                "remarks": st.column_config.TextColumn("Remarks", width="medium")
            }
            st.dataframe(
                display_df[list(summary_columns.keys())],
                column_config=summary_columns,
                hide_index=True,
                use_container_width=True
            )
        
        st.dataframe(
            display_df,
            column_config=display_columns,
            hide_index=True,
            use_container_width=True
        )
        
        # Action buttons
        col1, col2, col3 = create_standardized_columns('actions')
        with col1:
            create_export_button(
                st.session_state.measurements, 
                "measurements", 
                "📥 Export CSV",
                "measurements"
            )
        
        with col2:
            if create_standardized_button("🗑️ Clear All", 'danger'):
                if st.session_state.get('confirm_clear', False):
                    clear_dataframe('measurements')
                    st.session_state.confirm_clear = False
                    st.success("All measurements cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm clearing all measurements.")
        
        with col3:
            if create_standardized_button("🔄 Reset Confirmation", 'secondary'):
                st.session_state.confirm_clear = False
        
        # Measurement Analysis Section
        st.subheader("📊 Measurement Analysis")
        
        analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
        
        with analysis_col1:
            # Unit-wise summary
            if not current_measurements.empty:
                unit_summary = current_measurements.groupby('unit')['net_total'].agg(['count', 'sum']).round(3)
                unit_summary.columns = ['Items', 'Total Quantity']
                st.write("**📏 Unit-wise Summary:**")
                st.dataframe(unit_summary, use_container_width=True)
        
        with analysis_col2:
            # Location-wise summary (if locations are specified)
            if not current_measurements.empty and 'location' in current_measurements.columns:
                location_data = current_measurements[current_measurements['location'].str.strip() != '']
                if not location_data.empty:
                    location_summary = location_data.groupby('location')['net_total'].sum().round(3)
                    st.write("**📍 Location-wise Totals:**")
                    st.dataframe(location_summary.to_frame('Total Quantity'), use_container_width=True)
                else:
                    st.info("No location data specified")
        
        with analysis_col3:
            # Deduction analysis
            if not current_measurements.empty and 'deduction' in current_measurements.columns:
                total_deductions = current_measurements['deduction'].sum()
                items_with_deductions = (current_measurements['deduction'] > 0).sum()
                
                st.write("**➖ Deduction Analysis:**")
                st.metric("Total Deductions", f"{total_deductions:.3f}")
                st.metric("Items with Deductions", items_with_deductions)
                
                if total_deductions > 0:
                    deduction_items = current_measurements[current_measurements['deduction'] > 0][
                        ['item_no', 'description', 'deduction', 'unit']
                    ]
                    with st.expander("View Deduction Details"):
                        st.dataframe(deduction_items, hide_index=True, use_container_width=True)
        
        # Measurement Validation
        if not current_measurements.empty:
            st.subheader("🔍 Measurement Validation")
            
            validation_issues = []
            
            # Check for zero quantities
            zero_quantities = current_measurements[current_measurements['net_total'] <= 0]
            if not zero_quantities.empty:
                validation_issues.append({
                    'Issue': 'Zero/Negative Quantities',
                    'Count': len(zero_quantities),
                    'Items': ', '.join(zero_quantities['item_no'].astype(str).tolist()[:5])
                })
            
            # Check for missing descriptions
            missing_desc = current_measurements[current_measurements['description'].str.strip() == '']
            if not missing_desc.empty:
                validation_issues.append({
                    'Issue': 'Missing Descriptions',
                    'Count': len(missing_desc),
                    'Items': ', '.join(missing_desc['item_no'].astype(str).tolist()[:5])
                })
            
            # Check for unusual dimensions (very large or very small)
            unusual_dims = current_measurements[
                (current_measurements['length'] > 1000) | 
                (current_measurements['breadth'] > 1000) | 
                (current_measurements['height'] > 100) |
                ((current_measurements['length'] > 0) & (current_measurements['length'] < 0.01))
            ]
            if not unusual_dims.empty:
                validation_issues.append({
                    'Issue': 'Unusual Dimensions',
                    'Count': len(unusual_dims),
                    'Items': ', '.join(unusual_dims['item_no'].astype(str).tolist()[:5])
                })
            
            # Check for deductions greater than gross quantities
            invalid_deductions = current_measurements[current_measurements['deduction'] > current_measurements['total']]
            if not invalid_deductions.empty:
                validation_issues.append({
                    'Issue': 'Deductions > Gross Total',
                    'Count': len(invalid_deductions),
                    'Items': ', '.join(invalid_deductions['item_no'].astype(str).tolist()[:5])
                })
            
            if validation_issues:
                st.warning("⚠️ **Validation Issues Found:**")
                validation_df = pd.DataFrame(validation_issues)
                st.dataframe(validation_df, hide_index=True, use_container_width=True)
            else:
                st.success("✅ **All measurements validated successfully!**")
    else:
        st.info("No measurements added yet. Use the form above to add your first measurement.")
        
        # Show sample measurement structure based on the PDF
        with st.expander("📋 Sample Measurement Structure (Based on Construction Projects)"):
            st.write("**Example measurement patterns from construction estimates:**")
            
            sample_data = [
                {
                    "Type": "Earth Work Excavation",
                    "Pattern": "Average Width × Length × Depth",
                    "Example": "34.14 × 37.80 × 1.20 = 1548.59 Cum"
                },
                {
                    "Type": "Concrete Footings", 
                    "Pattern": "Multiple footings with different sizes",
                    "Example": "F1: 2.00×2.30×0.30, F2: 2.40×2.70×0.30, etc."
                },
                {
                    "Type": "RCC Columns",
                    "Pattern": "Cross-section × Height × Quantity", 
                    "Example": "C1: 0.30×0.60×3.25, C2: 0.45×0.68×3.25, etc."
                },
                {
                    "Type": "Brick Work with Deductions",
                    "Pattern": "Gross Area - Door/Window Openings",
                    "Example": "Wall Area - (Doors + Windows + Ventilators)"
                },
                {
                    "Type": "Steel Reinforcement",
                    "Pattern": "Concrete Volume × Steel Rate per Cum",
                    "Example": "Footings: 72.03 Cum @ 25 Kg/Cum = 1801 Kg"
                }
            ]
            
            st.table(pd.DataFrame(sample_data))
            
            st.info("💡 **Tip:** Use the enhanced measurement form above to handle all these complex calculation patterns!")
    
    # Bulk measurement import section
    with st.expander("📥 Bulk Import Measurements (For Complex Projects)"):
        st.write("**Import multiple measurements from structured data:**")
        
        # Template download
        col1, col2 = st.columns(2)
        with col1:
            st.write("**📋 Download Template:**")
            template_data = pd.DataFrame([
                {
                    'item_no': '1',
                    'description': 'Earth work excavation in foundation trenches',
                    'specification': 'All kinds of soil, lift up to 1.5m',
                    'location': 'Foundation area',
                    'quantity': 1,
                    'length': 34.14,
                    'breadth': 37.80,
                    'height': 1.20,
                    'diameter': 0,
                    'thickness': 0,
                    'unit': 'Cum',
                    'deduction': 0,
                    'remarks': 'Average width calculation'
                },
                {
                    'item_no': '2',
                    'description': 'Cement concrete 1:4:8 in footings',
                    'specification': 'M15 grade with 40mm aggregate',
                    'location': 'Footing F1',
                    'quantity': 1,
                    'length': 2.00,
                    'breadth': 2.30,
                    'height': 0.30,
                    'diameter': 0,
                    'thickness': 0,
                    'unit': 'Cum',
                    'deduction': 0,
                    'remarks': 'Individual footing'
                }
            ])
            
            csv_template = template_data.to_csv(index=False)
            st.download_button(
                "📥 Download CSV Template",
                data=csv_template,
                file_name=f"measurement_template_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.write("**📤 Upload Bulk Data:**")
            uploaded_bulk = st.file_uploader("Upload CSV with measurements", type=['csv'])
            
            if uploaded_bulk is not None:
                try:
                    bulk_df = pd.read_csv(uploaded_bulk)
                    
                    # Validate required columns
                    required_cols = ['item_no', 'description', 'quantity', 'length', 'breadth', 'height', 'unit']
                    missing_cols = [col for col in required_cols if col not in bulk_df.columns]
                    
                    if missing_cols:
                        st.error(f"Missing required columns: {', '.join(missing_cols)}")
                    else:
                        st.success(f"✅ Found {len(bulk_df)} measurements to import")
                        
                        if st.button("🚀 Import All Measurements"):
                            # Add missing columns with defaults
                            for col in MEASUREMENT_COLUMNS:
                                if col not in bulk_df.columns:
                                    if col in ['diameter', 'thickness', 'deduction']:
                                        bulk_df[col] = 0
                                    elif col in ['specification', 'location', 'remarks', 'ssr_code']:
                                        bulk_df[col] = ''
                                    elif col == 'id':
                                        bulk_df[col] = range(1, len(bulk_df) + 1)
                                    elif col in ['total', 'net_total']:
                                        bulk_df[col] = bulk_df['quantity'] * bulk_df['length'] * bulk_df['breadth'] * bulk_df['height']
                            
                            # Add to selected sheet
                            st.session_state.measurement_sheets[selected_sheet] = pd.concat([
                                st.session_state.measurement_sheets[selected_sheet],
                                bulk_df[MEASUREMENT_COLUMNS]
                            ], ignore_index=True)
                            
                            st.success(f"✅ Successfully imported {len(bulk_df)} measurements to {selected_sheet}!")
                            st.rerun()
                            
                except Exception as e:
                    st.error(f"Error reading CSV file: {str(e)}")
        
        # Show preview of uploaded data
        if uploaded_bulk is not None:
            try:
                preview_df = pd.read_csv(uploaded_bulk)
                st.write("**📋 Preview of uploaded data:**")
                st.dataframe(preview_df.head(), use_container_width=True)
            except:
                pass

# SSR Database Page
elif page == "📚 SSR Database":
    st.title("📚 Standard Schedule of Rates (SSR)")
    
    # Search and filter section
    col1, col2, col3 = create_standardized_columns('search')
    with col1:
        search_term = st.text_input("🔍 Search SSR Items", placeholder="Search by code or description...")
    with col2:
        categories = ["All Categories"] + sorted(st.session_state.ssr_items['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
    with col3:
        # Quick code search
        quick_codes = ["Quick Search..."] + st.session_state.ssr_items['code'].tolist()
        quick_code = st.selectbox("Jump to Code", quick_codes)
    
    # Filter SSR items
    filtered_ssr = st.session_state.ssr_items.copy()
    
    # Apply quick code search first
    if quick_code != "Quick Search...":
        filtered_ssr = filtered_ssr[filtered_ssr['code'] == quick_code]
        st.info(f"🎯 Showing details for SSR Code: **{quick_code}**")
    else:
        # Apply text search
        if search_term:
            mask = (
                filtered_ssr['code'].str.contains(search_term, case=False, na=False) |
                filtered_ssr['description'].str.contains(search_term, case=False, na=False)
            )
            filtered_ssr = filtered_ssr[mask]
        
        # Apply category filter
        if selected_category != "All Categories":
            filtered_ssr = filtered_ssr[filtered_ssr['category'] == selected_category]
    
    # Display results count
    st.write(f"**Showing {len(filtered_ssr)} of {len(st.session_state.ssr_items)} items**")
    
    # Display SSR table with enhanced features
    if not filtered_ssr.empty:
        st.write(f"**Showing {len(filtered_ssr)} of {len(st.session_state.ssr_items)} SSR items**")
        
        # Highlight selected item if using quick search
        if quick_code != "Quick Search...":
            selected_item = filtered_ssr.iloc[0]
            
            # Show detailed card for selected item
            with st.container():
                st.markdown(f"""
                <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;">
                    <h3>🏷️ SSR Code: {selected_item['code']}</h3>
                    <p><strong>📋 Description:</strong> {selected_item['description']}</p>
                    <p><strong>📂 Category:</strong> {selected_item['category']}</p>
                    <p><strong>📏 Unit:</strong> {selected_item['unit']}</p>
                    <p><strong>💰 Rate:</strong> ₹{selected_item['rate']:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.info("💡 **Tip:** Use this code in Measurement Sheets to auto-populate description and rate!")
        
        # Display full table
        st.dataframe(
            filtered_ssr,
            column_config={
                "code": "SSR Code",
                "description": st.column_config.TextColumn("Description", width="large"),
                "category": "Category",
                "unit": "Unit",
                "rate": st.column_config.NumberColumn("Rate (₹)", format="%.2f")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("No SSR items found matching your search criteria.")
    
    # Add new SSR item
    with st.expander("➕ Add New SSR Item"):
        with st.form("add_ssr_item"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_code = st.text_input("SSR Code", placeholder="e.g., 11.1.1")
                new_category = st.text_input("Category", placeholder="e.g., Concrete Work")
                new_unit = st.selectbox("Unit", UNITS)
            
            with col2:
                new_description = st.text_area("Description", placeholder="Enter detailed description...")
                new_rate = st.number_input("Rate (₹)", min_value=0.0, step=0.01)
            
            submitted = create_standardized_form_button("➕ Add SSR Item", 'primary')
            
            if submitted and new_code and new_description and new_category:
                # Check if code already exists
                if new_code in st.session_state.ssr_items['code'].values:
                    st.error(f"SSR Code '{new_code}' already exists!")
                else:
                    new_ssr_item = {
                        "code": new_code,
                        "description": validate_and_strip(new_description),
                        "category": validate_and_strip(new_category),
                        "unit": new_unit,
                        "rate": new_rate
                    }
                    
                    st.session_state.ssr_items = pd.concat([
                        st.session_state.ssr_items,
                        pd.DataFrame([new_ssr_item])
                    ], ignore_index=True)
                    
                    st.success("✅ SSR item added successfully!")
                    st.rerun()
            elif submitted:
                st.error("Please fill in all required fields (Code, Description, Category).")

# Excel Import Page
elif page == "📥 Import Excel Data":
    st.title("📥 Import Excel Data")
    
    tab1, tab2, tab3 = st.tabs(["Import Measurements", "Import SSR", "Import Estimate"])
    
    # Import Measurements Tab
    with tab1:
        create_import_section(
            "Import Measurement Data from Excel",
            "Measurements", 
            import_excel_measurements
        )
    
    # Import SSR Tab
    with tab2:
        create_import_section(
            "Import SSR Data from Excel",
            "SSR Data",
            import_ssr_from_excel
        )
    
    # Import Estimate Tab
    with tab3:
        st.info("Import entire estimate with all sheets and data")
        create_import_section(
            "Import Complete Estimate",
            "Complete Estimate",
            import_complete_estimate
        )

# Technical Report Page
elif page == "📊 Technical Report":
    st.title("📊 Technical Report")
    
    # Project Information Header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        project_name = st.text_input("Project Name", 
            value="CONSTRUCTION OF COMMERCIAL COMPLEX FOR PANCHAYAT SAMITI GIRWA, UDAIPUR",
            help="Enter the project name for the technical report")
    
    with col2:
        report_date = st.date_input("Report Date", value=datetime.now().date())
    
    st.divider()
    
    # Technical Report Content
    st.subheader("📋 Technical Report Content")
    
    # Technical report content from attached_assets/technical_report.txt
    default_technical_content = """
**Government of Rajasthan**
**PWD - Building Division, Udaipur**

**TECHNICAL REPORT & DETAILED ESTIMATE**

**Project:** Construction of Commercial Complex for Panchayat Samiti, Girwa, Udaipur
**Building:** G + 5 RCC Framed Structure  
**Built-up Area:** 2345 m²
**Estimated Cost:** ₹ [Auto-calculated from General Abstract] Crore

**Administrative Sanction No.:** ____________________    **Date:** ________________

**1. Name of Work**
Construction of Commercial Complex for Panchayat Samiti, Girwa, Udaipur.

**2. Location**
Site: Girwa, Udaipur, Rajasthan.

**3. Scope of Work**
G+5 RCC framed commercial complex including retail spaces, offices, circulation, services, and external development works.

**4. General Specifications**
- **Foundation:** Isolated RCC footings in M20 concrete with random rubble masonry as required.
- **Superstructure:** RCC framed structure (M20 concrete) with Fe500 reinforcement; brick/stone masonry infill.
- **Flooring:** Vitrified tiles/Kota stone as per finish schedule.
- **Finishes:** External acrylic weather coat; internal OBD/distemper; enamel on metal/wood.
- **Sanitary:** CP fittings, PVC/SWR piping as per PWD specifications.
- **Electrical:** Concealed copper wiring with MCB distribution and LED fixtures.
- **Rainwater Harvesting and Solar provision** as per report.

**5. Design Basis**
Design to conform to BIS codes including IS 456, IS 1893, IS 875 and NBC 2016.

**6. Detailed Abstract of Cost (Stage-wise)**
The detailed abstract below includes cost breakup for all stages of work, rounded to two decimal places (₹ in Lakhs).

| S. No. | Description of Works | Amount (₹ Lakhs) |
|--------|---------------------|------------------|
| 1 | Civil Work (Ground Floor) - Structural works, etc. | 64.60 |
| 2 | Civil Work (First Floor) - Structural works, etc. | 52.97 |
| 3 | Civil Work (Second Floor) - Structural works, etc. | 54.30 |
| 4 | Civil Work (Third Floor) - Structural works, etc. | 55.65 |
| 5 | Civil Work (Fourth Floor) - Structural works, etc. | 57.05 |
| 6 | Civil Work (Fifth Floor) - Structural works, etc. | 58.47 |
| 7 | Sanitary Work - Internal sanitary installations | 27.44 |
| 8 | Electrical Work - Internal electrification | 41.16 |
| 9 | Sewerage Work - SWR/PVC piping, manholes | 13.72 |
| 10 | Development Work - External paving, boundary wall | 27.44 |
| 11 | Contingencies, Supervision, Quality assurance | 19.14 |
| **Total** | **Estimated Cost** | **444.51 (≈ ₹ 4.45 Crore)** |

**Note:** All values are rounded to two decimal places.

**7. Technical Specifications (Detailed)**

**A. FOUNDATION & STRUCTURAL WORK:**
- **Foundation Type:** Isolated RCC footings in M20 grade concrete
- **Foundation Depth:** As per soil investigation report and structural design
- **Masonry:** Random rubble stone masonry in cement mortar 1:6
- **RCC Grade:** M20 concrete with Fe500 TMT bars
- **Structural Design:** As per IS 456:2000, IS 1893:2016, IS 875 (Parts 1-5)

**B. SUPERSTRUCTURE:**
- **Frame:** RCC framed structure with columns, beams, and slabs
- **Infill Walls:** Brick/stone masonry as per architectural requirements
- **Slab Thickness:** As per structural design (typically 125-150mm)
- **Column Size:** As per structural design and load calculations

**C. FLOORING & FINISHES:**
- **Ground Floor:** Vitrified tiles 600x600mm or Kota stone as specified
- **Upper Floors:** Vitrified tiles with proper waterproofing
- **Staircase:** Kota stone treads with anti-skid finish
- **Toilet Areas:** Ceramic tiles with proper slope and drainage

**D. WALL FINISHES:**
- **External Walls:** Acrylic weather coat paint over cement plaster
- **Internal Walls:** Oil Bound Distemper (OBD) or emulsion paint
- **Wet Areas:** Ceramic tiles up to required height
- **Ceiling:** Distemper paint over cement plaster

**E. DOORS & WINDOWS:**
- **Main Entrance:** Teak wood frame with decorative panels
- **Internal Doors:** Flush doors with teak wood frames
- **Windows:** Aluminum sliding windows with clear glass
- **Hardware:** ISI marked locks, hinges, and accessories

**F. ELECTRICAL INSTALLATION:**
- **Wiring:** Concealed copper wiring in PVC conduits
- **Distribution:** Main panel with MCB distribution boards
- **Lighting:** LED fixtures for energy efficiency
- **Power Points:** Adequate 5A and 15A points as per requirement
- **Earthing:** Proper earthing system as per IS 3043

**G. PLUMBING & SANITARY:**
- **Water Supply:** CPVC pipes with brass fittings
- **Drainage:** PVC pipes with proper slope and ventilation
- **Sanitary Fixtures:** CP fittings - WCs, wash basins, urinals
- **Water Storage:** Overhead tank and underground sump as required

**H. SPECIAL FEATURES:**
- **Rainwater Harvesting:** Collection and recharge system
- **Solar Provision:** Structural provision for solar panels
- **Fire Safety:** As per NBC 2016 requirements
- **Accessibility:** Ramp and accessible toilet facilities

**8. Quality Control & Testing**
- **Concrete:** Cube testing for each grade of concrete
- **Steel:** Test certificates for TMT bars and structural steel
- **Materials:** All materials to conform to IS specifications
- **Supervision:** Regular inspection at each stage of construction

**9. Environmental Compliance**
- **Waste Management:** Proper disposal of construction waste
- **Water Conservation:** Rainwater harvesting and recycling
- **Energy Efficiency:** LED lighting and natural ventilation
- **Green Building:** Compliance with green building norms

**10. Project Timeline**
- **Design & Approval:** 2 months
- **Construction:** 18 months
- **Testing & Commissioning:** 1 month
- **Total Project Duration:** 21 months

**11. Drawings**
Architectural Plans, Structural Drawings, Electrical & Sanitary Layouts, and Site plan are attached as Annexures.

**12. Certificates**
I hereby certify that the estimate has been prepared as per PWD specifications and local Schedule of Rates. The design and estimate are recommended for administrative sanction.

**Prepared by:**
**Assistant Engineer, PWD Sub Division – Girwa**

**Checked by:**
**Executive Engineer, PWD Division – Udaipur**

**Date:** [Current Date]
**Place:** Udaipur, Rajasthan

---

**Note:** This technical report is based on the detailed estimate and specifications. All work shall be executed as per PWD specifications, IS codes, and approved drawings. Any deviation shall require prior approval from the competent authority.
    """
    
    # Editable technical report content
    with st.expander("📝 Edit Technical Report Content", expanded=True):
        technical_content = st.text_area(
            "Technical Report Content",
            value=default_technical_content,
            height=600,
            help="Edit the technical report content. Use Markdown formatting for better presentation."
        )
    
    # Display formatted technical report
    st.subheader("📄 Formatted Technical Report")
    
    # Auto-populate estimated cost from General Abstract
    ga_totals = calculate_general_abstract_totals()
    estimated_cost_lacs = ga_totals['grand_total'] / 100000
    
    # Replace placeholder with actual cost
    formatted_content = technical_content.replace(
        "[Auto-calculated from General Abstract]", 
        f"{estimated_cost_lacs:.2f} Lacs"
    )
    
    # Display the formatted report
    with st.container():
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 2rem; border-radius: 10px; border: 1px solid #dee2e6;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #1f4e79; margin: 0;">{project_name}</h2>
                <p style="color: #666; margin: 0.5rem 0;">Report Date: {report_date}</p>
            </div>
            <div style="text-align: left; line-height: 1.6;">
                {formatted_content.replace('**', '<strong>').replace('**', '</strong>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical Specifications Summary
    st.subheader("🔧 Technical Specifications Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏗️ Structural Specifications:**
        - Foundation: Isolated RCC footings in M20 concrete
        - Superstructure: RCC framed structure (M20) with Fe500 TMT
        - Masonry: Brick/stone masonry infill as per design
        - Design Codes: IS 456, IS 1893, IS 875, NBC 2016
        - Frame Type: G+5 RCC framed structure
        """)
    
    with col2:
        st.markdown("""
        **🎨 Finishing Specifications:**
        - Flooring: Vitrified tiles/Kota stone as per schedule
        - External: Acrylic weather coat paint
        - Internal: OBD/distemper paint on walls
        - Doors: Teak wood frames with flush doors
        - Windows: Aluminum sliding with clear glass
        - Electrical: Concealed copper wiring with LED fixtures
        """)
    
    with col3:
        st.markdown("""
        **📏 Project Details:**
        - Building Type: G+5 Commercial Complex
        - Total Built-up Area: 2,345 m²
        - Project Duration: 21 months
        - Design Basis: BIS codes & NBC 2016
        - Special Features: Rainwater harvesting, Solar provision
        - Estimated Cost: ₹{:,.2f} Crore
        """.format(estimated_cost_lacs/100))
    
    # Cost Integration
    st.subheader("💰 Cost Integration with General Abstract")
    
    if ga_totals['grand_total'] > 0:
        cost_breakdown = {
            'Component': ['Civil Work', 'Sanitary Work', 'Electric Work', 'Electric Fixtures', 'Total'],
            'Amount (₹)': [
                ga_totals['civil_work'],
                ga_totals['sanitary_work'], 
                ga_totals['electric_work'],
                ga_totals['electric_fixtures'],
                ga_totals['grand_total']
            ],
            'Amount (Lacs)': [
                ga_totals['civil_work']/100000,
                ga_totals['sanitary_work']/100000,
                ga_totals['electric_work']/100000, 
                ga_totals['electric_fixtures']/100000,
                ga_totals['grand_total']/100000
            ]
        }
        
        cost_df = pd.DataFrame(cost_breakdown)
        st.dataframe(
            cost_df,
            column_config={
                "Component": "Cost Component",
                "Amount (₹)": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
                "Amount (Lacs)": st.column_config.NumberColumn("Amount (Lacs)", format="%.2f")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("💡 Add measurements and abstract items to see cost integration")
    
    # Export Options
    st.subheader("📥 Export Technical Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export as Text"):
            # Create plain text version
            plain_text = f"""
{project_name}
Report Date: {report_date}

{formatted_content}

Cost Summary:
- Total Estimated Cost: ₹{ga_totals['grand_total']:,.2f}
- Cost in Lacs: {estimated_cost_lacs:.2f} Lacs

Generated by Construction Estimation System
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            st.download_button(
                "📥 Download Text Report",
                data=plain_text,
                file_name=f"technical_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📊 Export with Cost Data"):
            # Create detailed report with cost breakdown
            detailed_report = f"""
{project_name}
Technical Report with Cost Analysis
Report Date: {report_date}

{formatted_content}

DETAILED COST BREAKDOWN:
======================
Civil Work: ₹{ga_totals['civil_work']:,.2f}
Sanitary Work: ₹{ga_totals['sanitary_work']:,.2f}
Electric Work: ₹{ga_totals['electric_work']:,.2f}
Electric Fixtures: ₹{ga_totals['electric_fixtures']:,.2f}
GRAND TOTAL: ₹{ga_totals['grand_total']:,.2f}

Cost per Sqm: ₹{ga_totals['grand_total']/339.50:,.2f} per Sqm
Total Area: 339.50 Sqm

Generated by Construction Estimation System
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            st.download_button(
                "📥 Download Detailed Report",
                data=detailed_report,
                file_name=f"technical_report_detailed_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("🖨️ Print-Ready Format"):
            # Create print-ready format
            print_ready = formatted_content.replace('**', '').replace('*', '')
            
            st.download_button(
                "📥 Download Print Format",
                data=print_ready,
                file_name=f"technical_report_print_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
    
    # Additional Technical Information
    with st.expander("ℹ️ Technical Report Guidelines"):
        st.markdown("""
        **Technical Report Guidelines:**
        
        1. **Project Information**: Ensure all project details are accurate and complete
        2. **Specifications**: Follow PWD standards and local building codes
        3. **Cost Integration**: Costs are automatically updated from General Abstract
        4. **Documentation**: Include all necessary drawings and approvals
        5. **Review Process**: Have the report reviewed by qualified engineers
        
        **Report Sections:**
        - Project identification and location
        - Technical specifications for all components
        - Scope of work and project dimensions
        - Cost estimates with basis of calculation
        - Required drawings and documentation
        - Professional signatures and approvals
        
        **Export Options:**
        - **Text Format**: Simple text for basic documentation
        - **Detailed Report**: Includes complete cost breakdown
        - **Print Format**: Clean format for official submission
        """)

# System Tools Page
elif page == "🔧 System Tools":
    st.title("🔧 System Tools & Utilities")
    
    st.info("🚧 **System Tools section coming soon!** This will include backup, restore, data validation, and other utility functions.")
    
    # Placeholder for system tools
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Data Management")
        st.write("- Backup/Restore functionality")
        st.write("- Data validation tools")
        st.write("- System diagnostics")
    
    with col2:
        st.subheader("📊 Advanced Features")
        st.write("- Bulk operations")
        st.write("- Custom report generation")
        st.write("- Integration tools")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏗️ Construction Estimation System | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)
