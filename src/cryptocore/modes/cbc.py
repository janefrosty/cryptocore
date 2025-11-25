from Crypto.Cipher import AES
from .ecb import pkcs7_pad, pkcs7_unpad

def aes_cbc_encrypt(key, data, iv):
    """Simplified CBC encryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pkcs7_pad(data)
    
    ciphertext = b''
    prev_block = iv
    
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        # XOR with previous block
        xored = bytes(a ^ b for a, b in zip(block, prev_block))
        # Encrypt
        encrypted = cipher.encrypt(xored)
        ciphertext += encrypted
        prev_block = encrypted
    
    return ciphertext

def aes_cbc_decrypt(key, data, iv):
    """Simplified CBC decryption"""
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Check alignment
    if len(data) % 16 != 0:
        raise ValueError(f"Ciphertext length {len(data)} is not multiple of 16")
    
    plaintext = b''
    prev_block = iv
    
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        # Decrypt
        decrypted = cipher.decrypt(block)
        # XOR with previous ciphertext block
        plain = bytes(a ^ b for a, b in zip(decrypted, prev_block))
        plaintext += plain
        prev_block = block
    
    return pkcs7_unpad(plaintext)