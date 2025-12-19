"""
PBKDF2-HMAC-SHA256 implementation.
"""

import struct
import hashlib
import hmac

def hmac_sha256(key, msg):
    """HMAC-SHA256 implementation."""
    return hmac.new(key, msg, hashlib.sha256).digest()

def pbkdf2_hmac_sha256(password, salt, iterations, dklen):
    """
    PBKDF2 with HMAC-SHA256 implementation.
    
    Args:
        password: The password as bytes or string
        salt: The salt as bytes or string
        iterations: Number of iterations
        dklen: Desired key length in bytes
    
    Returns:
        Derived key as bytes
    """
    # Convert inputs to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    if isinstance(salt, str):
        # Check if it's hex string
        try:
            salt = bytes.fromhex(salt)
        except ValueError:
            salt = salt.encode('utf-8')
    
    # Calculate number of blocks needed (SHA-256 produces 32-byte blocks)
    hlen = 32
    blocks_needed = (dklen + hlen - 1) // hlen
    
    derived_key = b''
    
    for i in range(1, blocks_needed + 1):
        # Compute block: U1 = HMAC(password, salt || INT_32_BE(i))
        block_salt = salt + struct.pack('>I', i)
        u_current = hmac_sha256(password, block_salt)
        block = u_current
        
        # Compute U2 through Uc and XOR them
        for _ in range(2, iterations + 1):
            u_current = hmac_sha256(password, u_current)
            # XOR u_current into block
            block = bytes(a ^ b for a, b in zip(block, u_current))
        
        derived_key += block
    
    # Return exactly dklen bytes
    return derived_key[:dklen]