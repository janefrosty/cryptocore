
## SPRINT 3 Features

- **Automatic Key Generation**: Secure random key generation when `--key` is omitted
- **CSPRNG Module**: Cryptographically secure random number generator using OS RNG
- **Weak Key Detection**: Warning for potentially weak user-provided keys
- **NIST Test Suite**: Support for statistical randomness testing

## Installation

```bash
pip install -r requirements.txt
pip install -e .

# Key will be automatically generated and displayed
cryptocore --algorithm aes --mode cbc --encrypt --input plaintext.txt --output ciphertext.bin

# Output: 
# [INFO] Generated random key: 1a2b3c4d5e6f7890fedcba9876543210
# Encryption successful. Output written to ciphertext.bin
# IV (hex): a1b2c3d4e5f678901234567890abcdef