import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CryptoCore - Cryptographic Tool Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # SPRINT 4: Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encryption/decryption command (existing functionality)
    enc_parser = subparsers.add_parser('enc', help='Encryption/decryption operations')
    
    enc_parser.add_argument(
        "--algorithm", 
        required=True,
        help="Cryptographic algorithm to use"
    )
    
    enc_parser.add_argument(
        "--mode", 
        required=True,
        choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
        help="Block cipher mode of operation"
    )

    action_group = enc_parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--encrypt", action="store_true")
    action_group.add_argument("--decrypt", action="store_true")

    enc_parser.add_argument("--key", help="Encryption key as hexadecimal string (optional for encryption)")
    enc_parser.add_argument("--iv", help="Initialization vector as hexadecimal string (for decryption)")
    enc_parser.add_argument("--input", required=True, help="Input file path")
    enc_parser.add_argument("--output", help="Output file path")
    
    # SPRINT 4: Hash command
    hash_parser = subparsers.add_parser('dgst', help='Compute message digests')
    
    hash_parser.add_argument(
        "--algorithm",
        required=True,
        choices=['sha256', 'sha3-256'],
        help="Hash algorithm to use"
    )
    
    hash_parser.add_argument(
        "--input",
        required=True,
        help="Input file path"
    )
    
    hash_parser.add_argument(
        "--output",
        help="Output file for hash (optional)"
    )

    args = parser.parse_args()
    
    # Handle no command provided
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # SPRINT 4: Different validation for different commands
    if args.command == 'enc':
        _validate_encryption_args(args)
    elif args.command == 'dgst':
        _validate_hash_args(args)
    
    return args

def _validate_encryption_args(args):
    # Validate algorithm
    if args.algorithm.lower() != "aes":
        print("Error: Only AES is supported for encryption.", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting operations
    if args.encrypt == args.decrypt:
        print("Error: Choose exactly one: --encrypt or --decrypt", file=sys.stderr)
        sys.exit(1)

    # Key validation
    if args.key:
        try:
            key_bytes = bytes.fromhex(args.key)
            key_length = len(key_bytes)
            if key_length not in [16, 24, 32]:
                print("Error: AES key must be 16, 24, or 32 bytes (32, 48, or 64 hex characters).", file=sys.stderr)
                sys.exit(1)
            
            # Check for weak keys
            if _is_weak_key(key_bytes):
                print(f"Warning: The provided key may be weak. Consider using a randomly generated key.", file=sys.stderr)
                
        except ValueError:
            print("Error: Key must be valid hex.", file=sys.stderr)
            sys.exit(1)
    else:
        # Key is optional for encryption, required for decryption
        if args.decrypt:
            print("Error: Key is required for decryption operations.", file=sys.stderr)
            sys.exit(1)

    # IV validation
    if args.iv:
        if args.encrypt:
            print("Warning: IV is generated automatically during encryption. Provided IV will be ignored.", 
                  file=sys.stderr)
        else:
            try:
                iv_bytes = bytes.fromhex(args.iv)
                if len(iv_bytes) != 16:
                    print("Error: IV must be 16 bytes (32 hex characters).", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print("Error: IV must be valid hex.", file=sys.stderr)
                sys.exit(1)

    # Auto output
    if args.output is None:
        if args.encrypt:
            args.output = args.input + ".enc"
        else:
            args.output = args.input + ".dec"

def _validate_hash_args(args):
    # Input file validation will happen in main
    pass

def _is_weak_key(key_bytes):
    # Check for all zeros
    if all(b == 0 for b in key_bytes):
        return True
    
    # Check for sequential bytes
    sequential_up = all(key_bytes[i] == (key_bytes[i-1] + 1) % 256 for i in range(1, len(key_bytes)))
    sequential_down = all(key_bytes[i] == (key_bytes[i-1] - 1) % 256 for i in range(1, len(key_bytes)))
    
    if sequential_up or sequential_down:
        return True
    
    # Check for repeated patterns
    if len(key_bytes) >= 4:
        # Check if key is all same byte
        if len(set(key_bytes)) == 1:
            return True
        
        # Check for simple repeating patterns
        for pattern_len in [2, 4, 8]:
            if len(key_bytes) % pattern_len == 0:
                pattern = key_bytes[:pattern_len]
                repeats_correct = all(key_bytes[i:i+pattern_len] == pattern 
                                    for i in range(pattern_len, len(key_bytes), pattern_len))
                if repeats_correct:
                    return True
    
    return False