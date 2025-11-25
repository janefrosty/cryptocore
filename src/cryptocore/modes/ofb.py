from Crypto.Cipher import AES

def aes_ofb_encrypt(key, data, iv):
    """
    Encrypt data using AES-OFB mode
    """
    return _aes_ofb_process(key, data, iv)

def aes_ofb_decrypt(key, data, iv):
    """
    Decrypt data using AES-OFB mode (same as encryption)
    """
    return _aes_ofb_process(key, data, iv)

def _aes_ofb_process(key, data, iv):
    """
    Common processing function for OFB encryption and decryption
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    output_blocks = []
    keystream_block = iv
    
    for block in blocks:
        # Generate next keystream block
        keystream_block = cipher.encrypt(keystream_block)
        # XOR plaintext/ciphertext with keystream
        output_block = bytes(a ^ b for a, b in zip(block, keystream_block))
        output_blocks.append(output_block)
    
    return b''.join(output_blocks)