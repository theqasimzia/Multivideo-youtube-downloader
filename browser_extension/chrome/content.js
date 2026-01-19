// Content script to add download button to YouTube pages

const API_URL = 'http://localhost:5000/api';

// Create download button
function createDownloadButton() {
  // Check if button already exists
  if (document.getElementById('yt-downloader-btn')) {
    return;
  }

  // Find YouTube's action buttons container
  const actionButtons = document.querySelector('#menu-container, #top-level-buttons-computed, ytd-menu-renderer');
  
  if (!actionButtons) {
    // Try alternative selectors
    const alternatives = [
      document.querySelector('#actions'),
      document.querySelector('.ytd-video-primary-info-renderer'),
      document.querySelector('#watch-header')
    ];
    
    for (const alt of alternatives) {
      if (alt) {
        actionButtons = alt;
        break;
      }
    }
  }

  if (actionButtons) {
    const button = document.createElement('button');
    button.id = 'yt-downloader-btn';
    button.className = 'yt-downloader-button';
    button.innerHTML = '⬇️ Download';
    button.title = 'Add to Download Queue';
    
    button.addEventListener('click', async () => {
      const url = window.location.href;
      await addToQueue(url);
    });
    
    // Insert button
    if (actionButtons.parentNode) {
      actionButtons.parentNode.insertBefore(button, actionButtons.nextSibling);
    } else {
      actionButtons.appendChild(button);
    }
  }
}

// Add video to download queue
async function addToQueue(url) {
  try {
    const button = document.getElementById('yt-downloader-btn');
    if (button) {
      button.disabled = true;
      button.innerHTML = '⏳ Adding...';
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
      if (button) {
        button.innerHTML = '✅ Added!';
        button.style.backgroundColor = '#22c55e';
        setTimeout(() => {
          button.innerHTML = '⬇️ Download';
          button.style.backgroundColor = '';
          button.disabled = false;
        }, 2000);
      }
      
      // Show notification
      showNotification('Video added to download queue!', 'success');
    } else {
      throw new Error(data.message || 'Failed to add to queue');
    }
  } catch (error) {
    console.error('Error adding to queue:', error);
    
    const button = document.getElementById('yt-downloader-btn');
    if (button) {
      button.innerHTML = '❌ Error';
      button.style.backgroundColor = '#ef4444';
      setTimeout(() => {
        button.innerHTML = '⬇️ Download';
        button.style.backgroundColor = '';
        button.disabled = false;
      }, 2000);
    }
    
    showNotification('Failed to add to queue. Make sure the app is running!', 'error');
  }
}

// Show notification
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `yt-downloader-notification yt-downloader-${type}`;
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.classList.add('show');
  }, 10);

  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

// Check if API server is running
async function checkAPIServer() {
  try {
    const response = await fetch(`${API_URL}/health`);
    const data = await response.json();
    return data.status === 'ok';
  } catch (error) {
    return false;
  }
}

// Initialize
if (window.location.hostname.includes('youtube.com')) {
  // Wait for page to load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createDownloadButton);
  } else {
    createDownloadButton();
  }

  // Re-create button on navigation (YouTube SPA)
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      setTimeout(createDownloadButton, 1000);
    }
  }).observe(document, { subtree: true, childList: true });
}
