# -*- coding: utf-8 -*-
import io, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(r'C:\Users\LZ\Desktop\软工')

start = '''@echo off
chcp 936 >nul
title 启动 MySQL 8.0.44 - 图书管理系统实验
set "BIN=D:\\Develop\\MySQL\\mysql-8.0.44-winx64\\bin"
set "INI=D:\\Develop\\MySQL\\my.ini"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if not errorlevel 1 (
    echo [提示] MySQL 已经在运行，端口 3306 正在监听。
    goto END
)

if not exist "%BIN%\\mysqld.exe" (
    echo [错误] 未找到 %BIN%\\mysqld.exe
    goto END
)

echo 正在启动 MySQL 8.0.44 ...
start "" /b "%BIN%\\mysqld.exe" --defaults-file="%INI%"

for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    netstat -ano | findstr ":3306 " | findstr LISTENING >nul
    if not errorlevel 1 goto OK
)
echo [错误] 启动超时，请查看 D:\\Develop\\MySQL\\data\\mysql-error.log
goto END

:OK
echo.
echo [成功] MySQL 已启动，监听 127.0.0.1:3306
echo         数据库：library_db      用户名：root      密码：<见环境变量>
echo         可用 Navicat Premium 17 连接后查看。
echo.

:END
pause
'''

stop = '''@echo off
chcp 936 >nul
title 停止 MySQL 8.0.44 - 图书管理系统实验
set "BIN=D:\\Develop\\MySQL\\mysql-8.0.44-winx64\\bin"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [提示] MySQL 当前没有运行。
    goto END
)

echo 正在停止 MySQL ...
"%BIN%\\mysqladmin.exe" -u root -p"%LIBRARY_DB_PASSWORD%" -h 127.0.0.1 --port=3306 shutdown 2>nul
timeout /t 2 /nobreak >nul

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [成功] MySQL 已停止。
) else (
    echo [警告] 端口 3306 仍在监听，请手动结束 mysqld.exe 进程。
)

:END
pause
'''

for name, text in [('启动MySQL服务.bat', start), ('停止MySQL服务.bat', stop)]:
    p = ROOT / name
    p.write_text(text.replace(chr(10), chr(13) + chr(10)), encoding='gbk')
    print('written', p)
