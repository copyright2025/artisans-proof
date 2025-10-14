#!/usr/bin/env python3
"""
Image Attachment System - Phase 3
Encrypted lyric diaries with version control
"""

import hashlib
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class ImageAttachmentSystem:
    def __init__(self):
        print("📸 IMAGE ATTACHMENT SYSTEM - PHASE 3")
        
    def encrypt_lyric_diary(self, image_path, fractal_seed):
        """Encrypt image using fractal seed as key"""
        # Derive encryption key from fractal seed
        encryption_key = self.derive_encryption_key(fractal_seed)
        
        # Read and encrypt image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        encrypted_data = self.aes_encrypt(image_data, encryption_key)
        content_hash = hashlib.sha256(encrypted_data).hexdigest()
        
        return encrypted_data, content_hash
    
    def derive_encryption_key(self, fractal_seed):
        """Derive AES key from fractal seed"""
        # Use fractal seed to create deterministic encryption key
        key_material = fractal_seed.encode() + b'artisans_proof_phase3'
        return hashlib.sha256(key_material).digest()
    
    def aes_encrypt(self, data, key):
        """AES-256 encrypt data"""
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = cipher.iv
        return iv + ct_bytes
    
    def create_attachment_record(self, encrypted_data, content_hash, attachment_type, description, previous_version=None):
        """Create attachment record for blockchain"""
        attachment = {
            'content_hash': content_hash,
            'attachment_type': attachment_type,
            'description': description,
            'timestamp': self.current_timestamp(),
            'data_size': len(encrypted_data),
            'previous_version': previous_version
        }
        
        return attachment
    
    def decrypt_lyric_diary(self, encrypted_data, fractal_seed):
        """Decrypt image using fractal seed"""
        encryption_key = self.derive_encryption_key(fractal_seed)
        
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        
        return pt
    
    def current_timestamp(self):
        import time
        return int(time.time())

if __name__ == "__main__":
    print("Encrypted lyric diary system ready")
    print("Version control for creative process documentation")
