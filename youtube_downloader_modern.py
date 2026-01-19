import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
import time
import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class YouTubeDownloaderModern:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube 4K Video Downloader")
        self.root.geometry("1800x1000")
        self.root.minsize(1600, 900)
        
        # Set download path
        self.download_path = str(Path.home() / "Downloads")
        self.history_file = "download_history.json"
        self.config_file = "config.json"
        self.download_history = self.load_history()
        self.config = self.load_config()
        
        self.download_process = None
        self.is_downloading = False
        self.download_queue = []
        self.current_download = None
        self.queue_thread = None
        self.queue_file = "download_queue.json"
        
        # Start Flask API server in background
        self.start_api_server()
        
        # Periodically sync queue from file (for external additions)
        self.sync_queue_from_file()
        
        self.setup_ui()
        self.setup_history_window()
        
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'auto_download': False,
            'default_quality': 'best',
            'default_format': 'mp4',
            'default_path': str(Path.home() / "Downloads"),
            'audio_bitrate': '192k'
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
        except:
            pass
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
        
    def setup_ui(self):
        """Setup the modern UI"""
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Left panel - Download controls
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Middle panel - Queue
        middle_panel = ctk.CTkFrame(content_frame)
        middle_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right panel - History and logs
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Setup panels
        self.create_download_panel(left_panel)
        self.create_queue_panel(middle_panel)
        self.create_history_panel(right_panel)
        
    def create_header(self, parent):
        """Create header section"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(header_frame, text="🎬 YouTube 4K Video Downloader", 
                                  font=ctk.CTkFont(size=32, weight="bold"))
        title_label.pack(side="left")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(header_frame, text="● Ready", 
                                        font=ctk.CTkFont(size=14),
                                        text_color="#22c55e")
        self.status_label.pack(side="right")
        
    def create_download_panel(self, parent):
        """Create download control panel"""
        # Panel title
        title = ctk.CTkLabel(parent, text="📥 Download Configuration", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 20))
        
        # URL input
        url_label = ctk.CTkLabel(parent, text="🔗 YouTube URL", 
                                font=ctk.CTkFont(size=14, weight="bold"))
        url_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.url_var = tk.StringVar()
        self.url_entry = ctk.CTkEntry(parent, textvariable=self.url_var, 
                                      placeholder_text="Paste YouTube URL here...",
                                      height=40, font=ctk.CTkFont(size=12))
        self.url_entry.pack(fill="x", padx=20, pady=(0, 5))
        
        self.url_status_label = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=11))
        self.url_status_label.pack(anchor="w", padx=20, pady=(0, 20))
        
        self.url_var.trace('w', self.validate_url)
        
        # Quality selection
        quality_label = ctk.CTkLabel(parent, text="🎯 Video Quality", 
                                    font=ctk.CTkFont(size=14, weight="bold"))
        quality_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        quality_frame = ctk.CTkFrame(parent, fg_color="transparent")
        quality_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.quality_var = tk.StringVar(value=self.config.get('default_quality', 'best'))
        quality_options = [
            ("🏆 Best (4K/8K)", "best"),
            ("📺 4K (2160p)", "2160"),
            ("📱 2K (1440p)", "1440"),
            ("💻 1080p", "1080"),
            ("📱 720p", "720"),
            ("📺 480p", "480"),
            ("📱 360p", "360")
        ]
        
        for i, (text, value) in enumerate(quality_options):
            rb = ctk.CTkRadioButton(quality_frame, text=text, variable=self.quality_var, 
                                   value=value, font=ctk.CTkFont(size=12))
            rb.grid(row=i//2, column=i%2, sticky="w", padx=(0, 20), pady=5)
        
        # Format selection
        format_label = ctk.CTkLabel(parent, text="📁 Output Format", 
                                    font=ctk.CTkFont(size=14, weight="bold"))
        format_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        format_frame = ctk.CTkFrame(parent, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.format_var = tk.StringVar(value=self.config.get('default_format', 'mp4'))
        format_options = [
            "mp4 (Video)",
            "mkv (Video)",
            "webm (Video)",
            "avi (Video)",
            "mp3 (Audio Only)",
            "m4a (Audio Only)",
            "wav (Audio Only)",
            "opus (Audio Only)"
        ]
        
        self.format_combo = ctk.CTkComboBox(format_frame, values=format_options, 
                                           variable=self.format_var,
                                           font=ctk.CTkFont(size=12))
        self.format_combo.pack(fill="x")
        
        # Audio quality (if audio format selected)
        self.audio_quality_label = ctk.CTkLabel(parent, text="🎵 Audio Bitrate", 
                                                font=ctk.CTkFont(size=14, weight="bold"))
        self.audio_quality_var = tk.StringVar(value=self.config.get('audio_bitrate', '192k'))
        self.audio_quality_combo = ctk.CTkComboBox(parent, 
                                                   values=["128k", "192k", "256k", "320k"],
                                                   variable=self.audio_quality_var,
                                                   font=ctk.CTkFont(size=12))
        
        # Show/hide audio quality based on format
        self.format_var.trace('w', self.toggle_audio_quality)
        self.toggle_audio_quality()
        
        # Download path
        path_label = ctk.CTkLabel(parent, text="💾 Download Path", 
                                 font=ctk.CTkFont(size=14, weight="bold"))
        path_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.path_var = tk.StringVar(value=self.config.get('default_path', self.download_path))
        self.path_entry = ctk.CTkEntry(path_frame, textvariable=self.path_var, 
                                       height=40, font=ctk.CTkFont(size=12))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(path_frame, text="📂 Browse", command=self.browse_folder,
                                   width=100, font=ctk.CTkFont(size=12))
        browse_btn.pack(side="right")
        
        # Buttons
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.add_queue_btn = ctk.CTkButton(button_frame, text="🚀 Add to Queue", 
                                           command=self.add_to_queue,
                                           height=50, font=ctk.CTkFont(size=14, weight="bold"))
        self.add_queue_btn.pack(fill="x", pady=(0, 10))
        
        self.download_now_btn = ctk.CTkButton(button_frame, text="⬇️ Download Now", 
                                             command=self.download_now,
                                             height=40, font=ctk.CTkFont(size=13),
                                             fg_color="#3b82f6", hover_color="#2563eb")
        self.download_now_btn.pack(fill="x", pady=(0, 10))
        
        # Auto-download checkbox
        self.auto_download_var = tk.BooleanVar(value=self.config.get('auto_download', False))
        self.auto_download_checkbox = ctk.CTkCheckBox(button_frame, 
                                                      text="🔄 Auto-download when added to queue",
                                                      variable=self.auto_download_var,
                                                      command=self.toggle_auto_download,
                                                      font=ctk.CTkFont(size=12))
        self.auto_download_checkbox.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(parent, variable=self.progress_var)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        
        self.progress_label = ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=11))
        self.progress_label.pack(anchor="w", padx=20)
        
    def toggle_audio_quality(self, *args):
        """Show/hide audio quality selector"""
        format_val = self.format_var.get()
        is_audio = any(x in format_val.lower() for x in ['mp3', 'm4a', 'wav', 'opus'])
        
        if is_audio:
            self.audio_quality_label.pack(anchor="w", padx=20, pady=(0, 10))
            self.audio_quality_combo.pack(fill="x", padx=20, pady=(0, 20))
        else:
            self.audio_quality_label.pack_forget()
            self.audio_quality_combo.pack_forget()
    
    def create_queue_panel(self, parent):
        """Create queue management panel"""
        title = ctk.CTkLabel(parent, text="📋 Download Queue", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 20))
        
        # Queue treeview
        queue_frame = ctk.CTkFrame(parent)
        queue_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Treeview
        columns = ('Status', 'Title', 'Quality', 'Format')
        self.queue_tree = tk.ttk.Treeview(queue_frame, columns=columns, show='headings', height=15)
        
        self.queue_tree.heading('Status', text='📊 Status')
        self.queue_tree.heading('Title', text='📺 Title')
        self.queue_tree.heading('Quality', text='🎯 Quality')
        self.queue_tree.heading('Format', text='📁 Format')
        
        self.queue_tree.column('Status', width=100)
        self.queue_tree.column('Title', width=250)
        self.queue_tree.column('Quality', width=80)
        self.queue_tree.column('Format', width=100)
        
        scrollbar = tk.ttk.Scrollbar(queue_frame, orient="vertical", command=self.queue_tree.yview)
        self.queue_tree.configure(yscrollcommand=scrollbar.set)
        
        self.queue_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Queue controls
        controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.start_queue_btn = ctk.CTkButton(controls_frame, text="▶️ Start Queue", 
                                             command=self.start_queue,
                                             font=ctk.CTkFont(size=12))
        self.start_queue_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(controls_frame, text="🗑️ Clear Queue", 
                                 command=self.clear_queue,
                                 font=ctk.CTkFont(size=12),
                                 fg_color="#ef4444", hover_color="#dc2626")
        clear_btn.pack(side="left")
        
    def create_history_panel(self, parent):
        """Create history and log panel"""
        title = ctk.CTkLabel(parent, text="📚 History & Logs", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(20, 20))
        
        # History
        history_label = ctk.CTkLabel(parent, text="📚 Recent Downloads", 
                                    font=ctk.CTkFont(size=14, weight="bold"))
        history_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        history_frame = ctk.CTkFrame(parent)
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columns = ('Date', 'Title', 'Quality', 'Size', 'Status')
        self.history_tree = tk.ttk.Treeview(history_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        history_scrollbar = tk.ttk.Scrollbar(history_frame, orient="vertical", 
                                            command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        history_scrollbar.pack(side="right", fill="y")
        
        self.history_tree.bind('<Double-1>', self.open_download_location)
        
        # Log
        log_label = ctk.CTkLabel(parent, text="📋 Download Log", 
                                font=ctk.CTkFont(size=14, weight="bold"))
        log_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        log_frame = ctk.CTkFrame(parent)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.log_text = ctk.CTkTextbox(log_frame, height=150, font=ctk.CTkFont(size=11))
        self.log_text.pack(fill="both", expand=True)
        
    def setup_history_window(self):
        """Setup history window"""
        self.history_window = None
        
    def validate_url(self, *args):
        """Validate YouTube URL"""
        url = self.url_var.get().strip()
        if not url:
            self.url_status_label.configure(text="")
            return
        
        if url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            self.url_status_label.configure(text="✅ Valid YouTube URL", text_color="#22c55e")
        else:
            self.url_status_label.configure(text="❌ Invalid URL format", text_color="#ef4444")
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.path_var.set(folder)
            self.download_path = folder
            self.config['default_path'] = folder
            self.save_config()
    
    def toggle_auto_download(self):
        """Toggle auto-download setting"""
        self.config['auto_download'] = self.auto_download_var.get()
        self.save_config()
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
    
    def update_status(self, message, color="#22c55e"):
        """Update status indicator"""
        self.status_label.configure(text=f"● {message}", text_color=color)
    
    def get_video_title(self, url):
        """Get video title from URL"""
        try:
            cmd = ['yt-dlp', '--get-title', '--no-playlist', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                title = result.stdout.strip()
                title = re.sub(r'[^\w\s\-\.]', '', title)[:50]
                return title if title else "Unknown Title"
        except:
            pass
        return "Unknown Title"
    
    def add_to_queue(self):
        """Add video to download queue"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        # Get video title
        self.log_message(f"🔍 Getting video information...")
        title = self.get_video_title(url)
        
        # Get format
        format_val = self.format_var.get()
        format_type = format_val.split(' ')[0].lower()
        
        # Add to queue
        queue_item = {
            'url': url,
            'title': title,
            'quality': self.quality_var.get(),
            'format': format_type,
            'audio_bitrate': self.audio_quality_var.get() if 'audio' in format_val.lower() else None,
            'status': 'Queued',
            'added_time': datetime.now().strftime("%H:%M:%S")
        }
        
        self.download_queue.append(queue_item)
        self.save_queue_to_file()
        self.update_queue_display()
        self.url_var.set("")
        
        self.log_message(f"✅ Added to queue: {title}")
        
        # Auto-download if enabled
        if self.auto_download_var.get() and not self.is_downloading:
            self.start_queue()
    
    def update_queue_display(self):
        """Update queue display"""
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        for item in self.download_queue:
            status_icon = "⏳" if item['status'] == 'Queued' else "🔄" if item['status'] == 'Downloading' else "✅" if item['status'] == 'Completed' else "❌"
            self.queue_tree.insert('', 'end', values=(
                f"{status_icon} {item['status']}",
                item['title'][:40] + "..." if len(item['title']) > 40 else item['title'],
                item['quality'],
                item['format']
            ))
    
    def start_queue(self):
        """Start processing queue"""
        if not self.download_queue:
            messagebox.showwarning("Empty Queue", "No videos in the download queue")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Already Downloading", "A download is already in progress")
            return
        
        self.queue_thread = threading.Thread(target=self.process_queue, daemon=True)
        self.queue_thread.start()
    
    def process_queue(self):
        """Process download queue"""
        self.is_downloading = True
        self.update_status("Processing queue...", "#f59e0b")
        
        for i, item in enumerate(self.download_queue):
            if item['status'] == 'Queued':
                self.current_download = item
                item['status'] = 'Downloading'
                self.update_queue_display()
                
                self.log_message(f"📥 Starting download {i+1}/{len(self.download_queue)}: {item['title']}")
                
                success = self.download_single_video(item)
                
                if success:
                    item['status'] = 'Completed'
                    self.log_message(f"✅ Completed: {item['title']}")
                else:
                    item['status'] = 'Failed'
                    self.log_message(f"❌ Failed: {item['title']}")
                
                self.update_queue_display()
                self.add_to_history(item['url'], item['title'], item['quality'], 
                                  item['format'], "Success" if success else "Failed")
        
        self.is_downloading = False
        self.current_download = None
        self.update_status("Queue completed!", "#22c55e")
        self.log_message("🎉 All downloads completed!")
    
    def download_single_video(self, item):
        """Download a single video"""
        try:
            url = item['url']
            quality = item['quality']
            format_type = item['format']
            download_path = self.path_var.get()
            
            os.makedirs(download_path, exist_ok=True)
            
            cmd = ['yt-dlp']
            
            # Audio extraction
            if format_type in ['mp3', 'm4a', 'wav', 'opus']:
                cmd.extend(['-x', '--audio-format', format_type])
                if item.get('audio_bitrate'):
                    cmd.extend(['--audio-quality', item['audio_bitrate']])
            else:
                # Video format
                if quality == 'best':
                    cmd.extend(['--format', 'best'])
                else:
                    cmd.extend(['--format', f'best[height<={quality}]'])
                
                if format_type != 'best':
                    cmd.extend(['--merge-output-format', format_type])
            
            cmd.extend(['--output', f'{download_path}/%(title)s.%(ext)s'])
            cmd.extend([
                '--no-playlist',
                '--retries', '10',
                '--fragment-retries', '10',
                '--socket-timeout', '30',
                '--http-chunk-size', '10485760',
                '--concurrent-fragments', '4',
                '--buffer-size', '65536'
            ])
            cmd.append(url)
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=download_path,
                bufsize=1,
                shell=False
            )
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.log_message(line)
                    if '[download]' in line and '%' in line:
                        try:
                            parts = line.split('%')[0].split()
                            if parts:
                                percent = float(parts[-1])
                                self.progress_var.set(percent)
                                self.progress_label.configure(text=f"Downloading... {percent:.1f}%")
                        except:
                            pass
            
            return_code = process.wait()
            return return_code == 0
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            return False
    
    def download_now(self):
        """Download video immediately"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        # Add to queue and start immediately
        self.add_to_queue()
        if not self.is_downloading:
            self.start_queue()
    
    def clear_queue(self):
        """Clear download queue"""
        if self.download_queue and not self.is_downloading:
            self.download_queue.clear()
            self.update_queue_display()
            self.log_message("🗑️ Queue cleared")
        elif self.is_downloading:
            messagebox.showwarning("Cannot Clear", "Cannot clear queue while downloading")
    
    def add_to_history(self, url, title, quality, format_type, status):
        """Add download to history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        """Update history display"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
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
        """Open download location"""
        selection = self.history_tree.selection()
        if selection:
            os.startfile(self.path_var.get())
    
    def show_history(self):
        """Show detailed history window"""
        if self.history_window is None or not self.history_window.winfo_exists():
            self.history_window = ctk.CTkToplevel(self.root)
            self.history_window.title("📚 Download History")
            self.history_window.geometry("1000x700")
            
            history_frame = ctk.CTkFrame(self.history_window)
            history_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            columns = ('Date', 'URL', 'Title', 'Quality', 'Format', 'Status')
            history_tree = tk.ttk.Treeview(history_frame, columns=columns, show='headings')
            
            for col in columns:
                history_tree.heading(col, text=col)
                history_tree.column(col, width=120)
            
            for entry in reversed(self.download_history):
                status_icon = "✅" if entry['status'] == "Success" else "❌"
                history_tree.insert('', 'end', values=(
                    entry['timestamp'],
                    entry['url'][:50] + "..." if len(entry['url']) > 50 else entry['url'],
                    entry['title'],
                    entry['quality'],
                    entry['format'],
                    f"{status_icon} {entry['status']}"
                ))
            
            history_tree.pack(fill="both", expand=True)
    
    def load_history(self):
        """Load download history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_history(self):
        """Save download history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.download_history, f, indent=2)
        except:
            pass
    
    def start_api_server(self):
        """Start Flask API server in background thread"""
        self.api_app = Flask(__name__)
        CORS(self.api_app)
        
        @self.api_app.route('/api/health', methods=['GET'])
        def health_check():
            return jsonify({'status': 'ok', 'message': 'API server is running'})
        
        @self.api_app.route('/api/add-to-queue', methods=['POST'])
        def add_to_queue_api():
            try:
                data = request.json
                url = data.get('url', '').strip()
                
                if not url:
                    return jsonify({'status': 'error', 'message': 'URL is required'}), 400
                
                if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
                    return jsonify({'status': 'error', 'message': 'Invalid YouTube URL'}), 400
                
                # Get video title
                title = self.get_video_title(url)
                
                # Get format
                format_val = data.get('format', self.config.get('default_format', 'mp4'))
                format_type = format_val.split(' ')[0].lower() if ' ' in format_val else format_val
                
                # Create queue item
                queue_item = {
                    'url': url,
                    'title': title,
                    'quality': data.get('quality', self.config.get('default_quality', 'best')),
                    'format': format_type,
                    'audio_bitrate': data.get('audio_bitrate', self.config.get('audio_bitrate', '192k')) if 'audio' in format_type else None,
                    'status': 'Queued',
                    'added_time': datetime.now().strftime("%H:%M:%S"),
                    'source': 'browser_extension'
                }
                
                # Add to queue
                self.download_queue.append(queue_item)
                self.save_queue_to_file()
                
                # Update UI on main thread
                self.root.after(0, self.update_queue_display)
                self.root.after(0, lambda: self.log_message(f"✅ Added from browser: {title}"))
                
                # Auto-download if enabled
                if self.auto_download_var.get() and not self.is_downloading:
                    self.root.after(0, self.start_queue)
                
                return jsonify({
                    'status': 'success',
                    'message': f'Video added to queue: {title}',
                    'queue_item': queue_item
                })
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        
        @self.api_app.route('/api/get-queue', methods=['GET'])
        def get_queue_api():
            return jsonify({'status': 'success', 'queue': self.download_queue})
        
        # Start Flask server in background thread
        def run_server():
            self.api_app.run(host='localhost', port=5000, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        self.log_message("🌐 API server started on http://localhost:5000")
    
    def sync_queue_from_file(self):
        """Periodically sync queue from JSON file (for external additions)"""
        def sync():
            try:
                if os.path.exists(self.queue_file):
                    with open(self.queue_file, 'r') as f:
                        file_queue = json.load(f)
                    
                    # Add new items from file that aren't in memory queue
                    file_urls = {item.get('url') for item in file_queue}
                    memory_urls = {item.get('url') for item in self.download_queue}
                    
                    new_items = [item for item in file_queue if item.get('url') not in memory_urls]
                    if new_items:
                        self.download_queue.extend(new_items)
                        self.update_queue_display()
                        self.log_message(f"📥 Synced {len(new_items)} item(s) from file")
                    
                    # Clear the file after syncing
                    if new_items:
                        with open(self.queue_file, 'w') as f:
                            json.dump([], f)
            except:
                pass
        
        # Sync every 2 seconds
        def periodic_sync():
            while True:
                time.sleep(2)
                sync()
        
        sync_thread = threading.Thread(target=periodic_sync, daemon=True)
        sync_thread.start()
    
    def save_queue_to_file(self):
        """Save queue to file"""
        try:
            with open(self.queue_file, 'w') as f:
                json.dump(self.download_queue, f, indent=2)
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
    
    root = ctk.CTk()
    app = YouTubeDownloaderModern(root)
    app.update_history_display()
    root.mainloop()

if __name__ == "__main__":
    main()
