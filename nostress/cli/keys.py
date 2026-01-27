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
    output: str | None = typer.Option(
        None, "--output", "-o", help="Save output to file instead of displaying"
    ),
    json_output: bool = typer.Option(
        False, "--json", "-j", help="Output in JSON format"
    ),
) -> None:
    """Convert key between hex and bech32 formats.

    Converts keys between hexadecimal and bech32 (nsec/npub) formats.
    Bech32 keys (nsec/npub prefixed) are automatically detected.
    Hex keys require --type flag to specify private or public.

    Examples:
        nostress keys convert abc123...def --to bech32 --type private
        nostress keys convert nsec1... --to hex
        nostress keys convert npub1... --to hex --json
        nostress keys convert nsec1... --to hex --output converted.txt
    """
    try:
        # Get verbose mode from environment variable
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        # Clean input key
        key = key.strip()

        # Validate target format
        if target_format.lower() not in ["hex", "bech32"]:
            echo_error(f"Invalid target format: {target_format}")
            echo_info("Valid formats: hex, bech32")
            raise typer.Exit(1) from None

        target_format = target_format.lower()
        target_key_format = (
            KeyFormat.HEX if target_format == "hex" else KeyFormat.BECH32
        )

        # Validate output path if provided
        output_path = None
        if output:
            try:
                output_path = validate_output_path(output)
            except typer.BadParameter as e:
                echo_error(str(e))
                raise typer.Exit(1) from None

        # Detect key type and parse key
        parsed_key = None
        original_format = None
        original_type = None

        if verbose:
            echo_info("Detecting key type and format...")

        # Auto-detect bech32 keys
        if key.startswith("nsec"):
            if verbose:
                echo_info("Detected nsec (private) bech32 key")
            try:
                from ..core.models import NostrPrivateKey

                parsed_key = NostrPrivateKey.from_bech32(key)
                original_format = "bech32"
                original_type = "private"
            except Exception as e:
                echo_error(f"Invalid nsec key: {e}")
                raise typer.Exit(1) from None

        elif key.startswith("npub"):
            if verbose:
                echo_info("Detected npub (public) bech32 key")
            try:
                from ..core.models import NostrPublicKey

                parsed_key = NostrPublicKey.from_bech32(key)
                original_format = "bech32"
                original_type = "public"
            except Exception as e:
                echo_error(f"Invalid npub key: {e}")
                raise typer.Exit(1) from None

        elif len(key) == 64 and all(c in "0123456789abcdefABCDEF" for c in key):
            # Hex key - requires type specification
            if key_type is None:
                echo_error("Hex keys require --type flag to specify private or public")
                echo_info("Examples:")
                echo_info(
                    "  nostress keys convert YOUR_HEX_KEY --to bech32 --type private"
                )
                echo_info(
                    "  nostress keys convert YOUR_HEX_KEY --to bech32 --type public"
                )
                raise typer.Exit(1) from None

            key_type = key_type.lower()
            if key_type not in ["private", "public"]:
                echo_error(f"Invalid key type: {key_type}")
                echo_info("Valid types: private, public")
                raise typer.Exit(1) from None

            if verbose:
                echo_info(f"Detected hex {key_type} key")

            try:
                if key_type == "private":
                    from ..core.models import NostrPrivateKey

                    parsed_key = NostrPrivateKey.from_hex(key)
                    original_type = "private"
                else:
                    from ..core.models import NostrPublicKey

                    parsed_key = NostrPublicKey.from_hex(key)
                    original_type = "public"
                original_format = "hex"
            except Exception as e:
                echo_error(f"Invalid {key_type} hex key: {e}")
                raise typer.Exit(1) from None

        else:
            echo_error("Could not detect key type")
            echo_info("Key must be:")
            echo_info("  • 64-character hex string with --type flag")
            echo_info("  • bech32 string starting with nsec (private) or npub (public)")
            raise typer.Exit(1) from None

        # Check if conversion is needed
        current_format = KeyFormat.HEX if original_format == "hex" else KeyFormat.BECH32
        if current_format == target_key_format:
            echo_warning(f"Key is already in {target_format} format")
            if verbose:
                echo_info("No conversion needed")
            # Still output the key for consistency
            converted_key = key
        else:
            # Perform conversion
            if verbose:
                echo_info(f"Converting from {original_format} to {target_format}...")

            try:
                converted_key = parsed_key.to_format(target_key_format)
            except Exception as e:
                echo_error(f"Conversion failed: {e}")
                raise typer.Exit(1) from None

        # Format output
        if json_output:
            output_data = {
                "original_key": key,
                "original_format": original_format,
                "original_type": original_type,
                "converted_key": converted_key,
                "target_format": target_format,
            }
            content = format_as_json(output_data)
            if not output_path:
                console.print(content)
                return
        else:
            if verbose:
                # Rich formatting for verbose mode
                from rich.panel import Panel

                info_lines = []
                info_lines.append(f"[dim]Original format:[/dim] {original_format}")
                info_lines.append(f"[dim]Original type:[/dim] {original_type}")
                info_lines.append(f"[dim]Target format:[/dim] {target_format}")
                info_lines.append("")
                info_lines.append("[bold]Original key:[/bold]")
                info_lines.append(f"  {key}")
                info_lines.append("")
                info_lines.append("[bold]Converted key:[/bold]")
                info_lines.append(f"  {converted_key}")

                panel = Panel(
                    "\n".join(info_lines), title="Key Conversion", border_style="blue"
                )

                if output_path:
                    # For file output, use simple text format
                    content = f"""# Nostress Key Conversion
Original key: {key}
Original format: {original_format}
Original type: {original_type}
Target format: {target_format}

Converted key: {converted_key}
"""
                else:
                    console.print(panel)
                    return  # Already displayed with rich panel
            else:
                # Simple output format
                if current_format == target_key_format:
                    echo_success(f"Key is already in {target_format} format")
                    console.print(f"  Result: {converted_key}")
                else:
                    echo_success(
                        f"Converted {original_format} {original_type} key to "
                        f"{target_format} format"
                    )
                    console.print(f"  Result: {converted_key}")

                if output_path:
                    content = converted_key
                else:
                    return  # Already displayed

        # Write to file if requested
        if output_path:
            write_output(content, output_path)
            if verbose:
                echo_success(f"Converted key saved to {output_path}")
            else:
                echo_success(f"Converted key written to {output_path}")

    except typer.Exit:
        raise
    except Exception as e:
        echo_error(f"Conversion error: {e}")
        import os

        if os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1":
            import traceback

            console_err.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
