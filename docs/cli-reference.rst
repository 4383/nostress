CLI Reference
=============

This section provides comprehensive documentation for all Nostress command-line interfaces.

Global Options
--------------

These options are available for all commands:

``--version``
    Show the version and exit.

``--verbose``
    Enable verbose output with detailed information.

Main Command
------------

.. program:: nostress

The main ``nostress`` command provides access to all functionality.

Synopsis::

    nostress [OPTIONS] COMMAND [ARGS]...

Options
~~~~~~~

.. option:: --version

   Display the version of Nostress and exit.

.. option:: --verbose

   Enable verbose output mode. This provides detailed information about
   operations, including timing information and internal details.

Commands
~~~~~~~~

.. option:: keys

   Key management operations (generate, validate, convert).

.. option:: tips

   Support and sponsorship information for Nostr development.

Keys Commands
-------------

.. program:: nostress keys

The ``keys`` subcommand group handles all cryptographic key operations.

Synopsis::

    nostress keys [OPTIONS] COMMAND [ARGS]...

Generate Command
~~~~~~~~~~~~~~~~

.. program:: nostress keys generate

Generate a new Nostr keypair.

Synopsis::

    nostress keys generate [OPTIONS]

Description
^^^^^^^^^^^

Generates a cryptographically secure Nostr keypair using secp256k1 elliptic curve cryptography.
The private key is generated using the system's secure random number generator.

Options
^^^^^^^

.. option:: --format <format>

   Output format for the keys. Choices:

   - ``hex`` (default): Hexadecimal format
   - ``bech32``: Bech32 format with nsec/npub prefixes
   - ``both``: Both hex and bech32 formats

.. option:: --json

   Output keys in JSON format for scripting and automation.

.. option:: --output <file>, -o <file>

   Save the generated keys to a file instead of displaying on screen.

.. option:: --encrypt

   Encrypt the output with a password. Prompts for password input.
   Only used when saving to a file with ``--output``.

.. option:: --verbose

   Show detailed generation information including timing and key properties.

Examples
^^^^^^^^

Generate a basic keypair::

    nostress keys generate

Generate in bech32 format with verbose output::

    nostress keys generate --format bech32 --verbose

Generate both formats and save to file::

    nostress keys generate --format both --output my-keys.txt

Generate for automation with JSON output::

    nostress keys generate --json

Generate and encrypt with password::

    nostress keys generate --encrypt --output secure-keys.txt

Validate Command
~~~~~~~~~~~~~~~~

.. program:: nostress keys validate

Validate the format and cryptographic validity of Nostr keys.

Synopsis::

    nostress keys validate [OPTIONS] KEY

Description
^^^^^^^^^^^

Validates that a provided key is properly formatted and cryptographically valid.
Supports both hexadecimal and bech32 formats for private and public keys.

Arguments
^^^^^^^^^

.. option:: KEY

   The key to validate. Can be in hex or bech32 format.

Options
^^^^^^^

.. option:: --type <key_type>

   Specify the expected key type for validation. Choices:

   - ``nsec``: Expect a bech32 private key (nsec1...)
   - ``npub``: Expect a bech32 public key (npub1...)
   - ``auto`` (default): Auto-detect the key type

.. option:: --verbose

   Show detailed validation information including key properties and format details.

Examples
^^^^^^^^

Validate a hex private key::

    nostress keys validate a1b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef0123456789ab

Validate a bech32 public key::

    nostress keys validate npub1xyz123...

Validate with type checking::

    nostress keys validate nsec1abc789... --type nsec

Validate with detailed output::

    nostress keys validate npub1xyz123... --verbose

Convert Command
~~~~~~~~~~~~~~~

.. program:: nostress keys convert

Convert keys between different formats.

.. warning::
   This command is currently not implemented and will display a warning message.
   It is planned for a future release.

Synopsis::

    nostress keys convert [OPTIONS] KEY

Description
^^^^^^^^^^^

Convert keys between hexadecimal and bech32 formats. This command will be
available in a future release.

Planned functionality:

- Convert hex keys to bech32 format
- Convert bech32 keys to hex format
- Batch conversion of multiple keys
- File-based conversion operations

Tips Commands
-------------

.. program:: nostress tips

The ``tips`` subcommand group provides ways to support Nostr development and connect with the project.

Synopsis::

    nostress tips [OPTIONS] COMMAND [ARGS]...

Show Command
~~~~~~~~~~~~

.. program:: nostress tips show

Display comprehensive support and sponsorship information.

Synopsis::

    nostress tips show [OPTIONS]

Description
^^^^^^^^^^^

Shows available ways to support Nostr development through Lightning Network zaps,
Bitcoin donations, and sponsorship options. Perfect for sharing with users who
want to support the project.

Options
^^^^^^^

.. option:: --format <format>, -f <format>

   Output format for the information. Choices:

   - ``rich`` (default): Rich formatted panels with styling
   - ``table``: Clean table format
   - ``json``: JSON format for automation
   - ``text``: Plain text format

.. option:: --output <file>, -o <file>

   Save output to file instead of displaying on screen.

.. option:: --qr

   Include QR codes for easy scanning. Only works with ``rich`` format.
   Requires the ``qrcode`` package to be installed.

Examples
^^^^^^^^

Show support information::

    nostress tips show

Show in table format::

    nostress tips show --format table

Save to file for sharing::

    nostress tips show --format text --output support-info.txt

Show with QR codes::

    nostress tips show --qr

Lightning Command
~~~~~~~~~~~~~~~~~

.. program:: nostress tips lightning

Display Lightning Network address for zaps.

Synopsis::

    nostress tips lightning [OPTIONS]

Description
^^^^^^^^^^^

Shows just the Lightning Network address for quick copying or sharing.
Perfect for adding to documentation or sharing in Nostr posts.

Options
^^^^^^^

.. option:: --format <format>, -f <format>

   Output format. Choices:

   - ``text`` (default): Plain text address
   - ``json``: JSON format with structured data

Examples
^^^^^^^^

Get Lightning address::

    nostress tips lightning

Get as JSON for scripting::

    nostress tips lightning --format json

Nostr Command
~~~~~~~~~~~~~

.. program:: nostress tips nostr

Display Nostr public key for following.

Synopsis::

    nostress tips nostr [OPTIONS]

Description
^^^^^^^^^^^

Shows the developer's Nostr public key for following and zapping.

Options
^^^^^^^

.. option:: --format <format>, -f <format>

   Output format. Choices:

   - ``text`` (default): Plain text public key
   - ``json``: JSON format with structured data

Examples
^^^^^^^^

Get Nostr public key::

    nostress tips nostr

Get as JSON for automation::

    nostress tips nostr --format json

Logo Command
~~~~~~~~~~~~

.. program:: nostress tips logo

Display the Nostress ASCII art logo.

Synopsis::

    nostress tips logo [OPTIONS]

Description
^^^^^^^^^^^

Shows the beautiful ASCII art logo with lightning-themed colors.
Perfect for documentation, presentations, or just admiring the artwork!

Options
^^^^^^^

.. option:: --plain, -p

   Display plain text without colors.

.. option:: --output <file>, -o <file>

   Save logo to file instead of displaying on screen.

Examples
^^^^^^^^

Display colorful logo::

    nostress tips logo

Display without colors::

    nostress tips logo --plain

Save logo to file::

    nostress tips logo --output logo.txt

Exit Codes
----------

Nostress uses standard exit codes:

- ``0``: Success
- ``1``: General error (invalid arguments, validation failure)
- ``2``: File operation error (cannot read/write files)
- ``3``: Cryptographic error (invalid key format, generation failure)

Error Handling
--------------

Nostress provides clear error messages for common issues:

Key Format Errors
~~~~~~~~~~~~~~~~~~

When a key is not properly formatted::

    Error: Invalid key format. Expected hex (64 chars) or bech32 (nsec1.../npub1...)

File Permission Errors
~~~~~~~~~~~~~~~~~~~~~~~

When unable to write to a file::

    Error: Permission denied: Cannot write to 'output.txt'

Validation Errors
~~~~~~~~~~~~~~~~~~

When a key fails cryptographic validation::

    Error: Key validation failed: Invalid private key (not on secp256k1 curve)

Verbose Mode
------------

Using ``--verbose`` with any command provides additional information:

- Detailed timing information
- Internal operation details
- Key properties and metadata
- Validation steps and results

Example verbose output for key generation::

    nostress keys generate --verbose

    Nostress Key Generation
    ─────────────────────────────────────

    📊 Key Properties
    ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Property       ┃ Value                         ┃
    ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ Private Key    │ a1b2c3d4...                   │
    │ Public Key     │ 123456...                     │
    │ Curve          │ secp256k1                     │
    │ Key Length     │ 256 bits                      │
    └────────────────┴───────────────────────────────┘

Configuration Files
-------------------

Nostress follows XDG Base Directory specification:

Config Directory
~~~~~~~~~~~~~~~~

``$XDG_CONFIG_HOME/nostress/`` or ``~/.config/nostress/``

- Configuration files
- User preferences
- Custom settings

Data Directory
~~~~~~~~~~~~~~

``$XDG_DATA_HOME/nostress/`` or ``~/.local/share/nostress/``

- Application data
- Cached information
- Generated files

Cache Directory
~~~~~~~~~~~~~~~

``$XDG_CACHE_HOME/nostress/`` or ``~/.cache/nostress/``

- Temporary files
- Download cache
- Build artifacts

Environment Variables
---------------------

.. envvar:: NOSTRESS_VERBOSE

   Set to ``1`` to enable verbose mode globally.

.. envvar:: XDG_CONFIG_HOME

   Override default config directory location.

.. envvar:: XDG_DATA_HOME

   Override default data directory location.

.. envvar:: XDG_CACHE_HOME

   Override default cache directory location.

Scripting and Automation
-------------------------

JSON Output
~~~~~~~~~~~

Use ``--json`` flag to get machine-readable output::

    nostress keys generate --json | jq '.private_key.hex'
    nostress tips show --format json | jq '.lightning_address'

This is perfect for shell scripts and automation pipelines.

Error Handling in Scripts
~~~~~~~~~~~~~~~~~~~~~~~~~

Check exit codes in your scripts:

.. code-block:: bash

    if nostress keys validate "$KEY"; then
        echo "Key is valid"
    else
        echo "Key validation failed"
        exit 1
    fi

Batch Operations
~~~~~~~~~~~~~~~~

Generate multiple keys:

.. code-block:: bash

    for i in {1..10}; do
        nostress keys generate --json > "key-$i.json"
    done
