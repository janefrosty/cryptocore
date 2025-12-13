# Sprint 6: Аутентифицированное шифрование
- Реализация GCM (режим Галуа/счетчика) с нуля
- AEAD (аутентифицированное шифрование с ассоциированными данными)
- Поддержка AAD (ассоциированные аутентифицированные данные)
- Катастрофический сбой при ошибках аутентификации
- Парадигма «шифрование с последующим MAC-проверкой

## GCM Authenticated Encryption 
```bash
# GCM encryption with AAD
cryptocore enc --algorithm aes --mode gcm --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin --aad aabbccddeeff

# GCM decryption with correct AAD
cryptocore enc --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --input ciphertext.bin --output decrypted.txt --aad aabbccddeeff

# GCM decryption with wrong AAD (will fail catastrophically)
cryptocore enc --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --input ciphertext.bin --output decrypted.txt --aad wrongaad123
```
## GCM with Empty AAD
```bash
# Encryption without AAD
cryptocore enc --algorithm aes --mode gcm --encrypt --key [KEY] --input file.txt --output file.enc

# Decryption without AAD
cryptocore enc --algorithm aes --mode gcm --decrypt --key [KEY] --input file.enc --output file.txt
```
GCM
- Соответствие NIST SP 800-38D: Реализует стандартную спецификацию GCM
- Аутентифицированное шифрование: Обеспечивает как конфиденциальность, так и целостность
- Поддержка AAD: Аутентифицирует связанные данные без их шифрования
- Катастрофический сбой: Отсутствие вывода открытого текста при сбое аутентификации
- Умножение в поле Галуа: GF(2^128) с неприводимым многочленом x^128 + x^7 + x^2 + x + 1
- Управление одноразовыми числами: Генерация 12-байтовых случайных одноразовых чисел с гарантией уникальности

Ключевые особенности
1. Конфиденциальность: Шифрование на основе AES-CTR
2. Целостность: Аутентификация GHASH
3. Аутентификация: 16-байтовый тег аутентификации
4. Связанные данные: Поддержка аутентифицированных незашифрованных данных
5. Обнаружение несанкционированного доступа: Обнаруживает изменения зашифрованного текста, AAD и ключа

## Testing
```bash
# Run GCM tests
python tests/test_gcm.py

# Run CLI tests
.\tests\test_sprint6_cli.ps1

# Run HMAC tests
python tests/test_hmac.py

# Run hash tests
python tests/test_hash_functions.py

# Run all encryption tests
.\tests\roundtrip_test.ps1
```
