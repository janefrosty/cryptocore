# Sprint 6: Аутентифицированное шифрование
- Реализация GCM (режим Галуа/счетчика) с нуля
- AEAD (аутентифицированное шифрование с ассоциированными данными)
- Поддержка AAD (ассоциированные аутентифицированные данные)
- Катастрофический сбой при ошибках аутентификации
- Парадигма «шифрование с последующим MAC-проверкой

## GCM Authenticated Encryption 
bash
# GCM encryption with AAD
cryptocore enc --algorithm aes --mode gcm --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin --aad aabbccddeeff

# GCM decryption with correct AAD
cryptocore enc --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --input ciphertext.bin --output decrypted.txt --aad aabbccddeeff

# GCM decryption with wrong AAD (will fail catastrophically)
cryptocore enc --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --input ciphertext.bin --output decrypted.txt --aad wrongaad123
GCM with Empty AAD
bash
# Encryption without AAD
cryptocore enc --algorithm aes --mode gcm --encrypt --key [KEY] --input file.txt --output file.enc

# Decryption without AAD
cryptocore enc --algorithm aes --mode gcm --decrypt --key [KEY] --input file.enc --output file.txt
