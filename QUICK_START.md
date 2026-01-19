# 🚀 Quick Start Guide

## Installation

1. **Install Python 3.7+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or on Windows, simply double-click `install.bat`

## Running the Application

### Main Application
```bash
python youtube_downloader_modern.py
```

### API Server (for Browser Extension)
```bash
python api_server.py
```

## Browser Extension Setup

### Chrome
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `browser_extension/chrome/` folder

### Firefox
1. Open `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select `browser_extension/firefox/manifest.json`

## Building EXE

```bash
pip install pyinstaller
python build_exe.py
```

The executable will be in the `dist/` folder.

## Features

✅ **Modern UI** with CustomTkinter  
✅ **Queue Management** - Add multiple videos  
✅ **Auto-Download** - Automatic queue processing  
✅ **Audio Formats** - MP3, M4A, WAV, Opus  
✅ **Browser Extension** - One-click download from browser  
✅ **VPN Optimized** - Enhanced retry logic  
✅ **Download History** - Track all downloads  

## Need Help?

Check the main [README.md](README.md) for detailed documentation.
