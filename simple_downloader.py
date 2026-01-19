"""
Simple YouTube Downloader - No GUI Required
Use this if you prefer command-line interface
"""

import subprocess
import sys
import os

def install_yt_dlp():
    """Install yt-dlp if not already installed"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'yt-dlp'], check=True)
        print("✅ yt-dlp installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install yt-dlp")
        return False

def download_video(url, quality="best", output_dir="Downloads"):
    """Download YouTube video with specified quality"""
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Build command
        cmd = [
            'yt-dlp',
            '-f', f'best[height<={quality}]' if quality != 'best' else 'best',
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            url
        ]
        
        print(f"Downloading: {url}")
        print(f"Quality: {quality}")
        print(f"Output: {output_dir}")
        print("-" * 50)
        
        # Run download
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Download completed successfully!")
            return True
        else:
            print(f"❌ Download failed: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ yt-dlp not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("YouTube 4K Video Downloader - Simple Version")
    print("=" * 50)
    
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        print("✅ yt-dlp is already installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing yt-dlp...")
        if not install_yt_dlp():
            return
    
    print("\nEnter YouTube URL (or 'quit' to exit):")
    url = input("URL: ").strip()
    
    if url.lower() == 'quit':
        return
    
    if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
        print("❌ Please enter a valid YouTube URL")
        return
    
    print("\nSelect quality:")
    print("1. Best Quality (4K/8K)")
    print("2. 4K (2160p)")
    print("3. 1080p")
    print("4. 720p")
    print("5. 480p")
    
    choice = input("Choice (1-5): ").strip()
    
    quality_map = {
        '1': 'best',
        '2': '2160',
        '3': '1080',
        '4': '720',
        '5': '480'
    }
    
    quality = quality_map.get(choice, 'best')
    
    output_dir = input("Download folder (press Enter for 'Downloads'): ").strip()
    if not output_dir:
        output_dir = "Downloads"
    
    download_video(url, quality, output_dir)

if __name__ == "__main__":
    main()

