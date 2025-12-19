
# Test CLI for KDF functionality

Write-Host "Testing KDF functionality..." -ForegroundColor Green

# Test 1: Basic derivation with specified salt
Write-Host "`nTest 1: Basic derivation with specified salt" -ForegroundColor Yellow
python -m cryptocore derive --password "MySecurePassword123!" --salt a1b2c3d4e5f601234567890123456789 --iterations 1000 --length 32

# Test 2: Derivation with auto-generated salt
Write-Host "`nTest 2: Derivation with auto-generated salt" -ForegroundColor Yellow
python -m cryptocore derive --password "AnotherPassword" --iterations 500000 --length 16

# Test 3: RFC 6070 test vector 1
Write-Host "`nTest 3: RFC 6070 test vector 1" -ForegroundColor Yellow
python -m cryptocore derive --password "password" --salt 73616c74 --iterations 1 --length 20
Write-Host "Expected: 0c60c80f961f0e71f3a9b524af6012062fe037a6 <salt>" -ForegroundColor Cyan

# Test 4: RFC 6070 test vector 2
Write-Host "`nTest 4: RFC 6070 test vector 2" -ForegroundColor Yellow
python -m cryptocore derive --password "password" --salt 73616c74 --iterations 2 --length 20
Write-Host "Expected: ea6c014dc72d6f8ccd1ed92ace1d41f0d8de8957 <salt>" -ForegroundColor Cyan

# Test 5: Save to file
Write-Host "`nTest 5: Save to file" -ForegroundColor Yellow
python -m cryptocore derive --password "test" --salt 1234567890abcdef --iterations 1000 --length 32 --output test_key.bin
if (Test-Path "test_key.bin") {
    $key = Get-Content -Path "test_key.bin" -Encoding Byte -ReadCount 0
    Write-Host "Key saved (32 bytes): $($key.Length) bytes" -ForegroundColor Green
    Remove-Item "test_key.bin"
}

Write-Host "`nAll CLI tests completed!" -ForegroundColor Green