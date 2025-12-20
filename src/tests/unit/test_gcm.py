#!/usr/bin/env python3
"""
Sprint 6: GCM test suite
Tests Galois/Counter Mode implementation with authentication
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.modes.gcm import GCM, aes_gcm_encrypt, aes_gcm_decrypt, AuthenticationError

def test_gcm_round_trip():
    print("Testing GCM round trip...")
    
    import os
    key = os.urandom(16)
    plaintext = b"Test message for GCM"
    aad = b"Associated data"
    
    ciphertext = aes_gcm_encrypt(key, plaintext, aad)
    
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad)
        if decrypted == plaintext:
            print("  PASS: GCM round trip successful")
            return True
        else:
            print("  FAIL: GCM decryption mismatch")
            return False
    except Exception as e:
        print(f"  FAIL: GCM round trip failed: {e}")
        return False

def test_gcm_aad_tamper():
    print("Testing GCM AAD tamper detection...")
    
    import os
    key = os.urandom(16)
    plaintext = b"Secret message"
    aad_correct = b"correct_aad"
    aad_wrong = b"wrong_aad"
    
    ciphertext = aes_gcm_encrypt(key, plaintext, aad_correct)
    
    try:
        decrypted = aes_gcm_decrypt(key, ciphertext, aad_wrong)
        print("  FAIL: GCM should have failed with wrong AAD")
        return False
    except AuthenticationError:
        print("  PASS: GCM correctly failed with wrong AAD")
        return True
    except Exception as e:
        print(f"  FAIL: GCM wrong AAD test failed: {e}")
        return False

if __name__ == "__main__":
    print("GCM Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    try:
        all_passed &= test_gcm_round_trip()
        print()
        
        all_passed &= test_gcm_aad_tamper()
        print()
        
        if all_passed:
            print("GCM tests passed!")
        else:
            print("GCM tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test suite failed with exception: {e}")
        sys.exit(1)