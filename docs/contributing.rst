Contributing
============

Thank you for your interest in contributing to Nostress! This comprehensive guide will help you get started and be productive quickly.

How to Contribute
-----------------

There are many ways to contribute to Nostress:

- 🐛 **Report bugs** and issues
- 💡 **Suggest new features** and improvements
- 📖 **Improve documentation**
- 🧪 **Write tests** and improve coverage
- 💻 **Submit code** via pull requests
- 🗣️ **Spread the word** in the Nostr community

Getting Started
---------------

Development Setup
~~~~~~~~~~~~~~~~~

**1. Fork and clone the repository**::

    git clone https://github.com/yourusername/nostress.git
    cd nostress

**2. Set up development environment**::

    # Using uv (recommended) - installs all dev and test dependencies
    uv sync --group dev-test

    # Or using pip
    pip install -e ".[dev-test]"

**3. Install pre-commit hooks**::

    uv run pre-commit install

**4. Verify setup**::

    uv run nostress --help
    uv run pytest

Development Workflow
~~~~~~~~~~~~~~~~~~~~

**Daily development workflow:**

1. **Create a feature branch**::

    git checkout -b feature/your-feature-name

2. **Make your changes** following the coding standards below

3. **Run tests and linting**::

    # Quick check during development
    uv run pytest tests/unit/  # Fast unit tests
    uv run ruff check         # Linting

    # Before committing
    uv run pytest            # Full test suite
    uv run pre-commit run --all-files  # All quality checks

4. **Commit your changes**::

    git add .
    git commit -m "feat: add new feature description"

5. **Push and create a pull request**::

    git push origin feature/your-feature-name

Development Commands
--------------------

The project uses a **unified testing strategy** that avoids duplication between local development and CI/CD. All commands work identically locally and in CI.

Testing Commands
~~~~~~~~~~~~~~~~

**Available Commands:**

- ``uv run pytest`` - Run all tests (CI: ``pytest tests/ -v``)
- ``uv run pytest tests/unit/`` - Unit tests only (CI: ``pytest tests/unit/ -v``)
- ``uv run pytest tests/integration/`` - Integration tests only (CI: ``pytest tests/integration/ -v``)
- ``uv run pytest --cov=nostress`` - Tests with coverage (CI: ``pytest tests/ --cov=nostress``)
- ``uv run pytest --cov=nostress --cov-report=html`` - HTML coverage report (opens ``htmlcov/index.html``)

Code Quality Commands
~~~~~~~~~~~~~~~~~~~~~

**Available Commands:**

- ``uv run pre-commit run --all-files`` - All quality checks (CI: ``pre-commit run --all-files``)
- ``uv run ruff check`` - Linting only (CI: ``ruff check``)
- ``uv run ruff check --fix`` - Lint with auto-fix (CI: ``ruff check --fix``)
- ``uv run ruff format`` - Format code (CI: ``ruff format``)
- ``uv run ruff format --check`` - Check formatting only (CI: ``ruff format --check``)

CI Simulation Commands
~~~~~~~~~~~~~~~~~~~~~~

Run the exact same commands that run in CI:

.. code-block:: bash

    # Simulate lint job
    uv sync --group dev
    uv run pre-commit run --all-files

    # Simulate test job
    uv sync --group dev-test
    uv run pytest tests/unit/ -v --cov=nostress --cov-report=term-missing
    uv run pytest tests/integration/ -v

    # Simulate build job
    uv build

    # Simulate documentation build
    uv sync --group docs
    cd docs/
    uv run sphinx-build -b html . _build/html -W --keep-going

Testing Infrastructure
----------------------

Test Structure
~~~~~~~~~~~~~~

::

    tests/
    ├── conftest.py              # Shared fixtures and configuration
    ├── unit/                    # Fast, isolated unit tests
    │   └── test_crypto.py       # Cryptographic operations
    └── integration/             # CLI and end-to-end tests
        └── test_cli_keys.py     # Key management commands

Test Categories
~~~~~~~~~~~~~~~

- **Unit Tests** (``@pytest.mark.unit``): Fast, isolated component tests
- **Integration Tests** (``@pytest.mark.integration``): CLI and multi-component tests
- **CLI Tests** (``@pytest.mark.cli``): Command-line interface tests

Coverage Requirements
~~~~~~~~~~~~~~~~~~~~~

- **Minimum Coverage**: 30% (configured in ``pyproject.toml``)
- **Coverage Reports**: Terminal, HTML, and XML formats
- **CI Integration**: Coverage uploaded to Codecov

Pre-commit Hooks
~~~~~~~~~~~~~~~~

Pre-commit hooks run automatically before each commit:

**Code Quality:**
- **Ruff Linter**: Comprehensive Python linting (E, W, F, I, N, UP, B, C4, S, T20, SIM)
- **Ruff Formatter**: Consistent code formatting
- **Basic Hooks**: Trailing whitespace, EOF newlines, large files check

**File Validation:**
- **YAML/TOML Syntax**: Validates config files
- **Python AST**: Ensures valid Python syntax
- **Merge Conflicts**: Detects unresolved conflicts

**Security:**
- **Secrets Detection**: Scans for accidentally committed secrets

GitHub Actions CI Pipeline
---------------------------

The CI pipeline consists of parallel jobs that use the same tools as local development:

**1. Documentation Build** (``docs`` job)
    Builds documentation with Sphinx using strict error checking

**2. Code Quality** (``lint`` job)
    Runs the same pre-commit hooks as local development

**3. Test Suite** (``test`` job)
    - Runs pytest with coverage
    - Separates unit and integration tests
    - Uploads coverage reports to Codecov

**4. Build Package** (``build`` job)
    - Builds wheel and source distributions
    - Tests installation from built package
    - Uploads artifacts for other jobs

**5. CLI Integration** (``cli-integration`` job)
    - Tests actual CLI commands
    - Verifies end-to-end functionality
    - Uses built package from previous job

**6. Security Scan** (``security`` job)
    - Runs bandit for security analysis
    - Runs safety for dependency vulnerability checks

Code Standards
--------------

Coding Style
~~~~~~~~~~~~

Nostress follows modern Python coding standards:

- **Python 3.12+** features and syntax
- **Type hints** for all function parameters and returns
- **Google-style docstrings** for all public functions
- **Ruff** for linting and formatting
- **Black-compatible** formatting with double quotes

Example of proper code style:

.. code-block:: python

    def generate_keypair(format: KeyFormat = KeyFormat.HEX) -> NostrKeypair:
        """Generate a new Nostr keypair.

        Args:
            format: The output format for the keypair

        Returns:
            A new NostrKeypair instance

        Raises:
            CryptographicError: If key generation fails
        """
        try:
            return NostrKeypair.generate()
        except Exception as e:
            raise CryptographicError(f"Key generation failed: {e}") from e

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

All code must be thoroughly documented:

- **Module docstrings** explaining the module's purpose
- **Class docstrings** with clear descriptions
- **Function docstrings** with Args, Returns, and Raises sections
- **Type hints** for all parameters and return values
- **Inline comments** for complex logic

Testing Standards
~~~~~~~~~~~~~~~~~

All new code must include comprehensive tests:

- **Unit tests** for individual functions
- **Integration tests** for command interactions
- **Edge case testing** for error conditions
- **Property-based testing** for cryptographic functions

Minimum test coverage is 30%, but aim for higher coverage on new code.

Git Commit Standards
~~~~~~~~~~~~~~~~~~~~

Use conventional commit messages:

- ``feat: add new feature``
- ``fix: resolve bug in validation``
- ``docs: update API documentation``
- ``test: add tests for crypto module``
- ``refactor: simplify key generation logic``
- ``style: format code with ruff``

Reporting Issues
----------------

Bug Reports
~~~~~~~~~~~

When reporting bugs, please include:

1. **Description** of the problem
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **Environment details**:
   - Nostress version
   - Python version
   - Operating system
5. **Relevant logs** with ``--verbose`` output

Use this template::

    **Bug Description**
    Brief description of what went wrong.

    **Steps to Reproduce**
    1. Run command: `nostress keys generate --format bech32`
    2. Observe error message
    3. ...

    **Expected Behavior**
    Should generate a bech32 keypair successfully.

    **Actual Behavior**
    Error: KeyFormatError occurred.

    **Environment**
    - Nostress version: 0.1.0
    - Python version: 3.12.1
    - OS: Ubuntu 24.04

    **Additional Context**
    Include verbose output or relevant logs.

Feature Requests
~~~~~~~~~~~~~~~~

When suggesting features, please include:

1. **Use case** - Why is this feature needed?
2. **Proposed solution** - How should it work?
3. **Alternatives** - Other ways to solve the problem
4. **Additional context** - Examples, mockups, etc.

Pull Request Guidelines
-----------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. **Check existing issues** to avoid duplicating work
2. **Discuss large changes** in an issue first
3. **Run the full test suite** and ensure it passes
4. **Update documentation** for new features
5. **Add tests** for new functionality

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. **Create a clear title** describing the change
2. **Fill out the PR template** with all required information
3. **Link related issues** using "Fixes #123" or "Closes #456"
4. **Request review** from maintainers
5. **Address feedback** promptly and courteously

PR Description Template::

    ## Description
    Brief description of the changes made.

    ## Type of Change
    - [ ] Bug fix (non-breaking change)
    - [ ] New feature (non-breaking change)
    - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
    - [ ] Documentation update

    ## Testing
    - [ ] All existing tests pass
    - [ ] New tests added for new functionality
    - [ ] Manual testing completed

    ## Checklist
    - [ ] Code follows project style guidelines
    - [ ] Self-review of the code completed
    - [ ] Code is commented where necessary
    - [ ] Documentation updated where necessary

Development Guidelines
----------------------

Adding New Features
~~~~~~~~~~~~~~~~~~~

When adding new features:

1. **Start with tests** - Write tests first (TDD approach)
2. **Follow architecture** - Use existing patterns and layers
3. **Update documentation** - Include API docs and user guides
4. **Consider security** - Validate inputs and handle errors
5. **Test thoroughly** - Include edge cases and error conditions

Example workflow for adding a new command:

.. code-block:: bash

    # 1. Create tests
    touch tests/unit/test_new_feature.py
    touch tests/integration/test_cli_new_feature.py

    # 2. Implement feature
    touch nostress/cli/new_feature.py

    # 3. Register command
    # Edit nostress/main.py

    # 4. Run tests
    uv run pytest tests/ -v

    # 5. Update documentation
    # Edit docs/cli-reference.rst

Improving Documentation
~~~~~~~~~~~~~~~~~~~~~~~

Documentation improvements are always welcome:

1. **Fix typos** and grammatical errors
2. **Add examples** and usage scenarios
3. **Improve API documentation** with better docstrings
4. **Create tutorials** for common use cases
5. **Update architecture docs** when code changes

To build documentation locally::

    # Install docs dependencies
    uv sync --group docs

    # Build documentation
    cd docs/
    uv run sphinx-build -b html . _build/html

    # Live development with auto-reload
    uv run sphinx-autobuild . _build/html --open-browser --port 8888

Adding Tests
~~~~~~~~~~~~

Test coverage improvements help ensure reliability:

1. **Write unit tests** for new functions
2. **Add integration tests** for CLI commands
3. **Test error conditions** and edge cases
4. **Use property-based testing** for cryptographic functions
5. **Mock external dependencies** appropriately

Example test structure:

.. code-block:: python

    import pytest
    from nostress.core.models import NostrKeypair
    from nostress.exceptions import KeyFormatError

    class TestKeypairGeneration:
        """Test keypair generation functionality."""

        def test_generate_valid_keypair(self):
            """Test that keypair generation produces valid keys."""
            keypair = NostrKeypair.generate()

            assert len(keypair.private_key.hex) == 64
            assert len(keypair.public_key.hex) == 64
            assert keypair.private_key.bech32.startswith("nsec1")
            assert keypair.public_key.bech32.startswith("npub1")

        def test_invalid_private_key_raises_error(self):
            """Test that invalid private keys raise appropriate errors."""
            with pytest.raises(KeyFormatError):
                NostrPrivateKey.from_hex("invalid")

        @pytest.mark.parametrize("invalid_key", [
            "",
            "too_short",
            "not_hex_characters_xyz",
            "a" * 63,  # One character too short
            "a" * 65,  # One character too long
        ])
        def test_invalid_key_formats(self, invalid_key):
            """Test various invalid key formats."""
            with pytest.raises(KeyFormatError):
                NostrPrivateKey.from_hex(invalid_key)

Troubleshooting
---------------

Common Development Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

**Pre-commit hooks fail**::

    # Update hooks to latest versions
    uv run pre-commit autoupdate

    # Run specific hook
    uv run pre-commit run ruff --all-files

**Test failures**::

    # Run tests with verbose output
    uv run pytest -v

    # Run specific test file
    uv run pytest tests/unit/test_crypto.py -v

    # Run with pdb debugger
    uv run pytest tests/unit/test_crypto.py --pdb

**Coverage too low**::

    # Generate HTML report to see what's missing
    uv run pytest --cov=nostress --cov-report=html
    # Open htmlcov/index.html in browser

**CI/CD issues**::

    # Simulate exact CI environment locally
    # Check specific CI job locally
    uv sync --group dev
    uv run pre-commit run --all-files  # Same as CI lint job
    uv run pytest tests/ --cov=nostress  # Same as CI test job

Configuration Files
~~~~~~~~~~~~~~~~~~~

**Main Configuration:**
- ``pyproject.toml``: Project metadata, dependencies, tool configuration
- ``.pre-commit-config.yaml``: Code quality hooks (single source of truth)
- ``.github/workflows/ci.yml``: GitHub Actions CI pipeline

**Tool Configuration in pyproject.toml:**
- **pytest**: Test discovery, markers, coverage settings
- **ruff**: Linting and formatting rules
- **uv**: Development scripts for unified commands

Benefits of This Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **No Duplication**
   - Pre-commit configuration is used both locally and in CI
   - Same commands work locally and in GitHub Actions
   - Single source of truth for code quality rules

2. **Fast Feedback**
   - Pre-commit hooks catch issues before they reach CI
   - Local testing exactly matches CI behavior
   - Developer can simulate full CI pipeline locally

3. **Consistency**
   - All environments use the same tools and versions
   - Predictable behavior across development and production
   - Easy onboarding for new contributors

Security Considerations
-----------------------

When contributing to Nostress, security is paramount:

Security Guidelines
~~~~~~~~~~~~~~~~~~~

1. **Never commit secrets** - Use ``.gitignore`` and ``detect-secrets``
2. **Validate all inputs** - Use proper validation functions
3. **Handle errors securely** - Don't leak sensitive information
4. **Use secure defaults** - Choose safe default values
5. **Review crypto code carefully** - Extra scrutiny for cryptographic operations

Security Review Process
~~~~~~~~~~~~~~~~~~~~~~~

All cryptographic code changes require:

1. **Security-focused code review** by maintainers
2. **Test coverage** for security-relevant functionality
3. **Documentation** of security considerations
4. **Validation** of cryptographic correctness

Community
---------

Communication Channels
~~~~~~~~~~~~~~~~~~~~~~

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Nostr**: Connect with us on the decentralized network
- **Lightning**: Support development with lightning payments

Code of Conduct
~~~~~~~~~~~~~~~

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- **Be respectful** and professional in all interactions
- **Help newcomers** and answer questions patiently
- **Focus on constructive feedback** in code reviews
- **Celebrate contributions** from all community members
- **Report inappropriate behavior** to maintainers

Recognition
-----------

Contributors are recognized in several ways:

- **Contributor list** in README and documentation
- **Release notes** mentioning significant contributions
- **Lightning tips** for valuable contributions
- **Nostr mentions** celebrating community members

Getting Help
------------

If you need help with contributing:

1. **Check existing documentation** and examples
2. **Search issues** for similar questions
3. **Open a discussion** for general questions
4. **Ask in issues** for specific problems
5. **Reach out on Nostr** for community support

Development Environment Tips
----------------------------

IDE Setup
~~~~~~~~~

For the best development experience:

**VS Code**:
- Install Python extension
- Configure Ruff extension for linting
- Set up pytest integration
- Use type checking with Pylance

**PyCharm**:
- Configure Ruff as external tool
- Set up pytest as test runner
- Enable type checking
- Configure pre-commit hooks

Debugging
~~~~~~~~~

For debugging Nostress:

.. code-block:: python

    # Add verbose logging
    import os
    os.environ["NOSTRESS_VERBOSE"] = "1"

    # Use pdb for debugging
    import pdb; pdb.set_trace()

    # Test specific functions
    from nostress.core.models import NostrKeypair
    keypair = NostrKeypair.generate()

Performance Testing
~~~~~~~~~~~~~~~~~~~

To test performance improvements:

.. code-block:: python

    import time
    from nostress.core.models import NostrKeypair

    # Benchmark key generation
    start = time.time()
    for _ in range(1000):
        NostrKeypair.generate()
    end = time.time()

    print(f"Generated 1000 keypairs in {end - start:.2f} seconds")

Support the Project
-------------------

If you find Nostress valuable, consider supporting the project:

Lightning Support ⚡
~~~~~~~~~~~~~~~~~~~~

Support development with Lightning payments:

.. image:: _static/images/lightning.png
   :alt: Lightning Support QR Code
   :width: 200
   :align: center

Contact: ``hberaud@nostrcheck.me``

Connect on Nostr 🔗
~~~~~~~~~~~~~~~~~~~

Follow project updates on the decentralized Nostr network:

.. image:: _static/images/nostr.png
   :alt: Nostr Connection QR Code
   :width: 200
   :align: center

Thank you for contributing to Nostress! Your contributions help make Nostr more accessible to developers and users worldwide. 🚀
