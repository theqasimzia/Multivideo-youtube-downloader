# 🎬 Multi-Video YouTube Downloader

A powerful, modern YouTube video downloader with queue management, browser extension support, and advanced features for downloading videos in 4K/8K quality or extracting audio in multiple formats.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ✨ Features

### 🎥 Video Download Capabilities
- **4K/8K Support**: Download videos in up to 8K Ultra HD quality
- **Multiple Quality Options**: Choose from 360p to 8K (360p, 480p, 720p, 1080p, 1440p, 2160p, Best Quality)
- **Format Support**: Download in MP4, MKV, WebM, or AVI formats
- **Custom Download Path**: Choose where to save your videos
- **Real-time Progress**: Live download progress tracking with percentage updates

### 🎵 Audio Extraction
- **Multiple Audio Formats**: Extract audio as MP3, M4A, WAV, or Opus
- **Audio Quality Selection**: Choose bitrate (128k, 192k, 256k, 320k)
- **Batch Audio Conversion**: Convert entire queue to audio format

### 📋 Queue Management System
- **Multiple Video Queue**: Add unlimited videos to download queue
- **Sequential Processing**: Downloads videos one by one automatically
- **Queue Status Tracking**: Real-time status updates (Queued, Downloading, Completed, Failed)
- **Auto-Download Option**: Automatically start downloading when videos are added to queue
- **Queue Controls**: Clear queue, pause/resume downloads
- **Video Title Extraction**: Automatically fetches and displays video titles

### 🌐 Browser Extension Integration
- **One-Click Download**: Click button in browser to add video to queue
- **Chrome Extension**: Works with Google Chrome
- **Firefox Extension**: Works with Mozilla Firefox
- **Real-time Sync**: Instant communication between browser and app
- **YouTube Integration**: Detects YouTube pages automatically

### 📚 Download History
- **Complete History**: Track all previous downloads with timestamps
- **Video Titles**: Shows actual video titles (not just URLs)
- **Status Tracking**: Success/failure status for each download
- **File Location Access**: Double-click to open download folder
- **Persistent Storage**: History saved between sessions

### 🛡️ VPN Optimization
- **Enhanced Retry Logic**: 10 retries for VPN stability
- **Larger Chunk Sizes**: Better for VPN connections
- **Parallel Downloads**: 4 concurrent fragments
- **Smart Error Detection**: Handles 403 Forbidden errors
- **Connection Management**: Better VPN drop handling

### 🎨 Modern UI/UX
- **Shadcn-Inspired Design**: Beautiful, modern interface
- **Dark Theme**: Professional dark color scheme
- **Responsive Layout**: Adapts to window resizing
- **Real-time Updates**: Live status and progress indicators
- **Professional Typography**: Modern fonts and spacing

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theqasimzia/Multivideo-youtube-downloader.git
   cd Multivideo-youtube-downloader
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python youtube_downloader_modern.py
   ```

### Windows Quick Install
Double-click `install.bat` to automatically install all dependencies.

## 📖 Usage

### Basic Video Download

1. **Launch the application**
2. **Paste YouTube URL** in the input field
3. **Select video quality** (4K, 1080p, etc.)
4. **Choose output format** (MP4, MKV, etc.)
5. **Click "Add to Queue"** or **"Download Now"**

### Queue Management

1. **Add Multiple Videos**: Paste URLs and click "Add to Queue" for each
2. **Start Queue**: Click "▶️ Start Queue" to begin downloading
3. **Auto-Download**: Enable "Auto-download" in settings to start automatically
4. **Monitor Progress**: Watch real-time progress in the queue panel

### Audio Extraction

1. **Select Format**: Choose "MP3 (Audio Only)" or other audio formats
2. **Select Quality**: Choose audio bitrate (128k, 192k, 256k, 320k)
3. **Add to Queue**: Add videos to convert to audio
4. **Start Download**: Begin audio extraction process

### Browser Extension

1. **Install Extension**: 
   - Chrome: Load unpacked extension from `browser_extension/chrome/`
   - Firefox: Load from `browser_extension/firefox/`
2. **Start App**: Make sure the Python app is running
3. **Browse YouTube**: Visit any YouTube video page
4. **Click Download**: Click the "Download" button on the page
5. **Auto-Add**: Video automatically added to queue

## 🎯 Supported URLs

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- YouTube playlists (with playlist support)

## 📁 Output Formats

### Video Formats
- **MP4**: Most compatible format (recommended)
- **MKV**: High-quality container format
- **WebM**: Web-optimized format
- **AVI**: Legacy format

### Audio Formats
- **MP3**: Most compatible audio format
- **M4A**: Apple-compatible format
- **WAV**: Uncompressed audio
- **Opus**: Modern, efficient format

## ⚙️ Configuration

### Settings Panel
- **Default Download Quality**: Set preferred quality
- **Default Download Path**: Set default save location
- **Auto-Download**: Enable automatic queue processing
- **VPN Optimization**: Configure VPN-specific settings
- **Notification Preferences**: Enable/disable notifications

### Configuration File
Settings are saved in `config.json` in the application directory.

## 🔧 Advanced Features

### VPN Optimization
The app includes built-in VPN optimization:
- Automatic retry on connection failures
- Larger buffer sizes for stability
- Parallel fragment downloads
- Smart error detection and recovery

### Queue Management
- **Sequential Downloads**: One video at a time for stability
- **Status Tracking**: Real-time status for each video
- **Error Handling**: Failed downloads don't stop the queue
- **Resume Support**: Can resume interrupted downloads

### History Management
- **Persistent History**: All downloads saved to `download_history.json`
- **Search Functionality**: Search through download history
- **Export History**: Export history to CSV
- **Clear History**: Option to clear download history

## 🌐 Browser Extension Setup

### Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `browser_extension/chrome/` folder
5. Extension is now installed!

### Firefox Extension
1. Open Firefox and go to `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Select `browser_extension/firefox/manifest.json`
5. Extension is now installed!

### API Server
The browser extension requires the Flask API server to be running:
```bash
python api_server.py
```

The server runs on `http://localhost:5000` by default.

## 📦 Packaging as EXE

### Using PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTubeDownloader" youtube_downloader_modern.py
```

The executable will be created in the `dist/` folder.

### Creating Installer
Use Inno Setup or NSIS to create a professional installer:
1. Build EXE using PyInstaller
2. Create installer script
3. Include all dependencies
4. Add desktop shortcut and start menu entry

## 🛠️ Development

### Project Structure
```
Multivideo-youtube-downloader/
├── youtube_downloader_modern.py    # Main application
├── api_server.py                   # Flask API for browser extension
├── browser_extension/              # Browser extension files
│   ├── chrome/                    # Chrome extension
│   └── firefox/                   # Firefox extension
├── requirements.txt                # Python dependencies
├── config.json                     # Configuration file
├── download_history.json          # Download history
└── README.md                       # This file
```

### Dependencies
- **yt-dlp**: YouTube video downloader
- **customtkinter**: Modern UI framework
- **Flask**: Web API for browser extension
- **requests**: HTTP requests
- **Pillow**: Image processing

## 🐛 Troubleshooting

### Common Issues

1. **"yt-dlp not found" error:**
   ```bash
   pip install yt-dlp
   ```

2. **Download fails:**
   - Check internet connection
   - Verify YouTube URL is correct
   - Some videos may be region-restricted
   - Try disabling VPN temporarily

3. **Browser extension not working:**
   - Make sure Flask API server is running
   - Check if app is listening on `localhost:5000`
   - Verify extension is enabled in browser

4. **GUI not working:**
   - Install tkinter: `python -m tkinter`
   - On Linux: `sudo apt-get install python3-tk`

### Performance Tips
- For 4K/8K downloads, ensure stable internet connection
- Large files may take significant time to download
- Consider available disk space for high-quality videos
- Use VPN optimization settings for better stability

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- **yt-dlp**: For the amazing YouTube downloader
- **CustomTkinter**: For the modern UI framework
- **Flask**: For the web API framework

## 🎉 Features Roadmap

- [x] Queue management system
- [x] Browser extension integration
- [x] Auto-download option
- [x] Multiple audio formats (MP3, M4A, WAV, Opus)
- [x] Modern UI with CustomTkinter
- [x] EXE packaging support
- [ ] Playlist download support
- [ ] Subtitle download
- [ ] Video thumbnail extraction
- [ ] Scheduled downloads
- [ ] Cloud storage integration

---

**Made with ❤️ for YouTube content creators and enthusiasts**