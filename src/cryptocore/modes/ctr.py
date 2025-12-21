from Crypto.Cipher import AES

def aes_ctr_encrypt(key, data, iv):
    """
    Sprint 2: AES-CTR encryption
    Counter mode - stream cipher using counter
    """
    return _aes_ctr_process(key, data, iv)

def aes_ctr_decrypt(key, data, iv):
    """
    Sprint 2: AES-CTR decryption  
    Same as encryption for stream cipher property
    """
    return _aes_ctr_process(key, data, iv)

def _aes_ctr_process(key, data, iv):
    """
    Common processing for CTR encryption and decryption
    Counter incremented for each block
    """
    cipher = AES.new(key, AES.MODE_ECB)
    
    blocks = []
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        
        counter = int.from_bytes(iv, 'big') + (i // 16)
        counter_block = counter.to_bytes(16, 'big')
        
        keystream = cipher.encrypt(counter_block)
        
        output_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
        blocks.append(output_block)
    
    return b''.join(blocks)