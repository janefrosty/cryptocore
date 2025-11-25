#!/usr/bin/env pwsh

Write-Host "🚀 Sprint 4 CLI Test Suite" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Create test files
"Hello, CryptoCore! This is Sprint 4 hash testing." | Out-File -FilePath "test_hash_input.txt" -Encoding ascii
"Short test" | Out-File -FilePath "small_file.txt" -Encoding ascii

Write-Host "`n1. Testing Hash Command Syntax..." -ForegroundColor Yellow

# Test basic hash commands
Write-Host "`n   Testing SHA-256..." -ForegroundColor Green
cryptocore dgst --algorithm sha256 --input test_hash_input.txt

Write-Host "`n   Testing SHA3-256..." -ForegroundColor Green
cryptocore dgst --algorithm sha3-256 --input test_hash_input.txt

Write-Host "`n2. Testing Hash Output to File..." -ForegroundColor Yellow

cryptocore dgst --algorithm sha256 --input test_hash_input.txt --output sha256_hash.txt
if (Test-Path "sha256_hash.txt") {
    $hash_content = Get-Content "sha256_hash.txt"
    Write-Host "    SHA-256 hash written to file: $hash_content" -ForegroundColor Green
} else {
    Write-Host "    SHA-256 hash file not created" -ForegroundColor Red
}

cryptocore dgst --algorithm sha3-256 --input test_hash_input.txt --output sha3_hash.txt
if (Test-Path "sha3_hash.txt") {
    $hash_content = Get-Content "sha3_hash.txt"
    Write-Host "    SHA3-256 hash written to file: $hash_content" -ForegroundColor Green
} else {
    Write-Host "    SHA3-256 hash file not created" -ForegroundColor Red
}

Write-Host "`n3. Testing Empty File Hashing..." -ForegroundColor Yellow

# Create empty file
$null > empty_file.txt
cryptocore dgst --algorithm sha256 --input empty_file.txt
cryptocore dgst --algorithm sha3-256 --input empty_file.txt

Write-Host "`n4. Testing Backward Compatibility..." -ForegroundColor Yellow

Write-Host "`n   Testing encryption (should still work)..." -ForegroundColor Green
cryptocore enc --algorithm aes --mode cbc --encrypt --input small_file.txt --output encrypted_test.bin
if ($LASTEXITCODE -eq 0) {
    Write-Host "    Encryption still works" -ForegroundColor Green
} else {
    Write-Host "    Encryption broken" -ForegroundColor Red
}

Write-Host "`n5. Testing Error Handling..." -ForegroundColor Yellow

Write-Host "`n   Testing non-existent file..." -ForegroundColor Gray
cryptocore dgst --algorithm sha256 --input nonexistent_file.txt

Write-Host "`n   Testing invalid algorithm..." -ForegroundColor Gray
cryptocore dgst --algorithm invalid_algo --input test_hash_input.txt

Write-Host "`n6. Testing Command Help..." -ForegroundColor Yellow

cryptocore --help
Write-Host "`n   Encryption help:" -ForegroundColor Gray
cryptocore enc --help
Write-Host "`n   Hash help:" -ForegroundColor Gray
cryptocore dgst --help

# Cleanup
Remove-Item "test_hash_input.txt" -ErrorAction SilentlyContinue
Remove-Item "small_file.txt" -ErrorAction SilentlyContinue
Remove-Item "empty_file.txt" -ErrorAction SilentlyContinue
Remove-Item "encrypted_test.bin" -ErrorAction SilentlyContinue
Remove-Item "sha256_hash.txt" -ErrorAction SilentlyContinue
Remove-Item "sha3_hash.txt" -ErrorAction SilentlyContinue

Write-Host "`n Sprint 4 CLI Testing Complete!" -ForegroundColor Cyan