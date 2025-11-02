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

# Initialize abstract items
if 'abstract_items' not in st.session_state:
    st.session_state.abstract_items = pd.DataFrame([
        {"id": "1", "description": "Civil Work - Earth excavation, concrete foundation, brick masonry", "quantity": 51.6, "unit": "cum", "rate": 4850.0, "amount": 250260.0},
        {"id": "2", "description": "Sanitary Work - Plumbing, fixtures, drainage system", "quantity": 1, "unit": "LS", "rate": 125000.0, "amount": 125000.0},
        {"id": "3", "description": "Electrical Work - Wiring, switches, distribution board", "quantity": 1, "unit": "LS", "rate": 85000.0, "amount": 85000.0},
    ])

# Initialize attached assets path
if 'attached_assets_path' not in st.session_state:
    st.session_state.attached_assets_path = os.path.join(os.path.dirname(__file__), "attached_assets")

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

# Enhanced Excel Import Functionality
def find_estimate_files(pattern="att*.xlsx"):
    """Find estimate files in attached_assets folder matching pattern"""
    attached_assets_path = st.session_state.attached_assets_path
    if not os.path.exists(attached_assets_path):
        return []
    
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
    
    # Work type selector
    selected_work_type = st.selectbox("Select Work Type", list(WORK_TYPES.keys()))
    st.write(f"**Current Sheet:** {WORK_TYPES[selected_work_type]} {selected_work_type}")
    
    # Add measurement form
    with st.expander("➕ Add New Measurement", expanded=True):
        with st.form("add_measurement"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                item_no = st.text_input("Item No.", placeholder="1, 2, 3...")
                unit = st.selectbox("Unit", UNITS)
                
                # SSR Code selector (optional)
                ssr_codes = ["None"] + st.session_state.ssr_items['code'].tolist()
                selected_ssr = st.selectbox("Link to SSR Code (Optional)", ssr_codes)
            
            with col2:
                description = st.text_area("Description", placeholder="Enter detailed description of work item...")
                
                # Show SSR details if selected
                if selected_ssr != "None":
                    ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr].iloc[0]
                    st.info(f"**SSR:** {ssr_item['description']} | **Rate:** ₹{ssr_item['rate']:.2f}/{ssr_item['unit']}")
            
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
            
            # Show estimated cost if SSR is selected
            if selected_ssr != "None":
                ssr_item = st.session_state.ssr_items[st.session_state.ssr_items['code'] == selected_ssr].iloc[0]
                estimated_cost = total * ssr_item['rate']
                st.success(f"**Calculated Total: {total:.2f} {unit}** | **Estimated Cost: ₹{estimated_cost:,.2f}**")
            else:
                st.info(f"**Calculated Total: {total:.2f} {unit}**")
            
            submitted = st.form_submit_button("➕ Add Measurement", type="primary")
            
            if submitted and description.strip():
                new_measurement = {
                    'id': st.session_state.counter,
                    'item_no': item_no,
                    'description': description.strip(),
                    'quantity': quantity,
                    'length': length,
                    'breadth': breadth,
                    'height': height,
                    'unit': unit,
                    'total': total
                }
                
                st.session_state.measurements = pd.concat([
                    st.session_state.measurements,
                    pd.DataFrame([new_measurement])
                ], ignore_index=True)
                
                st.session_state.counter += 1
                st.success("✅ Measurement added successfully!")
                st.rerun()
            elif submitted:
                st.error("Please enter a description for the measurement.")
    
    # Display measurements
    if not st.session_state.measurements.empty:
        st.subheader(f"📋 {selected_work_type} Measurements")
        
        # Create display dataframe
        display_df = st.session_state.measurements.copy()
        
        # Add total row
        if len(display_df) > 0:
            total_quantity = display_df['total'].sum()
            total_row = pd.DataFrame([{
                'id': '',
                'item_no': 'TOTAL',
                'description': f'Total {selected_work_type}',
                'quantity': '',
                'length': '',
                'breadth': '',
                'height': '',
                'unit': display_df.iloc[0]['unit'],
                'total': total_quantity
            }])
            display_df = pd.concat([display_df, total_row], ignore_index=True)
        
        # Display table
        st.dataframe(
            display_df,
            column_config={
                "id": None,
                "item_no": "Item No.",
                "description": st.column_config.TextColumn("Description", width="large"),
                "quantity": st.column_config.NumberColumn("Qty", format="%.2f"),
                "length": st.column_config.NumberColumn("Length", format="%.2f"),
                "breadth": st.column_config.NumberColumn("Breadth", format="%.2f"),
                "height": st.column_config.NumberColumn("Height", format="%.2f"),
                "unit": "Unit",
                "total": st.column_config.NumberColumn("Total", format="%.2f")
            },
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
    col1, col2 = st.columns([2, 1])
    with col1:
        search_term = st.text_input("🔍 Search SSR Items", placeholder="Search by code or description...")
    with col2:
        categories = ["All Categories"] + sorted(st.session_state.ssr_items['category'].unique().tolist())
        selected_category = st.selectbox("Filter by Category", categories)
    
    # Filter SSR items
    filtered_ssr = st.session_state.ssr_items.copy()
    
    if search_term:
        mask = (
            filtered_ssr['code'].str.contains(search_term, case=False, na=False) |
            filtered_ssr['description'].str.contains(search_term, case=False, na=False)
        )
        filtered_ssr = filtered_ssr[mask]
    
    if selected_category != "All Categories":
        filtered_ssr = filtered_ssr[filtered_ssr['category'] == selected_category]
    
    # Display results count
    st.write(f"**Showing {len(filtered_ssr)} of {len(st.session_state.ssr_items)} items**")
    
    # Display SSR table
    if not filtered_ssr.empty:
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
        measurement_files = find_estimate_files("*measurement*.xlsx")
        if measurement_files:
            selected_file = st.selectbox("Select measurement file:", measurement_files, 
                                       format_func=lambda x: os.path.basename(x))
            if st.button("Import Selected Measurement File"):
                import_excel_measurements(selected_file)
        else:
            st.info("No measurement files found in attached_assets folder")
        
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
                    os.unlink(tmp_path)
    
    # Import SSR Tab
    with tab2:
        st.subheader("Import SSR Data from Excel")
        
        # Check for files in attached_assets
        ssr_files = find_estimate_files("*ssr*.xlsx")
        if ssr_files:
            selected_file = st.selectbox("Select SSR file:", ssr_files, 
                                       format_func=lambda x: os.path.basename(x))
            if st.button("Import Selected SSR File"):
                import_ssr_from_excel(selected_file)
        else:
            st.info("No SSR files found in attached_assets folder")
        
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
                    os.unlink(tmp_path)
    
    # Import Estimate Tab
    with tab3:
        st.subheader("Import Complete Estimate")
        st.info("Import entire estimate with all sheets and data")
        
        # Check for files in attached_assets
        estimate_files = find_estimate_files("att*.xlsx")
        if estimate_files:
            selected_file = st.selectbox("Select estimate file:", estimate_files, 
                                       format_func=lambda x: os.path.basename(x))
            if st.button("Import Selected Estimate"):
                st.info("Complete estimate import functionality would be implemented here")
                st.success(f"Would import complete estimate from: {os.path.basename(selected_file)}")
        else:
            st.info("No estimate files found in attached_assets folder matching 'att*.xlsx'")
        
        # Manual file upload
        uploaded_file = st.file_uploader("Or upload complete estimate", type=['xlsx', 'xls'], key="estimate_upload")
        if uploaded_file is not None:
            if st.button("Import Uploaded Estimate"):
                st.info("Complete estimate import functionality would be implemented here")
                st.success(f"Would import complete estimate from: {uploaded_file.name}")

# Abstract of Cost Page
elif page == "💰 Abstract of Cost":
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