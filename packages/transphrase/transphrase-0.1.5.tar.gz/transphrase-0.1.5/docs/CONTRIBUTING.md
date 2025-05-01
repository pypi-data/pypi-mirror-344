# Contributing to TransPhrase

Thank you for considering contributing to TransPhrase! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Development Environment Setup

### Prerequisites
- Python 3.10 or higher
- Git
- pip

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/TransPhrase.git
   cd TransPhrase
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

5. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

## Project Structure

TransPhrase is structured as follows:

```
transphrase/
├── api/              # API interaction logic
├── cache/            # Translation caching implementation
├── cli/              # Command-line interface
├── core/             # Core application logic
│   ├── config.py     # Configuration classes and default values
│   ├── container.py  # Dependency injection container
│   ├── context_tracker.py  # Context tracking for translations
│   ├── file_processor.py   # File processing operations
│   └── text_processing.py  # Text chunking and processing
├── database/         # Database models and operations
├── plugins/          # Plugin system implementation
├── rate_limiting/    # Rate limiting implementation
└── ui/               # User interface components
```

## Development Workflow

1. **Create a new branch** for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the [coding standards](#coding-standards)

3. **Run tests** to ensure your changes don't break existing functionality
   ```bash
   pytest
   ```

4. **Check code quality**
   ```bash
   black transphrase
   isort transphrase
   ruff transphrase
   mypy transphrase
   ```

5. **Commit your changes** with clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

## Coding Standards

TransPhrase follows these coding standards:

### Python Style Guide
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Sort imports with [isort](https://pycqa.github.io/isort/)
- Use type hints for all function parameters and return values

### Docstrings
- Use Google-style docstrings for all modules, classes, and functions
- Example:
  ```python
  def translate_chunk(self, prompt: str, text: str, model: str) -> str:
      """
      Translate a chunk of text using the specified model.

      Args:
          prompt: The system prompt for translation
          text: The text to translate
          model: The model ID to use

      Returns:
          The translated text

      Raises:
          APIError: If the API request fails
      """
  ```

### Error Handling
- Use specific exception types instead of bare `except` clauses
- Log exceptions with appropriate severity levels
- Provide helpful error messages for users

## Testing

TransPhrase uses pytest for testing. All code should have appropriate test coverage.

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=transphrase

# Run specific test file
pytest tests/test_file_processor.py
```

### Writing Tests
- Place tests in the tests directory
- Name test files with `test_` prefix
- Use descriptive test function names that explain what they're testing
- Use fixtures for common test setups
- Example:
  ```python
  def test_context_tracker_updates_name_frequencies():
      """Test that the context tracker properly updates name frequencies."""
      tracker = ContextTracker("job1", "Chinese", "English", "model1", "series1")
      tracker.start_file(Path("test.txt"))

      # Test with a name that appears in the text
      tracker.update_context("原文", "John went to the store. John bought an apple.")

      assert "John" in tracker.name_frequencies
      assert tracker.name_frequencies["John"] == 2
  ```

## Documentation

- Update documentation when adding or changing features
- Keep README.md up to date with current features and usage
- Add docstrings for all public classes and methods
- Add explanatory comments for complex code sections

## Submitting Changes

1. **Push your changes** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** from your fork to the main repository
   - Provide a clear title and description
   - Reference any related issues using #issue-number
   - Explain what your changes do and why they should be included

3. **Respond to code review feedback** if requested

4. **Update your PR** if needed by pushing additional commits to your branch

## Feature Requests and Bug Reports

- Use the GitHub Issues system to report bugs or request features
- Provide detailed information for bug reports:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Error messages and logs if applicable
  - Environment information (OS, Python version, etc.)

Thank you for contributing to TransPhrase!
