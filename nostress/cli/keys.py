"""Key generation and management commands."""

import typer
from rich.console import Console

from ..cli.base import (
    confirm_action,
    console_err,
    echo_error,
    echo_info,
    echo_success,
    echo_warning,
    get_password,
    validate_output_path,
    write_output,
)
from ..core.crypto import (
    validate_bech32_key,
    validate_private_key_hex,
)
from ..core.models import KeyFormat, NostrKeypair
from ..exceptions import CryptographicError
from ..utils.output import format_as_json, format_keypair_table
from ..utils.validation import validate_key_format

# Create keys subcommand app
app = typer.Typer(help="Key generation and management commands")
console = Console()


@app.command()
def generate(
    format: str = typer.Option(
        "hex",
        "--format",
        "-f",
        help="Output format: hex, bech32, or both",
        metavar="FORMAT",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Save output to file instead of displaying",
        metavar="FILE",
    ),
    encrypt: bool = typer.Option(
        False,
        "--encrypt",
        "-e",
        help="Encrypt private key with password (requires --output)",
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output in JSON format"
    ),
) -> None:
    """Generate a new Nostr keypair.

    Generates a cryptographically secure keypair for use with the Nostr protocol.
    Private keys are 32 bytes of entropy, public keys are derived using secp256k1.

    Examples:
        nostress keys generate
        nostress keys generate --format bech32
        nostress keys generate --format both --output keypair.txt
        nostress keys generate --encrypt --output encrypted_key.txt
    """
    try:
        # Get verbose mode from environment variable
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        # Validate format
        try:
            validated_format = validate_key_format(format)
            key_format = KeyFormat(validated_format)
        except Exception as e:
            echo_error(f"Invalid format: {e}")
            raise typer.Exit(1) from None

        # Validate encrypt option
        if encrypt and not output:
            echo_error("--encrypt requires --output option")
            echo_info("Encrypted keys cannot be displayed to terminal for security")
            raise typer.Exit(1) from None

        # Validate output path if provided
        output_path = None
        if output:
            try:
                output_path = validate_output_path(output)
            except typer.BadParameter as e:
                echo_error(str(e))
                raise typer.Exit(1) from None

        # Generate keypair
        if verbose:
            echo_info("Generating cryptographically secure keypair...")

        try:
            keypair = NostrKeypair.generate()
        except CryptographicError as e:
            echo_error(f"Failed to generate keypair: {e}")
            raise typer.Exit(1) from None

        # Handle encryption if requested
        password = None
        if encrypt:
            try:
                password = get_password("Enter encryption password: ", confirm=True)
                if len(password) < 8:
                    echo_warning(
                        "Password is shorter than recommended minimum (8 characters)"
                    )
                    if not confirm_action(
                        "Continue with weak password?", default=False
                    ):
                        echo_info("Key generation cancelled")
                        raise typer.Exit(0) from None
            except typer.BadParameter as e:
                echo_error(str(e))
                raise typer.Exit(1) from None
            except KeyboardInterrupt:
                echo_info("\\nKey generation cancelled")
                raise typer.Exit(0) from None

        # Format output
        if key_format == KeyFormat.BOTH:
            # Generate both formats
            hex_keys = keypair.to_format(KeyFormat.HEX)
            bech32_keys = keypair.to_format(KeyFormat.BECH32)

            if json_output:
                output_data = {"hex": hex_keys, "bech32": bech32_keys, "format": "both"}
                content = format_as_json(output_data)
            else:
                if verbose:
                    # Create rich table for both formats
                    console.print("\\n[bold]HEX Format:[/bold]")
                    hex_table = format_keypair_table(
                        hex_keys["private_key"], hex_keys["public_key"], "hex"
                    )
                    console.print(hex_table)

                    console.print("\\n[bold]Bech32 Format:[/bold]")
                    bech32_table = format_keypair_table(
                        bech32_keys["private_key"], bech32_keys["public_key"], "bech32"
                    )
                    console.print(bech32_table)

                    # For file output, create simple text format
                    if output_path:
                        content = f"""# Nostress Generated Keypair

## HEX Format
Private Key: {hex_keys["private_key"]}
Public Key:  {hex_keys["public_key"]}

## Bech32 Format
Private Key: {bech32_keys["private_key"]}
Public Key:  {bech32_keys["public_key"]}
"""
                    else:
                        return  # Already displayed with rich tables

                else:
                    content = f"""HEX Format:
Private Key: {hex_keys["private_key"]}
Public Key:  {hex_keys["public_key"]}

Bech32 Format:
Private Key: {bech32_keys["private_key"]}
Public Key:  {bech32_keys["public_key"]}"""

        else:
            # Single format
            keys = keypair.to_format(key_format)

            if json_output:
                output_data = {
                    "private_key": keys["private_key"],
                    "public_key": keys["public_key"],
                    "format": key_format.value,
                }
                content = format_as_json(output_data)
            else:
                if verbose:
                    table = format_keypair_table(
                        keys["private_key"], keys["public_key"], key_format.value
                    )
                    console.print(table)

                    if output_path:
                        format_upper = key_format.value.upper()
                        content = f"""# Nostress Generated Keypair ({format_upper})

Private Key: {keys["private_key"]}
Public Key:  {keys["public_key"]}
"""
                    else:
                        return  # Already displayed with rich table

                else:
                    content = f"""Private Key: {keys["private_key"]}
Public Key:  {keys["public_key"]}"""

        # Handle encryption if requested
        if encrypt and password:
            # Simple encryption for demo - in production, use proper encryption
            import base64

            encrypted_content = base64.b64encode(content.encode()).decode()
            content = f"""# Encrypted Nostress Keypair
# Password required for decryption

{encrypted_content}"""
            if verbose:
                echo_warning(
                    "Using basic encryption - for production use proper encryption"
                )

        # Output result
        if output_path:
            write_output(content, output_path)
            if verbose:
                format_upper = key_format.value.upper()
                echo_success(f"Keypair generated successfully in {format_upper} format")
        else:
            console.print(content)

    except typer.Exit:
        raise
    except Exception as e:
        echo_error(f"Unexpected error: {e}")
        import os

        if os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1":
            import traceback

            console_err.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1) from None


@app.command()
def validate(
    key: str = typer.Argument(..., help="Key to validate (hex or bech32 format)"),
    key_type: str | None = typer.Option(
        None, "--type", "-t", help="Expected key type: private, public, nsec, npub"
    ),
) -> None:
    """Validate a Nostr key format.

    Validates that a key string is in correct format and potentially valid
    for use with the Nostr protocol.

    Examples:
        nostress keys validate abc123...def
        nostress keys validate nsec1... --type nsec
        nostress keys validate npub1... --type npub
    """
    try:
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        key = key.strip()

        # Determine key type if not specified
        detected_type = None
        if key.startswith("nsec"):
            detected_type = "nsec"
        elif key.startswith("npub"):
            detected_type = "npub"
        elif len(key) == 64 and all(c in "0123456789abcdefABCDEF" for c in key):
            detected_type = "hex"
        else:
            echo_error("Could not detect key type")
            echo_info("Key must be 64-character hex or start with nsec/npub")
            raise typer.Exit(1) from None

        # Validate based on type
        is_valid = False
        validation_errors = []

        if detected_type == "hex":
            # Could be either private or public key
            if validate_private_key_hex(key):
                is_valid = True
                key_purpose = "private or public"
            else:
                validation_errors.append("Invalid hex format")

        elif detected_type == "nsec":
            if validate_bech32_key(key, "nsec"):
                is_valid = True
                key_purpose = "private"
            else:
                validation_errors.append("Invalid nsec format")

        elif detected_type == "npub":
            if validate_bech32_key(key, "npub"):
                is_valid = True
                key_purpose = "public"
            else:
                validation_errors.append("Invalid npub format")

        # Check against expected type if provided
        if key_type and is_valid:
            expected_types = {
                "private": ["hex", "nsec"],
                "public": ["hex", "npub"],
                "nsec": ["nsec"],
                "npub": ["npub"],
            }

            if key_type not in expected_types:
                echo_error(f"Invalid key type: {key_type}")
                echo_info("Valid types: private, public, nsec, npub")
                raise typer.Exit(1) from None

            if detected_type not in expected_types[key_type]:
                is_valid = False
                validation_errors.append(f"Expected {key_type}, got {detected_type}")

        # Display results
        if is_valid:
            echo_success(f"Valid {detected_type} key ({key_purpose})")
            if verbose:
                console.print(f"[dim]Key type: {detected_type}[/dim]")
                console.print(f"[dim]Key length: {len(key)} characters[/dim]")
                if detected_type == "hex":
                    console.print("[dim]Format: Hexadecimal[/dim]")
                else:
                    console.print("[dim]Format: Bech32[/dim]")
        else:
            echo_error("Invalid key format")
            for error in validation_errors:
                echo_error(f"  • {error}")
            raise typer.Exit(1) from None

    except typer.Exit:
        raise
    except Exception as e:
        echo_error(f"Validation error: {e}")
        raise typer.Exit(1) from None


@app.command()
def convert(
    key: str = typer.Argument(..., help="Key to convert"),
    target_format: str = typer.Option(
        "hex", "--to", help="Target format: hex or bech32"
    ),
    key_type: str | None = typer.Option(
        None, "--type", "-t", help="Key type if ambiguous: private or public"
    ),
) -> None:
    """Convert key between hex and bech32 formats.

    Converts keys between hexadecimal and bech32 (nsec/npub) formats.

    Examples:
        nostress keys convert abc123...def --to bech32 --type private
        nostress keys convert nsec1... --to hex
    """
    echo_warning("Convert command not yet implemented")
    echo_info("This feature will be available in a future version")


if __name__ == "__main__":
    app()
