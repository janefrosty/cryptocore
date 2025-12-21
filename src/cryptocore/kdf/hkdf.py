
import hashlib
import hmac

def hkdf(ikm, info=b"", length=32, salt=None):
    """
    Simple HKDF-HMAC-SHA256 implementation.
    
    Args:
        ikm: Input Keying Material (bytes)
        info: Context info (bytes)
        length: Output length in bytes
        salt: Salt (bytes, optional)
    
    Returns:
        Derived key (bytes)
    """
    if salt is None:
        salt = b"\x00" * 32
    
    # Extract phase
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    
    # Expand phase
    okm = b""
    t = b""
    
    for i in range(1, (length + 31) // 32 + 1):
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha256).digest()
        okm += t
    
    return okm[:length]