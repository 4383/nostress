API Reference
=============

This section provides comprehensive API documentation for all Nostress modules,
automatically generated from docstrings in the source code.

Overview
--------

Nostress is organized into several main modules:

- :mod:`nostress.core` - Core cryptographic functionality and data models
- :mod:`nostress.cli` - Command-line interface implementations
- :mod:`nostress.utils` - Utility functions for validation, output, and configuration
- :mod:`nostress.exceptions` - Custom exception classes

Core Module
-----------

The core module contains the fundamental cryptographic operations and data models.

.. automodule:: nostress.core
   :members:
   :undoc-members:
   :show-inheritance:

Cryptographic Operations
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: nostress.core.crypto
   :members:
   :undoc-members:
   :show-inheritance:

Data Models
~~~~~~~~~~~

.. automodule:: nostress.core.models
   :members:
   :undoc-members:
   :show-inheritance:

CLI Module
----------

The CLI module contains the command-line interface implementations.

.. automodule:: nostress.cli
   :members:
   :undoc-members:
   :show-inheritance:

Base CLI Utilities
~~~~~~~~~~~~~~~~~~

.. automodule:: nostress.cli.base
   :members:
   :undoc-members:
   :show-inheritance:

Key Management Commands
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: nostress.cli.keys
   :members:
   :undoc-members:
   :show-inheritance:

Utilities Module
----------------

The utils module provides supporting functionality for validation, output formatting,
and configuration management.

.. automodule:: nostress.utils
   :members:
   :undoc-members:
   :show-inheritance:

Output Formatting
~~~~~~~~~~~~~~~~~

.. automodule:: nostress.utils.output
   :members:
   :undoc-members:
   :show-inheritance:

Input Validation
~~~~~~~~~~~~~~~~

.. automodule:: nostress.utils.validation
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: nostress.utils.config
   :members:
   :undoc-members:
   :show-inheritance:

Exception Classes
-----------------

.. automodule:: nostress.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Main Entry Point
----------------

.. automodule:: nostress.main
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

Basic Usage Examples
~~~~~~~~~~~~~~~~~~~~

Generate a keypair programmatically:

.. code-block:: python

    from nostress.core.models import NostrKeypair

    # Generate a new keypair
    keypair = NostrKeypair.generate()

    # Access the keys
    private_hex = keypair.private_key.hex
    public_hex = keypair.public_key.hex
    private_bech32 = keypair.private_key.bech32
    public_bech32 = keypair.public_key.bech32

    print(f"Private (hex): {private_hex}")
    print(f"Public (bech32): {public_bech32}")

Validate keys:

.. code-block:: python

    from nostress.core.models import NostrPrivateKey, NostrPublicKey
    from nostress.exceptions import KeyFormatError

    try:
        # Validate a hex private key
        private_key = NostrPrivateKey.from_hex("a1b2c3d4...")
        print("Private key is valid")

        # Validate a bech32 public key
        public_key = NostrPublicKey.from_bech32("npub1...")
        print("Public key is valid")

    except KeyFormatError as e:
        print(f"Key validation failed: {e}")

Advanced Cryptographic Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use low-level crypto functions:

.. code-block:: python

    from nostress.core import crypto

    # Generate raw private key bytes
    private_bytes = crypto.generate_private_key()

    # Derive public key
    public_bytes = crypto.derive_public_key(private_bytes)

    # Convert to different formats
    hex_key = crypto.bytes_to_hex(private_bytes)
    bech32_key = crypto.encode_bech32("nsec", private_bytes)

    print(f"Generated key: {hex_key}")
    print(f"Bech32 format: {bech32_key}")

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Work with configuration:

.. code-block:: python

    from nostress.utils.config import load_config, get_data_dir

    # Load user configuration
    config = load_config()

    # Get data directory
    data_dir = get_data_dir()
    print(f"Data directory: {data_dir}")

Output Formatting
~~~~~~~~~~~~~~~~~

Use Rich formatting utilities:

.. code-block:: python

    from nostress.utils.output import create_keypair_table, output_json
    from nostress.core.models import NostrKeypair
    from rich.console import Console

    # Create a keypair
    keypair = NostrKeypair.generate()

    # Display as Rich table
    console = Console()
    table = create_keypair_table(keypair)
    console.print(table)

    # Output as JSON
    json_str = output_json(keypair)
    print(json_str)

Type Information
----------------

Nostress extensively uses type hints for better development experience:

Key Types
~~~~~~~~~

.. code-block:: python

    from typing import Union
    from nostress.core.models import NostrPrivateKey, NostrPublicKey

    # Union type for any key
    AnyKey = Union[NostrPrivateKey, NostrPublicKey]

    # Function with type hints
    def process_key(key: AnyKey) -> str:
        return key.hex

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

    from nostress.exceptions import (
        NostrError,
        CryptographicError,
        KeyFormatError,
        ValidationError
    )

    try:
        # Some operation that might fail
        result = some_crypto_operation()
    except CryptographicError as e:
        print(f"Crypto error: {e}")
    except KeyFormatError as e:
        print(f"Key format error: {e}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    except NostrError as e:
        print(f"General Nostress error: {e}")

Testing Integration
~~~~~~~~~~~~~~~~~~~

Example of using Nostress in tests:

.. code-block:: python

    import pytest
    from nostress.core.models import NostrKeypair
    from nostress.exceptions import KeyFormatError

    def test_keypair_generation():
        """Test that keypair generation works correctly."""
        keypair = NostrKeypair.generate()

        # Verify keys are properly formatted
        assert len(keypair.private_key.hex) == 64
        assert len(keypair.public_key.hex) == 64
        assert keypair.private_key.bech32.startswith("nsec1")
        assert keypair.public_key.bech32.startswith("npub1")

    def test_invalid_key_format():
        """Test that invalid keys raise appropriate errors."""
        with pytest.raises(KeyFormatError):
            NostrPrivateKey.from_hex("invalid")

Integration Examples
~~~~~~~~~~~~~~~~~~~~

Web Application Integration:

.. code-block:: python

    from fastapi import FastAPI, HTTPException
    from nostress.core.models import NostrKeypair
    from nostress.exceptions import NostrError

    app = FastAPI()

    @app.post("/generate-keypair")
    async def generate_keypair():
        try:
            keypair = NostrKeypair.generate()
            return {
                "private_key": keypair.private_key.bech32,
                "public_key": keypair.public_key.bech32
            }
        except NostrError as e:
            raise HTTPException(status_code=500, detail=str(e))

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

For high-performance applications:

.. code-block:: python

    import time
    from nostress.core.models import NostrKeypair

    # Benchmark key generation
    start_time = time.time()

    keypairs = []
    for _ in range(1000):
        keypair = NostrKeypair.generate()
        keypairs.append(keypair)

    end_time = time.time()
    print(f"Generated 1000 keypairs in {end_time - start_time:.2f} seconds")

Development Utilities
~~~~~~~~~~~~~~~~~~~~~

For development and debugging:

.. code-block:: python

    import os
    from nostress.core.models import NostrKeypair
    from nostress.utils.output import create_keypair_table
    from rich.console import Console

    # Enable verbose mode
    os.environ["NOSTRESS_VERBOSE"] = "1"

    # Generate and display keypair with full information
    keypair = NostrKeypair.generate()

    console = Console()
    table = create_keypair_table(keypair)
    console.print(table)

    # Display internal properties
    print(f"Private key bytes length: {len(keypair.private_key._private_bytes)}")
    print(f"Public key bytes length: {len(keypair.public_key._public_bytes)}")
