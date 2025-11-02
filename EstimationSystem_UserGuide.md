# Construction Estimation System - User Guide

## Overview
The Construction Estimation System is a powerful Excel-based tool that helps construction professionals create, manage, and export detailed cost estimates. The system provides dynamic linkages between measurement sheets and abstracts, automatic calculations, and multi-format export capabilities.

## System Requirements
- Microsoft Excel 2016 or later (Windows)
- Macro support enabled
- Read/write permissions to save files

## Installation
1. Open the Excel template file
2. Enable macros when prompted
3. The system will initialize automatically

## Main Features

### 1. Dynamic Sheet Structure
The system automatically creates and maintains linkages between:
- **General Abstract**: Master summary of all parts
- **Abstract of Cost [Part Name]**: Detailed cost breakdown for each part
- **Measurement [Part Name]**: Quantity calculations for each part

### 2. Keyboard Shortcuts
- **Alt+F1**: Show Help
- **Alt+F2**: Add New Item
- **Alt+F3**: Delete Selected Item
- **Alt+F4**: Add New Part
- **Alt+F5**: Delete Part
- **Alt+F6**: Export to PDF
- **Alt+F7**: Multi-Format Export

### 3. Import Functionality
Import existing Excel estimate files with automatic sheet mapping:
1. Press **Alt+F1** then select "Import Sample Estimate"
2. Choose your Excel file
3. The system will automatically map and link sheets

### 4. Export Options
Export your estimate in multiple formats:
- **PDF**: Print-ready document with proper formatting
- **Excel**: Clean copy without protection
- **HTML**: Single-file printable version
- **CSV**: Zipped package with one file per sheet

## How to Use

### Creating a New Estimate
1. Open the template file
2. The system automatically creates a "General Abstract" and "Ground Floor" part
3. Add items using **Alt+F2** or the "Add New Item" button
4. Add new parts using **Alt+F4** or the "Add New Part" button

### Adding Items
1. Select the appropriate sheet (Abstract or Measurement)
2. Press **Alt+F2** or click "Add New Item"
3. Enter item details when prompted
4. The system automatically generates formulas and linkages

### Managing Parts
1. **Add Part**: Press **Alt+F4** to create a new part with paired Abstract and Measurement sheets
2. **Delete Part**: Press **Alt+F5** to remove a part and update the General Abstract

### Exporting Your Estimate
1. Press **Alt+F6** for PDF export or **Alt+F7** for multi-format options
2. Choose your desired format
3. Enter project name and select save location
4. The system generates a properly formatted document

## Best Practices

### Naming Conventions
- Use descriptive part names (e.g., "First Floor", "Roof Structure")
- Avoid special characters in names: \ / : * ? " < > | [ ]

### Data Entry
- Always enter data in unlocked cells
- Formulas in protected cells update automatically
- Use consistent units of measurement

### File Management
- Regularly save your work
- Use the export function to create backup copies
- The system maintains logs in hidden sheets

## Troubleshooting

### Common Issues
1. **Macros not running**: Ensure macro security is set to "Enable all macros"
2. **Formulas not updating**: Press Ctrl+Alt+F9 to force full calculation
3. **Sheet protection errors**: Use "Reset System" function to rebuild structure

### Error Messages
- **"General Abstract sheet is missing"**: The system will automatically recreate it
- **"Invalid part name"**: Check for special characters
- **"Part already exists"**: Choose a different name

## Technical Support
For technical issues or feature requests, please contact:
- Email: support@estimationsystem.com
- Phone: +1-800-ESTIMATE

## Version Information
- Current Version: 2.0
- Release Date: November 2025
- Compatible with: Excel 2016, 2019, and Microsoft 365 (Windows)