import subprocess
import os

def test_download():
    url = "https://www.youtube.com/watch?v=PyxBVuiq2NY"
    download_path = r"C:\Users\WIN-10\Downloads"
    
    print(f"Testing download to: {download_path}")
    print(f"URL: {url}")
    
    # Ensure directory exists
    os.makedirs(download_path, exist_ok=True)
    
    # Build command
    cmd = [
        'yt-dlp',
        '--format', 'best',
        '--output', f'{download_path}/%(title)s.%(ext)s',
        '--no-playlist',
        '--verbose',
        url
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print("Starting download...")
    
    try:
        # Execute download
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=download_path,
            bufsize=1
        )
        
        # Read output in real-time
        for line in process.stdout:
            line = line.strip()
            if line:
                print(f"OUTPUT: {line}")
        
        # Wait for process to complete
        return_code = process.wait()
        
        print(f"Return code: {return_code}")
        
        if return_code == 0:
            print("✅ Download successful!")
        else:
            print("❌ Download failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_download()
