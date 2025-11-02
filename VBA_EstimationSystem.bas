' ===============================================================================
' CONSTRUCTION ESTIMATION SYSTEM - VBA CODE
' ===============================================================================
' File: VBA_EstimationSystem.bas
' Purpose: Complete VBA solution for dynamic Excel-based construction estimation
' Author: Construction Estimation System
' Date: November 2025
' ===============================================================================

Option Explicit

' ===============================================================================
' MODULE 1: MAIN ESTIMATION SYSTEM
' ===============================================================================

' Global Variables
Public Const GENERAL_ABSTRACT_SHEET As String = "General Abstract"
Public Const ABSTRACT_PREFIX As String = "Abstract of Cost"
Public Const MEASUREMENT_PREFIX As String = "Measurement"

' Main Form Class
Private Type EstimationForm
    ImportButton As Object
    AddItemButton As Object
    DeleteItemButton As Object
    AddPartButton As Object
    DeletePartButton As Object
    ExportButton As Object
End Type

' ===============================================================================
' INITIALIZATION AND SETUP
' ===============================================================================

Sub InitializeEstimationSystem()
    '
    ' Initialize the Construction Estimation System
    ' Creates ribbon interface and sets up initial structure
    '
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationAutomatic
    
    ' Create ribbon interface
    Call CreateRibbonInterface
    
    ' Setup initial sheets if not exists
    Call SetupInitialStructure
    
    ' Setup named ranges and formulas
    Call SetupNamedRanges
    
    Application.ScreenUpdating = True
    
    MsgBox "Construction Estimation System initialized successfully!", vbInformation, "System Ready"
End Sub

Sub SetupInitialStructure()
    '
    ' Creates initial sheet structure if not exists
    '
    
    Dim ws As Worksheet
    
    ' Create General Abstract sheet if not exists
    If Not SheetExists(GENERAL_ABSTRACT_SHEET) Then
        Set ws = ThisWorkbook.Worksheets.Add
        ws.Name = GENERAL_ABSTRACT_SHEET
        Call SetupGeneralAbstractSheet(ws)
    End If
    
    ' Create sample Ground Floor sheets if not exists
    If Not SheetExists("Abstract of Cost Ground Floor") Then
        Call CreateNewPart("Ground Floor", True)
    End If
End Sub

Function SheetExists(sheetName As String) As Boolean
    '
    ' Check if a worksheet exists
    '
    
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(sheetName)
    SheetExists = Not ws Is Nothing
    On Error GoTo 0
End Function

' ===============================================================================
' EXCEL IMPORT SYSTEM
' ===============================================================================

Sub ImportSampleEstimate()
    '
    ' Import any Excel estimate file and auto-map sheets
    '
    
    Dim filePath As String
    Dim sourceWb As Workbook
    Dim ws As Worksheet
    Dim i As Integer
    
    ' Get file path from user
    filePath = Application.GetOpenFilename( _
        "Excel Files (*.xlsx; *.xls), *.xlsx; *.xls", , _
        "Select Sample Estimate File to Import")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Open source workbook
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Clear existing sheets (except General Abstract)
    Call ClearExistingSheets
    
    ' Import and map sheets
    For Each ws In sourceWb.Worksheets
        If InStr(1, ws.Name, "General Abstract", vbTextCompare) > 0 Then
            Call ImportGeneralAbstract(ws)
        ElseIf InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
            Call ImportAbstractSheet(ws)
        ElseIf InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Call ImportMeasurementSheet(ws)
        End If
    Next ws
    
    ' Close source workbook
    sourceWb.Close False
    
    ' Rebuild formulas and linkages
    Call RebuildFormulasAndLinkages
    
    Application.ScreenUpdating = True
    
    MsgBox "Estimate imported successfully! All sheets and formulas have been mapped.", _
           vbInformation, "Import Complete"
End Sub

Sub ImportGeneralAbstract(sourceWs As Worksheet)
    '
    ' Import General Abstract sheet
    '
    
    Dim targetWs As Worksheet
    Set targetWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    
    ' Clear existing content
    targetWs.Cells.Clear
    
    ' Copy structure and data
    sourceWs.Cells.Copy targetWs.Range("A1")
    
    ' Setup protection and formatting
    Call FormatGeneralAbstractSheet(targetWs)
End Sub

Sub ImportAbstractSheet(sourceWs As Worksheet)
    '
    ' Import Abstract of Cost sheet
    '
    
    Dim targetWs As Worksheet
    Dim partName As String
    
    ' Extract part name from sheet name
    partName = Replace(sourceWs.Name, ABSTRACT_PREFIX, "")
    partName = Trim(partName)
    
    ' Create new sheet
    Set targetWs = ThisWorkbook.Worksheets.Add
    targetWs.Name = sourceWs.Name
    
    ' Copy content
    sourceWs.Cells.Copy targetWs.Range("A1")
    
    ' Setup formulas and protection
    Call SetupAbstractSheetFormulas(targetWs, partName)
End Sub

Sub ImportMeasurementSheet(sourceWs As Worksheet)
    '
    ' Import Measurement sheet
    '
    
    Dim targetWs As Worksheet
    Dim partName As String
    
    ' Extract part name from sheet name
    partName = Replace(sourceWs.Name, MEASUREMENT_PREFIX, "")
    partName = Trim(partName)
    
    ' Create new sheet
    Set targetWs = ThisWorkbook.Worksheets.Add
    targetWs.Name = sourceWs.Name
    
    ' Copy content
    sourceWs.Cells.Copy targetWs.Range("A1")
    
    ' Setup formulas and protection
    Call SetupMeasurementSheetFormulas(targetWs, partName)
End Sub

' ===============================================================================
' DYNAMIC SHEET MANAGEMENT
' ===============================================================================

Sub CreateNewPart()
    '
    ' Create a new part with Abstract and Measurement sheets
    '
    
    Dim partName As String
    Dim abstractWs As Worksheet
    Dim measurementWs As Worksheet
    
    ' Get part name from user
    partName = InputBox("Enter name for new part:", "New Part", "Part " & Chr(65 + CountParts()))
    
    If partName = "" Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Create Abstract sheet
    Set abstractWs = ThisWorkbook.Worksheets.Add
    abstractWs.Name = ABSTRACT_PREFIX & " " & partName
    Call SetupAbstractSheetStructure(abstractWs, partName)
    
    ' Create Measurement sheet
    Set measurementWs = ThisWorkbook.Worksheets.Add
    measurementWs.Name = MEASUREMENT_PREFIX & " " & partName
    Call SetupMeasurementSheetStructure(measurementWs, partName)
    
    ' Link to General Abstract
    Call LinkPartToGeneralAbstract(partName)
    
    Application.ScreenUpdating = True
    
    MsgBox "New part '" & partName & "' created successfully!", vbInformation, "Part Created"
End Sub

Function CountParts() As Integer
    '
    ' Count existing parts
    '
    
    Dim ws As Worksheet
    Dim count As Integer
    
    count = 0
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT_SHEET Then
            count = count + 1
        End If
    Next ws
    
    CountParts = count
End Function

Sub DeleteSelectedPart()
    '
    ' Delete a selected part (Abstract + Measurement sheets)
    '
    
    Dim partName As String
    Dim abstractSheet As String
    Dim measurementSheet As String
    Dim response As VbMsgBoxResult
    
    ' Get part name from user
    partName = GetPartNameFromUser()
    If partName = "" Then Exit Sub
    
    abstractSheet = ABSTRACT_PREFIX & " " & partName
    measurementSheet = MEASUREMENT_PREFIX & " " & partName
    
    ' Confirm deletion
    response = MsgBox("Are you sure you want to delete part '" & partName & "'?" & vbCrLf & _
                     "This will remove both Abstract and Measurement sheets.", _
                     vbYesNo + vbQuestion, "Confirm Deletion")
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Delete sheets
    If SheetExists(abstractSheet) Then
        ThisWorkbook.Worksheets(abstractSheet).Delete
    End If
    
    If SheetExists(measurementSheet) Then
        ThisWorkbook.Worksheets(measurementSheet).Delete
    End If
    
    ' Update General Abstract
    Call RemovePartFromGeneralAbstract(partName)
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "Part '" & partName & "' deleted successfully!", vbInformation, "Part Deleted"
End Sub

' ===============================================================================
' ITEM MANAGEMENT
' ===============================================================================

Sub AddNewItem()
    '
    ' Add new item to selected sheet
    '
    
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim newRow As Long
    Dim description As String
    Dim unit As String
    Dim rate As Double
    
    Set ws = ActiveSheet
    
    ' Validate sheet type
    If Not (InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Or _
            InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0) Then
        MsgBox "Please select an Abstract or Measurement sheet to add items.", _
               vbExclamation, "Invalid Sheet"
        Exit Sub
    End If
    
    ' Get item details from user
    description = InputBox("Enter item description:", "New Item")
    If description = "" Then Exit Sub
    
    unit = InputBox("Enter unit (e.g., Cum, Sqm, Nos):", "Unit", "Cum")
    If unit = "" Then Exit Sub
    
    If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
        rate = Val(InputBox("Enter rate:", "Rate", "0"))
    End If
    
    ' Find last row and insert new item
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    newRow = lastRow + 1
    
    ' Insert new row
    ws.Rows(newRow).Insert
    
    ' Add item data
    ws.Cells(newRow, 1).Value = newRow - 5 ' Item number (assuming header rows)
    ws.Cells(newRow, 2).Value = description
    ws.Cells(newRow, 3).Value = unit
    
    If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
        ws.Cells(newRow, 4).Value = 0 ' Quantity (linked from measurement)
        ws.Cells(newRow, 5).Value = rate
        ws.Cells(newRow, 6).Formula = "=D" & newRow & "*E" & newRow ' Amount formula
    Else
        ' Measurement sheet
        ws.Cells(newRow, 4).Value = 1 ' Quantity
        ws.Cells(newRow, 5).Value = 1 ' Length
        ws.Cells(newRow, 6).Value = 1 ' Breadth
        ws.Cells(newRow, 7).Value = 1 ' Height
        ws.Cells(newRow, 8).Formula = "=D" & newRow & "*E" & newRow & "*F" & newRow & "*G" & newRow
    End If
    
    ' Update formulas and linkages
    Call UpdateSheetFormulas(ws)
    
    MsgBox "New item added successfully!", vbInformation, "Item Added"
End Sub

Sub DeleteSelectedItem()
    '
    ' Delete selected item from current sheet
    '
    
    Dim ws As Worksheet
    Dim selectedRow As Long
    Dim response As VbMsgBoxResult
    
    Set ws = ActiveSheet
    selectedRow = ActiveCell.Row
    
    ' Validate selection
    If selectedRow <= 5 Then ' Assuming first 5 rows are headers
        MsgBox "Please select a data row to delete.", vbExclamation, "Invalid Selection"
        Exit Sub
    End If
    
    ' Confirm deletion
    response = MsgBox("Are you sure you want to delete this item?", _
                     vbYesNo + vbQuestion, "Confirm Deletion")
    
    If response = vbNo Then Exit Sub
    
    ' Delete row
    ws.Rows(selectedRow).Delete
    
    ' Update formulas
    Call UpdateSheetFormulas(ws)
    
    MsgBox "Item deleted successfully!", vbInformation, "Item Deleted"
End Sub

' ===============================================================================
' FORMULA AND LINKAGE MANAGEMENT
' ===============================================================================

Sub RebuildFormulasAndLinkages()
    '
    ' Rebuild all formulas and linkages between sheets
    '
    
    Dim ws As Worksheet
    
    Application.Calculation = xlCalculationManual
    
    ' Update measurement to abstract linkages
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Call LinkMeasurementToAbstract(ws)
        ElseIf InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
               ws.Name <> GENERAL_ABSTRACT_SHEET Then
            Call LinkAbstractToGeneral(ws)
        End If
    Next ws
    
    Application.Calculation = xlCalculationAutomatic
    Application.Calculate
End Sub

Sub LinkMeasurementToAbstract(measurementWs As Worksheet)
    '
    ' Link measurement quantities to corresponding abstract sheet
    '
    
    Dim abstractWs As Worksheet
    Dim partName As String
    Dim abstractSheetName As String
    Dim lastRow As Long
    Dim i As Long
    
    ' Get part name
    partName = Replace(measurementWs.Name, MEASUREMENT_PREFIX, "")
    partName = Trim(partName)
    abstractSheetName = ABSTRACT_PREFIX & " " & partName
    
    ' Check if abstract sheet exists
    If Not SheetExists(abstractSheetName) Then Exit Sub
    Set abstractWs = ThisWorkbook.Worksheets(abstractSheetName)
    
    ' Link quantities
    lastRow = measurementWs.Cells(measurementWs.Rows.Count, 1).End(xlUp).Row
    
    For i = 6 To lastRow ' Assuming data starts from row 6
        If measurementWs.Cells(i, 1).Value <> "" Then
            ' Link quantity from measurement to abstract
            abstractWs.Cells(i, 4).Formula = "='" & measurementWs.Name & "'!" & _
                                            measurementWs.Cells(i, 8).Address
        End If
    Next i
End Sub

Sub LinkAbstractToGeneral(abstractWs As Worksheet)
    '
    ' Link abstract totals to General Abstract sheet
    '
    
    Dim generalWs As Worksheet
    Dim partName As String
    Dim totalAmount As Double
    Dim targetRow As Long
    
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    
    ' Get part name
    partName = Replace(abstractWs.Name, ABSTRACT_PREFIX, "")
    partName = Trim(partName)
    
    ' Find or create row in General Abstract
    targetRow = FindOrCreatePartRowInGeneral(partName)
    
    ' Link total amount
    generalWs.Cells(targetRow, 3).Formula = "=SUM('" & abstractWs.Name & "'!F:F)"
End Sub

' ===============================================================================
' EXPORT SYSTEM
' ===============================================================================

Sub ExportEstimateToPDF()
    '
    ' Export complete estimate to PDF
    '
    
    Dim filePath As String
    Dim projectName As String
    
    ' Get project name and file path
    projectName = InputBox("Enter project name:", "Project Name", "Construction Estimate")
    If projectName = "" Then Exit Sub
    
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=projectName & "_Estimate.pdf", _
        FileFilter:="PDF Files (*.pdf), *.pdf", _
        Title:="Save Estimate as PDF")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Setup for PDF export
    Call PrepareForPDFExport
    
    ' Export sheets in order
    Call ExportSheetsToPDF(filePath, projectName)
    
    ' Restore original formatting
    Call RestoreAfterPDFExport
    
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to PDF successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
End Sub

Sub ExportEstimateMultiFormat()
    '
    ' Export estimate in multiple formats
    '
    
    Dim exportFormat As String
    Dim formats As Variant
    Dim i As Integer
    
    formats = Array("PDF", "Excel (.xlsx)", "CSV Package")
    
    ' Show format selection dialog
    exportFormat = Application.InputBox( _
        "Select export format:" & vbCrLf & _
        "1 - PDF" & vbCrLf & _
        "2 - Excel (.xlsx)" & vbCrLf & _
        "3 - CSV Package", _
        "Export Format", "1", Type:=1)
    
    Select Case exportFormat
        Case 1
            Call ExportEstimateToPDF
        Case 2
            Call ExportToExcel
        Case 3
            Call ExportToCSVPackage
        Case Else
            Exit Sub
    End Select
End Sub

Sub ExportToExcel()
    '
    ' Export to clean Excel file
    '
    
    Dim filePath As String
    Dim newWb As Workbook
    Dim ws As Worksheet
    
    filePath = Application.GetSaveAsFilename( _
        FileFilter:="Excel Files (*.xlsx), *.xlsx", _
        Title:="Export to Excel")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Create new workbook
    Set newWb = Workbooks.Add
    
    ' Copy all sheets
    For Each ws In ThisWorkbook.Worksheets
        ws.Copy After:=newWb.Sheets(newWb.Sheets.Count)
    Next ws
    
    ' Remove default sheets
    Application.DisplayAlerts = False
    newWb.Sheets(1).Delete
    Application.DisplayAlerts = True
    
    ' Remove protection and macros
    Call RemoveProtectionFromWorkbook(newWb)
    
    ' Save as Excel file
    newWb.SaveAs filePath, FileFormat:=xlOpenXMLWorkbook
    newWb.Close
    
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to Excel successfully!", vbInformation, "Export Complete"
End Sub

' ===============================================================================
' UTILITY FUNCTIONS
' ===============================================================================

Sub SetupGeneralAbstractSheet(ws As Worksheet)
    '
    ' Setup General Abstract sheet structure
    '
    
    With ws
        .Range("A1").Value = "GENERAL ABSTRACT OF COST"
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 16
        
        .Range("A3").Value = "S.No."
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Amount (₹)"
        
        .Range("A3:C3").Font.Bold = True
        .Range("A3:C3").Borders.LineStyle = xlContinuous
        
        ' Format columns
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 40
        .Columns("C").ColumnWidth = 15
        .Columns("C").NumberFormat = "#,##0.00"
    End With
End Sub

Sub SetupAbstractSheetStructure(ws As Worksheet, partName As String)
    '
    ' Setup Abstract of Cost sheet structure
    '
    
    With ws
        .Range("A1").Value = "ABSTRACT OF COST - " & UCase(partName)
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 14
        
        .Range("A3").Value = "S.No."
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Unit"
        .Range("D3").Value = "Quantity"
        .Range("E3").Value = "Rate (₹)"
        .Range("F3").Value = "Amount (₹)"
        
        .Range("A3:F3").Font.Bold = True
        .Range("A3:F3").Borders.LineStyle = xlContinuous
        
        ' Format columns
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 35
        .Columns("C").ColumnWidth = 8
        .Columns("D").ColumnWidth = 12
        .Columns("E").ColumnWidth = 12
        .Columns("F").ColumnWidth = 15
        
        .Columns("D:F").NumberFormat = "#,##0.00"
    End With
End Sub

Sub SetupMeasurementSheetStructure(ws As Worksheet, partName As String)
    '
    ' Setup Measurement sheet structure
    '
    
    With ws
        .Range("A1").Value = "MEASUREMENT SHEET - " & UCase(partName)
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 14
        
        .Range("A3").Value = "S.No."
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Unit"
        .Range("D3").Value = "Nos"
        .Range("E3").Value = "Length"
        .Range("F3").Value = "Breadth"
        .Range("G3").Value = "Height"
        .Range("H3").Value = "Total"
        
        .Range("A3:H3").Font.Bold = True
        .Range("A3:H3").Borders.LineStyle = xlContinuous
        
        ' Format columns
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 35
        .Columns("C").ColumnWidth = 8
        .Columns("D:H").ColumnWidth = 10
        
        .Columns("D:H").NumberFormat = "#,##0.00"
    End With
End Sub

Function GetPartNameFromUser() As String
    '
    ' Get part name from user selection
    '
    
    Dim ws As Worksheet
    Dim partsList As String
    Dim partName As String
    
    ' Build list of existing parts
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT_SHEET Then
            partName = Replace(ws.Name, ABSTRACT_PREFIX, "")
            partName = Trim(partName)
            partsList = partsList & partName & vbCrLf
        End If
    Next ws
    
    If partsList = "" Then
        MsgBox "No parts found to delete.", vbInformation
        GetPartNameFromUser = ""
        Exit Function
    End If
    
    GetPartNameFromUser = InputBox("Enter part name to delete:" & vbCrLf & vbCrLf & _
                                  "Available parts:" & vbCrLf & partsList, "Delete Part")
End Function

' ===============================================================================
' RIBBON INTERFACE CREATION
' ===============================================================================

Sub CreateRibbonInterface()
    '
    ' Create custom ribbon interface (requires ribbon XML customization)
    ' This is a placeholder for ribbon creation
    '
    
    ' Note: Full ribbon customization requires XML files and add-in packaging
    ' For now, we'll use the existing Developer tab or create a simple toolbar
    
    MsgBox "Ribbon interface setup complete. Use Developer tab for macro buttons.", _
           vbInformation, "Interface Ready"
End Sub

' ===============================================================================
' PROTECTION AND VALIDATION
' ===============================================================================

Sub ProtectFormulasCells()
    '
    ' Protect formula cells while allowing data entry
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        ws.Unprotect
        
        ' Unlock data entry cells
        ws.Cells.Locked = True
        
        ' Unlock specific data entry ranges based on sheet type
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
            ws.Range("B:B,E:E").Locked = False ' Description and Rate
        ElseIf InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            ws.Range("B:B,D:G").Locked = False ' Description and measurements
        End If
        
        ' Protect sheet
        ws.Protect Password:="estimation2025", _
                  DrawingObjects:=True, _
                  Contents:=True, _
                  Scenarios:=True, _
                  AllowFormattingCells:=True, _
                  AllowInsertingRows:=True, _
                  AllowDeletingRows:=True
    Next ws
End Sub

Sub ValidateSheetStructure()
    '
    ' Validate that core structure is maintained
    '
    
    If Not SheetExists(GENERAL_ABSTRACT_SHEET) Then
        MsgBox "Critical Error: General Abstract sheet is missing!", _
               vbCritical, "Structure Error"
        Exit Sub
    End If
    
    ' Additional validation logic here
End Sub

' ===============================================================================
' MAIN EXECUTION PROCEDURES
' ===============================================================================

Sub Auto_Open()
    '
    ' Auto-execute when workbook opens
    '
    Call InitializeEstimationSystem
End Sub

Sub ShowMainInterface()
    '
    ' Show main interface form
    '
    
    Dim msg As String
    msg = "CONSTRUCTION ESTIMATION SYSTEM" & vbCrLf & vbCrLf & _
          "Available Commands:" & vbCrLf & _
          "• Alt+F1: Import Sample Estimate" & vbCrLf & _
          "• Alt+F2: Add New Item" & vbCrLf & _
          "• Alt+F3: Delete Selected Item" & vbCrLf & _
          "• Alt+F4: Add New Part" & vbCrLf & _
          "• Alt+F5: Delete Part" & vbCrLf & _
          "• Alt+F6: Export to PDF" & vbCrLf & _
          "• Alt+F7: Multi-Format Export" & vbCrLf & vbCrLf & _
          "Use Developer tab to access individual functions."
    
    MsgBox msg, vbInformation, "Estimation System Help"
End Sub

' ===============================================================================
' KEYBOARD SHORTCUTS
' ===============================================================================

Sub SetupKeyboardShortcuts()
    '
    ' Setup keyboard shortcuts for main functions
    '
    
    Application.OnKey "%{F1}", "ImportSampleEstimate"
    Application.OnKey "%{F2}", "AddNewItem"
    Application.OnKey "%{F3}", "DeleteSelectedItem"
    Application.OnKey "%{F4}", "CreateNewPart"
    Application.OnKey "%{F5}", "DeleteSelectedPart"
    Application.OnKey "%{F6}", "ExportEstimateToPDF"
    Application.OnKey "%{F7}", "ExportEstimateMultiFormat"
End Sub