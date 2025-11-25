#!/usr/bin/env pwsh

# Debug test script
Write-Host "Creating test files..." -ForegroundColor Yellow
"Test data for encryption debugging" | Out-File -FilePath "test_plain.txt" -Encoding ascii

Write-Host "Testing CBC mode with auto-generated key..." -ForegroundColor Green

# Encryption with auto-generated key
Write-Host "Encrypting..." -ForegroundColor Cyan
cryptocore --algorithm aes --mode cbc --encrypt --input test_plain.txt --output test_encrypted.bin

if ($LASTEXITCODE -ne 0) {
    Write-Host "Encryption failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Encryption successful" -ForegroundColor Green

# Check file sizes
$plainSize = (Get-Item "test_plain.txt").Length
$encryptedSize = (Get-Item "test_encrypted.bin").Length

Write-Host "Plaintext size: $plainSize bytes" -ForegroundColor Gray
Write-Host "Ciphertext size: $encryptedSize bytes" -ForegroundColor Gray
Write-Host "Expected ciphertext size: $($plainSize + 16 + (16 - ($plainSize % 16))) bytes (plain + IV + padding)" -ForegroundColor Gray

# Try decryption with manual key input
Write-Host "`nPlease enter the generated key for decryption:" -ForegroundColor Yellow
$key = Read-Host "Key"

Write-Host "Decrypting with key: $key" -ForegroundColor Cyan
cryptocore --algorithm aes --mode cbc --decrypt --key $key --input test_encrypted.bin --output test_decrypted.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Decryption successful!" -ForegroundColor Green
    
    # Compare files
    $original = Get-Content "test_plain.txt" -Raw
    $decrypted = Get-Content "test_decrypted.txt" -Raw
    
    if ($original -eq $decrypted) {
        Write-Host "SUCCESS: Files are identical!" -ForegroundColor Green
    } else {
        Write-Host "FAILED: Files differ!" -ForegroundColor Red
    }
} else {
    Write-Host "Decryption failed!" -ForegroundColor Red
}

# Cleanup
Remove-Item "test_plain.txt" -ErrorAction SilentlyContinue
Remove-Item "test_encrypted.bin" -ErrorAction SilentlyContinue
Remove-Item "test_decrypted.txt" -ErrorAction SilentlyContinue