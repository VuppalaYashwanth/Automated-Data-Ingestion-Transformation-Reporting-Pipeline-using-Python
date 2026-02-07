# Contributing to Market News Pipeline

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the Issues tab
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Your environment details (OS, Python version)

### Submitting Changes

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit your changes (`git commit -am 'Add some feature'`)
7. Push to the branch (`git push origin feature/your-feature-name`)
8. Create a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write descriptive commit messages

### Testing

Before submitting a PR:

```bash
# Test the demo
cd src
python demo.py

# Verify all modules work independently
python fetch_data.py
python clean_data.py
python store_data.py
python generate_report.py
```

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/market_news_pipeline.git
cd market_news_pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pytest black flake8
```

## Questions?

Feel free to open an issue for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
