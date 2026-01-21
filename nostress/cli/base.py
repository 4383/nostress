"""Common CLI utilities and base functionality."""

import sys
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ..exceptions import NostressError

# Global console instances for consistent output
console = Console()
console_err = Console(stderr=True)


def echo_info(message: str) -> None:
    """Print info message to stdout.

    Args:
        message: Message to display
    """
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def echo_success(message: str) -> None:
    """Print success message to stdout.

    Args:
        message: Message to display
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def echo_warning(message: str) -> None:
    """Print warning message to stderr.

    Args:
        message: Message to display
    """
    console_err.print(f"[bold yellow]⚠[/bold yellow] {message}")


def echo_error(message: str) -> None:
    """Print error message to stderr.

    Args:
        message: Message to display
    """
    console_err.print(f"[bold red]✗[/bold red] {message}")


def confirm_action(message: str, default: bool = False) -> bool:
    """Prompt user for confirmation.

    Args:
        message: Confirmation message
        default: Default value if user presses enter

    Returns:
        bool: True if confirmed
    """
    return typer.confirm(message, default=default)


def get_password(prompt: str = "Password: ", confirm: bool = False) -> str:
    """Securely get password from user input.

    Args:
        prompt: Password prompt
        confirm: Whether to ask for confirmation

    Returns:
        str: Password entered by user
    """
    import getpass

    password = getpass.getpass(prompt)
    if confirm:
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            raise typer.BadParameter("Passwords don't match")

    return password


def handle_exception(exc: Exception, verbose: bool = False) -> None:
    """Handle and display exceptions appropriately.

    Args:
        exc: Exception to handle
        verbose: Whether to show detailed error info
    """
    if isinstance(exc, NostressError):
        echo_error(str(exc))
        if verbose:
            import traceback

            console_err.print("[dim]" + traceback.format_exc() + "[/dim]")
    else:
        if verbose:
            import traceback

            echo_error(f"Unexpected error: {exc}")
            console_err.print("[dim]" + traceback.format_exc() + "[/dim]")
        else:
            echo_error(f"Unexpected error: {exc}")

    sys.exit(1)


def validate_output_path(path: str) -> Path:
    """Validate and return output file path.

    Args:
        path: File path to validate

    Returns:
        Path: Validated path object

    Raises:
        typer.BadParameter: If path is invalid
    """
    output_path = Path(path)

    # Check if parent directory exists
    if not output_path.parent.exists():
        raise typer.BadParameter(f"Directory does not exist: {output_path.parent}")

    # Check if file already exists and warn
    if output_path.exists() and not confirm_action(
        f"File {path} already exists. Overwrite?", default=False
    ):
        echo_info("Operation cancelled")
        sys.exit(0)

    return output_path


def write_output(content: str, output_path: Path | None = None) -> None:
    """Write content to file or stdout.

    Args:
        content: Content to write
        output_path: Optional file path, stdout if None
    """
    if output_path:
        try:
            output_path.write_text(content)
            echo_success(f"Output written to {output_path}")
        except OSError as e:
            echo_error(f"Failed to write to {output_path}: {e}")
            sys.exit(1)
    else:
        console.print(content)


def create_key_panel(title: str, content: dict[str, Any], style: str = "blue") -> Panel:
    """Create a formatted panel for displaying key information.

    Args:
        title: Panel title
        content: Key-value pairs to display
        style: Panel border style

    Returns:
        Panel: Formatted panel
    """
    text = Text()

    for key, value in content.items():
        text.append(f"{key}: ", style="bold")
        text.append(f"{value}\n")

    return Panel(text, title=title, border_style=style, padding=(1, 2))


def format_keypair_output(
    private_key: str, public_key: str, format_name: str, verbose: bool = False
) -> str:
    """Format keypair for output.

    Args:
        private_key: Private key string
        public_key: Public key string
        format_name: Format name (hex, bech32)
        verbose: Whether to include verbose info

    Returns:
        str: Formatted output
    """
    if verbose:
        # Create rich formatted output
        content = {
            "Private Key": private_key,
            "Public Key": public_key,
            "Format": format_name.upper(),
        }
        panel = create_key_panel("Generated Keypair", content)
        with Console() as temp_console:
            with temp_console.capture() as capture:
                temp_console.print(panel)
            return capture.get()
    else:
        # Simple output format
        return f"Private Key: {private_key}\nPublic Key: {public_key}"
