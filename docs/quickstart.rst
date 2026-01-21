Quick Start
===========

This guide will help you get started with Nostress quickly and efficiently.

Your First Keypair
-------------------

The most common operation in Nostress is generating a new Nostr keypair.

Basic Generation
~~~~~~~~~~~~~~~~

Generate a keypair in hexadecimal format (default)::

    nostress keys generate

This will output something like::

    Private Key: a1b2c3d4e5f6789...
    Public Key:  123456789abcdef...

Bech32 Format
~~~~~~~~~~~~~

Generate a keypair in bech32 format (nsec/npub)::

    nostress keys generate --format bech32

Output::

    Private Key (nsec): nsec1xyz...
    Public Key (npub):  npub1abc...

Verbose Output
~~~~~~~~~~~~~~

See detailed information about your keypair::

    nostress keys generate --verbose

This shows a beautiful table with all key information and formats.

Both Formats
~~~~~~~~~~~~

Generate keys in both hex and bech32 formats::

    nostress keys generate --format both

JSON Output
~~~~~~~~~~~

Perfect for scripts and automation::

    nostress keys generate --json

Example output:

.. code-block:: json

    {
        "private_key": {
            "hex": "a1b2c3d4...",
            "bech32": "nsec1xyz..."
        },
        "public_key": {
            "hex": "123456...",
            "bech32": "npub1abc..."
        }
    }

Saving Keys to File
-------------------

Save Generated Keys
~~~~~~~~~~~~~~~~~~~

Save your keypair to a file::

    nostress keys generate --output my-keypair.txt

The file will contain both private and public keys with clear labels.

Encrypted Storage
~~~~~~~~~~~~~~~~~

Save keys with password protection::

    nostress keys generate --encrypt --output secure-keypair.txt

You'll be prompted to enter a password to encrypt the file.

Key Validation
--------------

Nostress can validate keys to ensure they're properly formatted and cryptographically valid.

Validate Hex Keys
~~~~~~~~~~~~~~~~~

::

    nostress keys validate a1b2c3d4e5f6789abcdef...

Validate Bech32 Keys
~~~~~~~~~~~~~~~~~~~~

::

    nostress keys validate nsec1xyz123...

With type checking::

    nostress keys validate nsec1xyz123... --type nsec
    nostress keys validate npub1abc789... --type npub

Common Use Cases
----------------

Script Integration
~~~~~~~~~~~~~~~~~~

Generate a keypair for use in scripts:

.. code-block:: bash

    #!/bin/bash

    # Generate keypair and extract private key
    PRIVATE_KEY=$(nostress keys generate --json | jq -r '.private_key.hex')

    # Use the key in your application
    echo "Generated private key: $PRIVATE_KEY"

Daily Key Generation
~~~~~~~~~~~~~~~~~~~~

Generate daily development keys::

    # Generate and save with timestamp
    nostress keys generate --format both --output "keys-$(date +%Y%m%d).txt"

Multiple Key Generation
~~~~~~~~~~~~~~~~~~~~~~~

Generate multiple keypairs for testing:

.. code-block:: bash

    for i in {1..5}; do
        nostress keys generate --format bech32 --output "test-key-$i.txt"
    done

Configuration
-------------

Nostress follows XDG Base Directory standards:

- **Config**: ``~/.config/nostress/``
- **Data**: ``~/.local/share/nostress/``
- **Cache**: ``~/.cache/nostress/``

Getting Help
------------

Nostress has comprehensive help built-in:

Main Help
~~~~~~~~~

::

    nostress --help

Command-Specific Help
~~~~~~~~~~~~~~~~~~~~~

::

    nostress keys --help
    nostress keys generate --help
    nostress keys validate --help

Verbose Mode
~~~~~~~~~~~~

Add ``--verbose`` to any command to see detailed output and execution information.

Security Notes
--------------

Key Storage
~~~~~~~~~~~

- Always store private keys securely
- Use the ``--encrypt`` option for sensitive keys
- Never share private keys or commit them to version control
- Consider using hardware wallets for long-term storage

Key Generation
~~~~~~~~~~~~~~

- Nostress uses cryptographically secure random number generation
- Keys are generated using the secp256k1 elliptic curve
- No network connection is required for key generation

Best Practices
~~~~~~~~~~~~~~

1. **Backup your keys** - Generate backups and store them securely
2. **Test with small amounts** - When using keys for real transactions, test with small amounts first
3. **Verify keys** - Use the validation commands to ensure keys are valid
4. **Use verbose mode** - When learning, use ``--verbose`` to understand what's happening

Next Steps
----------

Now that you've generated your first keypair, you might want to:

- Read the :doc:`cli-reference` for complete command documentation
- Explore the :doc:`api-reference` if you're integrating Nostress into Python applications
- Check out the :doc:`architecture` to understand how Nostress works internally
- Contribute to the project by reading :doc:`contributing`

Troubleshooting
---------------

If you encounter issues:

1. **Check your installation**: ``nostress --version``
2. **Verify Python version**: ``python --version`` (requires 3.12+)
3. **Run with verbose mode**: Add ``--verbose`` to see detailed error information
4. **Check file permissions**: Ensure you have write access when saving keys
5. **Validate your keys**: Use ``nostress keys validate`` to check key format

For more help, see the full documentation or open an issue on GitHub.
