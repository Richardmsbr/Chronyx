# Security Guide

## Security Features Implemented

### 1. Input Validation
- Message length validation (1-2000 characters)
- Control character sanitization
- Prompt injection protection
- Context validation

### 2. Rate Limiting
- Configurable requests per minute per user
- Token bucket algorithm
- Clear error messages when limit is reached

### 3. Credential Protection
- API keys only in environment variables
- `.env` in `.gitignore`
- No hardcoded keys in code

## Secure Configuration

### Environment Variables

```bash
# .env
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Never commit this file!
```

### Using OpenAI

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
DEFAULT_MODEL=gpt-4-turbo
```

### Using Anthropic

```bash
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
DEFAULT_MODEL=claude-3-haiku-20240307
```

## Best Practices

### 1. Always use `.env` for secrets
```python
# Good
from config.settings import settings
api_key = settings.openai_api_key

# Bad
api_key = "sk-123456..."  # Never do this!
```

### 2. Validate all inputs
```python
# The system does this automatically
response = await agent.process_message(user_input)
```

### 3. Monitor API usage
```python
# Check remaining requests
remaining = agent.rate_limiter.get_remaining_requests(user_id)
print(f"Remaining requests: {remaining}")
```

## What NOT to Do

- **Never** commit `.env` files
- **Never** hardcode API keys in code
- **Never** share `.env` in messages/chat
- **Never** use same API key in multiple projects
- **Never** expose API keys in logs

## Security Audit Checklist

- [x] API keys protected
- [x] Input validation implemented
- [x] Rate limiting active
- [x] Sanitization against injection
- [x] `.env` in `.gitignore`
- [ ] Logging configured
- [ ] Monitoring implemented
- [ ] Security tests

## Report Vulnerabilities

If you find security vulnerabilities, **DO NOT** create a public issue.

Send email to: richardmsbr@gmail.com

## Key Rotation

Recommended to rotate API keys every:
- **30 days** - Production
- **90 days** - Development
- **Immediately** - If suspected exposure

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [OpenAI API Security](https://platform.openai.com/docs/guides/safety-best-practices)
