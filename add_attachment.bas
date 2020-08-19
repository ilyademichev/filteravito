Attribute VB_Name = "add_attachment"
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

Public Sub LoadAttchm(sFilePath As String, query As String)

Dim w As DAO.Workspace, db As DAO.Database
Dim sSQL As String, sUpdate As String
Dim rst As DAO.Recordset


Set w = DBEngine.Workspaces(0)
Set db = w.Databases(0)
Set rst = db.OpenRecordset(query, dbOpenDynaset)
aFiles = FF_ListFilesInDir(sFilePath, "png")
   
On Error GoTo Err_Transaction
Debug.Print "Transaction started:adding attachments"
    w.BeginTrans
    rst.Edit
        Set attchField = rst.Fields("Att").Value
        For i = LBound(aFiles) To UBound(aFiles)
            attchField.AddNew
                attchField.Fields("FileData").LoadFromFile sFilePath + aFiles(i)
                Debug.Print "Adding file: "; aFiles(i)
            attchField.Update
        Next i
    rst.Update
    'db.Execute sSQL, dbFailOnError
    w.CommitTrans
Debug.Print "Transaction committed:adding attachments"
    rst.Close
    w.Close
    db.Close
    Exit Sub
Err_Transaction:
    Debug.Print Err.Description
    Debug.Print "Rollback"
    w.Rollback

Error_Handler_Exit:
    On Error Resume Next
    Exit Sub

Set w = Nothing
Set db = Nothing
Set rst = Nothing

End Sub





