# CryptoProvider
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
### Запуск теста:
```powershell
powershell -ExecutionPolicy Bypass tests/roundtrip_test.ps1
```




