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
import re

class YouTubeDownloaderQueue:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube 4K Video Downloader - Queue Edition")
        self.root.geometry("1800x1200")
        self.root.configure(bg='#0a0a0a')
        self.root.minsize(1600, 1000)
        
        # Set download path FIRST
        self.download_path = str(Path.home() / "Downloads")
        self.history_file = "download_history.json"
        self.download_history = self.load_history()
        self.download_process = None
        self.is_downloading = False
        self.download_queue = []
        self.current_download = None
        self.queue_thread = None
        
        # Shadcn-inspired color scheme
        self.colors = {
            'background': '#0a0a0a',
            'card': '#111111',
            'card_secondary': '#1a1a1a',
            'border': '#2a2a2a',
            'input': '#1a1a1a',
            'primary': '#22c55e',
            'primary_hover': '#16a34a',
            'secondary': '#3b82f6',
            'secondary_hover': '#2563eb',
            'destructive': '#ef4444',
            'destructive_hover': '#dc2626',
            'warning': '#f59e0b',
            'warning_hover': '#d97706',
            'muted': '#6b7280',
            'muted_foreground': '#9ca3af',
            'foreground': '#ffffff',
            'foreground_secondary': '#e5e7eb',
            'accent': '#f3f4f6',
            'accent_foreground': '#111827',
            'ring': '#22c55e',
            'radius': '8px'
        }
        
        self.setup_styles()
        self.setup_ui()
        self.setup_history_window()
        
    def setup_styles(self):
        """Setup shadcn-inspired styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure shadcn-inspired styles
        style.configure('ShadcnTitle.TLabel', 
                       background=self.colors['background'], 
                       foreground=self.colors['primary'],
                       font=('Inter', 32, 'bold'))
        
        style.configure('ShadcnHeading.TLabel', 
                       background=self.colors['background'], 
                       foreground=self.colors['foreground'],
                       font=('Inter', 18, 'bold'))
        
        style.configure('ShadcnSubheading.TLabel', 
                       background=self.colors['background'], 
                       foreground=self.colors['foreground'],
                       font=('Inter', 14, 'bold'))
        
        style.configure('ShadcnBody.TLabel', 
                       background=self.colors['background'], 
                       foreground=self.colors['foreground_secondary'],
                       font=('Inter', 12))
        
        style.configure('ShadcnMuted.TLabel', 
                       background=self.colors['background'], 
                       foreground=self.colors['muted_foreground'],
                       font=('Inter', 11))
        
        style.configure('ShadcnButton.TButton', 
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Inter', 13, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(24, 16))
        
        style.map('ShadcnButton.TButton',
                 background=[('active', self.colors['primary_hover']),
                           ('pressed', self.colors['primary_hover'])])
        
        style.configure('ShadcnSecondary.TButton', 
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Inter', 12, 'bold'),
                       borderwidth=0,
                       padding=(20, 12))
        
        style.map('ShadcnSecondary.TButton',
                 background=[('active', self.colors['secondary_hover'])])
        
        style.configure('ShadcnOutline.TButton', 
                       background=self.colors['card'],
                       foreground=self.colors['foreground'],
                       font=('Inter', 11),
                       borderwidth=1,
                       padding=(16, 10))
        
        style.map('ShadcnOutline.TButton',
                 background=[('active', self.colors['border'])])
        
        style.configure('ShadcnInput.TEntry', 
                       fieldbackground=self.colors['input'],
                       foreground=self.colors['foreground'],
                       borderwidth=1,
                       insertcolor=self.colors['primary'],
                       font=('Inter', 12))
        
        style.configure('ShadcnSelect.TCombobox', 
                       fieldbackground=self.colors['input'],
                       foreground=self.colors['foreground'],
                       borderwidth=1,
                       font=('Inter', 12))
        
        style.configure('ShadcnRadio.TRadiobutton', 
                       background=self.colors['background'],
                       foreground=self.colors['foreground'],
                       font=('Inter', 12),
                       focuscolor='none')
        
    def setup_ui(self):
        """Setup the shadcn-inspired UI with queue system"""
        # Main container with modern spacing
        main_container = tk.Frame(self.root, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
        
        # Header section with modern design
        self.create_shadcn_header(main_container)
        
        # Main content area with grid layout
        content_frame = tk.Frame(main_container, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(32, 0))
        
        # Left panel - Download controls with card design
        left_panel = self.create_card(content_frame, "Download Configuration", side=tk.LEFT, padx=(0, 16))
        
        # Middle panel - Queue management
        middle_panel = self.create_card(content_frame, "Download Queue", side=tk.LEFT, padx=(8, 8))
        
        # Right panel - History and logs with card design
        right_panel = self.create_card(content_frame, "Download History & Logs", side=tk.RIGHT, padx=(16, 0))
        
        # Setup panels
        self.create_shadcn_download_panel(left_panel)
        self.create_shadcn_queue_panel(middle_panel)
        self.create_shadcn_history_panel(right_panel)
        
    def create_card(self, parent, title, side=tk.LEFT, padx=(0, 0)):
        """Create a modern card container"""
        card_frame = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT, bd=0)
        card_frame.pack(side=side, fill=tk.BOTH, expand=True, padx=padx)
        
        # Card header
        header_frame = tk.Frame(card_frame, bg=self.colors['card_secondary'], height=60)
        header_frame.pack(fill=tk.X, padx=24, pady=24)
        header_frame.pack_propagate(False)
        
        ttk.Label(header_frame, text=title, 
                 style='ShadcnHeading.TLabel').pack(side=tk.LEFT, pady=18)
        
        # Content frame
        content_frame = tk.Frame(card_frame, bg=self.colors['card'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))
        
        return content_frame
        
    def create_shadcn_header(self, parent):
        """Create the shadcn-inspired header section"""
        header_frame = tk.Frame(parent, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 32))
        
        # Title with modern styling
        title_frame = tk.Frame(header_frame, bg=self.colors['background'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = ttk.Label(title_frame, text="🎬 YouTube 4K Video Downloader", 
                               style='ShadcnTitle.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator with modern design
        self.status_frame = tk.Frame(header_frame, bg=self.colors['background'])
        self.status_frame.pack(side=tk.RIGHT)
        
        # Status badge
        status_badge = tk.Frame(self.status_frame, bg=self.colors['primary'], relief=tk.FLAT, bd=0)
        status_badge.pack(side=tk.LEFT, padx=(0, 12), pady=8)
        
        self.status_indicator = tk.Label(status_badge, text="●", 
                                       fg='white', 
                                       bg=self.colors['primary'],
                                       font=('Inter', 16))
        self.status_indicator.pack(side=tk.LEFT, padx=(12, 8), pady=8)
        
        self.status_label = ttk.Label(status_badge, text="Ready to Download", 
                                    style='ShadcnBody.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=(0, 12), pady=8)
        
    def create_shadcn_download_panel(self, parent):
        """Create the shadcn-inspired download control panel"""
        # URL input section with modern design
        self.create_shadcn_url_section(parent)
        
        # Quality selection section
        self.create_shadcn_quality_section(parent)
        
        # Format and path section
        self.create_shadcn_format_section(parent)
        
        # Download button with modern design
        self.create_shadcn_download_button(parent)
        
        # Progress section with modern styling
        self.create_shadcn_progress_section(parent)
        
    def create_shadcn_url_section(self, parent):
        """Create shadcn-inspired URL input section"""
        url_frame = tk.Frame(parent, bg=self.colors['card'])
        url_frame.pack(fill=tk.X, pady=(0, 24))
        
        ttk.Label(url_frame, text="🔗 YouTube URL", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        url_input_frame = tk.Frame(url_frame, bg=self.colors['card'])
        url_input_frame.pack(fill=tk.X)
        
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, 
                                  style='ShadcnInput.TEntry', font=('Inter', 13))
        self.url_entry.pack(fill=tk.X, pady=(0, 8))
        
        # URL validation with modern styling
        self.url_status_label = ttk.Label(url_input_frame, text="", 
                                         style='ShadcnMuted.TLabel')
        self.url_status_label.pack(anchor=tk.W)
        
        # Bind URL validation
        self.url_var.trace('w', self.validate_url)
        
    def create_shadcn_quality_section(self, parent):
        """Create shadcn-inspired quality selection section"""
        quality_frame = tk.Frame(parent, bg=self.colors['card'])
        quality_frame.pack(fill=tk.X, pady=(0, 24))
        
        ttk.Label(quality_frame, text="🎯 Video Quality", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 16))
        
        quality_options_frame = tk.Frame(quality_frame, bg=self.colors['card'])
        quality_options_frame.pack(fill=tk.X)
        
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
                               style='ShadcnRadio.TRadiobutton')
            rb.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 32), pady=6)
        
    def create_shadcn_format_section(self, parent):
        """Create shadcn-inspired format and path selection section"""
        format_frame = tk.Frame(parent, bg=self.colors['card'])
        format_frame.pack(fill=tk.X, pady=(0, 24))
        
        # Format selection
        format_row = tk.Frame(format_frame, bg=self.colors['card'])
        format_row.pack(fill=tk.X, pady=(0, 16))
        
        ttk.Label(format_row, text="📁 Output Format", 
                 style='ShadcnSubheading.TLabel').pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(format_row, textvariable=self.format_var, 
                                   values=["mp4", "mkv", "webm", "avi"], 
                                   style='ShadcnSelect.TCombobox', state="readonly")
        format_combo.pack(side=tk.RIGHT)
        
        # Path selection
        path_row = tk.Frame(format_frame, bg=self.colors['card'])
        path_row.pack(fill=tk.X)
        
        ttk.Label(path_row, text="💾 Download Path", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 8))
        
        path_input_frame = tk.Frame(path_row, bg=self.colors['card'])
        path_input_frame.pack(fill=tk.X)
        
        self.path_var = tk.StringVar(value=self.download_path)
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.path_var, 
                                   style='ShadcnInput.TEntry')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
        
        browse_btn = ttk.Button(path_input_frame, text="📂 Browse", 
                               command=self.browse_folder, style='ShadcnOutline.TButton')
        browse_btn.pack(side=tk.RIGHT)
        
    def create_shadcn_download_button(self, parent):
        """Create shadcn-inspired download button section"""
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, pady=(0, 24))
        
        # Main download button
        self.download_btn = ttk.Button(button_frame, text="🚀 Add to Queue", 
                                      command=self.add_to_queue, style='ShadcnButton.TButton')
        self.download_btn.pack(fill=tk.X, pady=(0, 12))
        
        # Start queue button
        self.start_queue_btn = ttk.Button(button_frame, text="▶️ Start Queue", 
                                        command=self.start_queue, style='ShadcnSecondary.TButton')
        self.start_queue_btn.pack(fill=tk.X, pady=(0, 16))
        
        # Quick actions with modern styling
        actions_frame = tk.Frame(button_frame, bg=self.colors['card'])
        actions_frame.pack(fill=tk.X)
        
        ttk.Button(actions_frame, text="📋 View History", 
                  command=self.show_history, style='ShadcnSecondary.TButton').pack(side=tk.LEFT, padx=(0, 12))
        
        ttk.Button(actions_frame, text="⚙️ Settings", 
                  command=self.show_settings, style='ShadcnOutline.TButton').pack(side=tk.LEFT)
        
    def create_shadcn_progress_section(self, parent):
        """Create shadcn-inspired progress section"""
        progress_frame = tk.Frame(parent, bg=self.colors['card'])
        progress_frame.pack(fill=tk.X, pady=(0, 24))
        
        # Progress bar with modern styling
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 12))
        
        # Progress label with modern styling
        self.progress_label = ttk.Label(progress_frame, text="", 
                                       style='ShadcnBody.TLabel')
        self.progress_label.pack(anchor=tk.W)
        
    def create_shadcn_queue_panel(self, parent):
        """Create the queue management panel"""
        # Queue list
        queue_frame = tk.Frame(parent, bg=self.colors['card'])
        queue_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        ttk.Label(queue_frame, text="📋 Download Queue", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 16))
        
        # Queue treeview
        columns = ('Status', 'Title', 'Quality', 'Format')
        self.queue_tree = ttk.Treeview(queue_frame, columns=columns, show='headings', height=12)
        
        # Configure columns
        self.queue_tree.heading('Status', text='📊 Status')
        self.queue_tree.heading('Title', text='📺 Title')
        self.queue_tree.heading('Quality', text='🎯 Quality')
        self.queue_tree.heading('Format', text='📁 Format')
        
        self.queue_tree.column('Status', width=100)
        self.queue_tree.column('Title', width=250)
        self.queue_tree.column('Quality', width=80)
        self.queue_tree.column('Format', width=80)
        
        # Scrollbar
        queue_scrollbar = ttk.Scrollbar(queue_frame, orient=tk.VERTICAL, command=self.queue_tree.yview)
        self.queue_tree.configure(yscrollcommand=queue_scrollbar.set)
        
        self.queue_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        queue_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Queue controls
        controls_frame = tk.Frame(parent, bg=self.colors['card'])
        controls_frame.pack(fill=tk.X)
        
        ttk.Button(controls_frame, text="🗑️ Clear Queue", 
                  command=self.clear_queue, style='ShadcnOutline.TButton').pack(side=tk.LEFT, padx=(0, 12))
        
        ttk.Button(controls_frame, text="⏸️ Pause Queue", 
                  command=self.pause_queue, style='ShadcnOutline.TButton').pack(side=tk.LEFT)
        
    def create_shadcn_history_panel(self, parent):
        """Create the shadcn-inspired history panel"""
        # History list with modern styling
        self.create_shadcn_history_list(parent)
        
        # Log section with modern styling
        self.create_shadcn_log_section(parent)
        
    def create_shadcn_history_list(self, parent):
        """Create shadcn-inspired download history list"""
        history_frame = tk.Frame(parent, bg=self.colors['card'])
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 24))
        
        ttk.Label(history_frame, text="📚 Recent Downloads", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 16))
        
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
        
    def create_shadcn_log_section(self, parent):
        """Create shadcn-inspired log section"""
        log_frame = tk.Frame(parent, bg=self.colors['card'])
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(log_frame, text="📋 Download Log", 
                 style='ShadcnSubheading.TLabel').pack(anchor=tk.W, pady=(0, 16))
        
        # Log text area with modern styling
        log_text_frame = tk.Frame(log_frame, bg=self.colors['input'], relief=tk.FLAT, bd=1)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=8, bg=self.colors['input'], 
                               fg=self.colors['foreground'], font=('JetBrains Mono', 11),
                               wrap=tk.WORD, state=tk.DISABLED, bd=0, padx=16, pady=16)
        
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
                                       foreground=self.colors['primary'])
        else:
            self.url_status_label.config(text="❌ Invalid URL format", 
                                       foreground=self.colors['destructive'])
    
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
    
    def get_video_title(self, url):
        """Get video title from URL using yt-dlp"""
        try:
            cmd = ['yt-dlp', '--get-title', '--no-playlist', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                title = result.stdout.strip()
                # Clean up title for display
                title = re.sub(r'[^\w\s\-\.]', '', title)[:50]  # Remove special chars and limit length
                return title if title else "Unknown Title"
            else:
                return "Unknown Title"
        except:
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
        self.log_message(f"🔍 Getting video information for: {url}")
        title = self.get_video_title(url)
        
        # Add to queue
        queue_item = {
            'url': url,
            'title': title,
            'quality': self.quality_var.get(),
            'format': self.format_var.get(),
            'status': 'Queued',
            'added_time': datetime.now().strftime("%H:%M:%S")
        }
        
        self.download_queue.append(queue_item)
        self.update_queue_display()
        
        # Clear URL field
        self.url_var.set("")
        
        self.log_message(f"✅ Added to queue: {title}")
        messagebox.showinfo("Added to Queue", f"Video added to download queue:\n{title}")
    
    def update_queue_display(self):
        """Update the queue display"""
        # Clear existing items
        for item in self.queue_tree.get_children():
            self.queue_tree.delete(item)
        
        # Add queue items
        for i, item in enumerate(self.download_queue):
            status_icon = "⏳" if item['status'] == 'Queued' else "🔄" if item['status'] == 'Downloading' else "✅" if item['status'] == 'Completed' else "❌"
            self.queue_tree.insert('', 'end', values=(
                f"{status_icon} {item['status']}",
                item['title'][:40] + "..." if len(item['title']) > 40 else item['title'],
                item['quality'],
                item['format']
            ))
    
    def start_queue(self):
        """Start processing the download queue"""
        if not self.download_queue:
            messagebox.showwarning("Empty Queue", "No videos in the download queue")
            return
        
        if self.is_downloading:
            messagebox.showwarning("Already Downloading", "A download is already in progress")
            return
        
        # Start queue processing in a separate thread
        self.queue_thread = threading.Thread(target=self.process_queue, daemon=True)
        self.queue_thread.start()
    
    def process_queue(self):
        """Process the download queue"""
        self.is_downloading = True
        self.update_status("Processing queue...", self.colors['warning'])
        
        for i, item in enumerate(self.download_queue):
            if item['status'] == 'Queued':
                self.current_download = item
                item['status'] = 'Downloading'
                self.update_queue_display()
                
                self.log_message(f"📥 Starting download {i+1}/{len(self.download_queue)}: {item['title']}")
                
                # Download the video
                success = self.download_single_video(item)
                
                if success:
                    item['status'] = 'Completed'
                    self.log_message(f"✅ Completed: {item['title']}")
                else:
                    item['status'] = 'Failed'
                    self.log_message(f"❌ Failed: {item['title']}")
                
                self.update_queue_display()
                
                # Add to history
                self.add_to_history(item['url'], item['title'], item['quality'], item['format'], 
                                  "Success" if success else "Failed")
        
        self.is_downloading = False
        self.current_download = None
        self.update_status("Queue completed!", self.colors['primary'])
        self.log_message("🎉 All downloads completed!")
    
    def download_single_video(self, item):
        """Download a single video from the queue"""
        try:
            url = item['url']
            quality = item['quality']
            format_type = item['format']
            download_path = self.path_var.get()
            
            # Ensure download path exists
            os.makedirs(download_path, exist_ok=True)
            
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
                '--retries', '10',
                '--fragment-retries', '10',
                '--socket-timeout', '30',
                '--http-chunk-size', '10485760',
                '--concurrent-fragments', '4',
                '--buffer-size', '65536',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ])
            
            if format_type != 'best':
                cmd.extend(['--merge-output-format', format_type])
            
            cmd.append(url)
            
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
            for line in process.stdout:
                line = line.strip()
                if line:
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
            
            # Wait for process to complete
            return_code = process.wait()
            
            return return_code == 0
            
        except Exception as e:
            self.log_message(f"❌ Error downloading {item['title']}: {str(e)}")
            return False
    
    def clear_queue(self):
        """Clear the download queue"""
        if self.download_queue and not self.is_downloading:
            self.download_queue.clear()
            self.update_queue_display()
            self.log_message("🗑️ Queue cleared")
        elif self.is_downloading:
            messagebox.showwarning("Cannot Clear", "Cannot clear queue while downloading")
    
    def pause_queue(self):
        """Pause the download queue"""
        if self.is_downloading:
            self.is_downloading = False
            self.update_status("Queue paused", self.colors['warning'])
            self.log_message("⏸️ Queue paused")
        else:
            messagebox.showinfo("Queue Status", "Queue is not currently running")
    
    def add_to_history(self, url, title, quality, format_type, status):
        """Add download to history with proper title"""
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
            self.history_window.geometry("1200x800")
            self.history_window.configure(bg=self.colors['background'])
            
            # History list
            history_frame = tk.Frame(self.history_window, bg=self.colors['card'])
            history_frame.pack(fill=tk.BOTH, expand=True, padx=32, pady=32)
            
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
        messagebox.showinfo("Settings", "Settings panel coming soon!\n\nFeatures to be added:\n• Default download quality\n• Auto-download folder\n• VPN optimization settings\n• Queue management preferences")
    
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
    app = YouTubeDownloaderQueue(root)
    
    # Load initial history
    app.update_history_display()
    
    root.mainloop()

if __name__ == "__main__":
    main()
