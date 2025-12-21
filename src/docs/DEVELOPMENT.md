# CryptoCore Development Guide

## Table of Contents
1. Development Setup
2. Project Structure
3. Coding Standards
4. Testing
5. Adding New Features
6. Release Process

## 1. Development Setup

### 1.1 Clone Repository
```
git clone <repository-url>
cd cryptocore
```

### 1.2 Create Virtual Environment
```
python -m venv venv
# Windows: venv\Scripts\activate
# Unix/Mac: source venv/bin/activate
```

### 1.3 Install Dependencies
```
pip install -e .
pip install pytest pytest-cov
```

### 1.4 Verify Setup
```
python -m pytest tests/unit/test_hash_functions.py -v
```

## 2. Project Structure

```
cryptocore/
├── src/
│   ├── hash/              # Hash functions
│   ├── kdf/               # Key derivation functions
│   ├── mac/               # MAC functions
│   └── modes/             # CLI and utilities
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   ├── vectors/          # Test vectors
│   └── run_tests.py      # Test runner
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
├── setup.py              # Package config
└── README.md             # Overview
```

## 3. Coding Standards

### 3.1 Python Style
- Follow PEP 8
- Maximum line length: 100 characters
- Use snake_case for functions/variables
- Use type hints for all functions

### 3.2 Documentation
Every public function must have a Google-style docstring:

```python
def function(arg1: str, arg2: int) -> bool:
    """Short description.
    
    Args:
        arg1: Description of arg1.
        arg2: Description of arg2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When something goes wrong.
    """
```

### 3.3 Imports Order
1. Standard library imports
2. Third-party imports
3. Local application imports

### 3.4 Error Handling
- Use specific exceptions (ValueError, TypeError, IOError)
- Print errors to stderr in CLI
- Never expose sensitive information in error messages

### 3.5 Security
- Clear sensitive data from memory
- Use constant-time comparisons for MAC verification
- Validate all inputs

## 4. Testing

### 4.1 Running Tests
**Run all tests:**
```
python tests/run_tests.py
```

**Run with pytest:**
```
pytest tests/ -v
```

**Test coverage:**
```
pytest tests/ --cov=src --cov-report=html
```

### 4.2 Test Structure
- **Unit tests**: Test individual functions
- **Integration tests**: Test CLI commands
- **Test vectors**: Official NIST/RFC vectors

### 4.3 Example Test
```python
import unittest
from cryptocore.hash import sha256

class TestSHA256(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(
            sha256(b"").hex(),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
```

## 5. Adding New Features

### 5.1 Steps
1. Create/modify source files in `src/`
2. Add comprehensive tests in `tests/`
3. Update documentation:
   - Add to `docs/API.md` (if public API)
   - Add examples to `docs/USERGUIDE.md`
4. Update `__init__.py` files

### 5.2 Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added
- [ ] Documentation updated
- [ ] No security issues introduced

## 6. Release Process

### 6.1 Versioning
Follow Semantic Versioning (SemVer):
- MAJOR: Incompatible API changes
- MINOR: New functionality
- PATCH: Bug fixes

### 6.2 Release Steps
1. Update version in `setup.py` and `docs/API.md`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create release commit:
   ```
   git add .
   git commit -m "Release vX.Y.Z"
   git tag -a vX.Y.Z -m "Version X.Y.Z"
   ```
5. Push:
   ```
   git push origin main --tags
   ```
