' ===============================================================================
' MAIN INTERFACE USER FORM
' ===============================================================================
' File: UserForm_MainInterface.frm
' Purpose: Main interface form for Construction Estimation System
' ===============================================================================

VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} frmMainInterface 
   Caption         =   "Construction Estimation System"
   ClientHeight    =   7000
   ClientLeft      =   45
   ClientTop       =   375
   ClientWidth     =   8400
   OleObjectBlob   =   "frmMainInterface.frx":0000
   StartUpPosition =   1  'CenterOwner
End

' Form Code
Private Sub UserForm_Initialize()
    '
    ' Initialize the main interface form
    '
    
    Me.Caption = "Construction Estimation System v2.0"
    
    ' Setup form properties
    Me.Width = 420
    Me.Height = 450
    
    ' Create controls programmatically
    Call CreateFormControls
End Sub

Private Sub CreateFormControls()
    '
    ' Create all form controls
    '
    
    Dim btnImport As MSForms.CommandButton
    Dim btnImportAttached As MSForms.CommandButton
    Dim btnImportSSR As MSForms.CommandButton
    Dim btnAddItem As MSForms.CommandButton
    Dim btnAddMeasurement As MSForms.CommandButton
    Dim btnDeleteItem As MSForms.CommandButton
    Dim btnAddPart As MSForms.CommandButton
    Dim btnDeletePart As MSForms.CommandButton
    Dim btnUpdateMeasurements As MSForms.CommandButton
    Dim btnExportPDF As MSForms.CommandButton
    Dim btnExportMulti As MSForms.CommandButton
    Dim btnImportWhole As MSForms.CommandButton
    Dim lblTitle As MSForms.Label
    
    ' Title Label
    Set lblTitle = Me.Controls.Add("Forms.Label.1", "lblTitle")
    With lblTitle
        .Caption = "Construction Estimation System"
        .Font.Size = 14
        .Font.Bold = True
        .Left = 20
        .Top = 10
        .Width = 360
        .Height = 25
        .TextAlign = fmTextAlignCenter
    End With
    
    ' Import Sample Estimate Button
    Set btnImport = Me.Controls.Add("Forms.CommandButton.1", "btnImport")
    With btnImport
        .Caption = "Import Sample Estimate"
        .Left = 20
        .Top = 50
        .Width = 160
        .Height = 35
    End With
    
    ' Import From Attached Assets Button
    Set btnImportAttached = Me.Controls.Add("Forms.CommandButton.1", "btnImportAttached")
    With btnImportAttached
        .Caption = "Import From Attached"
        .Left = 200
        .Top = 50
        .Width = 160
        .Height = 35
    End With
    
    ' Add New Item Button
    Set btnAddItem = Me.Controls.Add("Forms.CommandButton.1", "btnAddItem")
    With btnAddItem
        .Caption = "Add New Item"
        .Left = 20
        .Top = 100
        .Width = 160
        .Height = 35
    End With
    
    ' Add New Measurement Line Button
    Set btnAddMeasurement = Me.Controls.Add("Forms.CommandButton.1", "btnAddMeasurement")
    With btnAddMeasurement
        .Caption = "Add Measurement Line"
        .Left = 200
        .Top = 100
        .Width = 160
        .Height = 35
    End With
    
    ' Delete Item Button
    Set btnDeleteItem = Me.Controls.Add("Forms.CommandButton.1", "btnDeleteItem")
    With btnDeleteItem
        .Caption = "Delete Selected Item"
        .Left = 20
        .Top = 150
        .Width = 160
        .Height = 35
    End With
    
    ' Update All Measurements Button
    Set btnUpdateMeasurements = Me.Controls.Add("Forms.CommandButton.1", "btnUpdateMeasurements")
    With btnUpdateMeasurements
        .Caption = "Update Measurements"
        .Left = 200
        .Top = 150
        .Width = 160
        .Height = 35
    End With
    
    ' Add New Part Button
    Set btnAddPart = Me.Controls.Add("Forms.CommandButton.1", "btnAddPart")
    With btnAddPart
        .Caption = "Add New Part"
        .Left = 20
        .Top = 200
        .Width = 160
        .Height = 35
    End With
    
    ' Delete Part Button
    Set btnDeletePart = Me.Controls.Add("Forms.CommandButton.1", "btnDeletePart")
    With btnDeletePart
        .Caption = "Delete Part"
        .Left = 200
        .Top = 200
        .Width = 160
        .Height = 35
    End With
    
    ' Import SSR Button
    Set btnImportSSR = Me.Controls.Add("Forms.CommandButton.1", "btnImportSSR")
    With btnImportSSR
        .Caption = "Import SSR Data"
        .Left = 20
        .Top = 250
        .Width = 160
        .Height = 35
    End With
    
    ' Import Whole Estimate Button
    Set btnImportWhole = Me.Controls.Add("Forms.CommandButton.1", "btnImportWhole")
    With btnImportWhole
        .Caption = "Import Whole Estimate"
        .Left = 200
        .Top = 250
        .Width = 160
        .Height = 35
    End With
    
    ' Export to PDF Button
    Set btnExportPDF = Me.Controls.Add("Forms.CommandButton.1", "btnExportPDF")
    With btnExportPDF
        .Caption = "Export to PDF"
        .Left = 20
        .Top = 300
        .Width = 160
        .Height = 35
    End With
    
    ' Multi-Format Export Button
    Set btnExportMulti = Me.Controls.Add("Forms.CommandButton.1", "btnExportMulti")
    With btnExportMulti
        .Caption = "Multi-Format Export"
        .Left = 200
        .Top = 300
        .Width = 160
        .Height = 35
    End With
End Sub

' Event Handlers
Private Sub btnImport_Click()
    Me.Hide
    Call ImportSampleEstimate
End Sub

Private Sub btnImportAttached_Click()
    Me.Hide
    Call ImportEstimateFromAttachedAssets
End Sub

Private Sub btnAddItem_Click()
    Me.Hide
    Call AddNewItem
End Sub

Private Sub btnAddMeasurement_Click()
    Me.Hide
    Call AddNewLineToMeasurements
End Sub

Private Sub btnDeleteItem_Click()
    Me.Hide
    Call DeleteSelectedItem
End Sub

Private Sub btnUpdateMeasurements_Click()
    Me.Hide
    Call UpdateAllMeasurements
End Sub

Private Sub btnAddPart_Click()
    Me.Hide
    Call CreateNewPart
End Sub

Private Sub btnDeletePart_Click()
    Me.Hide
    Call DeleteSelectedPart
End Sub

Private Sub btnImportSSR_Click()
    Me.Hide
    Call ImportSSRFromExcel
End Sub

Private Sub btnImportWhole_Click()
    Me.Hide
    Call ImportWholeEstimate
End Sub

Private Sub btnExportPDF_Click()
    Me.Hide
    Call ExportEstimateToPDF
End Sub

Private Sub btnExportMulti_Click()
    Me.Hide
    Call ExportEstimateMultiFormat
End Sub

' Show the main interface
Sub ShowMainInterface()
    frmMainInterface.Show
End Sub