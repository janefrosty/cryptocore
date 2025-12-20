
# CryptoCore User Guide

## Table of Contents
1. Installation
2. Quick Start
3. Command Reference
4. Use Cases & Examples
5. Troubleshooting
6. Security Best Practices

## 1. Installation

### Prerequisites
- Python 3.8 or higher

### Steps
1. Clone or download the CryptoCore repository.
2. Navigate to the project root directory in your terminal.
3. Install in development mode:
   ```
   pip install -e .
   ```

### Verification
After installation, verify it works:
```
cryptocore --version
```

## 2. Quick Start

1. Compute a hash of a string:
   ```
   cryptocore --mode hash --algorithm sha256 --input-text "hello world"
   ```

2. Compute a hash of a file:
   ```
   cryptocore --mode hash --algorithm sha256 --input myfile.pdf
   ```

3. Generate an HMAC for a file:
   ```
   cryptocore --mode hmac --key aabbccddeeff00112233445566778899 --input data.bin
   ```

## 3. Command Reference

Run `cryptocore --help` to see all available options:

```
usage: cryptocore [-h] [--version] --mode {hash,hmac,kdf,pbkdf2,hkdf,random} [--algorithm {sha256,sha3_256}] [--key KEY] [--salt SALT] [--iterations ITERATIONS]
                  [--dklen DKLEN] [--info INFO] [--input INPUT] [--output OUTPUT] [--input-text INPUT_TEXT] [--num-bytes NUM_BYTES]

Cryptographic command-line toolkit.

required arguments:
  --mode {hash,hmac,kdf,pbkdf2,hkdf,random}
                        Operation mode (required)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --algorithm {sha256,sha3_256}
                        Hash algorithm (for hash, hmac, pbkdf2, hkdf modes)
  --key KEY             Key in hexadecimal format (for hmac, hkdf modes)
  --salt SALT           Salt in hexadecimal format (for pbkdf2, hkdf modes)
  --iterations ITERATIONS
                        Iteration count (for pbkdf2 mode)
  --dklen DKLEN         Desired key length in bytes (for pbkdf2, hkdf modes)
  --info INFO           Context info in hexadecimal (for hkdf mode)
  --input INPUT         Input file path
  --output OUTPUT       Output file path (default: stdout)
  --input-text INPUT_TEXT
                        Input text (instead of file)
  --num-bytes NUM_BYTES
                        Number of random bytes to generate (for random mode)
```

**Key Format:** All `--key`, `--salt`, `--info` arguments must be provided as **hexadecimal strings** (e.g., `00112233445566778899aabbccddeeff`). No `0x` prefix.

## 4. Use Cases & Examples

### Hashing Files

**SHA-256 of a document:**
```
cryptocore --mode hash --algorithm sha256 --input document.pdf
```

**SHA3-256 of a string:**
```
cryptocore --mode hash --algorithm sha3_256 --input-text "sensitive data"
```

**Save hash to a file:**
```
cryptocore --mode hash --algorithm sha256 --input largefile.iso --output file_hash.txt
```

### Generating HMACs

**Generate an HMAC-SHA256 for a file:**
```
cryptocore --mode hmac --algorithm sha256 --key aabbccddeeff00112233445566778899 --input transaction.log
```

### Deriving Keys with PBKDF2

**Derive a 32-byte key from a password:**
```
export PASSWORD="MyStrongPassword"
export SALT="$(openssl rand -hex 16)"

cryptocore --mode pbkdf2 \
  --input-text "$PASSWORD" \
  --salt "$SALT" \
  --iterations 100000 \
  --dklen 32
```

### Deriving Keys with HKDF

**Expand a master key:**
```
cryptocore --mode hkdf \
  --key 00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff \
  --salt 77656261707073616c74 \
  --info 4145532d3235362d47434d \
  --dklen 32
```

### Generating Random Data

**Generate a 256-bit cryptographic key:**
```
cryptocore --mode random --num-bytes 32
```

**Generate a random salt:**
```
cryptocore --mode random --num-bytes 16 --output salt.bin
```

## 5. Troubleshooting

| Error Message | Possible Cause | Solution |
|---------------|----------------|----------|
| `Invalid hex string` | Key/salt/info contains non-hex characters | Ensure string contains only 0-9, a-f, A-F |
| `File not found` | Input file path is incorrect | Check path and permissions |
| `Unsupported algorithm` | Algorithm not implemented | Check `--algorithm` spelling |
| `ERROR: --mode is required` | Forgot to specify mode | Add `--mode hash` |
| Command not found | Not installed or PATH issue | Run `pip install -e .` again |

## 6. Security Best Practices

1. **Key Management**
   - Never hardcode keys in scripts
   - Store keys in secure vaults or environment variables
   - Use `--mode random` to generate strong keys

2. **Password-based Key Derivation**
   - Use high iteration counts (≥ 100,000)
   - Use unique, random salts for each password
   - Store salt alongside the derived key

3. **HMAC**
   - Use keys at least 32 bytes long
   - Never reuse the same key for both encryption and MAC

4. **General**
   - Verify hashes/HMACs before trusting data
   - Prefer SHA-256 or SHA3-256
   - Keep the library updated
