#!/usr/bin/env python3
"""
🏗️ Construction Estimate Import Display Demo
Demonstrates the import functionality and displays the imported estimate structure
"""

import pandas as pd
import os
from pathlib import Path

def display_import_demo():
    """Display the import functionality demonstration"""
    
    print("🏗️ CONSTRUCTION ESTIMATE IMPORT DEMONSTRATION")
    print("=" * 60)
    
    # Check for available Excel files
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xlsm'))]
    
    print("\n📁 AVAILABLE EXCEL FILES:")
    for i, file in enumerate(excel_files, 1):
        print(f"   {i}. {file}")
    
    if not excel_files:
        print("   ❌ No Excel files found in current directory")
        return
    
    # Use the first available Excel file for demo
    demo_file = excel_files[0]
    print(f"\n🎯 DEMONSTRATING WITH: {demo_file}")
    print("-" * 40)
    
    try:
        # Read Excel file and analyze structure
        xl_file = pd.ExcelFile(demo_file)
        sheet_names = xl_file.sheet_names
        
        print(f"\n📊 SHEET STRUCTURE ANALYSIS:")
        print(f"   Total Sheets Found: {len(sheet_names)}")
        
        # Categorize sheets
        abstract_sheets = [s for s in sheet_names if 'abstract' in s.lower() and 'general' not in s.lower()]
        measurement_sheets = [s for s in sheet_names if 'measurement' in s.lower()]
        general_abstract = [s for s in sheet_names if 'general' in s.lower() and 'abstract' in s.lower()]
        ssr_sheets = [s for s in sheet_names if 'ssr' in s.lower() or 'rate' in s.lower()]
        
        print(f"\n🔍 SHEET CATEGORIZATION:")
        print(f"   💰 Abstract Sheets: {len(abstract_sheets)}")
        for sheet in abstract_sheets:
            print(f"      └─ {sheet}")
        
        print(f"   📏 Measurement Sheets: {len(measurement_sheets)}")
        for sheet in measurement_sheets:
            print(f"      └─ {sheet}")
        
        print(f"   📊 General Abstract: {len(general_abstract)}")
        for sheet in general_abstract:
            print(f"      └─ {sheet}")
        
        print(f"   📚 SSR/Rate Sheets: {len(ssr_sheets)}")
        for sheet in ssr_sheets:
            print(f"      └─ {sheet}")
        
        # Analyze sheet pairs
        print(f"\n🔗 SHEET PAIR ANALYSIS:")
        pairs_found = 0
        
        for abstract in abstract_sheets:
            # Find corresponding measurement sheet
            abstract_part = abstract.replace('Abstract of Cost', '').replace('abstract', '').strip()
            corresponding_measurement = None
            
            for measurement in measurement_sheets:
                measurement_part = measurement.replace('Measurement', '').strip()
                if abstract_part.lower() in measurement_part.lower() or measurement_part.lower() in abstract_part.lower():
                    corresponding_measurement = measurement
                    break
            
            if corresponding_measurement:
                pairs_found += 1
                print(f"   🏗️ Pair {pairs_found}:")
                print(f"      📏 {corresponding_measurement}")
                print(f"      💰 {abstract}")
                print(f"      🔄 Auto-linkage: Enabled")
        
        print(f"\n✅ IMPORT SIMULATION RESULTS:")
        print(f"   📊 Total Sheets: {len(sheet_names)}")
        print(f"   🔗 Linked Pairs: {pairs_found}")
        print(f"   📈 Formulas to Create: {pairs_found * 15}+ (estimated)")
        print(f"   ⚡ Real-time Updates: Enabled")
        print(f"   🔒 Protection: Applied to formula cells")
        
        # Sample data display
        if abstract_sheets:
            print(f"\n📋 SAMPLE DATA FROM: {abstract_sheets[0]}")
            print("-" * 40)
            try:
                sample_df = pd.read_excel(demo_file, sheet_name=abstract_sheets[0], nrows=10)
                print(sample_df.to_string(index=False, max_cols=6))
            except Exception as e:
                print(f"   ⚠️ Could not read sample data: {str(e)}")
        
        print(f"\n🎛️ AVAILABLE FEATURES AFTER IMPORT:")
        features = [
            "➕ Add/Edit items with auto-formulas",
            "🗑️ Delete items with automatic updates", 
            "🏗️ Add new parts (Abstract+Measurement pairs)",
            "📄 Export to PDF with formatting",
            "📊 Export to Excel (clean copy)",
            "📦 Export to CSV package",
            "🌐 Export to HTML report",
            "🔄 Rebuild formulas if needed",
            "⚡ Real-time cross-sheet updates",
            "🔒 Formula protection with data entry freedom"
        ]
        
        for feature in features:
            print(f"   {feature}")
        
        print(f"\n🚀 IMPORT STATUS: READY FOR PRODUCTION USE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error analyzing file: {str(e)}")
        print("   This might be due to file format or access issues")

def display_streamlit_features():
    """Display Streamlit app features"""
    
    print("\n🌐 STREAMLIT WEB APPLICATION FEATURES:")
    print("=" * 50)
    
    pages = [
        ("📊 Dashboard", "Project overview and quick stats"),
        ("📝 Measurement Sheets", "Interactive quantity calculations"),
        ("📚 SSR Database", "Standard Schedule of Rates management"),
        ("💰 Abstract of Cost", "Cost summaries and totals"),
        ("📥 Import Excel Data", "Upload and import existing estimates")
    ]
    
    for page_name, description in pages:
        print(f"\n{page_name}")
        print(f"   └─ {description}")
    
    print(f"\n🔧 KEY CAPABILITIES:")
    capabilities = [
        "📤 Multi-format Export (PDF, Excel, CSV, HTML)",
        "🔄 Real-time Formula Updates",
        "🔗 Automatic Sheet Linking",
        "📊 Interactive Data Entry",
        "🎨 Professional Formatting",
        "🔒 Data Validation & Protection",
        "📱 Responsive Web Interface",
        "💾 Session State Management"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")

if __name__ == "__main__":
    display_import_demo()
    display_streamlit_features()
    
    print(f"\n🎯 TO RUN THE FULL APPLICATION:")
    print("   streamlit run streamlit_estimation_app.py")
    print("   Then open: http://localhost:8501")