Option Compare Database
Sub AddImageAttchm()
    Dim sFilePath As String
    Dim sSQL As String
    Dim sAttfieldName As String
    'name for photo field attachment
    sAttfieldName = "Ôîòî"
    'root directory for images
    sFilePath = "C:\REALTYDB\avito_images_by_adv_id\"
    'check for folders
    folders = FF_ListFilesInDir(sFilePath)
    For i = LBound(folders) To UBound(folders)
        sSQL = "SELECT * FROM Çàïèñü WHERE [Íîìåð îáúåâëåíèÿ àâèòî] Like '" & folders(i) & "'"
        Call LoadAttchm(sAttfieldName, sFilePath & "\" & folders(i), sSQL)
    Next
End Sub





Public Function AddImageAttchmFunc()
    Call AddImageAttchm
End Function


