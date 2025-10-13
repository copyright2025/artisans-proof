#!/usr/bin/env python3
import json
import hashlib
import sys
import os

# Add the current directory to path so we can import biological_core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.biological_core import create_voiceprint

def anchor_voiceprint_on_chain(audio_path, artist_name):
    """Anchor voiceprint with artist identity"""
    
    # Create biological voiceprint
    print("🔬 Creating biological voiceprint...")
    voiceprint = create_voiceprint(audio_path)
    
    if not voiceprint:
        print("❌ Voiceprint creation failed")
        return None
    
    # Create proof data
    proof_data = {
        'artist': artist_name,
        'biological_hash': voiceprint['biological_hash'],
        'feature_digest': voiceprint['feature_digest'],
        'confidence_score': voiceprint['confidence_score'],
        'protocol': 'SovereignAudio v1.0',
        'timestamp': voiceprint['timestamp']
    }
    
    # Create proof hash
    proof_hash = hashlib.sha256(json.dumps(proof_data).encode()).hexdigest()
    
    anchor_proof = {
        'voiceprint_data': voiceprint,
        'on_chain_proof': proof_data,
        'proof_hash': proof_hash,
        'status': 'READY_FOR_BLOCKCHAIN_ANCHORING'
    }
    
    # Save proof
    output_file = f"proofs/voiceprint_anchor_{proof_hash[:16]}.json"
    with open(output_file, 'w') as f:
        json.dump(anchor_proof, f, indent=2)
    
    print(f"🎯 Artist: {artist_name}")
    print(f"🔬 Biological Hash: {voiceprint['biological_hash']}")
    print(f"📊 Confidence: {voiceprint['confidence_score']:.1%}")
    print(f"📁 Proof ready: {output_file}")
    print(f"🔗 Ready for blockchain anchoring")
    
    return anchor_proof

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 anchor_voiceprint.py <audio_file> <artist_name>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    artist_name = sys.argv[2]
    
    anchor_voiceprint_on_chain(audio_file, artist_name)
