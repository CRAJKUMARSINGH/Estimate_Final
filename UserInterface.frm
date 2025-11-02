VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} frmMainInterface 
   Caption         =   "Construction Estimation System"
   ClientHeight    =   7200
   ClientLeft      =   45
   ClientTop       =   375
   ClientWidth     =   9600
   OleObjectBlob   =   "frmMainInterface.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "frmMainInterface"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

' ===============================================================================
' MAIN INTERFACE USER FORM
' ===============================================================================
' File: UserInterface.frm
' Purpose: Main interactive interface for Construction Estimation System
' ===============================================================================

Option Explicit

Private Sub UserForm_Initialize()
    '
    ' Initialize the main interface form
    '
    
    Me.Caption = "Construction Estimation System v2.0"
    Me.Width = 480
    Me.Height = 420
    
    ' Create all controls
    Call CreateInterfaceControls
    
    ' Update project name display
    Call UpdateProjectInfo
End Sub

Private Sub CreateInterfaceControls()
    '
    ' Create all form controls programmatically
    '
    
    Dim lblTitle As MSForms.Label
    Dim lblProject As MSForms.Label
    Dim txtProject As MSForms.TextBox
    Dim btnUpdateProject As MSForms.CommandButton
    
    ' Import/Export Group
    Dim lblImportExport As MSForms.Label
    Dim btnImport As MSForms.CommandButton
    Dim btnExportPDF As MSForms.CommandButton
    Dim btnExportMulti As MSForms.CommandButton
    
    ' Item Management Group
    Dim lblItemMgmt As MSForms.Label
    Dim btnAddItem As MSForms.CommandButton
    Dim btnDeleteItem As MSForms.CommandButton
    
    ' Part Management Group
    Dim lblPartMgmt As MSForms.Label
    Dim btnAddPart As MSForms.CommandButton
    Dim btnDeletePart As MSForms.CommandButton
    
    ' System Tools Group
    Dim lblSystemTools As MSForms.Label
    Dim btnRebuildFormulas As MSForms.CommandButton
    Dim btnProtectSheets As MSForms.CommandButton
    Dim btnHelp As MSForms.CommandButton
    
    ' Title
    Set lblTitle = Me.Controls.Add("Forms.Label.1", "lblTitle")
    With lblTitle
        .Caption = "🏗️ Construction Estimation System"
        .Font.Size = 16
        .Font.Bold = True
        .Left = 20
        .Top = 10
        .Width = 420
        .Height = 30
        .TextAlign = fmTextAlignCenter
        .ForeColor = RGB(44, 62, 80)
    End With
    
    ' Project Information
    Set lblProject = Me.Controls.Add("Forms.Label.1", "lblProject")
    With lblProject
        .Caption = "Project Name:"
        .Font.Bold = True
        .Left = 20
        .Top = 50
        .Width = 80
        .Height = 20
    End With
    
    Set txtProject = Me.Controls.Add("Forms.TextBox.1", "txtProject")
    With txtProject
        .Left = 110
        .Top = 50
        .Width = 250
        .Height = 20
        .Value = g_ProjectName
    End With
    
    Set btnUpdateProject = Me.Controls.Add("Forms.CommandButton.1", "btnUpdateProject")
    With btnUpdateProject
        .Caption = "Update"
        .Left = 370
        .Top = 50
        .Width = 60
        .Height = 20
    End With
    
    ' Import/Export Group
    Set lblImportExport = Me.Controls.Add("Forms.Label.1", "lblImportExport")
    With lblImportExport
        .Caption = "📁 Import & Export"
        .Font.Bold = True
        .Left = 20
        .Top = 90
        .Width = 200
        .Height = 20
        .ForeColor = RGB(52, 73, 94)
    End With
    
    Set btnImport = Me.Controls.Add("Forms.CommandButton.1", "btnImport")
    With btnImport
        .Caption = "📥 Import Sample Estimate"
        .Left = 20
        .Top = 115
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    Set btnExportPDF = Me.Controls.Add("Forms.CommandButton.1", "btnExportPDF")
    With btnExportPDF
        .Caption = "📄 Export to PDF"
        .Left = 240
        .Top = 115
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    Set btnExportMulti = Me.Controls.Add("Forms.CommandButton.1", "btnExportMulti")
    With btnExportMulti
        .Caption = "📦 Multi-Format Export"
        .Left = 130
        .Top = 160
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    ' Item Management Group
    Set lblItemMgmt = Me.Controls.Add("Forms.Label.1", "lblItemMgmt")
    With lblItemMgmt
        .Caption = "📝 Item Management"
        .Font.Bold = True
        .Left = 20
        .Top = 210
        .Width = 200
        .Height = 20
        .ForeColor = RGB(52, 73, 94)
    End With
    
    Set btnAddItem = Me.Controls.Add("Forms.CommandButton.1", "btnAddItem")
    With btnAddItem
        .Caption = "➕ Add New Item"
        .Left = 20
        .Top = 235
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    Set btnDeleteItem = Me.Controls.Add("Forms.CommandButton.1", "btnDeleteItem")
    With btnDeleteItem
        .Caption = "🗑️ Delete Selected Item"
        .Left = 240
        .Top = 235
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    ' Part Management Group
    Set lblPartMgmt = Me.Controls.Add("Forms.Label.1", "lblPartMgmt")
    With lblPartMgmt
        .Caption = "🏗️ Part Management"
        .Font.Bold = True
        .Left = 20
        .Top = 285
        .Width = 200
        .Height = 20
        .ForeColor = RGB(52, 73, 94)
    End With
    
    Set btnAddPart = Me.Controls.Add("Forms.CommandButton.1", "btnAddPart")
    With btnAddPart
        .Caption = "🏗️ Add New Part"
        .Left = 20
        .Top = 310
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    Set btnDeletePart = Me.Controls.Add("Forms.CommandButton.1", "btnDeletePart")
    With btnDeletePart
        .Caption = "🗂️ Delete Part"
        .Left = 240
        .Top = 310
        .Width = 200
        .Height = 35
        .Font.Size = 10
    End With
    
    ' System Tools Group
    Set lblSystemTools = Me.Controls.Add("Forms.Label.1", "lblSystemTools")
    With lblSystemTools
        .Caption = "🔧 System Tools"
        .Font.Bold = True
        .Left = 20
        .Top = 360
        .Width = 200
        .Height = 20
        .ForeColor = RGB(52, 73, 94)
    End With
    
    Set btnRebuildFormulas = Me.Controls.Add("Forms.CommandButton.1", "btnRebuildFormulas")
    With btnRebuildFormulas
        .Caption = "🔄 Rebuild Formulas"
        .Left = 20
        .Top = 385
        .Width = 130
        .Height = 30
        .Font.Size = 9
    End With
    
    Set btnProtectSheets = Me.Controls.Add("Forms.CommandButton.1", "btnProtectSheets")
    With btnProtectSheets
        .Caption = "🔒 Protect Sheets"
        .Left = 160
        .Top = 385
        .Width = 130
        .Height = 30
        .Font.Size = 9
    End With
    
    Set btnHelp = Me.Controls.Add("Forms.CommandButton.1", "btnHelp")
    With btnHelp
        .Caption = "❓ Help"
        .Left = 300
        .Top = 385
        .Width = 130
        .Height = 30
        .Font.Size = 9
    End With
End Sub

Private Sub UpdateProjectInfo()
    '
    ' Update project information display
    '
    
    If g_ProjectName = "" Then
        g_ProjectName = "Construction Estimate"
    End If
    
    Me.Controls("txtProject").Value = g_ProjectName
End Sub

' ===============================================================================
' EVENT HANDLERS
' ===============================================================================

Private Sub btnUpdateProject_Click()
    '
    ' Update project name
    '
    
    Dim newName As String
    newName = Trim(Me.Controls("txtProject").Value)
    
    If newName <> "" Then
        g_ProjectName = newName
        Call UpdateAllSheetHeaders
        MsgBox "Project name updated successfully!", vbInformation, "Update Complete"
    End If
End Sub

Private Sub btnImport_Click()
    '
    ' Import sample estimate
    '
    
    Me.Hide
    Call ImportSampleEstimate
    Call UpdateProjectInfo
    Me.Show
End Sub

Private Sub btnExportPDF_Click()
    '
    ' Export to PDF
    '
    
    Me.Hide
    Call ExportToPDF
    Me.Show
End Sub

Private Sub btnExportMulti_Click()
    '
    ' Multi-format export
    '
    
    Me.Hide
    Call ExportMultiFormat
    Me.Show
End Sub

Private Sub btnAddItem_Click()
    '
    ' Add new item
    '
    
    Me.Hide
    Call AddNewItem
    Me.Show
End Sub

Private Sub btnDeleteItem_Click()
    '
    ' Delete selected item
    '
    
    Me.Hide
    Call DeleteSelectedItem
    Me.Show
End Sub

Private Sub btnAddPart_Click()
    '
    ' Add new part
    '
    
    Me.Hide
    Call CreateNewPartPair
    Me.Show
End Sub

Private Sub btnDeletePart_Click()
    '
    ' Delete part
    '
    
    Me.Hide
    Call DeleteSelectedPart
    Me.Show
End Sub

Private Sub btnRebuildFormulas_Click()
    '
    ' Rebuild all formulas
    '
    
    Me.Hide
    
    Dim response As VbMsgBoxResult
    response = MsgBox("This will rebuild all formulas and linkages." & vbCrLf & _
                     "Continue?", vbYesNo + vbQuestion, "Rebuild Formulas")
    
    If response = vbYes Then
        Call RebuildAllFormulas
        MsgBox "All formulas rebuilt successfully!", vbInformation, "Rebuild Complete"
    End If
    
    Me.Show
End Sub

Private Sub btnProtectSheets_Click()
    '
    ' Protect all sheets
    '
    
    Call ProtectAllSheets
    MsgBox "All sheets protected successfully!", vbInformation, "Protection Applied"
End Sub

Private Sub btnHelp_Click()
    '
    ' Show help information
    '
    
    Call ShowSystemHelp
End Sub

' ===============================================================================
' HELPER FUNCTIONS
' ===============================================================================

Sub UpdateAllSheetHeaders()
    '
    ' Update project name in all sheet headers
    '
    
    Dim ws As Worksheet
    
    For Each ws In ThisWorkbook.Worksheets
        If ws.Range("A2").Value Like "PROJECT:*" Then
            ws.Range("A2").Value = "PROJECT: " & g_ProjectName
        End If
    Next ws
End Sub

Sub ShowSystemHelp()
    '
    ' Show comprehensive help information
    '
    
    Dim helpText As String
    
    helpText = "🏗️ CONSTRUCTION ESTIMATION SYSTEM HELP" & vbCrLf & vbCrLf & _
               "MAIN FUNCTIONS:" & vbCrLf & _
               "• Import Sample Estimate: Load existing Excel estimate files" & vbCrLf & _
               "• Export to PDF: Generate complete PDF report" & vbCrLf & _
               "• Multi-Format Export: Export in PDF, Excel, CSV, or HTML" & vbCrLf & vbCrLf & _
               "ITEM MANAGEMENT:" & vbCrLf & _
               "• Add New Item: Insert items in Abstract/Measurement sheets" & vbCrLf & _
               "• Delete Item: Remove selected items with formula updates" & vbCrLf & vbCrLf & _
               "PART MANAGEMENT:" & vbCrLf & _
               "• Add New Part: Create new Abstract+Measurement pair" & vbCrLf & _
               "• Delete Part: Remove complete part with confirmation" & vbCrLf & vbCrLf & _
               "SYSTEM TOOLS:" & vbCrLf & _
               "• Rebuild Formulas: Repair all linkages and calculations" & vbCrLf & _
               "• Protect Sheets: Lock formulas while allowing data entry" & vbCrLf & vbCrLf & _
               "KEYBOARD SHORTCUTS:" & vbCrLf & _
               "• Ctrl+Shift+I: Import Sample Estimate" & vbCrLf & _
               "• Ctrl+Shift+A: Add New Item" & vbCrLf & _
               "• Ctrl+Shift+P: Add New Part" & vbCrLf & _
               "• Ctrl+Shift+E: Export to PDF" & vbCrLf & vbCrLf & _
               "REAL-TIME FEATURES:" & vbCrLf & _
               "• Measurements automatically update Abstract quantities" & vbCrLf & _
               "• Abstract amounts automatically update General totals" & vbCrLf & _
               "• All calculations happen instantly without refresh" & vbCrLf & vbCrLf & _
               "For detailed instructions, see the User Guide document."
    
    MsgBox helpText, vbInformation, "System Help"
End Sub

' Show the main interface
Sub ShowMainInterface()
    frmMainInterface.Show
End Sub