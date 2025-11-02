# Construction Estimation System

## Overview
This is a comprehensive Excel-based construction estimation system with dynamic import capabilities, real-time calculations, and multi-format export functionality.

## Key Features Implemented

### 1. Dynamic Excel Import System
- Automatically loads any Excel estimate file while preserving formulas and sheet linkages
- Auto-maps sheets based on naming patterns ("Abstract of Cost*" and "Measurement*" pairs)
- Maintains hierarchical summation logic between all sheets

### 2. Automatic Linkage Rules
- Quantities from "Measurement [Part/Floor]" sheets SUM dynamically into corresponding "Abstract of Cost [Part/Floor]" sheets
- Totals from each "Abstract of Cost [Part/Floor]" sheet SUM dynamically into the "General Abstract" sheet
- Uses structured, named ranges to maintain integrity when rows are added/removed

### 3. Interactive Interface
- [Import Sample Estimate] button: Load any .xlsx estimate file with auto-mapping
- [Add New Item] button: Insert new rows with user-input fields and auto-generated unique IDs
- [Delete Item] button: Remove selected rows and update all dependent sums instantly
- [Add New Part] button: Create new paired sheets with auto-linking to General Abstract
- [Delete Part] button: Remove part pairs and update General Abstract accordingly

### 4. Real-Time Recalculation
- Any change in Measurement quantity instantly updates Abstract amount (Qty × Rate)
- Changes propagate to General Abstract without manual refresh
- Full compatibility with Excel 2016+ (Windows) and .xlsx format

### 5. Enhanced Validation
- Prevents deletion of sheets that break core structure (e.g., General Abstract)
- Warns when deleting parts that contain data
- Auto-names new parts sequentially if user leaves blank (e.g., Part A, Part B)

### 6. Multi-Format Export System
- **PDF Export**: Single multi-page document with proper formatting
- **Excel Export**: Clean .xlsx copy with current data and structure
- **HTML Export**: Single printable HTML file with styled tables
- **CSV Package**: Zipped collection of one CSV per sheet

### 7. Additional Features
- Protection of formula cells while allowing data entry in designated cells
- Export logs in hidden sheets for tracking
- Progress indicators for large operations
- Comprehensive error handling and logging

## Files Included

### VBA Modules
1. **VBA_EstimationSystem.bas** - Core system functionality
2. **VBA_ExportModule.bas** - Advanced export capabilities
3. **VBA_HelperFunctions.bas** - Utility functions and helpers
4. **VBA_EnhancedEstimationSystem.bas** - Enhanced features and improvements
5. **UserForm_MainInterface.frm** - Main interface form

### Documentation
1. **EstimationSystem_UserGuide.md** - Complete user guide
2. **README_ESTIMATION_SYSTEM.md** - This file

### Sample Files
1. **XXXX.xlsx** - Sample estimate file in [attached_assets](file://c:\Users\Rajkumar\estimate_replit\attached_assets) folder

## How to Use the System

### Initial Setup
1. Open the Excel template file
2. Enable macros when prompted
3. The system will initialize automatically with a sample structure

### Keyboard Shortcuts
- **Alt+F1**: Show Help
- **Alt+F2**: Add New Item
- **Alt+F3**: Delete Selected Item
- **Alt+F4**: Add New Part
- **Alt+F5**: Delete Part
- **Alt+F6**: Export to PDF
- **Alt+F7**: Multi-Format Export

### Importing Existing Estimates
1. Press **Alt+F1** and select "Import Sample Estimate"
2. Choose your Excel file
3. The system will automatically map and link all sheets

### Creating New Parts
1. Press **Alt+F4** or use the "Add New Part" button
2. Enter a name for your new part
3. The system creates paired Abstract and Measurement sheets with proper linkages

### Exporting Your Work
1. Press **Alt+F6** for PDF or **Alt+F7** for multi-format options
2. Choose your desired format
3. Enter project name and select save location

## Testing the System
The system has been tested with the provided sample "XXXX" estimate file with the following operations:
- Add/remove items in Ground Floor
- Add a new Part "Roof"
- Delete an existing Part
- Verify all totals in General Abstract update correctly

## System Requirements
- Microsoft Excel 2016 or later (Windows only)
- Macro support enabled
- Read/write permissions for saving files

## Support
For issues or questions, please refer to the User Guide or contact technical support.