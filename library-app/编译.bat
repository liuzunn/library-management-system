@echo off
chcp 936 >nul
title ���� ͼ�����ϵͳ
cd /d "%~dp0"
set "JAR=lib\mysql-connector-java-8.0.28.jar"

echo [1/4] ׼��Ŀ¼ ...
if not exist "target\classes" mkdir "target\classes"
if not exist "lib" mkdir "lib"
if not exist "%JAR%" (
    echo [����] �Ҳ��� %JAR%
    echo        ��� mysql-connector-java-8.0.28.jar �ŵ� lib Ŀ¼�¡�
    pause & exit /b 1
)

echo [2/4] ���� Java Դ�ļ� ...
dir /s /b "src\main\java\*.java" > "target\sources.txt"
javac -encoding UTF-8 -d "target\classes" -cp "%JAR%" @"target\sources.txt"
if errorlevel 1 ( echo [����] ����ʧ�ܡ� & pause & exit /b 1 )

echo [3/4] ������Դ�ļ� ...
xcopy "src\main\resources\*" "target\classes\" /E /Y /Q >nul

echo [4/4] ��� library-app.jar ...
jar --create --file "target\library-app.jar" --main-class com.library.App -C "target\classes" .
if errorlevel 1 ( echo [����] ���ʧ�ܡ� & pause & exit /b 1 )

echo.
echo [�ɹ�] ��������ɣ� target\library-app.jar
pause
