import os
import sys
from .cli_parser import parse_arguments
from .file_io import read_binary_file, write_binary_file, read_file_with_iv, write_file_with_iv
from .csprng import generate_key, generate_iv

# Encryption imports (Sprints 1-2)
from .modes.ecb import aes_ecb_encrypt, aes_ecb_decrypt
from .modes.cbc import aes_cbc_encrypt, aes_cbc_decrypt
from .modes.cfb import aes_cfb_encrypt, aes_cfb_decrypt
from .modes.ofb import aes_ofb_encrypt, aes_ofb_decrypt
from .modes.ctr import aes_ctr_encrypt, aes_ctr_decrypt

# Hash imports (Sprint 4)
from .hash.sha256 import sha256_file
from .hash.sha3_256 import sha3_256_file

# Sprint 5: HMAC imports
from .mac.hmac import hmac_sha256_file

# Mode function mapping (Sprint 2)
ENCRYPT_FUNCTIONS = {
    'ecb': aes_ecb_encrypt,
    'cbc': aes_cbc_encrypt,
    'cfb': aes_cfb_encrypt,
    'ofb': aes_ofb_encrypt,
    'ctr': aes_ctr_encrypt
}

DECRYPT_FUNCTIONS = {
    'ecb': aes_ecb_decrypt,
    'cbc': aes_cbc_decrypt,
    'cfb': aes_cfb_decrypt,
    'ofb': aes_ofb_decrypt,
    'ctr': aes_ctr_decrypt
}

# Hash function mapping (Sprint 4)
HASH_FUNCTIONS = {
    'sha256': sha256_file,
    'sha3-256': sha3_256_file
}

def handle_encryption(args):
    """
    Handle encryption/decryption operations (Sprints 1-3)
    """
    if args.key:
        key = bytes.fromhex(args.key)
    else:
        key = generate_key(16)
        key_hex = key.hex()
        print(f"[INFO] Generated random key: {key_hex}")
    
    if args.encrypt:
        if args.mode == 'ecb':
            data = read_binary_file(args.input)
            result = aes_ecb_encrypt(key, data)
            write_binary_file(args.output, result)
            print(f"Encryption successful. Output written to {args.output}")
        else:
            iv = generate_iv()
            data = read_binary_file(args.input)
            encrypt_func = ENCRYPT_FUNCTIONS[args.mode]
            result = encrypt_func(key, data, iv)
            write_file_with_iv(args.output, iv, result)
            print(f"Encryption successful. Output written to {args.output}")
            print(f"IV (hex): {iv.hex()}")
    
    else:
        decrypt_func = DECRYPT_FUNCTIONS[args.mode]
        
        if args.mode == 'ecb':
            data = read_binary_file(args.input)
            result = decrypt_func(key, data)
            write_binary_file(args.output, result)
            print(f"Decryption successful. Output written to {args.output}")
        else:
            if args.iv:
                iv = bytes.fromhex(args.iv)
                data = read_binary_file(args.input)
            else:
                try:
                    iv, data = read_file_with_iv(args.input)
                except ValueError as e:
                    print(f"Error reading IV from file: {e}", file=sys.stderr)
                    sys.exit(1)
            
            try:
                result = decrypt_func(key, data, iv)
                write_binary_file(args.output, result)
                print(f"Decryption successful. Output written to {args.output}")
            except ValueError as e:
                print(f"Decryption error: {e}", file=sys.stderr)
                sys.exit(1)

def handle_hash(args):
    """
    Handle hash and HMAC operations (Sprints 4-5)
    Sprint 5: Added HMAC computation and verification
    """
    try:
        if args.hmac:
            # Sprint 5: HMAC mode
            key = bytes.fromhex(args.key)
            
            if args.algorithm != 'sha256':
                print("Error: HMAC currently only supports SHA-256", file=sys.stderr)
                sys.exit(1)
            
            # Compute HMAC
            hmac_value = hmac_sha256_file(key, args.input)
            output_line = f"{hmac_value} {args.input}"
            
            # Sprint 5: Verification mode
            if args.verify:
                # Read expected HMAC from file
                try:
                    with open(args.verify, 'r') as f:
                        expected_line = f.read().strip()
                    
                    # Parse expected HMAC (handle different formats)
                    expected_parts = expected_line.split()
                    if len(expected_parts) >= 1:
                        expected_hmac = expected_parts[0]
                    else:
                        print(f"Error: Invalid HMAC file format", file=sys.stderr)
                        sys.exit(1)
                    
                    # Compare
                    if hmac_value == expected_hmac:
                        print(f"[OK] HMAC verification successful")
                        sys.exit(0)
                    else:
                        print(f"[ERROR] HMAC verification failed", file=sys.stderr)
                        print(f"  Expected: {expected_hmac}", file=sys.stderr)
                        print(f"  Computed: {hmac_value}", file=sys.stderr)
                        sys.exit(1)
                        
                except FileNotFoundError:
                    print(f"Error: HMAC verification file '{args.verify}' not found", file=sys.stderr)
                    sys.exit(1)
            
        else:
            # Sprint 4: Regular hash mode
            hash_func = HASH_FUNCTIONS[args.algorithm]
            hash_value = hash_func(args.input)
            output_line = f"{hash_value} {args.input}"
        
        # Output handling (common for both hash and HMAC)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_line + '\n')
            print(f"Output written to {args.output}")
        else:
            print(output_line)
            
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main entry point for CryptoCore
    """
    try:
        args = parse_arguments()
        
        if args.command == 'enc':
            handle_encryption(args)
        elif args.command == 'dgst':
            handle_hash(args)
        else:
            print(f"Error: Unknown command '{args.command}'", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()