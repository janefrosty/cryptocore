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
        help="Block cipher mode of operation"
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--encrypt", action="store_true")
    action_group.add_argument("--decrypt", action="store_true")

    parser.add_argument("--key", required=True, help="Encryption key as hexadecimal string")
    parser.add_argument("--iv", help="Initialization vector as hexadecimal string (for decryption)")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Validate algorithm
    if args.algorithm.lower() != "aes":
        print("Error: Only AES is supported.", file=sys.stderr)
        sys.exit(1)

    # SPRINT 2: Extended mode support - ВАЖНО: убрана проверка на ECB!
    supported_modes = ['ecb', 'cbc', 'cfb', 'ofb', 'ctr']
    if args.mode.lower() not in supported_modes:
        print(f"Error: Supported modes are: {', '.join(supported_modes)}", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting operations
    if args.encrypt == args.decrypt:
        print("Error: Choose exactly one: --encrypt or --decrypt", file=sys.stderr)
        sys.exit(1)

    # Key validation
    try:
        key_bytes = bytes.fromhex(args.key)
        key_length = len(key_bytes)
        if key_length not in [16, 24, 32]:
            print("Error: AES key must be 16, 24, or 32 bytes (32, 48, or 64 hex characters).", file=sys.stderr)
            sys.exit(1)
    except ValueError:
        print("Error: Key must be valid hex.", file=sys.stderr)
        sys.exit(1)

    # SPRINT 2: IV validation
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