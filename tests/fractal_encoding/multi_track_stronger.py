#!/usr/bin/env python3
"""
Test stronger multi-track encoding for better composite detection
"""

import numpy as np
import soundfile as sf

# [Include all the same functions from multi_track_orchestra.py here...]
# [Copy all the function definitions from the previous file]

def test_different_strengths():
    """Test how encoding strength affects composite detection"""
    
    tracks = create_multi_track_audio()
    master_seed = "strength_test_2024"
    
    strength_profiles = {
        'Gentle': [0.01, 0.015, 0.02],
        'Medium': [0.02, 0.03, 0.04], 
        'Strong': [0.03, 0.045, 0.06],
        'Very Strong': [0.05, 0.075, 0.1]
    }
    
    print("🔬 MULTI-TRACK STRENGTH OPTIMIZATION")
    print("Testing how encoding strength affects composite detection")
    print("-" * 60)
    
    results = {}
    
    for profile_name, strengths in strength_profiles.items():
        print(f"\n🧪 Testing {profile_name} profile: {strengths}")
        
        encoded_tracks, fractal_family, composite_sig = encode_multi_track(
            tracks, master_seed, strengths
        )
        
        composite_corr, composite_detected = verify_composite_signature(
            encoded_tracks, composite_sig, threshold=0.95  # Higher threshold
        )
        
        # Check individual track quality
        individual_corrs = []
        for track_name, audio in encoded_tracks.items():
            original = tracks[track_name]
            corr = np.corrcoef(original, audio)[0,1]
            individual_corrs.append(corr)
        
        avg_individual = np.mean(individual_corrs)
        
        results[profile_name] = {
            'composite_correlation': composite_corr,
            'composite_detected': composite_detected,
            'avg_individual_correlation': avg_individual,
            'strengths': strengths
        }
        
        print(f"   Composite Correlation: {composite_corr:.6f}")
        print(f"   Composite Detected (>0.95): {'✅ YES' if composite_detected else '❌ NO'}")
        print(f"   Avg Individual Correlation: {avg_individual:.6f}")
    
    # Find optimal profile
    best_profile = None
    best_score = 0
    
    for profile_name, result in results.items():
        score = (result['composite_correlation'] + result['avg_individual_correlation']) / 2
        if score > best_score:
            best_score = score
            best_profile = profile_name
    
    print(f"\n🎯 OPTIMAL PROFILE: {best_profile}")
    print(f"   Strengths: {results[best_profile]['strengths']}")
    print(f"   Composite: {results[best_profile]['composite_correlation']:.6f}")
    print(f"   Individual: {results[best_profile]['avg_individual_correlation']:.6f}")
    
    return results, best_profile

# Run the optimization test
if __name__ == "__main__":
    # [Include all the function definitions...]
    
    # Copy all the functions from multi_track_orchestra.py here
    # (I'm omitting them for brevity, but they need to be included)
    
    print("This test requires all the functions from the previous file.")
    print("Let me run a simpler version...")
    
    # Simple version with just the core test
    from multi_track_orchestra import *
    
    results, best = test_different_strengths()
