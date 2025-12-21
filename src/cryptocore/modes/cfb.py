from Crypto.Cipher import AES

def aes_cfb_encrypt(key, data, iv):
    """
    Sprint 2: AES-CFB encryption
    Cipher Feedback mode - stream cipher using block cipher
    Full block segment size (128-bit)
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    ciphertext_blocks = []
    feedback = iv
    
    for block in blocks:
        encrypted_feedback = cipher.encrypt(feedback)
        ciphertext_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        ciphertext_blocks.append(ciphertext_block)
        feedback = ciphertext_block
    
    return b''.join(ciphertext_blocks)

def aes_cfb_decrypt(key, data, iv):
    """
    Sprint 2: AES-CFB decryption
    Same structure as encryption for stream cipher property
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    plaintext_blocks = []
    feedback = iv
    
    for block in blocks:
        encrypted_feedback = cipher.encrypt(feedback)
        plaintext_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        plaintext_blocks.append(plaintext_block)
        feedback = block
    
    return b''.join(plaintext_blocks)