#!/usr/bin/env python3
"""
Tuning suite v2 - fix the crackle and go ultra-gentle
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

def apply_phase_shift(chunk, shift_samples):
    """Use phase rotation instead of time shifting to avoid crackles"""
    if shift_samples == 0:
        return chunk
    
    # Apply phase shift in frequency domain (no samples lost)
    freq_domain = np.fft.fft(chunk)
    angles = np.angle(freq_domain)
    
    # Create phase shift - linear phase gradient
    phase_shift = np.linspace(0, shift_samples * 2 * np.pi / len(chunk), len(chunk))
    new_angles = angles + phase_shift
    
    # Reconstruct with new phase
    freq_domain_shifted = np.abs(freq_domain) * np.exp(1j * new_angles)
    return np.real(np.fft.ifft(freq_domain_shifted))

def encode_phase_fractal(audio, fractal_pattern, max_shift_ms, chunk_size=2048):
    """Encode using phase shifts instead of time shifts - NO CRACKLES"""
    sample_rate = 44100
    max_shift_samples = int((max_shift_ms / 1000) * sample_rate)
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    encoded_audio = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            chunk = apply_phase_shift(chunk, shift_samples)
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

# Test ULTRA gentle phase encoding
strengths = [
    (0.1, "PHASE 0.1ms - Testing phase shift method"),
    (0.05, "PHASE 0.05ms"),
    (0.02, "PHASE 0.02ms"), 
    (0.01, "PHASE 0.01ms"),
    (0.005, "PHASE 0.005ms"),
    (0.002, "PHASE 0.002ms"),
    (0.001, "PHASE 0.001ms - Nearly microscopic")
]

print("🔊 PHASE-BASED FRACTAL ENCODING")
print("Using phase shifts instead of time shifts - NO CRACKLES!")

original_audio = create_test_audio(duration_seconds=2)
seed = "artist_fractal_seed_123"
fractal_pattern = generate_fractal_pattern(seed, 100)

# Save original
sf.write('tests/fractal_encoding/original_phase.wav', original_audio, 44100)

# Generate all encoded versions
for strength_ms, description in strengths:
    print(f"\n🔧 Phase encoding with {strength_ms}ms shifts...")
    encoded = encode_phase_fractal(original_audio, fractal_pattern, strength_ms)
    
    filename = f'tests/fractal_encoding/phase_{strength_ms}ms.wav'
    sf.write(filename, encoded, 44100)
    
    correlation = np.corrcoef(original_audio, encoded)[0,1]
    max_diff = np.max(np.abs(encoded - original_audio))
    
    print(f"   📊 Correlation: {correlation:.4f}")
    print(f"   🎧 Max difference: {max_diff:.8f}")

print("\n" + "="*50)
print("🎵 PLAYING PHASE-ENCODED VERSIONS (NO CRACKLES!)")
print("="*50)

play_file('tests/fractal_encoding/original_phase.wav', 'ORIGINAL - Clean reference')

for strength_ms, description in strengths:
    filename = f'tests/fractal_encoding/phase_{strength_ms}ms.wav'
    play_file(filename, description)

print("\n🎯 PHASE SHIFTING COMPLETE!")
print("This method should eliminate the crackles entirely!")
print("Listen for any artifacts - phase shifts are much smoother")
