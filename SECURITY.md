# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in CryptoCore, please report it responsibly.

### How to Report
1. **DO NOT** create a public issue
2. Email security details to: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect
- We will acknowledge receipt within 48 hours
- We will investigate and provide updates
- We will coordinate public disclosure after fix is released

### Scope
This security policy applies to:
- The CryptoCore library source code
- Official documentation
- Release packages

### Out of Scope
- Third-party integrations
- User misconfiguration
- Feature requests

## Security Best Practices

### For Users
1. Always verify hashes/HMACs before trusting data
2. Use strong, randomly generated keys
3. Keep the library updated
4. Follow key management best practices

### For Developers
1. Never log or print sensitive data
2. Use cryptographically secure random number generation
3. Validate all inputs
4. Clear sensitive data from memory

## Security Considerations in Code

### Critical Requirements
- [ ] No secret keys logged or printed
- [ ] All random values from secure RNG
- [ ] Sensitive memory cleared after use
- [ ] Authentication before decryption
- [ ] Input validation on all user data
- [ ] Proper error handling without information leakage

## Updates
This policy may be updated as needed. Check back regularly for changes.

