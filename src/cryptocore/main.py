import os
import sys
from .cli_parser import parse_arguments
from .file_io import read_binary_file, write_binary_file, read_file_with_iv, write_file_with_iv
from .csprng import generate_key, generate_iv
from .kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt

# Sprint 1: ECB mode imports
from .modes.ecb import aes_ecb_encrypt, aes_ecb_decrypt

# Sprint 2: Additional mode imports
from .modes.cbc import aes_cbc_encrypt, aes_cbc_decrypt
from .modes.cfb import aes_cfb_encrypt, aes_cfb_decrypt
from .modes.ofb import aes_ofb_encrypt, aes_ofb_decrypt
from .modes.ctr import aes_ctr_encrypt, aes_ctr_decrypt

# Sprint 6: GCM import
from .modes.gcm import aes_gcm_encrypt, aes_gcm_decrypt, AuthenticationError

# Sprint 4: Hash function imports
from .hash.sha256 import sha256_file
from .hash.sha3_256 import sha3_256_file

# Sprint 5: HMAC imports
from .mac.hmac import hmac_sha256_file

# Mode function mapping (Sprint 2, 6)
ENCRYPT_FUNCTIONS = {
    'ecb': aes_ecb_encrypt,
    'cbc': aes_cbc_encrypt,
    'cfb': aes_cfb_encrypt,
    'ofb': aes_ofb_encrypt,
    'ctr': aes_ctr_encrypt,
    'gcm': aes_gcm_encrypt,
}

DECRYPT_FUNCTIONS = {
    'ecb': aes_ecb_decrypt,
    'cbc': aes_cbc_decrypt,
    'cfb': aes_cfb_decrypt,
    'ofb': aes_ofb_decrypt,
    'ctr': aes_ctr_decrypt,
    'gcm': aes_gcm_decrypt,
}

# Hash function mapping (Sprint 4)
HASH_FUNCTIONS = {
    'sha256': sha256_file,
    'sha3-256': sha3_256_file
}

def handle_encryption(args):
    """
    Handle encryption/decryption operations
    Sprint 1-3, 6: All encryption modes including GCM
    """
    if args.key:
        key = bytes.fromhex(args.key)
    else:
        key = generate_key(16)
        key_hex = key.hex()
        print(f"[INFO] Generated random key: {key_hex}")
    
    # Sprint 6: Parse AAD for GCM
    aad = bytes.fromhex(args.aad) if args.aad else b""
    
    if args.encrypt:
        if args.mode == 'gcm':
            # Sprint 6: GCM encryption
            try:
                data = read_binary_file(args.input)
                result = aes_gcm_encrypt(key, data, aad)
                write_binary_file(args.output, result)
                print(f"GCM encryption successful. Output written to {args.output}")
                
                nonce = result[:12]
                print(f"Nonce (hex): {nonce.hex()}")
                if aad:
                    print(f"AAD (hex): {aad.hex()}")
                    
            except Exception as e:
                print(f"GCM encryption error: {e}", file=sys.stderr)
                sys.exit(1)
                
        elif args.mode == 'ecb':
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
        # Decryption
        if args.mode == 'gcm':
            # Sprint 6: GCM decryption with authentication
            try:
                data = read_binary_file(args.input)
                
                if len(data) < 28:
                    print("Error: Input file too short for GCM format", file=sys.stderr)
                    sys.exit(1)
                
                result = aes_gcm_decrypt(key, data, aad)
                write_binary_file(args.output, result)
                print(f"[SUCCESS] GCM decryption and authentication completed successfully")
                
            except AuthenticationError as e:
                if os.path.exists(args.output):
                    os.remove(args.output)
                print(f"[ERROR] Authentication failed: {e}", file=sys.stderr)
                sys.exit(1)
                
            except Exception as e:
                if os.path.exists(args.output):
                    os.remove(args.output)
                print(f"GCM decryption error: {e}", file=sys.stderr)
                sys.exit(1)
                
        elif args.mode == 'ecb':
            data = read_binary_file(args.input)
            result = aes_ecb_decrypt(key, data)
            write_binary_file(args.output, result)
            print(f"Decryption successful. Output written to {args.output}")
        else:
            decrypt_func = DECRYPT_FUNCTIONS[args.mode]
            
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
    Handle hash and HMAC operations
    Sprint 4-5: Hash functions and HMAC
    """
    try:
        if args.hmac:
            # Sprint 5: HMAC mode
            key = bytes.fromhex(args.key)
            
            if args.algorithm != 'sha256':
                print("Error: HMAC currently only supports SHA-256", file=sys.stderr)
                sys.exit(1)
            
            hmac_value = hmac_sha256_file(key, args.input)
            output_line = f"{hmac_value} {args.input}"
            
            if args.verify:
                try:
                    with open(args.verify, 'r') as f:
                        expected_line = f.read().strip()
                    
                    expected_parts = expected_line.split()
                    if len(expected_parts) >= 1:
                        expected_hmac = expected_parts[0]
                    else:
                        print(f"Error: Invalid HMAC file format", file=sys.stderr)
                        sys.exit(1)
                    
                    if hmac_value == expected_hmac:
                        print(f"[OK] HMAC verification successful")
                        sys.exit(0)
                    else:
                        print(f"[ERROR] HMAC verification failed", file=sys.stderr)
                        sys.exit(1)
                        
                except FileNotFoundError:
                    print(f"Error: HMAC verification file '{args.verify}' not found", file=sys.stderr)
                    sys.exit(1)
            
        else:
            # Sprint 4: Regular hash mode
            hash_func = HASH_FUNCTIONS[args.algorithm]
            hash_value = hash_func(args.input)
            output_line = f"{hash_value} {args.input}"
        
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
    Routes to appropriate handler based on command
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

def derive_command(args):
    """Handle derive command"""
    try:
        # Read password from file if specified
        password = None
        if args.password_file:
            with open(args.password_file, 'r') as f:
                password = f.read().strip()
        else:
            password = args.password
        
        if not password:
            print("Error: Password cannot be empty")
            return 1
        
        # Generate salt if not provided
        if args.salt is None:
            salt = generate_salt(16)
            salt_hex = salt.hex()
            print(f"Generated salt: {salt_hex}")
            
            # Save salt to file if requested
            if args.output_salt:
                with open(args.output_salt, 'w') as f:
                    f.write(salt_hex)
                print(f"Salt saved to: {args.output_salt}")
        else:
            salt_hex = args.salt
            salt = bytes.fromhex(salt_hex)
        
        # Validate parameters
        if args.iterations < 1:
            print("Error: Iterations must be positive")
            return 1
        
        if args.length < 1:
            print("Error: Length must be positive")
            return 1
        
        # Derive key
        print(f"Deriving key with {args.iterations} iterations...")
        derived_key = pbkdf2_hmac_sha256(
            password=password,
            salt=salt,
            iterations=args.iterations,
            dklen=args.length
        )
        
        # Clear password from memory
        password = None
        args.password = None
        
        # Output result
        if args.output:
            with open(args.output, 'wb') as f:
                f.write(derived_key)
            print(f"Key written to {args.output}")
            print(f"Key (hex): {derived_key.hex()}")
            print(f"Salt (hex): {salt_hex}")
        else:
            # Output format: KEY_HEX SALT_HEX
            print(f"{derived_key.hex()} {salt_hex}")
        
        return 0
        
    except ValueError as e:
        print(f"Error: Invalid input format - {e}")
        return 1
    except Exception as e:
        print(f"Error during key derivation: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()