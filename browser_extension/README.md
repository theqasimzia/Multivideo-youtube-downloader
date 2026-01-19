# Browser Extension Setup Guide

## Chrome Extension Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `browser_extension/chrome/` folder
5. Extension is now installed!

## Firefox Extension Installation

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox" in the left sidebar
3. Click "Load Temporary Add-on"
4. Navigate to `browser_extension/firefox/` and select `manifest.json`
5. Extension is now installed!

## Usage

1. **Start the API Server**: Run `python api_server.py` in the main directory
2. **Browse YouTube**: Visit any YouTube video page
3. **Click Download**: Click the "⬇️ Download" button on the page
4. **Auto-Add**: Video is automatically added to your download queue

## Requirements

- Python Flask API server must be running on `http://localhost:5000`
- Main downloader app should be running to process the queue

## Troubleshooting

- **Button not appearing**: Make sure you're on a YouTube video page
- **Connection error**: Ensure `api_server.py` is running
- **Extension not loading**: Check browser console for errors
