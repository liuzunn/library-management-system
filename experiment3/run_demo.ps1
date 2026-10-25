# -*- coding: utf-8 -*-
# 生成实验三 main() 的管道运行记录：_work/exp3_triangle_demo.txt
# 用法（在项目根目录执行）：powershell -ExecutionPolicy Bypass -File experiment3\run_demo.ps1
# 注意：本文件需以 UTF-8 BOM 保存，Windows PowerShell 5.1 才能正确解析中文。
$ErrorActionPreference = 'Continue'

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$JavaExe = 'D:\Develop\JDK21\bin\java.exe'
$ClassPath = Join-Path $ProjectRoot 'experiment3\out'
$OutFile = Join-Path $ProjectRoot '_work\exp3_triangle_demo.txt'
$MainClass = 'com.library.triangle.TriangleClassifier'

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
# 管道写入子进程的标准输入时不要带 BOM，否则首个整数会被解析成 "﻿3" 而报非整数
$OutputEncoding = New-Object System.Text.UTF8Encoding($false)

$scenarios = @(
    @{ Input = '3 4 5';       Note = '一般三角形：三边互不相等（勾股数）' },
    @{ Input = '5 5 5';       Note = '等边三角形：三边全等' },
    @{ Input = '5 5 8';       Note = '等腰三角形：两边相等' },
    @{ Input = '100 100 100'; Note = '等边三角形：三边均为上边界 100' },
    @{ Input = '1 2 3';       Note = '退化三角形：1+2=3，不构成三角形' },
    @{ Input = '1 1 2';       Note = '等腰退化：1+1=2，不构成三角形' },
    @{ Input = '0 3 4';       Note = '越界：0 不在 1~100 范围内' },
    @{ Input = '101 50 50';   Note = '越界：101 不在 1~100 范围内' },
    @{ Input = 'abc';         Note = '非整数输入：无法解析为整数' },
    @{ Input = '3 4';         Note = '输入个数不足：只读到 2 个整数' },
    @{ Input = '3 4 5 6';     Note = '输入个数过多：多出 1 个整数' }
)

$versionLine = (& $JavaExe -version 2>&1 | Select-Object -First 1)
$javaVersion = ($versionLine -replace '^java version "([^"]+)".*$', 'Java $1')

$rule = '=' * 72
$thin = '-' * 72
$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add($rule)
$lines.Add(' 实验三 三角形判定程序 —— main 运行记录（标准输入管道）')
$lines.Add($rule)
$lines.Add('运行环境 : ' + $javaVersion)
$lines.Add('项目根目录: ' + $ProjectRoot)
$lines.Add('调用方式 : <输入文本> | java -cp experiment3\out com.library.triangle.TriangleClassifier')
$lines.Add($thin)

$index = 0
foreach ($s in $scenarios) {
    $index++
    $lines.Add('【场景 ' + $index + '】' + $s.Note)
    $lines.Add('$ "' + $s.Input + '" | java -cp experiment3\out com.library.triangle.TriangleClassifier')
    $output = $s.Input | & $JavaExe '-Dstdout.encoding=UTF-8' '-Dstderr.encoding=UTF-8' -cp $ClassPath $MainClass 2>&1
    $exitCode = $LASTEXITCODE
    if ($null -eq $output) {
        $lines.Add('(无输出)')
    } else {
        foreach ($line in @($output)) { $lines.Add([string]$line) }
    }
    $lines.Add('[退出码] ' + $exitCode)
    $lines.Add($thin)
}

$total = $scenarios.Count
$lines.Add('场景总数: ' + $total + '（正常分类结果退出码 0，输入越界退出码 1，输入个数错误退出码 2，非整数退出码 3）')
$lines.Add($rule)

[System.IO.File]::WriteAllLines($OutFile, $lines, [System.Text.UTF8Encoding]::new($false))
Write-Output ('已生成: ' + $OutFile)
Write-Output ('场景数: ' + $total)
exit 0
