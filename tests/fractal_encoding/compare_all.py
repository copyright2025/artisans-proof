#!/usr/bin/env python3
"""
Play all test files for comparison
"""

import subprocess
import time

def play_file(filename, description):
    print(f"🎵 Playing: {description}")
    print(f"   File: {filename}")
    try:
        subprocess.run(['aplay', filename], check=True)
    except subprocess.CalledProcessError:
        print(f"   ❌ Could not play {filename}")
    print("--- Waiting 2 seconds ---")
    time.sleep(2)

print("🔊 FRACTAL ENCODING COMPARISON")
print("You will hear 3 files with 2-second pauses between them")
print()

play_file('tests/fractal_encoding/original.wav', 'ORIGINAL - Clean sine wave')
play_file('tests/fractal_encoding/encoded.wav', 'ENCODED STRONG - 2ms timing shifts (you said "awful")')
play_file('tests/fractal_encoding/encoded_gentle.wav', 'ENCODED GENTLE - 0.5ms timing shifts (if it exists)')

print("🎧 Comparison complete!")
print("Please describe the differences you heard:")
print("1. Original vs Strong encoding")
print("2. Original vs Gentle encoding (if available)")
print("3. Strong vs Gentle encoding (if available)")
