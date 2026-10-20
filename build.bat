@echo off
title Compilando Data Bridge (.EXE)...
echo ============================================================
echo   DATA BRIDGE - BUILD EXECUTAVEL STANDALONE (.EXE)
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Verificando dependencias...
py -3.11 -m pip install customtkinter py7zr psutil pyinstaller pillow --quiet

echo [2/2] Empacotando executavel standalone (.exe individual)...
py -3.11 -m PyInstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "DataBridge" ^
    --icon "app_icon.ico" ^
    --add-data "nyxia_logo.png;." ^
    --add-data "header_icon.png;." ^
    --add-data "app_icon.ico;." ^
    --add-data "app_icon.png;." ^
    --collect-all customtkinter ^
    --collect-all py7zr ^
    app.py

echo.
echo ============================================================
echo   BUILD FINALIZADO COM SUCESSO!
echo   Executavel standalone gerado em: dist\DataBridge.exe
echo ============================================================
pause
