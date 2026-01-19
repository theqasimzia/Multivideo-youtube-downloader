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

class YouTubeDownloaderPremium:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube 4K Video Downloader Premium")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0a0a0a')
        self.root.minsize(1000, 700)
        
        # Set download path FIRST
        self.download_path = str(Path.home() / "Downloads")
        self.history_file = "download_history.json"
        self.download_history = self.load_history()
        
        # Modern color scheme
        self.colors = {
            'bg_primary': '#0a0a0a',
            'bg_secondary': '#1a1a1a',
            'bg_tertiary': '#2a2a2a',
            'accent': '#00d4ff',
            'accent_hover': '#0099cc',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_muted': '#888888'
        }
        
        self.setup_styles()
        self.setup_ui()
        self.setup_history_window()
        
    def setup_styles(self):
        """Setup modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('Heading.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Body.TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 10))
        
        style.configure('Modern.TButton', 
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['accent_hover']),
                           ('pressed', self.colors['accent_hover'])])
        
        style.configure('Secondary.TButton', 
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       borderwidth=0)
        
        style.configure('Modern.TEntry', 
                       fieldbackground=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       insertcolor=self.colors['accent'])
        
        style.configure('Modern.TCombobox', 
                       fieldbackground=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1)
        
        style.configure('Modern.TRadiobutton', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10),
                       focuscolor='none')
        
        # Progress bar styling removed to avoid compatibility issues
        
    def setup_ui(self):
        """Setup the main UI"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Main content area
        content_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Left panel - Download controls
        left_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel - History and logs
        right_panel = tk.Frame(content_frame, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Setup panels
        self.create_download_panel(left_panel)
        self.create_history_panel(right_panel)
        
    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="🎬 YouTube 4K Video Downloader Premium", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        self.status_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        self.status_frame.pack(side=tk.RIGHT)
        
        self.status_indicator = tk.Label(self.status_frame, text="●", 
                                       fg=self.colors['success'], 
                                       bg=self.colors['bg_primary'],
                                       font=('Segoe UI', 16))
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", 
                                    style='Body.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
    def create_download_panel(self, parent):
        """Create the download control panel"""
        # Panel header
        header_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=40)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text="📥 Download Video", 
                 style='Heading.TLabel').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Content frame
        content_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # URL input section
        self.create_url_section(content_frame)
        
        # Quality selection section
        self.create_quality_section(content_frame)
        
        # Format and path section
        self.create_format_section(content_frame)
        
        # Download button
        self.create_download_button(content_frame)
        
        # Progress section
        self.create_progress_section(content_frame)
        
    def create_url_section(self, parent):
        """Create URL input section"""
        url_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        url_frame.pack(fill=tk.X, pady=(20, 15))
        
        ttk.Label(url_frame, text="🔗 YouTube URL", 
                 style='Heading.TLabel').pack(anchor=tk.W, padx=20, pady=(0, 5))
        
        url_input_frame = tk.Frame(url_frame, bg=self.colors['bg_secondary'])
        url_input_frame.pack(fill=tk.X, padx=20)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='Modern.TEntry', font=('Segoe UI', 11))
        self.url_entry.pack(fill=tk.X, pady=(0, 5))
        
        # URL validation label
        self.url_status_label = ttk.Label(url_input_frame, text="", 
                                         style='Body.TLabel')
        self.url_status_label.pack(anchor=tk.W)
        
        # Bind URL validation
        self.url_var.trace('w', self.validate_url)
        
    def create_quality_section(self, parent):
        """Create quality selection section"""
        quality_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        quality_frame.pack(fill=tk.X, pady=15)
        
        ttk.Label(quality_frame, text="🎯 Video Quality", 
                 style='Heading.TLabel').pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        quality_options_frame = tk.Frame(quality_frame, bg=self.colors['bg_secondary'])
        quality_options_frame.pack(fill=tk.X, padx=20)
        
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
                               style='Modern.TRadiobutton')
            rb.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=3)
        
    def create_format_section(self, parent):
        """Create format and path selection section"""
        format_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        format_frame.pack(fill=tk.X, pady=15)
        
        # Format selection
        format_row = tk.Frame(format_frame, bg=self.colors['bg_secondary'])
        format_row.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Label(format_row, text="📁 Format", 
                 style='Heading.TLabel').pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(format_row, textvariable=self.format_var, 
                                   values=["mp4", "mkv", "webm", "avi"], 
                                   style='Modern.TCombobox', state="readonly")
        format_combo.pack(side=tk.RIGHT)
        
        # Path selection
        path_row = tk.Frame(format_frame, bg=self.colors['bg_secondary'])
        path_row.pack(fill=tk.X, padx=20)
        
        ttk.Label(path_row, text="💾 Download Path", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        path_input_frame = tk.Frame(path_row, bg=self.colors['bg_secondary'])
        path_input_frame.pack(fill=tk.X)
        
        self.path_var = tk.StringVar(value=self.download_path)
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.path_var, 
                                   style='Modern.TEntry')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(path_input_frame, text="📂 Browse", 
                               command=self.browse_folder, style='Secondary.TButton')
        browse_btn.pack(side=tk.RIGHT)
        
    def create_download_button(self, parent):
        """Create download button section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        button_frame.pack(fill=tk.X, pady=20, padx=20)
        
        self.download_btn = ttk.Button(button_frame, text="🚀 Download Video", 
                                      command=self.start_download, style='Modern.TButton')
        self.download_btn.pack(fill=tk.X, pady=10)
        
        # Quick actions
        actions_frame = tk.Frame(button_frame, bg=self.colors['bg_secondary'])
        actions_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(actions_frame, text="📋 History", 
                  command=self.show_history, style='Secondary.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions_frame, text="⚙️ Settings", 
                  command=self.show_settings, style='Secondary.TButton').pack(side=tk.LEFT)
        
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="", 
                                       style='Body.TLabel')
        self.progress_label.pack(anchor=tk.W)
        
    def create_history_panel(self, parent):
        """Create the history panel"""
        # Panel header
        header_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=40)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text="📚 Download History", 
                 style='Heading.TLabel').pack(side=tk.LEFT, padx=15, pady=10)
        
        # Content frame
        content_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # History list
        self.create_history_list(content_frame)
        
        # Log section
        self.create_log_section(content_frame)
        
    def create_history_list(self, parent):
        """Create download history list"""
        history_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 10), padx=20)
        
        # History treeview
        columns = ('Date', 'Title', 'Quality', 'Size', 'Status')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
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
        
        # Scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to open file location
        self.history_tree.bind('<Double-1>', self.open_download_location)
        
    def create_log_section(self, parent):
        """Create log section"""
        log_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20), padx=20)
        
        ttk.Label(log_frame, text="📋 Download Log", 
                 style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        
        # Log text area
        log_text_frame = tk.Frame(log_frame, bg=self.colors['bg_tertiary'], relief=tk.SUNKEN, bd=1)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=6, bg=self.colors['bg_tertiary'], 
                               fg=self.colors['text_primary'], font=('Consolas', 9),
                               wrap=tk.WORD, state=tk.DISABLED)
        
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=2)
        
    def setup_history_window(self):
        """Setup the history window (initially hidden)"""
        self.history_window = None
        
    def validate_url(self, *args):
        """Validate YouTube URL"""
        url = self.url_var.get().strip()
        if not url:
            self.url_status_label.config(text="")
            return
        
        if url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            self.url_status_label.config(text="✅ Valid YouTube URL", foreground=self.colors['success'])
        else:
            self.url_status_label.config(text="❌ Invalid URL format", foreground=self.colors['error'])
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.path_var.set(folder)
            self.download_path = folder
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def update_status(self, message, color=None):
        """Update status indicator"""
        self.status_label.config(text=message)
        if color:
            self.status_indicator.config(fg=color)
    
    def start_download(self):
        """Start download process"""
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
        self.update_status("Starting download...", self.colors['warning'])
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()
    
    def download_video(self):
        """Download video with enhanced logging"""
        try:
            url = self.url_var.get().strip()
            quality = self.quality_var.get()
            format_type = self.format_var.get()
            download_path = self.path_var.get()
            
            # Ensure download path exists
            os.makedirs(download_path, exist_ok=True)
            
            self.log_message("=" * 60)
            self.log_message("🚀 Starting YouTube Download")
            self.log_message("=" * 60)
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
                '--verbose'
            ])
            
            if format_type != 'best':
                cmd.extend(['--merge-output-format', format_type])
            
            cmd.append(url)
            
            self.log_message("🔧 Command: " + ' '.join(cmd))
            self.log_message("")
            self.log_message("📥 Starting download...")
            self.log_message("-" * 40)
            
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
                                parts = line.split('%')[0].split()
                                if parts:
                                    percent = float(parts[-1])
                                    self.progress_var.set(percent)
                                    self.update_status(f"Downloading... {percent:.1f}%", self.colors['warning'])
                            except:
                                pass
                        elif 'ERROR' in line.upper() or 'FAILED' in line.upper():
                            self.log_message(f"⚠️  WARNING: {line}")
                
                # Wait for process to complete
                return_code = process.wait()
                
            except Exception as e:
                self.log_message(f"❌ Error reading process output: {str(e)}")
                return_code = -1
            
            self.log_message("-" * 40)
            
            if return_code == 0:
                self.update_status("✅ Download completed!", self.colors['success'])
                self.progress_var.set(100)
                self.log_message("🎉 SUCCESS: Video downloaded successfully!")
                self.log_message(f"📁 Saved to: {download_path}")
                
                # Add to history
                self.add_to_history(url, quality, format_type, "Success")
                
                messagebox.showinfo("Success", f"Video downloaded successfully!\nSaved to: {download_path}")
            else:
                self.update_status("❌ Download failed!", self.colors['error'])
                self.log_message("💥 FAILED: Download did not complete successfully")
                self.log_message(f"🔍 Return code: {return_code}")
                
                # Add to history
                self.add_to_history(url, quality, format_type, "Failed")
                
                if output_lines:
                    self.log_message("📋 Last few lines of output:")
                    for line in output_lines[-5:]:
                        self.log_message(f"   {line}")
                
                messagebox.showerror("Download Failed", 
                    f"Download failed with return code {return_code}.\n"
                    f"Check the log for details.")
                
        except FileNotFoundError as e:
            self.log_message(f"❌ yt-dlp not found: {str(e)}")
            self.update_status("❌ yt-dlp not installed!", self.colors['error'])
            messagebox.showerror("yt-dlp Not Found", 
                "yt-dlp is not installed or not in PATH.\n"
                "Please run: python -m pip install yt-dlp")
        except Exception as e:
            self.log_message(f"💥 Unexpected error: {str(e)}")
            self.update_status("💥 Download failed!", self.colors['error'])
            messagebox.showerror("Error", f"An unexpected error occurred:\n{str(e)}")
        finally:
            self.download_btn.config(state='normal')
    
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
            self.history_window.geometry("800x600")
            self.history_window.configure(bg=self.colors['bg_primary'])
            
            # History list
            history_frame = tk.Frame(self.history_window, bg=self.colors['bg_secondary'])
            history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
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
        messagebox.showinfo("Settings", "Settings panel coming soon!\n\nFeatures to be added:\n• Default download quality\n• Auto-download folder\n• Notification preferences")
    
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
    app = YouTubeDownloaderPremium(root)
    
    # Load initial history
    app.update_history_display()
    
    root.mainloop()

if __name__ == "__main__":
    main()
