@echo off
echo YouTube 4K Video Downloader - Quick Setup
echo ==========================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
echo.

echo Installing yt-dlp...
python -m pip install yt-dlp

echo.
echo Installing GUI dependencies...
python -m pip install Pillow

echo.
echo Setup complete! Starting YouTube Downloader...
echo.

python youtube_downloader.py

pause

