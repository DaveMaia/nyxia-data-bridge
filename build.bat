@echo off
title Compilando Nyxia Data Bridge (.EXE)...
echo ============================================================
echo   NYXIA DATA BRIDGE - BUILD EXECUTAVEL STANDALONE (.EXE)
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
    --name "NyxiaDataBridge" ^
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
echo   Executavel standalone gerado em: dist\NyxiaDataBridge.exe
echo ============================================================
pause
