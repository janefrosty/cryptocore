import os
import sys
from .kdf.pbkdf2 import pbkdf2_hmac_sha256
from .kdf.hkdf import derive_key
from .csprng import generate_random_bytes

def perform_derive(args):
    try:
        # Read password
        password = read_password(args)
        
        # Get or generate salt
        salt = get_salt(args)
        
        # Perform derivation
        if args.algorithm == 'pbkdf2':
            derived_key = pbkdf2_hmac_sha256(
                password, 
                salt, 
                args.iterations, 
                args.length
            )
        
        # Output results
        output_results(derived_key, salt, args)
        
        # Clear sensitive data
        clear_sensitive_data(password, derived_key)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def read_password(args):
    """Read password from command line or file."""
    if args.password:
        return args.password
    elif args.password_file:
        try:
            with open(args.password_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: Password file '{args.password_file}' not found", 
                  file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: No password source specified", file=sys.stderr)
        sys.exit(1)

def get_salt(args):
    """Get salt from args or generate random."""
    if args.salt:
        try:
            return bytes.fromhex(args.salt)
        except ValueError:
            print("Error: Salt must be a valid hexadecimal string", 
                  file=sys.stderr)
            sys.exit(1)
    else:
        # Generate random 16-byte salt
        return generate_random_bytes(16)

def output_results(derived_key, salt, args):
    """Output derived key and salt."""
    key_hex = derived_key.hex()
    salt_hex = salt.hex()
    
    # Print to stdout
    print(f"{key_hex} {salt_hex}")
    
    # Write to output file if specified
    if args.output:
        try:
            with open(args.output, 'wb') as f:
                f.write(derived_key)
            print(f"Key written to: {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
    
    # Write salt to separate file if requested
    if args.output_salt:
        try:
            with open(args.output_salt, 'wb') as f:
                f.write(salt)
            print(f"Salt written to: {args.output_salt}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing salt to file: {e}", file=sys.stderr)

def clear_sensitive_data(*data_items):
    """Attempt to clear sensitive data from memory."""
    for data in data_items:
        if isinstance(data, (bytes, bytearray)):
            # Overwrite with zeros
            for i in range(len(data)):
                data = None