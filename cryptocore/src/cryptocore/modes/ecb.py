from Crypto.Cipher import AES

BLOCK = 16

def pkcs7_pad(data):
    pad_len = BLOCK - (len(data) % BLOCK)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK:
        raise ValueError("Invalid padding")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def aes_ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pkcs7_pad(plaintext)
    blocks = [padded[i:i+BLOCK] for i in range(0, len(padded), BLOCK)]
    encrypted = b''.join(cipher.encrypt(b) for b in blocks)
    return encrypted

def aes_ecb_decrypt(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    blocks = [ciphertext[i:i+BLOCK] for i in range(0, len(ciphertext), BLOCK)]
    decrypted = b''.join(cipher.decrypt(b) for b in blocks)
    return pkcs7_unpad(decrypted)
