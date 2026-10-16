@echo off
chcp 936 >nul
title 停止 MySQL 8.0.44 - 图书管理系统实验
set "BIN=D:\Develop\MySQL\mysql-8.0.44-winx64\bin"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [提示] MySQL 当前没有运行。
    goto END
)

echo 正在停止 MySQL ...
"%BIN%\mysqladmin.exe" -u root -p123456 -h 127.0.0.1 --port=3306 shutdown 2>nul
timeout /t 2 /nobreak >nul

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [成功] MySQL 已停止。
) else (
    echo [警告] 端口 3306 仍在监听，请手动结束 mysqld.exe 进程。
)

:END
pause
