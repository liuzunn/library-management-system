@echo off
chcp 936 >nul
title ֹͣ MySQL 8.0.44 - ͼ�����ϵͳʵ��
set "BIN=D:\Develop\MySQL\mysql-8.0.44-winx64\bin"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [��ʾ] MySQL ��ǰû�����С�
    goto END
)

echo ����ֹͣ MySQL ...
"%BIN%\mysqladmin.exe" -u root -p"%LIBRARY_DB_PASSWORD%" -h 127.0.0.1 --port=3306 shutdown 2>nul
timeout /t 2 /nobreak >nul

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if errorlevel 1 (
    echo [�ɹ�] MySQL ��ֹͣ��
) else (
    echo [����] �˿� 3306 ���ڼ��������ֶ����� mysqld.exe ���̡�
)

:END
pause
