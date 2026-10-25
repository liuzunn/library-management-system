@echo off
chcp 936 >nul
title Æô¶¯ MySQL 8.0.44 - Í¼Êé¹ÜÀíÏµÍ³ÊµÑé
set "BIN=D:\Develop\MySQL\mysql-8.0.44-winx64\bin"
set "INI=D:\Develop\MySQL\my.ini"

netstat -ano | findstr ":3306 " | findstr LISTENING >nul
if not errorlevel 1 (
    echo [ÌáÊ¾] MySQL ÒÑ¾­ÔÚÔËÐÐ£¬¶Ë¿Ú 3306 ÕýÔÚ¼àÌý¡£
    goto END
)

if not exist "%BIN%\mysqld.exe" (
    echo [´íÎó] Î´ÕÒµ½ %BIN%\mysqld.exe
    goto END
)

echo ÕýÔÚÆô¶¯ MySQL 8.0.44 ...
start "" /b "%BIN%\mysqld.exe" --defaults-file="%INI%"

for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul
    netstat -ano | findstr ":3306 " | findstr LISTENING >nul
    if not errorlevel 1 goto OK
)
echo [´íÎó] Æô¶¯³¬Ê±£¬Çë²é¿´ D:\Develop\MySQL\data\mysql-error.log
goto END

:OK
echo.
echo [³É¹¦] MySQL ÒÑÆô¶¯£¬¼àÌý 127.0.0.1:3306
echo         Êý¾Ý¿â£ºlibrary_db      ÓÃ»§Ãû£ºroot      ÃÜÂë£º<Á¯ƒØÏ>
echo         ¿ÉÓÃ Navicat Premium 17 Á¬½Óºó²é¿´¡£
echo.

:END
pause
