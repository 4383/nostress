"""Output formatting utilities."""

import json
from typing import Any

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table


def format_as_json(data: dict[str, Any], pretty: bool = True) -> str:
    """Format data as JSON string.

    Args:
        data: Data to format
        pretty: Whether to pretty-print

    Returns:
        str: JSON formatted string
    """
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def format_as_table(data: dict[str, Any], title: str | None = None) -> Table:
    """Format data as Rich table.

    Args:
        data: Data to format as key-value pairs
        title: Optional table title

    Returns:
        Table: Rich table object
    """
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")

    for key, value in data.items():
        table.add_row(key, str(value))

    return table


def format_keypair_table(private_key: str, public_key: str, format_type: str) -> Table:
    """Create a formatted table for keypair display.

    Args:
        private_key: Private key string
        public_key: Public key string
        format_type: Key format (hex, bech32)

    Returns:
        Table: Formatted keypair table
    """
    table = Table(title="Generated Keypair", show_header=True, header_style="bold blue")
    table.add_column("Key Type", style="cyan", no_wrap=True, width=12)
    table.add_column("Value", style="white", overflow="fold")

    table.add_row("Private Key", f"[red]{private_key}[/red]")
    table.add_row("Public Key", f"[green]{public_key}[/green]")
    table.add_row("Format", f"[yellow]{format_type.upper()}[/yellow]")

    return table


def create_info_panel(title: str, content: str, style: str = "blue") -> Panel:
    """Create an information panel.

    Args:
        title: Panel title
        content: Panel content
        style: Border style

    Returns:
        Panel: Rich panel object
    """
    return Panel(content, title=title, border_style=style, padding=(1, 2))


def print_json_pretty(data: dict[str, Any], console: Console | None = None) -> None:
    """Print JSON data with syntax highlighting.

    Args:
        data: Data to print
        console: Optional console instance
    """
    if console is None:
        console = Console()

    json_obj = JSON(json.dumps(data, indent=2))
    console.print(json_obj)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate string to specified length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
