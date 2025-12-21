"""
PBKDF2-HMAC-SHA256 implementation following RFC 2898
"""

import os
import sys

# Добавляем путь к корню проекта для импортов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Используем абсолютные импорты
try:
    from cryptocore.mac.hmac import HMAC
    from cryptocore.hash.sha256 import SHA256
except ImportError:
    # Альтернативный путь для тестов
    try:
        from ..mac.hmac import HMAC
        from ..hash.sha256 import SHA256
    except ImportError:
        from mac.hmac import HMAC
        from hash.sha256 import SHA256


def pbkdf2_hmac_sha256(password, salt, iterations, dklen):
    """
    PBKDF2-HMAC-SHA256 key derivation function
    
    Args:
        password: Password as bytes or string
        salt: Salt as bytes, string, or hex string
        iterations: Number of iterations (int)
        dklen: Desired key length in bytes (int)
    
    Returns:
        Derived key as bytes
    """
    # Convert inputs to bytes if needed
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    if isinstance(salt, str):
        # Check if it's a hex string
        try:
            if all(c in '0123456789abcdefABCDEF' for c in salt):
                salt = bytes.fromhex(salt)
            else:
                salt = salt.encode('utf-8')
        except:
            salt = salt.encode('utf-8')
    
    # Calculate number of blocks needed (SHA-256 output is 32 bytes)
    blocks_needed = (dklen + 31) // 32
    derived_key = b''
    
    for block_index in range(1, blocks_needed + 1):
        # U1 = HMAC(password, salt || INT_32_BE(i))
        block_salt = salt + block_index.to_bytes(4, 'big')
        
        # Используем нашу реализацию HMAC
        hmac_calculator = HMAC(password, SHA256)
        hmac_calculator.update(block_salt)
        block = hmac_calculator.digest()
        u_prev = block
        
        # Compute U2 through Uc (iterations)
        for _ in range(2, iterations + 1):
            hmac_calculator = HMAC(password, SHA256)
            hmac_calculator.update(u_prev)
            u_curr = hmac_calculator.digest()
            
            # XOR u_curr into block
            block = bytes(a ^ b for a, b in zip(block, u_curr))
            u_prev = u_curr
        
        derived_key += block
    
    # Return exactly dklen bytes
    return derived_key[:dklen]


def generate_salt(length=16):
    """Generate a cryptographically secure random salt"""
    return os.urandom(length)


def test_basic():
    """Basic test function"""
    print("Testing PBKDF2...")
    
    # Simple test
    password = "test"
    salt = b"salt123"
    iterations = 1000
    dklen = 32
    
    key = pbkdf2_hmac_sha256(password, salt, iterations, dklen)
    print(f"Key derived: {key.hex()}")
    print(f"Key length: {len(key)} bytes")
    
    # Test with hex salt
    salt_hex = "73616c74"  # "salt" in hex
    key2 = pbkdf2_hmac_sha256("password", salt_hex, 1, 20)
    print(f"\nRFC 6070 test vector 1: {key2.hex()}")
    
    return key


if __name__ == "__main__":
    test_basic()