
Разработка крипто провайдера, имплементирующего блочный шифр
# CryptoCore – AES-128 ECB Encryption Tool

CryptoCore — это командный инструмент для шифрования и расшифрования файлов с использованием **AES-128** в режиме **ECB**.  
Проект создан в рамках Sprint 1 и включает полную реализацию:

- AES-128 в режиме ECB  
- PKCS#7 padding  
- Корректную работу с бинарными файлами  
- CLI-парсер аргументов  
- Структурированный и расширяемый код  

---

## Возможности

- Шифрование файлов любых форматов  
- Расшифровка ранее зашифрованных данных  
- Ключ передается в виде 32-символьной hex-строки  
- Работа полностью совместима с OpenSSL  
- Корректное добавление и удаление PKCS#7 padding  
- CLI-утилита `cryptocore`

---

## Установка

### Требования
- Python 3.10+  
- Windows 10/11  
- pip  
- Git (если клонируете репозиторий)

### Установка зависимостей

```powershell
pip install -r requirements.txt
```
### Показать помощь:
```powershell
cryptocore --help
```
### Пример шифрования:
```powershell
cryptocore ^
  --algorithm aes ^
  --mode ecb ^
  --encrypt ^
  --key 00112233445566778899aabbccddeeff ^
  --input plaintext.txt ^
  --output ciphertext.bin
```
### Пример расшифровки:
```powershell
cryptocore ^
  --algorithm aes ^
  --mode ecb ^
  --decrypt ^
  --key 00112233445566778899aabbccddeeff ^
  --input ciphertext.bin ^
  --output decrypted.txt
```
### Другие методы
```powershell
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

### Цикл с авто-генерацией ключа
```powershell
# Шифрование с авто-генерацией
cryptocore --algorithm aes --mode cbc --encrypt --input original.txt --output auto_enc.bin

# Запоминаем сгенерированный ключ из вывода
# Расшифровка с сгенерированным ключом  
cryptocore --algorithm aes --mode cbc --decrypt --key [GENERATED_KEY] --input auto_enc.bin --output auto_dec.txt

# Проверка целостности
fc original.txt auto_dec.txt /b
```
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
### Запуск тестов:
```powershell
.\tests\sprint3_test.ps1
.\tests\test_csprng_comprehensive.ps1  
.\tests\integration_test.ps1
python tests/test_hash_functions.py
.\tests\test_sprint4_cli.ps1
.\tests\roundtrip_test.ps1
```




