@echo off
chcp 936 >nul
title 启动 MySQL 8.0.44 - 图书管理系统实验
set "BIN=D:\Develop\MySQL\mysql-8.0.44-winx64\bin"
set "INI=D:\Develop\MySQL\my.ini"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if not errorlevel 1 (
    echo [提示] MySQL 已经在运行，端口 3306 正在监听。
    goto END
)

if not exist "%BIN%\mysqld.exe" (
    echo [错误] 未找到 %BIN%\mysqld.exe
    goto END
)

echo 正在启动 MySQL 8.0.44 ...
start "" /b "%BIN%\mysqld.exe" --defaults-file="%INI%"

for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    netstat -ano | findstr ":3306 " | findstr LISTENING >nul
    if not errorlevel 1 goto OK
)
echo [错误] 启动超时，请查看 D:\Develop\MySQL\data\mysql-error.log
goto END

:OK
echo.
echo [成功] MySQL 已启动，监听 127.0.0.1:3306
echo         数据库：library_db      用户名：root      密码：123456
echo         可用 Navicat Premium 17 连接后查看。
echo.

:END
pause
