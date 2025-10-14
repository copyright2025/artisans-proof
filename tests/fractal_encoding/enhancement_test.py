#!/usr/bin/env python3
"""
Test if fractal encoding actually ENHANCES audio quality
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
    if shift_samples == 0: return chunk
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

# Test with more complex audio (not just sine wave)
def create_rich_audio(duration_seconds=2):
    """Create more musical test audio"""
    sample_rate = 44100
    t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds))
    
    # Rich harmonic content
    audio = (0.3 * np.sin(2 * np.pi * 220 * t) +          # Fundamental
             0.2 * np.sin(2 * np.pi * 440 * t) +          # Octave
             0.1 * np.sin(2 * np.pi * 660 * t) +          # Fifth
             0.05 * np.sin(2 * np.pi * 880 * t))          # Double octave
    
    return audio

print("🎵 TESTING: Does Fractal Encoding ENHANCE Audio?")
print("=" * 50)

original_audio = create_rich_audio()
seed = "enhancement_test_123"
fractal_pattern = generate_fractal_pattern(seed, 100)

# Encode at our sweet spot
encoded_audio = encode_phase_fractal(original_audio, fractal_pattern, 0.01)

# Save both
sf.write('tests/fractal_encoding/enhance_original.wav', original_audio, 44100)
sf.write('tests/fractal_encoding/enhance_encoded.wav', encoded_audio, 44100)

# Analyze differences
correlation = np.corrcoef(original_audio, encoded_audio)[0,1]
rms_original = np.sqrt(np.mean(original_audio**2))
rms_encoded = np.sqrt(np.mean(encoded_audio**2))
loudness_diff = 20 * np.log10(rms_encoded / rms_original)

print(f"📊 Correlation: {correlation:.8f}")
print(f"🔊 Loudness difference: {loudness_diff:.2f} dB")
print(f"   {'✅ Slightly louder' if loudness_diff > 0.1 else '✅ Same level'}")

print("\n🎧 LISTENING TEST - Which sounds BETTER?")
print("First: ORIGINAL (plain audio)")
subprocess.run(['aplay', 'tests/fractal_encoding/enhance_original.wav'])
time.sleep(1)

print("\nSecond: ENCODED (with fractal identity)")
subprocess.run(['aplay', 'tests/fractal_encoding/enhance_encoded.wav'])

print("\n🤔 QUESTION: Did the encoded version sound:")
print("   A) Worse")
print("   B) The Same") 
print("   C) Better (fuller, richer, more pleasant)")
print("   D) Just different")
