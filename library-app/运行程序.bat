@echo off
chcp 936 >nul
title ͼ�����ϵͳ - ��������ʵ���
cd /d "%~dp0"

if not exist "target\library-app.jar" (
    echo ��û�б��룬�����Զ����� ...
    call "����.bat"
)

echo �����������ݿ� library_db ������ͼ�����ϵͳ ...
start "" javaw -Dfile.encoding=UTF-8 -cp "target\library-app.jar;lib\mysql-connector-java-8.0.28.jar" com.library.library.App
exit /b 0
