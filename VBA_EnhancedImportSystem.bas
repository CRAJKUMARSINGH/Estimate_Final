' ===============================================================================
' ENHANCED IMPORT SYSTEM FOR CONSTRUCTION ESTIMATION
' ===============================================================================
' File: VBA_EnhancedImportSystem.bas
' Purpose: Enhanced Excel import functionality for estimates and SSR data
' ===============================================================================

Option Explicit

' Constants for file patterns
Public Const ATTACHED_ASSETS_FOLDER As String = "attached_assets"
Public Const ESTIMATE_FILE_PATTERN As String = "att*.xlsx"
Public Const SSR_FILE_PATTERN As String = "*ssr*.xlsx"

' ===============================================================================
' ENHANCED IMPORT FROM ATTACHED ASSETS FOLDER
' ===============================================================================

Sub ImportEstimateFromAttachedAssets()
    '
    ' Import estimate from attached_assets folder with att* pattern
    '
    
    Dim folderPath As String
    Dim fileName As String
    Dim filePath As String
    Dim fileCount As Integer
    Dim selectedFile As String
    Dim i As Integer
    Dim fileList As Collection
    Dim userChoice As String
    
    ' Determine folder path
    folderPath = ThisWorkbook.Path & "\" & ATTACHED_ASSETS_FOLDER
    If Dir(folderPath, vbDirectory) = "" Then
        folderPath = Application.ActiveWorkbook.Path & "\" & ATTACHED_ASSETS_FOLDER
        If Dir(folderPath, vbDirectory) = "" Then
            MsgBox "Attached assets folder not found! Please ensure the '" & ATTACHED_ASSETS_FOLDER & "' folder exists.", _
                   vbCritical, "Folder Not Found"
            Exit Sub
        End If
    End If
    
    ' Find files matching pattern
    Set fileList = New Collection
    fileName = Dir(folderPath & "\att*.xlsx")
    
    Do While fileName <> ""
        fileList.Add fileName
        fileName = Dir
    Loop
    
    ' Check if any files found
    If fileList.Count = 0 Then
        MsgBox "No estimate files found in '" & folderPath & "' matching pattern 'att*.xlsx'", _
               vbInformation, "No Files Found"
        Exit Sub
    End If
    
    ' If only one file, use it directly
    If fileList.Count = 1 Then
        selectedFile = fileList(1)
    Else
        ' Create file selection dialog
        Dim fileListText As String
        fileListText = "Select an estimate file to import:" & vbCrLf & vbCrLf
        For i = 1 To fileList.Count
            fileListText = fileListText & i & ". " & fileList(i) & vbCrLf
        Next i
        fileListText = fileListText & vbCrLf & "Enter number (1-" & fileList.Count & "):"
        
        userChoice = InputBox(fileListText, "Select Estimate File", "1")
        If userChoice = "" Then Exit Sub
        
        ' Validate user choice
        If Not IsNumeric(userChoice) Then
            MsgBox "Invalid selection!", vbExclamation, "Invalid Input"
            Exit Sub
        End If
        
        i = CInt(userChoice)
        If i < 1 Or i > fileList.Count Then
            MsgBox "Selection out of range!", vbExclamation, "Invalid Selection"
            Exit Sub
        End If
        
        selectedFile = fileList(i)
    End If
    
    ' Create full file path
    filePath = folderPath & "\" & selectedFile
    
    ' Import the selected file
    Call ImportEstimateFromFile(filePath)
End Sub

Sub ImportEstimateFromFile(filePath As String)
    '
    ' Import estimate from specified file path
    '
    
    Dim sourceWb As Workbook
    Dim ws As Worksheet
    Dim partPairs As Collection
    Dim partName As String
    Dim abstractSheet As String
    Dim measurementSheet As String
    Dim response As VbMsgBoxResult
    
    ' Confirm import
    response = MsgBox("Import estimate from '" & filePath & "'?" & vbCrLf & vbCrLf & _
                     "This will replace all current estimate data.", _
                     vbYesNo + vbQuestion, "Confirm Import")
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Importing estimate file..."
    
    ' Open source workbook
    On Error GoTo ErrorHandler
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Clear existing sheets (except General Abstract)
    Call ClearExistingSheets
    
    ' Create collection to track part pairs
    Set partPairs = New Collection
    
    ' Import and map sheets
    For Each ws In sourceWb.Worksheets
        If InStr(1, ws.Name, "General Abstract", vbTextCompare) > 0 Then
            Call ImportGeneralAbstract(ws)
        ElseIf InStr(1, ws.Name, "Abstract of Cost", vbTextCompare) > 0 Then
            Call ImportAbstractSheet(ws)
            ' Extract part name and add to collection
            partName = Replace(ws.Name, "Abstract of Cost", "")
            partName = Trim(partName)
            abstractSheet = ws.Name
            partPairs.Add Array(partName, abstractSheet, ""), partName & "_abstract"
        ElseIf InStr(1, ws.Name, "Measurement", vbTextCompare) > 0 Then
            Call ImportMeasurementSheet(ws)
            ' Extract part name and update collection
            partName = Replace(ws.Name, "Measurement", "")
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
    Application.StatusBar = False
    
    MsgBox "Estimate imported successfully from '" & filePath & "'!" & vbCrLf & _
           "Total parts imported: " & partPairs.Count & vbCrLf & vbCrLf & _
           "All sheets and formulas have been mapped.", _
           vbInformation, "Import Complete"
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.StatusBar = False
    MsgBox "Error importing file: " & Err.Description, vbCritical, "Import Error"
End Sub

' ===============================================================================
' ENHANCED MEASUREMENTS FUNCTIONALITY
' ===============================================================================

Sub AddNewLineToMeasurements()
    '
    ' Add new line to selected measurement sheet
    '
    
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim newRow As Long
    Dim description As String
    Dim unit As String
    Dim quantity As Double, length As Double, breadth As Double, height As Double
    Dim itemId As String
    Dim nextId As Long
    
    ' Check if active sheet is a measurement sheet
    Set ws = ActiveSheet
    If InStr(1, ws.Name, "Measurement", vbTextCompare) = 0 Then
        MsgBox "Please select a Measurement sheet to add items.", _
               vbExclamation, "Invalid Sheet"
        Exit Sub
    End If
    
    ' Get next item ID
    nextId = GetNextItemId(ws)
    itemId = Format(nextId, "000")
    
    ' Get item details from user
    description = InputBox("Enter item description:", "New Measurement Item", "")
    If description = "" Then Exit Sub
    
    unit = InputBox("Enter unit (e.g., Cum, Sqm, Nos):", "Unit", "Cum")
    If unit = "" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Adding new measurement item..."
    
    ' Get measurements
    quantity = Val(InputBox("Enter number of items:", "Quantity", "1"))
    length = Val(InputBox("Enter length:", "Length", "1"))
    breadth = Val(InputBox("Enter breadth:", "Breadth", "1"))
    height = Val(InputBox("Enter height:", "Height", "1"))
    
    ' Find last row and insert new item
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    newRow = lastRow + 1
    
    ' Insert new row
    ws.Rows(newRow).Insert
    
    ' Add item data
    ws.Cells(newRow, 1).Value = itemId ' Item ID
    ws.Cells(newRow, 2).Value = description
    ws.Cells(newRow, 3).Value = unit
    ws.Cells(newRow, 4).Value = quantity
    ws.Cells(newRow, 5).Value = length
    ws.Cells(newRow, 6).Value = breadth
    ws.Cells(newRow, 7).Value = height
    ws.Cells(newRow, 8).Formula = "=D" & newRow & "*E" & newRow & "*F" & newRow & "*G" & newRow ' Total formula
    
    ' Update formulas and linkages
    Call UpdateSheetFormulas(ws)
    Call RebuildFormulasAndLinkages
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "New measurement item added successfully!" & vbCrLf & _
           "Item ID: " & itemId & vbCrLf & _
           "Description: " & description, vbInformation, "Item Added"
End Sub

Sub UpdateAllMeasurements()
    '
    ' Update all measurement calculations
    '
    
    Dim ws As Worksheet
    Dim updatedCount As Integer
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Updating measurements..."
    
    updatedCount = 0
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, "Measurement", vbTextCompare) > 0 Then
            Call UpdateSheetFormulas(ws)
            updatedCount = updatedCount + 1
        End If
    Next ws
    
    ' Rebuild all linkages
    Call RebuildFormulasAndLinkages
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "Updated " & updatedCount & " measurement sheet(s)!" & vbCrLf & _
           "All formulas and linkages have been recalculated.", _
           vbInformation, "Update Complete"
End Sub

' ===============================================================================
' ENHANCED SSR FUNCTIONALITY
' ===============================================================================

Sub ImportSSRFromExcel()
    '
    ' Import SSR data from Excel file
    '
    
    Dim filePath As String
    Dim sourceWb As Workbook
    Dim sourceWs As Worksheet
    Dim ssrWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim importedCount As Long
    
    ' Get file path from user
    filePath = Application.GetOpenFilename( _
        "Excel Files (*.xlsx; *.xls), *.xlsx; *.xls", , _
        "Select SSR Excel File to Import")
    
    If filePath = "False" Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Importing SSR data..."
    
    ' Open source workbook
    On Error GoTo ErrorHandler
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Try to find SSR sheet in source workbook
    For Each sourceWs In sourceWb.Worksheets
        If InStr(1, sourceWs.Name, "SSR", vbTextCompare) > 0 Or _
           InStr(1, sourceWs.Name, "Schedule", vbTextCompare) > 0 Then
            Set ssrWs = sourceWs
            Exit For
        End If
    Next sourceWs
    
    ' If no SSR sheet found, use first sheet
    If ssrWs Is Nothing Then
        Set ssrWs = sourceWb.Worksheets(1)
    End If
    
    ' Import SSR data
    importedCount = 0
    lastRow = ssrWs.Cells(ssrWs.Rows.Count, 1).End(xlUp).Row
    
    ' Look for SSR data in General Abstract sheet or create new
    Dim targetWs As Worksheet
    If SheetExists("SSR Database") Then
        Set targetWs = ThisWorkbook.Worksheets("SSR Database")
        targetWs.Cells.Clear
    Else
        Set targetWs = ThisWorkbook.Worksheets.Add
        targetWs.Name = "SSR Database"
    End If
    
    ' Copy headers and data
    ssrWs.Rows(1).Copy targetWs.Rows(1) ' Copy headers
    For i = 2 To lastRow
        If ssrWs.Cells(i, 1).Value <> "" Then
            ssrWs.Rows(i).Copy targetWs.Rows(importedCount + 2)
            importedCount = importedCount + 1
        End If
    Next i
    
    ' Close source workbook
    sourceWb.Close False
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "SSR data imported successfully!" & vbCrLf & _
           "Total items imported: " & importedCount, _
           vbInformation, "SSR Import Complete"
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.StatusBar = False
    MsgBox "Error importing SSR data: " & Err.Description, vbCritical, "Import Error"
End Sub

Sub UpdateSSRDatabase()
    '
    ' Update SSR database from current estimate
    '
    
    Dim ws As Worksheet
    Dim ssrWs As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim ssrItems As Collection
    Dim currentItem As Variant
    Dim newItem As Boolean
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Updating SSR database..."
    
    ' Create or get SSR Database sheet
    If Not SheetExists("SSR Database") Then
        Set ssrWs = ThisWorkbook.Worksheets.Add
        ssrWs.Name = "SSR Database"
        ' Setup headers
        ssrWs.Cells(1, 1).Value = "Code"
        ssrWs.Cells(1, 2).Value = "Description"
        ssrWs.Cells(1, 3).Value = "Category"
        ssrWs.Cells(1, 4).Value = "Unit"
        ssrWs.Cells(1, 5).Value = "Rate"
        ssrWs.Cells(1, 6).Value = "Source Sheet"
        ssrWs.Rows(1).Font.Bold = True
    Else
        Set ssrWs = ThisWorkbook.Worksheets("SSR Database")
    End If
    
    ' Collect SSR items from all sheets
    Set ssrItems = New Collection
    
    For Each ws In ThisWorkbook.Worksheets
        ' Look for SSR references in Abstract sheets
        If InStr(1, ws.Name, "Abstract of Cost", vbTextCompare) > 0 Then
            lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
            For i = 6 To lastRow ' Assuming data starts from row 6
                If ws.Cells(i, 1).Value <> "" Then
                    ' Check if item has SSR code reference
                    If ws.Cells(i, 9).Value <> "" Then ' Assuming SSR code in column I
                        newItem = True
                        ' Check if item already exists
                        For Each currentItem In ssrItems
                            If currentItem(1) = ws.Cells(i, 9).Value Then
                                newItem = False
                                Exit For
                            End If
                        Next currentItem
                        
                        ' Add new item if not exists
                        If newItem Then
                            ssrItems.Add Array(ws.Cells(i, 9).Value, _
                                             ws.Cells(i, 2).Value, _
                                             "From Estimate", _
                                             ws.Cells(i, 3).Value, _
                                             ws.Cells(i, 5).Value, _
                                             ws.Name)
                        End If
                    End If
                End If
            Next i
        End If
    Next ws
    
    ' Add collected items to SSR database
    For i = 1 To ssrItems.Count
        ssrWs.Cells(i + 1, 1).Value = ssrItems(i)(0) ' Code
        ssrWs.Cells(i + 1, 2).Value = ssrItems(i)(1) ' Description
        ssrWs.Cells(i + 1, 3).Value = ssrItems(i)(2) ' Category
        ssrWs.Cells(i + 1, 4).Value = ssrItems(i)(3) ' Unit
        ssrWs.Cells(i + 1, 5).Value = ssrItems(i)(4) ' Rate
        ssrWs.Cells(i + 1, 6).Value = ssrItems(i)(5) ' Source
    Next i
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    MsgBox "SSR database updated!" & vbCrLf & _
           "Total items in database: " & ssrItems.Count, _
           vbInformation, "SSR Update Complete"
End Sub

' ===============================================================================
' WHOLE ESTIMATE IMPORT FUNCTIONALITY
' ===============================================================================

Sub ImportWholeEstimate()
    '
    ' Import entire estimate as a whole with all components
    '
    
    Dim filePath As String
    Dim sourceWb As Workbook
    Dim ws As Worksheet
    Dim response As VbMsgBoxResult
    Dim importSummary As String
    Dim sheetCount As Integer
    Dim partCount As Integer
    Dim ssrCount As Integer
    
    ' Get file path from user
    filePath = Application.GetOpenFilename( _
        "Excel Files (*.xlsx; *.xls), *.xlsx; *.xls", , _
        "Select Complete Estimate File to Import")
    
    If filePath = "False" Then Exit Sub
    
    ' Confirm import
    response = MsgBox("Import complete estimate from '" & filePath & "'?" & vbCrLf & vbCrLf & _
                     "This will replace all current data including SSR database.", _
                     vbYesNo + vbQuestion + vbDefaultButton2, "Confirm Import")
    If response = vbNo Then Exit Sub
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.StatusBar = "Importing complete estimate..."
    
    ' Open source workbook
    On Error GoTo ErrorHandler
    Set sourceWb = Workbooks.Open(filePath, ReadOnly:=True)
    
    ' Clear all existing sheets
    Call ClearAllSheets
    
    ' Import all sheets
    sheetCount = 0
    partCount = 0
    ssrCount = 0
    
    For Each ws In sourceWb.Worksheets
        sheetCount = sheetCount + 1
        
        ' Copy sheet to current workbook
        ws.Copy After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count)
        
        ' Update counters based on sheet type
        If InStr(1, ws.Name, "Abstract of Cost", vbTextCompare) > 0 Then
            partCount = partCount + 1
        ElseIf InStr(1, ws.Name, "SSR", vbTextCompare) > 0 Then
            ssrCount = ssrCount + 1
        End If
    Next ws
    
    ' Close source workbook
    sourceWb.Close False
    
    ' Rebuild formulas and linkages
    Call RebuildFormulasAndLinkages
    
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.StatusBar = False
    
    ' Create import summary
    importSummary = "Complete estimate imported successfully!" & vbCrLf & vbCrLf & _
                  "Summary:" & vbCrLf & _
                  "• Total sheets: " & sheetCount & vbCrLf & _
                  "• Parts imported: " & partCount & vbCrLf & _
                  "• SSR sheets: " & ssrCount & vbCrLf & vbCrLf & _
                  "All formulas and linkages have been rebuilt."
    
    MsgBox importSummary, vbInformation, "Complete Import Complete"
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    Application.StatusBar = False
    MsgBox "Error importing complete estimate: " & Err.Description, vbCritical, "Import Error"
End Sub

' ===============================================================================
' UTILITY FUNCTIONS
' ===============================================================================

Sub ClearAllSheets()
    '
    ' Clear all sheets including logs and SSR database
    '
    
    Dim ws As Worksheet
    Dim sheetsToDelete As Collection
    Dim i As Integer
    
    Set sheetsToDelete = New Collection
    
    ' Collect all sheets except very hidden ones
    For Each ws In ThisWorkbook.Worksheets
        If ws.Visible = xlSheetVisible Then
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

' ===============================================================================
' INTERFACE INTEGRATION
' ===============================================================================

Sub AddEnhancedImportButtons()
    '
    ' Add enhanced import functionality to main interface
    '
    
    ' This would typically be called to add buttons to the ribbon or form
    ' For now, we'll just show a message with available functions
    Dim msg As String
    msg = "Enhanced Import Functions Available:" & vbCrLf & vbCrLf & _
          "VBA Functions:" & vbCrLf & _
          "• ImportEstimateFromAttachedAssets - Import from att*.xlsx files" & vbCrLf & _
          "• AddNewLineToMeasurements - Add new line to measurement sheets" & vbCrLf & _
          "• UpdateAllMeasurements - Recalculate all measurements" & vbCrLf & _
          "• ImportSSRFromExcel - Import SSR data from Excel" & vbCrLf & _
          "• UpdateSSRDatabase - Update SSR from current estimate" & vbCrLf & _
          "• ImportWholeEstimate - Import complete estimate as whole" & vbCrLf & vbCrLf & _
          "Assign these to buttons or keyboard shortcuts as needed."
    
    MsgBox msg, vbInformation, "Enhanced Import Functions"
End Sub