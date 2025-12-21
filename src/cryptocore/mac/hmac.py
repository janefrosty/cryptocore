"""
HMAC (Hash-based Message Authentication Code) implementation
"""

import math

class HMAC:
    """HMAC implementation supporting multiple hash functions"""
    
    def __init__(self, key, hash_class):
        """
        Initialize HMAC with key and hash function.
        
        Args:
            key: Secret key as bytes
            hash_class: Hash class with update() and digest() methods
        """
        if not isinstance(key, bytes):
            key = key.encode('utf-8') if isinstance(key, str) else bytes(key)
        
        self.hash_class = hash_class
        self.block_size = 64  # Block size for SHA-256
        
        # Keys longer than block_size are hashed
        if len(key) > self.block_size:
            hash_obj = hash_class()
            hash_obj.update(key)
            key = hash_obj.digest()
        
        # Keys shorter than block_size are padded with zeros
        if len(key) < self.block_size:
            key = key + b'\x00' * (self.block_size - len(key))
        
        # Create inner and outer padded keys
        self.inner_pad = bytes(x ^ 0x36 for x in key)
        self.outer_pad = bytes(x ^ 0x5C for x in key)
        
        # Initialize inner hash
        self.inner_hash = hash_class()
        self.inner_hash.update(self.inner_pad)
        
        # Track if we've already computed the digest
        self._digest_computed = False
        self._digest = None
    
    def update(self, data):
        """
        Add data to HMAC calculation.
        
        Args:
            data: Data as bytes
        """
        if self._digest_computed:
            raise RuntimeError("HMAC digest already computed")
        
        if not isinstance(data, bytes):
            data = data.encode('utf-8') if isinstance(data, str) else bytes(data)
        
        self.inner_hash.update(data)
        return self
    
    def digest(self):
        """
        Return HMAC digest as bytes.
        """
        if self._digest_computed:
            return self._digest
        
        # Get inner hash digest
        inner_digest = self.inner_hash.digest()
        
        # Compute outer hash
        outer_hash = self.hash_class()
        outer_hash.update(self.outer_pad)
        outer_hash.update(inner_digest)
        
        self._digest = outer_hash.digest()
        self._digest_computed = True
        
        return self._digest
    
    def hexdigest(self):
        """
        Return HMAC digest as hexadecimal string.
        """
        return self.digest().hex()


# Convenience functions
def hmac_sha256(key, message):
    """
    Convenience function for HMAC-SHA256.
    
    Args:
        key: Secret key as bytes or string
        message: Message as bytes or string
    
    Returns:
        HMAC-SHA256 digest as bytes
    """
    from ..hash.sha256 import SHA256
    hmac = HMAC(key, SHA256)
    hmac.update(message)
    return hmac.digest()