"Hello from Windows!" | Out-File -Encoding ascii original.txt

cryptocore --algorithm aes --mode ecb --encrypt `
  --key 00112233445566778899aabbccddeeff `
  --input original.txt --output encrypted.bin

cryptocore --algorithm aes --mode ecb --decrypt `
  --key 00112233445566778899aabbccddeeff `
  --input encrypted.bin --output decrypted.txt

Write-Host "Comparing files..."
if (Compare-Object (Get-Content original.txt) (Get-Content decrypted.txt)) {
    Write-Host "Files differ!"
} else {
    Write-Host "SUCCESS: files are identical!"
}
