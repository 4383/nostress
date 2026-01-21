"""Core business logic for Nostr cryptographic operations.

This module contains the fundamental cryptographic functionality and data models
that power nostress. It provides secure key generation, format conversion, and
validation capabilities for the Nostr protocol.

Modules:
    crypto: Low-level cryptographic operations using the cryptography library
    models: Pydantic data models for keys and validation

Key Features:
    - Secure key generation using cryptographically secure random numbers
    - Support for both hexadecimal and bech32 key formats
    - Comprehensive input validation and error handling
    - Type-safe data models with automatic validation

Example:
    from nostress.core.models import NostrKeypair

    # Generate a new keypair
    keypair = NostrKeypair.generate()

    # Access keys in different formats
    private_hex = keypair.private_key.hex
    public_bech32 = keypair.public_key.bech32
"""
