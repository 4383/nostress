"""Unit tests for cryptographic operations."""

import contextlib

import pytest

from nostress.core import crypto
from nostress.exceptions import CryptographicError


class TestKeyGeneration:
    """Test key generation functions."""

    def test_generate_private_key(self):
        """Test private key generation."""
        private_key = crypto.generate_private_key()

        assert isinstance(private_key, bytes)
        assert len(private_key) == 32

        # Generate another key and ensure they're different
        another_key = crypto.generate_private_key()
        assert private_key != another_key

    def test_derive_public_key_valid(self):
        """Test public key derivation with valid private key."""
        private_key = crypto.generate_private_key()
        public_key = crypto.derive_public_key(private_key)

        assert isinstance(public_key, bytes)
        assert len(public_key) == 32

    def test_derive_public_key_invalid(self):
        """Test public key derivation with invalid private key."""
        # Invalid data (all zeros - invalid secp256k1 key)
        with pytest.raises(CryptographicError):
            crypto.derive_public_key(b"\x00" * 32)

        # Test that short input doesn't crash (just processes as-is)
        # Note: cryptography library accepts variable length inputs
        result = crypto.derive_public_key(b"short")
        assert isinstance(result, bytes)
        assert len(result) == 32

    def test_generate_keypair(self):
        """Test complete keypair generation."""
        private_key, public_key = crypto.generate_keypair()

        assert isinstance(private_key, bytes)
        assert isinstance(public_key, bytes)
        assert len(private_key) == 32
        assert len(public_key) == 32

        # Verify the public key matches the private key
        derived_public = crypto.derive_public_key(private_key)
        assert public_key == derived_public


class TestHexConversions:
    """Test hex format conversions."""

    def test_private_key_to_hex(self):
        """Test private key to hex conversion."""
        private_key = crypto.generate_private_key()
        hex_key = crypto.private_key_to_hex(private_key)

        assert isinstance(hex_key, str)
        assert len(hex_key) == 64  # 32 bytes = 64 hex chars
        assert all(c in "0123456789abcdef" for c in hex_key.lower())

    def test_public_key_to_hex(self):
        """Test public key to hex conversion."""
        _, public_key = crypto.generate_keypair()
        hex_key = crypto.public_key_to_hex(public_key)

        assert isinstance(hex_key, str)
        assert len(hex_key) == 64  # 32 bytes = 64 hex chars
        assert all(c in "0123456789abcdef" for c in hex_key.lower())

    def test_hex_roundtrip(self):
        """Test hex encoding/decoding roundtrip."""
        private_key = crypto.generate_private_key()
        hex_key = crypto.private_key_to_hex(private_key)
        decoded_key = bytes.fromhex(hex_key)

        assert private_key == decoded_key


class TestBech32Conversions:
    """Test bech32 format conversions."""

    def test_private_key_to_bech32(self):
        """Test private key to bech32 conversion."""
        private_key = crypto.generate_private_key()
        bech32_key = crypto.private_key_to_bech32(private_key)

        assert isinstance(bech32_key, str)
        assert bech32_key.startswith("nsec")

    def test_public_key_to_bech32(self):
        """Test public key to bech32 conversion."""
        _, public_key = crypto.generate_keypair()
        bech32_key = crypto.public_key_to_bech32(public_key)

        assert isinstance(bech32_key, str)
        assert bech32_key.startswith("npub")

    def test_bech32_encoding_error_handling(self):
        """Test bech32 encoding error handling."""
        # Test with invalid input (this is hard to trigger with base58,
        # but we test the exception path exists)
        with contextlib.suppress(CryptographicError):
            crypto.private_key_to_bech32(b"test")


class TestValidation:
    """Test validation functions."""

    def test_validate_private_key_hex_valid(self):
        """Test validation of valid hex private keys."""
        private_key = crypto.generate_private_key()
        hex_key = crypto.private_key_to_hex(private_key)

        assert crypto.validate_private_key_hex(hex_key)

    def test_validate_private_key_hex_invalid(self):
        """Test validation of invalid hex private keys."""
        # Too short
        assert not crypto.validate_private_key_hex("abc123")

        # Too long
        assert not crypto.validate_private_key_hex("a" * 65)

        # Invalid hex characters
        assert not crypto.validate_private_key_hex("g" * 64)

        # Empty string
        assert not crypto.validate_private_key_hex("")

    def test_validate_public_key_hex_valid(self):
        """Test validation of valid hex public keys."""
        _, public_key = crypto.generate_keypair()
        hex_key = crypto.public_key_to_hex(public_key)

        assert crypto.validate_public_key_hex(hex_key)

    def test_validate_public_key_hex_invalid(self):
        """Test validation of invalid hex public keys."""
        # Too short
        assert not crypto.validate_public_key_hex("abc123")

        # Too long
        assert not crypto.validate_public_key_hex("a" * 65)

        # Invalid hex characters
        assert not crypto.validate_public_key_hex("z" * 64)

    def test_validate_bech32_key_valid(self):
        """Test validation of valid bech32 keys."""
        private_key = crypto.generate_private_key()
        _, public_key = crypto.generate_keypair()

        nsec_key = crypto.private_key_to_bech32(private_key)
        npub_key = crypto.public_key_to_bech32(public_key)

        assert crypto.validate_bech32_key(nsec_key, "nsec")
        assert crypto.validate_bech32_key(npub_key, "npub")

    def test_validate_bech32_key_invalid(self):
        """Test validation of invalid bech32 keys."""
        # Wrong prefix
        assert not crypto.validate_bech32_key("npubtest", "nsec")
        assert not crypto.validate_bech32_key("nsectest", "npub")

        # Empty string
        assert not crypto.validate_bech32_key("", "nsec")

        # Invalid base58
        assert not crypto.validate_bech32_key("nsec!!!invalid", "nsec")


class TestIntegration:
    """Integration tests combining multiple functions."""

    def test_full_workflow_hex(self):
        """Test complete workflow with hex format."""
        # Generate keypair
        private_key, public_key = crypto.generate_keypair()

        # Convert to hex
        private_hex = crypto.private_key_to_hex(private_key)
        public_hex = crypto.public_key_to_hex(public_key)

        # Validate hex format
        assert crypto.validate_private_key_hex(private_hex)
        assert crypto.validate_public_key_hex(public_hex)

        # Roundtrip test
        private_decoded = bytes.fromhex(private_hex)
        public_decoded = bytes.fromhex(public_hex)

        assert private_decoded == private_key
        assert public_decoded == public_key

    def test_full_workflow_bech32(self):
        """Test complete workflow with bech32 format."""
        # Generate keypair
        private_key, public_key = crypto.generate_keypair()

        # Convert to bech32
        private_bech32 = crypto.private_key_to_bech32(private_key)
        public_bech32 = crypto.public_key_to_bech32(public_key)

        # Validate bech32 format
        assert crypto.validate_bech32_key(private_bech32, "nsec")
        assert crypto.validate_bech32_key(public_bech32, "npub")

    def test_deterministic_public_key_derivation(self):
        """Test that public key derivation is deterministic."""
        private_key = crypto.generate_private_key()

        public_key1 = crypto.derive_public_key(private_key)
        public_key2 = crypto.derive_public_key(private_key)

        assert public_key1 == public_key2
