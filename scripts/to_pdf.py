# -*- coding: utf-8 -*-
"""用 Word COM 把实验报告 DOCX 导出为 PDF。"""
import io, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(r'C:\Users\LZ\Desktop\软工')
DOCX = ROOT / '实验报告（上机）-图书管理系统数据库设计.docx'
PDF = ROOT / '实验报告（上机）-图书管理系统数据库设计.pdf'
ps = '$ErrorActionPreference = "Stop"\n' \
     '$word = New-Object -ComObject Word.Application\n' \
     '$word.Visible = $false\n' \
     '$word.DisplayAlerts = 0\n' \
     '$doc = $word.Documents.Open("' + str(DOCX) + '", $false, $true)\n' \
     '$doc.ExportAsFixedFormat("' + str(PDF) + '", 17)\n' \
     'Write-Output ("pages=" + $doc.ComputeStatistics(2))\n' \
     '$doc.Close($false)\n' \
     '$word.Quit()\n'
sp = ROOT / '_work' / 'conv2.ps1'
sp.write_text(ps, encoding='utf-8-sig')
print('ok')
