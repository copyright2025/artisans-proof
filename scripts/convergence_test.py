#!/usr/bin/env python3
"""
Convergence test using your actual hashes from Artisan's Proof
"""

def hamming_distance(hash1, hash2):
    """Calculate similarity between two hashes"""
    if len(hash1) != len(hash2):
        return 1.0
    return sum(c1 != c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)

def calculate_convergence(bio_hash, micro_hash, economic_pattern="3/97"):
    """Three-point sovereignty convergence"""
    
    # Convert economic pattern to comparable format
    economic_hash = str(hash(economic_pattern))
    
    # Calculate divergences
    bio_micro_div = hamming_distance(str(bio_hash), str(micro_hash))
    bio_economic_div = hamming_distance(str(bio_hash), economic_hash)
    micro_economic_div = hamming_distance(str(micro_hash), economic_hash)
    
    # Perfect convergence = 0 divergence across all pairs
    total_divergence = bio_micro_div + bio_economic_div + micro_economic_div
    
    # Normalize to 0-1 scale (1 = perfect convergence)
    convergence_score = 1.0 / (1.0 + total_divergence)
    
    return {
        'biological_hash': bio_hash,
        'micro_architecture_hash': micro_hash, 
        'economic_pattern': economic_pattern,
        'convergence_score': convergence_score,
        'sovereignty_validated': convergence_score > 0.6
    }

# Your actual hashes from completed phases
biological_hash = "9b8e74c202e5ac158ee3adc83d4e1a29db7fc8644c190e66f08835f47a0d2f04"
lyric_hash = "6fb3c8a95f15eea953381220ca589fefac3fa298ae81cb71f4363113a04d1ae6"
economic_pattern = "3/97"  # Your profit distribution

print("🎯 ARTISAN'S PROOF - CONVERGENCE VALIDATION")
print("Testing your actual sovereign identity...")

result = calculate_convergence(biological_hash, lyric_hash, economic_pattern)

print(f"🧬 Biological Hash: {result['biological_hash'][:16]}...")
print(f"📝 Lyric Structure Hash: {result['micro_architecture_hash'][:16]}...") 
print(f"💰 Economic Pattern: {result['economic_pattern']}")
print(f"🎯 Convergence Score: {result['convergence_score']:.4f}")
print(f"✅ Sovereignty Validated: {result['sovereignty_validated']}")

if result['sovereignty_validated']:
    print("\n🎉 SOVEREIGN IDENTITY CONFIRMED!")
    print("Your biological, creative, and economic signatures converge!")
else:
    print("\n🔧 Convergence needs tuning - this is expected for first test")
