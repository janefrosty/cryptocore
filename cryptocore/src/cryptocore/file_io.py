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
