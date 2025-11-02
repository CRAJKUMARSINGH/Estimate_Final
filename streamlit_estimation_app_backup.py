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
    st.session_state.measurements = pd.DataFrame(columns=[
        'id', 'item_no', 'description', 'quantity', 
        'length', 'breadth', 'height', 'unit', 'total', 'ssr_code'
    ])
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
    st.session_state.abstract_items = pd.DataFrame(columns=[
        'id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount', 'linked_from_measurement'
    ])

# Initialize separate sheets for different work types
if 'measurement_sheets' not in st.session_state:
    st.session_state.measurement_sheets = {
        'Ground Floor': pd.DataFrame(columns=['id', 'ssr_code', 'item_no', 'description', 'quantity', 'length', 'breadth', 'height', 'unit', 'total']),
        'First Floor': pd.DataFrame(columns=['id', 'ssr_code', 'item_no', 'description', 'quantity', 'length', 'breadth', 'height', 'unit', 'total']),
        'Basement': pd.DataFrame(columns=['id', 'ssr_code', 'item_no', 'description', 'quantity', 'length', 'breadth', 'height', 'unit', 'total'])
    }

if 'abstract_sheets' not in st.session_state:
    st.session_state.abstract_sheets = {
        'Ground Floor': pd.DataFrame(columns=['id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount']),
        'First Floor': pd.DataFrame(columns=['id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount']),
        'Basement': pd.DataFrame(columns=['id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount'])
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

UNITS = ["RM", "Cum", "Sqm", "Nos", "Kg", "Ton", "Ltr", "LS"]

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
    "📝 Measurement Sheets", 
    "📚 SSR Database",
    "📥 Import Excel Data",
    "💰 Abstract of Cost"
])

# Helper Functions
def calculate_total(quantity, length, breadth, height):
    return quantity * max(1, length) * max(1, breadth) * max(1, height)

def export_to_csv(dataframe, filename):
    return dataframe.to_csv(index=False).encode('utf-8')

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
        'id': len(st.session_state.abstract_sheets[sheet_name]) + 1,
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
    
    # Create the blank formulated measurement lines with SAME DESCRIPTION
    for i, template in enumerate(measurement_templates):
        measurement_line = {
            'id': len(st.session_state.measurement_sheets[sheet_name]) + 1,
            'ssr_code': ssr_code,
            'item_no': f"{abstract_item['id']}.{i+1}",
            'description': template['desc'],  # EXACT SAME DESCRIPTION as in estimate
            'quantity': template['qty'],
            'length': template['l'],
            'breadth': template['b'], 
            'height': template['h'],
            'unit': abstract_item['unit'],
            'total': template['qty'] * max(1, template['l']) * max(1, template['b']) * max(1, template['h'])
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
        st.session_state.abstract_sheets[sheet_name] = pd.DataFrame(columns=[
            'id', 'ssr_code', 'description', 'unit', 'quantity', 'rate', 'amount'
        ])
        
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

# Dashboard Page
if page == "📊 Dashboard":
    st.title("📊 Project Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
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
        total_cost = st.session_state.abstract_items['amount'].sum()
        st.metric(
            "Total Estimated Cost", 
            f"₹{total_cost:,.0f}",
            delta=None
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
        col1, col2 = st.columns(2)
        
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

# Measurement Sheets Page
elif page == "📝 Measurement Sheets":
    st.title("📝 Measurement Sheets")
    
    # Sheet selector (different floors/parts)
    available_sheets = list(st.session_state.measurement_sheets.keys())
    selected_sheet = st.selectbox("Select Measurement Sheet", available_sheets)
    st.write(f"**Current Sheet:** 📏 Measurement {selected_sheet}")
    
    # Show linkage info
    st.info(f"💡 **Auto-Linkage:** Measurements in this sheet automatically feed quantities into 'Abstract of Cost {selected_sheet}' sheet")
    
    # Add measurement form with enhanced SSR integration
    with st.expander("➕ Add New Measurement", expanded=True):
        # SSR Code Selection Section
        st.subheader("🔍 SSR Code Selection")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # SSR Code selector
            ssr_codes = ["Select SSR Code..."] + st.session_state.ssr_items['code'].tolist()
            selected_ssr = st.selectbox("SSR Item Code", ssr_codes, key="ssr_selector")
        
        with col2:
            # Auto-populate description when SSR code is selected
            if selected_ssr != "Select SSR Code...":
                ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr].iloc[0]
                st.success(f"**📋 Description:** {ssr_item['description']}")
                st.info(f"**📂 Category:** {ssr_item['category']} | **📏 Unit:** {ssr_item['unit']} | **💰 Rate:** ₹{ssr_item['rate']:,.2f}")
                auto_description = ssr_item['description']
                auto_unit = ssr_item['unit'].title()
                auto_rate = ssr_item['rate']
            else:
                auto_description = ""
                auto_unit = "Cum"
                auto_rate = 0
                st.info("Select an SSR code to auto-populate description and rate")
        
        st.divider()
        
        with st.form("add_measurement"):
            # Item details
            col1, col2 = st.columns([1, 2])
            
            with col1:
                item_no = st.text_input("Item No.", placeholder="1, 2, 3...")
                
                # Auto-select unit based on SSR or allow manual selection
                if selected_ssr != "Select SSR Code..." and auto_unit in UNITS:
                    unit_index = UNITS.index(auto_unit)
                    unit = st.selectbox("Unit", UNITS, index=unit_index)
                else:
                    unit = st.selectbox("Unit", UNITS)
            
            with col2:
                # Auto-populate description or allow manual entry
                if selected_ssr != "Select SSR Code...":
                    description = st.text_area("Description", value=auto_description, 
                                             help="Description auto-populated from SSR. You can modify if needed.")
                else:
                    description = st.text_area("Description", placeholder="Enter detailed description of work item...")
            
            # Measurement inputs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                quantity = st.number_input("Quantity", min_value=0.0, step=0.01, value=1.0)
            with col2:
                length = st.number_input("Length (m)", min_value=0.0, step=0.01, value=0.0)
            with col3:
                breadth = st.number_input("Breadth (m)", min_value=0.0, step=0.01, value=0.0)
            with col4:
                height = st.number_input("Height (m)", min_value=0.0, step=0.01, value=0.0)
            
            # Calculate and display total
            total = calculate_total(quantity, length, breadth, height)
            
            # Show calculated total and estimated cost
            if selected_ssr != "Select SSR Code...":
                ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr].iloc[0]
                estimated_cost = total * ssr_item['rate']
                st.success(f"**📏 Total Quantity: {total:.2f} {unit}** | **💰 Estimated Cost: ₹{estimated_cost:,.2f}**")
                st.caption(f"Calculation: {total:.2f} {unit} × ₹{ssr_item['rate']:,.2f} = ₹{estimated_cost:,.2f}")
            else:
                st.info(f"**📏 Calculated Total: {total:.2f} {unit}**")
            
            submitted = st.form_submit_button("➕ Add Measurement", type="primary")
            
            if submitted and description.strip():
                new_measurement = {
                    'id': len(st.session_state.measurement_sheets[selected_sheet]) + 1,
                    'ssr_code': selected_ssr if selected_ssr != "Select SSR Code..." else "",
                    'item_no': item_no,
                    'description': description.strip(),
                    'quantity': quantity,
                    'length': length,
                    'breadth': breadth,
                    'height': height,
                    'unit': unit,
                    'total': total
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
                    st.success(f"🔗 **Auto-linked** to Abstract of Cost {selected_sheet} | Estimated Cost: **₹{total * auto_rate:,.2f}**")
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
        
        # Add total row
        if len(display_df) > 0:
            total_quantity = display_df['total'].sum()
            total_row = pd.DataFrame([{
                'id': '',
                'ssr_code': '',
                'item_no': 'TOTAL',
                'description': f'Total {selected_sheet}',
                'quantity': '',
                'length': '',
                'breadth': '',
                'height': '',
                'unit': display_df.iloc[0]['unit'] if len(display_df) > 0 else '',
                'total': total_quantity
            }])
            display_df = pd.concat([display_df, total_row], ignore_index=True)
        
        # Display table with enhanced columns
        display_columns = {
            "id": None,
            "item_no": "Item No.",
            "description": st.column_config.TextColumn("Description", width="large"),
            "quantity": st.column_config.NumberColumn("Qty", format="%.2f"),
            "length": st.column_config.NumberColumn("Length", format="%.2f"),
            "breadth": st.column_config.NumberColumn("Breadth", format="%.2f"),
            "height": st.column_config.NumberColumn("Height", format="%.2f"),
            "unit": "Unit",
            "total": st.column_config.NumberColumn("Total", format="%.2f")
        }
        
        # Add SSR code column
        if 'ssr_code' in display_df.columns:
            display_columns["ssr_code"] = "SSR Code"
        
        st.dataframe(
            display_df,
            column_config=display_columns,
            hide_index=True,
            use_container_width=True
        )
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            csv_data = export_to_csv(st.session_state.measurements, "measurements")
            st.download_button(
                "📥 Export CSV",
                data=csv_data,
                file_name=f"measurements_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col2:
            if st.button("🗑️ Clear All", type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    st.session_state.measurements = pd.DataFrame(columns=[
                        'id', 'item_no', 'description', 'quantity', 
                        'length', 'breadth', 'height', 'unit', 'total'
                    ])
                    st.session_state.counter = 1
                    st.session_state.confirm_clear = False
                    st.success("All measurements cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm clearing all measurements.")
        
        with col3:
            if st.button("🔄 Reset Confirmation"):
                st.session_state.confirm_clear = False
    else:
        st.info("No measurements added yet. Use the form above to add your first measurement.")

# SSR Database Page
elif page == "📚 SSR Database":
    st.title("📚 Standard Schedule of Rates (SSR)")
    
    # Search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
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
            
            submitted = st.form_submit_button("➕ Add SSR Item", type="primary")
            
            if submitted and new_code and new_description and new_category:
                # Check if code already exists
                if new_code in st.session_state.ssr_items['code'].values:
                    st.error(f"SSR Code '{new_code}' already exists!")
                else:
                    new_ssr_item = {
                        "code": new_code,
                        "description": new_description.strip(),
                        "category": new_category.strip(),
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
        st.subheader("Import Measurement Data from Excel")
        
        # Check for files in attached_assets
        measurement_files = find_estimate_files("*.xlsx")
        if measurement_files:
            selected_file = st.selectbox("Select measurement file:", measurement_files, 
                                       format_func=lambda x: os.path.basename(x))
            if st.button("Import Selected Measurement File"):
                if import_excel_measurements(selected_file):
                    st.success(f"✅ Measurements imported successfully from: {os.path.basename(selected_file)}")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import measurements from: {os.path.basename(selected_file)}")
        else:
            st.info("No Excel files found in attached_assets folder")
        
        # Manual file upload
        uploaded_file = st.file_uploader("Or upload Excel file", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            if st.button("Import Uploaded Measurement File"):
                # Save to temporary file and import
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                if import_excel_measurements(tmp_path):
                    st.success(f"✅ Measurements imported successfully from: {uploaded_file.name}")
                    os.unlink(tmp_path)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import measurements from: {uploaded_file.name}")
                    os.unlink(tmp_path)
    
    # Import SSR Tab
    with tab2:
        st.subheader("Import SSR Data from Excel")
        
        # Check for files in attached_assets
        ssr_files = find_estimate_files("*.xlsx")
        if ssr_files:
            selected_file = st.selectbox("Select SSR file:", ssr_files, 
                                       format_func=lambda x: os.path.basename(x), key="ssr_select")
            if st.button("Import Selected SSR File"):
                if import_ssr_from_excel(selected_file):
                    st.success(f"✅ SSR data imported successfully from: {os.path.basename(selected_file)}")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import SSR data from: {os.path.basename(selected_file)}")
        else:
            st.info("No Excel files found in attached_assets folder")
        
        # Manual file upload
        uploaded_file = st.file_uploader("Or upload SSR Excel file", type=['xlsx', 'xls'], key="ssr_upload")
        if uploaded_file is not None:
            if st.button("Import Uploaded SSR File"):
                # Save to temporary file and import
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                if import_ssr_from_excel(tmp_path):
                    st.success(f"✅ SSR data imported successfully from: {uploaded_file.name}")
                    os.unlink(tmp_path)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import SSR data from: {uploaded_file.name}")
                    os.unlink(tmp_path)
    
    # Import Estimate Tab
    with tab3:
        st.subheader("Import Complete Estimate")
        st.info("Import entire estimate with all sheets and data")
        
        # Check for files in attached_assets
        estimate_files = find_estimate_files("*.xlsx")
        if estimate_files:
            selected_file = st.selectbox("Select estimate file:", estimate_files, 
                                       format_func=lambda x: os.path.basename(x), key="estimate_select")
            if st.button("Import Selected Estimate"):
                if import_complete_estimate(selected_file):
                    st.success(f"✅ Complete estimate imported successfully from: {os.path.basename(selected_file)}")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import complete estimate from: {os.path.basename(selected_file)}")
        else:
            st.info("No Excel files found in attached_assets folder")
        
        # Manual file upload
        uploaded_file = st.file_uploader("Or upload complete estimate", type=['xlsx', 'xls'], key="estimate_upload")
        if uploaded_file is not None:
            if st.button("Import Uploaded Estimate"):
                # Save to temporary file and import
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                if import_complete_estimate(tmp_path):
                    st.success(f"✅ Complete estimate imported successfully from: {uploaded_file.name}")
                    os.unlink(tmp_path)
                    st.rerun()
                else:
                    st.error(f"❌ Failed to import complete estimate from: {uploaded_file.name}")
                    os.unlink(tmp_path)

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
        st.subheader("🔍 SSR Code Selection")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            # SSR Code selector
            ssr_codes = ["Select SSR Code..."] + st.session_state.ssr_items['code'].tolist()
            selected_ssr_abstract = st.selectbox("SSR Item Code", ssr_codes, key="ssr_abstract_selector")
        
        with col2:
            # Auto-populate description when SSR code is selected
            if selected_ssr_abstract != "Select SSR Code...":
                ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr_abstract].iloc[0]
                st.success(f"**📋 Description:** {ssr_item['description']}")
                st.info(f"**📂 Category:** {ssr_item['category']} | **📏 Unit:** {ssr_item['unit']} | **💰 Rate:** ₹{ssr_item['rate']:,.2f}")
                auto_description = ssr_item['description']
                auto_unit = ssr_item['unit'].title()
                auto_rate = ssr_item['rate']
            else:
                auto_description = ""
                auto_unit = "Cum"
                auto_rate = 0
                st.info("Select an SSR code to auto-populate description and rate")
        
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
            
            submitted_abstract = st.form_submit_button("➕ Add Abstract Item & Create Measurement Lines", type="primary")
            
            if submitted_abstract and abs_description.strip():
                # Create abstract item
                new_abstract_item = {
                    'id': len(st.session_state.abstract_sheets[selected_abstract_sheet]) + 1,
                    'ssr_code': selected_ssr_abstract if selected_ssr_abstract != "Select SSR Code..." else "",
                    'description': abs_description.strip(),
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
            col1, col2, col3 = st.columns(3)
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
if page == "💰 Abstract of Cost":
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
        
        col1, col2 = st.columns([2, 1])
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
    
    else:
        st.info("No abstract items created yet. Add items to see the General Abstract summary.")
    
    if not st.session_state.measurements.empty and not st.session_state.ssr_items.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("💡 You can auto-generate abstract items by matching measurements with SSR rates")
        
        with col2:
            if st.button("🔄 Auto-Generate Abstract", type="primary"):
                # Clear existing abstract items
                st.session_state.abstract_items = pd.DataFrame(columns=[
                    "id", "description", "quantity", "unit", "rate", "amount"
                ])
                
                # Group measurements by work type/category
                measurements_df = st.session_state.measurements.copy()
                ssr_df = st.session_state.ssr_items.copy()
                
                # Try to match measurements with SSR items
                abstract_counter = 1
                
                for _, measurement in measurements_df.iterrows():
                    # Find matching SSR item by description keywords or unit
                    measurement_desc = measurement['description'].lower()
                    measurement_unit = measurement['unit'].lower()
                    
                    # Look for SSR matches
                    matching_ssr = ssr_df[
                        (ssr_df['unit'].str.lower() == measurement_unit) |
                        (ssr_df['description'].str.lower().str.contains(measurement_desc.split()[0] if measurement_desc else '', case=False, na=False))
                    ]
                    
                    if not matching_ssr.empty:
                        # Use the first matching SSR item
                        ssr_item = matching_ssr.iloc[0]
                        rate = ssr_item['rate']
                    else:
                        # Use default rate based on unit
                        unit_rates = {
                            'cum': 3500.0,
                            'sqm': 150.0,
                            'rm': 100.0,
                            'nos': 500.0,
                            'kg': 60.0,
                            'ton': 60000.0,
                            'ltr': 50.0,
                            'ls': 50000.0
                        }
                        rate = unit_rates.get(measurement_unit, 1000.0)
                    
                    # Create abstract item
                    amount = measurement['total'] * rate
                    
                    new_abstract_item = {
                        "id": str(abstract_counter),
                        "description": measurement['description'],
                        "quantity": measurement['total'],
                        "unit": measurement['unit'],
                        "rate": rate,
                        "amount": amount
                    }
                    
                    st.session_state.abstract_items = pd.concat([
                        st.session_state.abstract_items,
                        pd.DataFrame([new_abstract_item])
                    ], ignore_index=True)
                    
                    abstract_counter += 1
                
                st.success(f"✅ Generated {len(st.session_state.abstract_items)} abstract items from measurements!")
                st.rerun()
    
    # Display abstract items
    if not st.session_state.abstract_items.empty:
        st.subheader("📋 Cost Abstract Items")
        
        # Add edit functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Current Abstract Items:**")
        with col2:
            if st.button("🗑️ Clear Abstract"):
                st.session_state.abstract_items = pd.DataFrame(columns=[
                    "id", "description", "quantity", "unit", "rate", "amount"
                ])
                st.rerun()
        
        # Display editable dataframe
        edited_df = st.data_editor(
            st.session_state.abstract_items,
            column_config={
                "id": st.column_config.TextColumn("S.No.", disabled=True),
                "description": st.column_config.TextColumn("Description", width="large"),
                "quantity": st.column_config.NumberColumn("Quantity", format="%.2f"),
                "unit": st.column_config.SelectboxColumn("Unit", options=UNITS),
                "rate": st.column_config.NumberColumn("Rate (₹)", format="%.2f"),
                "amount": st.column_config.NumberColumn("Amount (₹)", format="%.2f", disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        # Update amounts when rate or quantity changes
        if not edited_df.equals(st.session_state.abstract_items):
            edited_df['amount'] = edited_df['quantity'] * edited_df['rate']
            st.session_state.abstract_items = edited_df
            st.rerun()
        
        # Cost calculations
        st.subheader("💹 Cost Breakdown")
        
        subtotal = st.session_state.abstract_items['amount'].sum()
        
        # Calculate additional charges
        civil_work = st.session_state.abstract_items[
            st.session_state.abstract_items['description'].str.contains('Civil Work', case=False, na=False)
        ]
        civil_amount = civil_work['amount'].sum() if not civil_work.empty else 0
        
        electrification_rate = 0.07  # 7%
        electrification_charge = civil_amount * electrification_rate
        
        total_after_electrification = subtotal + electrification_charge
        
        prorata_rate = 0.13  # 13%
        prorata_charges = total_after_electrification * prorata_rate
        
        grand_total = total_after_electrification + prorata_charges
        
        # Display calculations in a nice format
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Subtotal (Direct Costs):**")
            st.write(f"**Add Electrification @ {electrification_rate*100}% on Civil Work:**")
            st.write("**Total after Electrification:**")
            st.write(f"**Add Prorata Charges @ {prorata_rate*100}%:**")
            st.write("---")
            st.write("**GRAND TOTAL:**")
        
        with col2:
            st.write(f"₹{subtotal:,.2f}")
            st.write(f"₹{electrification_charge:,.2f}")
            st.write(f"₹{total_after_electrification:,.2f}")
            st.write(f"₹{prorata_charges:,.2f}")
            st.write("---")
            st.write(f"**₹{grand_total:,.2f}**")
        
        # Summary metrics
        st.subheader("📊 Project Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Base Cost", f"₹{subtotal:,.0f}")
        with col2:
            st.metric("Additional Charges", f"₹{(electrification_charge + prorata_charges):,.0f}")
        with col3:
            st.metric("Final Total", f"₹{grand_total:,.0f}")
        
        # Export options
        st.subheader("📥 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            abstract_csv = export_to_csv(st.session_state.abstract_items, "abstract")
            st.download_button(
                "📥 Export Abstract CSV",
                data=abstract_csv,
                file_name=f"cost_abstract_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Create detailed cost breakdown
            breakdown_data = {
                'Item': ['Subtotal', 'Electrification (7%)', 'Prorata Charges (13%)', 'GRAND TOTAL'],
                'Amount': [subtotal, electrification_charge, prorata_charges, grand_total]
            }
            breakdown_df = pd.DataFrame(breakdown_data)
            breakdown_csv = export_to_csv(breakdown_df, "cost_breakdown")
            
            st.download_button(
                "📥 Export Cost Breakdown",
                data=breakdown_csv,
                file_name=f"cost_breakdown_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No abstract items available. Add some measurements first to generate cost abstracts.")
        
        # Quick add abstract item
        with st.expander("➕ Add Abstract Item"):
            with st.form("add_abstract_item"):
                col1, col2 = st.columns(2)
                
                with col1:
                    abs_description = st.text_area("Description")
                    abs_quantity = st.number_input("Quantity", min_value=0.0, step=0.01, value=1.0)
                    abs_unit = st.selectbox("Unit", UNITS)
                
                with col2:
                    abs_rate = st.number_input("Rate (₹)", min_value=0.0, step=0.01)
                    abs_amount = abs_quantity * abs_rate
                    st.info(f"**Amount: ₹{abs_amount:,.2f}**")
                
                submitted = st.form_submit_button("➕ Add Abstract Item", type="primary")
                
                if submitted and abs_description.strip():
                    new_abstract_item = {
                        "id": str(len(st.session_state.abstract_items) + 1),
                        "description": abs_description.strip(),
                        "quantity": abs_quantity,
                        "unit": abs_unit,
                        "rate": abs_rate,
                        "amount": abs_amount
                    }
                    
                    st.session_state.abstract_items = pd.concat([
                        st.session_state.abstract_items,
                        pd.DataFrame([new_abstract_item])
                    ], ignore_index=True)
                    
                    st.success("✅ Abstract item added successfully!")
                    st.rerun()

else:
    # Abstract of Cost Page
    st.title("💰 Abstract of Cost")
    
    # Auto-generate abstract from measurements and SSR
    st.subheader("🔄 Generate Abstract from Measurements")
    
    if not st.session_state.measurements.empty and not st.session_state.ssr_items.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("💡 You can auto-generate abstract items by matching measurements with SSR rates")
        
        with col2:
            if st.button("🔄 Auto-Generate Abstract", type="primary"):
                # Clear existing abstract items
                st.session_state.abstract_items = pd.DataFrame(columns=[
                    "id", "description", "quantity", "unit", "rate", "amount"
                ])
                
                # Group measurements by work type/category
                measurements_df = st.session_state.measurements.copy()
                ssr_df = st.session_state.ssr_items.copy()
                
                # Try to match measurements with SSR items
                abstract_counter = 1
                
                for _, measurement in measurements_df.iterrows():
                    # Find matching SSR item by description keywords or unit
                    measurement_desc = measurement['description'].lower()
                    measurement_unit = measurement['unit'].lower()
                    
                    # Look for SSR matches
                    matching_ssr = ssr_df[
                        (ssr_df['unit'].str.lower() == measurement_unit) |
                        (ssr_df['description'].str.lower().str.contains(measurement_desc.split()[0] if measurement_desc else '', case=False, na=False))
                    ]
                    
                    if not matching_ssr.empty:
                        # Use the first matching SSR item
                        ssr_item = matching_ssr.iloc[0]
                        rate = ssr_item['rate']
                    else:
                        # Use default rate based on unit
                        unit_rates = {
                            'cum': 3500.0,
                            'sqm': 150.0,
                            'rm': 100.0,
                            'nos': 500.0,
                            'kg': 60.0,
                            'ton': 60000.0,
                            'ltr': 50.0,
                            'ls': 50000.0
                        }
                        rate = unit_rates.get(measurement_unit, 1000.0)
                    
                    # Create abstract item
                    amount = measurement['total'] * rate
                    
                    new_abstract_item = {
                        "id": str(abstract_counter),
                        "description": measurement['description'],
                        "quantity": measurement['total'],
                        "unit": measurement['unit'],
                        "rate": rate,
                        "amount": amount
                    }
                    
                    st.session_state.abstract_items = pd.concat([
                        st.session_state.abstract_items,
                        pd.DataFrame([new_abstract_item])
                    ], ignore_index=True)
                    
                    abstract_counter += 1
                
                st.success(f"✅ Generated {len(st.session_state.abstract_items)} abstract items from measurements!")
                st.rerun()
    
    # Display abstract items
    if not st.session_state.abstract_items.empty:
        st.subheader("📋 Cost Abstract Items")
        
        # Add edit functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write("**Current Abstract Items:**")
        with col2:
            if st.button("🗑️ Clear Abstract"):
                st.session_state.abstract_items = pd.DataFrame(columns=[
                    "id", "description", "quantity", "unit", "rate", "amount"
                ])
                st.rerun()
        
        # Display editable dataframe
        edited_df = st.data_editor(
            st.session_state.abstract_items,
            column_config={
                "id": st.column_config.TextColumn("S.No.", disabled=True),
                "description": st.column_config.TextColumn("Description", width="large"),
                "quantity": st.column_config.NumberColumn("Quantity", format="%.2f"),
                "unit": st.column_config.SelectboxColumn("Unit", options=UNITS),
                "rate": st.column_config.NumberColumn("Rate (₹)", format="%.2f"),
                "amount": st.column_config.NumberColumn("Amount (₹)", format="%.2f", disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        # Update amounts when rate or quantity changes
        if not edited_df.equals(st.session_state.abstract_items):
            edited_df['amount'] = edited_df['quantity'] * edited_df['rate']
            st.session_state.abstract_items = edited_df
            st.rerun()
        
        # Cost calculations
        st.subheader("💹 Cost Breakdown")
        
        subtotal = st.session_state.abstract_items['amount'].sum()
        
        # Calculate additional charges
        civil_work = st.session_state.abstract_items[
            st.session_state.abstract_items['description'].str.contains('Civil Work', case=False, na=False)
        ]
        civil_amount = civil_work['amount'].sum() if not civil_work.empty else 0
        
        electrification_rate = 0.07  # 7%
        electrification_charge = civil_amount * electrification_rate
        
        total_after_electrification = subtotal + electrification_charge
        
        prorata_rate = 0.13  # 13%
        prorata_charges = total_after_electrification * prorata_rate
        
        grand_total = total_after_electrification + prorata_charges
        
        # Display calculations in a nice format
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Subtotal (Direct Costs):**")
            st.write(f"**Add Electrification @ {electrification_rate*100}% on Civil Work:**")
            st.write("**Total after Electrification:**")
            st.write(f"**Add Prorata Charges @ {prorata_rate*100}%:**")
            st.write("---")
            st.write("**GRAND TOTAL:**")
        
        with col2:
            st.write(f"₹{subtotal:,.2f}")
            st.write(f"₹{electrification_charge:,.2f}")
            st.write(f"₹{total_after_electrification:,.2f}")
            st.write(f"₹{prorata_charges:,.2f}")
            st.write("---")
            st.write(f"**₹{grand_total:,.2f}**")
        
        # Summary metrics
        st.subheader("📊 Project Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Base Cost", f"₹{subtotal:,.0f}")
        with col2:
            st.metric("Additional Charges", f"₹{(electrification_charge + prorata_charges):,.0f}")
        with col3:
            st.metric("Final Total", f"₹{grand_total:,.0f}")
        
        # Export options
        st.subheader("📥 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            abstract_csv = export_to_csv(st.session_state.abstract_items, "abstract")
            st.download_button(
                "📥 Export Abstract CSV",
                data=abstract_csv,
                file_name=f"cost_abstract_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Create detailed cost breakdown
            breakdown_data = {
                'Item': ['Subtotal', 'Electrification (7%)', 'Prorata Charges (13%)', 'GRAND TOTAL'],
                'Amount': [subtotal, electrification_charge, prorata_charges, grand_total]
            }
            breakdown_df = pd.DataFrame(breakdown_data)
            breakdown_csv = export_to_csv(breakdown_df, "cost_breakdown")
            
            st.download_button(
                "📥 Export Cost Breakdown",
                data=breakdown_csv,
                file_name=f"cost_breakdown_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No abstract items available. Add some measurements first to generate cost abstracts.")
        
        # Quick add abstract item
        with st.expander("➕ Add Abstract Item"):
            with st.form("add_abstract_item"):
                col1, col2 = st.columns(2)
                
                with col1:
                    abs_description = st.text_area("Description")
                    abs_quantity = st.number_input("Quantity", min_value=0.0, step=0.01, value=1.0)
                    abs_unit = st.selectbox("Unit", UNITS)
                
                with col2:
                    abs_rate = st.number_input("Rate (₹)", min_value=0.0, step=0.01)
                    abs_amount = abs_quantity * abs_rate
                    st.info(f"**Amount: ₹{abs_amount:,.2f}**")
                
                submitted = st.form_submit_button("➕ Add Abstract Item", type="primary")
                
                if submitted and abs_description.strip():
                    new_abstract_item = {
                        "id": str(len(st.session_state.abstract_items) + 1),
                        "description": abs_description.strip(),
                        "quantity": abs_quantity,
                        "unit": abs_unit,
                        "rate": abs_rate,
                        "amount": abs_amount
                    }
                    
                    st.session_state.abstract_items = pd.concat([
                        st.session_state.abstract_items,
                        pd.DataFrame([new_abstract_item])
                    ], ignore_index=True)
                    
                    st.success("✅ Abstract item added successfully!")
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏗️ Construction Estimation System | Built with Streamlit</p>
    </div>
""", unsafe_allow_html=True)