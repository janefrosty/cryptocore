import os
from Crypto.Cipher import AES

class AuthenticationError(Exception):
   
    pass

class GCM:

    # Irreducible polynomial for GF(2^128): x^128 + x^7 + x^2 + x + 1
    R = 0xE1000000000000000000000000000000
    
    def __init__(self, key, nonce=None):

        self.aes = AES.new(key, AES.MODE_ECB)
        self.key = key
        
        # Standard nonce size for GCM is 12 bytes (96 bits)
        if nonce is None:
            self.nonce = os.urandom(12)
        else:
            self.nonce = nonce
        
        # Precompute H for GHASH: H = E_K(0^128)
        self.H = self._bytes_to_int(self.aes.encrypt(b'\x00' * 16))
        
        # Precompute multiplication table for performance
        self._precompute_table()
    
    def _bytes_to_int(self, data):
        return int.from_bytes(data, 'big')
    
    def _int_to_bytes(self, num):
        return num.to_bytes(16, 'big')
    
    def _precompute_table(self):
        self.M = [0] * 16
        
        # M[0] = 0
        # M[1] = H
        self.M[1] = self.H
        
        # M[i] = M[i-1] * 2 in GF(2^128)
        for i in range(2, 16):
            self.M[i] = self._mult_gf_quick(self.M[i-1], self.M[1])
    
    def _mult_gf_quick(self, x, y):
        z = 0
        y = self.H if y == self.H else y
        
        for i in range(16):
            # Process byte by byte
            byte = (x >> (120 - 8 * i)) & 0xFF
            
            if byte != 0:
                # Split byte into two 4-bit nibbles
                high = (byte >> 4) & 0x0F
                low = byte & 0x0F
                
                if high != 0:
                    z ^= self.M[high]
                
                if low != 0:
                    z ^= self.M[low]
            
            # Multiply y by x
            if i < 15:
                # Multiply current result by x^8
                for _ in range(8):
                    if z & 1:
                        z = (z >> 1) ^ self.R
                    else:
                        z >>= 1
        
        return z
    
    def _mult_gf_simple(self, x, y):
        z = 0
        v = y
        
        for i in range(127, -1, -1):
            if (x >> i) & 1:
                z ^= v
            
            # Multiply v by x
            if v & 1:
                v = (v >> 1) ^ self.R
            else:
                v >>= 1
        
        return z
    
    def _ghash(self, aad, ciphertext):
        # Prepare blocks: AAD || ciphertext || len(AAD) || len(ciphertext)
        blocks = []
        
        # Process AAD in 16-byte blocks
        for i in range(0, len(aad), 16):
            block = aad[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(self._bytes_to_int(block))
        
        # Process ciphertext in 16-byte blocks
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            if len(block) < 16:
                block += b'\x00' * (16 - len(block))
            blocks.append(self._bytes_to_int(block))
        
        # Add length blocks: len(AAD) || len(ciphertext)
        len_aad = len(aad) * 8  # length in bits
        len_ct = len(ciphertext) * 8
        
        blocks.append((len_aad << 64) | len_ct)
        
        # Compute GHASH
        y = 0
        for block in blocks:
            y ^= block
            y = self._mult_gf_quick(y, self.H)
        
        return y
    
    def _compute_tag(self, j0, ciphertext, aad):
        # Compute S = GHASH_H(AAD, C)
        s = self._ghash(aad, ciphertext)
        
        # Encrypt J0 with AES to get tag
        j0_enc = self.aes.encrypt(self._int_to_bytes(j0))
        t = self._bytes_to_int(j0_enc) ^ s
        
        return t
    
    def _generate_iv(self):
        if len(self.nonce) == 12:
            # Standard 96-bit nonce
            j0 = self._bytes_to_int(self.nonce + b'\x00\x00\x00\x01')
        else:
            # Non-standard nonce length
            # GHASH the nonce with empty AAD
            s = self._ghash(b'', self.nonce)
            j0 = s
        
        return j0
    
    def encrypt(self, plaintext, aad=b""):
        # Generate J0 from nonce
        j0 = self._generate_iv()
        
        # Encrypt using CTR mode with counters J0+1, J0+2, ...
        ciphertext = bytearray()
        blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
        
        for i, block in enumerate(blocks):
            # Counter = J0 + i + 1
            counter = j0 + i + 1
            counter_bytes = self._int_to_bytes(counter)[:16]
            
            # Encrypt counter to get keystream
            keystream = self.aes.encrypt(counter_bytes)
            
            # XOR with plaintext block
            encrypted_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            ciphertext.extend(encrypted_block)
        
        ciphertext = bytes(ciphertext)
        
        # Compute authentication tag
        tag = self._compute_tag(j0, ciphertext, aad)
        tag_bytes = self._int_to_bytes(tag)
        
        # Return: nonce || ciphertext || tag
        return self.nonce + ciphertext + tag_bytes
    
    def decrypt(self, data, aad=b""):
        # Parse input: nonce || ciphertext || tag
        if len(data) < 28:  # Minimum: 12 nonce + 0 ciphertext + 16 tag
            raise ValueError("Data too short for GCM format")
        
        nonce = data[:12]
        tag = data[-16:]
        ciphertext = data[12:-16]
        
        # Reinitialize with same nonce
        self.nonce = nonce
        self.H = self._bytes_to_int(self.aes.encrypt(b'\x00' * 16))
        self._precompute_table()
        
        # Generate J0 from nonce
        j0 = self._generate_iv()
        
        # Verify tag before decryption
        expected_tag = self._compute_tag(j0, ciphertext, aad)
        received_tag = self._bytes_to_int(tag)
        
        if expected_tag != received_tag:
            raise AuthenticationError("GCM authentication failed: tag mismatch")
        
        # Decrypt using CTR mode
        plaintext = bytearray()
        blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
        
        for i, block in enumerate(blocks):
            # Counter = J0 + i + 1
            counter = j0 + i + 1
            counter_bytes = self._int_to_bytes(counter)[:16]
            
            # Encrypt counter to get keystream
            keystream = self.aes.encrypt(counter_bytes)
            
            # XOR with ciphertext block
            decrypted_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
            plaintext.extend(decrypted_block)
        
        return bytes(plaintext)

def aes_gcm_encrypt(key, data, aad=b""):
    gcm = GCM(key)
    return gcm.encrypt(data, aad)

def aes_gcm_decrypt(key, data, aad=b""):
    gcm = GCM(key)
    return gcm.decrypt(data, aad)

def aes_gcm_encrypt_with_nonce(key, nonce, data, aad=b""):
    gcm = GCM(key, nonce)
    return gcm.encrypt(data, aad)