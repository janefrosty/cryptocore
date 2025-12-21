import argparse
import sys
try:
    from cryptocore.kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt
except ImportError:
    from kdf.pbkdf2 import pbkdf2_hmac_sha256, generate_salt

def parse_arguments():
    """
    CLI argument parser for CryptoCore
    Sprint 1: Basic encryption arguments
    Sprint 2: Added mode and IV support
    Sprint 3: Made key optional for encryption, added weak key detection
    Sprint 4: Added subcommand structure (enc/dgst)
    Sprint 5: Added HMAC support with --hmac and --verify
    Sprint 6: Added GCM mode and AAD support
    """
    parser = argparse.ArgumentParser(
        description="CryptoCore - Cryptographic Tool Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Sprint 4: Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Encryption/decryption command (Sprints 1-3, 6)
    enc_parser = subparsers.add_parser('enc', help='Encryption/decryption operations')
    
    enc_parser.add_argument(
        "--algorithm", 
        required=True,
        help="Cryptographic algorithm to use"
    )
    
    # Sprint 2, 6: Extended mode support
    enc_parser.add_argument(
        "--mode", 
        required=True,
        choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr', 'gcm'],
        help="Block cipher mode of operation"
    )

    action_group = enc_parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--encrypt", action="store_true")
    action_group.add_argument("--decrypt", action="store_true")

    enc_parser.add_argument("--key", help="Encryption key as hexadecimal string (optional for encryption)")
    
    # Sprint 2: IV for traditional modes, Sprint 6: nonce for GCM
    enc_parser.add_argument("--iv", help="Initialization vector/nonce as hexadecimal string (for decryption)")
    enc_parser.add_argument("--nonce", help="Nonce for GCM mode (alternative to --iv)")
    
    # Sprint 6: AAD for GCM
    enc_parser.add_argument(
        "--aad", 
        help="Associated Authenticated Data as hexadecimal string (for GCM mode)"
    )
    
    enc_parser.add_argument("--input", required=True, help="Input file path")
    enc_parser.add_argument("--output", help="Output file path")
    
    # Hash/HMAC command (Sprints 4-5)
    hash_parser = subparsers.add_parser('dgst', help='Compute message digests and HMACs')
    
    hash_parser.add_argument(
        "--algorithm",
        required=True,
        choices=['sha256', 'sha3-256'],
        help="Hash algorithm to use"
    )
    
    # Sprint 5: HMAC options
    hash_parser.add_argument(
        "--hmac",
        action="store_true",
        help="Enable HMAC mode (requires --key)"
    )
    
    hash_parser.add_argument(
        "--key",
        help="Key for HMAC mode (hexadecimal string, required when --hmac is used)"
    )
    
    hash_parser.add_argument(
        "--verify",
        help="Verify HMAC against file containing expected value"
    )
    
    hash_parser.add_argument(
        "--input",
        required=True,
        help="Input file path"
    )
    
    hash_parser.add_argument(
        "--output",
        help="Output file for hash/HMAC (optional)"
    )

    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'enc':
        _validate_encryption_args(args)
    elif args.command == 'dgst':
        _validate_hash_args(args)
    
    return args

def _validate_encryption_args(args):

    if args.algorithm.lower() != "aes":
        print("Error: Only AES is supported for encryption.", file=sys.stderr)
        sys.exit(1)

    if args.encrypt == args.decrypt:
        print("Error: Choose exactly one: --encrypt or --decrypt", file=sys.stderr)
        sys.exit(1)

    # Sprint 3: Key validation - optional for encryption, required for decryption
    if args.key:
        try:
            key_bytes = bytes.fromhex(args.key)
            key_length = len(key_bytes)
            if key_length not in [16, 24, 32]:
                print("Error: AES key must be 16, 24, or 32 bytes.", file=sys.stderr)
                sys.exit(1)
            
            # Sprint 3: Weak key detection
            if _is_weak_key(key_bytes):
                print(f"Warning: The provided key may be weak.", file=sys.stderr)
                
        except ValueError:
            print("Error: Key must be valid hex.", file=sys.stderr)
            sys.exit(1)
    else:
        if args.decrypt:
            print("Error: Key is required for decryption operations.", file=sys.stderr)
            sys.exit(1)

    # Sprint 6: GCM specific validation
    if args.mode == 'gcm':
        if args.encrypt:
            if args.iv or args.nonce:
                print("Warning: Nonce is generated automatically during GCM encryption.", file=sys.stderr)
        else:
            if args.iv:
                try:
                    nonce_bytes = bytes.fromhex(args.iv)
                    if len(nonce_bytes) != 12:
                        print("Warning: GCM typically uses 12-byte nonce.", file=sys.stderr)
                except ValueError:
                    print("Error: Nonce must be valid hex.", file=sys.stderr)
                    sys.exit(1)
            elif args.nonce:
                try:
                    nonce_bytes = bytes.fromhex(args.nonce)
                    if len(nonce_bytes) != 12:
                        print("Warning: GCM typically uses 12-byte nonce.", file=sys.stderr)
                except ValueError:
                    print("Error: Nonce must be valid hex.", file=sys.stderr)
                    sys.exit(1)
    
    # Sprint 6: AAD validation
    if args.aad:
        if args.mode != 'gcm':
            print("Warning: AAD is only used with GCM mode.", file=sys.stderr)
        
        try:
            aad_bytes = bytes.fromhex(args.aad)
        except ValueError:
            print("Error: AAD must be valid hex.", file=sys.stderr)
            sys.exit(1)
    else:
        args.aad = ""

    if args.output is None:
        if args.encrypt:
            args.output = args.input + ".enc"
        else:
            args.output = args.input + ".dec"

def _validate_hash_args(args):

    if args.hmac:
        if not args.key:
            print("Error: --key is required when using --hmac", file=sys.stderr)
            sys.exit(1)
        
        try:
            key_bytes = bytes.fromhex(args.key)
            if len(key_bytes) == 0:
                print("Error: Key cannot be empty", file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print("Error: Key must be valid hexadecimal string", file=sys.stderr)
            sys.exit(1)
    
    if args.verify and not args.hmac:
        print("Error: --verify can only be used with --hmac", file=sys.stderr)
        sys.exit(1)

def _is_weak_key(key_bytes):

    if all(b == 0 for b in key_bytes):
        return True
    
    sequential_up = all(key_bytes[i] == (key_bytes[i-1] + 1) % 256 for i in range(1, len(key_bytes)))
    sequential_down = all(key_bytes[i] == (key_bytes[i-1] - 1) % 256 for i in range(1, len(key_bytes)))
    
    if sequential_up or sequential_down:
        return True
    
    if len(key_bytes) >= 4:
        if len(set(key_bytes)) == 1:
            return True
        
        for pattern_len in [2, 4, 8]:
            if len(key_bytes) % pattern_len == 0:
                pattern = key_bytes[:pattern_len]
                repeats_correct = all(key_bytes[i:i+pattern_len] == pattern 
                                    for i in range(pattern_len, len(key_bytes), pattern_len))
                if repeats_correct:
                    return True
    
    return False

def add_derive_subparser(subparsers):
    """Add derive command to CLI"""
    derive_parser = subparsers.add_parser(
        'derive',
        help='Derive keys from passwords or master keys'
    )
    
    # Группа для ввода пароля
    password_group = derive_parser.add_mutually_exclusive_group(required=True)
    password_group.add_argument(
        '--password',
        type=str,
        help='Password string (use quotes for special characters)'
    )
    password_group.add_argument(
        '--password-file',
        type=str,
        help='File containing password'
    )
    
    derive_parser.add_argument(
        '--salt',
        type=str,
        default=None,
        help='Salt as hexadecimal string (generated if not provided)'
    )
    
    derive_parser.add_argument(
        '--iterations',
        type=int,
        default=100000,
        help='Number of iterations (default: 100000)'
    )
    
    derive_parser.add_argument(
        '--length',
        type=int,
        default=32,
        help='Derived key length in bytes (default: 32)'
    )
    
    derive_parser.add_argument(
        '--algorithm',
        type=str,
        default='pbkdf2',
        choices=['pbkdf2'],
        help='KDF algorithm (default: pbkdf2)'
    )
    
    derive_parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file for derived key (binary format)'
    )
    
    derive_parser.add_argument(
        '--output-salt',
        type=str,
        default=None,
        help='Output file for salt (if generated)'
    )
    
    return derive_parser