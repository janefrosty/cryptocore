import sys
import os

def read_binary_file(path):
    """
    Sprint 1: Basic file reading in binary mode
    """
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"File read error: {e}", file=sys.stderr)
        sys.exit(1)

def write_binary_file(path, data):
    """
    Sprint 1: Basic file writing in binary mode
    """
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        print(f"File write error: {e}", file=sys.stderr)
        sys.exit(1)

def read_file_with_iv(filename):
    """
    Sprint 2: Read file and extract IV from first 16 bytes
    For CBC, CFB, OFB, CTR modes
    """
    data = read_binary_file(filename)
    if len(data) < 16:
        raise ValueError("Input file is too short to contain IV")
    
    iv = data[:16]
    ciphertext = data[16:]
    return iv, ciphertext

def write_file_with_iv(filename, iv, data):
    """
    Sprint 2: Write IV followed by data to file
    File format: <16-byte IV><ciphertext bytes>
    """
    try:
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        with open(filename, "wb") as f:
            f.write(iv)
            f.write(data)
    except Exception as e:
        print(f"File write error: {e}", file=sys.stderr)
        sys.exit(1)