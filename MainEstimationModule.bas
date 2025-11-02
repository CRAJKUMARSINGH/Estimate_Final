' ===============================================================================
' CONSTRUCTION ESTIMATION SYSTEM - MAIN MODULE
' ===============================================================================
' File: MainEstimationModule.bas
' Purpose: Core functionality for dynamic Excel-based construction estimation
' Compatible: Excel 2016+ (Windows)
' Author: Construction Estimation System
' Date: November 2025
' ===============================================================================

Option Explicit

' ===============================================================================
' GLOBAL CONSTANTS AND VARIABLES
' ===============================================================================

' Sheet naming constants
Public Const GENERAL_ABSTRACT As String = "General Abstract"
Public Const ABSTRACT_PREFIX As String = "Abstract of Cost"
Public Const MEASUREMENT_PREFIX As String = "Measurement"

' Application state variables
Public g_ProjectName As String
Public g_IsUpdating As Boolean
Public g_RibbonUI As IRibbonUI

' Named range prefixes
Public Const NR_ABSTRACT_DATA As String = "AbstractData_"
Public Const NR_MEASUREMENT_DATA As String = "MeasurementData_"
Public Const NR_GENERAL_DATA As String = "GeneralData"

' ===============================================================================
' SYSTEM INITIALIZATION
' ===============================================================================

Sub Auto_Open()
    '
    ' Auto-execute when workbook opens
    '
    Application.ScreenUpdating = False
    Call InitializeEstimationSystem
    Application.ScreenUpdating = True
End Sub

Sub InitializeEstimationSystem()
    '
    ' Initialize the Construction Estimation System
    '
    
    On Error GoTo ErrorHandler
    
    ' Set application properties
    Application.Calculation = xlCalculationAutomatic
    Application.EnableEvents = True
    
    ' Initialize project name
    If g_ProjectName = "" Then
        g_ProjectName = "Construction Estimate"
    End If
    
    ' Setup initial structure if needed
    Call EnsureBasicStructure
    
    ' Setup named ranges
    Call SetupNamedRanges
    
    ' Setup keyboard shortcuts
    Call SetupKeyboardShortcuts
    
    ' Show welcome message
    Call ShowWelcomeMessage
    
    Exit Sub
    
ErrorHandler:
    Call HandleError("InitializeEstimationSystem", Err.Description)
End Sub

Sub EnsureBasicStructure()
    '
    ' Ensure basic sheet structure exists
    '
    
    ' Create General Abstract if not exists
    If Not SheetExists(GENERAL_ABSTRACT) Then
        Call CreateGeneralAbstractSheet
    End If
    
    ' Create sample Ground Floor if no parts exist
    If CountPartPairs() = 0 Then
        Call CreateNewPartPair("Ground Floor", True)
    End If
End Sub

Function SheetExists(sheetName As String) As Boolean
    '
    ' Check if worksheet exists in current workbook
    '
    
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(sheetName)
    SheetExists = Not ws Is Nothing
    On Error GoTo 0
End Function

Function CountPartPairs() As Integer
    '
    ' Count existing Abstract-Measurement pairs
    '
    
    Dim ws As Worksheet
    Dim count As Integer
    
    count = 0
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            count = count + 1
        End If
    Next ws
    
    CountPartPairs = count
End Function

' ===============================================================================
' EXCEL IMPORT SYSTEM
' ===============================================================================

Sub ImportSampleEstimate()
    '
    ' Import Excel estimate file with auto-mapping
    '
    
    Dim filePath As String
    Dim sourceWb As Workbook
    Dim progressForm As Object
    
    On Error GoTo ErrorHandler
    
    ' Get file from user
    filePath = Application.GetOpenFilename( _
        "Excel Files (*.xlsx; *.xls), *.xlsx; *.xls", , _
        "Select Construction Estimate File to Import")
    
    If filePath = "False" Then Exit Sub
    
    ' Show progress indicator
    Application.StatusBar = "Importing estimate file..."
    Application.ScreenUpdating = False
    g_IsUpdating = True
    
    ' Open source workbook
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True, UpdateLinks:=False)
    
    ' Clear existing structure (except General Abstract)
    Call ClearExistingParts
    
    ' Analyze and import sheets
    Call AnalyzeAndImportSheets(sourceWb)
    
    ' Close source workbook
    sourceWb.Close False
    
    ' Rebuild all formulas and linkages
    Call RebuildAllFormulas
    
    ' Setup protection
    Call ProtectAllSheets
    
    g_IsUpdating = False
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "Estimate imported successfully!" & vbCrLf & _
           "All sheets mapped and formulas linked.", _
           vbInformation, "Import Complete"
    
    Exit Sub
    
ErrorHandler:
    If Not sourceWb Is Nothing Then sourceWb.Close False
    g_IsUpdating = False
    Application.ScreenUpdating = True
    Application.StatusBar = False
    Call HandleError("ImportSampleEstimate", Err.Description)
End Sub

Sub AnalyzeAndImportSheets(sourceWb As Workbook)
    '
    ' Analyze source workbook and import sheets with mapping
    '
    
    Dim ws As Worksheet
    Dim sheetType As String
    Dim partName As String
    
    ' First pass: Import General Abstract
    For Each ws In sourceWb.Worksheets
        sheetType = IdentifySheetType(ws.Name)
        If sheetType = "General" Then
            Call ImportGeneralAbstract(ws)
            Exit For
        End If
    Next ws
    
    ' Second pass: Import Abstract sheets
    For Each ws In sourceWb.Worksheets
        sheetType = IdentifySheetType(ws.Name)
        If sheetType = "Abstract" Then
            partName = ExtractPartName(ws.Name, "Abstract")
            Call ImportAbstractSheet(ws, partName)
        End If
    Next ws
    
    ' Third pass: Import Measurement sheets
    For Each ws In sourceWb.Worksheets
        sheetType = IdentifySheetType(ws.Name)
        If sheetType = "Measurement" Then
            partName = ExtractPartName(ws.Name, "Measurement")
            Call ImportMeasurementSheet(ws, partName)
        End If
    Next ws
End Sub

Function IdentifySheetType(sheetName As String) As String
    '
    ' Identify sheet type based on naming patterns
    '
    
    Dim name As String
    name = LCase(sheetName)
    
    If InStr(name, "general") > 0 And InStr(name, "abstract") > 0 Then
        IdentifySheetType = "General"
    ElseIf InStr(name, "abstract of cost") > 0 Or InStr(name, "abstract") > 0 Then
        IdentifySheetType = "Abstract"
    ElseIf InStr(name, "measurement") > 0 Then
        IdentifySheetType = "Measurement"
    Else
        IdentifySheetType = "Other"
    End If
End Function

Function ExtractPartName(sheetName As String, sheetType As String) As String
    '
    ' Extract part name from sheet name
    '
    
    Dim partName As String
    partName = sheetName
    
    If sheetType = "Abstract" Then
        partName = Replace(partName, "Abstract of Cost", "", 1, 1, vbTextCompare)
        partName = Replace(partName, "Abstract", "", 1, 1, vbTextCompare)
    ElseIf sheetType = "Measurement" Then
        partName = Replace(partName, "Measurement of", "", 1, 1, vbTextCompare)
        partName = Replace(partName, "Measurement", "", 1, 1, vbTextCompare)
    End If
    
    ExtractPartName = Trim(partName)
End Function

' ===============================================================================
' SHEET CREATION AND MANAGEMENT
' ===============================================================================

Sub CreateNewPartPair(Optional partName As String = "", Optional silent As Boolean = False)
    '
    ' Create new Abstract-Measurement pair
    '
    
    Dim abstractWs As Worksheet
    Dim measurementWs As Worksheet
    Dim finalPartName As String
    
    On Error GoTo ErrorHandler
    
    ' Get part name from user if not provided
    If partName = "" Then
        partName = InputBox("Enter name for new part/floor:", "New Part", GetNextPartName())
        If partName = "" Then Exit Sub
    End If
    
    ' Validate part name
    If Not ValidatePartName(partName) Then
        MsgBox "Invalid part name. Please use only letters, numbers, and spaces.", _
               vbExclamation, "Invalid Name"
        Exit Sub
    End If
    
    finalPartName = Trim(partName)
    
    Application.ScreenUpdating = False
    g_IsUpdating = True
    
    ' Create Abstract sheet
    Set abstractWs = ThisWorkbook.Worksheets.Add
    abstractWs.Name = ABSTRACT_PREFIX & " " & finalPartName
    Call SetupAbstractSheet(abstractWs, finalPartName)
    
    ' Create Measurement sheet
    Set measurementWs = ThisWorkbook.Worksheets.Add
    measurementWs.Name = MEASUREMENT_PREFIX & " " & finalPartName
    Call SetupMeasurementSheet(measurementWs, finalPartName)
    
    ' Create named ranges
    Call CreateNamedRangesForPart(finalPartName)
    
    ' Link to General Abstract
    Call LinkPartToGeneral(finalPartName)
    
    ' Setup formulas
    Call SetupPartFormulas(finalPartName)
    
    ' Protect sheets
    Call ProtectSheet(abstractWs)
    Call ProtectSheet(measurementWs)
    
    g_IsUpdating = False
    Application.ScreenUpdating = True
    
    If Not silent Then
        MsgBox "New part '" & finalPartName & "' created successfully!", _
               vbInformation, "Part Created"
    End If
    
    Exit Sub
    
ErrorHandler:
    g_IsUpdating = False
    Application.ScreenUpdating = True
    Call HandleError("CreateNewPartPair", Err.Description)
End Sub

Function GetNextPartName() As String
    '
    ' Generate next sequential part name
    '
    
    Dim partCount As Integer
    Dim partLetter As String
    
    partCount = CountPartPairs()
    
    If partCount = 0 Then
        GetNextPartName = "Ground Floor"
    ElseIf partCount = 1 Then
        GetNextPartName = "First Floor"
    ElseIf partCount = 2 Then
        GetNextPartName = "Second Floor"
    Else
        partLetter = Chr(65 + partCount - 3) ' Start from 'A' after standard floors
        GetNextPartName = "Part " & partLetter
    End If
End Function

Sub DeleteSelectedPart()
    '
    ' Delete selected part pair with confirmation
    '
    
    Dim partName As String
    Dim abstractSheet As String
    Dim measurementSheet As String
    Dim response As VbMsgBoxResult
    Dim hasData As Boolean
    
    On Error GoTo ErrorHandler
    
    ' Get part name from user
    partName = GetPartNameFromUser("delete")
    If partName = "" Then Exit Sub
    
    abstractSheet = ABSTRACT_PREFIX & " " & partName
    measurementSheet = MEASUREMENT_PREFIX & " " & partName
    
    ' Check if part has data
    hasData = PartHasData(partName)
    
    ' Confirm deletion
    If hasData Then
        response = MsgBox("Part '" & partName & "' contains data." & vbCrLf & _
                         "Are you sure you want to delete it?", _
                         vbYesNo + vbExclamation, "Confirm Deletion")
    Else
        response = MsgBox("Delete part '" & partName & "'?", _
                         vbYesNo + vbQuestion, "Confirm Deletion")
    End If
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    g_IsUpdating = True
    
    ' Remove from General Abstract first
    Call RemovePartFromGeneral(partName)
    
    ' Delete sheets
    If SheetExists(abstractSheet) Then
        ThisWorkbook.Worksheets(abstractSheet).Delete
    End If
    
    If SheetExists(measurementSheet) Then
        ThisWorkbook.Worksheets(measurementSheet).Delete
    End If
    
    ' Clean up named ranges
    Call CleanupNamedRangesForPart(partName)
    
    g_IsUpdating = False
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "Part '" & partName & "' deleted successfully!", _
           vbInformation, "Part Deleted"
    
    Exit Sub
    
ErrorHandler:
    g_IsUpdating = False
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    Call HandleError("DeleteSelectedPart", Err.Description)
End Sub

Function PartHasData(partName As String) As Boolean
    '
    ' Check if part contains data
    '
    
    Dim abstractWs As Worksheet
    Dim measurementWs As Worksheet
    Dim hasData As Boolean
    
    hasData = False
    
    ' Check Abstract sheet
    If SheetExists(ABSTRACT_PREFIX & " " & partName) Then
        Set abstractWs = ThisWorkbook.Worksheets(ABSTRACT_PREFIX & " " & partName)
        If abstractWs.Range("B6:B100").Count > 0 Then hasData = True
    End If
    
    ' Check Measurement sheet
    If SheetExists(MEASUREMENT_PREFIX & " " & partName) Then
        Set measurementWs = ThisWorkbook.Worksheets(MEASUREMENT_PREFIX & " " & partName)
        If measurementWs.Range("B6:B100").Count > 0 Then hasData = True
    End If
    
    PartHasData = hasData
End Function

' ===============================================================================
' ITEM MANAGEMENT
' ===============================================================================

Sub AddNewItem()
    '
    ' Add new item to selected sheet
    '
    
    Dim ws As Worksheet
    Dim sheetType As String
    Dim newRow As Long
    Dim itemData As ItemData
    
    On Error GoTo ErrorHandler
    
    Set ws = ActiveSheet
    sheetType = GetSheetType(ws.Name)
    
    If sheetType = "Unknown" Then
        MsgBox "Please select an Abstract or Measurement sheet to add items.", _
               vbExclamation, "Invalid Sheet"
        Exit Sub
    End If
    
    ' Get item details from user
    If Not GetItemDataFromUser(itemData, sheetType) Then Exit Sub
    
    Application.ScreenUpdating = False
    g_IsUpdating = True
    
    ' Find insertion point
    newRow = FindNextEmptyRow(ws)
    
    ' Insert new row
    ws.Rows(newRow).Insert Shift:=xlDown
    
    ' Add item data
    Call InsertItemData(ws, newRow, itemData, sheetType)
    
    ' Update formulas
    Call UpdateSheetFormulas(ws)
    
    g_IsUpdating = False
    Application.ScreenUpdating = True
    
    MsgBox "New item added successfully!", vbInformation, "Item Added"
    
    Exit Sub
    
ErrorHandler:
    g_IsUpdating = False
    Application.ScreenUpdating = True
    Call HandleError("AddNewItem", Err.Description)
End Sub

Sub DeleteSelectedItem()
    '
    ' Delete selected item with confirmation
    '
    
    Dim ws As Worksheet
    Dim selectedRow As Long
    Dim response As VbMsgBoxResult
    
    On Error GoTo ErrorHandler
    
    Set ws = ActiveSheet
    selectedRow = ActiveCell.Row
    
    ' Validate selection
    If selectedRow <= 5 Or ws.Cells(selectedRow, 2).Value = "" Then
        MsgBox "Please select a data row to delete.", vbExclamation, "Invalid Selection"
        Exit Sub
    End If
    
    ' Confirm deletion
    response = MsgBox("Delete item: " & ws.Cells(selectedRow, 2).Value & "?", _
                     vbYesNo + vbQuestion, "Confirm Deletion")
    
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    g_IsUpdating = True
    
    ' Delete row
    ws.Rows(selectedRow).Delete Shift:=xlUp
    
    ' Update formulas and numbering
    Call UpdateSheetFormulas(ws)
    Call RenumberItems(ws)
    
    g_IsUpdating = False
    Application.ScreenUpdating = True
    
    MsgBox "Item deleted successfully!", vbInformation, "Item Deleted"
    
    Exit Sub
    
ErrorHandler:
    g_IsUpdating = False
    Application.ScreenUpdating = True
    Call HandleError("DeleteSelectedItem", Err.Description)
End Sub

' ===============================================================================
' FORMULA AND LINKAGE SYSTEM
' ===============================================================================

Sub RebuildAllFormulas()
    '
    ' Rebuild all formulas and linkages
    '
    
    Dim ws As Worksheet
    Dim partName As String
    
    On Error GoTo ErrorHandler
    
    Application.Calculation = xlCalculationManual
    g_IsUpdating = True
    
    ' Update all measurement to abstract linkages
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            partName = ExtractPartName(ws.Name, "Measurement")
            Call LinkMeasurementToAbstract(partName)
        End If
    Next ws
    
    ' Update all abstract to general linkages
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            partName = ExtractPartName(ws.Name, "Abstract")
            Call LinkAbstractToGeneral(partName)
        End If
    Next ws
    
    ' Update General Abstract formulas
    Call UpdateGeneralAbstractFormulas
    
    g_IsUpdating = False
    Application.Calculation = xlCalculationAutomatic
    Application.Calculate
    
    Exit Sub
    
ErrorHandler:
    g_IsUpdating = False
    Application.Calculation = xlCalculationAutomatic
    Call HandleError("RebuildAllFormulas", Err.Description)
End Sub

Sub LinkMeasurementToAbstract(partName As String)
    '
    ' Link measurement totals to abstract quantities
    '
    
    Dim measurementWs As Worksheet
    Dim abstractWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    
    On Error Resume Next
    
    Set measurementWs = ThisWorkbook.Worksheets(MEASUREMENT_PREFIX & " " & partName)
    Set abstractWs = ThisWorkbook.Worksheets(ABSTRACT_PREFIX & " " & partName)
    
    If measurementWs Is Nothing Or abstractWs Is Nothing Then Exit Sub
    
    lastRow = measurementWs.Cells(measurementWs.Rows.Count, 2).End(xlUp).Row
    
    ' Link quantities (assuming data starts from row 6)
    For i = 6 To lastRow
        If measurementWs.Cells(i, 2).Value <> "" Then
            ' Link quantity from measurement total to abstract
            abstractWs.Cells(i, 4).Formula = _
                "=IF('" & measurementWs.Name & "'!" & measurementWs.Cells(i, 8).Address & _
                "<>0,'" & measurementWs.Name & "'!" & measurementWs.Cells(i, 8).Address & ","""")"
        End If
    Next i
End Sub

Sub LinkAbstractToGeneral(partName As String)
    '
    ' Link abstract totals to General Abstract
    '
    
    Dim abstractWs As Worksheet
    Dim generalWs As Worksheet
    Dim targetRow As Long
    
    On Error Resume Next
    
    Set abstractWs = ThisWorkbook.Worksheets(ABSTRACT_PREFIX & " " & partName)
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT)
    
    If abstractWs Is Nothing Or generalWs Is Nothing Then Exit Sub
    
    ' Find or create row in General Abstract
    targetRow = FindOrCreateGeneralRow(partName)
    
    ' Link total amount using SUMIF to handle dynamic ranges
    generalWs.Cells(targetRow, 3).Formula = _
        "=SUMIF('" & abstractWs.Name & "'!D:D,"">0"",'" & abstractWs.Name & "'!F:F)"
End Sub

' ===============================================================================
' EXPORT SYSTEM
' ===============================================================================

Sub ExportToPDF()
    '
    ' Export complete estimate to PDF
    '
    
    Dim filePath As String
    Dim projectName As String
    
    On Error GoTo ErrorHandler
    
    ' Get project details
    projectName = InputBox("Enter project name:", "Project Name", g_ProjectName)
    If projectName = "" Then Exit Sub
    
    g_ProjectName = projectName
    
    ' Get save location
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=projectName & "_Estimate.pdf", _
        FileFilter:="PDF Files (*.pdf), *.pdf", _
        Title:="Export Estimate to PDF")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    
    ' Prepare sheets for PDF export
    Call PrepareForPDFExport(projectName)
    
    ' Export to PDF
    Call ExportSheetsToPDF(filePath)
    
    ' Restore original formatting
    Call RestoreAfterPDFExport
    
    ' Log export
    Call LogExport("PDF", filePath)
    
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to PDF successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Call HandleError("ExportToPDF", Err.Description)
End Sub

Sub ExportMultiFormat()
    '
    ' Export estimate in multiple formats with dropdown selection
    '
    
    Dim exportType As String
    Dim formats As Variant
    Dim selection As Integer
    
    On Error GoTo ErrorHandler
    
    formats = Array("PDF", "Excel (.xlsx)", "CSV Package", "HTML Report")
    
    ' Show format selection
    selection = Application.InputBox( _
        "Select export format:" & vbCrLf & vbCrLf & _
        "1 - PDF (Complete Report)" & vbCrLf & _
        "2 - Excel (.xlsx Clean Copy)" & vbCrLf & _
        "3 - CSV Package (All Sheets)" & vbCrLf & _
        "4 - HTML Report (Printable)", _
        "Export Format Selection", 1, Type:=1)
    
    If selection < 1 Or selection > 4 Then Exit Sub
    
    Select Case selection
        Case 1
            Call ExportToPDF
        Case 2
            Call ExportToExcel
        Case 3
            Call ExportToCSVPackage
        Case 4
            Call ExportToHTML
    End Select
    
    Exit Sub
    
ErrorHandler:
    Call HandleError("ExportMultiFormat", Err.Description)
End Sub

' ===============================================================================
' USER INTERFACE HELPERS
' ===============================================================================

Type ItemData
    Description As String
    Unit As String
    Quantity As Double
    Length As Double
    Breadth As Double
    Height As Double
    Rate As Double
End Type

Function GetItemDataFromUser(ByRef itemData As ItemData, sheetType As String) As Boolean
    '
    ' Get item data from user input
    '
    
    ' Description
    itemData.Description = InputBox("Enter item description:", "New Item")
    If itemData.Description = "" Then
        GetItemDataFromUser = False
        Exit Function
    End If
    
    ' Unit
    itemData.Unit = InputBox("Enter unit (Cum, Sqm, Nos, etc.):", "Unit", "Cum")
    If itemData.Unit = "" Then itemData.Unit = "Nos"
    
    If sheetType = "Abstract" Then
        ' Rate for Abstract sheets
        itemData.Rate = Val(InputBox("Enter rate per unit:", "Rate", "0"))
        itemData.Quantity = 0 ' Will be linked from measurement
    Else
        ' Measurements for Measurement sheets
        itemData.Quantity = Val(InputBox("Enter quantity/nos:", "Quantity", "1"))
        itemData.Length = Val(InputBox("Enter length (if applicable):", "Length", "1"))
        itemData.Breadth = Val(InputBox("Enter breadth (if applicable):", "Breadth", "1"))
        itemData.Height = Val(InputBox("Enter height (if applicable):", "Height", "1"))
    End If
    
    GetItemDataFromUser = True
End Function

Function GetPartNameFromUser(action As String) As String
    '
    ' Get part name from user with list of available parts
    '
    
    Dim ws As Worksheet
    Dim partsList As String
    Dim partName As String
    
    ' Build list of existing parts
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            partName = ExtractPartName(ws.Name, "Abstract")
            partsList = partsList & partName & vbCrLf
        End If
    Next ws
    
    If partsList = "" Then
        MsgBox "No parts found to " & action & ".", vbInformation
        GetPartNameFromUser = ""
        Exit Function
    End If
    
    GetPartNameFromUser = InputBox( _
        "Enter part name to " & action & ":" & vbCrLf & vbCrLf & _
        "Available parts:" & vbCrLf & partsList, _
        UCase(Left(action, 1)) & Mid(action, 2) & " Part")
End Function

' ===============================================================================
' UTILITY FUNCTIONS
' ===============================================================================

Function ValidatePartName(partName As String) As Boolean
    '
    ' Validate part name for special characters and duplicates
    '
    
    Dim invalidChars As String
    Dim i As Integer
    
    invalidChars = "\/:*?""<>|[]"
    
    ' Check length
    If Len(partName) = 0 Or Len(partName) > 50 Then
        ValidatePartName = False
        Exit Function
    End If
    
    ' Check for invalid characters
    For i = 1 To Len(invalidChars)
        If InStr(partName, Mid(invalidChars, i, 1)) > 0 Then
            ValidatePartName = False
            Exit Function
        End If
    Next i
    
    ' Check for duplicates
    If SheetExists(ABSTRACT_PREFIX & " " & partName) Then
        ValidatePartName = False
        Exit Function
    End If
    
    ValidatePartName = True
End Function

Sub HandleError(source As String, description As String)
    '
    ' Centralized error handling
    '
    
    Dim errorMsg As String
    
    errorMsg = "Error in " & source & ":" & vbCrLf & vbCrLf & _
               description & vbCrLf & vbCrLf & _
               "Please try again or use 'Rebuild Formulas' if the problem persists."
    
    MsgBox errorMsg, vbCritical, "System Error"
    
    ' Log error for debugging
    Call LogError(source, description)
End Sub

Sub ShowWelcomeMessage()
    '
    ' Show welcome message with system information
    '
    
    Dim msg As String
    
    msg = "🏗️ CONSTRUCTION ESTIMATION SYSTEM" & vbCrLf & vbCrLf & _
          "System initialized successfully!" & vbCrLf & vbCrLf & _
          "Available Functions:" & vbCrLf & _
          "• Import Sample Estimate (Ctrl+Shift+I)" & vbCrLf & _
          "• Add New Item (Ctrl+Shift+A)" & vbCrLf & _
          "• Add New Part (Ctrl+Shift+P)" & vbCrLf & _
          "• Export to PDF (Ctrl+Shift+E)" & vbCrLf & vbCrLf & _
          "Use the Construction Estimation ribbon tab for all functions."
    
    MsgBox msg, vbInformation, "Welcome to Construction Estimation System"
End Sub

Sub SetupKeyboardShortcuts()
    '
    ' Setup keyboard shortcuts
    '
    
    Application.OnKey "^+I", "ImportSampleEstimate"
    Application.OnKey "^+A", "AddNewItem"
    Application.OnKey "^+P", "CreateNewPartPair"
    Application.OnKey "^+D", "DeleteSelectedItem"
    Application.OnKey "^+E", "ExportToPDF"
    Application.OnKey "^+M", "ExportMultiFormat"
    Application.OnKey "^+R", "RebuildAllFormulas"
End Sub