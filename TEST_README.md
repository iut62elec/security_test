# Security Scanner Test Suite

Intentionally **vulnerable** and **clean** code to test security scanning tools.

## Structure

```
vulnerable/                  # Should be FLAGGED
  user_service.py           # Python - 15+ vulnerabilities
  api_handler.js            # JavaScript - 12+ vulnerabilities
  DataAccessLayer.java      # Java - 10+ vulnerabilities

clean/                       # Should PASS
  user_service_secure.py    # Python - secure patterns
  api_handler_secure.js     # JavaScript - secure patterns
```

## Vulnerability Coverage (11 categories)

| Category | Vuln Count | Languages |
|----------|-----------|-----------|
| SQL Injection | 8 | Python, JS, Java |
| Command Injection | 6 | Python, JS, Java |
| Hardcoded Secrets | 12+ | Python, JS, Java |
| Path Traversal | 4 | Python, JS, Java |
| XSS (Reflected) | 2 | JS |
| SSRF | 3 | Python, Java |
| Insecure Deserialization | 3 | Python, JS, Java |
| Weak Cryptography | 3 | Python, Java |
| XXE | 2 | Python, Java |
| Code Injection (eval) | 2 | Python |
| Missing Auth/AuthZ | 3 | Python, JS |

## Expected Results

A good scanner should find **~47 findings** in `vulnerable/` and **0** in `clean/`.

---
*Test suite v3 - rescan after timeout fix deployment*
