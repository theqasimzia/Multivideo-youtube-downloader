"""
Flask API Server for Browser Extension Integration
Handles requests from browser extension to add videos to download queue
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime
import subprocess
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for browser extension

# Configuration
QUEUE_FILE = "download_queue.json"
CONFIG_FILE = "config.json"

def load_queue():
    """Load download queue from file"""
    try:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_queue(queue):
    """Save download queue to file"""
    try:
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=2)
    except:
        pass

def get_video_title(url):
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

def load_config():
    """Load configuration"""
    default_config = {
        'default_quality': 'best',
        'default_format': 'mp4',
        'default_path': str(Path.home() / "Downloads")
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return {**default_config, **config}
    except:
        pass
    return default_config

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API server is running'})

@app.route('/api/add-to-queue', methods=['POST'])
def add_to_queue():
    """Add video to download queue"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
        
        # Validate YouTube URL
        if not url.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'https://youtube.com/')):
            return jsonify({'status': 'error', 'message': 'Invalid YouTube URL'}), 400
        
        # Get video title
        title = get_video_title(url)
        
        # Load config
        config = load_config()
        
        # Create queue item
        queue_item = {
            'url': url,
            'title': title,
            'quality': data.get('quality', config.get('default_quality', 'best')),
            'format': data.get('format', config.get('default_format', 'mp4')),
            'status': 'Queued',
            'added_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source': 'browser_extension'
        }
        
        # Load queue and add item
        queue = load_queue()
        queue.append(queue_item)
        save_queue(queue)
        
        return jsonify({
            'status': 'success',
            'message': f'Video added to queue: {title}',
            'queue_item': queue_item
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-queue', methods=['GET'])
def get_queue():
    """Get current download queue"""
    try:
        queue = load_queue()
        return jsonify({'status': 'success', 'queue': queue})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/clear-queue', methods=['POST'])
def clear_queue():
    """Clear download queue"""
    try:
        save_queue([])
        return jsonify({'status': 'success', 'message': 'Queue cleared'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-video-info', methods=['POST'])
def get_video_info():
    """Get video information"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
        
        title = get_video_title(url)
        
        return jsonify({
            'status': 'success',
            'title': title,
            'url': url
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask API server...")
    print("📡 Server running on http://localhost:5000")
    print("🌐 Browser extension can now connect to this server")
    app.run(host='localhost', port=5000, debug=False)
