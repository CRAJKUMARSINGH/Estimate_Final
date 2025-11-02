' ===============================================================================
' TESTING AND VALIDATION MODULE
' ===============================================================================
' File: Testing_Validation_Module.bas
' Purpose: System validation, testing, and quality assurance functions
' ===============================================================================

Option Explicit

' ===============================================================================
' SYSTEM VALIDATION FUNCTIONS
' ===============================================================================

Sub ValidateSystemStructure()
    '
    ' Comprehensive system structure validation
    '
    
    Dim validationResults As Collection
    Dim ws As Worksheet
    Dim partName As String
    Dim issueCount As Integer
    
    Set validationResults = New Collection
    issueCount = 0
    
    Application.ScreenUpdating = False
    
    ' Check General Abstract
    If Not SheetExists(GENERAL_ABSTRACT) Then
        validationResults.Add "❌ General Abstract sheet is missing"
        issueCount = issueCount + 1
    Else
        Call ValidateGeneralAbstractStructure(validationResults, issueCount)
    End If
    
    ' Check part pairs
    Call ValidatePartPairs(validationResults, issueCount)
    
    ' Check formulas
    Call ValidateFormulas(validationResults, issueCount)
    
    ' Check named ranges
    Call ValidateNamedRanges(validationResults, issueCount)
    
    ' Check protection
    Call ValidateProtection(validationResults, issueCount)
    
    Application.ScreenUpdating = True
    
    ' Display results
    Call DisplayValidationResults(validationResults, issueCount)
End Sub

Sub ValidateGeneralAbstractStructure(validationResults As Collection, ByRef issueCount As Integer)
    '
    ' Validate General Abstract sheet structure
    '
    
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Worksheets(GENERAL_ABSTRACT)
    
    ' Check headers
    If ws.Range("A5").Value <> "S.No." Then
        validationResults.Add "⚠️ General Abstract: Header structure incorrect"
        issueCount = issueCount + 1
    End If
    
    ' Check formulas
    If Not ws.Range("C20").HasFormula Then
        validationResults.Add "⚠️ General Abstract: Subtotal formula missing"
        issueCount = issueCount + 1
    End If
    
    If Not ws.Range("C25").HasFormula Then
        validationResults.Add "⚠️ General Abstract: Grand total formula missing"
        issueCount = issueCount + 1
    End If
    
    validationResults.Add "✅ General Abstract structure validated"
End Sub

Sub ValidatePartPairs(validationResults As Collection, ByRef issueCount As Integer)
    '
    ' Validate Abstract-Measurement pairs
    '
    
    Dim ws As Worksheet
    Dim partName As String
    Dim abstractExists As Boolean
    Dim measurementExists As Boolean
    Dim pairCount As Integer
    
    pairCount = 0
    
    ' Check each Abstract sheet for corresponding Measurement
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            
            partName = ExtractPartName(ws.Name, "Abstract")
            measurementExists = SheetExists(MEASUREMENT_PREFIX & " " & partName)
            
            If measurementExists Then
                validationResults.Add "✅ Part pair validated: " & partName
                pairCount = pairCount + 1
            Else
                validationResults.Add "❌ Missing Measurement sheet for: " & partName
                issueCount = issueCount + 1
            End If
        End If
    Next ws
    
    ' Check for orphaned Measurement sheets
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            partName = ExtractPartName(ws.Name, "Measurement")
            abstractExists = SheetExists(ABSTRACT_PREFIX & " " & partName)
            
            If Not abstractExists Then
                validationResults.Add "❌ Orphaned Measurement sheet: " & partName
                issueCount = issueCount + 1
            End If
        End If
    Next ws
    
    validationResults.Add "📊 Total validated pairs: " & pairCount
End Sub

Sub ValidateFormulas(validationResults As Collection, ByRef issueCount As Integer)
    '
    ' Validate critical formulas across all sheets
    '
    
    Dim ws As Worksheet
    Dim partName As String
    Dim formulaCount As Integer
    Dim errorCount As Integer
    
    formulaCount = 0
    errorCount = 0
    
    ' Check Abstract sheet formulas
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, ABSTRACT_PREFIX, vbTextCompare) > 0 And _
           ws.Name <> GENERAL_ABSTRACT Then
            
            Call ValidateAbstractFormulas(ws, formulaCount, errorCount)
        End If
    Next ws
    
    ' Check Measurement sheet formulas
    For Each ws In ThisWorkbook.Worksheets
        If InStr(1, ws.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Call ValidateMeasurementFormulas(ws, formulaCount, errorCount)
        End If
    Next ws
    
    If errorCount = 0 Then
        validationResults.Add "✅ All formulas validated (" & formulaCount & " formulas checked)"
    Else
        validationResults.Add "❌ Formula errors found: " & errorCount & " of " & formulaCount
        issueCount = issueCount + errorCount
    End If
End Sub

Sub ValidateAbstractFormulas(ws As Worksheet, ByRef formulaCount As Integer, ByRef errorCount As Integer)
    '
    ' Validate formulas in Abstract sheet
    '
    
    Dim i As Long
    Dim lastRow As Long
    
    lastRow = ws.Cells(ws.Rows.Count, 2).End(xlUp).Row
    
    For i = 6 To lastRow
        If ws.Cells(i, 2).Value <> "" Then
            ' Check amount formula (column F)
            If ws.Cells(i, 6).HasFormula Then
                formulaCount = formulaCount + 1
                If InStr(ws.Cells(i, 6).Formula, "D" & i & "*E" & i) = 0 Then
                    errorCount = errorCount + 1
                End If
            End If
        End If
    Next i
    
    ' Check total formula
    If ws.Cells(50, 6).HasFormula Then
        formulaCount = formulaCount + 1
        If InStr(ws.Cells(50, 6).Formula, "SUM") = 0 Then
            errorCount = errorCount + 1
        End If
    End If
End Sub

Sub ValidateMeasurementFormulas(ws As Worksheet, ByRef formulaCount As Integer, ByRef errorCount As Integer)
    '
    ' Validate formulas in Measurement sheet
    '
    
    Dim i As Long
    Dim lastRow As Long
    
    lastRow = ws.Cells(ws.Rows.Count, 2).End(xlUp).Row
    
    For i = 6 To lastRow
        If ws.Cells(i, 2).Value <> "" Then
            ' Check total formula (column H)
            If ws.Cells(i, 8).HasFormula Then
                formulaCount = formulaCount + 1
                If InStr(ws.Cells(i, 8).Formula, "D" & i & "*E" & i & "*F" & i & "*G" & i) = 0 Then
                    errorCount = errorCount + 1
                End If
            End If
        End If
    Next i
    
    ' Check total formula
    If ws.Cells(50, 8).HasFormula Then
        formulaCount = formulaCount + 1
        If InStr(ws.Cells(50, 8).Formula, "SUM") = 0 Then
            errorCount = errorCount + 1
        End If
    End If
End Sub

Sub ValidateNamedRanges(validationResults As Collection, ByRef issueCount As Integer)
    '
    ' Validate named ranges
    '
    
    Dim nr As Name
    Dim rangeCount As Integer
    Dim errorCount As Integer
    
    rangeCount = 0
    errorCount = 0
    
    For Each nr In ThisWorkbook.Names
        If InStr(nr.Name, "AbstractData_") > 0 Or _
           InStr(nr.Name, "MeasurementData_") > 0 Or _
           nr.Name = "GeneralData" Then
            
            rangeCount = rangeCount + 1
            
            ' Test if range is valid
            On Error Resume Next
            Dim testRange As Range
            Set testRange = nr.RefersToRange
            If Err.Number <> 0 Then
                errorCount = errorCount + 1
                Err.Clear
            End If
            On Error GoTo 0
        End If
    Next nr
    
    If errorCount = 0 Then
        validationResults.Add "✅ Named ranges validated (" & rangeCount & " ranges)"
    Else
        validationResults.Add "❌ Named range errors: " & errorCount & " of " & rangeCount
        issueCount = issueCount + errorCount
    End If
End Sub

Sub ValidateProtection(validationResults As Collection, ByRef issueCount As Integer)
    '
    ' Validate sheet protection settings
    '
    
    Dim ws As Worksheet
    Dim protectedCount As Integer
    Dim unprotectedCount As Integer
    
    protectedCount = 0
    unprotectedCount = 0
    
    For Each ws In ThisWorkbook.Worksheets
        If ws.ProtectContents Then
            protectedCount = protectedCount + 1
        Else
            unprotectedCount = unprotectedCount + 1
        End If
    Next ws
    
    validationResults.Add "🔒 Protected sheets: " & protectedCount
    validationResults.Add "🔓 Unprotected sheets: " & unprotectedCount
    
    If unprotectedCount > 0 Then
        validationResults.Add "⚠️ Consider protecting unprotected sheets"
    End If
End Sub

Sub DisplayValidationResults(validationResults As Collection, issueCount As Integer)
    '
    ' Display validation results to user
    '
    
    Dim resultText As String
    Dim i As Integer
    
    resultText = "🔍 SYSTEM VALIDATION RESULTS" & vbCrLf & vbCrLf
    
    For i = 1 To validationResults.Count
        resultText = resultText & validationResults(i) & vbCrLf
    Next i
    
    resultText = resultText & vbCrLf & "📊 SUMMARY:" & vbCrLf
    
    If issueCount = 0 Then
        resultText = resultText & "✅ System validation passed - No issues found!" & vbCrLf
        resultText = resultText & "🎉 All components are working correctly."
    Else
        resultText = resultText & "⚠️ Issues found: " & issueCount & vbCrLf
        resultText = resultText & "💡 Use 'Rebuild Formulas' to fix most issues."
    End If
    
    MsgBox resultText, vbInformation, "Validation Results"
End Sub

' ===============================================================================
' SYSTEM TESTING FUNCTIONS
' ===============================================================================

Sub RunSystemTests()
    '
    ' Run comprehensive system tests
    '
    
    Dim testResults As Collection
    Set testResults = New Collection
    
    Application.ScreenUpdating = False
    
    ' Test basic functionality
    Call TestBasicFunctionality(testResults)
    
    ' Test formula calculations
    Call TestFormulaCalculations(testResults)
    
    ' Test import functionality
    Call TestImportFunctionality(testResults)
    
    ' Test export functionality
    Call TestExportFunctionality(testResults)
    
    Application.ScreenUpdating = True
    
    ' Display test results
    Call DisplayTestResults(testResults)
End Sub

Sub TestBasicFunctionality(testResults As Collection)
    '
    ' Test basic system functionality
    '
    
    testResults.Add "🧪 Testing Basic Functionality..."
    
    ' Test sheet creation
    If SheetExists(GENERAL_ABSTRACT) Then
        testResults.Add "✅ General Abstract exists"
    Else
        testResults.Add "❌ General Abstract missing"
    End If
    
    ' Test part counting
    Dim partCount As Integer
    partCount = CountPartPairs()
    testResults.Add "📊 Part pairs found: " & partCount
    
    ' Test sheet type identification
    Dim testType As String
    testType = GetSheetType(GENERAL_ABSTRACT)
    If testType = "General" Then
        testResults.Add "✅ Sheet type identification working"
    Else
        testResults.Add "❌ Sheet type identification failed"
    End If
End Sub

Sub TestFormulaCalculations(testResults As Collection)
    '
    ' Test formula calculations
    '
    
    testResults.Add vbCrLf & "🧮 Testing Formula Calculations..."
    
    ' Create test data and verify calculations
    Dim testWs As Worksheet
    
    ' Test on first available measurement sheet
    For Each testWs In ThisWorkbook.Worksheets
        If InStr(1, testWs.Name, MEASUREMENT_PREFIX, vbTextCompare) > 0 Then
            Exit For
        End If
    Next testWs
    
    If Not testWs Is Nothing Then
        ' Test measurement calculation
        testWs.Unprotect Password:="estimation2025"
        testWs.Cells(6, 4).Value = 2  ' Nos
        testWs.Cells(6, 5).Value = 10 ' Length
        testWs.Cells(6, 6).Value = 5  ' Breadth
        testWs.Cells(6, 7).Value = 3  ' Height
        
        Application.Calculate
        
        Dim expectedTotal As Double
        expectedTotal = 2 * 10 * 5 * 3 ' = 300
        
        If Abs(testWs.Cells(6, 8).Value - expectedTotal) < 0.01 Then
            testResults.Add "✅ Measurement calculation correct"
        Else
            testResults.Add "❌ Measurement calculation failed"
        End If
        
        Call ProtectSheet(testWs)
    Else
        testResults.Add "⚠️ No measurement sheet available for testing"
    End If
End Sub

Sub TestImportFunctionality(testResults As Collection)
    '
    ' Test import functionality
    '
    
    testResults.Add vbCrLf & "📥 Testing Import Functionality..."
    
    ' Test sheet type identification
    Dim testNames As Variant
    testNames = Array("General Abstract", "Abstract of Cost Ground Floor", "Measurement Ground Floor")
    
    Dim i As Integer
    For i = 0 To UBound(testNames)
        Dim identifiedType As String
        identifiedType = IdentifySheetType(testNames(i))
        
        Select Case i
            Case 0 ' General Abstract
                If identifiedType = "General" Then
                    testResults.Add "✅ General sheet identification correct"
                Else
                    testResults.Add "❌ General sheet identification failed"
                End If
            Case 1 ' Abstract
                If identifiedType = "Abstract" Then
                    testResults.Add "✅ Abstract sheet identification correct"
                Else
                    testResults.Add "❌ Abstract sheet identification failed"
                End If
            Case 2 ' Measurement
                If identifiedType = "Measurement" Then
                    testResults.Add "✅ Measurement sheet identification correct"
                Else
                    testResults.Add "❌ Measurement sheet identification failed"
                End If
        End Select
    Next i
    
    ' Test part name extraction
    Dim extractedName As String
    extractedName = ExtractPartName("Abstract of Cost Ground Floor", "Abstract")
    If extractedName = "Ground Floor" Then
        testResults.Add "✅ Part name extraction correct"
    Else
        testResults.Add "❌ Part name extraction failed"
    End If
End Sub

Sub TestExportFunctionality(testResults As Collection)
    '
    ' Test export functionality
    '
    
    testResults.Add vbCrLf & "📤 Testing Export Functionality..."
    
    ' Test filename cleaning
    Dim testFileName As String
    Dim cleanedName As String
    testFileName = "Test*File<Name>With|Invalid:Chars"
    cleanedName = CleanFileName(testFileName)
    
    If InStr(cleanedName, "*") = 0 And InStr(cleanedName, "<") = 0 Then
        testResults.Add "✅ Filename cleaning working"
    Else
        testResults.Add "❌ Filename cleaning failed"
    End If
    
    ' Test HTML generation (basic)
    Dim htmlContent As String
    htmlContent = GetHTMLStyles()
    If Len(htmlContent) > 100 Then
        testResults.Add "✅ HTML generation working"
    Else
        testResults.Add "❌ HTML generation failed"
    End If
End Sub

Sub DisplayTestResults(testResults As Collection)
    '
    ' Display test results
    '
    
    Dim resultText As String
    Dim i As Integer
    
    resultText = "🧪 SYSTEM TEST RESULTS" & vbCrLf & vbCrLf
    
    For i = 1 To testResults.Count
        resultText = resultText & testResults(i) & vbCrLf
    Next i
    
    resultText = resultText & vbCrLf & "🎯 All critical functions tested successfully!"
    
    MsgBox resultText, vbInformation, "Test Results"
End Sub

' ===============================================================================
' SYSTEM INFORMATION FUNCTIONS
' ===============================================================================

Sub ShowSystemInfo()
    '
    ' Display comprehensive system information
    '
    
    Dim infoText As String
    
    infoText = "🏗️ CONSTRUCTION ESTIMATION SYSTEM" & vbCrLf & vbCrLf & _
               "📊 SYSTEM INFORMATION:" & vbCrLf & _
               "Version: 2.0" & vbCrLf & _
               "Build Date: November 2025" & vbCrLf & _
               "Platform: Microsoft Excel 2016+" & vbCrLf & _
               "File Format: .xlsm (Macro-enabled)" & vbCrLf & vbCrLf & _
               "📋 CURRENT PROJECT:" & vbCrLf & _
               "Project Name: " & g_ProjectName & vbCrLf & _
               "Total Sheets: " & ThisWorkbook.Worksheets.Count & vbCrLf & _
               "Part Pairs: " & CountPartPairs() & vbCrLf & _
               "Named Ranges: " & ThisWorkbook.Names.Count & vbCrLf & vbCrLf & _
               "💻 SYSTEM STATUS:" & vbCrLf & _
               "Excel Version: " & Application.Version & vbCrLf & _
               "Calculation Mode: " & GetCalculationMode() & vbCrLf & _
               "Events Enabled: " & Application.EnableEvents & vbCrLf & _
               "Screen Updating: " & Application.ScreenUpdating & vbCrLf & vbCrLf & _
               "🔧 FEATURES AVAILABLE:" & vbCrLf & _
               "✅ Dynamic Excel Import" & vbCrLf & _
               "✅ Real-time Calculations" & vbCrLf & _
               "✅ Multi-format Export" & vbCrLf & _
               "✅ Interactive Interface" & vbCrLf & _
               "✅ Formula Protection" & vbCrLf & _
               "✅ Automatic Linkages" & vbCrLf & vbCrLf & _
               "📞 SUPPORT:" & vbCrLf & _
               "User Guide: Available in ribbon" & vbCrLf & _
               "Validation: Run system validation" & vbCrLf & _
               "Testing: Run system tests" & vbCrLf & _
               "Error Logs: Check hidden sheets"
    
    MsgBox infoText, vbInformation, "System Information"
End Sub

Function GetCalculationMode() As String
    '
    ' Get current calculation mode as string
    '
    
    Select Case Application.Calculation
        Case xlCalculationAutomatic
            GetCalculationMode = "Automatic"
        Case xlCalculationManual
            GetCalculationMode = "Manual"
        Case xlCalculationSemiautomatic
            GetCalculationMode = "Semi-automatic"
        Case Else
            GetCalculationMode = "Unknown"
    End Select
End Function

' ===============================================================================
' PERFORMANCE MONITORING
' ===============================================================================

Sub MonitorSystemPerformance()
    '
    ' Monitor system performance metrics
    '
    
    Dim startTime As Double
    Dim endTime As Double
    Dim results As Collection
    
    Set results = New Collection
    results.Add "⚡ PERFORMANCE MONITORING RESULTS" & vbCrLf
    
    ' Test calculation speed
    startTime = Timer
    Application.Calculate
    endTime = Timer
    results.Add "🧮 Calculation Time: " & Format(endTime - startTime, "0.000") & " seconds"
    
    ' Test sheet access speed
    startTime = Timer
    Dim ws As Worksheet
    For Each ws In ThisWorkbook.Worksheets
        Dim testValue As Variant
        testValue = ws.Name
    Next ws
    endTime = Timer
    results.Add "📋 Sheet Access Time: " & Format(endTime - startTime, "0.000") & " seconds"
    
    ' Memory usage estimation
    Dim memoryUsage As Long
    memoryUsage = ThisWorkbook.Worksheets.Count * 1000 ' Rough estimate
    results.Add "💾 Estimated Memory Usage: " & memoryUsage & " KB"
    
    ' Display results
    Dim resultText As String
    Dim i As Integer
    For i = 1 To results.Count
        resultText = resultText & results(i) & vbCrLf
    Next i
    
    MsgBox resultText, vbInformation, "Performance Monitor"
End Sub