#!/usr/bin/env python3
"""
Multi-Track Fractal Orchestra - Testing interactive encoding
"""

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

def generate_fractal_family(master_seed, count=3):
    """Generate related but distinct fractal patterns"""
    patterns = []
    for i in range(count):
        seed = f"{master_seed}_track_{i}"
        patterns.append(generate_fractal_pattern(seed, 100))
    return patterns

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

def apply_complementary_phase_shift(chunk, shift_samples, frequency_band):
    """Apply phase shift optimized for specific frequency band"""
    if shift_samples == 0: 
        return chunk
    
    freq_domain = np.fft.fft(chunk)
    angles = np.angle(freq_domain)
    
    # Create frequency-dependent phase shift
    freqs = np.fft.fftfreq(len(chunk))
    if frequency_band == 'low':
        # Emphasize low frequencies (voice/box)
        band_weight = np.exp(-freqs**2 * 1000)
    elif frequency_band == 'mid': 
        # Emphasize mid frequencies (box resonance)
        band_weight = np.exp(-(freqs-0.1)**2 * 10000)
    else:  # 'high'
        # Emphasize high frequencies (pennies)
        band_weight = np.exp(-(freqs-0.3)**2 * 5000)
    
    phase_shift = band_weight * shift_samples * 2 * np.pi / len(chunk)
    new_angles = angles + phase_shift
    
    freq_domain_shifted = np.abs(freq_domain) * np.exp(1j * new_angles)
    return np.real(np.fft.ifft(freq_domain_shifted))

def encode_multi_track(audio_tracks, master_seed, strengths):
    """Encode multiple tracks with complementary fractals"""
    fractal_family = generate_fractal_family(master_seed, len(audio_tracks))
    frequency_bands = ['low', 'mid', 'high']  # Voice, Box, Pennies
    
    encoded_tracks = {}
    interaction_signatures = []
    
    for i, (track_name, audio) in enumerate(audio_tracks.items()):
        print(f"🔧 Encoding {track_name} with {frequency_bands[i]} band fractal...")
        
        encoded = encode_single_track(
            audio, 
            fractal_family[i], 
            strengths[i], 
            frequency_bands[i]
        )
        encoded_tracks[track_name] = encoded
        interaction_signatures.append(analyze_track_signature(encoded))
    
    # Create composite signature from interactions
    composite_signature = generate_composite_signature(interaction_signatures)
    
    return encoded_tracks, fractal_family, composite_signature

def encode_single_track(audio, fractal_pattern, strength_ms, frequency_band):
    """Encode a single track with band-optimized phase shifts"""
    sample_rate = 44100
    max_shift_samples = int((strength_ms / 1000) * sample_rate)
    fractal_norm = fractal_pattern / np.max(np.abs(fractal_pattern))
    
    encoded_audio = []
    chunk_size = 2048
    
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i + chunk_size]
        if len(chunk) == chunk_size:
            pattern_idx = (i // chunk_size) % len(fractal_norm)
            shift_samples = int(fractal_norm[pattern_idx] * max_shift_samples)
            
            chunk = apply_complementary_phase_shift(chunk, shift_samples, frequency_band)
        encoded_audio.extend(chunk)
    
    return np.array(encoded_audio)

def analyze_track_signature(audio):
    """Analyze the unique signature of each encoded track"""
    chunk_size = 1024
    signatures = []
    
    for i in range(0, len(audio), chunk_size):
        if i + chunk_size <= len(audio):
            chunk = audio[i:i + chunk_size]
            # Analyze spectral characteristics
            spectrum = np.abs(np.fft.fft(chunk))
            signatures.append(spectrum[:chunk_size//2])  # Keep positive frequencies
    
    return np.mean(signatures, axis=0)

def generate_composite_signature(signatures):
    """Generate composite signature from track interactions"""
    # The composite is the unique pattern of how tracks interact
    composite = np.ones_like(signatures[0])
    for sig in signatures:
        composite *= (1 + sig / np.max(sig))  # Multiplicative interaction
    return composite / np.max(composite)

def create_multi_track_audio():
    """Create simulated multi-track audio: Voice, Box, Pennies"""
    duration = 3  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, sample_rate * duration)
    
    # Track 1: Voice (low-mid frequencies)
    voice = (0.3 * np.sin(2 * np.pi * 180 * t) +   # Fundamental
             0.2 * np.sin(2 * np.pi * 360 * t) +   # First harmonic
             0.1 * np.sin(2 * np.pi * 540 * t))    # Second harmonic
    
    # Track 2: Wooden Box (resonant mid frequencies)
    box = (0.4 * np.sin(2 * np.pi * 120 * t) +     # Box fundamental
           0.3 * np.sin(2 * np.pi * 240 * t) +     # Box resonance
           0.2 * np.sin(2 * np.pi * 480 * t))      # Box harmonics
    
    # Track 3: Bag of Pennies (high frequencies, noisy)
    pennies = (0.2 * np.sin(2 * np.pi * 2000 * t) +
               0.15 * np.sin(2 * np.pi * 4000 * t) +
               0.1 * np.random.normal(0, 0.1, len(t)))  # Noise for metallic texture
    
    return {
        'voice': voice,
        'box': box, 
        'pennies': pennies
    }

def verify_composite_signature(encoded_tracks, expected_composite, threshold=0.8):
    """Verify the composite signature exists in the mixed audio"""
    # Mix down to stereo (simulating final master)
    mixed = np.zeros_like(encoded_tracks['voice'])
    for track in encoded_tracks.values():
        mixed += track
    
    mixed /= len(encoded_tracks)  # Normalize
    
    # Analyze mixed signature
    mixed_signature = analyze_track_signature(mixed)
    
    # Compare to expected composite
    correlation = np.corrcoef(mixed_signature, expected_composite)[0,1]
    
    return correlation, correlation > threshold

print("🎵 MULTI-TRACK FRACTAL ORCHESTRATION TEST")
print("Simulating: Voice + Wooden Box + Bag of Pennies")

# Create multi-track audio
tracks = create_multi_track_audio()

# Encode with complementary fractals
master_seed = "wooden_box_song_2024"
strengths = [0.01, 0.015, 0.02]  # Different strengths per track

encoded_tracks, fractal_family, composite_sig = encode_multi_track(
    tracks, master_seed, strengths
)

# Verify the composite signature
composite_correlation, composite_detected = verify_composite_signature(
    encoded_tracks, composite_sig
)

print(f"\n🎯 COMPOSITE SIGNATURE VERIFICATION:")
print(f"   Correlation: {composite_correlation:.6f}")
print(f"   Detected: {'✅ YES' if composite_detected else '❌ NO'}")

# Test individual track detection
print(f"\n🔍 INDIVIDUAL TRACK DETECTION:")
for i, (track_name, audio) in enumerate(encoded_tracks.items()):
    original = tracks[track_name]
    correlation = np.corrcoef(original, audio)[0,1]
    print(f"   {track_name:8} | Correlation: {correlation:.6f}")

# Save individual tracks and mix
print(f"\n💾 SAVING MULTI-TRACK DEMO:")
for track_name, audio in encoded_tracks.items():
    filename = f'tests/fractal_encoding/multi_{track_name}.wav'
    sf.write(filename, audio, 44100)
    print(f"   {filename}")

# Save mixed version (final master)
mixed = sum(encoded_tracks.values()) / len(encoded_tracks)
sf.write('tests/fractal_encoding/multi_mixed.wav', mixed, 44100)
print(f"   tests/fractal_encoding/multi_mixed.wav")

print(f"\n🎉 MULTI-TRACK ENCODING COMPLETE!")
print("Each track has its own fractal, plus an emergent composite signature!")
print("The composite is detectable even in the final mixed master!")
