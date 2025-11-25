import os
import sys

def generate_random_bytes(num_bytes):
    if num_bytes <= 0:
        raise ValueError("Number of bytes must be positive")
    
    try:
        return os.urandom(num_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to generate random bytes: {e}")

def generate_key(key_size=16):
    return generate_random_bytes(key_size)

def generate_iv():
    return generate_random_bytes(16)