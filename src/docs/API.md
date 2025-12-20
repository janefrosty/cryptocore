```markdown
# CryptoCore API Documentation

**Version:** 1.0.0 | **Python:** 3.8+

## Table of Contents
1. [Overview](#overview)
2. [Module: hash](#module-hash)
   - [sha256](#sha256)
   - [sha3_256](#sha3_256)
3. [Module: kdf](#module-kdf)
   - [pbkdf2](#pbkdf2)
   - [hkdf](#hkdf)
4. [Module: mac](#module-mac)
   - [hmac](#hmac)
5. [Module: modes](#module-modes)
   - [csprng](#csprng)
   - [cli_parser](#cli-parser)
   - [file_to](#file-to)
   - [main](#main)

## Overview

CryptoCore is a Python library providing essential cryptographic primitives for hashing, message authentication, key derivation, and symmetric encryption via a command-line interface. This document describes the public API for developers who wish to use CryptoCore as a library.

All functions expect and return `bytes` objects unless otherwise noted. String inputs should be encoded to bytes (e.g., `b"password"` or `"password".encode('utf-8')`).


## Module: `hash`

Functions for computing cryptographic hash digests.

### `sha256(data: bytes) -> bytes`

Computes the SHA-256 hash of the input data according to FIPS 180-4.

**Parameters:**
- `data` (`bytes`): The input data to hash. Can be of any length, including empty bytes.

**Returns:**
- `bytes`: The 32-byte (256-bit) SHA-256 digest.

**Raises:**
- `TypeError`: If the input is not of type `bytes`.

**Example:**
```python
from cryptocore.hash import sha256

message = b"hello world"
digest = sha256(message)
print(f"SHA-256: {digest.hex()}")
# Output: SHA-256: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
```

**Security Considerations:**
- SHA-256 is collision-resistant and considered secure for most applications.
- For password hashing, use a Key Derivation Function (KDF) like PBKDF2 instead.


### `sha3_256(data: bytes) -> bytes`

Computes the SHA3-256 (Keccak) hash of the input data according to FIPS 202.

**Parameters:**
- `data` (`bytes`): The input data to hash. Can be of any length.

**Returns:**
- `bytes`: The 32-byte (256-bit) SHA3-256 digest.

**Raises:**
- `TypeError`: If the input is not of type `bytes`.

**Example:**
```python
from cryptocore.hash import sha3_256

message = b"hello world"
digest = sha3_256(message)
print(f"SHA3-256: {digest.hex()}")
# Output: SHA3-256: 644bcc7e564373040999aac89e7622f3ca71fba1d972fd94a31c3bfbf24e3938
```

**Security Considerations:**
- SHA3-256 is part of the newer SHA-3 family and provides security strengths similar to SHA-256.
- It uses a different internal structure (sponge construction) than SHA-2.

## Module: `kdf`

Functions for deriving cryptographic keys from passwords or other weak secrets.

### `pbkdf2(password: bytes, salt: bytes, iterations: int, dklen: int, hash_name: str = 'sha256') -> bytes`

Derives a key using the Password-Based Key Derivation Function 2 (PBKDF2) algorithm as defined in RFC 8018.

**Parameters:**
- `password` (`bytes`): The input password or passphrase.
- `salt` (`bytes`): Cryptographic salt. Should be at least 8-16 bytes long and unique per password.
- `iterations` (`int`): Number of iterations. Higher values increase security but slow down derivation. Recommended minimum is 100,000.
- `dklen` (`int`): Desired length of the derived key in bytes.
- `hash_name` (`str`, optional): Underlying hash function to use. Supported: `'sha256'`, `'sha3_256'`. Defaults to `'sha256'`.

**Returns:**
- `bytes`: The derived key of length `dklen`.

**Raises:**
- `TypeError`: If `password` or `salt` are not `bytes`.
- `ValueError`: If `iterations` < 1, `dklen` < 1, or unsupported `hash_name` is provided.

**Example:**
```python
from cryptocore.kdf import pbkdf2

password = b"SuperSecretPassword"
salt = b"UniqueSalt123"
derived_key = pbkdf2(password, salt, iterations=100000, dklen=32)
print(f"Derived key (hex): {derived_key.hex()}")
```

**Security Considerations:**
- Always use a unique, random salt for each password.
- Choose iteration counts as high as tolerable for your application (e.g., > 100,000).
- Store the salt, iteration count, and hash name alongside the derived key.


### `hkdf(ikm: bytes, salt: bytes, info: bytes, dklen: int, hash_name: str = 'sha256') -> bytes`

Derives a key using the HMAC-based Extract-and-Expand Key Derivation Function (HKDF) as defined in RFC 5869.

**Parameters:**
- `ikm` (`bytes`): Input Keying Material (the initial secret).
- `salt` (`bytes`): Salt value (can be empty bytes `b""` for a "salt-free" operation).
- `info` (`bytes`): Context and application-specific information (can be empty).
- `dklen` (`int`): Desired length of the derived key in bytes.
- `hash_name` (`str`, optional): Underlying hash function for HMAC. Supported: `'sha256'`, `'sha3_256'`. Defaults to `'sha256'`.

**Returns:**
- `bytes`: The derived key of length `dklen`.

**Raises:**
- `TypeError`: If `ikm`, `salt`, or `info` are not `bytes`.
- `ValueError`: If `dklen` < 1, or unsupported `hash_name` is provided.

**Example:**
```python
from cryptocore.kdf import hkdf

initial_key = b"master-secret-key-32-bytes-long"
salt = b"application-salt"
context_info = b"AES-256-key-for-file-encryption"
derived_key = hkdf(initial_key, salt, context_info, dklen=32)
print(f"HKDF derived key: {derived_key.hex()}")
```

**Security Considerations:**
- HKDF is suitable for expanding existing cryptographic keys, not for weak passwords.
- Different `info` values produce independent keys from the same `ikm`.

---

## Module: `mac`

Functions for computing Message Authentication Codes (MACs).

### `hmac(key: bytes, message: bytes, hash_name: str = 'sha256') -> bytes`

Computes a Hash-based Message Authentication Code (HMAC) as defined in RFC 2104.

**Parameters:**
- `key` (`bytes`): The secret key. Can be of any length, but recommended length is at least the hash output size (32 bytes for SHA-256).
- `message` (`bytes`): The message to authenticate.
- `hash_name` (`str`, optional): Underlying hash function. Supported: `'sha256'`, `'sha3_256'`. Defaults to `'sha256'`.

**Returns:**
- `bytes`: The HMAC tag. Length equals the output size of the chosen hash (32 bytes for SHA-256).

**Raises:**
- `TypeError`: If `key` or `message` are not `bytes`.
- `ValueError`: If unsupported `hash_name` is provided.

**Example:**
```python
from cryptocore.mac import hmac

secret_key = b"0123456789abcdef" * 2  # 32-byte key
msg = b"Important transaction data"
tag = hmac(secret_key, msg)
print(f"HMAC-SHA256 tag: {tag.hex()}")

# Verification (recompute and compare)
tag2 = hmac(secret_key, msg)
assert tag == tag2, "HMAC verification failed"
```

**Security Considerations:**
- The security of HMAC depends on the secrecy of the key and the strength of the underlying hash.
- Never use the same key for both encryption and MAC (if required, derive separate keys using a KDF).

## Module: `modes`

This module provides the Command-Line Interface (CLI) and supporting utilities. Most functions here are internal. The primary public entry point is the `main()` function, which is called when executing the `cryptocore` command.

### `csprng.generate_random_bytes(num_bytes: int) -> bytes`

Generates cryptographically secure random bytes suitable for cryptographic use (keys, IVs, salts).

**Parameters:**
- `num_bytes` (`int`): Number of random bytes to generate.

**Returns:**
- `bytes`: A bytes object of length `num_bytes` containing random data.

**Raises:**
- `ValueError`: If `num_bytes` < 1.

**Example:**
```python
from cryptocore.modes.csprng import generate_random_bytes

key = generate_random_bytes(32)
iv = generate_random_bytes(16)
print(f"Random key: {key.hex()}")
print(f"Random IV: {iv.hex()}")
```

**Security Considerations:**
- This function uses `os.urandom()` or `secrets.token_bytes()` which are suitable for cryptographic purposes.
- Never use `random` module for cryptographic randomness.


### `cli_parser.create_parser() -> argparse.ArgumentParser`

Creates and configures the command-line argument parser for the `cryptocore` tool. This function is primarily used internally by `main()`.

**Returns:**
- `argparse.ArgumentParser`: A configured parser object.

**Example (internal usage):**
```python
from cryptocore.modes.cli_parser import create_parser
parser = create_parser()
args = parser.parse_args(["--mode", "hash", "--algorithm", "sha256", "--input", "file.txt"])
```

### `file_to.read_file_bytes(filepath: str) -> bytes`

Reads the entire contents of a file into a bytes object.

**Parameters:**
- `filepath` (`str`): Path to the file.

**Returns:**
- `bytes`: The file's contents.

**Raises:**
- `FileNotFoundError`: If the file does not exist.
- `PermissionError`: If insufficient permissions.
- `IOError`: For other I/O errors.

**Example:**
```python
from cryptocore.modes.file_to import read_file_bytes

data = read_file_bytes("document.pdf")
```

### `file_to.write_file_bytes(filepath: str, data: bytes) -> None`

Writes a bytes object to a file.

**Parameters:**
- `filepath` (`str`): Path to the output file.
- `data` (`bytes`): Data to write.

**Raises:**
- `PermissionError`: If insufficient permissions.
- `IOError`: For I/O errors.

**Example:**
```python
from cryptocore.modes.file_to import write_file_bytes

write_file_bytes("output.bin", b"some data")
```

### `main.main() -> None`

The main entry point for the CryptoCore CLI. This function is executed when running `cryptocore` from the command line. It parses arguments, calls the appropriate cryptographic functions, and handles output.

**Usage from shell:**
```bash
cryptocore --mode hash --algorithm sha256 --input file.txt
```

**Example (calling programmatically):**
```python
import sys
from cryptocore.modes.main import main

# Simulate command-line arguments
sys.argv = ["cryptocore", "--mode", "hash", "--algorithm", "sha256", "--input", "test.txt"]
try:
    main()
except SystemExit:
    pass  # argparse calls sys.exit()
```

