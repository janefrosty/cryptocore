

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.mac.hmac import HMAC, hmac_sha256

def test_rfc_4231():
    """
    Test HMAC with RFC 4231 test vectors
    Test cases 1-4 from Section 4.2
    """
    print("Testing HMAC with RFC 4231 test vectors...")
    
    test_cases = [
        {
            'name': 'Test Case 1',
            'key': '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b',  # 20 bytes of 0x0b
            'data': '4869205468657265',  # "Hi There"
            'expected': 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'
        },
        {
            'name': 'Test Case 2',
            'key': '4a656665',  # "Jefe"
            'data': '7768617420646f2079612077616e7420666f72206e6f7468696e673f',  # "what do ya want for nothing?"
            'expected': '5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843'
        },
        {
            'name': 'Test Case 3',
            'key': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',  # 20 bytes of 0xaa
            'data': 'dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',  # 50 bytes of 0xdd
            'expected': '773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe'
        },
        {
            'name': 'Test Case 4',
            'key': '0102030405060708090a0b0c0d0e0f10111213141516171819',  # 25 bytes
            'data': 'cdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcdcd',  # 50 bytes of 0xcd
            'expected': '82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b'
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        key = bytes.fromhex(test['key'])
        data = bytes.fromhex(test['data'])
        
        hmac = HMAC(key)
        result = hmac.compute(data)
        
        if result == test['expected']:
            print(f"   {test['name']} passed")
        else:
            print(f"   {test['name']} failed")
            print(f"     Expected: {test['expected']}")
            print(f"     Got:      {result}")
            all_passed = False
    
    return all_passed

def test_key_size_variations():
    """
    Test HMAC with various key sizes
    Keys shorter than, equal to, and longer than block size
    """
    print("Testing HMAC with various key sizes...")
    
    test_data = b"Test data for HMAC key size testing"
    
    key_variations = [
        ("Short key (16 bytes)", bytes.fromhex("00112233445566778899aabbccddeeff")),
        ("Block size key (64 bytes)", bytes.fromhex("00" * 64)),
        ("Long key (100 bytes)", bytes.fromhex("00" * 100)),
    ]
    
    all_passed = True
    
    for name, key in key_variations:
        try:
            hmac = HMAC(key)
            result = hmac.compute(test_data)
            
            # Basic validation: result should be 64 hex chars (32 bytes)
            if len(result) == 64:
                print(f"   {name} - Valid HMAC produced")
            else:
                print(f"   {name} - Invalid HMAC length: {len(result)}")
                all_passed = False
                
        except Exception as e:
            print(f"   {name} - Error: {e}")
            all_passed = False
    
    return all_passed

def test_tamper_detection():
    """
    Test that HMAC detects file modifications
    Changing one byte should produce different HMAC
    """
    print("Testing tamper detection...")
    
    test_content = b"Original message for tamper detection test"
    modified_content = b"Modified message for tamper detection test"  # Changed 'Original' to 'Modified'
    
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    
    # Compute HMAC for original
    hmac = HMAC(key)
    original_hmac = hmac.compute(test_content)
    
    # Compute HMAC for modified
    hmac = HMAC(key)
    modified_hmac = hmac.compute(modified_content)
    
    if original_hmac != modified_hmac:
        print(f"   Tamper detection works")
        print(f"     Original HMAC: {original_hmac[:16]}...")
        print(f"     Modified HMAC: {modified_hmac[:16]}...")
        return True
    else:
        print(f"   Tamper detection failed - HMACs are identical")
        return False

def test_key_detection():
    """
    Test that HMAC detects wrong keys
    Same data with different keys should produce different HMACs
    """
    print("Testing key detection...")
    
    test_data = b"Test data for key detection"
    key1 = bytes.fromhex("00112233445566778899aabbccddeeff")
    key2 = bytes.fromhex("ffeeeeddddccccbbbbaaaa999988887777")
    
    hmac1 = HMAC(key1)
    hmac1_result = hmac1.compute(test_data)
    
    hmac2 = HMAC(key2)
    hmac2_result = hmac2.compute(test_data)
    
    if hmac1_result != hmac2_result:
        print(f"   Key detection works")
        print(f"     Key1 HMAC: {hmac1_result[:16]}...")
        print(f"     Key2 HMAC: {hmac2_result[:16]}...")
        return True
    else:
        print(f"   Key detection failed - HMACs are identical")
        return False

def test_empty_file():
    """
    Test HMAC with empty files
    """
    print("Testing HMAC with empty file...")
    
    empty_filename = "empty_test_file.bin"
    
    try:
        # Create empty file
        with open(empty_filename, 'wb') as f:
            pass
        
        key = bytes.fromhex("00112233445566778899aabbccddeeff")
        
        # Manual computation for comparison
        hmac = HMAC(key)
        manual_hmac = hmac.compute(b"")
        
        # File computation
        hmac = HMAC(key)
        file_hmac = hmac.compute_file(empty_filename)
        
        if manual_hmac == file_hmac:
            print(f"   Empty file HMAC works")
            print(f"     HMAC: {manual_hmac}")
            return True
        else:
            print(f"   Empty file HMAC mismatch")
            return False
            
    finally:
        if os.path.exists(empty_filename):
            os.remove(empty_filename)

def test_large_file():
    """
    Test HMAC with large files using chunk processing
    """
    print("Testing HMAC with large file...")
    
    large_filename = "large_hmac_test.bin"
    file_size = 1024 * 1024  # 1MB
    
    try:
        # Create large file with predictable content
        with open(large_filename, 'wb') as f:
            for i in range(file_size // 1024):
                f.write(bytes([i % 256] * 1024))
        
        key = bytes.fromhex("00112233445566778899aabbccddeeff")
        
        # Test with different chunk sizes
        chunk_sizes = [1024, 4096, 8192]
        results = []
        
        for chunk_size in chunk_sizes:
            hmac = HMAC(key)
            result = hmac.compute_file(large_filename, chunk_size)
            results.append((chunk_size, result))
        
        # All should produce same result
        first_result = results[0][1]
        consistent = all(result == first_result for _, result in results)
        
        if consistent:
            print(f"   Large file HMAC consistent across chunk sizes")
            print(f"     HMAC: {first_result[:16]}...")
            return True
        else:
            print(f"   Large file HMAC inconsistent")
            for chunk_size, result in results:
                print(f"     Chunk {chunk_size}: {result[:16]}...")
            return False
            
    except Exception as e:
        print(f"   Large file test failed: {e}")
        return False
        
    finally:
        if os.path.exists(large_filename):
            os.remove(large_filename)

if __name__ == "__main__":
    print("Sprint 5: HMAC Test Suite")
    
    all_passed = True
    
    try:
        all_passed &= test_rfc_4231()
        print()
        
        all_passed &= test_key_size_variations()
        print()
        
        all_passed &= test_tamper_detection()
        print()
        
        all_passed &= test_key_detection()
        print()
        
        all_passed &= test_empty_file()
        print()
        
        all_passed &= test_large_file()
        print()
        
        if all_passed:
            print("🎉 All HMAC tests passed!")
        else:
            print(" Some HMAC tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f" Test suite failed with exception: {e}")
        sys.exit(1)