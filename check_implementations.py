import os
import sys

def check_file(filepath):
    """Check what's in a file"""
    print(f"\n{'='*60}")
    print(f"Checking: {filepath}")
    print('='*60)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            print(content[:500])  # Print first 500 chars
            print("..." if len(content) > 500 else "")
    else:
        print("File does not exist!")

# Проверяем текущую структуру
base_path = "src/cryptocore"

files_to_check = [
    f"{base_path}/mac/hmac.py",
    f"{base_path}/mac/__init__.py",
    f"{base_path}/hash/sha256.py",
    f"{base_path}/hash/__init__.py",
]

for filepath in files_to_check:
    check_file(filepath)

# Проверим импорты
print(f"\n{'='*60}")
print("Testing imports...")
print('='*60)

try:
    sys.path.insert(0, 'src')
    import cryptocore.mac.hmac as hmac_module
    print("✓ Successfully imported hmac module")
    
    # Check what's available
    print(f"Available in hmac module: {[x for x in dir(hmac_module) if not x.startswith('_')]}")
except Exception as e:
    print(f"✗ Error importing hmac: {e}")

try:
    import cryptocore.hash.sha256 as sha256_module
    print("\n✓ Successfully imported sha256 module")
    print(f"Available in sha256 module: {[x for x in dir(sha256_module) if not x.startswith('_')]}")
except Exception as e:
    print(f"✗ Error importing sha256: {e}")