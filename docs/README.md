# Nostress Documentation

This directory contains the documentation source files for Nostress, built using [Sphinx](https://www.sphinx-doc.org/).

## Documentation Structure

```
docs/
├── README.md              # This file
├── conf.py                # Sphinx configuration
├── index.rst              # Main documentation index
├── installation.rst       # Installation guide
├── quickstart.rst         # Quick start guide
├── cli-reference.rst      # CLI command reference
├── api-reference.rst      # API documentation
├── architecture.rst       # Architecture overview
├── contributing.rst       # Contributing guide
├── _static/               # Static assets
└── _build/                # Generated documentation (created during build)
```

## Building Documentation

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Sphinx and documentation dependencies

### Quick Build

Build the documentation using direct uv commands:

```bash
# Install documentation dependencies (from project root)
uv sync --group docs

# Build HTML documentation
cd docs/
uv run sphinx-build -b html . _build/html
```

### Development Build with Live Reload

For live documentation development with auto-reload:

```bash
# Install dependencies first
uv sync --group docs

# Start live development server
cd docs/
uv run sphinx-autobuild . _build/html --open-browser --port 8888
```

This will start a development server at `http://localhost:8888` that automatically rebuilds when you make changes.

### CI/Production Build

For strict builds (used in CI and production) with warnings as errors:

```bash
# Install dependencies
uv sync --group docs

# Build with strict error checking
cd docs/
uv run sphinx-build -b html . _build/html -W --keep-going
```

### Additional Build Commands

```bash
# Check for broken links
cd docs/
uv run sphinx-build -b linkcheck . _build/linkcheck

# Clean build directory
cd docs/
rm -rf _build/

# Full clean rebuild
cd docs/
rm -rf _build/
uv run sphinx-build -b html . _build/html
```

## Read the Docs Integration

This project is configured for [Read the Docs](https://readthedocs.org/) automatic documentation building.

### Configuration Files

- `.readthedocs.yaml` - Main RTD configuration
- `pyproject.toml` - Documentation dependencies in `[dependency-groups.docs]`

### Setting Up Read the Docs

1. **Connect Repository**: Link your GitHub repository to Read the Docs
2. **Import Project**: Import the project in RTD dashboard
3. **Configure Build**: RTD will automatically detect the `.readthedocs.yaml` configuration
4. **Enable Webhooks**: RTD will set up GitHub webhooks for automatic builds

### Build Process

Read the Docs will:
1. Use Python 3.12 environment
2. Install `uv` package manager
3. Run `uv sync --group docs` to install documentation dependencies
4. Build documentation using Sphinx
5. Publish to your RTD subdomain

## Documentation Standards

### Writing Guidelines

- Use [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html) format
- Follow Google-style docstrings in code
- Include examples and code snippets where helpful
- Keep language clear and concise

### Code Documentation

- All public functions must have comprehensive docstrings
- Use type hints consistently
- Include examples in docstrings
- Document exceptions that functions may raise

### Adding New Documentation

1. Create new `.rst` files in the docs directory
2. Add entries to `index.rst` toctree
3. Reference new pages from existing documentation
4. Build locally to test formatting

## API Documentation

API documentation is automatically generated from code docstrings using Sphinx's `autodoc` extension.

### Updating API Docs

When you add new modules or functions:
1. Ensure they have proper docstrings
2. Add them to `api-reference.rst` if needed
3. Rebuild documentation to see changes

### Docstring Format

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    \"\"\"Brief description of the function.

    Longer description if needed.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Returns:
        Description of return value

    Raises:
        ValueError: When parameter is invalid

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    \"\"\"
    return True
```

## Troubleshooting

### Common Build Errors

**Import Errors**: Make sure all dependencies are installed with `uv sync --group docs`

**Sphinx Errors**: Check that all `.rst` files have valid reStructuredText syntax

**Missing Modules**: Ensure the nostress package is properly installed in the environment

**Permission Errors**: Make sure you have write access to the docs directory

### Clean Build

If you encounter issues, try a clean build:

```bash
cd docs/
rm -rf _build/
uv run sphinx-build -b html . _build/html
```

### Checking Documentation Quality

Run these commands to check documentation quality:

```bash
# Check for broken links
cd docs/
uv run sphinx-build -b linkcheck . _build/linkcheck

# Build with warnings as errors (CI mode)
cd docs/
uv run sphinx-build -b html . _build/html -W --keep-going

# Validate that essential files were created (run from docs/ directory)
test -f _build/html/index.html && \
test -f _build/html/api-reference.html && \
echo "✓ Documentation build validation passed"
```

All commands use uv and standard Python tools exclusively.

## Contributing to Documentation

Documentation improvements are always welcome! See `contributing.rst` for details on:

- Fixing typos and grammar
- Adding examples and tutorials
- Improving API documentation
- Creating new guides

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Read the Docs Guide](https://docs.readthedocs.io/)
- [Furo Theme Documentation](https://pradyunsg.me/furo/)
