from src.cryptocore.cli_parser import parse_arguments
from src.cryptocore.file_io import read_binary_file, write_binary_file
from modes.ecb import aes_ecb_encrypt, aes_ecb_decrypt

def main():
    args = parse_arguments()

    key = bytes.fromhex(args.key)
    data = read_binary_file(args.input)

    if args.encrypt:
        result = aes_ecb_encrypt(key, data)
    else:
        result = aes_ecb_decrypt(key, data)

    write_binary_file(args.output, result)
