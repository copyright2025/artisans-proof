#!/usr/bin/env python3
"""
Find the DETECTION threshold first, then work backward to audibility
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
    """Phase shift - no crackles"""
    if shift_samples == 0:
        return chunk
    freq_domain = np.fft.fft(chunk)
    angles = np.angle(freq_domain)
    phase_shift = np.linspace(0, shift_samples * 2 * np.pi / len(chunk), len(chunk))
    new_angles = angles + phase_shift
    freq_domain_shifted = np.abs(freq_domain) * np.exp(1j * new_angles)
    return np.real(np.fft.ifft(freq_domain_shifted))

def encode_phase_fractal(audio, fractal_pattern, max_shift_ms):
    sample_rate = 44100
    max_shift_samples = int((max_shift_ms / 1000) * sample_rate)
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    encoded_audio = []
    chunk_size = 2048
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            chunk = apply_phase_shift(chunk, shift_samples)
        encoded_audio.extend(chunk)
    return np.array(encoded_audio)

def detect_fractal_pattern(original, encoded, fractal_pattern, chunk_size=2048):
    """How well can we detect the fractal encoding?"""
    correlations = []
    for i in range(0, min(len(original), len(encoded)), chunk_size):
        orig_chunk = original[i:i + chunk_size]
        enc_chunk = encoded[i:i + chunk_size]
        if len(orig_chunk) == chunk_size and len(enc_chunk) == chunk_size:
            corr = np.corrcoef(orig_chunk, enc_chunk)[0,1]
            correlations.append(corr)
    return np.mean(correlations), np.std(correlations)

def create_test_audio(duration_seconds=2, frequency=440):
    sample_rate = 44100
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    return 0.5 * np.sin(2 * np.pi * frequency * t)

def play_file(filename, description):
    print(f"🎵 {description}")
    try:
        subprocess.run(['aplay', filename], check=True)
    except:
        print(f"   ❌ Could not play {filename}")
    time.sleep(1.5)

print("🔬 DETECTION THRESHOLD FIRST - THEN AUDIBILITY")
print("Finding the minimum encoding that software can detect...")

original_audio = create_test_audio(duration_seconds=2)
seed = "artist_fractal_seed_123"
fractal_pattern = generate_fractal_pattern(seed, 100)

# Test microscopic encoding levels
microscopic_strengths = [
    (0.0001, "0.0001ms - Near digital noise floor"),
    (0.0005, "0.0005ms"), 
    (0.001, "0.001ms"),
    (0.002, "0.002ms"),
    (0.005, "0.005ms"),
    (0.01, "0.01ms"),
    (0.02, "0.02ms"),
    (0.05, "0.05ms"),
    (0.1, "0.1ms")
]

print("\n📊 TESTING DETECTABILITY AT MICROSCOPIC LEVELS:")
print("Strength | Correlation | Detectable | Likely Audible")
print("-" * 55)

detection_threshold = None
audibility_threshold = None

for strength_ms, description in microscopic_strengths:
    encoded = encode_phase_fractal(original_audio, fractal_pattern, strength_ms)
    
    correlation, std = detect_fractal_pattern(original_audio, encoded, fractal_pattern)
    detectable = correlation > 0.999  # Very strict detection
    likely_audible = strength_ms > 0.01  # Guess based on previous tests
    
    status = "✅ YES" if detectable else "❌ NO"
    audible_status = "🔊 YES" if likely_audible else "🔇 NO"
    
    print(f"{strength_ms:7.4f}ms | {correlation:10.6f} | {status:10} | {audible_status:12}")
    
    # Find thresholds
    if detectable and detection_threshold is None:
        detection_threshold = strength_ms
    if likely_audible and audibility_threshold is None:
        audibility_threshold = strength_ms
    
    # Save for listening if potentially interesting
    if 0.001 <= strength_ms <= 0.1:
        filename = f'tests/fractal_encoding/detect_{strength_ms}ms.wav'
        sf.write(filename, encoded, 44100)

print(f"\n🎯 DETECTION THRESHOLD: {detection_threshold}ms")
print(f"🎧 ESTIMATED AUDIBILITY THRESHOLD: {audibility_threshold}ms")

if detection_threshold and audibility_threshold:
    sweet_spot = (detection_threshold + audibility_threshold) / 2
    print(f"🍯 SUGGESTED SWEET SPOT: {sweet_spot:.4f}ms")
    
    # Create sweet spot version
    encoded_sweet = encode_phase_fractal(original_audio, fractal_pattern, sweet_spot)
    sf.write('tests/fractal_encoding/sweet_spot.wav', encoded_sweet, 44100)

print("\n" + "="*50)
print("🎵 PLAYING KEY VERSIONS AROUND THRESHOLDS")
print("="*50)

# Play the most informative versions
key_versions = [
    (detection_threshold, f"DETECTION THRESHOLD - {detection_threshold}ms"),
    (audibility_threshold, f"AUDIBILITY THRESHOLD - {audibility_threshold}ms"),
    (sweet_spot, f"SWEET SPOT - {sweet_spot:.4f}ms")
]

play_file('tests/fractal_encoding/original_phase.wav', 'ORIGINAL - Reference')

for strength_ms, description in key_versions:
    if strength_ms:
        filename = f'tests/fractal_encoding/detect_{strength_ms}ms.wav'
        play_file(filename, description)

print("\n🎯 STRATEGY: Use the sweet spot where:")
print("   - Software can reliably detect the encoding")
print("   - Human ears cannot perceive the difference")
