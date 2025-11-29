# Contributing to Chronyx Community Edition

Thank you for considering contributing to Chronyx.

## This is a FREE Project

Chronyx Community Edition is **100% free and open source** under the MIT License.

- Anyone can use it
- Anyone can contribute
- Anyone can fork it
- No commercial restrictions

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

When reporting bugs, include:
- **Clear title** - Describe the issue concisely
- **Steps to reproduce** - How to trigger the bug
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - Python version, OS, etc.
- **Error messages** - Full stack trace if available

### Suggesting Features

We welcome feature suggestions. Please:
- Check existing feature requests first
- Explain the use case and benefits
- Describe how it should work
- Consider if it fits the Community Edition scope

**Note:** Advanced features may be reserved for Professional Edition.

### Pull Requests

#### Before You Start

1. **Open an issue** first to discuss major changes
2. **Check existing PRs** to avoid duplicate work
3. **Follow the code style** of the project
4. **Test your changes** thoroughly

#### Pull Request Process

1. **Fork the repository**
   ```bash
   git clone https://github.com/Richardmsbr/Chronyx.git
   cd Chronyx
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow Python PEP 8 style guide
   - Add docstrings to functions
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Run existing tests
   pytest

   # Test manually
   python cli.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Use a clear title and description
   - Reference any related issues
   - Explain what changes you made and why
   - Include screenshots if applicable

#### Code Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged
- You'll be added to contributors list

## Code Style Guidelines

### Python Code

```python
# Good
def process_message(message: str, context: Optional[Dict] = None) -> str:
    """
    Process user message with AI agent.

    Args:
        message: User input message
        context: Optional conversation context

    Returns:
        AI-generated response
    """
    # Implementation
    pass

# Bad
def process(msg, ctx=None):  # No types, no docstring
    pass
```

### Documentation

- Use clear, simple language
- Include code examples
- Keep README.md up to date

### Security

- **Never commit API keys or secrets**
- **Always validate user input**
- **Use environment variables** for configuration
- **Review security implications** of changes

## What to Contribute

### High Priority

- Bug fixes
- Documentation improvements
- Test coverage
- Internationalization (i18n)
- UI/UX improvements

### Medium Priority

- New agent templates
- Integration improvements
- Performance optimizations
- DevOps and tooling

### Low Priority

- Code refactoring
- Comment improvements
- Code cleanup

## What NOT to Contribute

- Professional Edition features (those are commercial)
- Breaking changes without discussion
- Code without tests (for core functionality)
- Uncommented complex code
- Non-essential dependencies

## Questions?

- Email: richardmsbr@gmail.com
- Issues: https://github.com/Richardmsbr/Chronyx/issues
- Discussions: https://github.com/Richardmsbr/Chronyx/discussions

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for helping make Chronyx better.**
