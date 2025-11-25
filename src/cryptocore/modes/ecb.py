from Crypto.Cipher import AES

BLOCK_SIZE = 16

def pkcs7_pad(data):
    """PKCS#7 padding - SPRINT 1 (unchanged)"""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    """PKCS#7 unpadding - SPRINT 1 (unchanged)"""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def aes_ecb_encrypt(key, plaintext):
    """AES-ECB encryption - SPRINT 1 (unchanged)"""
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pkcs7_pad(plaintext)
    blocks = [padded[i:i+BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
    encrypted = b''.join(cipher.encrypt(b) for b in blocks)
    return encrypted

def aes_ecb_decrypt(key, ciphertext):
    """AES-ECB decryption - SPRINT 1 (unchanged)"""
    cipher = AES.new(key, AES.MODE_ECB)
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    decrypted = b''.join(cipher.decrypt(b) for b in blocks)
    return pkcs7_unpad(decrypted)