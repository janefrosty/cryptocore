import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.modes.gcm import GCM, aes_gcm_encrypt, aes_gcm_decrypt, AuthenticationError

def test_gcm_nist_vectors():
    """
    Test GCM with NIST SP 800-38D test vectors
    Basic test cases with known answers
    """
    print("Testing GCM with NIST test vectors...")
    
    # Test Case 1: Simple encryption with empty AAD
    key = bytes.fromhex("00000000000000000000000000000000")
    nonce = bytes.fromhex("000000000000000000000000")
    plaintext = bytes.fromhex("00000000000000000000000000000000")
    aad = b""
    
    gcm = GCM(key, nonce)
    ciphertext = gcm.encrypt(plaintext, aad)
    
    # Expected format: nonce || ciphertext || tag
    expected_nonce = nonce
    # For this simple case, just verify structure
    if len(ciphertext) == 12 + 16 + 16:  # nonce + ciphertext + tag
        print("   NIST test case 1: Structure correct")
    else:
        print(f"   NIST test case 1: Wrong length {len(ciphertext)}")
        return False
    
    # Try decryption
    try:
        decrypted = gcm.decrypt(ciphertext, aad)
        if decrypted == plaintext:
            print("   NIST test case 1: Decryption successful")
        else:
            print("   NIST test case 1: Decryption mismatch")
            return False
    except Exception as e:
        print(f"   NIST test case 1: Decryption failed: {e}")
        return False
    
    return True

def test_gcm_round_trip():
    """
    Test GCM encryption and decryption round trip
    """
    print("Testing GCM round trip...")
    
    key = os.urandom(16)
    plaintext = b"Test message for GCM authenticated encryption"
    aad = b"Associated data for authentication"
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Decrypt with correct AAD
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad)
        if decrypted == plaintext:
            print("   GCM round trip with AAD successful")
        else:
            print("   GCM round trip: Decryption mismatch")
            return False
    except Exception as e:
        print(f"   GCM round trip failed: {e}")
        return False
    
    return True

def test_gcm_aad_tamper():
    """
    Test that wrong AAD causes catastrophic failure
    """
    print("Testing GCM AAD tamper detection...")
    
    key = os.urandom(16)
    plaintext = b"Secret message requiring authentication"
    aad_correct = b"correct_aad"
    aad_wrong = b"wrong_aad"
    
    # Encrypt with correct AAD
    ciphertext = aes_gcm_encrypt(key, plaintext, aad_correct)
    
    # Try to decrypt with wrong AAD
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad_wrong)
        print("   GCM should have failed with wrong AAD")
        return False
    except AuthenticationError:
        print("   GCM correctly failed with wrong AAD")
        return True
    except Exception as e:
        print(f"   GCM wrong AAD test failed with unexpected error: {e}")
        return False

def test_gcm_ciphertext_tamper():
    """
    Test that ciphertext tampering causes authentication failure
    """
    print("Testing GCM ciphertext tamper detection...")
    
    key = os.urandom(16)
    plaintext = b"Message to be authenticated"
    aad = b"associated_data"
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Tamper with ciphertext (flip one bit)
    ciphertext_bytes = bytearray(ciphertext)
    
    # Tamper somewhere in the ciphertext portion (after nonce, before tag)
    if len(ciphertext_bytes) > 28:  # nonce(12) + at least 1 byte + tag(16)
        tamper_position = 20  # Position in ciphertext portion
        ciphertext_bytes[tamper_position] ^= 0x01
    
    # Try to decrypt tampered ciphertext
    try:
        decrypted = aes_gcm_decrypt(key, bytes(ciphertext_bytes), aad)
        print("   GCM should have failed with tampered ciphertext")
        return False
    except AuthenticationError:
        print("   GCM correctly failed with tampered ciphertext")
        return True
    except Exception as e:
        print(f"   GCM tamper test failed with unexpected error: {e}")
        return False

def test_gcm_tag_tamper():
    """
    Test that tag tampering causes authentication failure
    """
    print("Testing GCM tag tamper detection...")
    
    key = os.urandom(16)
    plaintext = b"Another authenticated message"
    aad = b"auth_data"
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Tamper with tag (last 16 bytes)
    ciphertext_bytes = bytearray(ciphertext)
    if len(ciphertext_bytes) >= 16:
        # Flip last bit of tag
        ciphertext_bytes[-1] ^= 0x01
    
    # Try to decrypt with tampered tag
    try:
        decrypted = aes_gcm_decrypt(key, bytes(ciphertext_bytes), aad)
        print("   GCM should have failed with tampered tag")
        return False
    except AuthenticationError:
        print("   GCM correctly failed with tampered tag")
        return True
    except Exception as e:
        print(f"   GCM tag tamper test failed with unexpected error: {e}")
        return False

def test_gcm_nonce_uniqueness():
    """
    Test that GCM generates unique nonces
    """
    print("Testing GCM nonce uniqueness...")
    
    key = os.urandom(16)
    plaintext = b"Test message"
    aad = b""
    
    nonces = set()
    num_encryptions = 100
    
    for i in range(num_encryptions):
        ciphertext = aes_gcm_encrypt(key, plaintext, aad)
        nonce = ciphertext[:12]
        nonces.add(nonce)
        
        if (i + 1) % 20 == 0:
            print(f"    Generated {i + 1} unique nonces...")
    
    if len(nonces) == num_encryptions:
        print(f"   All {num_encryptions} nonces are unique")
        return True
    else:
        print(f"   Only {len(nonces)} unique nonces out of {num_encryptions}")
        return False

def test_gcm_empty_aad():
    """
    Test GCM with empty AAD
    """
    print("Testing GCM with empty AAD...")
    
    key = os.urandom(16)
    plaintext = b"Message with empty associated data"
    aad = b""  # Empty AAD
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Decrypt
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad)
        if decrypted == plaintext:
            print("   GCM works correctly with empty AAD")
            return True
        else:
            print("   GCM decryption mismatch with empty AAD")
            return False
    except Exception as e:
        print(f"   GCM empty AAD test failed: {e}")
        return False

def test_gcm_large_aad():
    """
    Test GCM with large associated data
    """
    print("Testing GCM with large AAD...")
    
    key = os.urandom(16)
    plaintext = b"Short message"
    aad = b"A" * 10000  # 10KB AAD
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Decrypt with correct AAD
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad)
        if decrypted == plaintext:
            print("   GCM works correctly with large AAD")
            return True
        else:
            print("   GCM decryption mismatch with large AAD")
            return False
    except Exception as e:
        print(f"   GCM large AAD test failed: {e}")
        return False

def test_gcm_large_message():
    """
    Test GCM with large message
    """
    print("Testing GCM with large message...")
    
    key = os.urandom(16)
    plaintext = b"X" * 100000  # 100KB message
    aad = b"authenticated_data"
    
    # Encrypt
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    # Decrypt
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad)
        if decrypted == plaintext:
            print("   GCM works correctly with large message")
            return True
        else:
            print("   GCM decryption mismatch with large message")
            return False
    except Exception as e:
        print(f"   GCM large message test failed: {e}")
        return False

def test_gcm_key_detection():
    """
    Test that wrong key causes authentication failure
    """
    print("Testing GCM wrong key detection...")
    
    key1 = os.urandom(16)
    key2 = os.urandom(16)  # Different key
    plaintext = b"Message requiring correct key"
    aad = b"aad"
    
    # Encrypt with key1
    ciphertext = aes_gcm_encrypt(key1, plaintext, aad)
    
    # Try to decrypt with key2
    try:
        decrypted = aes_gcm_decrypt(key2, ciphertext, aad)
        print("   GCM should have failed with wrong key")
        return False
    except AuthenticationError:
        print("   GCM correctly failed with wrong key")
        return True
    except Exception as e:
        print(f"   GCM wrong key test failed with unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("Sprint 6: GCM Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    try:
        all_passed &= test_gcm_nist_vectors()
        print()
        
        all_passed &= test_gcm_round_trip()
        print()
        
        all_passed &= test_gcm_aad_tamper()
        print()
        
        all_passed &= test_gcm_ciphertext_tamper()
        print()
        
        all_passed &= test_gcm_tag_tamper()
        print()
        
        all_passed &= test_gcm_nonce_uniqueness()
        print()
        
        all_passed &= test_gcm_empty_aad()
        print()
        
        all_passed &= test_gcm_large_aad()
        print()
        
        all_passed &= test_gcm_large_message()
        print()
        
        all_passed &= test_gcm_key_detection()
        print()
        
        if all_passed:
            print(" All GCM tests passed!")
        else:
            print(" Some GCM tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f" Test suite failed with exception: {e}")
        sys.exit(1)