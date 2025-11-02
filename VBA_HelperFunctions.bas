' ===============================================================================
' HELPER FUNCTIONS MODULE
' ===============================================================================
' File: VBA_HelperFunctions.bas
' Purpose: Utility functions and helper procedures
' ===============================================================================

Option Explicit

' ===============================================================================
' RIBBON CALLBACK FUNCTIONS
' ===============================================================================

Sub OnRibbonLoad(ribbon As IRibbonUI)
    '
    ' Callback when ribbon loads
    '
    Set ribbonUI = ribbon
End Sub

Dim ribbonUI As IRibbonUI

' ===============================================================================
' SHEET STRUCTURE FUNCTIONS
' ===============================================================================

Function FindOrCreatePartRowInGeneral(partName As String) As Long
    '
    ' Find existing part row in General Abstract or create new one
    '
    
    Dim generalWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim foundRow As Long
    
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    lastRow = generalWs.Cells(generalWs.Rows.Count, 2).End(xlUp).Row
    
    ' Search for existing part
    foundRow = 0
    For i = 4 To lastRow ' Assuming data starts from row 4
        If InStr(1, generalWs.Cells(i, 2).Value, partName, vbTextCompare) > 0 Then
            foundRow = i
            Exit For
        End If
    Next i
    
    ' Create new row if not found
    If foundRow = 0 Then
        foundRow = lastRow + 1
        generalWs.Cells(foundRow, 1).Value = foundRow - 3 ' Serial number
        generalWs.Cells(foundRow, 2).Value = partName
        generalWs.Cells(foundRow, 3).Value = 0 ' Initial amount
    End If
    
    FindOrCreatePartRowInGeneral = foundRow
End Function

Sub RemovePartFromGeneralAbstract(partName As String)
    '
    ' Remove part row from General Abstract
    '
    
    Dim generalWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    lastRow = generalWs.Cells(generalWs.Rows.Count, 2).End(xlUp).Row
    
    ' Find and delete part row
    For i = 4 To lastRow
        If InStr(1, generalWs.Cells(i, 2).Value, partName, vbTextCompare) > 0 Then
            generalWs.Rows(i).Delete
            Exit For
        End If
    Next i
    
    ' Renumber remaining rows
    Call RenumberGeneralAbstract
End Sub

Sub RenumberGeneralAbstract()
    '
    ' Renumber serial numbers in General Abstract
    '
    
    Dim generalWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim counter As Long
    
    Set generalWs = ThisWorkbook.Worksheets(GENERAL_ABSTRACT_SHEET)
    lastRow = generalWs.Cells(generalWs.Rows.Count, 2).End(xlUp).Row
    
    counter = 1
    For i = 4 To lastRow
        If generalWs.Cells(i, 2).Value <> "" Then
            generalWs.Cells(i, 1).Value = counter
            counter = counter + 1
        End If
    Next i
End Sub

' ===============================================================================
' FORMULA MANAGEMENT FUNCTIONS
' ===============================================================================

Sub UpdateSheetFormulas(ws As Worksheet)
    '
    ' Update formulas in a specific sheet
    '
    
    Dim lastRow As Long
    Dim i As Long
    
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    
    If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
        ' Update Abstract sheet formulas
        For i = 6 To lastRow
            If ws.Cells(i, 1).Value <> "" Then
                ws.Cells(i, 6).Formula = "=D" & i & "*E" & i ' Amount = Quantity * Rate
            End If
        Next i
    ElseIf InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
        ' Update Measurement sheet formulas
        For i = 6 To lastRow
            If ws.Cells(i, 1).Value <> "" Then
                ws.Cells(i, 8).Formula = "=D" & i & "*E" & i & "*F" & i & "*G" & i ' Total = Nos*L*B*H
            End If
        Next i
    End If
    
    ' Recalculate
    ws.Calculate
End Sub

Sub SetupNamedRanges()
    '
    ' Setup named ranges for formula references
    '
    
    Dim ws As Worksheet
    Dim rangeName As String
    
    ' Create named ranges for each sheet's data area
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 Or _
           InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            
            rangeName = Replace(ws.Name, " ", "_") & "_Data"
            
            ' Delete existing named range if exists
            On Error Resume Next
            ThisWorkbook.Names(rangeName).Delete
            On Error GoTo 0
            
            ' Create new named range
            ThisWorkbook.Names.Add Name:=rangeName, _
                                  RefersTo:=ws.Range("A6:Z1000")
        End If
    Next ws
End Sub

' ===============================================================================
' DATA VALIDATION FUNCTIONS
' ===============================================================================

Function ValidatePartName(partName As String) As Boolean
    '
    ' Validate part name for special characters and length
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
    
    ValidatePartName = True
End Function

Function ValidateSheetName(sheetName As String) As Boolean
    '
    ' Validate sheet name before creation
    '
    
    Dim ws As Worksheet
    
    ' Check if name already exists
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(sheetName)
    On Error GoTo 0
    
    If Not ws Is Nothing Then
        ValidateSheetName = False
        Exit Function
    End If
    
    ' Check name validity
    ValidateSheetName = ValidatePartName(sheetName)
End Function

' ===============================================================================
' USER INTERFACE FUNCTIONS
' ===============================================================================

Sub ShowUserGuide()
    '
    ' Display user guide information
    '
    
    Dim guideText As String
    
    guideText = "CONSTRUCTION ESTIMATION SYSTEM - QUICK GUIDE" & vbCrLf & vbCrLf & _
                "MAIN FUNCTIONS:" & vbCrLf & _
                "• Import Sample Estimate: Load existing Excel files" & vbCrLf & _
                "• Add New Item: Insert items in Abstract/Measurement sheets" & vbCrLf & _
                "• Add New Part: Create new part with paired sheets" & vbCrLf & _
                "• Export Functions: Generate PDF, Excel, CSV, HTML reports" & vbCrLf & vbCrLf & _
                "KEYBOARD SHORTCUTS:" & vbCrLf & _
                "• Alt+F1: Import Sample" & vbCrLf & _
                "• Alt+F2: Add Item" & vbCrLf & _
                "• Alt+F4: Add Part" & vbCrLf & _
                "• Alt+F6: Export PDF" & vbCrLf & vbCrLf & _
                "SHEET STRUCTURE:" & vbCrLf & _
                "• General Abstract: Master summary" & vbCrLf & _
                "• Abstract of Cost [Part]: Detailed costs per part" & vbCrLf & _
                "• Measurement [Part]: Quantity calculations" & vbCrLf & vbCrLf & _
                "For detailed instructions, see the User Guide document."
    
    MsgBox guideText, vbInformation, "User Guide"
End Sub

Sub ShowAboutDialog()
    '
    ' Show about dialog
    '
    
    Dim aboutText As String
    
    aboutText = "CONSTRUCTION ESTIMATION SYSTEM" & vbCrLf & vbCrLf & _
                "Version: 2.0" & vbCrLf & _
                "Date: November 2025" & vbCrLf & _
                "Platform: Microsoft Excel 2016+" & vbCrLf & vbCrLf & _
                "FEATURES:" & vbCrLf & _
                "✓ Dynamic Excel import with auto-mapping" & vbCrLf & _
                "✓ Real-time formula linkages" & vbCrLf & _
                "✓ Interactive user interface" & vbCrLf & _
                "✓ Multi-format export (PDF, Excel, CSV, HTML)" & vbCrLf & _
                "✓ Data validation and protection" & vbCrLf & _
                "✓ Automatic calculations and updates" & vbCrLf & vbCrLf & _
                "SYSTEM REQUIREMENTS:" & vbCrLf & _
                "• Microsoft Excel 2016 or later" & vbCrLf & _
                "• Macro support enabled" & vbCrLf & _
                "• Windows operating system" & vbCrLf & vbCrLf & _
                "© 2025 Construction Estimation System"
    
    MsgBox aboutText, vbInformation, "About Construction Estimation System"
End Sub

' ===============================================================================
' ERROR HANDLING FUNCTIONS
' ===============================================================================

Sub HandleError(errorSource As String, errorDescription As String)
    '
    ' Centralized error handling
    '
    
    Dim errorMsg As String
    
    errorMsg = "An error occurred in: " & errorSource & vbCrLf & vbCrLf & _
               "Error Description: " & errorDescription & vbCrLf & vbCrLf & _
               "Please try the operation again. If the error persists, " & _
               "use 'Rebuild Formulas' from the Utilities group."
    
    MsgBox errorMsg, vbCritical, "System Error"
    
    ' Log error (optional)
    Call LogError(errorSource, errorDescription)
End Sub

Sub LogError(source As String, description As String)
    '
    ' Log errors to hidden sheet for debugging
    '
    
    Dim logWs As Worksheet
    Dim lastRow As Long
    
    On Error Resume Next
    Set logWs = ThisWorkbook.Worksheets("Error_Log")
    On Error GoTo 0
    
    If logWs Is Nothing Then
        Set logWs = ThisWorkbook.Worksheets.Add
        logWs.Name = "Error_Log"
        logWs.Visible = xlSheetVeryHidden
        
        ' Setup headers
        logWs.Range("A1").Value = "Timestamp"
        logWs.Range("B1").Value = "Source"
        logWs.Range("C1").Value = "Description"
        logWs.Range("A1:C1").Font.Bold = True
    End If
    
    lastRow = logWs.Cells(logWs.Rows.Count, 1).End(xlUp).Row + 1
    logWs.Cells(lastRow, 1).Value = Now
    logWs.Cells(lastRow, 2).Value = source
    logWs.Cells(lastRow, 3).Value = description
End Sub

' ===============================================================================
' CLEANUP FUNCTIONS
' ===============================================================================

Sub ClearExistingSheets()
    '
    ' Clear existing sheets except General Abstract
    '
    
    Dim ws As Worksheet
    Dim sheetsToDelete As Collection
    Dim i As Integer
    
    Set sheetsToDelete = New Collection
    
    ' Collect sheets to delete
    For Each ws In ThisWorkbook.Worksheets
        If ws.Name <> GENERAL_ABSTRACT_SHEET Then
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
                     vbYesNo + vbCritical, "Reset System")
    
    If response = vbYes Then
        Call ClearExistingSheets
        Call SetupInitialStructure
        MsgBox "System reset complete!", vbInformation, "Reset Complete"
    End If
End Sub

' ===============================================================================
' PERFORMANCE OPTIMIZATION
' ===============================================================================

Sub OptimizePerformance(enable As Boolean)
    '
    ' Enable/disable performance optimizations
    '
    
    If enable Then
        Application.ScreenUpdating = False
        Application.Calculation = xlCalculationManual
        Application.EnableEvents = False
        Application.DisplayAlerts = False
    Else
        Application.ScreenUpdating = True
        Application.Calculation = xlCalculationAutomatic
        Application.EnableEvents = True
        Application.DisplayAlerts = True
    End If
End Sub

' ===============================================================================
' BACKUP AND RECOVERY
' ===============================================================================

Sub CreateBackup()
    '
    ' Create backup of current workbook
    '
    
    Dim backupPath As String
    Dim timestamp As String
    
    timestamp = Format(Now, "yyyymmdd_hhmmss")
    backupPath = ThisWorkbook.Path & "\Backup_" & timestamp & ".xlsm"
    
    ThisWorkbook.SaveCopyAs backupPath
    
    MsgBox "Backup created: " & backupPath, vbInformation, "Backup Complete"
End Sub