@echo off
echo Installing YouTube 4K Video Downloader...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Installing yt-dlp...
pip install yt-dlp

echo.
echo Installation complete!
echo.
echo To run the application, use: python youtube_downloader.py
echo.
pause

