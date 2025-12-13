# Sprint 5: Коды аутентификации сообщений
- Реализация HMAC-SHA256 в соответствии с RFC 2104
- Проверка HMAC с флагом --verify
- Обнаружение подделки файлов и ключей
- Поддержка ключей переменной длины

## HMAC 
```bash
# Generate HMAC
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input message.txt

# Generate HMAC with output file
cryptocore dgst --algorithm sha256 --hmac --key [KEY] --input file.txt --output hmac.txt

# Verify HMAC
cryptocore dgst --algorithm sha256 --hmac --key [KEY] --input file.txt --verify expected_hmac.txt
```

## Key Size Variations for HMAC
```bash
# Short key (16 bytes)
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input file.txt

# Block size key (64 bytes)
cryptocore dgst --algorithm sha256 --hmac --key $(printf '%0.s00' {1..64}) --input file.txt

# Long key (100+ bytes)
cryptocore dgst --algorithm sha256 --hmac --key $(printf '%0.s00' {1..100}) --input file.txt
```

# Testing
```bash
# Run HMAC tests
python tests/test_hmac.py

# Run CLI tests
.\tests\test_sprint5_cli.ps1

# Run all hash tests
python tests/test_hash_functions.py
.\tests\roundtrip_test.ps1
```
