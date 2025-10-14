#!/usr/bin/env python3
"""
Progressive tuning - test multiple encoding strengths
"""

import numpy as np
import soundfile as sf
import subprocess
import time

def generate_fractal_pattern(seed, length):
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
    if shift_samples > 0:
        shifted = np.roll(chunk, shift_samples)
        shifted[:shift_samples] = 0
        fade_length = min(50, shift_samples)
        if fade_length > 0:
            fade_in = np.linspace(0, 1, fade_length)
            shifted[:fade_length] *= fade_in
    else:
        shift_samples = abs(shift_samples)
        shifted = np.roll(chunk, -shift_samples)
        shifted[-shift_samples:] = 0
        fade_length = min(50, shift_samples)
        if fade_length > 0:
            fade_out = np.linspace(1, 0, fade_length)
            shifted[-fade_length:] *= fade_out
    return shifted

def encode_timing_fractal(audio, fractal_pattern, max_shift_ms, chunk_size=1024):
    sample_rate = 44100
    max_shift_samples = int((max_shift_ms / 1000) * sample_rate)
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    encoded_audio = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            if shift_samples != 0:
                chunk = apply_smooth_shift(chunk, shift_samples)
        encoded_audio.extend(chunk)
    return np.array(encoded_audio)

def create_test_audio(duration_seconds=2, frequency=440):
    sample_rate = 44100
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def play_file(filename, description):
    print(f"🎵 {description}")
    print(f"   File: {filename}")
    try:
        subprocess.run(['aplay', filename], check=True)
    except subprocess.CalledProcessError:
        print(f"   ❌ Could not play {filename}")
    time.sleep(1.5)

# Test different encoding strengths
strengths = [
    (2.0, "VERY STRONG - 2.0ms shifts (original 'awful' version)"),
    (1.0, "STRONG - 1.0ms shifts"),
    (0.5, "MEDIUM - 0.5ms shifts (current test)"), 
    (0.2, "GENTLE - 0.2ms shifts"),
    (0.1, "VERY GENTLE - 0.1ms shifts"),
    (0.05, "ULTRA GENTLE - 0.05ms shifts")
]

print("🔊 FRACTAL ENCODING TUNING SUITE")
print("Testing multiple encoding strengths...")

original_audio = create_test_audio(duration_seconds=2)
seed = "artist_fractal_seed_123"
fractal_pattern = generate_fractal_pattern(seed, 100)

# Save original
sf.write('tests/fractal_encoding/original_tuning.wav', original_audio, 44100)

# Generate all encoded versions
for strength_ms, description in strengths:
    print(f"\n🔧 Encoding with {strength_ms}ms shifts...")
    encoded = encode_timing_fractal(original_audio, fractal_pattern, strength_ms)
    
    filename = f'tests/fractal_encoding/encoded_{strength_ms}ms.wav'
    sf.write(filename, encoded, 44100)
    
    correlation = np.corrcoef(original_audio, encoded)[0,1]
    max_diff = np.max(np.abs(encoded - original_audio))
    
    print(f"   📊 Correlation: {correlation:.4f}")
    print(f"   🎧 Max difference: {max_diff:.6f}")

print("\n" + "="*50)
print("🎵 NOW PLAYING ALL VERSIONS FOR COMPARISON")
print("="*50)

# Play all versions for comparison
play_file('tests/fractal_encoding/original_tuning.wav', 'ORIGINAL - Clean reference tone')

for strength_ms, description in strengths:
    filename = f'tests/fractal_encoding/encoded_{strength_ms}ms.wav'
    play_file(filename, description)

print("\n🎯 LISTENING COMPLETE!")
print("Please note which version is the best balance:")
print("- Still detectable (correlation > 0.99)")
print("- But inaudible to your ears")
print("Then we'll use that as our baseline!")
