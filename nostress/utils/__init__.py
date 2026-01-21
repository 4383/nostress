"""Utilities and helper functions for nostress.

This package contains utility modules that provide supporting functionality
across the nostress application, including validation, output formatting,
and configuration management.

Modules:
    config: Configuration management with XDG Base Directory compliance
    output: Rich formatting utilities for tables, JSON, and console output
    validation: Input validation functions with Typer integration

Features:
    - Type-safe input validation with clear error messages
    - Rich terminal formatting with tables and colors
    - JSON output support for automation and scripting
    - XDG-compliant configuration directory management
    - Cross-platform file system utilities

Example:
    from nostress.utils.output import format_keypair_table
    from nostress.utils.validation import validate_key_format

    # Format keypair for display
    table = format_keypair_table(private_key, public_key, "hex")

    # Validate user input
    format = validate_key_format("hex")
"""
