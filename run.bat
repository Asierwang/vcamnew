@echo off
set PYTHON_EXE=%~dp0python-embed\python.exe

echo Starting Virtual Camera Controller...
echo.

"%PYTHON_EXE%" main.py

if errorlevel 1 (
    echo.
    echo Program error!
    echo.
    echo Please check:
    echo 1. Run setup.bat to install dependencies
    echo 2. Install and enable OBS Studio virtual camera
    echo.
    pause
)