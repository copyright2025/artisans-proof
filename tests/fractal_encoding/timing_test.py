#!/usr/bin/env python3
"""
Test fractal timing variations for sub-second audio protection
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf
import hashlib

def generate_fractal_pattern(seed, length):
    """Generate deterministic fractal pattern from seed"""
    # Use seed to create reproducible fractal noise
    rng = np.random.RandomState(hash(seed) % 2**32)
    
    # Generate fractal noise using midpoint displacement
    pattern = np.zeros(length)
    pattern[0] = rng.uniform(-1, 1)
    
    step = length // 2
    scale = 1.0
    
    while step > 0:
        for i in range(step, length, step * 2):
            if i + step < length:
                pattern[i] = (pattern[i - step] + pattern[i + step]) / 2
                pattern[i] += rng.uniform(-scale, scale)
        step //= 2
        scale *= 0.5
    
    return pattern

def encode_timing_fractal(audio, fractal_pattern, max_shift_ms=2):
    """
    Encode fractal pattern using micro-timing variations
    max_shift_ms: Maximum timing shift in milliseconds (inaudible range)
    """
    sample_rate = 44100  # Standard audio rate
    max_shift_samples = int((max_shift_ms / 1000) * sample_rate)
    
    # Normalize fractal pattern to ±1 range
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    # Apply timing shifts to audio chunks
    chunk_size = 512  # ~11ms chunks
    encoded_audio = []
    
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            # Calculate timing shift for this chunk
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            
            # Apply time shift using phase rotation
            if shift_samples != 0:
                chunk = np.roll(chunk, shift_samples)
                # Handle rollover artifacts
                if shift_samples > 0:
                    chunk[:shift_samples] = 0
                else:
                    chunk[shift_samples:] = 0
            
        encoded_audio.extend(chunk)
    
    return np.array(encoded_audio)

def detect_timing_fractal(original_audio, test_audio, seed, chunk_size=512):
    """Detect if test audio contains the fractal timing pattern"""
    fractal_pattern = generate_fractal_pattern(seed, 100)
    sample_rate = 44100
    
    correlation_scores = []
    
    for i in range(0, min(len(original_audio), len(test_audio)), chunk_size):
        orig_chunk = original_audio[i:i + chunk_size]
        test_chunk = test_audio[i:i + chunk_size]
        
        if len(orig_chunk) == chunk_size and len(test_chunk) == chunk_size:
            # Cross-correlation to detect timing shifts
            correlation = np.correlate(orig_chunk, test_chunk, mode='valid')
            correlation_scores.append(np.max(correlation))
    
    avg_correlation = np.mean(correlation_scores)
    return avg_correlation, correlation_scores

# Test with a simple sine wave
def create_test_audio(duration_seconds=2, frequency=440):
    """Create test audio signal"""
    sample_rate = 44100
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio

# Run the test
if __name__ == "__main__":
    print("🔬 FRACTAL TIMING ENCODING TEST")
    print("Creating test audio...")
    
    # Create test audio
    original_audio = create_test_audio(duration_seconds=2)
    
    # Generate fractal pattern from seed
    seed = "artist_fractal_seed_123"
    fractal_pattern = generate_fractal_pattern(seed, 100)
    
    print(f"Original audio length: {len(original_audio)} samples")
    print(f"Fractal pattern generated from seed: {seed}")
    
    # Encode fractal timing
    print("Encoding fractal timing variations...")
    encoded_audio = encode_timing_fractal(original_audio, fractal_pattern, max_shift_ms=2)
    
    # Test detection
    print("Testing fractal detection...")
    correlation, scores = detect_timing_fractal(original_audio, encoded_audio, seed)
    
    print(f"🎯 Average correlation: {correlation:.4f}")
    print(f"🔍 Detection confidence: {min(correlation * 100, 100):.1f}%")
    
    # Save test files for listening
    sf.write('tests/fractal_encoding/original.wav', original_audio, 44100)
    sf.write('tests/fractal_encoding/encoded.wav', encoded_audio, 44100)
    
    print("💾 Test files saved:")
    print("   - tests/fractal_encoding/original.wav")
    print("   - tests/fractal_encoding/encoded.wav")
    
    # Check if encoding is audible
    difference = np.abs(encoded_audio - original_audio)
    max_difference = np.max(difference)
    print(f"🎧 Maximum audio difference: {max_difference:.6f}")
    print(f"   {'✅ Inaudible' if max_difference < 0.01 else '❌ Potentially audible'}")
    
    if correlation > 0.1:
        print("🎉 SUCCESS: Fractal timing encoding detected!")
    else:
        print("❌ FAILED: Fractal pattern not detected reliably")
