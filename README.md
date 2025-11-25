
## Sprint3

- **Automatic Key Generation**: Secure random key generation when `--key` is omitted
- **CSPRNG Module**: Cryptographically secure random number generator using OS RNG
- **Weak Key Detection**: Warning for potentially weak user-provided keys
- **NIST Test Suite**: Support for statistical randomness testing

## Базовое тестирование автоматической генерации ключей
```bash
# Тестирование всех режимов с авто-генерацией ключей
cryptocore --algorithm aes --mode ecb --encrypt --input original.txt --output test_ecb.bin
cryptocore --algorithm aes --mode cbc --encrypt --input original.txt --output test_cbc.bin  
cryptocore --algorithm aes --mode cfb --encrypt --input original.txt --output test_cfb.bin
cryptocore --algorithm aes --mode ofb --encrypt --input original.txt --output test_ofb.bin
cryptocore --algorithm aes --mode ctr --encrypt --input original.txt --output test_ctr.bin
```
## Тестирование обратной совместимости с ручными ключами
```bash
# Шифрование с явным ключом
cryptocore --algorithm aes --mode cbc --encrypt --key 00112233445566778899aabbccddeeff --input original.txt --output manual_enc.bin

# Расшифровка с тем же ключом
cryptocore --algorithm aes --mode cbc --decrypt --key 00112233445566778899aabbccddeeff --input manual_enc.bin --output manual_dec.txt
```
## Тестирование обнаружения слабых ключей
```bash
# Тест слабых ключей (должны быть предупреждения)
cryptocore --algorithm aes --mode cbc --encrypt --key 00000000000000000000000000000000 --input original.txt --output weak1.bin
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input original.txt --output weak2.bin
cryptocore --algorithm aes --mode cbc --encrypt --key 01010101010101010101010101010101 --input original.txt --output weak3.bin
```
## Тестирование обязательности ключа для дешифровки
```bash
# Должна быть ошибка - ключ обязателен для дешифровки
cryptocore --algorithm aes --mode cbc --decrypt --input test_cbc.bin --output should_fail.txt
```
## Запуск всех тестов
```bash
.\tests\sprint3_test.ps1
.\tests\test_csprng_comprehensive.ps1  
.\tests\integration_test.ps1
```


