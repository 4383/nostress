"""Data models for keys and validation."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ..exceptions import KeyFormatError
from .crypto import (
    private_key_to_bech32,
    private_key_to_hex,
    public_key_to_bech32,
    public_key_to_hex,
    validate_bech32_key,
    validate_private_key_hex,
    validate_public_key_hex,
)


class KeyFormat(str, Enum):
    """Supported key formats."""

    HEX = "hex"
    BECH32 = "bech32"
    BOTH = "both"


class NostrPrivateKey(BaseModel):
    """Nostr private key with format validation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw: bytes = Field(..., description="Raw 32-byte private key")

    @field_validator("raw")
    @classmethod
    def validate_raw_key(cls, v):
        if not isinstance(v, bytes):
            raise ValueError("Private key must be bytes")
        if len(v) != 32:
            raise ValueError("Private key must be exactly 32 bytes")
        return v

    @property
    def hex(self) -> str:
        """Get private key in hex format."""
        return private_key_to_hex(self.raw)

    @property
    def bech32(self) -> str:
        """Get private key in bech32 nsec format."""
        return private_key_to_bech32(self.raw)

    def to_format(self, format: KeyFormat) -> str:
        """Convert key to specified format.

        Args:
            format: Target format (hex, bech32)

        Returns:
            str: Formatted key
        """
        if format == KeyFormat.HEX:
            return self.hex
        elif format == KeyFormat.BECH32:
            return self.bech32
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def from_hex(cls, hex_key: str) -> "NostrPrivateKey":
        """Create private key from hex string.

        Args:
            hex_key: Hex-encoded private key

        Returns:
            NostrPrivateKey instance

        Raises:
            KeyFormatError: If hex key is invalid
        """
        if not validate_private_key_hex(hex_key):
            raise KeyFormatError(f"Invalid hex private key: {hex_key}")
        return cls(raw=bytes.fromhex(hex_key))

    @classmethod
    def from_bech32(cls, bech32_key: str) -> "NostrPrivateKey":
        """Create private key from bech32 string.

        Args:
            bech32_key: Bech32-encoded private key (nsec...)

        Returns:
            NostrPrivateKey instance

        Raises:
            KeyFormatError: If bech32 key is invalid
        """
        if not validate_bech32_key(bech32_key, "nsec"):
            raise KeyFormatError(f"Invalid bech32 private key: {bech32_key}")

        # Extract and decode the base58 part
        import base58

        encoded_part = bech32_key[4:]  # Remove "nsec" prefix
        raw_bytes = base58.b58decode(encoded_part)
        return cls(raw=raw_bytes)


class NostrPublicKey(BaseModel):
    """Nostr public key with format validation."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    raw: bytes = Field(..., description="Raw 32-byte public key")

    @field_validator("raw")
    @classmethod
    def validate_raw_key(cls, v):
        if not isinstance(v, bytes):
            raise ValueError("Public key must be bytes")
        if len(v) != 32:
            raise ValueError("Public key must be exactly 32 bytes")
        return v

    @property
    def hex(self) -> str:
        """Get public key in hex format."""
        return public_key_to_hex(self.raw)

    @property
    def bech32(self) -> str:
        """Get public key in bech32 npub format."""
        return public_key_to_bech32(self.raw)

    def to_format(self, format: KeyFormat) -> str:
        """Convert key to specified format.

        Args:
            format: Target format (hex, bech32)

        Returns:
            str: Formatted key
        """
        if format == KeyFormat.HEX:
            return self.hex
        elif format == KeyFormat.BECH32:
            return self.bech32
        else:
            raise ValueError(f"Unsupported format: {format}")

    @classmethod
    def from_hex(cls, hex_key: str) -> "NostrPublicKey":
        """Create public key from hex string.

        Args:
            hex_key: Hex-encoded public key

        Returns:
            NostrPublicKey instance

        Raises:
            KeyFormatError: If hex key is invalid
        """
        if not validate_public_key_hex(hex_key):
            raise KeyFormatError(f"Invalid hex public key: {hex_key}")
        return cls(raw=bytes.fromhex(hex_key))

    @classmethod
    def from_bech32(cls, bech32_key: str) -> "NostrPublicKey":
        """Create public key from bech32 string.

        Args:
            bech32_key: Bech32-encoded public key (npub...)

        Returns:
            NostrPublicKey instance

        Raises:
            KeyFormatError: If bech32 key is invalid
        """
        if not validate_bech32_key(bech32_key, "npub"):
            raise KeyFormatError(f"Invalid bech32 public key: {bech32_key}")

        # Extract and decode the base58 part
        import base58

        encoded_part = bech32_key[4:]  # Remove "npub" prefix
        raw_bytes = base58.b58decode(encoded_part)
        return cls(raw=raw_bytes)


class NostrKeypair(BaseModel):
    """Complete Nostr keypair with private and public keys."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    private_key: NostrPrivateKey = Field(..., description="Private key")
    public_key: NostrPublicKey = Field(..., description="Public key")

    @field_validator("public_key")
    @classmethod
    def validate_keypair_consistency(cls, public_key, info):
        """Ensure public key matches private key."""
        if hasattr(info, "data") and "private_key" in info.data:
            from .crypto import derive_public_key

            expected_public = derive_public_key(info.data["private_key"].raw)
            if public_key.raw != expected_public:
                raise ValueError("Public key does not match private key")
        return public_key

    def to_format(self, format: KeyFormat) -> dict:
        """Convert both keys to specified format.

        Args:
            format: Target format (hex, bech32)

        Returns:
            dict: Keys in specified format
        """
        return {
            "private_key": self.private_key.to_format(format),
            "public_key": self.public_key.to_format(format),
        }

    @classmethod
    def generate(cls) -> "NostrKeypair":
        """Generate a new random keypair.

        Returns:
            NostrKeypair: New random keypair
        """
        from .crypto import generate_keypair

        private_raw, public_raw = generate_keypair()

        return cls(
            private_key=NostrPrivateKey(raw=private_raw),
            public_key=NostrPublicKey(raw=public_raw),
        )


class KeyGenerationOptions(BaseModel):
    """Options for key generation."""

    model_config = ConfigDict(use_enum_values=True)

    format: KeyFormat = Field(KeyFormat.HEX, description="Output format")
    output_file: str | None = Field(None, description="Output file path")
    encrypt: bool = Field(False, description="Encrypt private key")
    password: str | None = Field(None, description="Encryption password")
    verbose: bool = Field(False, description="Verbose output")
