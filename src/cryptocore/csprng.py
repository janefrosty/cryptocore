import os
import sys

def generate_random_bytes(num_bytes):
    """
    Sprint 3: Cryptographically secure random number generator
    Uses os.urandom() for system-level entropy
    """
    if num_bytes <= 0:
        raise ValueError("Number of bytes must be positive")
    
    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to generate random bytes: {e}")

def generate_key(key_size=16):
    """
    Sprint 3: Generate random encryption key
    Default 16 bytes for AES-128
    """
    return generate_random_bytes(key_size)

def generate_iv():
    """
    Sprint 2: Generate random initialization vector
    16 bytes for AES block size
    """
    return generate_random_bytes(16)