"""
Sprint 6: Galois/Counter Mode (GCM) implementation
Follows NIST SP 800-38D specification for authenticated encryption
"""

import os
from Crypto.Cipher import AES

class AuthenticationError(Exception):
    """Exception raised when GCM authentication fails"""
    pass

class GCM:
    """
    GCM implementation with Galois Field multiplication in GF(2^128)
    Provides authenticated encryption with associated data (AEAD)
    """
    
    R = 0xE1000000000000000000000000000000
    
    def __init__(self, key, nonce=None):
        self.aes = AES.new(key, AES.MODE_ECB)
        self.key = key
        
        if nonce is None:
            self.nonce = os.urandom(12)
        else:
            self.nonce = nonce
        
        self.H = self._bytes_to_int(self.aes.encrypt(b'\x00' * 16))
        self._precompute_table()
    
    def _bytes_to_int(self, data):
        return int.from_bytes(data, 'big')
    
    def _int_to_bytes(self, num):
        return num.to_bytes(16, 'big')
    
    def _precompute_table(self):
        self.M = [0] * 16
        self.M[1] = self.H
        
        for i in range(2, 16):
            self.M[i] = self._mult_gf_quick(self.M[i-1], self.M[1])
    
    def _mult_gf_quick(self, x, y):
        z = 0
        y = self.H if y == self.H else y
        
        for i in range(16):
            byte = (x >> (120 - 8 * i)) & 0xFF
            
            if byte != 0:
                high = (byte >> 4) & 0x0F
                low = byte & 0x0F
                
                if high != 0:
                    z ^= self.M[high]
                
                if low != 0:
                    z ^= self.M[low]
            
            if i < 15:
                for _ in range(8):
                    if z & 1:
                        z = (z >> 1) ^ self.R
                    else:
                        z >>= 1
        
        return z
    
    def _ghash(self, aad, ciphertext):
        blocks = []
        
        for i in range(0, len(aad), 16):
            block = aad[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(self._bytes_to_int(block))
        
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(self._bytes_to_int(block))
        
        len_aad = len(aad) * 8
        len_ct = len(ciphertext) * 8
        blocks.append((len_aad << 64) | len_ct)
        
        y = 0
        for block in blocks:
            y ^= block
            y = self._mult_gf_quick(y, self.H)
        
        return y
    
    def _compute_tag(self, j0, ciphertext, aad):
        s = self._ghash(aad, ciphertext)
        j0_enc = self.aes.encrypt(self._int_to_bytes(j0))
        t = self._bytes_to_int(j0_enc) ^ s
        return t
    
    def _generate_iv(self):
        if len(self.nonce) == 12:
            j0 = self._bytes_to_int(self.nonce + b'\x00\x00\x00\x01')
        else:
            s = self._ghash(b'', self.nonce)
            j0 = s
        
        return j0
    
    def encrypt(self, plaintext, aad=b""):
        j0 = self._generate_iv()
        ciphertext = bytearray()
        blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
        
        for i, block in enumerate(blocks):
            counter = j0 + i + 1
            counter_bytes = self._int_to_bytes(counter)[:16]
            keystream = self.aes.encrypt(counter_bytes)
            encrypted_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            ciphertext.extend(encrypted_block)
        
        ciphertext = bytes(ciphertext)
        tag = self._compute_tag(j0, ciphertext, aad)
        tag_bytes = self._int_to_bytes(tag)
        
        return self.nonce + ciphertext + tag_bytes
    
    def decrypt(self, data, aad=b""):
        if len(data) < 28:
            raise ValueError("Data too short for GCM format")
        
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]
        
        self.nonce = nonce
        self.H = self._bytes_to_int(self.aes.encrypt(b'\x00' * 16))
        self._precompute_table()
        
        j0 = self._generate_iv()
        expected_tag = self._compute_tag(j0, ciphertext, aad)
        received_tag = self._bytes_to_int(tag)
        
        if expected_tag != received_tag:
            raise AuthenticationError("GCM authentication failed: tag mismatch")
        
        plaintext = bytearray()
        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        
        for i, block in enumerate(blocks):
            counter = j0 + i + 1
            counter_bytes = self._int_to_bytes(counter)[:16]
            keystream = self.aes.encrypt(counter_bytes)
            decrypted_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            plaintext.extend(decrypted_block)
        
        return bytes(plaintext)

def aes_gcm_encrypt(key, data, aad=b""):
    gcm = GCM(key)
    return gcm.encrypt(data, aad)

def aes_gcm_decrypt(key, data, aad=b""):
    gcm = GCM(key)
    return gcm.decrypt(data, aad)