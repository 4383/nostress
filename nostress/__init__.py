"""Nostress - Modern Python CLI for Nostr interactions.

Nostress provides a powerful, secure, and user-friendly command-line interface
for interacting with the Nostr protocol. Built with modern Python practices,
it emphasizes security, usability, and extensibility.

Key Features:
    - Secure key generation using cryptographically secure methods
    - Support for both hexadecimal and bech32 key formats
    - Rich terminal output with tables and colors
    - JSON output support for automation and scripting
    - Comprehensive input validation and error handling

Main Components:
    - CLI commands for key management
    - Core cryptographic operations
    - Utility functions for validation and formatting
    - Configuration management with XDG compliance

Example:
    Basic usage from command line:
        $ nostress keys generate
        $ nostress keys generate --format bech32 --verbose

    Programmatic usage:
        from nostress.core.models import NostrKeypair
        keypair = NostrKeypair.generate()
        print(f"Private: {keypair.private_key.hex}")
        print(f"Public: {keypair.public_key.bech32}")

For more information, visit the documentation or use:
    $ nostress --help
"""

try:
    from nostress._version import __version__
except ImportError:
    # Fallback version for development/editable installs
    __version__ = "0.0.0+dev"

__author__ = "nostress"
__description__ = (
    "Modern Python CLI for Nostr interactions - "
    "key generation, event creation, and relay management"
)
