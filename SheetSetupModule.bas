' ===============================================================================
' SHEET SETUP MODULE
' ===============================================================================
' File: SheetSetupModule.bas
' Purpose: Sheet creation, formatting, and structure setup
' ===============================================================================

Option Explicit

' ===============================================================================
' GENERAL ABSTRACT SHEET SETUP
' ===============================================================================

Sub CreateGeneralAbstractSheet()
    '
    ' Create and setup General Abstract sheet
    '
    
    Dim ws As Worksheet
    
    Set ws = ThisWorkbook.Worksheets.Add
    ws.Name = GENERAL_ABSTRACT
    
    Call SetupGeneralAbstractStructure(ws)
    Call FormatGeneralAbstractSheet(ws)
    Call ProtectSheet(ws)
End Sub

Sub SetupGeneralAbstractStructure(ws As Worksheet)
    '
    ' Setup General Abstract sheet structure and formulas
    '
    
    With ws
        ' Header
        .Range("A1").Value = "GENERAL ABSTRACT OF COST"
        .Range("A2").Value = "PROJECT: " & g_ProjectName
        .Range("A3").Value = "DATE: " & Format(Date, "dd-mmm-yyyy")
        
        ' Column headers
        .Range("A5").Value = "S.No."
        .Range("B5").Value = "Description of Work"
        .Range("C5").Value = "Amount (₹)"
        .Range("D5").Value = "Percentage"
        
        ' Initial structure rows
        .Range("A6").Value = 1
        .Range("B6").Value = "Civil Work"
        .Range("C6").Value = 0
        
        ' Subtotal row
        .Range("A20").Value = ""
        .Range("B20").Value = "SUB TOTAL"
        .Range("C20").Formula = "=SUM(C6:C19)"
        
        ' Additional charges
        .Range("A21").Value = ""
        .Range("B21").Value = "Add 7% for Electrification on Civil Work"
        .Range("C21").Formula = "=C6*0.07"
        
        .Range("A22").Value = ""
        .Range("B22").Value = "Total after Electrification"
        .Range("C22").Formula = "=C20+C21"
        
        .Range("A23").Value = ""
        .Range("B23").Value = "Add Prorata Charges @ 13%"
        .Range("C23").Formula = "=C22*0.13"
        
        .Range("A25").Value = ""
        .Range("B25").Value = "GRAND TOTAL"
        .Range("C25").Formula = "=C22+C23"
        
        ' Percentage calculations
        .Range("D6:D19").Formula = "=IF(C6<>0,C6/$C$25*100,"""")"
    End With
End Sub

Sub FormatGeneralAbstractSheet(ws As Worksheet)
    '
    ' Format General Abstract sheet
    '
    
    With ws
        ' Header formatting
        .Range("A1").Font.Size = 16
        .Range("A1").Font.Bold = True
        .Range("A1:D1").Merge
        .Range("A1").HorizontalAlignment = xlCenter
        
        .Range("A2:A3").Font.Size = 12
        .Range("A2:A3").Font.Bold = True
        
        ' Column headers
        .Range("A5:D5").Font.Bold = True
        .Range("A5:D5").Borders.LineStyle = xlContinuous
        .Range("A5:D5").Interior.Color = RGB(220, 230, 241)
        
        ' Column widths
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 45
        .Columns("C").ColumnWidth = 15
        .Columns("D").ColumnWidth = 12
        
        ' Number formatting
        .Range("C:C").NumberFormat = "#,##0.00"
        .Range("D:D").NumberFormat = "0.00%"
        
        ' Total rows formatting
        .Range("B20,B22,B25").Font.Bold = True
        .Range("C20,C22,C25").Font.Bold = True
        .Range("B25:C25").Font.Size = 12
        .Range("B25:C25").Interior.Color = RGB(255, 242, 204)
        
        ' Borders for data area
        .Range("A5:D25").Borders.LineStyle = xlContinuous
    End With
End Sub

' ===============================================================================
' ABSTRACT SHEET SETUP
' ===============================================================================

Sub SetupAbstractSheet(ws As Worksheet, partName As String)
    '
    ' Setup Abstract of Cost sheet structure
    '
    
    Call SetupAbstractStructure(ws, partName)
    Call FormatAbstractSheet(ws)
End Sub

Sub SetupAbstractStructure(ws As Worksheet, partName As String)
    '
    ' Setup Abstract sheet structure and formulas
    '
    
    With ws
        ' Header
        .Range("A1").Value = "ABSTRACT OF COST - " & UCase(partName)
        .Range("A2").Value = "PROJECT: " & g_ProjectName
        .Range("A3").Value = "DATE: " & Format(Date, "dd-mmm-yyyy")
        
        ' Column headers
        .Range("A5").Value = "S.No."
        .Range("B5").Value = "Description of Work"
        .Range("C5").Value = "Unit"
        .Range("D5").Value = "Quantity"
        .Range("E5").Value = "Rate (₹)"
        .Range("F5").Value = "Amount (₹)"
        
        ' Sample row with formulas
        .Range("A6").Value = 1
        .Range("B6").Value = "Sample Item (Replace with actual work)"
        .Range("C6").Value = "Cum"
        .Range("D6").Value = 0
        .Range("E6").Value = 0
        .Range("F6").Formula = "=IF(AND(D6<>0,E6<>0),D6*E6,"""")"
        
        ' Total row
        .Range("A50").Value = ""
        .Range("B50").Value = "TOTAL " & UCase(partName)
        .Range("C50").Value = ""
        .Range("D50").Value = ""
        .Range("E50").Value = ""
        .Range("F50").Formula = "=SUM(F6:F49)"
    End With
End Sub

Sub FormatAbstractSheet(ws As Worksheet)
    '
    ' Format Abstract sheet
    '
    
    With ws
        ' Header formatting
        .Range("A1").Font.Size = 14
        .Range("A1").Font.Bold = True
        .Range("A1:F1").Merge
        .Range("A1").HorizontalAlignment = xlCenter
        
        .Range("A2:A3").Font.Size = 10
        .Range("A2:A3").Font.Bold = True
        
        ' Column headers
        .Range("A5:F5").Font.Bold = True
        .Range("A5:F5").Borders.LineStyle = xlContinuous
        .Range("A5:F5").Interior.Color = RGB(220, 230, 241)
        
        ' Column widths
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 40
        .Columns("C").ColumnWidth = 8
        .Columns("D").ColumnWidth = 12
        .Columns("E").ColumnWidth = 12
        .Columns("F").ColumnWidth = 15
        
        ' Number formatting
        .Range("D:F").NumberFormat = "#,##0.00"
        
        ' Total row formatting
        .Range("B50:F50").Font.Bold = True
        .Range("B50:F50").Interior.Color = RGB(255, 242, 204)
        
        ' Data area borders
        .Range("A5:F50").Borders.LineStyle = xlContinuous
    End With
End Sub

' ===============================================================================
' MEASUREMENT SHEET SETUP
' ===============================================================================

Sub SetupMeasurementSheet(ws As Worksheet, partName As String)
    '
    ' Setup Measurement sheet structure
    '
    
    Call SetupMeasurementStructure(ws, partName)
    Call FormatMeasurementSheet(ws)
End Sub

Sub SetupMeasurementStructure(ws As Worksheet, partName As String)
    '
    ' Setup Measurement sheet structure and formulas
    '
    
    With ws
        ' Header
        .Range("A1").Value = "MEASUREMENT SHEET - " & UCase(partName)
        .Range("A2").Value = "PROJECT: " & g_ProjectName
        .Range("A3").Value = "DATE: " & Format(Date, "dd-mmm-yyyy")
        
        ' Column headers
        .Range("A5").Value = "S.No."
        .Range("B5").Value = "Description of Work"
        .Range("C5").Value = "Unit"
        .Range("D5").Value = "Nos"
        .Range("E5").Value = "Length"
        .Range("F5").Value = "Breadth"
        .Range("G5").Value = "Height"
        .Range("H5").Value = "Total"
        
        ' Sample row with formulas
        .Range("A6").Value = 1
        .Range("B6").Value = "Sample Item (Replace with actual work)"
        .Range("C6").Value = "Cum"
        .Range("D6").Value = 1
        .Range("E6").Value = 1
        .Range("F6").Value = 1
        .Range("G6").Value = 1
        .Range("H6").Formula = "=IF(D6<>"""",D6*E6*F6*G6,"""")"
        
        ' Total row
        .Range("A50").Value = ""
        .Range("B50").Value = "TOTAL " & UCase(partName)
        .Range("C50").Value = ""
        .Range("D50").Value = ""
        .Range("E50").Value = ""
        .Range("F50").Value = ""
        .Range("G50").Value = ""
        .Range("H50").Formula = "=SUM(H6:H49)"
    End With
End Sub

Sub FormatMeasurementSheet(ws As Worksheet)
    '
    ' Format Measurement sheet
    '
    
    With ws
        ' Header formatting
        .Range("A1").Font.Size = 14
        .Range("A1").Font.Bold = True
        .Range("A1:H1").Merge
        .Range("A1").HorizontalAlignment = xlCenter
        
        .Range("A2:A3").Font.Size = 10
        .Range("A2:A3").Font.Bold = True
        
        ' Column headers
        .Range("A5:H5").Font.Bold = True
        .Range("A5:H5").Borders.LineStyle = xlContinuous
        .Range("A5:H5").Interior.Color = RGB(220, 230, 241)
        
        ' Column widths
        .Columns("A").ColumnWidth = 8
        .Columns("B").ColumnWidth = 40
        .Columns("C").ColumnWidth = 8
        .Columns("D:H").ColumnWidth = 10
        
        ' Number formatting
        .Range("D:H").NumberFormat = "#,##0.00"
        
        ' Total row formatting
        .Range("B50:H50").Font.Bold = True
        .Range("B50:H50").Interior.Color = RGB(255, 242, 204)
        
        ' Data area borders
        .Range("A5:H50").Borders.LineStyle = xlContinuous
    End With
End Sub

' ===============================================================================
' NAMED RANGES MANAGEMENT
' ===============================================================================

Sub SetupNamedRanges()
    '
    ' Setup named ranges for all sheets
    '
    
    Dim ws As Worksheet
    
    ' Setup named range for General Abstract
    If SheetExists(GENERAL_ABSTRACT) Then
        Call CreateGeneralNamedRange
    End If
    
    ' Setup named ranges for all parts
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            Call CreateNamedRangesForPart(ExtractPartName(ws.Name, "Abstract"))
        End If
    Next ws
End Sub

Sub CreateGeneralNamedRange()
    '
    ' Create named range for General Abstract data
    '
    
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(GENERAL_ABSTRACT)
    
    ' Delete existing named range if it exists
    On Error Resume Next
    ThisWorkbook.Names(NR_GENERAL_DATA).Delete
    On Error GoTo 0
    
    ' Create new named range
    ThisWorkbook.Names.Add Name:=NR_GENERAL_DATA, _
                          RefersTo:=ws.Range("A6:D25")
End Sub

Sub CreateNamedRangesForPart(partName As String)
    '
    ' Create named ranges for a specific part
    '
    
    Dim abstractWs As Worksheet
    Dim measurementWs As Worksheet
    Dim abstractRangeName As String
    Dim measurementRangeName As String
    
    abstractRangeName = NR_ABSTRACT_DATA & Replace(partName, " ", "_")
    measurementRangeName = NR_MEASUREMENT_DATA & Replace(partName, " ", "_")
    
    ' Abstract sheet named range
    If SheetExists(ABSTRACT_PREFIX & " " & partName) Then
        Set abstractWs = ThisWorkbook.Worksheets(ABSTRACT_PREFIX & " " & partName)
        
        On Error Resume Next
        ThisWorkbook.Names(abstractRangeName).Delete
        On Error GoTo 0
        
        ThisWorkbook.Names.Add Name:=abstractRangeName, _
                              RefersTo:=abstractWs.Range("A6:F50")
    End If
    
    ' Measurement sheet named range
    If SheetExists(MEASUREMENT_PREFIX & " " & partName) Then
        Set measurementWs = ThisWorkbook.Worksheets(MEASUREMENT_PREFIX & " " & partName)
        
        On Error Resume Next
        ThisWorkbook.Names(measurementRangeName).Delete
        On Error GoTo 0
        
        ThisWorkbook.Names.Add Name:=measurementRangeName, _
                              RefersTo:=measurementWs.Range("A6:H50")
    End If
End Sub

Sub CleanupNamedRangesForPart(partName As String)
    '
    ' Clean up named ranges for deleted part
    '
    
    Dim abstractRangeName As String
    Dim measurementRangeName As String
    
    abstractRangeName = NR_ABSTRACT_DATA & Replace(partName, " ", "_")
    measurementRangeName = NR_MEASUREMENT_DATA & Replace(partName, " ", "_")
    
    On Error Resume Next
    ThisWorkbook.Names(abstractRangeName).Delete
    ThisWorkbook.Names(measurementRangeName).Delete
    On Error GoTo 0
End Sub

' ===============================================================================
' SHEET PROTECTION
' ===============================================================================

Sub ProtectSheet(ws As Worksheet)
    '
    ' Protect sheet with appropriate settings
    '
    
    Dim sheetType As String
    
    ws.Unprotect
    
    ' Unlock all cells first
    ws.Cells.Locked = False
    
    sheetType = GetSheetType(ws.Name)
    
    Select Case sheetType
        Case "General"
            ' Lock everything except description column
            ws.Cells.Locked = True
            ws.Range("B6:B19").Locked = False
            
        Case "Abstract"
            ' Lock formulas, unlock data entry cells
            ws.Cells.Locked = True
            ws.Range("B6:C49,E6:E49").Locked = False ' Description, Unit, Rate
            
        Case "Measurement"
            ' Lock formulas, unlock measurement cells
            ws.Cells.Locked = True
            ws.Range("B6:G49").Locked = False ' Description through Height
    End Select
    
    ' Protect with password
    ws.Protect Password:="estimation2025", _
              DrawingObjects:=True, _
              Contents:=True, _
              Scenarios:=True, _
              AllowFormattingCells:=True, _
              AllowInsertingRows:=True, _
              AllowDeletingRows:=True, _
              AllowSorting:=True, _
              AllowFiltering:=True
End Sub

Sub ProtectAllSheets()
    '
    ' Protect all sheets in workbook
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        Call ProtectSheet(ws)
    Next ws
End Sub

Sub UnprotectAllSheets()
    '
    ' Unprotect all sheets for maintenance
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        ws.Unprotect Password:="estimation2025"
    Next ws
End Sub

' ===============================================================================
' UTILITY FUNCTIONS
' ===============================================================================

Function GetSheetType(sheetName As String) As String
    '
    ' Determine sheet type from name
    '
    
    If sheetName = GENERAL_ABSTRACT Then
        GetSheetType = "General"
    ElseIf InStr(1, sheetName, ABSTRACT_PREFIX, vbTextCompare) > 0 Then
        GetSheetType = "Abstract"
    ElseIf InStr(1, sheetName, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
        GetSheetType = "Measurement"
    Else
        GetSheetType = "Unknown"
    End If
End Function

Function FindNextEmptyRow(ws As Worksheet) As Long
    '
    ' Find next empty row for data insertion
    '
    
    Dim lastRow As Long
    Dim checkRow As Long
    
    ' Find last row with data in column B (description)
    lastRow = ws.Cells(ws.Rows.Count, 2).End(xlUp).Row
    
    ' Look for empty row between data rows
    For checkRow = 6 To lastRow
        If ws.Cells(checkRow, 2).Value = "" Then
            FindNextEmptyRow = checkRow
            Exit Function
        End If
    Next checkRow
    
    ' If no empty row found, use next row after last data
    If lastRow < 49 Then
        FindNextEmptyRow = lastRow + 1
    Else
        FindNextEmptyRow = 49 ' Maximum data row
    End If
End Function

Sub InsertItemData(ws As Worksheet, row As Long, itemData As ItemData, sheetType As String)
    '
    ' Insert item data into specified row
    '
    
    With ws
        .Cells(row, 1).Value = row - 5 ' Serial number
        .Cells(row, 2).Value = itemData.Description
        .Cells(row, 3).Value = itemData.Unit
        
        If sheetType = "Abstract" Then
            .Cells(row, 4).Value = itemData.Quantity
            .Cells(row, 5).Value = itemData.Rate
            .Cells(row, 6).Formula = "=IF(AND(D" & row & "<>0,E" & row & "<>0),D" & row & "*E" & row & ","""")"
        Else ' Measurement
            .Cells(row, 4).Value = itemData.Quantity
            .Cells(row, 5).Value = itemData.Length
            .Cells(row, 6).Value = itemData.Breadth
            .Cells(row, 7).Value = itemData.Height
            .Cells(row, 8).Formula = "=IF(D" & row & "<>"""",D" & row & "*E" & row & "*F" & row & "*G" & row & ","""")"
        End If
    End With
End Sub

Sub UpdateSheetFormulas(ws As Worksheet)
    '
    ' Update formulas in sheet after row insertion/deletion
    '
    
    Dim sheetType As String
    Dim lastRow As Long
    Dim i As Long
    
    sheetType = GetSheetType(ws.Name)
    lastRow = ws.Cells(ws.Rows.Count, 2).End(xlUp).Row
    
    ' Update formulas for each data row
    For i = 6 To lastRow
        If ws.Cells(i, 2).Value <> "" Then
            If sheetType = "Abstract" Then
                ws.Cells(i, 6).Formula = "=IF(AND(D" & i & "<>0,E" & i & "<>0),D" & i & "*E" & i & ","""")"
            ElseIf sheetType = "Measurement" Then
                ws.Cells(i, 8).Formula = "=IF(D" & i & "<>"""",D" & i & "*E" & i & "*F" & i & "*G" & i & ","""")"
            End If
        End If
    Next i
End Sub

Sub RenumberItems(ws As Worksheet)
    '
    ' Renumber items after deletion
    '
    
    Dim lastRow As Long
    Dim i As Long
    Dim counter As Long
    
    lastRow = ws.Cells(ws.Rows.Count, 2).End(xlUp).Row
    counter = 1
    
    For i = 6 To lastRow
        If ws.Cells(i, 2).Value <> "" Then
            ws.Cells(i, 1).Value = counter
            counter = counter + 1
        End If
    Next i
End Sub