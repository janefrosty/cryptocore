import sys

def read_binary_file(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"File read error: {e}", file=sys.stderr)
        sys.exit(1)

def write_binary_file(path, data):
    try:
        with open(path, "wb") as f:
            f.write(data)
    except Exception as e:
        print(f"File write error: {e}", file=sys.stderr)
        sys.exit(1)

# SPRINT 2: New functions for IV handling
def read_file_with_iv(filename):
    """
    Read file and extract IV from first 16 bytes.
    Returns (iv, ciphertext)
    """
    data = read_binary_file(filename)
    if len(data) < 16:
        raise ValueError("Input file is too short to contain IV (less than 16 bytes)")
    
    iv = data[:16]
    ciphertext = data[16:]
    return iv, ciphertext

def write_file_with_iv(filename, iv, data):
    """
    Write IV followed by data to file
    """
    try:
        with open(filename, "wb") as f:
            f.write(iv)
            f.write(data)
    except Exception as e:
        print(f"File write error: {e}", file=sys.stderr)
        sys.exit(1)