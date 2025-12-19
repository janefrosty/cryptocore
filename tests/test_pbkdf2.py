import unittest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cryptocore.kdf.pbkdf2 import pbkdf2_hmac_sha256
from cryptocore.kdf.hkdf import derive_key

class TestPBKDF2(unittest.TestCase):
    """Test PBKDF2-HMAC-SHA256 implementation."""
    
    def test_rfc_6070_vectors(self):
        """Test with RFC 6070 test vectors."""
        test_cases = [
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 1,
                'dklen': 20,
                'expected': '0c60c80f961f0e71f3a9b524af6012062fe037a6'
            },
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 2,
                'dklen': 20,
                'expected': 'ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957'
            },
            {
                'password': b'password',
                'salt': b'salt',
                'iterations': 4096,
                'dklen': 20,
                'expected': '4b007901b765489abead49d926f721d065a429c1'
            },
        ]
        
        for i, test in enumerate(test_cases):
            with self.subTest(f"RFC 6070 test case {i+1}"):
                result = pbkdf2_hmac_sha256(
                    test['password'],
                    test['salt'],
                    test['iterations'],
                    test['dklen']
                )
                expected = bytes.fromhex(test['expected'])
                self.assertEqual(result, expected)
    
    def test_variable_length(self):
        """Test deriving keys of different lengths."""
        password = b'test'
        salt = b'salt'
        iterations = 1000
        
        for length in [1, 16, 32, 64, 100]:
            with self.subTest(f"Length {length}"):
                key = pbkdf2_hmac_sha256(password, salt, iterations, length)
                self.assertEqual(len(key), length)
    
    def test_deterministic(self):
        """Test that same inputs produce same output."""
        password = b'my_password'
        salt = b'my_salt'
        iterations = 50000
        dklen = 32
        
        key1 = pbkdf2_hmac_sha256(password, salt, iterations, dklen)
        key2 = pbkdf2_hmac_sha256(password, salt, iterations, dklen)
        
        self.assertEqual(key1, key2)


class TestKeyHierarchy(unittest.TestCase):
    """Test key hierarchy function."""
    
    def test_deterministic(self):
        """Test deterministic output."""
        master_key = b'0' * 32
        context = 'encryption'
        
        key1 = derive_key(master_key, context, 32)
        key2 = derive_key(master_key, context, 32)
        
        self.assertEqual(key1, key2)
    
    def test_context_separation(self):
        """Test different contexts produce different keys."""
        master_key = b'1' * 32
        
        key1 = derive_key(master_key, 'encryption', 32)
        key2 = derive_key(master_key, 'authentication', 32)
        key3 = derive_key(master_key, 'mac', 32)
        
        self.assertNotEqual(key1, key2)
        self.assertNotEqual(key1, key3)
        self.assertNotEqual(key2, key3)
    
    def test_variable_length(self):
        """Test deriving keys of different lengths."""
        master_key = b'2' * 32
        context = 'test'
        
        for length in [1, 16, 24, 32, 48, 64]:
            with self.subTest(f"Length {length}"):
                key = derive_key(master_key, context, length)
                self.assertEqual(len(key), length)


if __name__ == '__main__':
    unittest.main()