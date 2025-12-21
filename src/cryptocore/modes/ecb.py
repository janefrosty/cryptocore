from Crypto.Cipher import AES

BLOCK_SIZE = 16

def pkcs7_pad(data):
    """
    Sprint 1: PKCS#7 padding
    Appends bytes where each byte equals padding length
    """
    if len(data) % BLOCK_SIZE == 0:
        return data + bytes([BLOCK_SIZE] * BLOCK_SIZE)
    
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    """
    Sprint 1: PKCS#7 unpadding
    Removes padding bytes and validates padding
    """
    if len(data) == 0:
        raise ValueError("Cannot unpad empty data")
    
    pad_len = data[-1]
    
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    
    if not all(byte == pad_len for byte in data[-pad_len:]):
        raise ValueError("Invalid padding bytes")
    
    return data[:-pad_len]

def aes_ecb_encrypt(key, plaintext):
    """
    Sprint 1: AES-ECB encryption
    Electronic Codebook mode - each block encrypted independently
    """
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pkcs7_pad(plaintext)
    
    if len(padded) % BLOCK_SIZE != 0:
        raise ValueError("Padded data must be aligned to block boundary")
    
    blocks = [padded[i:i+BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
    encrypted = b''.join(cipher.encrypt(b) for b in blocks)
    return encrypted

def aes_ecb_decrypt(key, ciphertext):
    """
    Sprint 1: AES-ECB decryption
    Reverse of encryption with padding removal
    """
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Data must be aligned to block boundary in ECB mode")
    
    cipher = AES.new(key, AES.MODE_ECB)
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    decrypted = b''.join(cipher.decrypt(b) for b in blocks)
    return pkcs7_unpad(decrypted)