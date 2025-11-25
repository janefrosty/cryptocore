
## SPRINT 2 

- **New Modes**: CBC, CFB, OFB, CTR
- **IV Handling**: Secure random generation for encryption, flexible input for decryption
- **Interoperability**: Full compatibility with OpenSSL
- **Backward Compatibility**: All Sprint 1 features preserved

## Установка зависимостей

```PowerShell
pip install -r requirements.txt
pip install -e .
```
## Проверка всех режимов
```PowerShell

# CBC
cryptocore --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input original.txt --output encrypted.bin
cryptocore --algorithm aes --mode cbc --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt

# CFB
cryptocore --algorithm aes --mode cfb --encrypt --key 00112233445566778899aabbccddeeff --input original.txt --output encrypted.bin
cryptocore --algorithm aes --mode cfb --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt

# CTR
cryptocore --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input original.txt --output encrypted.bin
cryptocore --algorithm aes --mode ctr --decrypt --key 00112233445566778899aabbccddeeff --input encrypted.bin --output decrypted.txt
```
## Тесты
```PowerShell
# Round-trip тесты
.\tests\roundtrip_test.ps1

# OpenSSL интероперабельность
.\tests\openssl_interop_test.ps1
```

