"""Command-line interface implementations for nostress.

This package contains all CLI command implementations and utilities that
provide the user-facing interface for nostress. Built using Typer for
modern, type-safe command-line interface development.

Modules:
    base: Common CLI utilities and helper functions
    keys: Key management commands (generate, validate, convert)

Features:
    - Rich terminal output with tables and formatting
    - Type-safe command arguments and options
    - Comprehensive help and error messages
    - File input/output operations
    - Verbose mode support

Example:
    from nostress.cli.keys import generate_command

    # Commands are typically invoked through the main CLI app
    # but can also be used programmatically
"""
