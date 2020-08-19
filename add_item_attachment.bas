Attribute VB_Name = "add_item_attachment"
Option Compare Database
Sub AddImageAttchm()
    Dim sFilePath As String
    Dim sSQL As String
    sFilePath = "C:\\REALTYDB\\123456789\\"
    sSQL = "SELECT * FROM Faculty WHERE Company Like '12345678'"
    Call LoadAttchm(sFilePath, sSQL)
End Sub

