Option Compare Database

'---------------------------------------------------------------------------------------
' Procedure : FF_ListFilesInDir
' Author    : Daniel Pineault, CARDA Consultants Inc.
' Website   : http://www.cardaconsultants.com
' Purpose   : Return a list of files in a given directory
' Copyright : The following is release as Attribution-ShareAlike 4.0 International
'             (CC BY-SA 4.0) - https://creativecommons.org/licenses/by-sa/4.0/
' Req'd Refs: None required
'
' Input Variables:
' ~~~~~~~~~~~~~~~~
' sPath     : Full path of folder to examine with trailing \
' sFilter   : specific file extension to limmit search to, leave blank to list all files
'
' Usage:
' ~~~~~~
' FF_ListFilesInDir("C:\Users\Daniel\Documents\") 'List all the files
' FF_ListFilesInDir("C:\Users\Daniel\Documents\","xls") 'Only list Excel files
' FF_ListFilesInDir("C:\Users\Daniel\Documents\","doc") 'Only list Word files
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
Function FF_ListFilesInDir(sPath As String, Optional sFilter As String = "*") As Variant
    Dim aFiles()              As String
    Dim sFile                 As String
    Dim i                     As Long

    On Error GoTo Error_Handler

    If Right(sPath, 1) <> "\" Then sPath = sPath & "\"
    sFile = Dir(sPath & "*." & sFilter, vbDirectory)
    Do While sFile <> vbNullString
        If sFile <> "." And sFile <> ".." Then
            ReDim Preserve aFiles(i)
            aFiles(i) = sFile
            i = i + 1
        End If
        sFile = Dir     'Loop through the next file that was found
    Loop
    FF_ListFilesInDir = aFiles
 
Error_Handler_Exit:
    On Error Resume Next
    Exit Function
 
Error_Handler:
    MsgBox "The following error has occurred" & vbCrLf & vbCrLf & _
           "Error Number: " & Err.Number & vbCrLf & _
           "Error Source: FF_ListFilesInDir" & vbCrLf & _
           "Error Description: " & Err.Description & _
           Switch(Erl = 0, "", Erl <> 0, vbCrLf & "Line No: " & Erl) _
           , vbOKOnly + vbCritical, "An Error has Occurred!"
    Resume Error_Handler_Exit
End Function
