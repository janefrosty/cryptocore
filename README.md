
## Sprint4

- **Hash Functions**: SHA-256 and SHA3-256 implementations
- **File Integrity**: Verify data integrity with cryptographic hashes
- **New CLI Structure**: Subcommands for different operations
- **Interoperable**: Compatible with standard system hash tools

## Что было реализовано в Sprint 4
Новые хэш-функции
- SHA-256 - реализация с нуля по NIST FIPS 180-4
- SHA3-256 - реализация с нуля using Keccak sponge construction
- Поддержка файлов любого размера с chunk processing

## Новая структура CLI
Подкоманды: enc (шифрование) и dgst (хэширование)
Обратная совместимость с предыдущими версиями
Улучшенная система помощи

## Расширенное тестирование
Known-answer tests с NIST векторами
Avalanche effect testing
Interoperability tests с системными утилитами
Large file handling tests

## Хэширование 
```powershell
# Базовое хэширование
cryptocore dgst --algorithm sha256 --input file.txt
cryptocore dgst --algorithm sha3-256 --input file.pdf

# Хэширование с сохранением в файл
cryptocore dgst --algorithm sha256 --input document.pdf --output hash.txt

# Хэширование пустого файла
echo -n "" > empty.txt
cryptocore dgst --algorithm sha256 --input empty.txt
```
## Шифрование (обратная совместимость)
```powershell
# Автоматическая генерация ключа
cryptocore enc --algorithm aes --mode cbc --encrypt --input plaintext.txt --output ciphertext.bin

# С явным ключом
cryptocore enc --algorithm aes --mode ctr --encrypt --key 00112233445566778899aabbccddeeff --input file.txt --output file.enc
```

## Дешифровка
```powershell
cryptocore enc --algorithm aes --mode cbc --decrypt --key [KEY] --input ciphertext.bin --output decrypted.txt
Помощь и информация
```
## Структура

.../src/cryptocore/
├── hash/                   # NEW - Папка хэш-функций

│   ├── __init__.py        # NEW - Инициализация

│   ├── sha256.py          # NEW - SHA-256 с нуля

│   └── sha3_256.py        # NEW - SHA3-256 с нуля

├── cli_parser.py          # UPD - Поддержка подкоманд

├── main.py                # UPD - Обработка хэшей

└── ...

tests/

├── test_hash_functions.py     # NEW - Тесты хэшей

└── test_sprint4_cli.ps1      # NEW - CLI тесты

## Тестирование 
```powershell
python tests/test_hash_functions.py
.\tests\test_sprint4_cli.ps1
.\tests\roundtrip_test.ps1
```
