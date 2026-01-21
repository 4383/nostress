# ⚡ Nostress

<div align="center">

![Nostress Banner](docs/_static/images/banner.png)

</div>

[![PyPI - Downloads](https://img.shields.io/pypi/dm/nostress?style=flat-square&logo=pypi&logoColor=white&label=Downloads&labelColor=blue&color=blue)](https://pypi.org/project/nostress/)
[![Python Version](https://img.shields.io/pypi/pyversions/nostress?style=flat-square&logo=python&logoColor=white&label=Python&labelColor=blue&color=blue)](https://pypi.org/project/nostress/)
[![Documentation Status](https://readthedocs.org/projects/nostress/badge/?version=latest&style=flat-square)](https://nostress.readthedocs.io/en/latest/?badge=latest)
[![Test Coverage](https://img.shields.io/badge/Coverage-30%25-orange?style=flat-square&logo=pytest&logoColor=white&labelColor=orange)](https://github.com/4383/nostress)
[![Lightning](https://img.shields.io/badge/⚡-hberaud@nostrcheck.me-yellow?style=flat-square&logo=lightning&logoColor=white&labelColor=orange)](https://hberaud@nostrcheck.me)

> **A modern, secure, and lightning-fast CLI for Nostr protocol interactions**

Nostress empowers developers and Nostr enthusiasts with a powerful command-line interface for seamless key management, event creation, and relay interactions. Built with security-first principles and modern Python practices, it's the tool you've been waiting for to dive deeper into the decentralized web.

## ✨ Why Nostress?

**🔐 Security First**: Cryptographically secure key generation using industry-standard `secp256k1` elliptic curve cryptography

**⚡ Lightning Fast**: Built with modern Python and optimized for performance with rich terminal interfaces

**🛠️ Developer Friendly**: Intuitive CLI with comprehensive help, JSON output, and scripting support

**🔄 Format Flexible**: Seamless conversion between hex and bech32 formats (nsec/npub)

**🎨 Beautiful Output**: Rich terminal formatting with tables, colors, and verbose modes

## 🚀 Quick Start

### Installation

```bash
# Install via pip
pip install nostress

# Or using uv (recommended for development)
uv pip install nostress

# Verify installation
nostress --help
```

### Your First Keypair

```bash
# Generate a new keypair (hex format)
nostress keys generate

# Generate in bech32 format with verbose output
nostress keys generate --format bech32 --verbose

# Generate both formats and save to file
nostress keys generate --format both --output my-keypair.txt

# JSON output for scripting
nostress keys generate --json
```

## 🔑 Core Features

### Key Management Made Simple

**Generate Secure Keypairs**
```bash
# Basic generation
nostress keys generate

# Multiple formats
nostress keys generate --format both --verbose

# Encrypted storage
nostress keys generate --encrypt --output secure-key.txt
```

**Validate Any Key**
```bash
# Validate hex keys
nostress keys validate abc123...def

# Validate bech32 keys with type checking
nostress keys validate nsec1... --type nsec
nostress keys validate npub1... --type npub
```

**Format Conversion** *(Coming Soon)*
```bash
# Convert between formats
nostress keys convert nsec1... --to hex
nostress keys convert abc123... --to bech32 --type private
```

### Advanced Features

- **🔒 Encryption Support**: Password-protected key storage
- **📊 Rich Output**: Beautiful tables and formatted displays
- **🤖 JSON Mode**: Perfect for automation and scripting
- **🔍 Verbose Logging**: Detailed operation insights
- **📁 File Operations**: Save and load keys securely

## 🏗️ Architecture & Design

Nostress is built with a clean, modular architecture:

- **CLI Layer**: Intuitive command interface with Typer
- **Core Logic**: Cryptographic operations with the `cryptography` library
- **Utilities**: Validation, formatting, and configuration management
- **Rich Integration**: Beautiful terminal output with colors and tables

### Tech Stack

- **Python 3.12+**: Modern Python with type hints
- **Typer**: Powerful CLI framework with auto-completion
- **Rich**: Beautiful terminal formatting
- **Cryptography**: Industry-standard cryptographic operations
- **Pydantic**: Data validation and models

## 📖 Documentation

📚 **For comprehensive documentation, tutorials, and API reference, visit our [ReadTheDocs site](https://nostress.readthedocs.io/)**

### Quick Command Reference

```bash
# Main help
nostress --help

# Key management commands
nostress keys --help

# Specific command help
nostress keys generate --help
nostress keys validate --help
```

### Configuration

Nostress follows XDG Base Directory standards for configuration:

- **Config**: `~/.config/nostress/`
- **Data**: `~/.local/share/nostress/`
- **Cache**: `~/.cache/nostress/`

## 🛣️ Roadmap

**Current Features (v0.1.x)**
- ✅ Secure key generation (hex/bech32)
- ✅ Key validation and verification
- ✅ Rich terminal output and JSON support
- ✅ Encrypted key storage

**Coming Soon (v0.2.x)**
- 🔄 Format conversion between hex/bech32
- 📝 Event creation and signing
- 🔗 Relay connection management
- 🏪 Event publishing and querying

**Future Plans (v1.0+)**
- 📊 Advanced event filtering and search
- 🔐 Multi-signature support
- ⚡ Lightning integration
- 🕸️ Web interface companion

## 💖 Support the Project

Love Nostress? Support its development by sending some sats or connecting on Nostr!

### ⚡ Lightning Payments

**Lightning Address**: `hberaud@nostrcheck.me`

<div align="center">

![Lightning QR Code](docs/_static/images/lightning.png)

*Scan to send lightning payments*

</div>

Your support helps maintain and improve Nostress, ensuring it remains free and open-source for the entire Nostr community.

### 🫂 Follow on Nostr

**Nostr Public Key**: `npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty`

<div align="center">

![Nostr QR Code](docs/_static/images/nostr.png)

*Scan to follow me on Nostr*

</div>

### Other Ways to Contribute

- 🌟 **Star the repository** to show your support
- 🐛 **Report bugs** and suggest features
- 💻 **Contribute code** via pull requests
- 📖 **Improve documentation** and examples
- 🗣️ **Spread the word** in the Nostr community

## 📄 License

Nostress is open-source software. Check the `LICENSE` file for details.

## 🤝 Contributing

We welcome contributions from the community! Whether it's:

- Bug fixes and improvements
- New features and commands
- Documentation updates
- Test coverage improvements

Please see our contribution guidelines and feel free to open issues and pull requests.

## 🔗 Connect

- **Documentation**: [nostress.readthedocs.io](https://nostress.readthedocs.io/)
- **GitHub**: [github.com/4383/nostress](https://github.com/4383/nostress)
- **PyPI**: [pypi.org/project/nostress](https://pypi.org/project/nostress)
- **Lightning**: `hberaud@nostrcheck.me`
- **Nostr**: `npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty`

---

<div align="center">

**Built with ❤️ for the Nostr community**

*Nostress - Where cryptographic security meets developer experience*

</div>
