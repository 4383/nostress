"""Shared pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sample_keys():
    """Provide sample keys for testing."""
    from nostress.core.crypto import (
        generate_keypair,
        private_key_to_bech32,
        private_key_to_hex,
        public_key_to_bech32,
        public_key_to_hex,
    )

    # Generate a test keypair
    private_key, public_key = generate_keypair()

    return {
        "private_key_bytes": private_key,
        "public_key_bytes": public_key,
        "private_key_hex": private_key_to_hex(private_key),
        "public_key_hex": public_key_to_hex(public_key),
        "private_key_bech32": private_key_to_bech32(private_key),
        "public_key_bech32": public_key_to_bech32(public_key),
    }


@pytest.fixture
def temp_output_file(tmp_path):
    """Provide a temporary file for output testing."""
    output_file = tmp_path / "test_output.txt"
    yield output_file
    # Cleanup happens automatically with tmp_path
