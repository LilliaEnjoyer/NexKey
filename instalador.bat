@echo off
title Instalador CryptoVault - Modo Usuario
set PYTHON_PATH=%LocalAppData%\Programs\Python\Python314\python.exe

echo ====================================================
echo   INSTALANDO LIBRERIAS (RUTA DIRECTA)
echo ====================================================
echo.

:: Verificar si el archivo existe en esa ruta específica
if not exist "%PYTHON_PATH%" (
    echo [ERROR] No se encontro Python en la ruta: 
    echo %PYTHON_PATH%
    echo.
    echo Intenta buscar donde se instalo y cambia la ruta en este .bat
    pause
    exit
)

echo [+] Python detectado. Actualizando pip...
"%PYTHON_PATH%" -m pip install --upgrade pip

echo.
echo [+] Instalando dependencias...
"%PYTHON_PATH%" -m pip install customtkinter cryptography pillow --user

echo.
echo ====================================================
echo   PROCESO TERMINADO
echo ====================================================
pause