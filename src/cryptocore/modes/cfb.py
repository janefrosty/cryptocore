from Crypto.Cipher import AES

def aes_cfb_encrypt(key, data, iv):
    """
    Encrypt data using AES-CFB mode (full block segment size)
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    ciphertext_blocks = []
    feedback = iv
    
    for block in blocks:
        # Encrypt the feedback register
        encrypted_feedback = cipher.encrypt(feedback)
        # XOR with plaintext to produce ciphertext
        ciphertext_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        ciphertext_blocks.append(ciphertext_block)
        # Update feedback register with ciphertext
        feedback = ciphertext_block
    
    return b''.join(ciphertext_blocks)

def aes_cfb_decrypt(key, data, iv):
    """
    Decrypt data using AES-CFB mode (full block segment size)
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    plaintext_blocks = []
    feedback = iv
    
    for block in blocks:
        # Encrypt the feedback register
        encrypted_feedback = cipher.encrypt(feedback)
        # XOR with ciphertext to produce plaintext
        plaintext_block = bytes(a ^ b for a, b in zip(block, encrypted_feedback))
        plaintext_blocks.append(plaintext_block)
        # Update feedback register with ciphertext
        feedback = block
    
    return b''.join(plaintext_blocks)