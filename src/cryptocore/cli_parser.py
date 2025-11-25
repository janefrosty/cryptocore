import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CryptoCore - AES Encryption/Decryption Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--algorithm", 
        required=True,
        help="Cryptographic algorithm to use"
    )
    
    parser.add_argument(
        "--mode", 
        required=True,
        choices=['ecb', 'cbc', 'cfb', 'ofb', 'ctr'],
        help="Block cipher mode of operation"
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--encrypt", action="store_true")
    action_group.add_argument("--decrypt", action="store_true")

    parser.add_argument("--key", help="Encryption key as hexadecimal string (optional for encryption)")
    parser.add_argument("--iv", help="Initialization vector as hexadecimal string (for decryption)")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Validate algorithm
    if args.algorithm.lower() != "aes":
        print("Error: Only AES is supported.", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting operations
    if args.encrypt == args.decrypt:
        print("Error: Choose exactly one: --encrypt or --decrypt", file=sys.stderr)
        sys.exit(1)

    # SPRINT 3: Key validation - optional for encryption, required for decryption
    if args.key:
        try:
            key_bytes = bytes.fromhex(args.key)
            key_length = len(key_bytes)
            if key_length not in [16, 24, 32]:
                print("Error: AES key must be 16, 24, or 32 bytes (32, 48, or 64 hex characters).", file=sys.stderr)
                sys.exit(1)
            
            # SPRINT 3: Check for weak keys
            if _is_weak_key(key_bytes):
                print(f"Warning: The provided key may be weak. Consider using a randomly generated key.", file=sys.stderr)
                
        except ValueError:
            print("Error: Key must be valid hex.", file=sys.stderr)
            sys.exit(1)
    else:
        # SPRINT 3: Key is optional for encryption, required for decryption
        if args.decrypt:
            print("Error: Key is required for decryption operations.", file=sys.stderr)
            sys.exit(1)

    # SPRINT 3: IV validation
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

    return args

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