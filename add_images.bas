Option Compare Database
Public Function AddImageAttchm()
    Dim sFilePath As String
    Dim sSQL As String
    Dim sAttfieldName As String
    'name for photo field attachment
    sAttfieldName = "Фото"
    'root directory for images
    sFilePath = "C:\REALTYDB\avito_images_by_adv_id\"
    'check for folders
    folders = FF_ListFilesInDir(sFilePath)
    On Error Resume Next
    If IsError(UBound(folders)) Then
        Debug.Print "folders array is empty."
        Debug.Print "Skipping appending"
    Else
        For i = LBound(folders) To UBound(folders)
            sSQL = "SELECT * FROM [Запись] WHERE (Запись.[Номер объявления авито]) LIKE '" & folders(i) & "'"
            Call LoadAttchm(sAttfieldName, sFilePath & "\" & folders(i), "*", sSQL)
        Next
    End If
End Function





Public Function AddImageAttchmFunc()
    Call AddImageAttchm
End Function


