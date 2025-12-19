import sys
import argparse

def create_simple_parser():
    parser = argparse.ArgumentParser(description='CryptoCore')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Derive command
    derive_parser = subparsers.add_parser('derive', help='Derive keys')
    derive_parser.add_argument('--password', required=True)
    derive_parser.add_argument('--salt')
    derive_parser.add_argument('--iterations', type=int, default=100000)
    derive_parser.add_argument('--length', type=int, default=32)
    
    return parser

def main():
    try:
        parser = create_simple_parser()
        args = parser.parse_args()
        
        if args.command == 'derive':
            # Простая реализация
            from cryptocore.kdf.pbkdf2 import pbkdf2_hmac_sha256
            from cryptocore.csprng import generate_random_bytes
            
            salt = args.salt.encode() if args.salt else generate_random_bytes(16)
            key = pbkdf2_hmac_sha256(args.password, salt, args.iterations, args.length)
            
            print(f"{key.hex()} {salt.hex()}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()