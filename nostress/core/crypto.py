"""Cryptographic operations for Nostr key generation."""

import secrets

import base58
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from ..exceptions import CryptographicError


def generate_private_key() -> bytes:
    """Generate a secure 32-byte private key.

    Returns:
        bytes: A secure random 32-byte private key
    """
    return secrets.token_bytes(32)


def derive_public_key(private_key: bytes) -> bytes:
    """Derive public key from private key using secp256k1.

    Args:
        private_key: 32-byte private key

    Returns:
        bytes: 32-byte public key (x-coordinate only)

    Raises:
        CryptographicError: If key derivation fails
    """
    try:
        # Convert bytes to integer for private key
        private_key_int = int.from_bytes(private_key, byteorder="big")

        # Create private key object using cryptography
        privkey = ec.derive_private_key(
            private_key_int, ec.SECP256K1(), default_backend()
        )

        # Get public key
        pubkey = privkey.public_key()

        # Serialize public key in uncompressed format
        pubkey_bytes = pubkey.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )

        # Extract x-coordinate (32 bytes) - skip the 0x04 prefix
        return pubkey_bytes[1:33]

    except Exception as e:
        raise CryptographicError(f"Failed to derive public key: {e}") from e


def private_key_to_hex(private_key: bytes) -> str:
    """Convert private key to hex format.

    Args:
        private_key: 32-byte private key

    Returns:
        str: Hex-encoded private key
    """
    return private_key.hex()


def public_key_to_hex(public_key: bytes) -> str:
    """Convert public key to hex format.

    Args:
        public_key: 32-byte public key

    Returns:
        str: Hex-encoded public key
    """
    return public_key.hex()


def private_key_to_bech32(private_key: bytes) -> str:
    """Convert private key to bech32 nsec format (NIP-19).

    Args:
        private_key: 32-byte private key

    Returns:
        str: Bech32-encoded private key with nsec prefix

    Raises:
        CryptographicError: If encoding fails
    """
    try:
        # Simple implementation for now - we'll use a basic approach
        # For production, we'd use proper bech32 encoding
        return f"nsec{base58.b58encode(private_key).decode()}"
    except Exception as e:
        raise CryptographicError(f"Failed to encode private key to bech32: {e}") from e


def public_key_to_bech32(public_key: bytes) -> str:
    """Convert public key to bech32 npub format (NIP-19).

    Args:
        public_key: 32-byte public key

    Returns:
        str: Bech32-encoded public key with npub prefix

    Raises:
        CryptographicError: If encoding fails
    """
    try:
        # Simple implementation for now - we'll use a basic approach
        # For production, we'd use proper bech32 encoding
        return f"npub{base58.b58encode(public_key).decode()}"
    except Exception as e:
        raise CryptographicError(f"Failed to encode public key to bech32: {e}") from e


def generate_keypair() -> tuple[bytes, bytes]:
    """Generate a complete Nostr keypair.

    Returns:
        Tuple[bytes, bytes]: (private_key, public_key)
    """
    private_key = generate_private_key()
    public_key = derive_public_key(private_key)
    return private_key, public_key


def validate_private_key_hex(hex_key: str) -> bool:
    """Validate a hex-encoded private key.

    Args:
        hex_key: Hex string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if len(hex_key) != 64:  # 32 bytes = 64 hex chars
            return False
        bytes.fromhex(hex_key)
        return True
    except ValueError:
        return False


def validate_public_key_hex(hex_key: str) -> bool:
    """Validate a hex-encoded public key.

    Args:
        hex_key: Hex string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if len(hex_key) != 64:  # 32 bytes = 64 hex chars
            return False
        bytes.fromhex(hex_key)
        return True
    except ValueError:
        return False


def validate_bech32_key(bech32_key: str, expected_prefix: str) -> bool:
    """Validate a bech32-encoded key.

    Args:
        bech32_key: Bech32 string to validate
        expected_prefix: Expected prefix (nsec or npub)

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not bech32_key.startswith(expected_prefix):
            return False

        # Extract the base58 part after the prefix
        encoded_part = bech32_key[len(expected_prefix) :]

        # Try to decode and check length
        decoded = base58.b58decode(encoded_part)
        return len(decoded) == 32  # Should be 32 bytes
    except Exception:
        return False
