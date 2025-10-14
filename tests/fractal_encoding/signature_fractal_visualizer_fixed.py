#!/usr/bin/env python3
"""
Signature to Visual Fractal - Fixed version
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import hashlib

def create_signature_like_image():
    """Create a simulated signature since we don't have a real image"""
    img = Image.new('L', (400, 200), color=255)
    draw = ImageDraw.Draw(img)
    
    points = [
        (50, 100), (80, 90), (120, 110), (160, 85), 
        (200, 105), (240, 95), (280, 115), (320, 100), (350, 110)
    ]
    
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=0, width=3)
    
    draw.arc([330, 90, 370, 130], 0, 180, fill=0, width=2)
    return img

def signature_to_fractal_seed(signature_image):
    """Convert signature image features to fractal seed"""
    img_array = np.array(signature_image)
    
    features = {}
    ink_pixels = img_array < 128
    features['ink_density'] = np.sum(ink_pixels) / ink_pixels.size
    
    vertical_profile = np.sum(ink_pixels, axis=1)
    horizontal_profile = np.sum(ink_pixels, axis=0)
    
    features['vertical_center'] = np.argmax(vertical_profile) / len(vertical_profile)
    features['horizontal_center'] = np.argmax(horizontal_profile) / len(horizontal_profile)
    features['stroke_rhythm'] = np.std(horizontal_profile) / np.mean(horizontal_profile)
    
    feature_string = ''.join(f"{k}:{v:.6f}" for k, v in features.items())
    seed = hashlib.sha256(feature_string.encode()).hexdigest()[:16]
    
    return seed, features

def generate_visual_fractal(seed, size=100):
    """Generate a visual fractal from seed - FIXED VERSION"""
    rng = np.random.RandomState(int(seed, 16) % (2**32))
    
    # Use a simpler, more robust fractal algorithm
    fractal = np.zeros((size, size))
    
    # Start with random corners
    fractal[0, 0] = rng.uniform(-1, 1)
    fractal[0, -1] = rng.uniform(-1, 1)
    fractal[-1, 0] = rng.uniform(-1, 1)
    fractal[-1, -1] = rng.uniform(-1, 1)
    
    step = size - 1
    scale = 1.0
    
    while step > 1:
        half = step // 2
        
        # Diamond step
        for x in range(half, size, step):
            for y in range(half, size, step):
                fractal[x, y] = (
                    fractal[x - half, y - half] +
                    fractal[x - half, y + half] +
                    fractal[x + half, y - half] + 
                    fractal[x + half, y + half]
                ) / 4 + rng.uniform(-scale, scale)
        
        # Square step - with proper bounds checking
        for x in range(0, size, half):
            for y in range((x + half) % step, size, step):
                total = 0
                count = 0
                
                if x >= half:
                    total += fractal[x - half, y]
                    count += 1
                if x + half < size:
                    total += fractal[x + half, y] 
                    count += 1
                if y >= half:
                    total += fractal[x, y - half]
                    count += 1
                if y + half < size:
                    total += fractal[x, y + half]
                    count += 1
                
                if count > 0:
                    fractal[x, y] = total / count + rng.uniform(-scale, scale)
        
        step = half
        scale *= 0.5
    
    return fractal

def visualize_transformation(signature_img, fractal_img, features, seed):
    """Create visualization of signature to fractal transformation"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Original Signature
    axes[0, 0].imshow(signature_img, cmap='gray', aspect='auto')
    axes[0, 0].set_title('Your Signature', fontsize=16, fontweight='bold')
    axes[0, 0].axis('off')
    
    # Plot 2: Signature Features
    feature_names = list(features.keys())
    feature_values = list(features.values())
    axes[0, 1].bar(feature_names, feature_values, color='skyblue', alpha=0.7)
    axes[0, 1].set_title('Signature Features Extracted', fontsize=14)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Generated Visual Fractal
    im = axes[1, 0].imshow(fractal_img, cmap='plasma', aspect='auto')
    axes[1, 0].set_title('Your Signature Fractal', fontsize=16, fontweight='bold')
    axes[1, 0].axis('off')
    plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
    
    # Plot 4: Transformation Bridge
    axes[1, 1].text(0.5, 0.7, f'Fractal Seed:\n{seed}', 
                    ha='center', va='center', fontsize=12, fontfamily='monospace')
    axes[1, 1].text(0.5, 0.4, 'This seed becomes:\n• Audio protection DNA\n• Creative identity\n• Legal proof chain', 
                    ha='center', va='center', fontsize=11)
    axes[1, 1].set_title('The Sovereign Bridge', fontsize=14)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('tests/fractal_encoding/SIGNATURE_FRACTAL_VISUALIZATION.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    
    return fig

print("🖋️ SIGNATURE TO FRACTAL VISUALIZATION - FIXED")
print("=" * 50)

# Create simulated signature
print("1. Creating simulated signature...")
signature_img = create_signature_like_image()

# Convert to fractal seed
print("2. Analyzing signature features...")
seed, features = signature_to_fractal_seed(signature_img)

# Generate visual fractal
print("3. Generating visual fractal...")
fractal_img = generate_visual_fractal(seed)

# Create visualization
print("4. Creating transformation visualization...")
fig = visualize_transformation(signature_img, fractal_img, features, seed)

print("✅ VISUALIZATION COMPLETE!")
print("📊 Saved: tests/fractal_encoding/SIGNATURE_FRACTAL_VISUALIZATION.png")
print(f"🔑 Your Fractal Seed: {seed}")

print("\n🔗 THE SOVEREIGN BRIDGE:")
print("Physical World → Digital World → Creative World")
print("Your Signature → Fractal Seed → Audio Protection")
print("Legal Identity → Math Identity → Creative Identity")

print("\n🎨 This visualization shows how your UNCHANGING signature")
print("becomes the foundation for your EVER-CHANGING creative works!")
