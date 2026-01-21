"""Custom exceptions for nostress.

This module defines the exception hierarchy used throughout nostress for
consistent error handling and user feedback.

Exception Hierarchy:
    NostressError
    ├── CryptographicError
    ├── KeyFormatError
    ├── ValidationError
    └── ConfigurationError
"""


class NostressError(Exception):
    """Base exception for all nostress-specific errors.

    This is the root exception class from which all other nostress
    exceptions inherit. It provides a common base for catching any
    nostress-related error.

    Example:
        try:
            keypair = NostrKeypair.generate()
        except NostressError as e:
            print(f"Nostress error occurred: {e}")
    """

    pass


class CryptographicError(NostressError):
    """Error in cryptographic operations.

    Raised when cryptographic operations fail, such as:
    - Key generation failures
    - Invalid cryptographic parameters
    - Elliptic curve operation errors
    - Encoding/decoding failures in crypto contexts

    Example:
        try:
            public_key = derive_public_key(invalid_private_key)
        except CryptographicError as e:
            print(f"Crypto operation failed: {e}")
    """

    pass


class KeyFormatError(NostressError):
    """Error in key format validation.

    Raised when key strings are not properly formatted, such as:
    - Invalid hexadecimal characters in hex keys
    - Wrong key length (not 64 characters for hex)
    - Invalid bech32 prefixes (not nsec1.../npub1...)
    - Malformed bech32 encoding

    Example:
        try:
            key = NostrPrivateKey.from_hex("invalid_hex")
        except KeyFormatError as e:
            print(f"Invalid key format: {e}")
    """

    pass


class ValidationError(NostressError):
    """Error in input validation.

    Raised when user inputs fail validation, such as:
    - Invalid command-line arguments
    - File path validation failures
    - Parameter constraint violations
    - Type validation errors

    Example:
        try:
            validate_output_path("/invalid/path")
        except ValidationError as e:
            print(f"Validation failed: {e}")
    """

    pass


class ConfigurationError(NostressError):
    """Error in configuration management.

    Raised when configuration-related operations fail, such as:
    - Invalid configuration file format
    - Missing required configuration values
    - File system permission errors for config directories
    - XDG directory creation failures

    Example:
        try:
            config = load_config()
        except ConfigurationError as e:
            print(f"Configuration error: {e}")
    """

    pass
