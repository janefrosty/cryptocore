"Hello, CryptoCore! This is Sprint 4 hash testing." | Out-File -FilePath "test_hash_input.txt" -Encoding ascii
"Short test" | Out-File -FilePath "small_file.txt" -Encoding ascii

Write-Host "Testing Hash Command Syntax..."

Write-Host "Testing SHA-256..."
cryptocore dgst --algorithm sha256 --input test_hash_input.txt

Write-Host "Testing SHA3-256..."
cryptocore dgst --algorithm sha3-256 --input test_hash_input.txt

Write-Host "Testing Hash Output to File..."

cryptocore dgst --algorithm sha256 --input test_hash_input.txt --output sha256_hash.txt
if (Test-Path "sha256_hash.txt") {
    $hash_content = Get-Content "sha256_hash.txt"
    Write-Host "SHA-256 hash written to file: $hash_content"
} else {
    Write-Host "SHA-256 hash file not created"
}

cryptocore dgst --algorithm sha3-256 --input test_hash_input.txt --output sha3_hash.txt
if (Test-Path "sha3_hash.txt") {
    $hash_content = Get-Content "sha3_hash.txt"
    Write-Host "SHA3-256 hash written to file: $hash_content"
} else {
    Write-Host "SHA3-256 hash file not created"
}

Write-Host "Testing Empty File Hashing..."

$null > empty_file.txt
cryptocore dgst --algorithm sha256 --input empty_file.txt
cryptocore dgst --algorithm sha3-256 --input empty_file.txt

Write-Host "Testing Backward Compatibility..."

Write-Host "Testing encryption (should still work)..."
cryptocore enc --algorithm aes --mode cbc --encrypt --input small_file.txt --output encrypted_test.bin
if ($LASTEXITCODE -eq 0) {
    Write-Host "Encryption still works"
} else {
    Write-Host "Encryption broken"
}

Write-Host "Testing Error Handling..."

Write-Host "Testing non-existent file..."
cryptocore dgst --algorithm sha256 --input nonexistent_file.txt

Write-Host "Testing invalid algorithm..."
cryptocore dgst --algorithm invalid_algo --input test_hash_input.txt

Write-Host "Testing Command Help..."

cryptocore --help
Write-Host "Encryption help:"
cryptocore enc --help
Write-Host "Hash help:"
cryptocore dgst --help

# Cleanup
Remove-Item "test_hash_input.txt" -ErrorAction SilentlyContinue
Remove-Item "small_file.txt" -ErrorAction SilentlyContinue
Remove-Item "empty_file.txt" -ErrorAction SilentlyContinue
Remove-Item "encrypted_test.bin" -ErrorAction SilentlyContinue
Remove-Item "sha256_hash.txt" -ErrorAction SilentlyContinue
Remove-Item "sha3_hash.txt" -ErrorAction SilentlyContinue

Write-Host "Sprint 4 CLI Testing Complete!"