@echo off
title Construction Estimation System - Packaging Tool

echo ====================================================
echo 📦 CONSTRUCTION ESTIMATION SYSTEM - PACKAGING TOOL
echo ====================================================
echo.

echo This tool will create a distributable package of the
echo Construction Estimation System with all required files.
echo.

:: Create package directory
set package_dir=EstimationSystem_Package_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%
set package_dir=%package_dir: =0%
echo Creating package directory: %package_dir%
mkdir "%package_dir%" >nul 2>&1

if not exist "%package_dir%" (
    echo ❌ Failed to create package directory
    pause
    exit /b 1
)

echo ✅ Package directory created
echo.

:: Copy main files
echo Copying main files...
copy "*.bas" "%package_dir%\" >nul 2>&1
copy "*.frm" "%package_dir%\" >nul 2>&1
copy "*.frx" "%package_dir%\" >nul 2>&1
copy "README_ESTIMATION_SYSTEM.md" "%package_dir%\" >nul 2>&1
copy "EstimationSystem_UserGuide.md" "%package_dir%\" >nul 2>&1

echo ✅ Main files copied
echo.

:: Copy sample files
echo Copying sample files...
if exist "attached_assets" (
    xcopy "attached_assets" "%package_dir%\attached_assets\" /E /I /H /Y >nul 2>&1
    echo ✅ Sample files copied
) else (
    echo ⚠️  No sample files found
)
echo.

:: Create installation instructions
echo Creating installation instructions...
(
    echo # Installation Instructions
    echo.
    echo ## Prerequisites
    echo 1. Microsoft Excel 2016 or later ^(Windows only^)
    echo 2. Macro support enabled
    echo.
    echo ## Installation Steps
    echo 1. Open Excel
    echo 2. Press Alt+F11 to open the VBA editor
    echo 3. Import the .bas and .frm files from this package
    echo 4. Close the VBA editor
    echo 5. Save the workbook as a macro-enabled file ^(.xlsm^)
    echo 6. Enable macros when prompted
    echo.
    echo ## Getting Started
    echo 1. The system will initialize automatically when you open the file
    echo 2. Use Alt+F1 for help and to access all features
    echo 3. Refer to EstimationSystem_UserGuide.md for detailed instructions
    echo.
    echo ## Support
    echo For issues or questions, please refer to the documentation
) > "%package_dir%\INSTALLATION_INSTRUCTIONS.txt"

echo ✅ Installation instructions created
echo.

:: Create version file
echo Creating version information...
(
    echo Construction Estimation System
    echo Version: 2.0
    echo Release Date: %date%
    echo Platform: Microsoft Excel 2016+
    echo.
    echo Packaged on: %date% at %time%
) > "%package_dir%\VERSION.txt"

echo ✅ Version information created
echo.

:: Compress to ZIP if available
echo Checking for compression tools...
if exist "%ProgramFiles%\7-Zip\7z.exe" (
    echo Found 7-Zip - creating compressed archive...
    "%ProgramFiles%\7-Zip\7z.exe" a -tzip "%package_dir%.zip" "%package_dir%\*"
    if !errorlevel! equ 0 (
        echo ✅ Package compressed to %package_dir%.zip
    ) else (
        echo ⚠️  Compression failed, package folder available uncompressed
    )
) else (
    echo 7-Zip not found - package available as folder only
    echo You can manually compress the folder using Windows Explorer
)

echo.
echo ====================================================
echo 🎉 PACKAGING COMPLETE
echo ====================================================
echo.
echo Package location: %package_dir%
if exist "%package_dir%.zip" echo Compressed package: %package_dir%.zip
echo.
echo Contents:
echo ├── VBA modules ^(.bas files^)
echo ├── User form files ^(.frm, .frx^)
echo ├── Documentation ^(README, User Guide^)
echo ├── Sample files ^(if available^)
echo ├── Installation instructions
echo └── Version information
echo.
echo To install:
echo 1. Extract the package contents
echo 2. Follow INSTALLATION_INSTRUCTIONS.txt
echo 3. Import the VBA files into Excel
echo.
pause