import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="CryptoCore AES-128 ECB tool")

    parser.add_argument("--algorithm", required=True)
    parser.add_argument("--mode", required=True)

    parser.add_argument("--encrypt", action="store_true")
    parser.add_argument("--decrypt", action="store_true")

    parser.add_argument("--key", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")

    args = parser.parse_args()

    # Validate algorithm
    if args.algorithm.lower() != "aes":
        print("Error: Only AES is supported.", file=sys.stderr)
        sys.exit(1)

    # Validate mode
    if args.mode.lower() != "ecb":
        print("Error: Only ECB is supported.", file=sys.stderr)
        sys.exit(1)

    # Check for conflicting operations
    if args.encrypt == args.decrypt:
        print("Error: Choose exactly one: --encrypt or --decrypt", file=sys.stderr)
        sys.exit(1)

    # Key validation
    if len(args.key) != 32:
        print("Error: AES-128 key must be 16 bytes (32 hex characters).", file=sys.stderr)
        sys.exit(1)

    try:
        bytes.fromhex(args.key)
    except ValueError:
        print("Error: key must be valid hex.", file=sys.stderr)
        sys.exit(1)

    # Auto output
    if args.output is None:
        if args.encrypt:
            args.output = args.input + ".enc"
        else:
            args.output = args.input + ".dec"

    return args
