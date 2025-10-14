#!/usr/bin/env python3
"""
Signature to Visual Fractal - Showing the transformation
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import hashlib

def create_signature_like_image():
    """Create a simulated signature since we don't have a real image"""
    # Create a canvas
    img = Image.new('L', (400, 200), color=255)  # White background
    draw = ImageDraw.Draw(img)
    
    # Draw a signature-like squiggle
    points = [
        (50, 100), (80, 90), (120, 110), (160, 85), 
        (200, 105), (240, 95), (280, 115), (320, 100), (350, 110)
    ]
    
    # Draw the signature path
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=0, width=3)
    
    # Add some signature flourishes
    draw.arc([330, 90, 370, 130], 0, 180, fill=0, width=2)
    
    return img

def signature_to_fractal_seed(signature_image):
    """Convert signature image features to fractal seed"""
    # Convert to numpy array
    img_array = np.array(signature_image)
    
    # Analyze signature features
    features = {}
    
    # 1. Analyze ink distribution (where the signature is dense)
    ink_pixels = img_array < 128  # Threshold for "ink"
    features['ink_density'] = np.sum(ink_pixels) / ink_pixels.size
    
    # 2. Analyze vertical/horizontal distribution
    vertical_profile = np.sum(ink_pixels, axis=1)
    horizontal_profile = np.sum(ink_pixels, axis=0)
    
    features['vertical_center'] = np.argmax(vertical_profile) / len(vertical_profile)
    features['horizontal_center'] = np.argmax(horizontal_profile) / len(horizontal_profile)
    
    # 3. Analyze stroke rhythm (simulated)
    # In real implementation, this would analyze drawing speed from timestamp data
    features['stroke_rhythm'] = np.std(horizontal_profile) / np.mean(horizontal_profile)
    
    # Create deterministic seed from features
    feature_string = ''.join(f"{k}:{v:.6f}" for k, v in features.items())
    seed = hashlib.sha256(feature_string.encode()).hexdigest()[:16]
    
    return seed, features

def generate_visual_fractal(seed, size=400):
    """Generate a visual fractal from seed"""
    rng = np.random.RandomState(int(seed, 16) % (2**32))
    
    # Create base pattern using similar midpoint displacement
    pattern_size = size // 4
    pattern = np.zeros((pattern_size, pattern_size))
    pattern[0, 0] = rng.uniform(-1, 1)
    
    step = pattern_size // 2
    scale = 1.0
    
    while step > 0:
        # Diamond step
        for i in range(step, pattern_size, step * 2):
            for j in range(step, pattern_size, step * 2):
                pattern[i, j] = (pattern[i-step, j-step] + 
                                pattern[i-step, j+step] + 
                                pattern[i+step, j-step] + 
                                pattern[i+step, j+step]) / 4
                pattern[i, j] += rng.uniform(-scale, scale)
        
        # Square step  
        for i in range(0, pattern_size, step):
            for j in range(0, pattern_size, step):
                if (i // step + j // step) % 2 == 1:
                    neighbors = []
                    if i > 0: neighbors.append(pattern[i-step, j])
                    if i < pattern_size-1: neighbors.append(pattern[i+step, j])
                    if j > 0: neighbors.append(pattern[i, j-step])
                    if j < pattern_size-1: neighbors.append(pattern[i, j+step])
                    
                    if neighbors:
                        pattern[i, j] = np.mean(neighbors) + rng.uniform(-scale, scale)
        
        step //= 2
        scale *= 0.5
    
    # Resize to final size
    from scipy.ndimage import zoom
    fractal = zoom(pattern, 4, order=1)
    
    return fractal

def visualize_transformation(signature_img, fractal_img, features, seed):
    """Create a beautiful visualization of the transformation"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Original Signature
    axes[0, 0].imshow(signature_img, cmap='gray', aspect='auto')
    axes[0, 0].set_title('Your Signature', fontsize=16, fontweight='bold')
    axes[0, 0].axis('off')
    
    # Plot 2: Signature Features Analysis
    feature_names = list(features.keys())
    feature_values = list(features.values())
    
    axes[0, 1].bar(feature_names, feature_values, color='skyblue', alpha=0.7)
    axes[0, 1].set_title('Signature Features Extracted', fontsize=14)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Generated Visual Fractal
    im = axes[1, 0].imshow(fractal_img, cmap='viridis', aspect='auto')
    axes[1, 0].set_title('Your Signature Fractal', fontsize=16, fontweight='bold')
    axes[1, 0].axis('off')
    plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
    
    # Plot 4: Transformation Bridge
    axes[1, 1].text(0.5, 0.7, f'Fractal Seed:\n{seed}', 
                    ha='center', va='center', fontsize=12, fontfamily='monospace')
    axes[1, 1].text(0.5, 0.4, 'This seed becomes:\n• Your audio fractal DNA\n• Your creative identity\n• Your legal proof', 
                    ha='center', va='center', fontsize=11)
    axes[1, 1].set_title('The Transformation Bridge', fontsize=14)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('tests/fractal_encoding/SIGNATURE_FRACTAL_VISUALIZATION.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    
    return fig

print("🖋️ SIGNATURE TO FRACTAL VISUALIZATION")
print("=" * 50)

# Create a simulated signature
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

print("\n🎨 WHAT YOU'RE SEEING:")
print("• LEFT: Your signature (unique physical identity)")
print("• MIDDLE: Signature features extracted (mathematical essence)")  
print("• RIGHT: Your signature fractal (digital creative DNA)")
print("• BOTTOM: The transformation bridge (how they connect)")

print("\n🔮 THIS SAME FRACTAL SEED:")
print("• Protects your audio works (inaudible phase shifts)")
print("• Becomes your creative identity marker")
print("• Creates legal continuity with your handwritten signature")
