#!/usr/bin/env python3
import librosa
import numpy as np
import hashlib
import json
from scipy import signal
import warnings
warnings.filterwarnings('ignore')

class SovereignVoiceprint:
    def __init__(self, sample_rate=44100):
        self.sr = sample_rate
        self.biometric_data = {}
    
    def extract_universal_biometrics(self, audio_path):
        """Extract language-agnostic biological signatures"""
        print("🔬 Extracting universal biological metrics...")
        
        try:
            y, sr = librosa.load(audio_path, sr=self.sr, duration=30)  # First 30 seconds
        except Exception as e:
            print(f"❌ Error loading audio: {e}")
            return None
        
        # 1. VOCAL TRACT PHYSICS
        self.biometric_data['vocal_tract'] = self._extract_vocal_tract_physics(y, sr)
        
        # 2. CORD ELASTICITY  
        self.biometric_data['cord_elasticity'] = self._extract_cord_elasticity(y, sr)
        
        # 3. NEUROMUSCULAR TIMING
        self.biometric_data['neuromuscular_timing'] = self._extract_neuromuscular_timing(y, sr)
        
        # 4. BREATH CONTROL
        self.biometric_data['breath_control'] = self._extract_breath_control(y, sr)
        
        # 5. ARTICULATION CONSISTENCY
        self.biometric_data['articulation_consistency'] = self._extract_articulation_consistency(y, sr)
        
        return self.biometric_data
    
    def _extract_vocal_tract_physics(self, y, sr):
        """Vocal tract length and formant structure"""
        # Extract formants from vowel regions
        formants = self._extract_formants(y, sr)
        
        # Vocal tract length estimation (simplified)
        if len(formants) >= 2:
            vtl_estimate = (35000 / (2 * (formants[1] - formants[0]))) if formants[1] > formants[0] else 17.5
            vtl_estimate = max(10, min(25, vtl_estimate))  # Reasonable human range
        else:
            vtl_estimate = 17.5
        
        return {
            'vocal_tract_length_cm': vtl_estimate,
            'formant_1_hz': formants[0] if len(formants) > 0 else 500,
            'formant_2_hz': formants[1] if len(formants) > 1 else 1500,
            'formant_dispersion': formants[1] - formants[0] if len(formants) > 1 else 1000
        }
    
    def _extract_cord_elasticity(self, y, sr):
        """Vocal fold elasticity via pitch dynamics"""
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, fmin=80, fmax=400, sr=sr, frame_length=2048
        )
        f0_clean = f0[voiced_flag & ~np.isnan(f0)]
        
        if len(f0_clean) > 0:
            pitch_range = np.max(f0_clean) - np.min(f0_clean)
            pitch_octaves = np.log2(np.max(f0_clean) / np.min(f0_clean)) if np.min(f0_clean) > 0 else 0
        else:
            pitch_range = 0
            pitch_octaves = 0
        
        return {
            'pitch_range_hz': float(pitch_range),
            'pitch_range_octaves': float(pitch_octaves),
            'mean_pitch_hz': float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0
        }
    
    def _extract_neuromuscular_timing(self, y, sr):
        """Articulation coordination speed"""
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512, delta=0.1)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=512)
        
        if len(onset_times) > 1:
            ioi = np.diff(onset_times)
            timing_variability = np.std(ioi) / np.mean(ioi) if np.mean(ioi) > 0 else 0
            articulation_rate = len(onset_times) / (len(y) / sr)
        else:
            timing_variability = 0
            articulation_rate = 0
        
        return {
            'articulation_rate_hz': float(articulation_rate),
            'timing_consistency': float(timing_variability),
            'onset_count': len(onset_times)
        }
    
    def _extract_breath_control(self, y, sr):
        """Breath support and control"""
        # Energy envelope analysis
        frame_length = 1024
        hop_length = 256
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        
        # Simple breath group detection (energy dips)
        energy_threshold = np.mean(rms) * 0.3
        breath_groups = np.sum(rms < energy_threshold)
        
        # Phonation time estimate
        total_energy = np.sum(rms)
        avg_energy = np.mean(rms)
        
        return {
            'breath_group_count': int(breath_groups),
            'energy_consistency': float(np.std(rms) / avg_energy if avg_energy > 0 else 0),
            'phonation_stability': float(1.0 / (1.0 + np.std(rms)))  # Inverse of variability
        }
    
    def _extract_articulation_consistency(self, y, sr):
        """Motor pattern stability"""
        # Analyze consistency across time segments
        segment_length = sr * 3  # 3-second segments
        segments = []
        
        for i in range(0, len(y) - segment_length, segment_length):
            segment = y[i:i + segment_length]
            if len(segment) == segment_length:
                segments.append(segment)
        
        if len(segments) >= 2:
            # Compare spectral characteristics across segments
            spectral_centroids = []
            for seg in segments[:3]:  # First 3 segments
                centroid = librosa.feature.spectral_centroid(y=seg, sr=sr)[0]
                spectral_centroids.append(np.mean(centroid))
            
            consistency = 1.0 - (np.std(spectral_centroids) / np.mean(spectral_centroids) if np.mean(spectral_centroids) > 0 else 0)
        else:
            consistency = 0.5  # Default moderate consistency
        
        return {
            'motor_pattern_consistency': float(consistency),
            'analyzed_segments': len(segments) if len(segments) >= 2 else 0
        }
    
    def _extract_formants(self, y, sr, num_formants=3):
        """Simple formant extraction using spectral peaks"""
        # Focus on typical speech range
        D = librosa.stft(y)
        S = np.abs(D)
        freqs = librosa.fft_frequencies(sr=sr)
        
        # Find spectral peaks in speech range (100-4000 Hz)
        speech_mask = (freqs >= 100) & (freqs <= 4000)
        speech_freqs = freqs[speech_mask]
        speech_S = np.mean(S[speech_mask, :], axis=1)
        
        # Find prominent peaks (formants)
        peaks, _ = signal.find_peaks(speech_S, height=np.max(speech_S)*0.1, distance=100)
        
        formant_freqs = speech_freqs[peaks[:num_formants]] if len(peaks) >= num_formants else [500, 1500, 2500][:num_formants]
        
        return formant_freqs
    
    def create_biological_hash(self):
        """Create deterministic hash from biological features"""
        if not self.biometric_data:
            return None
        
        feature_string = ""
        
        # Convert all features to deterministic string
        for domain, metrics in self.biometric_data.items():
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    feature_string += f"{domain}_{key}_{value:.6f}_"
        
        biological_hash = hashlib.sha256(feature_string.encode()).hexdigest()
        
        return {
            'biological_hash': biological_hash,
            'feature_digest': hashlib.sha256(feature_string.encode()).hexdigest()[:16],
            'biometric_data': self.biometric_data,
            'confidence_score': self._calculate_confidence(),
            'timestamp': np.datetime64('now').astype(str)
        }
    
    def _calculate_confidence(self):
        """Calculate overall confidence score"""
        if not self.biometric_data:
            return 0.0
        
        confidence_factors = []
        
        # Vocal tract confidence
        if 'vocal_tract' in self.biometric_data:
            vt = self.biometric_data['vocal_tract']
            if vt['formant_dispersion'] > 500:  # Reasonable formant spacing
                confidence_factors.append(0.9)
        
        # Cord elasticity confidence
        if 'cord_elasticity' in self.biometric_data:
            ce = self.biometric_data['cord_elasticity']
            if ce['pitch_range_octaves'] > 0.5:  # Reasonable pitch range
                confidence_factors.append(0.8)
        
        # Neuromuscular timing confidence
        if 'neuromuscular_timing' in self.biometric_data:
            nt = self.biometric_data['neuromuscular_timing']
            if nt['onset_count'] > 10:  # Enough articulation events
                confidence_factors.append(0.7)
        
        return np.mean(confidence_factors) if confidence_factors else 0.5

def create_voiceprint(audio_path, output_path=None):
    """Main function to create sovereign voiceprint"""
    print(f"🎤 Processing: {audio_path}")
    
    vp = SovereignVoiceprint()
    biometrics = vp.extract_universal_biometrics(audio_path)
    
    if biometrics:
        result = vp.create_biological_hash()
        
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"💾 Voiceprint saved: {output_path}")
        
        return result
    else:
        print("❌ Failed to extract voiceprint")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 biological_core.py <audio_file>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_file = f"proofs/voiceprint_{hashlib.md5(audio_file.encode()).hexdigest()[:8]}.json"
    
    result = create_voiceprint(audio_file, output_file)
    if result:
        print(f"🎯 Biological Hash: {result['biological_hash']}")
        print(f"📊 Confidence: {result['confidence_score']:.1%}")
