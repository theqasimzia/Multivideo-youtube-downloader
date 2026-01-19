import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
import webbrowser
import time

class YouTubeDownloaderUltra:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube 4K Video Downloader Ultra")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        self.root.minsize(1200, 800)
        
        # Set download path FIRST
        self.download_path = str(Path.home() / "Downloads")
        self.history_file = "download_history.json"
        self.download_history = self.load_history()
        self.download_process = None
        self.is_downloading = False
        
        # Windows 11 inspired color scheme
        self.colors = {
            'bg_primary': '#0d1117',      # GitHub dark
            'bg_secondary': '#161b22',     # Slightly lighter
            'bg_tertiary': '#21262d',     # Card background
            'bg_quaternary': '#30363d',    # Input backgrounds
            'accent_primary': '#238636',   # GitHub green
            'accent_secondary': '#1f6feb', # GitHub blue
            'accent_warning': '#d29922',   # GitHub yellow
            'accent_danger': '#da3633',    # GitHub red
            'text_primary': '#f0f6fc',     # Almost white
            'text_secondary': '#8b949e',   # Muted text
            'text_muted': '#6e7681',       # Very muted
            'border': '#30363d',          # Subtle borders
            'hover': '#262c36',           # Hover states
            'gradient_start': '#1a1a2e',   # Gradient start
            'gradient_end': '#16213e'     # Gradient end
        }
        
        self.setup_styles()
        self.setup_ui()
        self.setup_history_window()
        
    def setup_styles(self):
        """Setup Windows 11 inspired styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern styles
        style.configure('UltraTitle.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['accent_primary'],
                       font=('Segoe UI', 28, 'bold'))
        
        style.configure('UltraHeading.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('UltraSubheading.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('UltraBody.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 11))
        
        style.configure('UltraButton.TButton', 
                       background=self.colors['accent_primary'],
                       foreground='white',
                       font=('Segoe UI', 12, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12))
        
        style.map('UltraButton.TButton',
                 background=[('active', '#2ea043'),
                           ('pressed', '#238636')])
        
        style.configure('UltraSecondary.TButton', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11),
                       borderwidth=0,
                       padding=(15, 8))
        
        style.map('UltraSecondary.TButton',
                 background=[('active', self.colors['hover'])])
        
        style.configure('UltraEntry.TEntry', 
                       fieldbackground=self.colors['bg_quaternary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       insertcolor=self.colors['accent_primary'],
                       font=('Segoe UI', 11))
        
        style.configure('UltraCombobox.TCombobox', 
                       fieldbackground=self.colors['bg_quaternary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       font=('Segoe UI', 11))
        
        style.configure('UltraRadiobutton.TRadiobutton', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11),
                       focuscolor='none')
        
        # Progress bar styling removed to avoid compatibility issues
        
    def setup_ui(self):
        """Setup the ultra-modern UI"""
        # Main container with gradient-like effect
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header section with modern styling
        self.create_ultra_header(main_container)
        
        # Main content area with cards
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(25, 0))
        
        # Left panel - Download controls with card design
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                             relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Right panel - History and logs with card design
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], 
                              relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))
        
        # Setup panels
        self.create_ultra_download_panel(left_panel)
        self.create_ultra_history_panel(right_panel)
        
    def create_ultra_header(self, parent):
        """Create the ultra-modern header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Title with modern styling
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="🎬 YouTube 4K Video Downloader Ultra", 
                               style='UltraTitle.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator with modern design
        self.status_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        self.status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Label(self.status_frame, text="●", 
                                       fg=self.colors['accent_primary'], 
                                       bg=self.colors['bg_primary'],
                                       font=('Segoe UI', 20))
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready to Download", 
                                    style='UltraBody.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
    def create_ultra_download_panel(self, parent):
        """Create the ultra-modern download control panel"""
        # Panel header with card design
        header_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=50)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text="🚀 Download Configuration", 
                 style='UltraHeading.TLabel').pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content frame with padding
        content_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # URL input section with modern design
        self.create_ultra_url_section(content_frame)
        
        # Quality selection section
        self.create_ultra_quality_section(content_frame)
        
        # Format and path section
        self.create_ultra_format_section(content_frame)
        
        # Download button with modern design
        self.create_ultra_download_button(content_frame)
        
        # Progress section with modern styling
        self.create_ultra_progress_section(content_frame)
        
    def create_ultra_url_section(self, parent):
        """Create ultra-modern URL input section"""
        url_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        url_frame.pack(fill=tk.X, pady=(25, 20))
        
        ttk.Label(url_frame, text="🔗 YouTube URL", 
                 style='UltraSubheading.TLabel').pack(anchor=tk.W, padx=25, pady=(0, 8))
        
        url_input_frame = tk.Frame(url_frame, bg=self.colors['bg_secondary'])
        url_input_frame.pack(fill=tk.X, padx=25)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='UltraEntry.TEntry', font=('Segoe UI', 12))
        self.url_entry.pack(fill=tk.X, pady=(0, 8))
        
        # URL validation with modern styling
        self.url_status_label = ttk.Label(url_input_frame, text="", 
                                         style='UltraBody.TLabel')
        self.url_status_label.pack(anchor=tk.W)
        
        # Bind URL validation
        self.url_var.trace('w', self.validate_url)
        
    def create_ultra_quality_section(self, parent):
        """Create ultra-modern quality selection section"""
        quality_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        quality_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(quality_frame, text="🎯 Video Quality", 
                 style='UltraSubheading.TLabel').pack(anchor=tk.W, padx=25, pady=(0, 15))
        
        quality_options_frame = tk.Frame(quality_frame, bg=self.colors['bg_secondary'])
        quality_options_frame.pack(fill=tk.X, padx=25)
        
        self.quality_var = tk.StringVar(value="best")
        quality_options = [
            ("🏆 Best Quality (4K/8K)", "best"),
            ("📺 4K Ultra HD (2160p)", "2160"),
            ("📱 2K (1440p)", "1440"),
            ("💻 Full HD (1080p)", "1080"),
            ("📱 HD (720p)", "720"),
            ("📺 SD (480p)", "480"),
            ("📱 Low (360p)", "360")
        ]
        
        for i, (text, value) in enumerate(quality_options):
            rb = ttk.Radiobutton(quality_options_frame, text=text, 
                               variable=self.quality_var, value=value,
                               style='UltraRadiobutton.TRadiobutton')
            rb.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 25), pady=5)
        
    def create_ultra_format_section(self, parent):
        """Create ultra-modern format and path selection section"""
        format_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        format_frame.pack(fill=tk.X, pady=20)
        
        # Format selection
        format_row = tk.Frame(format_frame, bg=self.colors['bg_secondary'])
        format_row.pack(fill=tk.X, padx=25, pady=(0, 15))
        
        ttk.Label(format_row, text="📁 Output Format", 
                 style='UltraSubheading.TLabel').pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(format_row, textvariable=self.format_var, 
                                   values=["mp4", "mkv", "webm", "avi"], 
                                   style='UltraCombobox.TCombobox', state="readonly")
        format_combo.pack(side=tk.RIGHT)
        
        # Path selection
        path_row = tk.Frame(format_frame, bg=self.colors['bg_secondary'])
        path_row.pack(fill=tk.X, padx=25)
        
        ttk.Label(path_row, text="💾 Download Path", 
                 style='UltraSubheading.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        path_input_frame = tk.Frame(path_row, bg=self.colors['bg_secondary'])
        path_input_frame.pack(fill=tk.X)
        
        self.path_var = tk.StringVar(value=self.download_path)
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.path_var, 
                                   style='UltraEntry.TEntry')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        
        browse_btn = ttk.Button(path_input_frame, text="📂 Browse", 
                               command=self.browse_folder, style='UltraSecondary.TButton')
        browse_btn.pack(side=tk.RIGHT)
        
    def create_ultra_download_button(self, parent):
        """Create ultra-modern download button section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X, pady=25, padx=25)
        
        self.download_btn = ttk.Button(button_frame, text="🚀 Download Video", 
                                      command=self.start_download, style='UltraButton.TButton')
        self.download_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Quick actions with modern styling
        actions_frame = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="📋 View History", 
                  command=self.show_history, style='UltraSecondary.TButton').pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(actions_frame, text="⚙️ Settings", 
                  command=self.show_settings, style='UltraSecondary.TButton').pack(side=tk.LEFT)
        
    def create_ultra_progress_section(self, parent):
        """Create ultra-modern progress section"""
        progress_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill=tk.X, pady=(0, 25), padx=25)
        
        # Progress bar with modern styling
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Progress label with modern styling
        self.progress_label = ttk.Label(progress_frame, text="", 
                                       style='UltraBody.TLabel')
        self.progress_label.pack(anchor=tk.W)
        
    def create_ultra_history_panel(self, parent):
        """Create the ultra-modern history panel"""
        # Panel header with card design
        header_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=50)
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text="📚 Download History & Logs", 
                 style='UltraHeading.TLabel').pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content frame
        content_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # History list with modern styling
        self.create_ultra_history_list(content_frame)
        
        # Log section with modern styling
        self.create_ultra_log_section(content_frame)
        
    def create_ultra_history_list(self, parent):
        """Create ultra-modern download history list"""
        history_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(25, 15), padx=25)
        
        # History treeview with modern styling
        columns = ('Date', 'Title', 'Quality', 'Size', 'Status')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        
        # Configure columns with modern styling
        self.history_tree.heading('Date', text='📅 Date')
        self.history_tree.heading('Title', text='📺 Title')
        self.history_tree.heading('Quality', text='🎯 Quality')
        self.history_tree.heading('Size', text='💾 Size')
        self.history_tree.heading('Status', text='✅ Status')
        
        self.history_tree.column('Date', width=120)
        self.history_tree.column('Title', width=200)
        self.history_tree.column('Quality', width=80)
        self.history_tree.column('Size', width=80)
        self.history_tree.column('Status', width=80)
        
        # Scrollbar with modern styling
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to open file location
        self.history_tree.bind('<Double-1>', self.open_download_location)
        
    def create_ultra_log_section(self, parent):
        """Create ultra-modern log section"""
        log_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 25), padx=25)
        
        ttk.Label(log_frame, text="📋 Download Log", 
                 style='UltraSubheading.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        # Log text area with modern styling
        log_text_frame = tk.Frame(log_frame, bg=self.colors['bg_quaternary'], relief=tk.FLAT, bd=1)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=6, bg=self.colors['bg_quaternary'], 
                               fg=self.colors['text_primary'], font=('Consolas', 10),
                               wrap=tk.WORD, state=tk.DISABLED, bd=0)
        
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3, pady=3)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=3)
        
    def setup_history_window(self):
        """Setup the history window (initially hidden)"""
        self.history_window = None
        
    def validate_url(self, *args):
        """Validate YouTube URL with modern feedback"""
        url = self.url_var.get().strip()
        if not url:
            self.url_status_label.config(text="")
            return
        
        if url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            self.url_status_label.config(text="✅ Valid YouTube URL", 
                                       foreground=self.colors['accent_primary'])
        else:
            self.url_status_label.config(text="❌ Invalid URL format", 
                                       foreground=self.colors['accent_danger'])
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.path_var.set(folder)
            self.download_path = folder
    
    def log_message(self, message):
        """Add message to log with modern styling"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def update_status(self, message, color=None):
        """Update status indicator with modern styling"""
        self.status_label.config(text=message)
        if color:
            self.status_indicator.config(fg=color)
    
    def start_download(self):
        """Start download process with VPN handling"""
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
        self.update_status("Starting download...", self.colors['accent_warning'])
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        download_thread = threading.Thread(target=self.download_video_ultra, daemon=True)
        download_thread.start()
    
    def download_video_ultra(self):
        """Download video with VPN handling and retry logic"""
        try:
            url = self.url_var.get().strip()
            quality = self.quality_var.get()
            format_type = self.format_var.get()
            download_path = self.path_var.get()
            
            # Ensure download path exists
            os.makedirs(download_path, exist_ok=True)
            
            self.log_message("=" * 70)
            self.log_message("🚀 Starting YouTube Download (VPN Optimized)")
            self.log_message("=" * 70)
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
            
            # Build yt-dlp command with VPN-friendly options
            cmd = ['yt-dlp']
            
            # Format selection
            if quality == 'best':
                cmd.extend(['--format', 'best'])
            else:
                cmd.extend(['--format', f'best[height<={quality}]'])
            
            # Output template
            cmd.extend(['--output', f'{download_path}/%(title)s.%(ext)s'])
            
            # VPN-friendly options
            cmd.extend([
                '--no-playlist',
                '--verbose',
                '--retries', '10',                    # More retries for VPN issues
                '--fragment-retries', '10',           # Retry fragments
                '--socket-timeout', '30',             # Longer timeout
                '--http-chunk-size', '10485760',      # Larger chunks
                '--concurrent-fragments', '4',        # Parallel downloads
                '--buffer-size', '65536',             # Larger buffer
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'  # Better user agent
            ])
            
            if format_type != 'best':
                cmd.extend(['--merge-output-format', format_type])
            
            cmd.append(url)
            
            self.log_message("🔧 Command: " + ' '.join(cmd))
            self.log_message("")
            self.log_message("📥 Starting download with VPN optimization...")
            self.log_message("🛡️ Using retry logic for VPN stability...")
            self.log_message("-" * 50)
            
            # Execute download with process management
            self.is_downloading = True
            self.download_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=download_path,
                bufsize=1,
                shell=False
            )
            
            # Read output in real-time with VPN error handling
            output_lines = []
            error_count = 0
            max_errors = 5
            
            try:
                for line in self.download_process.stdout:
                    if not self.is_downloading:  # Check if download was cancelled
                        break
                        
                    line = line.strip()
                    if line:
                        output_lines.append(line)
                        self.log_message(line)
                        
                        # Handle VPN-related errors
                        if 'HTTP Error 403' in line or 'Forbidden' in line:
                            error_count += 1
                            self.log_message(f"🛡️ VPN Error detected (attempt {error_count}/{max_errors})")
                            if error_count >= max_errors:
                                self.log_message("❌ Too many VPN errors. Consider switching VPN servers.")
                                break
                        
                        # Update progress if we can parse it
                        if '[download]' in line and '%' in line:
                            try:
                                parts = line.split('%')[0].split()
                                if parts:
                                    percent = float(parts[-1])
                                    self.progress_var.set(percent)
                                    self.update_status(f"Downloading... {percent:.1f}%", self.colors['accent_warning'])
                            except:
                                pass
                        elif 'ERROR' in line.upper() or 'FAILED' in line.upper():
                            self.log_message(f"⚠️  WARNING: {line}")
                
                # Wait for process to complete
                if self.is_downloading:
                    return_code = self.download_process.wait()
                else:
                    return_code = -1  # Cancelled
                
            except Exception as e:
                self.log_message(f"❌ Error reading process output: {str(e)}")
                return_code = -1
            
            self.log_message("-" * 50)
            
            if return_code == 0 and self.is_downloading:
                self.update_status("✅ Download completed!", self.colors['accent_primary'])
                self.progress_var.set(100)
                self.log_message("🎉 SUCCESS: Video downloaded successfully!")
                self.log_message(f"📁 Saved to: {download_path}")
                
                # Add to history
                self.add_to_history(url, quality, format_type, "Success")
                
                messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {download_path}")
            else:
                if not self.is_downloading:
                    self.update_status("❌ Download cancelled", self.colors['accent_danger'])
                    self.log_message("🛑 Download was cancelled by user")
                else:
                    self.update_status("❌ Download failed!", self.colors['accent_danger'])
                    self.log_message("💥 FAILED: Download did not complete successfully")
                    self.log_message(f"🔍 Return code: {return_code}")
                    
                    # Add to history
                    self.add_to_history(url, quality, format_type, "Failed")
                    
                    if output_lines:
                        self.log_message("📋 Last few lines of output:")
                        for line in output_lines[-5:]:
                            self.log_message(f"   {line}")
                    
                    # VPN-specific error message
                    if error_count > 0:
                        messagebox.showerror("Download Failed", 
                            f"Download failed due to VPN issues.\n"
                            f"Try:\n"
                            f"• Switching VPN servers\n"
                            f"• Disabling VPN temporarily\n"
                            f"• Using a different VPN provider")
                    else:
                        messagebox.showerror("Download Failed", 
                            f"Download failed with return code {return_code}.\n"
                            f"Check the log for details.")
                
        except FileNotFoundError as e:
            self.log_message(f"❌ yt-dlp not found: {str(e)}")
            self.update_status("❌ yt-dlp not installed!", self.colors['accent_danger'])
            messagebox.showerror("yt-dlp Not Found", 
                "yt-dlp is not installed or not in PATH.\n"
                "Please run: python -m pip install yt-dlp")
        except Exception as e:
            self.log_message(f"💥 Unexpected error: {str(e)}")
            self.update_status("💥 Download failed!", self.colors['accent_danger'])
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            self.download_btn.config(state='normal')
            self.is_downloading = False
            self.download_process = None
    
    def add_to_history(self, url, quality, format_type, status):
        """Add download to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Try to get video title from URL (simplified)
        title = "Unknown Title"
        if "watch?v=" in url:
            title = f"Video {url.split('watch?v=')[1][:11]}"
        
        history_entry = {
            'timestamp': timestamp,
            'url': url,
            'title': title,
            'quality': quality,
            'format': format_type,
            'status': status,
            'size': 'Unknown'
        }
        
        self.download_history.append(history_entry)
        self.save_history()
        self.update_history_display()
    
    def update_history_display(self):
        """Update the history display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add recent entries (last 20)
        for entry in self.download_history[-20:]:
            status_icon = "✅" if entry['status'] == "Success" else "❌"
            self.history_tree.insert('', 'end', values=(
                entry['timestamp'],
                entry['title'][:30] + "..." if len(entry['title']) > 30 else entry['title'],
                entry['quality'],
                entry['size'],
                f"{status_icon} {entry['status']}"
            ))
    
    def open_download_location(self, event):
        """Open download location for selected item"""
        selection = self.history_tree.selection()
        if selection:
            item = self.history_tree.item(selection[0])
            timestamp = item['values'][0]
            
            # Find the corresponding history entry
            for entry in self.download_history:
                if entry['timestamp'] == timestamp:
                    # Open file explorer to download folder
                    os.startfile(self.download_path)
                    break
    
    def show_history(self):
        """Show detailed history window"""
        if self.history_window is None or not self.history_window.winfo_exists():
            self.history_window = tk.Toplevel(self.root)
            self.history_window.title("📚 Download History")
            self.history_window.geometry("900x700")
            self.history_window.configure(bg=self.colors['bg_primary'])
            
            # History list
            history_frame = tk.Frame(self.history_window, bg=self.colors['bg_secondary'])
            history_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
            
            # Treeview for detailed history
            columns = ('Date', 'URL', 'Title', 'Quality', 'Format', 'Status')
            history_tree = ttk.Treeview(history_frame, columns=columns, show='headings')
            
            for col in columns:
                history_tree.heading(col, text=col)
                history_tree.column(col, width=120)
            
            # Add all history entries
            for entry in reversed(self.download_history):  # Show newest first
                status_icon = "✅" if entry['status'] == "Success" else "❌"
                history_tree.insert('', 'end', values=(
                    entry['timestamp'],
                    entry['url'][:50] + "..." if len(entry['url']) > 50 else entry['url'],
                    entry['title'],
                    entry['quality'],
                    entry['format'],
                    f"{status_icon} {entry['status']}"
                ))
            
            history_tree.pack(fill=tk.BOTH, expand=True)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_tree.yview)
            history_tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def show_settings(self):
        """Show settings window"""
        messagebox.showinfo("Settings", "Settings panel coming soon!\n\nFeatures to be added:\n• Default download quality\n• Auto-download folder\n• VPN optimization settings\n• Notification preferences")
    
    def load_history(self):
        """Load download history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_history(self):
        """Save download history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.download_history, f, indent=2)
        except:
            pass

def main():
    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp is not installed. Please install it first:")
        print("pip install yt-dlp")
        return
    
    root = tk.Tk()
    app = YouTubeDownloaderUltra(root)
    
    # Load initial history
    app.update_history_display()
    
    root.mainloop()

if __name__ == "__main__":
    main()
