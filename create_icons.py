"""
Create placeholder icons for browser extension
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a simple icon with download symbol"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (34, 197, 94, 255))  # Green background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple download arrow
    # Arrow pointing down
    arrow_size = size // 3
    center_x, center_y = size // 2, size // 2
    
    # Draw arrow (triangle pointing down)
    points = [
        (center_x, center_y + arrow_size // 2),  # Bottom point
        (center_x - arrow_size // 2, center_y - arrow_size // 2),  # Top left
        (center_x + arrow_size // 2, center_y - arrow_size // 2)   # Top right
    ]
    draw.polygon(points, fill=(255, 255, 255, 255))  # White arrow
    
    # Draw horizontal line
    line_y = center_y + arrow_size // 2 + 5
    draw.line([(center_x - arrow_size // 2, line_y), 
               (center_x + arrow_size // 2, line_y)], 
              fill=(255, 255, 255, 255), width=3)
    
    # Save icon
    img.save(output_path, 'PNG')
    print(f"Created {output_path} ({size}x{size})")

# Create icons for Chrome
chrome_dir = "browser_extension/chrome"
os.makedirs(chrome_dir, exist_ok=True)

create_icon(16, os.path.join(chrome_dir, "icon16.png"))
create_icon(48, os.path.join(chrome_dir, "icon48.png"))
create_icon(128, os.path.join(chrome_dir, "icon128.png"))

# Create icons for Firefox
firefox_dir = "browser_extension/firefox"
os.makedirs(firefox_dir, exist_ok=True)

create_icon(16, os.path.join(firefox_dir, "icon16.png"))
create_icon(48, os.path.join(firefox_dir, "icon48.png"))
create_icon(128, os.path.join(firefox_dir, "icon128.png"))

print("\nAll icons created successfully!")
