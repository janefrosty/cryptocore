# Contributing to CryptoCore

Thank you for considering contributing to CryptoCore!

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of cryptography

### Setting Up
1. Fork the repository on GitHub
2. Clone your fork locally:
   ```
   git clone https://github.com/YOUR-USERNAME/cryptocore.git
   cd cryptocore
   ```
3. Set up virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install in development mode:
   ```
   pip install -e .[dev]
   ```

## Development Process

### 1. Create a Branch
```
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
Follow the coding standards and testing requirements.

### 3. Test Your Changes
```
python tests/run_tests.py
```

### 4. Update Documentation
- Update `docs/API.md` if you changed public APIs
- Update `docs/USERGUIDE.md` if you changed CLI behavior
- Update `CHANGELOG.md` under `[Unreleased]` section

### 5. Commit Your Changes
Use descriptive commit messages.

### 6. Push and Create Pull Request
1. Push to your fork:
   ```
   git push origin feature/your-feature-name
   ```
2. Create Pull Request on GitHub
3. Describe your changes clearly

## What to Contribute
- Bug fixes
- New features aligned with project scope
- Documentation improvements
- Test cases
- Performance optimizations
