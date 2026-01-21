# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-01-21

### Added

**Core Foundation**
- Modern Python CLI framework built with Typer and Rich for elegant terminal interactions
- Comprehensive project structure with clear separation of concerns (CLI, core, utils)
- Production-ready configuration with pyproject.toml using modern Python tooling (uv, hatch-vcs)

**Key Management Features**
- Secure cryptographic key generation using the `cryptography` library with secp256k1 support
- Multi-format key support (HEX and Bech32) with automatic validation
- Key conversion utilities between different formats
- Comprehensive key validation with detailed error reporting
- File output capabilities with encryption support and overwrite protection

**Lightning Integration**
- Tips and sponsorship system with Lightning address support
- Nostr public key display and management
- Rich terminal formatting for tip information with QR code support
- JSON output format for scripting and automation

**Development Infrastructure**
- Comprehensive testing framework with pytest, including unit and integration tests
- Pre-commit hooks with ruff (formatting/linting), YAML validation, and security scanning
- Automated secret detection with detect-secrets and proper allowlisting
- Code coverage reporting and quality gates

**CI/CD Pipeline**
- GitHub Actions workflow with multi-stage validation (lint, test, build, security)
- Automated PyPI publishing on tag creation (no "v" prefix required)
- Trusted publishing setup with secure token-less deployment
- Cross-environment testing and CLI integration validation
- Artifact management and build verification

**Documentation**
- Sphinx documentation framework with Read the Docs integration
- Comprehensive API reference and CLI command documentation
- Installation guide, quickstart tutorial, and contribution guidelines
- Architecture documentation with clear development patterns

**Security & Quality**
- Security scanning with Bandit and safety checks
- Comprehensive error handling with custom exception hierarchy
- Input validation and sanitization throughout the application
- Secure defaults and protection against common vulnerabilities

**Developer Experience**
- Rich CLI help system with contextual guidance
- Verbose mode support for debugging and detailed output
- Consistent error messaging and user feedback
- Modern Python features with type hints and Pydantic models

### Technical Details
- **Python**: Requires 3.12+ for modern language features
- **Dependencies**: Typer, Rich, Cryptography, Pydantic, Base58
- **Build System**: Hatch with VCS versioning for automatic version management
- **Package Manager**: UV for fast, reliable dependency management
- **Testing**: Pytest with coverage reporting and integration tests
- **Linting**: Ruff for fast, comprehensive code quality checks
- **Security**: Multi-layered security scanning and validation

[unreleased]: https://github.com/4383/nostress/compare/0.1.0...HEAD
[0.1.0]: https://github.com/4383/nostress/releases/tag/0.1.0
