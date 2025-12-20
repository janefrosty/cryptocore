# Round-trip test for all encryption modes
# Tests Sprint 1-3, 6 functionality

$Key = "00112233445566778899aabbccddeeff"
$TestFile = "original.txt"
$EncryptedFile = "encrypted.bin"
$DecryptedFile = "decrypted.txt"

"Hello, CryptoCore! This is a test file for round-trip testing." | Out-File -FilePath $TestFile -Encoding ascii

$Modes = @("ecb", "cbc", "cfb", "ofb", "ctr", "gcm")

foreach ($Mode in $Modes) {
    Write-Host "Testing mode: $Mode"
    
    Write-Host "  Encrypting..."
    if ($Mode -eq "gcm") {
        cryptocore enc --algorithm aes --mode $Mode --encrypt --key $Key --input $TestFile --output $EncryptedFile
    } else {
        cryptocore enc --algorithm aes --mode $Mode --encrypt --key $Key --input $TestFile --output $EncryptedFile
    }
    
    Write-Host "  Decrypting..."
    if ($Mode -eq "gcm") {
        cryptocore enc --algorithm aes --mode $Mode --decrypt --key $Key --input $EncryptedFile --output $DecryptedFile
    } else {
        cryptocore enc --algorithm aes --mode $Mode --decrypt --key $Key --input $EncryptedFile --output $DecryptedFile
    }
    
    $OriginalHash = (Get-FileHash $TestFile -Algorithm SHA256).Hash
    $DecryptedHash = (Get-FileHash $DecryptedFile -Algorithm SHA256).Hash
    
    if ($OriginalHash -eq $DecryptedHash) {
        Write-Host "  SUCCESS: Round-trip test passed for $Mode"
    } else {
        Write-Host "  FAILED: Round-trip test failed for $Mode"
    }
    
    Write-Host ""
}

Remove-Item $EncryptedFile -ErrorAction SilentlyContinue
Remove-Item $DecryptedFile -ErrorAction SilentlyContinue
Remove-Item $TestFile -ErrorAction SilentlyContinue

Write-Host "All tests completed!"