#!/usr/bin/env python3
"""
Script to create Level 2 underground background using Pillow
Creates a PNG image with underground theme for Mario Level 2
"""

from PIL import Image, ImageDraw
import os

def create_underground_background():
    """Create an underground-themed background for Level 2"""
    
    # Image dimensions (same as Level 1 for consistency)
    width = 3392  # Level 1 width
    height = 480  # Level 1 height
    
    # Create new image with dark underground background
    img = Image.new('RGB', (width, height), color='#1a1a2e')  # Dark blue-purple
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (darker at top, lighter at bottom)
    for y in range(height):
        # Gradient from dark blue-purple to dark brown
        ratio = y / height
        r = int(26 + (40 - 26) * ratio)  # 26 to 40
        g = int(26 + (30 - 26) * ratio)  # 26 to 30
        b = int(46 + (20 - 46) * ratio)  # 46 to 20
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Ground level
    ground_y = 400
    ground_height = height - ground_y
    
    # Draw underground ground with brick pattern
    brick_color = '#4a3728'  # Dark brown
    mortar_color = '#3a2718'  # Darker brown
    
    # Fill ground area
    draw.rectangle([0, ground_y, width, height], fill=brick_color)
    
    # Add brick pattern
    brick_width = 32
    brick_height = 16
    
    for y in range(ground_y, height, brick_height):
        for x in range(0, width, brick_width):
            # Offset every other row
            offset = (brick_width // 2) if ((y - ground_y) // brick_height) % 2 else 0
            brick_x = x + offset
            
            if brick_x < width:
                # Draw mortar lines
                draw.rectangle([brick_x, y, brick_x + brick_width - 2, y + brick_height - 2], 
                             fill=brick_color)
                draw.rectangle([brick_x + brick_width - 2, y, brick_x + brick_width, y + brick_height], 
                             fill=mortar_color)
                draw.rectangle([brick_x, y + brick_height - 2, brick_x + brick_width, y + brick_height], 
                             fill=mortar_color)
    
    # Add underground pipes (green pipes with darker shading)
    pipe_color = '#2d5016'  # Dark green
    pipe_highlight = '#3d6026'  # Lighter green
    pipe_shadow = '#1d4006'  # Darker green
    
    # Pipe positions for underground level
    pipes = [
        {'x': 448, 'y': ground_y - 128, 'width': 64, 'height': 128},  # First pipe
        {'x': 896, 'y': ground_y - 96, 'width': 64, 'height': 96},   # Second pipe (shorter)
        {'x': 1344, 'y': ground_y - 160, 'width': 64, 'height': 160}, # Third pipe (taller)
        {'x': 1792, 'y': ground_y - 112, 'width': 64, 'height': 112}, # Fourth pipe
        {'x': 2240, 'y': ground_y - 144, 'width': 64, 'height': 144}, # Fifth pipe
        {'x': 2688, 'y': ground_y - 128, 'width': 64, 'height': 128}, # Sixth pipe
    ]
    
    for pipe in pipes:
        x, y, w, h = pipe['x'], pipe['y'], pipe['width'], pipe['height']
        
        # Main pipe body
        draw.rectangle([x, y, x + w, y + h], fill=pipe_color)
        
        # Pipe highlights (left side)
        draw.rectangle([x, y, x + 8, y + h], fill=pipe_highlight)
        
        # Pipe shadows (right side)
        draw.rectangle([x + w - 8, y, x + w, y + h], fill=pipe_shadow)
        
        # Pipe top (lip)
        lip_height = 16
        draw.rectangle([x - 8, y - lip_height, x + w + 8, y], fill=pipe_color)
        draw.rectangle([x - 8, y - lip_height, x, y], fill=pipe_highlight)
        draw.rectangle([x + w, y - lip_height, x + w + 8, y], fill=pipe_shadow)
    
    # Add underground platforms
    platform_color = '#5a4a3a'  # Brown stone
    platform_highlight = '#6a5a4a'
    platform_shadow = '#4a3a2a'
    
    platforms = [
        {'x': 640, 'y': 320, 'width': 128, 'height': 32},
        {'x': 1088, 'y': 280, 'width': 96, 'height': 32},
        {'x': 1536, 'y': 240, 'width': 160, 'height': 32},
        {'x': 1984, 'y': 300, 'width': 128, 'height': 32},
        {'x': 2432, 'y': 260, 'width': 96, 'height': 32},
    ]
    
    for platform in platforms:
        x, y, w, h = platform['x'], platform['y'], platform['width'], platform['height']
        
        # Main platform
        draw.rectangle([x, y, x + w, y + h], fill=platform_color)
        
        # Platform highlights (top)
        draw.rectangle([x, y, x + w, y + 4], fill=platform_highlight)
        
        # Platform shadows (bottom)
        draw.rectangle([x, y + h - 4, x + w, y + h], fill=platform_shadow)
    
    # Add stalactites (hanging from ceiling)
    stalactite_color = '#3a3a3a'  # Gray stone
    stalactite_positions = [
        {'x': 320, 'length': 60},
        {'x': 768, 'length': 80},
        {'x': 1216, 'length': 45},
        {'x': 1664, 'length': 70},
        {'x': 2112, 'length': 55},
        {'x': 2560, 'length': 65},
        {'x': 2944, 'length': 50},
    ]
    
    for stalactite in stalactite_positions:
        x = stalactite['x']
        length = stalactite['length']
        
        # Draw triangular stalactite
        points = [
            (x, 0),  # Top center
            (x - 12, 0),  # Top left
            (x + 12, 0),  # Top right
            (x, length)  # Bottom point
        ]
        draw.polygon(points, fill=stalactite_color)
    
    # Add underground crystals/gems
    crystal_color = '#4a4aff'  # Blue crystal
    crystal_positions = [
        {'x': 512, 'y': 350},
        {'x': 1024, 'y': 330},
        {'x': 1472, 'y': 310},
        {'x': 1920, 'y': 340},
        {'x': 2368, 'y': 320},
        {'x': 2816, 'y': 360},
    ]
    
    for crystal in crystal_positions:
        x, y = crystal['x'], crystal['y']
        
        # Draw diamond-shaped crystal
        points = [
            (x, y - 8),      # Top
            (x - 6, y),      # Left
            (x, y + 8),      # Bottom
            (x + 6, y)       # Right
        ]
        draw.polygon(points, fill=crystal_color)
    
    # Add some underground vegetation (mushrooms)
    mushroom_cap = '#8b4513'  # Brown cap
    mushroom_stem = '#deb887'  # Light brown stem
    
    mushroom_positions = [
        {'x': 384, 'y': ground_y - 20},
        {'x': 832, 'y': ground_y - 16},
        {'x': 1280, 'y': ground_y - 18},
        {'x': 1728, 'y': ground_y - 22},
        {'x': 2176, 'y': ground_y - 20},
        {'x': 2624, 'y': ground_y - 16},
    ]
    
    for mushroom in mushroom_positions:
        x, y = mushroom['x'], mushroom['y']
        
        # Mushroom stem
        draw.rectangle([x - 3, y, x + 3, ground_y], fill=mushroom_stem)
        
        # Mushroom cap
        draw.ellipse([x - 8, y - 12, x + 8, y + 4], fill=mushroom_cap)
    
    return img

def main():
    """Main function to create and save the Level 2 background"""
    print("Creating Level 2 underground background...")
    
    # Create the background image
    background = create_underground_background()
    
    # Save to resources/graphics directory
    output_path = os.path.join('resources', 'graphics', 'level_2.png')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the image
    background.save(output_path, 'PNG')
    
    print(f"Level 2 background saved to: {output_path}")
    print(f"Image dimensions: {background.size}")

if __name__ == "__main__":
    main()