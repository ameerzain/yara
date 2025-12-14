# Contributing to Yara

Thank you for your interest in contributing to Yara! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs if applicable

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and examples
- Potential implementation approach (if you have ideas)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add type hints to functions
   - Include docstrings
   - Write/update tests
4. **Test your changes**
   ```bash
   python backend/tests/test_chatbot.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: Description of your changes"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## Code Style

- Follow PEP 8 Python style guide
- Use type hints for function parameters and return types
- Add docstrings to modules, classes, and functions
- Keep functions focused and small
- Use meaningful variable and function names

## Testing

- Add tests for new features
- Ensure all existing tests pass
- Test edge cases and error conditions

## Documentation

- Update README.md if adding new features
- Update API documentation if changing endpoints
- Add comments for complex logic
- Update docstrings when modifying functions

## Questions?

Feel free to open an issue for any questions about contributing!

