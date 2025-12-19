"""
Key hierarchy function for deriving multiple keys from a master key.
"""

import struct
from ..mac.hmac import hmac_sha256

def derive_key(master_key, context, length=32):
    """
    Derive a key from a master key using deterministic HMAC-based method.
    
    Args:
        master_key: The master key as bytes
        context: Context string (e.g., "encryption", "authentication")
        length: Desired key length in bytes
    
    Returns:
        Derived key as bytes
    """
    if isinstance(context, str):
        context = context.encode('utf-8')
    
    if not isinstance(master_key, bytes):
        raise TypeError("master_key must be bytes")
    
    derived = b''
    counter = 1
    
    while len(derived) < length:
        # T_i = HMAC(master_key, context || counter)
        block = hmac_sha256(master_key, context + struct.pack('>I', counter))
        derived += block # type: ignore
        counter += 1
    
    # Return exactly the requested length
    return derived[:length]