from Crypto.Cipher import AES

BLOCK_SIZE = 16

def pkcs7_pad(data):
    if len(data) % BLOCK_SIZE == 0:
        # Если данные уже выровнены, добавляем целый блок padding
        return data + bytes([BLOCK_SIZE] * BLOCK_SIZE)
    
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    if len(data) == 0:
        raise ValueError("Cannot unpad empty data")
    
    pad_len = data[-1]
    
    # Проверяем валидность padding
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Invalid padding length")
    
    # Проверяем что все байты padding одинаковы
    if not all(byte == pad_len for byte in data[-pad_len:]):
        raise ValueError("Invalid padding bytes")
    
    return data[:-pad_len]

def aes_ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pkcs7_pad(plaintext)
    
    # Проверяем выравнивание
    if len(padded) % BLOCK_SIZE != 0:
        raise ValueError("Padded data must be aligned to block boundary")
    
    blocks = [padded[i:i+BLOCK_SIZE] for i in range(0, len(padded), BLOCK_SIZE)]
    encrypted = b''.join(cipher.encrypt(b) for b in blocks)
    return encrypted

def aes_ecb_decrypt(key, ciphertext):
    # Проверяем что шифртекст выровнен
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Data must be aligned to block boundary in ECB mode")
    
    cipher = AES.new(key, AES.MODE_ECB)
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    decrypted = b''.join(cipher.decrypt(b) for b in blocks)
    return pkcs7_unpad(decrypted)