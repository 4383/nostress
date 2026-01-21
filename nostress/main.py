"""Main CLI application entry point."""

import typer
from rich.console import Console
from rich.traceback import install

from . import __version__
from .cli.base import handle_exception
from .exceptions import NostressError

# Install rich traceback handler for better error display
install(show_locals=True)

# Create main application
app = typer.Typer(
    name="nostress",
    help=(
        "Modern Python CLI for Nostr interactions - "
        "key generation, event creation, and relay management"
    ),
    add_completion=False,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Global options
console = Console()


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"nostress version {__version__}")
        raise typer.Exit()


def verbose_callback(value: bool):
    """Set verbose mode."""
    if value:
        console.print("[dim]Verbose mode enabled[/dim]")
    return value


@app.callback()
def main_callback(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
) -> None:
    """Modern Python CLI for Nostr interactions.

    This CLI provides tools for:
    • Generating and managing Nostr keypairs
    • Creating and signing Nostr events
    • Interacting with Nostr relays
    """
    # Store global options - simplified approach without context
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")

    # Set a global variable for now (could use click.Context in future)
    import os

    if verbose:
        os.environ["NOSTRESS_VERBOSE"] = "1"


# Import and register command groups
from .cli import keys, tips  # noqa: E402

app.add_typer(keys.app, name="keys", help="Key generation and management commands")
app.add_typer(
    tips.app,
    name="tips",
    help="Tips and sponsorship information for supporting Nostr development",
)


def main() -> None:
    """Entry point for the CLI application."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        typer.Exit(1)
    except NostressError as e:
        # Get verbose setting from environment variable
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"
        handle_exception(e, verbose=verbose)
    except Exception as e:
        # Get verbose setting from environment variable
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"
        handle_exception(e, verbose=verbose)


if __name__ == "__main__":
    main()
