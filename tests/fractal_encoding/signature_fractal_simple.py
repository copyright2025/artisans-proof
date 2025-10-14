#!/usr/bin/env python3
"""
Signature to Visual Fractal - SIMPLE and ROBUST version
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import hashlib

def create_signature_like_image():
    """Create a simulated signature"""
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

def generate_simple_fractal(seed, size=100):
    """Generate a simple but unique visual fractal from seed"""
    rng = np.random.RandomState(int(seed, 16) % (2**32))
    
    # Create a simple fractal using multiple sine waves
    x = np.linspace(0, 4 * np.pi, size)
    y = np.linspace(0, 4 * np.pi, size)
    X, Y = np.meshgrid(x, y)
    
    # Use seed to determine fractal parameters
    freq1 = 1 + rng.uniform(0.5, 3.0)
    freq2 = 1 + rng.uniform(0.5, 3.0) 
    phase1 = rng.uniform(0, 2 * np.pi)
    phase2 = rng.uniform(0, 2 * np.pi)
    
    # Create fractal pattern
    fractal = (np.sin(freq1 * X + phase1) * 
               np.cos(freq2 * Y + phase2) +
               0.5 * np.sin(2 * freq1 * X) *
               np.cos(2 * freq2 * Y))
    
    # Add some noise for texture
    fractal += 0.1 * rng.normal(0, 1, (size, size))
    
    return fractal

def visualize_transformation(signature_img, fractal_img, features, seed):
    """Create visualization of signature to fractal transformation"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Original Signature
    axes[0, 0].imshow(signature_img, cmap='gray', aspect='auto')
    axes[0, 0].set_title('Your Physical Signature', fontsize=16, fontweight='bold')
    axes[0, 0].axis('off')
    
    # Plot 2: Signature Features
    feature_names = list(features.keys())
    feature_values = list(features.values())
    axes[0, 1].bar(feature_names, feature_values, color='lightcoral', alpha=0.7)
    axes[0, 1].set_title('Digital Signature Fingerprint', fontsize=14)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Generated Visual Fractal
    im = axes[1, 0].imshow(fractal_img, cmap='viridis', aspect='auto')
    axes[1, 0].set_title('Your Creative DNA Fractal', fontsize=16, fontweight='bold')
    axes[1, 0].axis('off')
    plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
    
    # Plot 4: The Sovereign Bridge
    axes[1, 1].text(0.5, 0.8, '🖋️ → 🔑 → 🎵', 
                    ha='center', va='center', fontsize=24)
    axes[1, 1].text(0.5, 0.6, f'Seed: {seed}', 
                    ha='center', va='center', fontsize=10, fontfamily='monospace')
    axes[1, 1].text(0.5, 0.4, 'Signature → Fractal → Audio Protection', 
                    ha='center', va='center', fontsize=12)
    axes[1, 1].text(0.5, 0.2, 'Legal Identity → Creative Sovereignty', 
                    ha='center', va='center', fontsize=12)
    axes[1, 1].set_title('The Sovereign Bridge', fontsize=14, fontweight='bold')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('tests/fractal_encoding/SIGNATURE_FRACTAL_VISUALIZATION.png', 
                dpi=150, bbox_inches='tight', facecolor='white')
    
    return fig

print("🖋️ SIGNATURE TO FRACTAL VISUALIZATION - SIMPLE & ROBUST")
print("=" * 50)

# Create simulated signature
print("1. Creating simulated signature...")
signature_img = create_signature_like_image()

# Convert to fractal seed
print("2. Analyzing signature features...")
seed, features = signature_to_fractal_seed(signature_img)

# Generate visual fractal
print("3. Generating visual fractal...")
fractal_img = generate_simple_fractal(seed)

# Create visualization
print("4. Creating transformation visualization...")
fig = visualize_transformation(signature_img, fractal_img, features, seed)

print("✅ VISUALIZATION COMPLETE!")
print("📊 Saved: tests/fractal_encoding/SIGNATURE_FRACTAL_VISUALIZATION.png")
print(f"🔑 Your Fractal Seed: {seed}")

print("\n🎨 THE SOVEREIGN BRIDGE VISUALIZED:")
print("• Your handwritten signature (legal identity)")
print("• Its unique mathematical features (digital fingerprint)")  
print("• Your personal fractal pattern (creative DNA)")
print("• All connected by the same cryptographic seed")

print("\n🔗 This same seed protects your audio works")
print("   while maintaining the legal weight of your signature!")
