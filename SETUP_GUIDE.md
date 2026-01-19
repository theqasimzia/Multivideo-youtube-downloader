# YouTube 4K Video Downloader - Setup Guide

## Option 1: Install Python (Recommended)

### Step 1: Download and Install Python

1. **Download Python 3.11+** from: https://www.python.org/downloads/
2. **Important**: During installation, check "Add Python to PATH"
3. **Verify installation** by opening a new Command Prompt and running:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Install Dependencies

```cmd
pip install yt-dlp
pip install Pillow
```

### Step 3: Run the Application

```cmd
python youtube_downloader.py
```

---

## Option 2: Portable Solution (No Python Installation Required)

If you prefer not to install Python, I can create a standalone executable version.

### Using PyInstaller (if Python is installed)

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed youtube_downloader.py
```

---

## Option 3: Alternative - Use yt-dlp Directly

You can download videos using yt-dlp directly from the command line:

### Install yt-dlp (if Python is available)
```cmd
pip install yt-dlp
```

### Download 4K Video
```cmd
yt-dlp -f "best[height<=2160]" "YOUTUBE_URL"
```

### Download Best Quality
```cmd
yt-dlp -f "best" "YOUTUBE_URL"
```

---

## Troubleshooting

### Python Not Found Error
- Make sure Python is installed from python.org
- Check "Add Python to PATH" during installation
- Restart Command Prompt after installation

### pip Not Found Error
- Python might not be in PATH
- Try: `python -m pip install yt-dlp`
- Or: `py -m pip install yt-dlp`

### GUI Not Working
- Install tkinter: `pip install tk`
- On Windows, tkinter should come with Python

---

## Quick Start (Once Python is Installed)

1. Open Command Prompt in this folder
2. Run: `pip install yt-dlp`
3. Run: `python youtube_downloader.py`
4. Paste YouTube URL and download!

---

## Features of This Downloader

- ✅ 4K/8K Video Support
- ✅ Modern GUI Interface
- ✅ Quality Selection (360p to 8K)
- ✅ Format Selection (MP4, MKV, WebM, AVI)
- ✅ Custom Download Path
- ✅ Real-time Progress
- ✅ Download Logging

