"""
PyInstaller build script for creating executable
Run: python build_exe.py
"""

import PyInstaller.__main__
import os
import sys

# Build arguments
args = [
    'youtube_downloader_modern.py',
    '--onefile',
    '--windowed',
    '--name=YouTubeDownloader',
    '--icon=NONE',  # Add icon path if you have one
    '--add-data=config.json;.',
    '--hidden-import=customtkinter',
    '--hidden-import=flask',
    '--hidden-import=flask_cors',
    '--collect-all=customtkinter',
    '--collect-all=flask',
    '--noconsole',
    '--clean'
]

print("🔨 Building executable with PyInstaller...")
print("This may take a few minutes...")

try:
    PyInstaller.__main__.run(args)
    print("\n✅ Build complete!")
    print("📦 Executable created in: dist/YouTubeDownloader.exe")
except Exception as e:
    print(f"\n❌ Build failed: {e}")
    sys.exit(1)
