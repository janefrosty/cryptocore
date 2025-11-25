#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.hash.sha256 import SHA256, sha256_hash, sha256_file
from cryptocore.hash.sha3_256 import SHA3_256, sha3_256_hash, sha3_256_file

def test_sha256_known_answers():
    print("Testing SHA-256 with known answers...")
    
    # NIST test vectors
    test_vectors = [
        # (input, expected_hash)
        ("", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        ("abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
        ("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq", 
         "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1"),
    ]
    
    for test_input, expected in test_vectors:
        result = sha256_hash(test_input.encode('utf-8') if test_input else b"")
        if result == expected:
            print(f"   '{test_input[:20]}...' -> {expected[:16]}...")
        else:
            print(f"   '{test_input}' failed")
            print(f"     Expected: {expected}")
            print(f"     Got:      {result}")
            return False
    
    print("   All SHA-256 known answer tests passed")
    return True

def test_sha3_256_known_answers():
    print("Testing SHA3-256 with known answers...")
    
    test_vectors = [
        # (input, expected_hash)
        ("", "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a"),
        ("abc", "3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532"),
    ]
    
    for test_input, expected in test_vectors:
        result = sha3_256_hash(test_input.encode('utf-8') if test_input else b"")
        if result == expected:
            print(f"   '{test_input[:20]}...' -> {expected[:16]}...")
        else:
            print(f"   '{test_input}' failed")
            print(f"     Expected: {expected}")
            print(f"     Got:      {result}")
            return False
    
    print("   All SHA3-256 known answer tests passed")
    return True

def test_avalanche_effect():
    print("Testing avalanche effect...")
    
    # Test data
    original_data = b"Hello, CryptoCore! This is avalanche effect testing."
    modified_data = b"Hello, CryptoCore! This is avalanche effect testing?"  # Changed last character
    
    # SHA-256
    sha256_1 = sha256_hash(original_data)
    sha256_2 = sha256_hash(modified_data)
    
    # Convert to binary and count differing bits
    bin1 = bin(int(sha256_1, 16))[2:].zfill(256)
    bin2 = bin(int(sha256_2, 16))[2:].zfill(256)
    diff_count_sha256 = sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))
    
    # SHA3-256
    sha3_1 = sha3_256_hash(original_data)
    sha3_2 = sha3_256_hash(modified_data)
    
    bin1_sha3 = bin(int(sha3_1, 16))[2:].zfill(256)
    bin2_sha3 = bin(int(sha3_2, 16))[2:].zfill(256)
    diff_count_sha3 = sum(bit1 != bit2 for bit1, bit2 in zip(bin1_sha3, bin2_sha3))
    
    print(f"  SHA-256 bits changed: {diff_count_sha256}/256 ({diff_count_sha256/256*100:.1f}%)")
    print(f"  SHA3-256 bits changed: {diff_count_sha3}/256 ({diff_count_sha3/256*100:.1f}%)")
    
    # Avalanche effect: should be ~128 bits changed (50%)
    if 100 < diff_count_sha256 < 156 and 100 < diff_count_sha3 < 156:
        print("   Strong avalanche effect confirmed")
        return True
    else:
        print("   Weak avalanche effect")
        return False

def test_file_hashing():
    print("Testing file hashing...")
    
    # Create test file
    test_content = "This is a test file for hash function testing."
    test_filename = "hash_test_file.txt"
    
    with open(test_filename, 'w') as f:
        f.write(test_content)
    
    try:
        # Test SHA-256 file hashing
        sha256_result = sha256_file(test_filename)
        sha256_direct = sha256_hash(test_content.encode('utf-8'))
        
        if sha256_result == sha256_direct:
            print("   SHA-256 file hashing works correctly")
        else:
            print("   SHA-256 file hashing failed")
            return False
        
        # Test SHA3-256 file hashing
        sha3_result = sha3_256_file(test_filename)
        sha3_direct = sha3_256_hash(test_content.encode('utf-8'))
        
        if sha3_result == sha3_direct:
            print("   SHA3-256 file hashing works correctly")
        else:
            print("   SHA3-256 file hashing failed")
            return False
            
    finally:
        # Cleanup
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    return True

def test_large_file_hashing():
    print("Testing large file hashing...")
    
    # Create a moderately large file (1MB)
    large_filename = "large_test_file.bin"
    file_size = 1024 * 1024  # 1MB
    
    try:
        # Generate random data
        import random
        with open(large_filename, 'wb') as f:
            for _ in range(file_size // 1024):
                f.write(bytes(random.getrandbits(8) for _ in range(1024)))
        
        # Hash with different chunk sizes
        chunk_sizes = [1024, 4096, 8192]
        results = {}
        
        for chunk_size in chunk_sizes:
            sha256_result = sha256_file(large_filename, chunk_size)
            sha3_result = sha3_256_file(large_filename, chunk_size)
            results[chunk_size] = (sha256_result, sha3_result)
        
        # All chunk sizes should produce same results
        first_sha256 = results[chunk_sizes[0]][0]
        first_sha3 = results[chunk_sizes[0]][1]
        
        for chunk_size, (sha256, sha3) in results.items():
            if sha256 != first_sha256 or sha3 != first_sha3:
                print(f"   Inconsistent results with chunk size {chunk_size}")
                return False
        
        print(f"   Large file hashing consistent across chunk sizes: {chunk_sizes}")
        
    except Exception as e:
        print(f"   Large file test failed: {e}")
        return False
        
    finally:
        # Cleanup
        if os.path.exists(large_filename):
            os.remove(large_filename)
    
    return True

def test_interoperability():
    print("Testing interoperability...")
    
    # Create test file
    test_content = "Interoperability test data"
    test_filename = "interop_test.txt"
    
    with open(test_filename, 'w') as f:
        f.write(test_content)
    
    try:
        # Compute hashes with our implementation
        our_sha256 = sha256_file(test_filename)
        our_sha3 = sha3_256_file(test_filename)
        
        print(f"  Our SHA-256:    {our_sha256}")
        print(f"  Our SHA3-256:   {our_sha3}")
        print("  Note: Compare with system commands:")
        print(f"    sha256sum {test_filename}")
        print(f"    sha3sum -a 256 {test_filename}")
        print("   Interoperability test completed - manually verify with system tools")
        
    finally:
        # Cleanup
        if os.path.exists(test_filename):
            os.remove(test_filename)
    
    return True

if __name__ == "__main__":
    print("🔬 Hash Functions Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    try:
        all_passed &= test_sha256_known_answers()
        print()
        
        all_passed &= test_sha3_256_known_answers()
        print()
        
        all_passed &= test_avalanche_effect()
        print()
        
        all_passed &= test_file_hashing()
        print()
        
        all_passed &= test_large_file_hashing()
        print()
        
        all_passed &= test_interoperability()
        print()
        
        if all_passed:
            print(" All hash function tests passed!")
        else:
            print(" Some tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f" Test suite failed with exception: {e}")
        sys.exit(1)