"""
Sprint 6: Authenticated Encryption with Associated Data (AEAD)
Encrypt-then-MAC paradigm combining encryption modes with HMAC
"""

from ..mac.hmac import HMAC
from ..modes.ctr import aes_ctr_encrypt, aes_ctr_decrypt
import os
import hmac as python_hmac
import hashlib

class AuthenticationError(Exception):
    """Exception for AEAD authentication failures"""
    pass

class EncryptThenMAC:
    """
    Encrypt-then-MAC AEAD implementation
    Combines CTR encryption with HMAC-SHA256 authentication
    Derives separate encryption and MAC keys from master key
    """
    
    def __init__(self, master_key):
        """
        Initialize with master key
        Derives separate keys for encryption and MAC using HKDF
        """
        self.master_key = master_key
        
        # Derive keys using simple KDF (for educational purposes)
        # In production, use proper HKDF
        self.enc_key = self._derive_key(b"encryption")
        self.mac_key = self._derive_key(b"authentication")
        
        # Initialize HMAC
        self.hmac = HMAC(self.mac_key)
    
    def _derive_key(self, context):
        """Simple key derivation for educational purposes"""
        # Use HMAC-based KDF
        h = python_hmac.new(self.master_key, context, hashlib.sha256)
        return h.digest()[:16]  # 16 bytes for AES-128
    
    def encrypt(self, plaintext, aad=b""):
        """
        Encrypt-then-MAC operation
        Returns: nonce || ciphertext || tag
        """
        # Generate random nonce
        nonce = os.urandom(12)
        
        # Encrypt with CTR mode using nonce as IV
        ciphertext = aes_ctr_encrypt(self.enc_key, plaintext, nonce)
        
        # Compute MAC over ciphertext || AAD
        mac_data = ciphertext + aad
        tag = self.hmac.compute(mac_data)
        tag_bytes = bytes.fromhex(tag)[:16]  # Use first 16 bytes as tag
        
        # Return: nonce || ciphertext || tag
        return nonce + ciphertext + tag_bytes
    
    def decrypt(self, data, aad=b""):
        """
        Decrypt and verify MAC
        Returns plaintext if authentication succeeds
        """
        if len(data) < 28:  # Minimum: 12 nonce + 0 ciphertext + 16 tag
            raise ValueError("Data too short for AEAD format")
        
        # Parse components
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]
        
        # Verify MAC before decryption
        mac_data = ciphertext + aad
        expected_tag = self.hmac.compute(mac_data)
        expected_tag_bytes = bytes.fromhex(expected_tag)[:16]
        
        # Use constant-time comparison
        if not self._constant_time_compare(tag, expected_tag_bytes):
            raise AuthenticationError("MAC verification failed")
        
        # Decrypt if MAC is valid
        plaintext = aes_ctr_decrypt(self.enc_key, ciphertext, nonce)
        
        return plaintext
    
    def _constant_time_compare(self, a, b):
        """Constant-time comparison to prevent timing attacks"""
        if len(a) != len(b):
            return False
        
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0

def encrypt_then_mac_encrypt(key, plaintext, aad=b""):
    """Convenience function for Encrypt-then-MAC encryption"""
    aead = EncryptThenMAC(key)
    return aead.encrypt(plaintext, aad)

def encrypt_then_mac_decrypt(key, data, aad=b""):
    """Convenience function for Encrypt-then-MAC decryption"""
    aead = EncryptThenMAC(key)
    return aead.decrypt(data, aad)