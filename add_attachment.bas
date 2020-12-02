Option Compare Database



'---------------------------------------------------------------------------------------
' Procedure : LoadAttchm
' Author    : Ilya Demichev
' Purpose   : Attach files to Attch field into the table by given ref
'
' Input Variables:
' ~~~~~~~~~~~~~~~~
' sPath     : Full path of folder to examine with trailing \
' sFilter   : specific file extension to limmit search to, leave blank to list all files
'
' Usage:
' ~~~~~~

'
' Revision History:
' Rev       Date(yyyy/mm/dd)        Description
' **************************************************************************************
' 1         2012-Jul-13             Initial Release
' 2         2019-02-03              Updated copyright & function header
'                                   Changed function name to follow naming convention
'                                   Added \ check in sPath string
'                                   Changed the function to return an array of the files
'---------------------------------------------------------------------------------------

Function IsArrayAllocated(Arr As Variant) As Boolean
        On Error Resume Next
        IsArrayAllocated = IsArray(Arr) And _
                           Not IsError(LBound(Arr, 1)) And _
                           LBound(Arr, 1) <= UBound(Arr, 1)
End Function

Public Function GetLength(a As Variant) As Integer
   On Error Resume Next
   If IsEmpty(a) Then
      GetLength = 0
   Else
      GetLength = UBound(a) - LBound(a) + 1
   End If
End Function

Public Sub LoadAttchm(sAttfieldName As String, sFilePath As String, attch_format As String, query As String)

Dim w As DAO.Workspace, db As DAO.Database
Dim sSQL As String, sUpdate As String
Dim rst As DAO.Recordset

Set w = DBEngine.Workspaces(0)
Set db = w.Databases(0)
Set rst = db.OpenRecordset(query, dbOpenDynaset)
aFiles = FF_ListFilesInDir(sFilePath, attch_format)
'check if it's empty
If GetLength(aFiles) = 0 Then
    Debug.Print "Folder " + sFilePath + " contains no " + attch_format + " files"
    Debug.Print "Skipping folder."
    ' return on nothing to add
    Exit Sub
End If
On Error GoTo Err_Transaction
Debug.Print "Transaction started:adding attachments"
' initiate the transaction
    w.BeginTrans
    rst.Edit
    ' field to add attachments
        Set attchField = rst.Fields(sAttfieldName).Value
        For i = LBound(aFiles) To UBound(aFiles)
        ' error while adding attachments
        On Error GoTo Err_AddAtchm
            attchField.AddNew
                attchField.Fields("FileData").LoadFromFile sFilePath + aFiles(i)
                Debug.Print "Adding file: "; aFiles(i)
            attchField.Update
        ' Error handler for adding attachments
Err_AddAtchm:
        Debug.Print Err.Description
        ' continue looping over attachments
    Resume NextAttchm
NextAttchm:
        Next i
    rst.Update
    'db.Execute sSQL, dbFailOnError
' commit the transaction
    w.CommitTrans
    ' successfull completion of transaction
    Debug.Print "Transaction committed:adding attachments"
    ' disposing
    rst.Close
    w.Close
    db.Close
    ' successfull transaction return
    Exit Sub
    ' general transactional error handler
Err_Transaction:
    Debug.Print Err.Description
    Debug.Print "Rollback"
    ' restoring the original state
    w.Rollback
    ' disposing
    rst.Close
    w.Close
    db.Close
    ' failed transaction return
    Exit Sub

Error_Handler_Exit:
    On Error Resume Next
    Exit Sub

Set w = Nothing
Set db = Nothing
Set rst = Nothing

End Sub