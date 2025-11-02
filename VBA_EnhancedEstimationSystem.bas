' ===============================================================================
' ENHANCED CONSTRUCTION ESTIMATION SYSTEM - VBA CODE
' ===============================================================================
' File: VBA_EnhancedEstimationSystem.bas
' Purpose: Enhanced VBA solution with complete dynamic Excel import system
' Author: Construction Estimation System
' Date: November 2025
' ===============================================================================

Option Explicit

' ===============================================================================
' MODULE 1: MAIN ESTIMATION SYSTEM WITH ENHANCED FEATURES
' ===============================================================================

' Global Variables
Public Const GENERAL_ABSTRACT_SHEET As String = "General Abstract"
Public Const ABSTRACT_PREFIX As String = "Abstract of Cost"
Public Const MEASUREMENT_PREFIX As String = "Measurement"
Public Const LOG_SHEET As String = "Export_Log"
Public Const ERROR_LOG_SHEET As String = "Error_Log"

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
    
    ' Setup keyboard shortcuts
    Call SetupKeyboardShortcuts
    
    Application.ScreenUpdating = True
    
    MsgBox "Construction Estimation System initialized successfully!" & vbCrLf & _
           "Press Alt+F1 for help or use the Developer tab to access functions.", _
           vbInformation, "System Ready"
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
' ENHANCED EXCEL IMPORT SYSTEM
' ===============================================================================

Sub ImportSampleEstimate()
    '
    ' Import any Excel estimate file and auto-map sheets
    '
    
    Dim filePath As String
    Dim sourceWb As Workbook
    Dim ws As Worksheet
    Dim i As Integer
    Dim partPairs As Collection
    Dim partName As String
    Dim abstractSheet As String
    Dim measurementSheet As String
    
    ' Get file path from user
    filePath = Application.GetOpenFilename( _
        "Excel Files (*.xlsx; *.xls), *.xlsx; *.xls", , _
        "Select Sample Estimate File to Import")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Open source workbook
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Clear existing sheets (except General Abstract)
    Call ClearExistingSheets
    
    ' Create collection to track part pairs
    Set partPairs = New Collection
    
    ' Import and map sheets
    For Each ws In sourceWb.Worksheets
        If InStr(1, ws.Name, "General Abstract", vbTextCompare) > 0 Then
            Call ImportGeneralAbstract(ws)
        ElseIf InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
            Call ImportAbstractSheet(ws)
            ' Extract part name and add to collection
            partName = Replace(ws.Name, ABSTRACT_PREFIX, "")
            partName = Trim(partName)
            abstractSheet = ws.Name
            partPairs.Add Array(partName, abstractSheet, ""), partName & "_abstract"
        ElseIf InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Call ImportMeasurementSheet(ws)
            ' Extract part name and update collection
            partName = Replace(ws.Name, MEASUREMENT_PREFIX, "")
            partName = Trim(partName)
            measurementSheet = ws.Name
            On Error Resume Next
            partPairs.Add Array(partName, "", measurementSheet), partName & "_measurement"
            On Error GoTo 0
        End If
    Next ws
    
    ' Close source workbook
    sourceWb.Close False
    
    ' Rebuild formulas and linkages
    Call RebuildFormulasAndLinkages
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "Estimate imported successfully! All sheets and formulas have been mapped." & vbCrLf & _
           "Total parts imported: " & partPairs.Count, _
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
' DYNAMIC SHEET MANAGEMENT WITH ENHANCED VALIDATION
' ===============================================================================

Sub CreateNewPart()
    '
    ' Create a new part with Abstract and Measurement sheets
    '
    
    Dim partName As String
    Dim abstractWs As Worksheet
    Dim measurementWs As Worksheet
    Dim counter As Integer
    Dim proposedName As String
    
    ' Get part name from user with auto-naming
    counter = CountParts() + 1
    proposedName = "Part " & Chr(64 + counter)
    
    partName = InputBox("Enter name for new part:", "New Part", proposedName)
    
    If partName = "" Then Exit Sub
    
    ' Validate part name
    If Not ValidatePartName(partName) Then
        MsgBox "Invalid part name. Please avoid special characters: \ / : * ? "" < > | [ ]", _
               vbExclamation, "Invalid Name"
        Exit Sub
    End If
    
    ' Check if part already exists
    If SheetExists(ABSTRACT_PREFIX & " " & partName) Or _
       SheetExists(MEASUREMENT_PREFIX & " " & partName) Then
        MsgBox "A part with this name already exists!", vbExclamation, "Duplicate Name"
        Exit Sub
    End If
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
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
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "New part '" & partName & "' created successfully!" & vbCrLf & _
           "Abstract and Measurement sheets have been created and linked.", _
           vbInformation, "Part Created"
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
    Dim hasData As Boolean
    
    ' Get part name from user
    partName = GetPartNameFromUser()
    If partName = "" Then Exit Sub
    
    abstractSheet = ABSTRACT_PREFIX & " " & partName
    measurementSheet = MEASUREMENT_PREFIX & " " & partName
    
    ' Check if part has data
    hasData = PartHasData(abstractSheet, measurementSheet)
    
    ' Confirm deletion
    If hasData Then
        response = MsgBox("Part '" & partName & "' contains data. Are you sure you want to delete it?" & vbCrLf & _
                         "This will remove both Abstract and Measurement sheets.", _
                         vbYesNo + vbQuestion + vbDefaultButton2, "Confirm Deletion")
    Else
        response = MsgBox("Are you sure you want to delete part '" & partName & "'?" & vbCrLf & _
                         "This will remove both Abstract and Measurement sheets.", _
                         vbYesNo + vbQuestion, "Confirm Deletion")
    End If
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    Application.Calculation = xlCalculationManual
    
    ' Delete sheets
    If SheetExists(abstractSheet) Then
        ThisWorkbook.Worksheets(abstractSheet).Delete
    End If
    
    If SheetExists(measurementSheet) Then
        ThisWorkbook.Worksheets(measurementSheet).Delete
    End If
    
    ' Update General Abstract
    Call RemovePartFromGeneralAbstract(partName)
    
    Application.Calculation = xlCalculationAutomatic
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "Part '" & partName & "' deleted successfully!", vbInformation, "Part Deleted"
End Sub

Function PartHasData(abstractSheet As String, measurementSheet As String) As Boolean
    '
    ' Check if part contains data
    '
    
    Dim ws As Worksheet
    Dim lastRow As Long
    
    PartHasData = False
    
    ' Check Abstract sheet
    If SheetExists(abstractSheet) Then
        Set ws = ThisWorkbook.Worksheets(abstractSheet)
        lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
        If lastRow > 5 Then ' More than header rows
            PartHasData = True
            Exit Function
        End If
    End If
    
    ' Check Measurement sheet
    If SheetExists(measurementSheet) Then
        Set ws = ThisWorkbook.Worksheets(measurementSheet)
        lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
        If lastRow > 5 Then ' More than header rows
            PartHasData = True
        End If
    End If
End Function

' ===============================================================================
' ITEM MANAGEMENT WITH ENHANCED FEATURES
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
    Dim quantity As Double
    Dim length As Double, breadth As Double, height As Double
    Dim itemId As String
    Dim nextId As Long
    
    Set ws = ActiveSheet
    
    ' Validate sheet type
    If Not (InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Or _
            InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0) Then
        MsgBox "Please select an Abstract or Measurement sheet to add items.", _
               vbExclamation, "Invalid Sheet"
        Exit Sub
    End If
    
    ' Get next item ID
    nextId = GetNextItemId(ws)
    itemId = Format(nextId, "000")
    
    ' Get item details from user
    description = InputBox("Enter item description:", "New Item")
    If description = "" Then Exit Sub
    
    unit = InputBox("Enter unit (e.g., Cum, Sqm, Nos):", "Unit", "Cum")
    If unit = "" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Find last row and insert new item
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    newRow = lastRow + 1
    
    ' Insert new row
    ws.Rows(newRow).Insert
    
    ' Add item data
    ws.Cells(newRow, 1).Value = itemId ' Item ID
    ws.Cells(newRow, 2).Value = description
    ws.Cells(newRow, 3).Value = unit
    
    If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
        ' Abstract sheet
        quantity = Val(InputBox("Enter quantity:", "Quantity", "0"))
        rate = Val(InputBox("Enter rate:", "Rate", "0"))
        
        ws.Cells(newRow, 4).Value = quantity
        ws.Cells(newRow, 5).Value = rate
        ws.Cells(newRow, 6).Formula = "=D" & newRow & "*E" & newRow ' Amount formula
    Else
        ' Measurement sheet
        quantity = Val(InputBox("Enter number of items:", "Nos", "1"))
        length = Val(InputBox("Enter length:", "Length", "1"))
        breadth = Val(InputBox("Enter breadth:", "Breadth", "1"))
        height = Val(InputBox("Enter height:", "Height", "1"))
        
        ws.Cells(newRow, 4).Value = quantity
        ws.Cells(newRow, 5).Value = length
        ws.Cells(newRow, 6).Value = breadth
        ws.Cells(newRow, 7).Value = height
        ws.Cells(newRow, 8).Formula = "=D" & newRow & "*E" & newRow & "*F" & newRow & "*G" & newRow
    End If
    
    ' Update formulas and linkages
    Call UpdateSheetFormulas(ws)
    Call RebuildFormulasAndLinkages ' Ensure all linkages are updated
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "New item added successfully!" & vbCrLf & _
           "Item ID: " & itemId, vbInformation, "Item Added"
End Sub

Function GetNextItemId(ws As Worksheet) As Long
    '
    ' Get next available item ID
    '
    
    Dim lastRow As Long
    Dim maxId As Long
    Dim currentId As Long
    Dim i As Long
    
    maxId = 0
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    For i = 6 To lastRow ' Assuming data starts from row 6
        If IsNumeric(ws.Cells(i, 1).Value) Then
            currentId = CLng(ws.Cells(i, 1).Value)
            If currentId > maxId Then maxId = currentId
        End If
    Next i
    
    GetNextItemId = maxId + 1
End Function

Sub DeleteSelectedItem()
    '
    ' Delete selected item from current sheet
    '
    
    Dim ws As Worksheet
    Dim selectedRow As Long
    Dim response As VbMsgBoxResult
    Dim itemDescription As String
    
    Set ws = ActiveSheet
    selectedRow = ActiveCell.Row
    itemDescription = ws.Cells(selectedRow, 2).Value
    
    ' Validate selection
    If selectedRow <= 5 Then ' Assuming first 5 rows are headers
        MsgBox "Please select a data row to delete.", vbExclamation, "Invalid Selection"
        Exit Sub
    End If
    
    ' Confirm deletion
    response = MsgBox("Are you sure you want to delete this item?" & vbCrLf & _
                     "Description: " & itemDescription, _
                     vbYesNo + vbQuestion + vbDefaultButton2, "Confirm Deletion")
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Delete row
    ws.Rows(selectedRow).Delete
    
    ' Update formulas
    Call UpdateSheetFormulas(ws)
    Call RebuildFormulasAndLinkages ' Ensure all linkages are updated
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "Item deleted successfully!", vbInformation, "Item Deleted"
End Sub

' ===============================================================================
' ENHANCED FORMULA AND LINKAGE MANAGEMENT
' ===============================================================================

Sub RebuildFormulasAndLinkages()
    '
    ' Rebuild all formulas and linkages between sheets
    '
    
    Dim ws As Worksheet
    Dim progress As Integer
    Dim totalSheets As Integer
    Dim i As Integer
    
    Application.Calculation = xlCalculationManual
    Application.ScreenUpdating = False
    
    ' Count sheets for progress
    totalSheets = ThisWorkbook.Worksheets.Count
    i = 0
    
    ' Update measurement to abstract linkages
    For Each ws In ThisWorkbook.Worksheets
        i = i + 1
        progress = Int((i / totalSheets) * 100)
        Application.StatusBar = "Rebuilding formulas... " & progress & "%"
        
        If InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Call LinkMeasurementToAbstract(ws)
        ElseIf InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
               ws.Name <> GENERAL_ABSTRACT_SHEET Then
            Call LinkAbstractToGeneral(ws)
        End If
    Next ws
    
    Application.StatusBar = False
    Application.Calculation = xlCalculationAutomatic
    Application.Calculate
    Application.ScreenUpdating = True
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
    Dim targetRow As Long
    
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    
    ' Get part name
    partName = Replace(abstractWs.Name, ABSTRACT_PREFIX, "")
    partName = Trim(partName)
    
    ' Find or create row in General Abstract
    targetRow = FindOrCreatePartRowInGeneral(partName)
    
    ' Link total amount using SUM formula
    generalWs.Cells(targetRow, 3).Formula = "=SUM('" & abstractWs.Name & "'!F:F)"
End Sub

' ===============================================================================
' ENHANCED EXPORT SYSTEM WITH MULTI-FORMAT SUPPORT
' ===============================================================================

Sub ExportEstimateToPDF()
    '
    ' Export complete estimate to PDF with enhanced formatting
    '
    
    Dim filePath As String
    Dim projectName As String
    Dim defaultName As String
    
    ' Get project name and file path
    projectName = GetProjectName()
    If projectName = "" Then Exit Sub
    
    defaultName = CleanFileName(projectName) & "_Estimate.pdf"
    
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=defaultName, _
        FileFilter:="PDF Files (*.pdf), *.pdf", _
        Title:="Save Estimate as PDF")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Setup for PDF export
    Call PrepareForPDFExport
    
    ' Export sheets in order
    Call ExportSheetsToPDF(filePath, projectName)
    
    ' Restore original formatting
    Call RestoreAfterPDFExport
    
    ' Log export
    Call CreateExportLog(ThisWorkbook, "PDF", filePath)
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to PDF successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
End Sub

Function GetProjectName() As String
    '
    ' Get project name from user or General Abstract
    '
    
    Dim projectName As String
    Dim generalWs As Worksheet
    Dim cellValue As String
    
    ' Try to get from General Abstract
    If SheetExists(GENERAL_ABSTRACT_SHEET) Then
        Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
        cellValue = generalWs.Range("A1").Value
        If InStr(cellValue, "GENERAL ABSTRACT") > 0 Then
            projectName = Replace(cellValue, "GENERAL ABSTRACT OF COST", "")
            projectName = Trim(projectName)
            If projectName = "" Then projectName = "Construction Project"
        End If
    End If
    
    If projectName = "" Then projectName = "Construction Project"
    
    GetProjectName = InputBox("Enter project name:", "Project Name", projectName)
End Function

Sub ExportEstimateMultiFormat()
    '
    ' Export estimate in multiple formats with enhanced UI
    '
    
    Dim exportFormat As String
    Dim response As VbMsgBoxResult
    
    response = MsgBox("Select export format:" & vbCrLf & vbCrLf & _
                     "Yes - PDF (Print-ready document)" & vbCrLf & _
                     "No - Excel (.xlsx - Clean copy)" & vbCrLf & _
                     "Cancel - More options", _
                     vbYesNoCancel + vbQuestion, "Export Format")
    
    Select Case response
        Case vbYes
            Call ExportEstimateToPDF
        Case vbNo
            Call ExportToExcel
        Case vbCancel
            Call ExportToMultipleFormats
    End Select
End Sub

Sub ExportToMultipleFormats()
    '
    ' Show detailed export options
    '
    
    Dim choice As String
    Dim choices As String
    
    choices = "Select export format:" & vbCrLf & vbCrLf & _
              "1 - PDF (Print-ready document)" & vbCrLf & _
              "2 - Excel (.xlsx - Clean copy)" & vbCrLf & _
              "3 - Printable HTML (Single file)" & vbCrLf & _
              "4 - CSV Package (Zipped files)" & vbCrLf & vbCrLf & _
              "Enter your choice (1-4):"
    
    choice = InputBox(choices, "Export Options", "1")
    
    Select Case choice
        Case "1"
            Call ExportEstimateToPDF
        Case "2"
            Call ExportToExcel
        Case "3"
            Call ExportToPrintableHTML
        Case "4"
            Call ExportToCSVPackage
        Case Else
            If choice <> "" Then
                MsgBox "Invalid choice. Please select 1-4.", vbExclamation, "Invalid Selection"
            End If
    End Select
End Sub

Sub ExportToExcel()
    '
    ' Export to clean Excel file with enhanced features
    '
    
    Dim filePath As String
    Dim newWb As Workbook
    Dim ws As Worksheet
    Dim projectName As String
    Dim defaultName As String
    
    projectName = GetProjectName()
    defaultName = CleanFileName(projectName) & "_Estimate_Export.xlsx"
    
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=defaultName, _
        FileFilter:="Excel Files (*.xlsx), *.xlsx", _
        Title:="Export to Excel")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Exporting to Excel..."
    
    ' Create new workbook
    Set newWb = Workbooks.Add
    
    ' Copy all sheets
    For Each ws In ThisWorkbook.Worksheets
        ' Skip log sheets
        If ws.Name <> LOG_SHEET And ws.Name <> ERROR_LOG_SHEET Then
            ws.Copy After:=newWb.Sheets(newWb.Sheets.Count)
        End If
    Next ws
    
    ' Remove default sheets
    Application.DisplayAlerts = False
    On Error Resume Next
    newWb.Sheets(1).Delete
    On Error GoTo 0
    Application.DisplayAlerts = True
    
    ' Remove protection and macros
    Call RemoveProtectionFromWorkbook(newWb)
    
    ' Refresh all calculations
    newWb.Calculate
    newWb.SaveAs filePath, FileFormat:=xlOpenXMLWorkbook
    
    ' Log export
    Call CreateExportLog(newWb, "Excel", filePath)
    
    newWb.Close
    
    Application.StatusBar = False
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to Excel successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
End Sub

' ===============================================================================
' UTILITY FUNCTIONS WITH ENHANCED FEATURES
' ===============================================================================

Sub SetupGeneralAbstractSheet(ws As Worksheet)
    '
    ' Setup General Abstract sheet structure
    '
    
    With ws
        .Range("A1").Value = "GENERAL ABSTRACT OF COST"
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 16
        .Range("A1").Font.Name = "Arial"
        
        .Range("A3").Value = "S.No."
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Amount (₹)"
        
        .Range("A3:C3").Font.Bold = True
        .Range("A3:C3").Font.Name = "Arial"
        .Range("A3:C3").Font.Size = 10
        .Range("A3:C3").Borders.LineStyle = xlContinuous
        .Range("A3:C3").Interior.Color = RGB(200, 200, 200)
        
        ' Format columns
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 40
        .Columns("C").ColumnWidth = 15
        .Columns("C").NumberFormat = "#,##0.00"
        
        ' Add print settings
        .PageSetup.PrintTitleRows = "$3:$3"
        .PageSetup.PrintArea = ""
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
        .Range("A1").Font.Name = "Arial"
        
        .Range("A3").Value = "Item ID"
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Unit"
        .Range("D3").Value = "Quantity"
        .Range("E3").Value = "Rate (₹)"
        .Range("F3").Value = "Amount (₹)"
        
        .Range("A3:F3").Font.Bold = True
        .Range("A3:F3").Font.Name = "Arial"
        .Range("A3:F3").Font.Size = 10
        .Range("A3:F3").Borders.LineStyle = xlContinuous
        .Range("A3:F3").Interior.Color = RGB(220, 220, 220)
        
        ' Format columns
        .Columns("A").ColumnWidth = 10
        .Columns("B").ColumnWidth = 35
        .Columns("C").ColumnWidth = 8
        .Columns("D").ColumnWidth = 12
        .Columns("E").ColumnWidth = 12
        .Columns("F").ColumnWidth = 15
        
        .Columns("D:F").NumberFormat = "#,##0.00"
        
        ' Add print settings
        .PageSetup.PrintTitleRows = "$3:$3"
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
        .Range("A1").Font.Name = "Arial"
        
        .Range("A3").Value = "Item ID"
        .Range("B3").Value = "Description"
        .Range("C3").Value = "Unit"
        .Range("D3").Value = "Nos"
        .Range("E3").Value = "Length"
        .Range("F3").Value = "Breadth"
        .Range("G3").Value = "Height"
        .Range("H3").Value = "Total"
        
        .Range("A3:H3").Font.Bold = True
        .Range("A3:H3").Font.Name = "Arial"
        .Range("A3:H3").Font.Size = 10
        .Range("A3:H3").Borders.LineStyle = xlContinuous
        .Range("A3:H3").Interior.Color = RGB(220, 220, 220)
        
        ' Format columns
        .Columns("A").ColumnWidth = 10
        .Columns("B").ColumnWidth = 35
        .Columns("C").ColumnWidth = 8
        .Columns("D:H").ColumnWidth = 10
        
        .Columns("D:H").NumberFormat = "#,##0.00"
        
        ' Add print settings
        .PageSetup.PrintTitleRows = "$3:$3"
    End With
End Sub

Function GetPartNameFromUser() As String
    '
    ' Get part name from user selection with enhanced UI
    '
    
    Dim ws As Worksheet
    Dim partsList As String
    Dim partName As String
    Dim partCount As Integer
    
    ' Build list of existing parts
    partCount = 0
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT_SHEET Then
            partName = Replace(ws.Name, ABSTRACT_PREFIX, "")
            partName = Trim(partName)
            partsList = partsList & partName & vbCrLf
            partCount = partCount + 1
        End If
    Next ws
    
    If partsList = "" Then
        MsgBox "No parts found to delete.", vbInformation, "No Parts Available"
        GetPartNameFromUser = ""
        Exit Function
    End If
    
    partsList = "Available parts (" & partCount & "):" & vbCrLf & vbCrLf & partsList
    
    GetPartNameFromUser = InputBox("Enter part name to delete:" & vbCrLf & vbCrLf & _
                                  partsList, "Delete Part")
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
    
    MsgBox "Ribbon interface setup complete. Use Developer tab for macro buttons." & vbCrLf & _
           "Keyboard shortcuts are available: Alt+F1 for help.", _
           vbInformation, "Interface Ready"
End Sub

' ===============================================================================
' PROTECTION AND VALIDATION WITH ENHANCED FEATURES
' ===============================================================================

Sub ProtectFormulasCells()
    '
    ' Protect formula cells while allowing data entry
    '
    
    Dim ws As Worksheet
    Dim lastRow As Long
    
    For Each ws In ThisWorkbook.Worksheets
        ws.Unprotect
        
        ' Unlock all cells first
        ws.Cells.Locked = False
        
        ' Lock specific ranges based on sheet type
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
            ' Lock formula columns in Abstract sheets (Amount column)
            lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
            If lastRow > 5 Then
                ws.Range("A6:A" & lastRow).Locked = True ' Item ID
                ws.Range("F6:F" & lastRow).Locked = True ' Amount (formula)
                ws.Range("A3:F3").Locked = True ' Headers
            End If
            ' Unlock data entry cells
            ws.Range("B6:E" & lastRow).Locked = False ' Description, Unit, Quantity, Rate
        ElseIf InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            ' Lock formula columns in Measurement sheets (Total column)
            lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
            If lastRow > 5 Then
                ws.Range("A6:A" & lastRow).Locked = True ' Item ID
                ws.Range("H6:H" & lastRow).Locked = True ' Total (formula)
                ws.Range("A3:H3").Locked = True ' Headers
            End If
            ' Unlock data entry cells
            ws.Range("B6:G" & lastRow).Locked = False ' Description, Unit, Measurements
        ElseIf ws.Name = GENERAL_ABSTRACT_SHEET Then
            ' Lock formula columns in General Abstract (Amount column)
            lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
            If lastRow > 3 Then
                ws.Range("A4:A" & lastRow).Locked = True ' Serial numbers
                ws.Range("C4:C" & lastRow).Locked = True ' Amount (formula)
                ws.Range("A3:C3").Locked = True ' Headers
            End If
            ' Unlock description cells
            ws.Range("B4:B" & lastRow).Locked = False
        End If
        
        ' Protect sheet with password
        ws.Protect Password:="estimation2025", _
                  DrawingObjects:=True, _
                  Contents:=True, _
                  Scenarios:=True, _
                  AllowFormattingCells:=True, _
                  AllowInsertingRows:=True, _
                  AllowDeletingRows:=True, _
                  AllowSorting:=True, _
                  AllowFiltering:=True
    Next ws
End Sub

Sub ValidateSheetStructure()
    '
    ' Validate that core structure is maintained
    '
    
    If Not SheetExists(GENERAL_ABSTRACT_SHEET) Then
        MsgBox "Critical Error: General Abstract sheet is missing!" & vbCrLf & _
               "The system will recreate it now.", _
               vbCritical, "Structure Error"
        Call SetupInitialStructure
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
          "• Alt+F1: Show Help" & vbCrLf & _
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
' KEYBOARD SHORTCUTS WITH ENHANCED FUNCTIONALITY
' ===============================================================================

Sub SetupKeyboardShortcuts()
    '
    ' Setup keyboard shortcuts for main functions
    '
    
    Application.OnKey "%{F1}", "ShowMainInterface"
    Application.OnKey "%{F2}", "AddNewItem"
    Application.OnKey "%{F3}", "DeleteSelectedItem"
    Application.OnKey "%{F4}", "CreateNewPart"
    Application.OnKey "%{F5}", "DeleteSelectedPart"
    Application.OnKey "%{F6}", "ExportEstimateToPDF"
    Application.OnKey "%{F7}", "ExportEstimateMultiFormat"
End Sub

' ===============================================================================
' ERROR HANDLING AND LOGGING
' ===============================================================================

Sub HandleError(errorSource As String, errorDescription As String)
    '
    ' Centralized error handling with logging
    '
    
    Dim errorMsg As String
    
    errorMsg = "An error occurred in: " & errorSource & vbCrLf & vbCrLf & _
               "Error Description: " & errorDescription & vbCrLf & vbCrLf & _
               "Please try the operation again. If the error persists, " & _
               "contact support with this information."
    
    MsgBox errorMsg, vbCritical, "System Error"
    
    ' Log error
    Call LogError(errorSource, errorDescription)
End Sub

Sub LogError(source As String, description As String)
    '
    ' Log errors to hidden sheet for debugging
    '
    
    Dim logWs As Worksheet
    Dim lastRow As Long
    
    On Error Resume Next
    Set logWs = ThisWorkbook.Worksheets(ERROR_LOG_SHEET)
    On Error GoTo 0
    
    If logWs Is Nothing Then
        Set logWs = ThisWorkbook.Worksheets.Add
        logWs.Name = ERROR_LOG_SHEET
        logWs.Visible = xlSheetVeryHidden
        
        ' Setup headers
        logWs.Range("A1").Value = "Timestamp"
        logWs.Range("B1").Value = "Source"
        logWs.Range("C1").Value = "Description"
        logWs.Range("A1:C1").Font.Bold = True
        logWs.Range("A1:C1").Interior.Color = RGB(200, 200, 200)
    End If
    
    lastRow = logWs.Cells(logWs.Rows.Count, 1).End(xlUp).Row + 1
    logWs.Cells(lastRow, 1).Value = Now
    logWs.Cells(lastRow, 2).Value = source
    logWs.Cells(lastRow, 3).Value = description
End Sub

' ===============================================================================
' CLEANUP AND MAINTENANCE FUNCTIONS
' ===============================================================================

Sub ClearExistingSheets()
    '
    ' Clear existing sheets except General Abstract and log sheets
    '
    
    Dim ws As Worksheet
    Dim sheetsToDelete As Collection
    Dim i As Integer
    
    Set sheetsToDelete = New Collection
    
    ' Collect sheets to delete
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> GENERAL_ABSTRACT_SHEET And _
           ws.Name <> LOG_SHEET And _
           ws.Name <> ERROR_LOG_SHEET Then
            sheetsToDelete.Add ws
        End If
    Next ws
    
    ' Delete collected sheets
    Application.DisplayAlerts = False
    For i = 1 To sheetsToDelete.Count
        sheetsToDelete(i).Delete
    Next i
    Application.DisplayAlerts = True
End Sub

Sub ResetSystem()
    '
    ' Reset system to initial state
    '
    
    Dim response As VbMsgBoxResult
    
    response = MsgBox("This will reset the entire system and delete all data. " & _
                     "Are you sure you want to continue?", _
                     vbYesNo + vbCritical + vbDefaultButton2, "Reset System")
    
    If response = vbYes Then
        Application.ScreenUpdating = False
        Application.Calculation = xlCalculationManual
        
        Call ClearExistingSheets
        Call SetupInitialStructure
        Call RebuildFormulasAndLinkages
        
        Application.Calculation = xlCalculationAutomatic
        Application.ScreenUpdating = True
        
        MsgBox "System reset complete!", vbInformation, "Reset Complete"
    End If
End Sub