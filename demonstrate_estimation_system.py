#!/usr/bin/env python3
"""
Demonstration script for the Construction Estimation System
This script provides a guided walkthrough of the system's features
"""

import os
import sys
import subprocess
import time

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🏗️  {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n{step_num}. {description}")

def print_info(message):
    """Print an info message"""
    print(f"   ℹ️  {message}")

def print_success(message):
    """Print a success message"""
    print(f"   ✅ {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"   ⚠️  {message}")

def wait_for_user():
    """Wait for user input"""
    input("\nPress Enter to continue...")

def main():
    """Main demonstration function"""
    print_header("CONSTRUCTION ESTIMATION SYSTEM - DEMONSTRATION")
    
    print("This script will guide you through the key features of the")
    print("Construction Estimation System for Excel.")
    
    wait_for_user()
    
    # Step 1: System Overview
    print_header("SYSTEM OVERVIEW")
    print_step(1, "System Components")
    print_info("The Construction Estimation System consists of:")
    print("   • VBA modules for core functionality")
    print("   • User interface forms")
    print("   • Sample Excel templates")
    print("   • Comprehensive documentation")
    
    print_step(2, "Key Features")
    print_info("The system provides:")
    print("   • Dynamic Excel import with auto-mapping")
    print("   • Real-time formula linkages")
    print("   • Interactive user interface")
    print("   • Multi-format export (PDF, Excel, CSV, HTML)")
    print("   • Data validation and protection")
    
    wait_for_user()
    
    # Step 2: Installation
    print_header("INSTALLATION PROCESS")
    print_step(1, "Prerequisites")
    print_info("Before using the system, ensure you have:")
    print("   • Microsoft Excel 2016 or later (Windows)")
    print("   • Macro support enabled")
    print("   • Read/write permissions for saving files")
    
    print_step(2, "Installation Steps")
    print_info("To install the system:")
    print("   1. Open Excel")
    print("   2. Press Alt+F11 to open the VBA editor")
    print("   3. Import the .bas and .frm files")
    print("   4. Close the VBA editor")
    print("   5. Save as a macro-enabled workbook (.xlsm)")
    print("   6. Enable macros when prompted")
    
    wait_for_user()
    
    # Step 3: Main Features
    print_header("MAIN FEATURES WALKTHROUGH")
    
    print_step(1, "Dynamic Sheet Structure")
    print_info("The system automatically creates and maintains linkages between:")
    print("   • General Abstract: Master summary of all parts")
    print("   • Abstract of Cost [Part Name]: Detailed cost breakdown")
    print("   • Measurement [Part Name]: Quantity calculations")
    
    print_step(2, "Keyboard Shortcuts")
    print_info("Access all features quickly with these shortcuts:")
    print("   • Alt+F1: Show Help")
    print("   • Alt+F2: Add New Item")
    print("   • Alt+F3: Delete Selected Item")
    print("   • Alt+F4: Add New Part")
    print("   • Alt+F5: Delete Part")
    print("   • Alt+F6: Export to PDF")
    print("   • Alt+F7: Multi-Format Export")
    
    print_step(3, "Import Functionality")
    print_info("Import existing Excel files with automatic sheet mapping:")
    print("   1. Press Alt+F1 then select 'Import Sample Estimate'")
    print("   2. Choose your Excel file")
    print("   3. System auto-maps and links sheets")
    
    print_step(4, "Export Options")
    print_info("Export your estimate in multiple formats:")
    print("   • PDF: Print-ready document with proper formatting")
    print("   • Excel: Clean copy without protection")
    print("   • HTML: Single-file printable version")
    print("   • CSV: Zipped package with one file per sheet")
    
    wait_for_user()
    
    # Step 4: Usage Examples
    print_header("USAGE EXAMPLES")
    
    print_step(1, "Creating a New Estimate")
    print_info("To create a new estimate:")
    print("   1. Open the template file")
    print("   2. System creates 'General Abstract' and 'Ground Floor' part")
    print("   3. Add items using Alt+F2")
    print("   4. Add new parts using Alt+F4")
    
    print_step(2, "Adding Items")
    print_info("To add items to your estimate:")
    print("   1. Select appropriate sheet (Abstract or Measurement)")
    print("   2. Press Alt+F2 or click 'Add New Item'")
    print("   3. Enter item details when prompted")
    print("   4. System generates formulas and linkages automatically")
    
    print_step(3, "Managing Parts")
    print_info("To manage parts in your estimate:")
    print("   • Add Part: Press Alt+F4 to create new paired sheets")
    print("   • Delete Part: Press Alt+F5 to remove part and update General Abstract")
    
    print_step(4, "Exporting Your Estimate")
    print_info("To export your completed estimate:")
    print("   1. Press Alt+F6 for PDF or Alt+F7 for multi-format options")
    print("   2. Choose desired format")
    print("   3. Enter project name and select save location")
    print("   4. System generates properly formatted document")
    
    wait_for_user()
    
    # Step 5: Best Practices
    print_header("BEST PRACTICES")
    
    print_step(1, "Naming Conventions")
    print_info("Use descriptive part names:")
    print("   • Good: 'First Floor', 'Roof Structure'")
    print("   • Avoid special characters: \\ / : * ? \" < > | [ ]")
    
    print_step(2, "Data Entry")
    print_info("For accurate results:")
    print("   • Always enter data in unlocked cells")
    print("   • Formulas in protected cells update automatically")
    print("   • Use consistent units of measurement")
    
    print_step(3, "File Management")
    print_info("To protect your work:")
    print("   • Regularly save your work")
    print("   • Use export function to create backup copies")
    print("   • System maintains logs in hidden sheets")
    
    wait_for_user()
    
    # Step 6: Troubleshooting
    print_header("TROUBLESHOOTING")
    
    print_step(1, "Common Issues")
    print_info("Solutions for common problems:")
    print("   • Macros not running: Enable all macros in security settings")
    print("   • Formulas not updating: Press Ctrl+Alt+F9 to force calculation")
    print("   • Sheet protection errors: Use 'Reset System' to rebuild structure")
    
    print_step(2, "Error Messages")
    print_info("Understanding system messages:")
    print("   • 'General Abstract sheet is missing': System will recreate it")
    print("   • 'Invalid part name': Check for special characters")
    print("   • 'Part already exists': Choose a different name")
    
    wait_for_user()
    
    # Conclusion
    print_header("CONCLUSION")
    print("The Construction Estimation System provides a comprehensive")
    print("solution for construction professionals to create, manage,")
    print("and export detailed cost estimates.")
    
    print("\n📋 KEY BENEFITS:")
    print("   • Save time with automated calculations")
    print("   • Reduce errors with dynamic linkages")
    print("   • Improve accuracy with real-time updates")
    print("   • Enhance professionalism with multi-format exports")
    print("   • Increase productivity with intuitive interface")
    
    print("\n📚 DOCUMENTATION:")
    print("   • User Guide: EstimationSystem_UserGuide.md")
    print("   • Technical Details: README_ESTIMATION_SYSTEM.md")
    print("   • VBA Source Code: VBA_*.bas files")
    
    print("\nFor technical support, please refer to the documentation")
    print("or contact the development team.")
    
    print_success("\nDemonstration complete!")
    
    # Offer to open documentation
    print("\nWould you like to view the user guide?")
    choice = input("Enter 'y' to open documentation, or any other key to exit: ").lower()
    
    if choice == 'y':
        user_guide = "EstimationSystem_UserGuide.md"
        if os.path.exists(user_guide):
            print_info(f"Opening {user_guide}...")
            # Try to open with default application
            try:
                if sys.platform == "win32":
                    os.startfile(user_guide)
                else:
                    subprocess.run(["open", user_guide], check=True)
            except:
                print_warning("Could not open file automatically. Please open EstimationSystem_UserGuide.md manually.")
        else:
            print_warning("User guide not found in current directory.")
    
    print("\nThank you for using the Construction Estimation System!")

if __name__ == "__main__":
    main()