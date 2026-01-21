# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` for package management. Always use `uv run` when executing nostress commands during development.

### Installation and Setup

```bash
# Install in development mode
uv pip install -e .

# Verify installation
uv run nostress --help
uv run nostress keys generate
```

### Testing the CLI
```bash
# Test key generation in different formats
uv run nostress keys generate --format hex
uv run nostress keys generate --format bech32
uv run nostress keys generate --format both --verbose

# Test validation
uv run nostress keys validate <hex_key>
uv run nostress keys validate <bech32_key> --type nsec

# Test JSON output
uv run nostress keys generate --json
```

### Development Testing
```bash
# Test module imports
uv run python -c "from nostress.core import crypto, models; print('✓ Core imports work')"

# Test basic crypto operations
uv run python -c "
from nostress.core.models import NostrKeypair
keypair = NostrKeypair.generate()
print(f'Generated: {keypair.private_key.hex[:16]}...')
"
```

## Architecture Overview

Nostress is a modern Python CLI for Nostr protocol interactions built with a layered architecture:

### Core Architecture Layers

**CLI Layer** (`cli/`):
- `main.py` - Typer app entry point, registers command groups
- `cli/base.py` - Common CLI utilities (echo functions, password input, file handling)
- `cli/keys.py` - Key management commands (generate, validate, convert)

**Business Logic** (`core/`):
- `core/crypto.py` - Low-level cryptographic operations using cryptography library
- `core/models.py` - Pydantic models (NostrKeypair, NostrPrivateKey, NostrPublicKey)

**Utilities** (`utils/`):
- `utils/validation.py` - Input validation with typer-compatible validators
- `utils/output.py` - Rich formatting (tables, JSON, panels)
- `utils/config.py` - Configuration management with XDG compliance

**Infrastructure**:
- `exceptions.py` - Custom exception hierarchy (CryptographicError, KeyFormatError, etc.)

### Key Architectural Patterns

**Global State Management**: Uses environment variable `NOSTRESS_VERBOSE` to pass verbose mode between main callback and subcommands (due to Typer context limitations in current version).

**Data Flow**: User input → CLI parsing → validation → Pydantic models → crypto operations → output formatting → Rich console/file output.

**Error Handling**: Custom exception types bubble up to `main.py:handle_exception()` which provides user-friendly error messages with optional verbose traceback.

### Cryptographic Implementation

**Key Generation**:
- Private keys: 32 bytes from `secrets.token_bytes()` (cryptographically secure)
- Public keys: Derived via secp256k1 elliptic curve using `cryptography` library (x-coordinate only, 32 bytes)
- Validation: Comprehensive format checking for both hex and bech32

**Format Support**:
- HEX: Standard hexadecimal encoding
- Bech32: Uses base58 encoding with nsec/npub prefixes (simplified implementation, not true bech32)

**Security Notes**:
- Uses `cryptography` library for robust elliptic curve operations (more reliable than `secp256k1` package)
- Current bech32 implementation uses base58, not proper bech32 encoding. Comments in code acknowledge this as a simplified approach.

### Extension Points

**Adding New Commands**:
1. Create command module in `cli/`
2. Register with main app in `main.py` using `app.add_typer()`
3. Use existing utilities from `cli/base.py` and `utils/`

**Adding New Key Formats**:
1. Add to `KeyFormat` enum in `core/models.py`
2. Implement conversion functions in `core/crypto.py`
3. Update validation in `utils/validation.py`

**Adding Configuration Options**:
1. Add fields to `NostressConfig` dataclass in `utils/config.py`
2. Use `load_config()` in command implementations

### Dependencies

**Core Dependencies**:
- `typer` - CLI framework (no [all] extra due to compatibility)
- `rich` - Terminal formatting and output
- `cryptography` - Elliptic curve cryptography (secp256k1 support)
- `base58` - Encoding for bech32 format
- `pydantic` - Data validation and models

**Python Version**: Requires 3.12+ (specified in pyproject.toml)

## Important Implementation Details

### Verbose Mode Handling
Due to Typer version constraints, verbose mode is passed via `NOSTRESS_VERBOSE` environment variable rather than context. Commands should check:
```python
import os
verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"
```

### Output Patterns
- Use functions from `cli/base.py` for consistent messaging (`echo_success`, `echo_error`, etc.)
- Rich tables for verbose keypair display
- JSON output option for scripting
- File output with proper validation and overwrite confirmation

### Validation Strategy
- Pydantic models handle data validation at the type level
- `utils/validation.py` provides input validation with typer integration
- Custom exception types provide context-specific error handling

## Documentation Standards

**Documentation Requirements**: All runtime code must be thoroughly documented to enable automated documentation generation and maintain project knowledge. Documentation is not optional—it's a critical component of the development process.

### Documentation Guidelines

**Code Documentation Standards**:
- All public functions, classes, and methods must have comprehensive docstrings
- Use Google-style docstrings for consistency with Python ecosystem
- Include parameter types, return values, and usage examples
- Document exceptions that functions may raise
- Add inline comments for complex logic or business rules

**Documentation Synchronization**:
- Documentation must remain aligned with code at all times
- When updating functions: update corresponding docstrings immediately
- When removing features: remove related documentation sections
- When adding new functionality: document it before or during implementation
- Architecture changes must be reflected in this CLAUDE.md file

**Module-Level Documentation**:
- Each module should have a clear docstring explaining its purpose
- Document public APIs and their intended usage patterns
- Include examples for complex modules (crypto, validation)
- Maintain up-to-date type hints for all public interfaces

**Maintenance Workflow**:
1. **Before changes**: Review existing documentation for accuracy
2. **During development**: Write/update docstrings as code evolves
3. **After changes**: Verify all documentation reflects current implementation
4. **Code removal**: Delete corresponding documentation to prevent confusion

**Documentation Automation**:
- Prepare codebase for automated documentation generation tools (Sphinx, mkdocs)
- Maintain consistent formatting for API documentation extraction
- Use type hints extensively to support automated documentation tools
- Keep examples in docstrings simple and testable

## Testing Requirements

**Mandatory Testing**: Claude must run unit tests whenever working on code to ensure all functionality remains intact. Testing is a critical verification step that cannot be skipped.

### Testing Workflow

**Before Making Changes**:
- Run existing tests to establish baseline functionality
- Identify which tests cover the code being modified
- Verify current test suite passes completely

**During Development**:
- Run relevant tests frequently during implementation
- Add new tests for new functionality as it's developed
- Update existing tests when behavior changes intentionally

**After Making Changes**:
- Run full test suite to ensure no regressions
- Verify all new functionality is properly tested
- Fix any failing tests before considering work complete
- Run tests with different Python versions if applicable

### Testing Commands

**Current State**: No testing framework is currently implemented, but when tests exist, use:

```bash
# When pytest is implemented:
uv run pytest                    # Run all tests
uv run pytest tests/            # Run tests in specific directory
uv run pytest -v                # Verbose output
uv run pytest --coverage        # Run with coverage reporting

# Test specific modules when implemented:
uv run pytest tests/test_crypto.py
uv run pytest tests/test_models.py -v
```

### Testing Standards

**Test Coverage Requirements**:
- All public functions and methods must have corresponding tests
- Edge cases and error conditions must be tested
- Integration tests for CLI commands when framework is ready
- Cryptographic functions require comprehensive testing

**Test Organization**:
- Mirror source structure in tests/ directory
- Use descriptive test names that explain what is being tested
- Group related tests in test classes
- Include both positive and negative test cases

**Implementation Priority**: Implementing a robust testing framework (pytest recommended) should be a high priority for this project. Until then, Claude should:
1. Manually verify functionality through the Development Testing commands
2. Test CLI commands using the examples in this file
3. Validate changes don't break existing functionality

### Future Architecture Considerations
- **HIGH PRIORITY**: Testing framework implementation with pytest (required for reliable development)
- Configuration system ready for user preferences
- Command structure designed for easy addition of event and relay commands
- Modular design supports independent development of crypto, CLI, and utility components
- Documentation generation pipeline ready for implementation
- CI/CD pipeline integration once testing framework is established
