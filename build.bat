@echo off
chcp 65001 >nul
set PYTHON_EXE=%~dp0python-embed\python.exe

echo ========================================
echo   Virtual Camera - Build Script
echo ========================================
echo.

echo [1/4] Checking environment...
"%PYTHON_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo Python OK
echo.

echo [2/4] Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Clean complete
echo.

echo [3/4] Building executable...
"%PYTHON_EXE%" -m PyInstaller --onefile ^
    --windowed ^
    --name "VirtualCamera" ^
    --icon camera_icon.ico ^
    --add-data "camera_icon.ico;." ^
    --distpath build ^
    --workpath build/temp ^
    --noconfirm ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Copying resources...
if not exist build\resources mkdir build\resources
copy sample_*.png build\resources\ >nul
echo Resources copied
echo.

echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Output: build\VirtualCamera.exe
echo.
echo Note: This program requires OBS Studio
echo with Virtual Camera enabled to work.
echo.
echo Download OBS: https://obsproject.com/download
echo.
pause