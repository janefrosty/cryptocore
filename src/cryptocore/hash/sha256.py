"""
SHA-256 hash implementation
"""

import struct
import binascii

class SHA256:
    """SHA-256 hash algorithm implementation"""
    
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    _h0 = 0x6a09e667
    _h1 = 0xbb67ae85
    _h2 = 0x3c6ef372
    _h3 = 0xa54ff53a
    _h4 = 0x510e527f
    _h5 = 0x9b05688c
    _h6 = 0x1f83d9ab
    _h7 = 0x5be0cd19
    
    # Constants (first 32 bits of fractional parts of cube roots of first 64 primes)
    _k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    def __init__(self, data=None):
        """Initialize SHA-256 context"""
        self._h = [
            self._h0, self._h1, self._h2, self._h3,
            self._h4, self._h5, self._h6, self._h7
        ]
        self._data_len = 0
        self._buffer = b''
        
        if data:
            self.update(data)
    
    def _right_rotate(self, value, count):
        """Right rotate a 32-bit value"""
        return ((value >> count) | (value << (32 - count))) & 0xFFFFFFFF
    
    def _process_chunk(self, chunk):
        """Process a 64-byte chunk"""
        # Prepare message schedule
        w = list(struct.unpack('>16I', chunk))
        
        # Extend to 64 words
        for i in range(16, 64):
            s0 = self._right_rotate(w[i-15], 7) ^ self._right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = self._right_rotate(w[i-2], 17) ^ self._right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
            w.append((w[i-16] + s0 + w[i-7] + s1) & 0xFFFFFFFF)
        
        # Initialize working variables
        a, b, c, d, e, f, g, h = self._h
        
        # Main compression loop
        for i in range(64):
            s1 = self._right_rotate(e, 6) ^ self._right_rotate(e, 11) ^ self._right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + self._k[i] + w[i]) & 0xFFFFFFFF
            s0 = self._right_rotate(a, 2) ^ self._right_rotate(a, 13) ^ self._right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & 0xFFFFFFFF
            
            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        # Update hash values
        self._h[0] = (self._h[0] + a) & 0xFFFFFFFF
        self._h[1] = (self._h[1] + b) & 0xFFFFFFFF
        self._h[2] = (self._h[2] + c) & 0xFFFFFFFF
        self._h[3] = (self._h[3] + d) & 0xFFFFFFFF
        self._h[4] = (self._h[4] + e) & 0xFFFFFFFF
        self._h[5] = (self._h[5] + f) & 0xFFFFFFFF
        self._h[6] = (self._h[6] + g) & 0xFFFFFFFF
        self._h[7] = (self._h[7] + h) & 0xFFFFFFFF
    
    def update(self, data):
        """
        Update hash with new data.
        
        Args:
            data: Data as bytes
        """
        if not isinstance(data, bytes):
            if isinstance(data, str):
                data = data.encode('utf-8')
            else:
                data = bytes(data)
        
        self._data_len += len(data)
        self._buffer += data
        
        # Process complete 64-byte chunks
        while len(self._buffer) >= 64:
            chunk = self._buffer[:64]
            self._buffer = self._buffer[64:]
            self._process_chunk(chunk)
        
        return self
    
    def digest(self):
        """
        Return digest as bytes.
        """
        # Make a copy to avoid modifying the original
        buffer = self._buffer
        data_len = self._data_len
        
        # Append the bit '1' to the message
        buffer += b'\x80'
        
        # Append zeros until length is 56 mod 64
        while (len(buffer) % 64) != 56:
            buffer += b'\x00'
        
        # Append original length in bits as 64-bit big-endian integer
        buffer += struct.pack('>Q', data_len * 8)
        
        # Process final chunks
        temp_hash = SHA256()
        temp_hash._h = self._h.copy()
        
        for i in range(0, len(buffer), 64):
            temp_hash._process_chunk(buffer[i:i+64])
        
        # Convert hash to bytes
        return struct.pack('>8I', *temp_hash._h)
    
    def hexdigest(self):
        """
        Return digest as hexadecimal string.
        """
        return self.digest().hex()


# Convenience function
def sha256(data):
    """
    Compute SHA-256 hash of data.
    
    Args:
        data: Data as bytes or string
    
    Returns:
        SHA-256 hash as bytes
    """
    h = SHA256()
    h.update(data if isinstance(data, bytes) else data.encode('utf-8'))
    return h.digest()