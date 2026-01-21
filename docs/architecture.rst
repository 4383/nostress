Architecture
============

This document provides a comprehensive overview of Nostress's architecture,
design principles, and implementation details.

Overview
--------

Nostress is built with a clean, layered architecture that separates concerns
and provides a solid foundation for future extensions. The design follows
modern Python practices and emphasizes security, maintainability, and extensibility.

Architectural Layers
--------------------

The application is organized into distinct layers, each with specific responsibilities:

.. code-block:: text

    ┌─────────────────────────────────────┐
    │           CLI Layer                 │
    │  (User Interface & Commands)        │
    ├─────────────────────────────────────┤
    │        Business Logic              │
    │    (Core Models & Operations)       │
    ├─────────────────────────────────────┤
    │         Utilities                   │
    │  (Validation, Output, Config)       │
    ├─────────────────────────────────────┤
    │       Infrastructure               │
    │    (Exceptions & Base Types)        │
    └─────────────────────────────────────┘

CLI Layer
~~~~~~~~~

**Location**: ``nostress/cli/`` and ``nostress/main.py``

**Responsibilities**:
- Command-line interface implementation using Typer
- User input parsing and validation
- Command routing and execution
- Error handling and user feedback

**Key Components**:

- ``main.py`` - Typer app entry point, registers command groups
- ``cli/base.py`` - Common CLI utilities (echo functions, password input, file handling)
- ``cli/keys.py`` - Key management commands (generate, validate, convert)

**Design Patterns**:
- Command pattern for CLI operations
- Dependency injection for shared utilities
- Rich integration for enhanced terminal output

Business Logic Layer
~~~~~~~~~~~~~~~~~~~~

**Location**: ``nostress/core/``

**Responsibilities**:
- Core cryptographic operations
- Data models and business logic
- Key generation and validation
- Format conversion between hex and bech32

**Key Components**:

- ``core/crypto.py`` - Low-level cryptographic operations using cryptography library
- ``core/models.py`` - Pydantic models (NostrKeypair, NostrPrivateKey, NostrPublicKey)

**Security Principles**:
- Uses cryptographically secure random number generation
- Implements secp256k1 elliptic curve cryptography
- Validates all cryptographic operations
- No network dependencies for core operations

Utilities Layer
~~~~~~~~~~~~~~~

**Location**: ``nostress/utils/``

**Responsibilities**:
- Input validation with type-safe validators
- Output formatting and presentation
- Configuration management
- Cross-cutting concerns

**Key Components**:

- ``utils/validation.py`` - Input validation with typer-compatible validators
- ``utils/output.py`` - Rich formatting (tables, JSON, panels)
- ``utils/config.py`` - Configuration management with XDG compliance

Infrastructure Layer
~~~~~~~~~~~~~~~~~~~~

**Location**: ``nostress/exceptions.py``

**Responsibilities**:
- Custom exception hierarchy
- Error handling patterns
- Base types and interfaces

**Exception Hierarchy**:

.. code-block:: text

    NostrError
    ├── CryptographicError
    ├── KeyFormatError
    ├── ValidationError
    └── ConfigurationError

Data Flow
---------

The typical data flow through the application follows this pattern:

.. code-block:: text

    User Input → CLI Parsing → Validation → Pydantic Models
                     ↓
    Crypto Operations → Output Formatting → Rich Console/File Output

Example: Key Generation Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **User Input**: ``nostress keys generate --format bech32``
2. **CLI Parsing**: Typer parses command and options
3. **Validation**: Options are validated using utility validators
4. **Model Creation**: Pydantic models handle data structure
5. **Crypto Operations**: Secure key generation using cryptography library
6. **Output Formatting**: Rich tables or JSON formatting
7. **Display/Save**: Console output or file writing

Key Design Decisions
--------------------

Cryptographic Library Choice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Decision**: Use the ``cryptography`` library instead of ``secp256k1``

**Rationale**:
- More robust and widely maintained
- Better error handling and validation
- Consistent with security best practices
- Easier installation across platforms

Pydantic for Data Models
~~~~~~~~~~~~~~~~~~~~~~~~

**Decision**: Use Pydantic v2 for all data models

**Rationale**:
- Automatic validation and type checking
- Excellent JSON serialization support
- Clear error messages for invalid data
- Integration with type hints

Typer for CLI Framework
~~~~~~~~~~~~~~~~~~~~~~~

**Decision**: Use Typer without the ``[all]`` extra

**Rationale**:
- Clean, modern CLI API
- Automatic help generation
- Type hint integration
- Rich compatibility without extra dependencies

State Management
~~~~~~~~~~~~~~~~

**Decision**: Use environment variables for global state (verbose mode)

**Rationale**:
- Current Typer version limitations with context passing
- Simple and effective for CLI applications
- Easy to test and debug
- Minimal complexity

Configuration Management
------------------------

XDG Base Directory Compliance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nostress follows the XDG Base Directory Specification:

**Config Directory**: ``$XDG_CONFIG_HOME/nostress/`` or ``~/.config/nostress/``
- User configuration files
- Application preferences
- Custom settings

**Data Directory**: ``$XDG_DATA_HOME/nostress/`` or ``~/.local/share/nostress/``
- Application data
- Generated files
- Persistent storage

**Cache Directory**: ``$XDG_CACHE_HOME/nostress/`` or ``~/.cache/nostress/``
- Temporary files
- Download cache
- Build artifacts

Configuration Structure
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @dataclass
    class NostressConfig:
        """Configuration settings for Nostress."""

        # Output preferences
        default_format: KeyFormat = KeyFormat.HEX
        verbose_by_default: bool = False

        # Security settings
        require_encryption: bool = False
        secure_deletion: bool = True

        # UI preferences
        color_output: bool = True
        table_style: str = "rounded"

Error Handling Strategy
-----------------------

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

All errors inherit from ``NostrError``, providing a clear hierarchy:

- ``CryptographicError``: Key generation or validation failures
- ``KeyFormatError``: Invalid key formats or encoding issues
- ``ValidationError``: Input validation failures
- ``ConfigurationError``: Configuration and file system issues

Error Recovery
~~~~~~~~~~~~~~

The application implements graceful error recovery:

1. **User-friendly messages**: Technical errors are translated to user-friendly descriptions
2. **Verbose mode**: Detailed error information available with ``--verbose``
3. **Exit codes**: Standard exit codes for script integration
4. **Validation**: Early validation prevents downstream errors

Security Architecture
---------------------

Key Generation Security
~~~~~~~~~~~~~~~~~~~~~~~

- Uses ``secrets.token_bytes()`` for cryptographically secure random generation
- Implements proper secp256k1 curve operations
- No dependencies on external services or network
- Secure memory handling where possible

Input Validation
~~~~~~~~~~~~~~~~

- All user inputs are validated before processing
- Type checking at runtime using Pydantic
- Format validation for key strings
- Path validation for file operations

File Operations
~~~~~~~~~~~~~~~

- Secure file permissions when writing keys
- Optional encryption for sensitive data
- Atomic file operations to prevent corruption
- Proper cleanup of temporary files

Extension Points
----------------

Adding New Commands
~~~~~~~~~~~~~~~~~~~

To add new command groups:

1. Create a new module in ``nostress/cli/``
2. Implement commands using Typer decorators
3. Register with the main app in ``main.py``
4. Use existing utilities from ``cli/base.py``

Example:

.. code-block:: python

    # nostress/cli/events.py
    import typer
    from nostress.cli.base import echo_success

    app = typer.Typer(name="events", help="Event operations")

    @app.command()
    def create():
        """Create a new Nostr event."""
        echo_success("Event created successfully")

    # nostress/main.py
    from nostress.cli.events import app as events_app
    main_app.add_typer(events_app)

Adding New Key Formats
~~~~~~~~~~~~~~~~~~~~~~

To support additional key formats:

1. Add to ``KeyFormat`` enum in ``core/models.py``
2. Implement conversion functions in ``core/crypto.py``
3. Update validation in ``utils/validation.py``
4. Add tests for the new format

Adding Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add new configuration options:

1. Add fields to ``NostressConfig`` dataclass
2. Update ``load_config()`` function
3. Use configuration in relevant commands
4. Add validation for new options

Testing Architecture
--------------------

Test Organization
~~~~~~~~~~~~~~~~~

- **Unit tests**: ``tests/unit/`` - Test individual modules
- **Integration tests**: ``tests/integration/`` - Test command interactions
- **CLI tests**: Test command-line interface behavior
- **Crypto tests**: Comprehensive cryptographic operation testing

Test Patterns
~~~~~~~~~~~~~

- Pytest fixtures for common test data
- Mock external dependencies
- Property-based testing for cryptographic functions
- Comprehensive edge case coverage

Performance Considerations
--------------------------

Key Generation Performance
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Optimized for single key generation (common use case)
- Minimal memory allocation during crypto operations
- Efficient format conversion between hex and bech32
- No unnecessary computation in critical paths

Memory Management
~~~~~~~~~~~~~~~~~

- Minimal memory footprint for CLI operations
- Secure cleanup of sensitive data where possible
- Efficient string handling for key formats
- Stream processing for future file operations

Future Architecture
-------------------

Planned Enhancements
~~~~~~~~~~~~~~~~~~~~

**Event Management** (v0.2.x):
- Event creation and signing
- JSON event serialization
- Event validation and verification

**Relay Integration** (v0.3.x):
- WebSocket connections to Nostr relays
- Event publishing and querying
- Subscription management

**Advanced Features** (v1.0+):
- Multi-signature support
- Hardware wallet integration
- Plugin architecture for extensions
- Web interface companion

Compatibility Strategy
~~~~~~~~~~~~~~~~~~~~~~

- Maintain backward compatibility for CLI interfaces
- Use feature flags for experimental functionality
- Deprecation warnings for legacy features
- Clear migration paths for breaking changes

Monitoring and Observability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Structured logging for operations
- Performance metrics collection
- Error reporting and analysis
- User feedback integration

This architecture provides a solid foundation for current functionality
while being flexible enough to support the planned roadmap of features.
