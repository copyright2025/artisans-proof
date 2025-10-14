#!/usr/bin/env python3
"""
Gentle fractal timing test - reduced strength for audibility
"""

import numpy as np
import soundfile as sf

def generate_fractal_pattern(seed, length):
    """Generate deterministic fractal pattern from seed"""
    rng = np.random.RandomState(hash(seed) % 2**32)
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

def apply_smooth_shift(chunk, shift_samples):
    """Apply timing shift with crossfade to avoid clicks"""
    if shift_samples > 0:
        # Shift right with fade
        shifted = np.roll(chunk, shift_samples)
        shifted[:shift_samples] = 0
        # Crossfade the transition
        fade_length = min(50, shift_samples)
        if fade_length > 0:
            fade_in = np.linspace(0, 1, fade_length)
            shifted[:fade_length] *= fade_in
    else:
        # Shift left
        shift_samples = abs(shift_samples)
        shifted = np.roll(chunk, -shift_samples)
        shifted[-shift_samples:] = 0
        fade_length = min(50, shift_samples)
        if fade_length > 0:
            fade_out = np.linspace(1, 0, fade_length)
            shifted[-fade_length:] *= fade_out
    return shifted

def encode_timing_fractal_gentle(audio, fractal_pattern, max_shift_ms=0.5):
    """Gentle encoding - much smaller timing shifts"""
    sample_rate = 44100
    max_shift_samples = int((max_shift_ms / 1000) * sample_rate)
    
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    encoded_audio = []
    chunk_size = 1024
    
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            
            if shift_samples != 0:
                # Use smooth crossfade instead of hard roll
                chunk = apply_smooth_shift(chunk, shift_samples)
            
        encoded_audio.extend(chunk)
    
    return np.array(encoded_audio)

def create_test_audio(duration_seconds=2, frequency=440):
    """Create test audio signal"""
    sample_rate = 44100
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    return audio

if __name__ == "__main__":
    print("🔬 GENTLE FRACTAL TIMING TEST")
    print("Using 0.5ms max shift (was 2ms)")
    
    original_audio = create_test_audio(duration_seconds=2)
    seed = "artist_fractal_seed_123"
    fractal_pattern = generate_fractal_pattern(seed, 100)
    
    print("Encoding with gentle timing variations...")
    encoded_audio = encode_timing_fractal_gentle(original_audio, fractal_pattern, max_shift_ms=0.5)
    
    # Simple detection test
    correlation = np.corrcoef(original_audio, encoded_audio)[0,1]
    
    print(f"🎯 Correlation with original: {correlation:.4f}")
    
    # Save files for listening
    sf.write('tests/fractal_encoding/original_gentle.wav', original_audio, 44100)
    sf.write('tests/fractal_encoding/encoded_gentle.wav', encoded_audio, 44100)
    
    print("💾 Test files saved:")
    print("   - tests/fractal_encoding/original_gentle.wav") 
    print("   - tests/fractal_encoding/encoded_gentle.wav")
    
    difference = np.abs(encoded_audio - original_audio)
    max_diff = np.max(difference)
    print(f"🎧 Maximum audio difference: {max_diff:.6f}")
    print(f"   {'✅ Probably inaudible' if max_diff < 0.001 else '❌ Potentially audible'}")
    
    if correlation > 0.99:
        print("🎉 SUCCESS: Gentle encoding works!")
    else:
        print(f"🔧 Correlation dropped to {correlation:.4f} - may be too gentle")
