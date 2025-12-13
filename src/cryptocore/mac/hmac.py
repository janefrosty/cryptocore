"""
Sprint 5: HMAC implementation from scratch
Follows RFC 2104 specification using SHA-256 from Sprint 4
"""

from ..hash.sha256 import SHA256

class HMAC:
    """
    HMAC implementation following RFC 2104
    Uses SHA-256 as underlying hash function
    """
    
    def __init__(self, key, hash_function='sha256'):
        """
        Initialize HMAC with key
        Supports variable length keys as per RFC 2104
        """
        self.hash_function = SHA256()  # Use our SHA-256 from Sprint 4
        self.block_size = 64  # bytes for SHA-256
        self.key = self._process_key(key)
    
    def _process_key(self, key):
        """
        Process key according to RFC 2104:
        - If key longer than block size: hash it
        - If key shorter than block size: pad with zeros
        """
        if len(key) > self.block_size:
            # Hash key if longer than block size
            self.hash_function.update(key)
            key = bytes.fromhex(self.hash_function.hexdigest())
            self.hash_function = SHA256()  # Reset for actual computation
        
        # Pad with zeros if shorter than block size
        if len(key) < self.block_size:
            key = key + b'\x00' * (self.block_size - len(key))
        
        return key
    
    def _xor_bytes(self, a, b):
        """XOR two byte strings of equal length"""
        return bytes(x ^ y for x, y in zip(a, b))
    
    def compute(self, message):
        """
        Compute HMAC according to RFC 2104:
        HMAC(K, m) = H((K ⊕ opad) || H((K ⊕ ipad) || m))
        where H is SHA-256, opad = 0x5c repeated, ipad = 0x36 repeated
        """
        # Create inner and outer pads
        ipad = self._xor_bytes(self.key, b'\x36' * self.block_size)
        opad = self._xor_bytes(self.key, b'\x5c' * self.block_size)
        
        # Inner hash: H((K ⊕ ipad) || message)
        inner_hash = SHA256()
        inner_hash.update(ipad + message)
        inner_digest = bytes.fromhex(inner_hash.hexdigest())
        
        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hash = SHA256()
        outer_hash.update(opad + inner_digest)
        
        return outer_hash.hexdigest()
    
    def compute_file(self, filename, chunk_size=8192):
        """
        Compute HMAC for a file with chunk processing
        Supports large files with constant memory usage
        """
        # Process key once
        ipad = self._xor_bytes(self.key, b'\x36' * self.block_size)
        opad = self._xor_bytes(self.key, b'\x5c' * self.block_size)
        
        # Inner hash: H((K ⊕ ipad) || message)
        inner_hash = SHA256()
        inner_hash.update(ipad)
        
        # Process file in chunks
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                inner_hash.update(chunk)
        
        inner_digest = bytes.fromhex(inner_hash.hexdigest())
        
        # Outer hash: H((K ⊕ opad) || inner_hash)
        outer_hash = SHA256()
        outer_hash.update(opad + inner_digest)
        
        return outer_hash.hexdigest()

def hmac_sha256(key, data):
    """Convenience function for one-shot HMAC computation"""
    hmac = HMAC(key)
    return hmac.compute(data)

def hmac_sha256_file(key, filename, chunk_size=8192):
    """Convenience function for file HMAC computation"""
    hmac = HMAC(key)
    return hmac.compute_file(filename, chunk_size)