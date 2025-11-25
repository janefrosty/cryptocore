from Crypto.Cipher import AES

def aes_ctr_encrypt(key, data, iv):
    return _aes_ctr_process(key, data, iv)

def aes_ctr_decrypt(key, data, iv):
    return _aes_ctr_process(key, data, iv)

def _aes_ctr_process(key, data, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    output = bytearray()
    
    for i in range(0, len(data), 16):
        # Increment IV for each block
        counter = (int.from_bytes(iv, 'big') + (i // 16)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        counter_block = counter.to_bytes(16, 'big')
        
        keystream = cipher.encrypt(counter_block)
        block = data[i:i+16]
        
        # XOR the block with keystream
        encrypted_block = bytes(b ^ k for b, k in zip(block, keystream))
        output.extend(encrypted_block)
    
    return bytes(output)