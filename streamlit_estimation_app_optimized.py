#!/usr/bin/env python3
"""
Construction Estimation System - Optimized Version
Comprehensive construction cost estimation with enhanced performance and deployment readiness
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import json
import os
import glob
from pathlib import Path
import math
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config - MUST be first Streamlit command
st.set_page_config(
    page_title="Construction Estimation System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/rajkumarsingh/construction-estimation',
        'Report a bug': 'mailto:crajkumarsingh@hotmail.com',
        'About': "Construction Estimation System v2.0 - Professional cost estimation tool"
    }
)

# Enhanced DataFrame Schemas - DEFINED BEFORE USE
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

# Work Types
WORK_TYPES = {
    "Civil Work": "🏗️",
    "Sanitary Work": "🚰", 
    "Electrical Work": "⚡",
    "Landscape Work": "🌳"
}

# UI Standardization Constants
BUTTON_TYPES = {
    'primary': 'primary',
    'secondary': 'secondary',
    'danger': 'secondary',
    'neutral': None
}

COLUMN_LAYOUTS = {
    'metrics': [1, 1, 1, 1],
    'form_basic': [1, 2],
    'form_detailed': [1, 2],
    'actions': [1, 1, 1],
    'search': [2, 1, 1],
    'cost_calc': [2, 1],
    'export': [1, 1],
    'stats': [1, 1]
}

# Cache configuration for performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_default_ssr_data():
    """Load default SSR data with caching for performance"""
    return pd.DataFrame([
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

# Initialize session state with error handling
def initialize_session_state():
    """Initialize all session state variables with proper error handling"""
    try:
        # Initialize measurements
        if 'measurements' not in st.session_state:
            st.session_state.measurements = pd.DataFrame(columns=MEASUREMENT_COLUMNS)
            st.session_state.counter = 1

        # Initialize SSR database
        if 'ssr_items' not in st.session_state:
            st.session_state.ssr_items = load_default_ssr_data()

        # Initialize abstract items
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

        # Initialize separate sheets for different work types
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
            
        logger.info("Session state initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing session state: {e}")
        st.error(f"Initialization error: {e}")

# Enhanced Helper Functions with caching
@lru_cache(maxsize=1000)
def calculate_total(quantity, length, breadth, height, diameter=0, thickness=0, measurement_type="Standard"):
    """Enhanced calculation function with caching for performance"""
    try:
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
            unit_weight = 7.85 if thickness > 0 else 1
            return quantity * max(1, length) * thickness * unit_weight
        else:  # Standard
            return quantity * max(1, length) * max(1, breadth) * max(1, height)
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        return 0

@lru_cache(maxsize=100)
def calculate_deduction_total(gross_total, deduction_total):
    """Calculate net total after deductions with caching"""
    return max(0, gross_total - deduction_total)

def export_to_csv(dataframe, filename):
    """Export DataFrame to CSV with error handling"""
    try:
        return dataframe.to_csv(index=False).encode('utf-8')
    except Exception as e:
        logger.error(f"CSV export error: {e}")
        st.error(f"Export failed: {e}")
        return None

@st.cache_data
def get_default_unit_rates():
    """Get default unit rates with caching"""
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
    """Centralized function to clear DataFrames with proper schema and error handling"""
    try:
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
        logger.info(f"Cleared {df_type} dataframe for {sheet_name or 'main'}")
    except Exception as e:
        logger.error(f"Error clearing dataframe: {e}")
        st.error(f"Clear operation failed: {e}")

def create_export_button(data, filename, button_text, file_prefix="export"):
    """Centralized export button creation with error handling"""
    try:
        if isinstance(data, pd.DataFrame):
            csv_data = export_to_csv(data, filename)
        else:
            csv_data = data
        
        if csv_data:
            return st.download_button(
                button_text,
                data=csv_data,
                file_name=f"{file_prefix}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    except Exception as e:
        logger.error(f"Export button creation error: {e}")
        st.error(f"Export button failed: {e}")

def get_next_id(df_type, sheet_name=None):
    """Get the next available ID for a DataFrame with error handling"""
    try:
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
    except Exception as e:
        logger.error(f"Error getting next ID: {e}")
        return 1

def validate_and_strip(text):
    """Validate and strip text input with error handling"""
    try:
        return text.strip() if text else ""
    except Exception as e:
        logger.error(f"Text validation error: {e}")
        return ""

def create_standardized_button(label, button_type='neutral', key=None, help_text=None):
    """Create standardized button with consistent styling"""
    try:
        button_params = {'label': label}
        
        if BUTTON_TYPES[button_type] is not None:
            button_params['type'] = BUTTON_TYPES[button_type]
        
        if key:
            button_params['key'] = key
        
        if help_text:
            button_params['help'] = help_text
        
        return st.button(**button_params)
    except Exception as e:
        logger.error(f"Button creation error: {e}")
        return st.button(label)

def create_standardized_form_button(label, button_type='primary', key=None):
    """Create standardized form submit button"""
    try:
        button_params = {'label': label}
        
        if BUTTON_TYPES[button_type] is not None:
            button_params['type'] = BUTTON_TYPES[button_type]
        
        if key:
            button_params['key'] = key
        
        return st.form_submit_button(**button_params)
    except Exception as e:
        logger.error(f"Form button creation error: {e}")
        return st.form_submit_button(label)

def create_standardized_columns(layout_type):
    """Create standardized column layouts"""
    try:
        if layout_type in COLUMN_LAYOUTS:
            return st.columns(COLUMN_LAYOUTS[layout_type])
        else:
            return st.columns([1, 1])
    except Exception as e:
        logger.error(f"Column layout error: {e}")
        return st.columns([1, 1])

def create_ssr_selection_section(key_prefix="ssr"):
    """Standardized SSR code selection UI component with error handling"""
    try:
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
    except Exception as e:
        logger.error(f"SSR selection error: {e}")
        st.error(f"SSR selection failed: {e}")
        return "Select SSR Code...", None

# Initialize the application
initialize_session_state()

# Custom CSS for better UI
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
        .stSpinner > div {
            border-top-color: #1f4e79 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Main App Header
st.markdown("""
    <div class="main-header">
        <h1>🏗️ Construction Estimation System</h1>
        <p>Professional Construction Cost Estimation Tool - Optimized Version</p>
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

# Add performance monitoring
if st.sidebar.button("🔄 Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.success("Cache cleared successfully!")

# Dashboard Page
if page == "📊 Dashboard":
    st.title("📊 Project Dashboard")
    
    try:
        # Summary metrics with error handling
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
            total_cost = st.session_state.abstract_items['amount'].sum() if not st.session_state.abstract_items.empty else 0
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
            col1, col2 = create_standardized_columns('stats')
            
            with col1:
                unit_counts = st.session_state.measurements['unit'].value_counts()
                st.write("**Most Used Units:**")
                for unit, count in unit_counts.head(3).items():
                    st.write(f"• {unit}: {count} items")
            
            with col2:
                total_by_unit = st.session_state.measurements.groupby('unit')['total'].sum()
                st.write("**Total Quantities:**")
                for unit, total in total_by_unit.head(3).items():
                    st.write(f"• {unit}: {total:.2f}")
        
        # Performance metrics
        st.subheader("⚡ System Performance")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cache_info = st.cache_data.get_stats()
            st.metric("Cache Hits", len(cache_info))
        
        with col2:
            memory_usage = st.session_state.measurements.memory_usage(deep=True).sum() if not st.session_state.measurements.empty else 0
            st.metric("Memory Usage", f"{memory_usage / 1024:.1f} KB")
        
        with col3:
            total_records = sum(len(df) for df in st.session_state.measurement_sheets.values())
            st.metric("Total Records", total_records)
            
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        st.error(f"Dashboard loading error: {e}")

# Add a simple placeholder for other pages to demonstrate the structure
elif page == "📋 General Abstract":
    st.title("📋 General Abstract of Cost")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "💰 Abstract of Cost":
    st.title("💰 Abstract of Cost")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "📝 Measurement Sheets":
    st.title("📝 Measurement Sheets")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "📊 Technical Report":
    st.title("📊 Technical Report")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "📚 SSR Database":
    st.title("📚 Standard Schedule of Rates (SSR)")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "📥 Import Excel Data":
    st.title("📥 Import Excel Data")
    st.info("🚧 This section is being optimized. Full implementation available in the complete version.")
    
elif page == "🔧 System Tools":
    st.title("🔧 System Tools & Utilities")
    
    st.subheader("🔧 Performance Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Cache"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("All caches cleared!")
        
        if st.button("📊 Memory Report"):
            total_memory = 0
            for key, value in st.session_state.items():
                if isinstance(value, pd.DataFrame):
                    memory = value.memory_usage(deep=True).sum()
                    total_memory += memory
                    st.write(f"• {key}: {memory / 1024:.1f} KB")
            st.write(f"**Total Memory Usage: {total_memory / 1024:.1f} KB**")
    
    with col2:
        if st.button("🔍 System Diagnostics"):
            st.write("**System Status:**")
            st.write(f"• Streamlit Version: {st.__version__}")
            st.write(f"• Pandas Version: {pd.__version__}")
            st.write(f"• NumPy Version: {np.__version__}")
            st.write(f"• Session State Keys: {len(st.session_state.keys())}")
        
        if st.button("📈 Performance Metrics"):
            cache_stats = st.cache_data.get_stats()
            st.write("**Cache Statistics:**")
            st.write(f"• Cache entries: {len(cache_stats)}")
            st.write(f"• Session uptime: {datetime.now().strftime('%H:%M:%S')}")

# Footer with version info
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🏗️ Construction Estimation System v2.0 (Optimized) | Built with Streamlit</p>
        <p>Performance Enhanced • Memory Optimized • Deployment Ready</p>
    </div>
""", unsafe_allow_html=True)