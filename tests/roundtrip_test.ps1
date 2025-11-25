#!/usr/bin/env pwsh

# SPRINT 2: Extended round-trip test for all modes
$Key = "00112233445566778899aabbccddeeff"
$TestFile = "original.txt"
$EncryptedFile = "encrypted.bin"
$DecryptedFile = "decrypted.txt"

# Create test file
"Hello from Windows! This is Sprint 2 testing." | Out-File -FilePath $TestFile -Encoding ascii

# SPRINT 2: Test all modes
$Modes = @("ecb", "cbc", "cfb", "ofb", "ctr")

foreach ($Mode in $Modes) {
    Write-Host "Testing mode: $Mode" -ForegroundColor Green
    
    # Encryption
    Write-Host "  Encrypting..." -ForegroundColor Yellow
    if ($Mode -eq "ecb") {
        cryptocore --algorithm aes --mode $Mode --encrypt `
            --key $Key `
            --input $TestFile --output $EncryptedFile
    } else {
        $Result = cryptocore --algorithm aes --mode $Mode --encrypt `
            --key $Key `
            --input $TestFile --output $EncryptedFile
        Write-Host $Result
    }
    
    # Decryption  
    Write-Host "  Decrypting..." -ForegroundColor Yellow
    if ($Mode -eq "ecb") {
        cryptocore --algorithm aes --mode $Mode --decrypt `
            --key $Key `
            --input $EncryptedFile --output $DecryptedFile
    } else {
        # For modes with IV, read from file (no --iv parameter)
        cryptocore --algorithm aes --mode $Mode --decrypt `
            --key $Key `
            --input $EncryptedFile --output $DecryptedFile
    }
    
    # Compare files
    Write-Host "  Comparing files..." -ForegroundColor Yellow
    $OriginalHash = (Get-FileHash $TestFile -Algorithm SHA256).Hash
    $DecryptedHash = (Get-FileHash $DecryptedFile -Algorithm SHA256).Hash
    
    if ($OriginalHash -eq $DecryptedHash) {
        Write-Host "  SUCCESS: Round-trip test passed for $Mode" -ForegroundColor Green
    } else {
        Write-Host "  FAILED: Round-trip test failed for $Mode" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Cleanup
Remove-Item $EncryptedFile -ErrorAction SilentlyContinue
Remove-Item $DecryptedFile -ErrorAction SilentlyContinue

Write-Host "All Sprint 2 tests completed!" -ForegroundColor Cyan