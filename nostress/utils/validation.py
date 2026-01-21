"""Input validation utilities."""

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

import typer

from ..exceptions import ValidationError


def validate_file_path(
    path: str, must_exist: bool = False, must_not_exist: bool = False
) -> Path:
    """Validate file path.

    Args:
        path: File path to validate
        must_exist: Whether file must exist
        must_not_exist: Whether file must not exist

    Returns:
        Path: Validated path object

    Raises:
        ValidationError: If validation fails
    """
    try:
        path_obj = Path(path).expanduser().resolve()

        if must_exist and not path_obj.exists():
            raise ValidationError(f"File does not exist: {path}")

        if must_not_exist and path_obj.exists():
            raise ValidationError(f"File already exists: {path}")

        # Check parent directory exists
        if not path_obj.parent.exists():
            raise ValidationError(f"Directory does not exist: {path_obj.parent}")

        return path_obj
    except (OSError, ValueError) as e:
        raise ValidationError(f"Invalid file path: {e}") from e


def validate_key_format(format_str: str) -> str:
    """Validate key format string.

    Args:
        format_str: Format string to validate

    Returns:
        str: Validated format string

    Raises:
        ValidationError: If format is invalid
    """
    valid_formats = {"hex", "bech32", "both"}
    format_lower = format_str.lower()

    if format_lower not in valid_formats:
        raise ValidationError(
            f"Invalid format '{format_str}'. Must be one of: {', '.join(valid_formats)}"
        )

    return format_lower


def validate_hex_string(hex_str: str, expected_length: int | None = None) -> str:
    """Validate hexadecimal string.

    Args:
        hex_str: Hex string to validate
        expected_length: Expected length in characters

    Returns:
        str: Validated hex string

    Raises:
        ValidationError: If validation fails
    """
    # Remove any whitespace
    hex_str = hex_str.strip()

    # Check if it's a valid hex string
    if not re.match(r"^[0-9a-fA-F]+$", hex_str):
        raise ValidationError(f"Invalid hexadecimal string: {hex_str}")

    # Check length if specified
    if expected_length is not None and len(hex_str) != expected_length:
        raise ValidationError(
            f"Hex string must be {expected_length} characters long, got {len(hex_str)}"
        )

    return hex_str.lower()


def validate_bech32_string(bech32_str: str, expected_prefix: str | None = None) -> str:
    """Validate bech32 string.

    Args:
        bech32_str: Bech32 string to validate
        expected_prefix: Expected prefix (nsec, npub)

    Returns:
        str: Validated bech32 string

    Raises:
        ValidationError: If validation fails
    """
    bech32_str = bech32_str.strip()

    # Basic format check
    if not re.match(r"^[a-z0-9]+$", bech32_str):
        raise ValidationError(f"Invalid bech32 format: {bech32_str}")

    # Check prefix if specified
    if expected_prefix is not None and not bech32_str.startswith(expected_prefix):
        prefix_part = bech32_str[: len(expected_prefix)]
        raise ValidationError(
            f"Expected prefix '{expected_prefix}', got: {prefix_part}"
        )

    return bech32_str


def create_validator(validation_func: Callable[[str], Any]) -> Callable[[str], Any]:
    """Create a typer-compatible validator function.

    Args:
        validation_func: Function that validates and returns the value

    Returns:
        Callable: Typer-compatible validator
    """

    def validator(value: str) -> Any:
        try:
            return validation_func(value)
        except ValidationError as e:
            raise typer.BadParameter(str(e)) from e

    return validator


# Pre-built validators for common use cases
validate_hex_private_key = create_validator(
    lambda x: validate_hex_string(x, expected_length=64)
)

validate_hex_public_key = create_validator(
    lambda x: validate_hex_string(x, expected_length=64)
)

validate_bech32_private_key = create_validator(
    lambda x: validate_bech32_string(x, expected_prefix="nsec")
)

validate_bech32_public_key = create_validator(
    lambda x: validate_bech32_string(x, expected_prefix="npub")
)

validate_output_file = create_validator(
    lambda x: validate_file_path(x, must_exist=False)
)


def validate_password_strength(password: str, min_length: int = 8) -> str:
    """Validate password strength.

    Args:
        password: Password to validate
        min_length: Minimum required length

    Returns:
        str: Validated password

    Raises:
        ValidationError: If password is too weak
    """
    if len(password) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters long")

    # Check for at least one digit and one letter
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)

    if not (has_digit and has_letter):
        raise ValidationError("Password must contain at least one letter and one digit")

    return password
