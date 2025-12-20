
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_pbkdf2():
    """Simple PBKDF2 test."""
    print("Testing PBKDF2...")
    
    try:
        from cryptocore.kdf.pbkdf2 import pbkdf2_hmac_sha256
        
        # Simple test case
        password = "password"
        salt = b"salt"
        iterations = 1
        dklen = 20
        
        result = pbkdf2_hmac_sha256(password, salt, iterations, dklen)
        
        if result and len(result) == dklen:
            print(f"  ✓ PBKDF2 works: {result.hex()[:16]}...")
            return True
        else:
            print(f"  ✗ PBKDF2 failed")
            return False
            
    except Exception as e:
        print(f"  ✗ PBKDF2 error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PBKDF2 TEST")
    print("=" * 60)
    
    success = test_pbkdf2()
    
    print("=" * 60)
    if success:
        print("✅ PBKDF2 TEST PASSED!")
        sys.exit(0)
    else:
        print("❌ PBKDF2 TEST FAILED!")
        sys.exit(1)