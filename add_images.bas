Option Compare Database
Public Function AddImageAttchm()
    Dim sFilePath As String
    Dim sSQL As String
    Dim sAttfieldName As String
    'name for photo field attachment
    sAttfieldName = "Ð¤Ð¾Ñ‚Ð¾"
    'root directory for images
    sFilePath = "C:\REALTYDB\avito_images_by_adv_id\"
    'check for folders
    folders = FF_ListFilesInDir(sFilePath)
    For i = LBound(folders) To UBound(folders)
        sSQL = "SELECT * FROM [Çàïèñü] WHERE (Çàïèñü.[Íîìåð îáúÿâëåíèÿ àâèòî]) LIKE '" & folders(i) & "'"
        Call LoadAttchm(sAttfieldName, sFilePath & "\" & folders(i), "*", sSQL)
    Next
End Function





Public Function AddImageAttchmFunc()
    Call AddImageAttchm
End Function