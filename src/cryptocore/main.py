import os
import sys
from .cli_parser import parse_arguments
from .file_io import read_binary_file, write_binary_file, read_file_with_iv, write_file_with_iv

# SPRINT 1 imports
from .modes.ecb import aes_ecb_encrypt, aes_ecb_decrypt

# SPRINT 2: New mode imports
from .modes.cbc import aes_cbc_encrypt, aes_cbc_decrypt
from .modes.cfb import aes_cfb_encrypt, aes_cfb_decrypt
from .modes.ofb import aes_ofb_encrypt, aes_ofb_decrypt
from .modes.ctr import aes_ctr_encrypt, aes_ctr_decrypt

# SPRINT 2: Mode function mapping
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

def main():
    try:
        args = parse_arguments()
        key = bytes.fromhex(args.key)
        
        # SPRINT 2: Extended mode handling
        if args.encrypt:
            if args.mode == 'ecb':
                # SPRINT 1: ECB mode (unchanged logic)
                data = read_binary_file(args.input)
                result = aes_ecb_encrypt(key, data)
                write_binary_file(args.output, result)
                print(f"Encryption successful. Output written to {args.output}")
            else:
                # SPRINT 2: New modes with IV
                data = read_binary_file(args.input)
                iv = os.urandom(16)  # Secure random IV
                encrypt_func = ENCRYPT_FUNCTIONS[args.mode]
                result = encrypt_func(key, data, iv)
                write_file_with_iv(args.output, iv, result)
                print(f"Encryption successful. Output written to {args.output}")
                print(f"IV (hex): {iv.hex()}")
        
        else:  # Decryption
            if args.mode == 'ecb':
                # SPRINT 1: ECB mode (unchanged logic)
                data = read_binary_file(args.input)
                result = aes_ecb_decrypt(key, data)
                write_binary_file(args.output, result)
                print(f"Decryption successful. Output written to {args.output}")
            else:
                # SPRINT 2: New modes with IV handling
                decrypt_func = DECRYPT_FUNCTIONS[args.mode]
                
                if args.iv:
                    # Use provided IV
                    iv = bytes.fromhex(args.iv)
                    data = read_binary_file(args.input)
                else:
                    # Read IV from file
                    iv, data = read_file_with_iv(args.input)
                
                result = decrypt_func(key, data, iv)
                write_binary_file(args.output, result)
                print(f"Decryption successful. Output written to {args.output}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)