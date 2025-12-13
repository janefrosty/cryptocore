# Sprint 5 CLI Test Suite for HMAC functionality

Write-Host "Sprint 5: HMAC CLI Test Suite"
Write-Host "================================"

# Create test files
"Test message for HMAC computation" | Out-File -FilePath "hmac_test.txt" -Encoding ascii

Write-Host "`n1. Testing HMAC Generation..."
Write-Host "-------------------------------"

$key = "00112233445566778899aabbccddeeff"

Write-Host "Generating HMAC for test file..."
cryptocore dgst --algorithm sha256 --hmac --key $key --input hmac_test.txt

Write-Host "`n2. Testing HMAC with Output File..."
Write-Host "--------------------------------------"

cryptocore dgst --algorithm sha256 --hmac --key $key --input hmac_test.txt --output computed_hmac.txt

if (Test-Path "computed_hmac.txt") {
    $hmac_content = Get-Content "computed_hmac.txt"
    Write-Host "HMAC written to file: $hmac_content"
} else {
    Write-Host "ERROR: HMAC file not created"
}

Write-Host "`n3. Testing HMAC Verification..."
Write-Host "----------------------------------"

# First create expected HMAC file
"expected_hmac_value_here hmac_test.txt" | Out-File -FilePath "expected_hmac.txt" -Encoding ascii

Write-Host "Testing verification with wrong HMAC (should fail)..."
cryptocore dgst --algorithm sha256 --hmac --key $key --input hmac_test.txt --verify expected_hmac.txt

Write-Host "`n4. Testing Different Key Sizes..."
Write-Host "------------------------------------"

$short_key = "00112233445566778899aabbccddeeff"  # 16 bytes
$block_key = "00" * 64  # 64 bytes (block size)
$long_key = "00" * 100  # 100 bytes (longer than block)

Write-Host "Testing with short key (16 bytes)..."
cryptocore dgst --algorithm sha256 --hmac --key $short_key --input hmac_test.txt

Write-Host "`nTesting with block size key (64 bytes)..."
cryptocore dgst --algorithm sha256 --hmac --key $block_key --input hmac_test.txt

Write-Host "`nTesting with long key (100 bytes)..."
cryptocore dgst --algorithm sha256 --hmac --key $long_key --input hmac_test.txt

Write-Host "`n5. Testing Error Handling..."
Write-Host "-------------------------------"

Write-Host "Testing without --key when using --hmac (should fail)..."
cryptocore dgst --algorithm sha256 --hmac --input hmac_test.txt

Write-Host "`nTesting with --verify but without --hmac (should fail)..."
cryptocore dgst --algorithm sha256 --input hmac_test.txt --verify expected_hmac.txt

Write-Host "`nTesting invalid key format..."
cryptocore dgst --algorithm sha256 --hmac --key "invalid_hex" --input hmac_test.txt

Write-Host "`n6. Testing Backward Compatibility..."
Write-Host "---------------------------------------"

Write-Host "Testing regular hash (should still work)..."
cryptocore dgst --algorithm sha256 --input hmac_test.txt

Write-Host "`nTesting encryption (should still work)..."
cryptocore enc --algorithm aes --mode cbc --encrypt --input hmac_test.txt --output test_encrypted.bin

Write-Host "`n7. Testing Tamper Detection..."
Write-Host "---------------------------------"

# Create original file
"Original content" | Out-File -FilePath "original.txt" -Encoding ascii

# Generate HMAC
cryptocore dgst --algorithm sha256 --hmac --key $key --input original.txt --output original_hmac.txt

# Tamper with file
"Modified content" | Out-File -FilePath "original.txt" -Encoding ascii

Write-Host "Verifying tampered file (should fail)..."
cryptocore dgst --algorithm sha256 --hmac --key $key --input original.txt --verify original_hmac.txt

# Cleanup
Remove-Item "hmac_test.txt" -ErrorAction SilentlyContinue
Remove-Item "computed_hmac.txt" -ErrorAction SilentlyContinue
Remove-Item "expected_hmac.txt" -ErrorAction SilentlyContinue
Remove-Item "original.txt" -ErrorAction SilentlyContinue
Remove-Item "original_hmac.txt" -ErrorAction SilentlyContinue
Remove-Item "test_encrypted.bin" -ErrorAction SilentlyContinue

Write-Host "`nSprint 5 CLI Testing Complete!"