#!/usr/bin/env python3
"""
HMAC Test Suite
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from cryptocore.mac.hmac import HMAC
from cryptocore.hash.sha256 import SHA256

def test_rfc_4231():
    print("Testing HMAC with RFC 4231 test vectors...")
    
    test_cases = [
        {
            'name': 'Test Case 1',
            'key': '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b',
            'data': '4869205468657265',
            'expected': 'b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7'
        },
        {
            'name': 'Test Case 2',
            'key': '4a656665',
            'data': '7768617420646f2079612077616e7420666f72206e6f7468696e673f',
            'expected': '5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843'
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        key = bytes.fromhex(test['key'])
        data = bytes.fromhex(test['data'])
        
        # Исправлено: передаем hash_class
        hmac = HMAC(key, SHA256)
        result = hmac.compute(data)
        
        if result == test['expected']:
            print(f"  PASS {test['name']}")
        else:
            print(f"  FAIL {test['name']}")
            print(f"    Expected: {test['expected']}")
            print(f"    Got: {result}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("HMAC Test Suite")
    print("=" * 60)
    
    try:
        if test_rfc_4231():
            print("HMAC tests passed!")
            sys.exit(0)
        else:
            print("HMAC tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Test suite failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)