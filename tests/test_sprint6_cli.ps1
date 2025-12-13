# Sprint 6 CLI Test Suite for GCM functionality

Write-Host "Sprint 6: GCM CLI Test Suite"
Write-Host "================================"

# Create test files
"Test message for GCM authenticated encryption" | Out-File -FilePath "gcm_test.txt" -Encoding ascii

$key = "00112233445566778899aabbccddeeff"
$aad = "aabbccddeeff00112233445566778899"

Write-Host "`n1. Testing GCM Encryption..."
Write-Host "-------------------------------"

Write-Host "Encrypting with GCM mode..."
cryptocore enc --algorithm aes --mode gcm --encrypt --key $key --input gcm_test.txt --output gcm_encrypted.bin --aad $aad

if (Test-Path "gcm_encrypted.bin") {
    $file_size = (Get-Item "gcm_encrypted.bin").Length
    Write-Host "   GCM encryption successful, file size: $file_size bytes"
    
    # Check that file contains nonce + ciphertext + tag
    if ($file_size -ge 28) {  # 12 nonce + at least 0 ciphertext + 16 tag
        Write-Host "   File structure appears correct"
    }
} else {
    Write-Host "   GCM encryption failed"
}

Write-Host "`n2. Testing GCM Decryption with Correct AAD..."
Write-Host "------------------------------------------------"

cryptocore enc --algorithm aes --mode gcm --decrypt --key $key --input gcm_encrypted.bin --output gcm_decrypted.txt --aad $aad

if ($LASTEXITCODE -eq 0 -and (Test-Path "gcm_decrypted.txt")) {
    Write-Host "   GCM decryption successful"
    
    # Compare with original
    $original = Get-Content "gcm_test.txt" -Raw
    $decrypted = Get-Content "gcm_decrypted.txt" -Raw
    
    if ($original -eq $decrypted) {
        Write-Host "   Files are identical - authentication successful"
    } else {
        Write-Host "   Files differ"
    }
} else {
    Write-Host "   GCM decryption failed"
}

Write-Host "`n3. Testing GCM Decryption with Wrong AAD..."
Write-Host "----------------------------------------------"

$wrong_aad = "ffffffffffffffffffffffffffffffff"

cryptocore enc --algorithm aes --mode gcm --decrypt --key $key --input gcm_encrypted.bin --output gcm_decrypted_wrong.txt --aad $wrong_aad

if ($LASTEXITCODE -ne 0) {
    Write-Host "   GCM correctly rejected wrong AAD"
    
    # Check that no output file was created
    if (-not (Test-Path "gcm_decrypted_wrong.txt")) {
        Write-Host "   No output file created (catastrophic failure)"
    } else {
        Write-Host "   Output file should not have been created"
    }
} else {
    Write-Host "   GCM should have failed with wrong AAD"
}

Write-Host "`n4. Testing GCM with Empty AAD..."
Write-Host "-----------------------------------"

# Create new encryption with empty AAD
cryptocore enc --algorithm aes --mode gcm --encrypt --key $key --input gcm_test.txt --output gcm_empty_aad.bin --aad ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "   GCM encryption with empty AAD successful"
    
    # Decrypt with empty AAD
    cryptocore enc --algorithm aes --mode gcm --decrypt --key $key --input gcm_empty_aad.bin --output gcm_empty_decrypted.txt --aad ""
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   GCM decryption with empty AAD successful"
    }
}

Write-Host "`n5. Testing GCM Tamper Detection..."
Write-Host "-------------------------------------"

# Create a copy and tamper with it
Copy-Item "gcm_encrypted.bin" "gcm_tampered.bin"

# Tamper with the file (change one byte)
$bytes = [System.IO.File]::ReadAllBytes("gcm_tampered.bin")
if ($bytes.Length -gt 20) {
    $bytes[20] = $bytes[20] -bxor 0xFF  # Flip all bits in this byte
    [System.IO.File]::WriteAllBytes("gcm_tampered.bin", $bytes)
    
    Write-Host "  Tampered ciphertext file created"
}

# Try to decrypt tampered file
cryptocore enc --algorithm aes --mode gcm --decrypt --key $key --input gcm_tampered.bin --output gcm_tampered_out.txt --aad $aad

if ($LASTEXITCODE -ne 0) {
    Write-Host "   GCM correctly detected tampered ciphertext"
} else {
    Write-Host "   GCM should have detected tampering"
}

Write-Host "`n6. Testing GCM with Wrong Key..."
Write-Host "-----------------------------------"

$wrong_key = "ffffffffffffffffffffffffffffffff"

cryptocore enc --algorithm aes --mode gcm --decrypt --key $wrong_key --input gcm_encrypted.bin --output gcm_wrong_key.txt --aad $aad

if ($LASTEXITCODE -ne 0) {
    Write-Host "   GCM correctly rejected wrong key"
} else {
    Write-Host "   GCM should have failed with wrong key"
}

Write-Host "`n7. Testing Backward Compatibility..."
Write-Host "---------------------------------------"

Write-Host "Testing CBC mode (should still work)..."
cryptocore enc --algorithm aes --mode cbc --encrypt --key $key --input gcm_test.txt --output cbc_encrypted.bin

if ($LASTEXITCODE -eq 0) {
    Write-Host "   CBC mode still works"
}

Write-Host "`nTesting HMAC (should still work)..."
cryptocore dgst --algorithm sha256 --hmac --key $key --input gcm_test.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "   HMAC still works"
}

Write-Host "`n8. Testing Error Handling..."
Write-Host "-------------------------------"

Write-Host "Testing GCM with missing key for decryption..."
cryptocore enc --algorithm aes --mode gcm --decrypt --input gcm_encrypted.bin --output should_fail.txt --aad $aad

Write-Host "`nTesting GCM with invalid key format..."
cryptocore enc --algorithm aes --mode gcm --encrypt --key "invalid_hex" --input gcm_test.txt --output should_fail2.bin --aad $aad

Write-Host "`nTesting GCM with invalid AAD format..."
cryptocore enc --algorithm aes --mode gcm --encrypt --key $key --input gcm_test.txt --output should_fail3.bin --aad "invalid_hex"

# Cleanup
Remove-Item "gcm_test.txt" -ErrorAction SilentlyContinue
Remove-Item "gcm_encrypted.bin" -ErrorAction SilentlyContinue
Remove-Item "gcm_decrypted.txt" -ErrorAction SilentlyContinue
Remove-Item "gcm_decrypted_wrong.txt" -ErrorAction SilentlyContinue
Remove-Item "gcm_empty_aad.bin" -ErrorAction SilentlyContinue
Remove-Item "gcm_empty_decrypted.txt" -ErrorAction SilentlyContinue
Remove-Item "gcm_tampered.bin" -ErrorAction SilentlyContinue
Remove-Item "gcm_tampered_out.txt" -ErrorAction SilentlyContinue
Remove-Item "gcm_wrong_key.txt" -ErrorAction SilentlyContinue
Remove-Item "cbc_encrypted.bin" -ErrorAction SilentlyContinue

Write-Host "`nSprint 6 CLI Testing Complete!"