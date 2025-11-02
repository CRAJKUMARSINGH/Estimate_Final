import os
import pandas as pd

print("🏗️ CONSTRUCTION ESTIMATE IMPORT DEMONSTRATION")
print("=" * 60)

# Check for Excel files
excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xlsm'))]

print(f"\n📁 AVAILABLE EXCEL FILES ({len(excel_files)} found):")
for i, file in enumerate(excel_files, 1):
    print(f"   {i}. {file}")

if excel_files:
    demo_file = excel_files[0]
    print(f"\n🎯 ANALYZING: {demo_file}")
    
    try:
        xl_file = pd.ExcelFile(demo_file)
        sheets = xl_file.sheet_names
        
        print(f"\n📊 SHEETS FOUND ({len(sheets)} total):")
        for sheet in sheets:
            print(f"   └─ {sheet}")
        
        # Categorize sheets
        abstract_sheets = [s for s in sheets if 'abstract' in s.lower() and 'general' not in s.lower()]
        measurement_sheets = [s for s in sheets if 'measurement' in s.lower()]
        
        print(f"\n🔍 SHEET ANALYSIS:")
        print(f"   💰 Abstract Sheets: {len(abstract_sheets)}")
        print(f"   📏 Measurement Sheets: {len(measurement_sheets)}")
        
        print(f"\n✅ IMPORT READY!")
        print("   🔗 Automatic linking will be established")
        print("   ⚡ Real-time updates will be enabled")
        print("   🎛️ Interactive controls will be available")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n🌐 TO RUN STREAMLIT APP:")
print("   streamlit run streamlit_estimation_app.py")