@echo off
set PYTHON_EXE=%~dp0python-embed\python.exe
set PIP_EXE=%~dp0python-embed\Scripts\pip.exe

echo ========================================
echo   Virtual Camera - Setup
echo ========================================
echo.

echo [1/4] Checking Python environment...
"%PYTHON_EXE%" --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please check python-embed directory.
    pause
    exit /b 1
)
echo Python environment OK
echo.

echo [2/4] Installing Python dependencies...
"%PIP_EXE%" install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

echo [3/4] Creating sample images...
"%PYTHON_EXE%" create_sample_image.py
if errorlevel 1 (
    echo WARNING: Sample image creation failed (program will still work)
)
echo Sample images ready
echo.

echo [4/4] OBS Studio check...
echo.
echo ========================================
echo   IMPORTANT
echo ========================================
echo This program requires OBS Studio virtual camera.
echo If not installed, please follow these steps:
echo.
echo 1. Visit https://obsproject.com/download
echo 2. Download and install OBS Studio
echo 3. Start OBS Studio, click Tools -^> Virtual Camera -^> Start
echo 4. Close OBS Studio or keep it running
echo.
echo ========================================
echo.

echo Setup complete!
echo.
echo To run the program:
echo   run.bat
echo.
pause