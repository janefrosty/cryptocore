## Sprint1

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
