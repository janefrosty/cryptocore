Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Sprint 7: Key Derivation Functions Tests" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$ErrorActionPreference = "Stop"

function Test-CLI {
    param([string]$Description, [scriptblock]$Command, [string]$ExpectedPattern)
    
    Write-Host "`n$Description" -ForegroundColor Yellow
    Write-Host "Command: $Command" -ForegroundColor Gray
    
    try {
        $output = Invoke-Expression $Command 2>&1 | Out-String
        Write-Host "Output: $($output.Trim())" -ForegroundColor Gray
        
        if ($ExpectedPattern -and $output -notmatch $ExpectedPattern) {
            Write-Host "FAIL: Output doesn't match pattern" -ForegroundColor Red
            return $false
        }
        
        Write-Host "PASS" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "FAIL: $_" -ForegroundColor Red
        return $false
    }
}

# Clean up from previous runs
Remove-Item -Path "test_derived_key.bin", "test_salt.bin" -ErrorAction SilentlyContinue

$allPassed = $true

# Test 1: Basic derivation
$allPassed = $allPassed -and (Test-CLI `
    -Description "Test 1: Basic key derivation" `
    -Command 'python -m cryptocore derive --password "test123" --salt 000102030405060708090a0b0c0d0e0f --iterations 1000 --length 32' `
    -ExpectedPattern "^[0-9a-f]{64} 000102030405060708090a0b0c0d0e0f$")

# Test 2: Auto-generated salt
$output = python -m cryptocore derive --password "test" --iterations 100 --length 16 2>&1
if ($output -match "^[0-9a-f]{32} ([0-9a-f]{32})$") {
    Write-Host "`nTest 2: Auto-generated salt" -ForegroundColor Yellow
    Write-Host "PASS: Salt generated successfully" -ForegroundColor Green
} else {
    Write-Host "`nTest 2: Auto-generated salt" -ForegroundColor Yellow
    Write-Host "FAIL: Invalid output format" -ForegroundColor Red
    $allPassed = $false
}

# Test 3: RFC 6070 test vector 1
$allPassed = $allPassed -and (Test-CLI `
    -Description "Test 3: RFC 6070 test vector 1" `
    -Command 'python -m cryptocore derive --password "password" --salt 73616c74 --iterations 1 --length 20' `
    -ExpectedPattern "^0c60c80f961f0e71f3a9b524af6012062fe037a6 73616c74$")

# Test 4: Save to file
Write-Host "`nTest 4: Save derived key to file" -ForegroundColor Yellow
python -m cryptocore derive --password "filetest" --salt 1122334455667788 --iterations 100 --length 32 --output test_derived_key.bin 2>&1 | Out-Null

if (Test-Path "test_derived_key.bin") {
    $fileSize = (Get-Item "test_derived_key.bin").Length
    if ($fileSize -eq 32) {
        Write-Host "PASS: Key file created with correct size (32 bytes)" -ForegroundColor Green
    } else {
        Write-Host "FAIL: Key file size incorrect ($fileSize bytes)" -ForegroundColor Red
        $allPassed = $false
    }
    Remove-Item "test_derived_key.bin"
} else {
    Write-Host "FAIL: Key file not created" -ForegroundColor Red
    $allPassed = $false
}

# Test 5: Different iterations produce different results
Write-Host "`nTest 5: Different iterations produce different keys" -ForegroundColor Yellow
$key1 = python -m cryptocore derive --password "test" --salt 1234567890abcdef --iterations 100 --length 32 2>&1 | Select-Object -First 1
$key2 = python -m cryptocore derive --password "test" --salt 1234567890abcdef --iterations 1000 --length 32 2>&1 | Select-Object -First 1

if ($key1 -ne $key2) {
    Write-Host "PASS: Different iterations produce different keys" -ForegroundColor Green
} else {
    Write-Host "FAIL: Same key from different iterations" -ForegroundColor Red
    $allPassed = $false
}

# Summary
Write-Host "`n=========================================" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "All tests PASSED! ✓" -ForegroundColor Green
} else {
    Write-Host "Some tests FAILED! ✗" -ForegroundColor Red
    exit 1
}
Write-Host "=========================================" -ForegroundColor Cyan