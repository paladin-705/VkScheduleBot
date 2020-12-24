Sub UnMergeCells()   
   Dim cc As Range, cm As Range, ccm As Range   
   For Each cc In ActiveSheet.UsedRange   
       If cc.MergeCells Then   
           If cc.MergeArea.Rows.Count > 1 Then   
               Set cm = Range(cc.MergeArea.Address)   
               cc.UnMerge   
               For Each ccm In cm.Rows   
                   ccm.Merge   
                   ccm = cm.Cells(1, 1)   
               Next ccm   
           End If   
       End If   
   Next cc   
   ActiveSheet.UsedRange.Rows.AutoFit   
   ActiveSheet.UsedRange.Columns.AutoFit   
   MsgBox "Конец!", vbInformation, "Конец"   
End Sub