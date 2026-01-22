Nostress Documentation
======================

.. image:: _static/images/banner.png
   :alt: Nostress Banner
   :align: center
   :width: 600

.. image:: https://img.shields.io/pypi/dm/nostress?style=flat-square&logo=pypi&logoColor=white&label=Downloads&labelColor=blue&color=blue
   :target: https://pypi.org/project/nostress/
   :alt: PyPI Downloads

.. image:: https://img.shields.io/pypi/pyversions/nostress?style=flat-square&logo=python&logoColor=white&label=Python&labelColor=blue&color=blue
   :target: https://pypi.org/project/nostress/
   :alt: Python Version

.. image:: https://github.com/4383/nostress/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/4383/nostress/actions/workflows/ci.yml
   :alt: CI Tests

.. image:: https://readthedocs.org/projects/nostress/badge/?version=latest&style=flat-square
   :target: https://nostress.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/Coverage-64%25-brightgreen?style=flat-square&logo=pytest&logoColor=white&labelColor=brightgreen
   :target: https://github.com/4383/nostress
   :alt: Test Coverage

.. image:: https://img.shields.io/badge/⚡-hberaud@nostrcheck.me-yellow?style=flat-square&logo=lightning&logoColor=white&labelColor=orange
   :target: https://hberaud@nostrcheck.me
   :alt: Lightning

**Nostress** is a modern Python CLI for Nostr protocol interactions, providing key generation, event creation, and relay management capabilities.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   cli-reference
   api-reference
   architecture
   contributing

Overview
--------

Nostress provides a clean, secure interface for interacting with the Nostr protocol. Built with modern Python practices, it offers:

* **Secure Key Management**: Generate and manage Nostr keypairs with cryptographically secure methods
* **Format Support**: Handle both hexadecimal and bech32 key formats
* **Rich CLI Interface**: Intuitive command-line interface with verbose output options
* **Extensible Architecture**: Well-structured codebase ready for additional Nostr features

Key Features
------------

🔐 **Cryptographic Operations**
   Secure key generation using the `cryptography` library with secp256k1 elliptic curve support.

🎨 **Rich Output**
   Beautiful terminal output with tables, JSON formatting, and progress indicators.

⚙️ **Modern Python**
   Built for Python 3.12+ with type hints, Pydantic models, and comprehensive testing.

🔧 **Developer Friendly**
   Extensive documentation, clear architecture, and ready for extension.

Quick Start
-----------

Installation::

    uv pip install nostress

Generate your first keypair::

    nostress keys generate

See the full output with verbose mode::

    nostress keys generate --verbose

Get help::

    nostress --help
    nostress keys --help

Support & Community
-------------------

**Lightning Support** ⚡

Support the development of Nostress with Lightning payments:

.. image:: _static/images/lightning.png
   :alt: Lightning Support QR Code
   :width: 200
   :align: center

**Connect on Nostr** 🔗

Follow and connect with the project on the decentralized Nostr network:

.. image:: _static/images/nostr.png
   :alt: Nostr Connection QR Code
   :width: 200
   :align: center

**Contact**: ``hberaud@nostrcheck.me``

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
