// Firefox popup script
const API_URL = 'http://localhost:5000/api';

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

document.getElementById('addCurrentBtn').addEventListener('click', async () => {
  try {
    const tabs = await browser.tabs.query({ active: true, currentWindow: true });
    const url = tabs[0].url;
    
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

document.getElementById('openAppBtn').addEventListener('click', () => {
  browser.tabs.create({ url: 'http://localhost:5000' });
});

checkStatus();
setInterval(checkStatus, 5000);
