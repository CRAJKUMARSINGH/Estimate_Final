' ===============================================================================
' EXPORT MODULE - Multi-Format Export System
' ===============================================================================
' File: ExportModule.bas
' Purpose: Comprehensive export functionality for PDF, Excel, CSV, and HTML
' ===============================================================================

Option Explicit

' ===============================================================================
' PDF EXPORT SYSTEM
' ===============================================================================

Sub PrepareForPDFExport(projectName As String)
    '
    ' Prepare all sheets for PDF export
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        Call SetupSheetForPDF(ws, projectName)
    Next ws
End Sub

Sub SetupSheetForPDF(ws As Worksheet, projectName As String)
    '
    ' Setup individual sheet for PDF export
    '
    
    With ws
        ' Hide gridlines and headers
        .DisplayGridlines = False
        .DisplayHeadings = False
        
        ' Page setup
        With .PageSetup
            .PrintGridlines = False
            .PrintHeadings = False
            .PaperSize = xlPaperA4
            .FitToPagesWide = 1
            .FitToPagesTall = False
            .Zoom = False
            
            ' Auto-detect orientation based on content
            If .Parent.UsedRange.Columns.Count > 6 Then
                .Orientation = xlLandscape
            Else
                .Orientation = xlPortrait
            End If
            
            ' Headers and footers
            .LeftHeader = "&L" & projectName
            .CenterHeader = "&C&B" & ws.Name
            .RightHeader = "&R" & Format(Now, "dd-mmm-yyyy")
            
            .LeftFooter = "&L" & "Construction Estimation System"
            .CenterFooter = ""
            .RightFooter = "&R" & "Page &P of &N"
            
            ' Margins
            .LeftMargin = Application.InchesToPoints(0.7)
            .RightMargin = Application.InchesToPoints(0.7)
            .TopMargin = Application.InchesToPoints(0.75)
            .BottomMargin = Application.InchesToPoints(0.75)
            .HeaderMargin = Application.InchesToPoints(0.3)
            .FooterMargin = Application.InchesToPoints(0.3)
        End With
    End With
End Sub

Sub ExportSheetsToPDF(filePath As String)
    '
    ' Export sheets to PDF in logical order
    '
    
    Dim sheetsToExport As Collection
    Dim ws As Worksheet
    Dim sheetArray() As String
    Dim i As Integer
    
    Set sheetsToExport = New Collection
    
    ' Add General Abstract first
    If SheetExists(GENERAL_ABSTRACT) Then
        sheetsToExport.Add ThisWorkbook.Worksheets(GENERAL_ABSTRACT)
    End If
    
    ' Add Abstract and Measurement pairs in order
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            
            ' Add Abstract sheet
            sheetsToExport.Add ws
            
            ' Add corresponding Measurement sheet
            Dim measurementName As String
            Dim partName As String
            partName = ExtractPartName(ws.Name, "Abstract")
            measurementName = MEASUREMENT_PREFIX & " " & partName
            
            If SheetExists(measurementName) Then
                sheetsToExport.Add ThisWorkbook.Worksheets(measurementName)
            End If
        End If
    Next ws
    
    ' Convert collection to array for export
    If sheetsToExport.Count > 0 Then
        ReDim sheetArray(1 To sheetsToExport.Count)
        
        For i = 1 To sheetsToExport.Count
            sheetArray(i) = sheetsToExport(i).Name
        Next i
        
        ' Export to PDF
        ThisWorkbook.Worksheets(sheetArray).ExportAsFixedFormat _
            Type:=xlTypePDF, _
            Filename:=filePath, _
            Quality:=xlQualityStandard, _
            IncludeDocProps:=True, _
            IgnorePrintAreas:=False, _
            OpenAfterPublish:=False
    End If
End Sub

Sub RestoreAfterPDFExport()
    '
    ' Restore original formatting after PDF export
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        ws.DisplayGridlines = True
        ws.DisplayHeadings = True
    Next ws
End Sub

' ===============================================================================
' EXCEL EXPORT SYSTEM
' ===============================================================================

Sub ExportToExcel()
    '
    ' Export to clean Excel file without macros
    '
    
    Dim filePath As String
    Dim newWb As Workbook
    Dim ws As Worksheet
    Dim newWs As Worksheet
    
    On Error GoTo ErrorHandler
    
    ' Get save location
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=g_ProjectName & "_Estimate_Export.xlsx", _
        FileFilter:="Excel Files (*.xlsx), *.xlsx", _
        Title:="Export to Excel")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Create new workbook
    Set newWb = Workbooks.Add
    
    ' Remove default sheets
    Do While newWb.Worksheets.Count > 1
        newWb.Worksheets(newWb.Worksheets.Count).Delete
    Loop
    
    ' Copy all sheets from source
    For Each ws In ThisWorkbook.Worksheets
        ws.Copy After:=newWb.Sheets(newWb.Sheets.Count)
        Set newWs = newWb.Sheets(newWb.Sheets.Count)
        
        ' Remove protection and unlock all cells
        newWs.Unprotect Password:="estimation2025"
        newWs.Cells.Locked = False
        
        ' Ensure formulas are calculated
        newWs.Calculate
    Next ws
    
    ' Remove the original default sheet
    newWb.Sheets(1).Delete
    
    ' Add export log
    Call CreateExportLogSheet(newWb, "Excel", filePath)
    
    ' Save as Excel file
    newWb.SaveAs filePath, FileFormat:=xlOpenXMLWorkbook
    newWb.Close
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "Estimate exported to Excel successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
    
    Exit Sub
    
ErrorHandler:
    If Not newWb Is Nothing Then newWb.Close False
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    Call HandleError("ExportToExcel", Err.Description)
End Sub

' ===============================================================================
' CSV EXPORT SYSTEM
' ===============================================================================

Sub ExportToCSVPackage()
    '
    ' Export all sheets as CSV files in a package
    '
    
    Dim folderPath As String
    Dim ws As Worksheet
    Dim csvPath As String
    Dim timestamp As String
    
    On Error GoTo ErrorHandler
    
    ' Get folder for CSV export
    With Application.FileDialog(msoFileDialogFolderPicker)
        .Title = "Select Folder for CSV Export"
        .AllowMultiSelect = False
        If .Show = -1 Then
            folderPath = .SelectedItems(1)
        Else
            Exit Sub
        End If
    End With
    
    ' Create subfolder with timestamp
    timestamp = Format(Now, "yyyymmdd_hhmmss")
    folderPath = folderPath & "\" & g_ProjectName & "_CSV_" & timestamp
    MkDir folderPath
    
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Export each sheet as CSV
    For Each ws In ThisWorkbook.Worksheets
        csvPath = folderPath & "\" & CleanFileName(ws.Name) & ".csv"
        Call ExportSheetToCSV(ws, csvPath)
    Next ws
    
    ' Create summary file
    Call CreateCSVSummary(folderPath)
    
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    
    MsgBox "CSV files exported successfully to:" & vbCrLf & folderPath, _
           vbInformation, "Export Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.DisplayAlerts = True
    Application.ScreenUpdating = True
    Call HandleError("ExportToCSVPackage", Err.Description)
End Sub

Sub ExportSheetToCSV(ws As Worksheet, filePath As String)
    '
    ' Export single sheet to CSV
    '
    
    Dim tempWb As Workbook
    Dim tempWs As Worksheet
    
    ' Create temporary workbook
    Set tempWb = Workbooks.Add
    Set tempWs = tempWb.Worksheets(1)
    
    ' Copy data (values only to avoid formula errors)
    ws.UsedRange.Copy
    tempWs.Range("A1").PasteSpecial xlPasteValues
    
    ' Save as CSV
    tempWb.SaveAs filePath, FileFormat:=xlCSV
    tempWb.Close False
    
    Application.CutCopyMode = False
End Sub

Function CleanFileName(fileName As String) As String
    '
    ' Clean filename for file system compatibility
    '
    
    Dim invalidChars As String
    Dim i As Integer
    
    invalidChars = "\/:*?""<>|"
    
    For i = 1 To Len(invalidChars)
        fileName = Replace(fileName, Mid(invalidChars, i, 1), "_")
    Next i
    
    CleanFileName = fileName
End Function

Sub CreateCSVSummary(folderPath As String)
    '
    ' Create summary file for CSV export
    '
    
    Dim summaryPath As String
    Dim fileNum As Integer
    Dim ws As Worksheet
    
    summaryPath = folderPath & "\README.txt"
    fileNum = FreeFile
    
    Open summaryPath For Output As fileNum
    
    Print #fileNum, "CONSTRUCTION ESTIMATE CSV EXPORT"
    Print #fileNum, "================================="
    Print #fileNum, ""
    Print #fileNum, "Project: " & g_ProjectName
    Print #fileNum, "Export Date: " & Format(Now, "dd-mmm-yyyy hh:mm")
    Print #fileNum, "Export Type: CSV Package"
    Print #fileNum, ""
    Print #fileNum, "Files Included:"
    Print #fileNum, "---------------"
    
    For Each ws In ThisWorkbook.Worksheets
        Print #fileNum, "- " & CleanFileName(ws.Name) & ".csv (" & ws.Name & ")"
    Next ws
    
    Print #fileNum, ""
    Print #fileNum, "Notes:"
    Print #fileNum, "- All formulas have been converted to values"
    Print #fileNum, "- Files can be opened in Excel or any spreadsheet application"
    Print #fileNum, "- Original formatting may not be preserved"
    
    Close fileNum
End Sub

' ===============================================================================
' HTML EXPORT SYSTEM
' ===============================================================================

Sub ExportToHTML()
    '
    ' Export estimate as printable HTML
    '
    
    Dim filePath As String
    Dim htmlContent As String
    Dim fileNum As Integer
    
    On Error GoTo ErrorHandler
    
    ' Get save location
    filePath = Application.GetSaveAsFilename( _
        InitialFilename:=g_ProjectName & "_Estimate.html", _
        FileFilter:="HTML Files (*.html), *.html", _
        Title:="Export to HTML")
    
    If filePath = "False" Then Exit Sub
    
    Application.StatusBar = "Generating HTML content..."
    
    ' Generate HTML content
    htmlContent = GenerateHTMLContent()
    
    ' Write to file
    fileNum = FreeFile
    Open filePath For Output As fileNum
    Print #fileNum, htmlContent
    Close fileNum
    
    Application.StatusBar = False
    
    ' Log export
    Call LogExport("HTML", filePath)
    
    MsgBox "HTML report created successfully!" & vbCrLf & filePath, _
           vbInformation, "Export Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.StatusBar = False
    Call HandleError("ExportToHTML", Err.Description)
End Sub

Function GenerateHTMLContent() As String
    '
    ' Generate complete HTML content
    '
    
    Dim html As String
    Dim ws As Worksheet
    
    ' HTML header
    html = "<!DOCTYPE html>" & vbCrLf & _
           "<html lang=""en"">" & vbCrLf & _
           "<head>" & vbCrLf & _
           "<meta charset=""UTF-8"">" & vbCrLf & _
           "<meta name=""viewport"" content=""width=device-width, initial-scale=1.0"">" & vbCrLf & _
           "<title>" & g_ProjectName & " - Construction Estimate</title>" & vbCrLf & _
           "<style>" & vbCrLf & _
           GetHTMLStyles() & vbCrLf & _
           "</style>" & vbCrLf & _
           "</head>" & vbCrLf & _
           "<body>" & vbCrLf & _
           "<div class=""header"">" & vbCrLf & _
           "<h1>Construction Estimate Report</h1>" & vbCrLf & _
           "<h2>" & g_ProjectName & "</h2>" & vbCrLf & _
           "<p>Generated on: " & Format(Now, "dd-mmm-yyyy hh:mm") & "</p>" & vbCrLf & _
           "</div>" & vbCrLf
    
    ' Add each sheet
    For Each ws In ThisWorkbook.Worksheets
        html = html & GenerateSheetHTML(ws) & vbCrLf
    Next ws
    
    ' HTML footer
    html = html & _
           "<div class=""footer"">" & vbCrLf & _
           "<p>Generated by Construction Estimation System</p>" & vbCrLf & _
           "</div>" & vbCrLf & _
           "</body>" & vbCrLf & _
           "</html>"
    
    GenerateHTMLContent = html
End Function

Function GetHTMLStyles() As String
    '
    ' Get CSS styles for HTML export
    '
    
    GetHTMLStyles = _
        "body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }" & vbCrLf & _
        ".header { text-align: center; margin-bottom: 30px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }" & vbCrLf & _
        ".header h1 { color: #2c3e50; margin: 0; }" & vbCrLf & _
        ".header h2 { color: #34495e; margin: 10px 0; }" & vbCrLf & _
        ".sheet-section { margin-bottom: 40px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }" & vbCrLf & _
        ".sheet-title { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-bottom: 20px; }" & vbCrLf & _
        "table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }" & vbCrLf & _
        "th { background-color: #3498db; color: white; padding: 12px 8px; text-align: left; font-weight: bold; }" & vbCrLf & _
        "td { padding: 8px; border-bottom: 1px solid #ddd; }" & vbCrLf & _
        "tr:nth-child(even) { background-color: #f8f9fa; }" & vbCrLf & _
        "tr:hover { background-color: #e8f4f8; }" & vbCrLf & _
        ".number { text-align: right; font-family: 'Courier New', monospace; }" & vbCrLf & _
        ".total-row { background-color: #fff3cd !important; font-weight: bold; }" & vbCrLf & _
        ".grand-total { background-color: #d4edda !important; font-weight: bold; font-size: 1.1em; }" & vbCrLf & _
        ".footer { text-align: center; margin-top: 40px; padding: 20px; color: #6c757d; }" & vbCrLf & _
        "@media print { body { background: white; } .sheet-section { box-shadow: none; page-break-inside: avoid; } }"
End Function

Function GenerateSheetHTML(ws As Worksheet) As String
    '
    ' Generate HTML table for a single sheet
    '
    
    Dim html As String
    Dim lastRow As Long, lastCol As Long
    Dim r As Long, c As Long
    Dim cellValue As Variant
    Dim cssClass As String
    
    html = "<div class=""sheet-section"">" & vbCrLf & _
           "<h2 class=""sheet-title"">" & ws.Name & "</h2>" & vbCrLf & _
           "<table>" & vbCrLf
    
    lastRow = ws.UsedRange.Rows.Count
    lastCol = ws.UsedRange.Columns.Count
    
    For r = 1 To lastRow
        ' Determine row class
        cssClass = ""
        If r = 5 Then cssClass = " class=""header-row"""
        If InStr(LCase(ws.Cells(r, 2).Value), "total") > 0 Then cssClass = " class=""total-row"""
        If InStr(LCase(ws.Cells(r, 2).Value), "grand total") > 0 Then cssClass = " class=""grand-total"""
        
        html = html & "<tr" & cssClass & ">"
        
        For c = 1 To lastCol
            cellValue = ws.Cells(r, c).Value
            
            ' Format cell content
            If IsNumeric(cellValue) And cellValue <> "" And c > 2 Then
                If cellValue = Int(cellValue) Then
                    html = html & "<td class=""number"">" & Format(cellValue, "#,##0") & "</td>"
                Else
                    html = html & "<td class=""number"">" & Format(cellValue, "#,##0.00") & "</td>"
                End If
            Else
                html = html & "<td>" & cellValue & "</td>"
            End If
        Next c
        
        html = html & "</tr>" & vbCrLf
    Next r
    
    html = html & "</table>" & vbCrLf & "</div>" & vbCrLf
    
    GenerateSheetHTML = html
End Function

' ===============================================================================
' EXPORT LOGGING SYSTEM
' ===============================================================================

Sub LogExport(exportType As String, filePath As String)
    '
    ' Log export activity
    '
    
    Dim logWs As Worksheet
    Dim lastRow As Long
    
    ' Get or create log sheet
    On Error Resume Next
    Set logWs = ThisWorkbook.Worksheets("Export_Log")
    On Error GoTo 0
    
    If logWs Is Nothing Then
        Set logWs = ThisWorkbook.Worksheets.Add
        logWs.Name = "Export_Log"
        logWs.Visible = xlSheetVeryHidden
        
        ' Setup headers
        logWs.Range("A1").Value = "Timestamp"
        logWs.Range("B1").Value = "Export Type"
        logWs.Range("C1").Value = "User"
        logWs.Range("D1").Value = "File Path"
        logWs.Range("E1").Value = "Project Name"
        logWs.Range("A1:E1").Font.Bold = True
    End If
    
    ' Add log entry
    lastRow = logWs.Cells(logWs.Rows.Count, 1).End(xlUp).Row + 1
    logWs.Cells(lastRow, 1).Value = Now
    logWs.Cells(lastRow, 2).Value = exportType
    logWs.Cells(lastRow, 3).Value = Application.UserName
    logWs.Cells(lastRow, 4).Value = filePath
    logWs.Cells(lastRow, 5).Value = g_ProjectName
End Sub

Sub CreateExportLogSheet(wb As Workbook, exportType As String, filePath As String)
    '
    ' Create export log sheet in exported workbook
    '
    
    Dim logWs As Worksheet
    
    Set logWs = wb.Worksheets.Add
    logWs.Name = "Export_Info"
    logWs.Visible = xlSheetVeryHidden
    
    With logWs
        .Range("A1").Value = "Export Information"
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Size = 14
        
        .Range("A3").Value = "Export Date:"
        .Range("B3").Value = Now
        
        .Range("A4").Value = "Export Type:"
        .Range("B4").Value = exportType
        
        .Range("A5").Value = "Original File:"
        .Range("B5").Value = ThisWorkbook.Name
        
        .Range("A6").Value = "Exported By:"
        .Range("B6").Value = Application.UserName
        
        .Range("A7").Value = "Project Name:"
        .Range("B7").Value = g_ProjectName
        
        .Range("A8").Value = "Export Path:"
        .Range("B8").Value = filePath
        
        .Range("A10").Value = "Notes:"
        .Range("A11").Value = "- This is a clean copy without macros"
        .Range("A12").Value = "- All formulas have been preserved"
        .Range("A13").Value = "- Sheet protection has been removed"
        .Range("A14").Value = "- Generated by Construction Estimation System"
    End With
End Sub

Sub LogError(source As String, description As String)
    '
    ' Log errors for debugging
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
        logWs.Range("D1").Value = "User"
        logWs.Range("A1:D1").Font.Bold = True
    End If
    
    lastRow = logWs.Cells(logWs.Rows.Count, 1).End(xlUp).Row + 1
    logWs.Cells(lastRow, 1).Value = Now
    logWs.Cells(lastRow, 2).Value = source
    logWs.Cells(lastRow, 3).Value = description
    logWs.Cells(lastRow, 4).Value = Application.UserName
End Sub