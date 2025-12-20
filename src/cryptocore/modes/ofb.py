from Crypto.Cipher import AES

def aes_ofb_encrypt(key, data, iv):
    """
    Sprint 2: AES-OFB encryption
    Output Feedback mode - stream cipher with keystream independent of plaintext
    """
    return _aes_ofb_process(key, data, iv)

def aes_ofb_decrypt(key, data, iv):
    """
    Sprint 2: AES-OFB decryption
    Same as encryption for stream cipher property
    """
    return _aes_ofb_process(key, data, iv)

def _aes_ofb_process(key, data, iv):
    """
    Common processing for OFB encryption and decryption
    Keystream generated from encrypted feedback
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    output_blocks = []
    keystream_block = iv
    
    for block in blocks:
        keystream_block = cipher.encrypt(keystream_block)
        output_block = bytes(a ^ b for a, b in zip(block, keystream_block))
        output_blocks.append(output_block)
    
    return b''.join(output_blocks)