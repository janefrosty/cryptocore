from Crypto.Cipher import AES
from .ecb import pkcs7_pad, pkcs7_unpad

def aes_cbc_encrypt(key, data, iv):
    """
    Encrypt data using AES-CBC mode
    """
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pkcs7_pad(data)
    
    blocks = [padded_data[i:i+16] for i in range(0, len(padded_data), 16)]
    ciphertext_blocks = []
    previous_block = iv
    
    for block in blocks:
        # XOR with previous ciphertext block (or IV for first block)
        xored_block = bytes(a ^ b for a, b in zip(block, previous_block))
        # Encrypt the result
        encrypted_block = cipher.encrypt(xored_block)
        ciphertext_blocks.append(encrypted_block)
        previous_block = encrypted_block
    
    return b''.join(ciphertext_blocks)

def aes_cbc_decrypt(key, data, iv):
    """
    Decrypt data using AES-CBC mode
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    plaintext_blocks = []
    previous_block = iv
    
    for block in blocks:
        # Decrypt the block
        decrypted_block = cipher.decrypt(block)
        # XOR with previous ciphertext block (or IV for first block)
        plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
        plaintext_blocks.append(plaintext_block)
        previous_block = block
    
    padded_plaintext = b''.join(plaintext_blocks)
    return pkcs7_unpad(padded_plaintext)