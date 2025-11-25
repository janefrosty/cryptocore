#!/usr/bin/env pwsh

# SPRINT 2: OpenSSL interoperability test
$Key = "000102030405060708090a0b0c0d0e0f"
$TestFile = "test_plain.txt"
$CryptoCoreEncrypted = "cryptocore_encrypted.bin"
$OpenSSLDecrypted = "openssl_decrypted.txt"
$OpenSSLEncrypted = "openssl_encrypted.bin"
$CryptoCoreDecrypted = "cryptocore_decrypted.txt"

# Create test file
"Test data for OpenSSL interoperability" | Out-File -FilePath $TestFile -Encoding ascii

$Modes = @("cbc", "cfb", "ofb", "ctr")

foreach ($Mode in $Modes) {
    Write-Host "Testing interoperability for mode: $Mode" -ForegroundColor Green
    
    # Test 1: CryptoCore -> OpenSSL
    Write-Host "  CryptoCore -> OpenSSL..." -ForegroundColor Yellow
    
    # Encrypt with CryptoCore
    cryptocore --algorithm aes --mode $Mode --encrypt `
        --key $Key `
        --input $TestFile --output $CryptoCoreEncrypted
    
    # Extract IV and ciphertext
    & dd if=$CryptoCoreEncrypted of=iv.bin bs=16 count=1 2>$null
    & dd if=$CryptoCoreEncrypted of=cipher_only.bin bs=16 skip=1 2>$null
    
    # Decrypt with OpenSSL
    $IVHex = & xxd -p iv.bin | tr -d "`n"
    openssl enc -aes-128-$Mode -d `
        -K $Key `
        -iv $IVHex `
        -in cipher_only.bin `
        -out $OpenSSLDecrypted
    
    # Compare
    $OriginalHash = (Get-FileHash $TestFile -Algorithm SHA256).Hash
    $DecryptedHash = (Get-FileHash $OpenSSLDecrypted -Algorithm SHA256).Hash
    
    if ($OriginalHash -eq $DecryptedHash) {
        Write-Host "  SUCCESS: CryptoCore -> OpenSSL works for $Mode" -ForegroundColor Green
    } else {
        Write-Host "  FAILED: CryptoCore -> OpenSSL failed for $Mode" -ForegroundColor Red
    }
    
    # Test 2: OpenSSL -> CryptoCore  
    Write-Host "  OpenSSL -> CryptoCore..." -ForegroundColor Yellow
    
    # Encrypt with OpenSSL
    $TestIV = "aabbccddeeff00112233445566778899"
    openssl enc -aes-128-$Mode `
        -K $Key `
        -iv $TestIV `
        -in $TestFile `
        -out $OpenSSLEncrypted
    
    # Decrypt with CryptoCore
    cryptocore --algorithm aes --mode $Mode --decrypt `
        --key $Key `
        --iv $TestIV `
        --input $OpenSSLEncrypted `
        --output $CryptoCoreDecrypted
    
    # Compare
    $DecryptedHash2 = (Get-FileHash $CryptoCoreDecrypted -Algorithm SHA256).Hash
    
    if ($OriginalHash -eq $DecryptedHash2) {
        Write-Host "  SUCCESS: OpenSSL -> CryptoCore works for $Mode" -ForegroundColor Green
    } else {
        Write-Host "  FAILED: OpenSSL -> CryptoCore failed for $Mode" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Cleanup
Remove-Item $CryptoCoreEncrypted -ErrorAction SilentlyContinue
Remove-Item $OpenSSLDecrypted -ErrorAction SilentlyContinue
Remove-Item $OpenSSLEncrypted -ErrorAction SilentlyContinue
Remove-Item $CryptoCoreDecrypted -ErrorAction SilentlyContinue
Remove-Item iv.bin -ErrorAction SilentlyContinue
Remove-Item cipher_only.bin -ErrorAction SilentlyContinue
Remove-Item $TestFile -ErrorAction SilentlyContinue

Write-Host "OpenSSL interoperability tests completed!" -ForegroundColor Cyan