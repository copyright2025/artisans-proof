#!/usr/bin/env python3
import hashlib
import json
import time
from datetime import datetime
import os

class LyricProof:
    def __init__(self):
        self.proof_data = {}
    
    def create_lyric_proof(self, lyric_text, song_title, artist_name):
        """Create cryptographic proof of lyric structure"""
        print(f"📝 Creating lyric proof for: {song_title}")
        
        # 1. Text normalization (remove extra whitespace, standardize)
        normalized_lyrics = self._normalize_lyrics(lyric_text)
        
        # 2. Structural analysis
        structure_hash = self._analyze_lyric_structure(normalized_lyrics)
        
        # 3. Create content hash
        content_hash = hashlib.sha256(normalized_lyrics.encode()).hexdigest()
        
        # 4. Create comprehensive proof
        self.proof_data = {
            'song_title': song_title,
            'artist': artist_name,
            'content_hash': content_hash,
            'structure_hash': structure_hash,
            'line_count': len(normalized_lyrics.split('\n')),
            'word_count': len(normalized_lyrics.split()),
            'character_count': len(normalized_lyrics),
            'timestamp': datetime.utcnow().isoformat(),
            'protocol': 'SovereignAudio v1.0'
        }
        
        return self.proof_data
    
    def _normalize_lyrics(self, lyric_text):
        """Normalize lyrics for consistent hashing"""
        # Remove extra whitespace but preserve structure
        lines = [line.strip() for line in lyric_text.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def _analyze_lyric_structure(self, lyrics):
        """Analyze lyric structure patterns"""
        lines = lyrics.split('\n')
        
        structural_features = []
        
        for i, line in enumerate(lines):
            line_features = {
                'line_number': i,
                'length': len(line),
                'word_count': len(line.split()),
                'ends_with_rhyme': line[-1] if line else '',  # Simple rhyme marker
                'is_chorus_like': self._is_chorus_like(line, lines)
            }
            structural_features.append(str(line_features))
        
        structure_string = '|'.join(structural_features)
        return hashlib.sha256(structure_string.encode()).hexdigest()
    
    def _is_chorus_like(self, line, all_lines):
        """Simple chorus detection (repeated lines)"""
        if not line:
            return False
        return all_lines.count(line) > 1
    
    def create_complete_lyric_proof(self, lyric_text, song_title, artist_name, output_dir="proofs"):
        """Complete lyric proof creation"""
        # Create proof data
        proof = self.create_lyric_proof(lyric_text, song_title, artist_name)
        
        # Save JSON proof
        json_filename = f"lyric_proof_{proof['content_hash'][:16]}.json"
        json_path = os.path.join(output_dir, json_filename)
        
        complete_proof = {
            'proof_data': proof,
            'status': 'READY_FOR_BLOCKCHAIN'
        }
        
        with open(json_path, 'w') as f:
            json.dump(complete_proof, f, indent=2)
        
        print(f"✅ Lyric proof created:")
        print(f"   Content Hash: {proof['content_hash']}")
        print(f"   Structure Hash: {proof['structure_hash']}")
        print(f"   JSON: {json_path}")
        
        return complete_proof

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 lyric_proof.py \"<lyric_text>\" \"<song_title>\" \"<artist_name>\"")
        print("Example: python3 lyric_proof.py \"Hello world\\nThis is a song\" \"My Song\" \"REDACTED\"")
        sys.exit(1)
    
    lyric_text = sys.argv[1]
    song_title = sys.argv[2]
    artist_name = sys.argv[3]
    
    lp = LyricProof()
    lp.create_complete_lyric_proof(lyric_text, song_title, artist_name)

if __name__ == "__main__":
    main()
