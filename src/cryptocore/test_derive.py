import sys
sys.path.insert(0, 'src')

from cryptocore.kdf.pbkdf2 import pbkdf2_hmac_sha256

# Простой тест
password = "test"
salt = "1234"
iterations = 100
length = 16

result = pbkdf2_hmac_sha256(password, salt, iterations, length)
print(f"Key: {result.hex()}")
print(f"Length: {len(result)} bytes")