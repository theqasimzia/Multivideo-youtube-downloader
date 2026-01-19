// Popup script

const API_URL = 'http://localhost:5000/api';

// Check API server status
async function checkStatus() {
  try {
    const response = await fetch(`${API_URL}/health`);
    const data = await response.json();
    
    const statusDiv = document.getElementById('status');
    const addBtn = document.getElementById('addCurrentBtn');
    
    if (data.status === 'ok') {
      statusDiv.textContent = '✅ Connected to app';
      statusDiv.className = 'status connected';
      addBtn.disabled = false;
    } else {
      throw new Error('Server not responding');
    }
  } catch (error) {
    const statusDiv = document.getElementById('status');
    const addBtn = document.getElementById('addCurrentBtn');
    
    statusDiv.textContent = '❌ App not running';
    statusDiv.className = 'status disconnected';
    addBtn.disabled = true;
  }
}

// Add current video to queue
document.getElementById('addCurrentBtn').addEventListener('click', async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
    
    if (!url.includes('youtube.com')) {
      alert('Please navigate to a YouTube video page');
      return;
    }
    
    const response = await fetch(`${API_URL}/add-to-queue`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        quality: 'best',
        format: 'mp4'
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      alert('Video added to download queue!');
    } else {
      alert('Error: ' + data.message);
    }
  } catch (error) {
    alert('Error: Make sure the app is running!');
  }
});

// Open app (if running locally)
document.getElementById('openAppBtn').addEventListener('click', () => {
  chrome.tabs.create({ url: 'http://localhost:5000' });
});

// Check status on load
checkStatus();
setInterval(checkStatus, 5000);
