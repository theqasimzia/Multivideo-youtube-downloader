import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import subprocess
import sys
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube 4K Video Downloader")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Set download path FIRST before anything else
        self.download_path = str(Path.home() / "Downloads")
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white')
        style.configure('TButton', background='#4a4a4a', foreground='white')
        style.configure('TEntry', fieldbackground='#3a3a3a', foreground='white')
        style.configure('TCombobox', fieldbackground='#3a3a3a', foreground='white')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube 4K Video Downloader", 
                               font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # URL input frame
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_frame, text="YouTube URL:", font=('Arial', 12)).pack(anchor=tk.W)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, font=('Arial', 11))
        self.url_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Quality selection frame
        quality_frame = ttk.Frame(main_frame)
        quality_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(quality_frame, text="Video Quality:", font=('Arial', 12)).pack(anchor=tk.W)
        
        quality_options_frame = ttk.Frame(quality_frame)
        quality_options_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.quality_var = tk.StringVar(value="best")
        quality_options = [
            ("Best Quality (4K/8K)", "best"),
            ("4K (2160p)", "2160"),
            ("2K (1440p)", "1440"),
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480"),
            ("360p", "360")
        ]
        
        for i, (text, value) in enumerate(quality_options):
            ttk.Radiobutton(quality_options_frame, text=text, variable=self.quality_var, 
                          value=value).grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=2)
        
        # Format selection frame
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(format_frame, text="Download Format:", font=('Arial', 12)).pack(anchor=tk.W)
        
        self.format_var = tk.StringVar(value="mp4")
        format_options = ["mp4", "mkv", "webm", "avi"]
        
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                   values=format_options, state="readonly")
        format_combo.pack(anchor=tk.W, pady=(5, 0))
        
        # Download path frame
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(path_frame, text="Download Path:", font=('Arial', 12)).pack(anchor=tk.W)
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.path_var = tk.StringVar(value=self.download_path)
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(path_input_frame, text="Browse", 
                  command=self.browse_folder).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="Download Video", 
                                      command=self.start_download)
        self.download_btn.pack(pady=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to download")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.pack()
        
        # Log text area
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        ttk.Label(log_frame, text="Download Log:", font=('Arial', 12)).pack(anchor=tk.W)
        
        self.log_text = tk.Text(log_frame, height=8, bg='#1a1a1a', fg='white', 
                               font=('Consolas', 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.path_var.set(folder)
            self.download_path = folder
    
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        # Start download in a separate thread
        self.download_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("Starting download...")
        self.log_text.delete(1.0, tk.END)
        
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()
    
    def download_video(self):
        try:
            url = self.url_var.get().strip()
            quality = self.quality_var.get()
            format_type = self.format_var.get()
            download_path = self.path_var.get()
            
            # Ensure download path exists
            os.makedirs(download_path, exist_ok=True)
            
            self.log_message("=" * 50)
            self.log_message("🚀 Starting YouTube Download")
            self.log_message("=" * 50)
            self.log_message(f"📺 URL: {url}")
            self.log_message(f"🎯 Quality: {quality}")
            self.log_message(f"📁 Format: {format_type}")
            self.log_message(f"💾 Path: {download_path}")
            self.log_message("")
            
            # Check if yt-dlp is available
            try:
                result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, timeout=10)
                if result.returncode != 0:
                    raise FileNotFoundError("yt-dlp not found")
                self.log_message(f"✅ yt-dlp version: {result.stdout.strip()}")
            except Exception as e:
                self.log_message(f"❌ yt-dlp check failed: {str(e)}")
                self.log_message("💡 Try running: python -m pip install yt-dlp")
                raise
            
            # Build yt-dlp command
            cmd = ['yt-dlp']
            
            # Format selection
            if quality == 'best':
                cmd.extend(['--format', 'best'])
            else:
                cmd.extend(['--format', f'best[height<={quality}]'])
            
            # Output template
            cmd.extend(['--output', f'{download_path}/%(title)s.%(ext)s'])
            
            # Additional options
            cmd.extend([
                '--no-playlist',
                '--verbose'  # Add verbose output for better logging
            ])
            
            if format_type != 'best':
                cmd.extend(['--merge-output-format', format_type])
            
            cmd.append(url)
            
            self.log_message("🔧 Command: " + ' '.join(cmd))
            self.log_message("")
            self.log_message("📥 Starting download...")
            self.log_message("-" * 30)
            
            # Execute download
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=download_path,
                bufsize=1,
                shell=False
            )
            
            # Read output in real-time
            output_lines = []
            try:
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        output_lines.append(line)
                        self.log_message(line)
                        
                        # Update progress if we can parse it
                        if '[download]' in line and '%' in line:
                            try:
                                # Extract percentage from lines like "[download] 45.2% of 123.45MiB at 1.23MiB/s ETA 00:12"
                                parts = line.split('%')[0].split()
                                if parts:
                                    percent = float(parts[-1])
                                    self.progress_var.set(percent)
                                    self.status_var.set(f"Downloading... {percent:.1f}%")
                            except:
                                pass
                        elif 'ERROR' in line.upper() or 'FAILED' in line.upper():
                            self.log_message(f"⚠️  WARNING: {line}")
                
                # Wait for process to complete
                return_code = process.wait()
                
            except Exception as e:
                self.log_message(f"❌ Error reading process output: {str(e)}")
                return_code = -1
            
            self.log_message("-" * 30)
            
            if return_code == 0:
                self.status_var.set("✅ Download completed successfully!")
                self.progress_var.set(100)
                self.log_message("🎉 SUCCESS: Video downloaded successfully!")
                self.log_message(f"📁 Saved to: {download_path}")
                messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {download_path}")
            else:
                self.status_var.set("❌ Download failed!")
                self.log_message("💥 FAILED: Download did not complete successfully")
                self.log_message(f"🔍 Return code: {return_code}")
                
                # Show last few lines of output for debugging
                if output_lines:
                    self.log_message("📋 Last few lines of output:")
                    for line in output_lines[-5:]:
                        self.log_message(f"   {line}")
                
                messagebox.showerror("Download Failed", 
                    f"Download failed with return code {return_code}.\n"
                    f"Check the log for details.\n"
                    f"Common issues:\n"
                    f"• Invalid URL\n"
                    f"• Video is private/restricted\n"
                    f"• Network connection issues")
                
        except FileNotFoundError as e:
            self.log_message(f"❌ yt-dlp not found: {str(e)}")
            self.log_message("💡 Solution: Run 'python -m pip install yt-dlp'")
            self.status_var.set("❌ yt-dlp not installed!")
            messagebox.showerror("yt-dlp Not Found", 
                "yt-dlp is not installed or not in PATH.\n"
                "Please run: python -m pip install yt-dlp")
        except subprocess.TimeoutExpired:
            self.log_message("⏰ Download timed out")
            self.status_var.set("⏰ Download timed out!")
            messagebox.showerror("Timeout", "Download timed out. Please try again.")
        except Exception as e:
            self.log_message(f"💥 Unexpected error: {str(e)}")
            self.status_var.set("💥 Download failed!")
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            self.download_btn.config(state='normal')

def main():
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp is not installed. Please install it first:")
        print("pip install yt-dlp")
        return
    
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
