#!/usr/bin/env pwsh

# SPRINT 3: Extended round-trip test with automatic key generation
$TestFile = "original.txt"
$EncryptedFile = "encrypted.bin"
$DecryptedFile = "decrypted.txt"

# Create test file
"Hello from Windows! This is Sprint 3 testing with automatic key generation." | Out-File -FilePath $TestFile -Encoding ascii

# Test modes
$Modes = @("ecb", "cbc", "cfb", "ofb", "ctr")

foreach ($Mode in $Modes) {
    Write-Host "Testing mode: $Mode" -ForegroundColor Green
    
    try {
        # SPRINT 3: Encryption with automatic key generation
        Write-Host "  Encrypting with auto-generated key..." -ForegroundColor Yellow
        $encryptResult = cryptocore --algorithm aes --mode $Mode --encrypt --input $TestFile --output $EncryptedFile
        Write-Host $encryptResult
        
        # Extract the generated key from output
        $keyLine = $encryptResult | Where-Object { $_ -match "Generated random key: ([0-9a-f]+)" }
        if ($keyLine -and $matches[1]) {
            $generatedKey = $matches[1]
            Write-Host "  Using generated key: $generatedKey" -ForegroundColor Cyan
        } else {
            Write-Host "  ERROR: Could not extract generated key" -ForegroundColor Red
            continue
        }
        
        # Decryption with the generated key
        Write-Host "  Decrypting with generated key..." -ForegroundColor Yellow
        decryptResult = cryptocore --algorithm aes --mode $Mode --decrypt --key $generatedKey --input $EncryptedFile --output $DecryptedFile
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  Decryption failed for $Mode" -ForegroundColor Red
            continue
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
    }
    catch {
        Write-Host "  ERROR testing $Mode : $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
}

Remove-Item $EncryptedFile -ErrorAction SilentlyContinue
Remove-Item $DecryptedFile -ErrorAction SilentlyContinue
Remove-Item $TestFile -ErrorAction SilentlyContinue

Write-Host "All Sprint 3 tests completed!" -ForegroundColor Cyan