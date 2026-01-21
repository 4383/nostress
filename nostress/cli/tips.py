"""Tips and sponsorship commands for supporting Nostr development."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..cli.base import (
    console_err,
    echo_error,
    echo_info,
    echo_success,
    validate_output_path,
    write_output,
)
from ..utils.output import format_as_json

# Create tips subcommand app
app = typer.Typer(
    help="Tips and sponsorship information for supporting Nostr development"
)
console = Console()


@app.command()
def show(
    format: str = typer.Option(
        "rich",
        "--format",
        "-f",
        help="Output format: rich, table, json, or text",
        metavar="FORMAT",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Save output to file instead of displaying",
        metavar="FILE",
    ),
    qr: bool = typer.Option(
        False,
        "--qr",
        help="Include QR codes for easy scanning (requires rich format)",
    ),
) -> None:
    """Display tips and sponsorship information.

    Shows available ways to support Nostr development through Lightning Network zaps,
    Bitcoin donations, and sponsorship options. Perfect for sharing with users who
    want to support the project.

    Examples:
        nostress tips show
        nostress tips show --format json
        nostress tips show --output support.txt
        nostress tips show --qr --format rich
    """
    try:
        # Get verbose mode from environment variable
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        # Validate format
        valid_formats = ["rich", "table", "json", "text"]
        if format not in valid_formats:
            echo_error(
                f"Invalid format '{format}'. Valid options: {', '.join(valid_formats)}"
            )
            raise typer.Exit(1) from None

        # QR codes only work with rich format
        if qr and format != "rich":
            echo_error("--qr flag requires --format rich")
            echo_info("QR codes can only be displayed in rich terminal format")
            raise typer.Exit(1) from None

        # Validate output path if provided
        output_path = None
        if output:
            try:
                output_path = validate_output_path(output)
            except typer.BadParameter as e:
                echo_error(str(e))
                raise typer.Exit(1) from None

        if verbose:
            echo_info("Preparing support and sponsorship information...")

        # Tips and sponsorship data
        tips_data = {
            "project": "nostress - Modern Python CLI for Nostr",
            "developer": "hberaud",
            "lightning_address": "hberaud@nostrcheck.me",
            # pragma: allowlist secret
            "nostr_pubkey": (
                "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            ),
            "github_repo": "https://github.com/4383/nostress",
            "description": "Support Nostr ecosystem development through Lightning zaps",
            "support_methods": [
                "Lightning Network zaps ⚡",
                "Follow on Nostr 🫂",
                "Direct contributions 🔧",
            ],
        }

        # Format output based on requested format
        if format == "json":
            content = format_as_json(tips_data, pretty=True)
            if not output:
                console.print_json(data=tips_data)

        elif format == "rich":
            # Create rich panels and tables
            title_panel = Panel(
                f"[bold cyan]{tips_data['project']}[/bold cyan]\n"
                f"[dim]{tips_data['description']}[/dim]",
                title="🚀 Support Nostr Development",
                border_style="cyan",
            )
            console.print(title_panel)
            console.print()

            # Lightning section
            lightning_panel = Panel(
                f"[bold yellow]⚡ Lightning Address:[/bold yellow]\n"
                f"[green]{tips_data['lightning_address']}[/green]\n\n"
                f"[dim]Send zaps directly through any "
                f"Lightning-enabled Nostr client[/dim]",
                title="Lightning Network Zaps",
                border_style="yellow",
            )
            console.print(lightning_panel)
            console.print()

            # Nostr section
            nostr_panel = Panel(
                f"[bold cyan]🫂 Follow on Nostr:[/bold cyan]\n"
                f"[green]{tips_data['nostr_pubkey']}[/green]\n\n"
                f"[dim]Follow the developer on Nostr for updates and zaps[/dim]",
                title="Nostr Public Key",
                border_style="cyan",
            )
            console.print(nostr_panel)
            console.print()

            # QR codes placeholder (would need qrcode library)
            if qr:
                console.print(
                    "[dim]🔍 QR code generation requires 'qrcode' package[/dim]"
                )
                console.print(
                    "[dim]Run: pip install qrcode[pil] to enable QR codes[/dim]"
                )

            if output:
                # For file output, create a text version
                content = (
                    f"{tips_data['project']}\n"
                    f"{tips_data['description']}\n\n"
                    f"Lightning Address: {tips_data['lightning_address']}\n"
                    f"Nostr Public Key: {tips_data['nostr_pubkey']}\n"
                    f"GitHub Repository: {tips_data['github_repo']}\n"
                )
            else:
                return  # Already displayed

        elif format == "table":
            # Create a clean table
            table = Table(
                title="Support Nostress Development",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Method", style="bold")
            table.add_column("Address/Link", style="green")
            table.add_column("Description", style="dim")

            table.add_row(
                "⚡ Lightning Zaps",
                tips_data["lightning_address"],
                "Send zaps through Nostr clients",
            )
            table.add_row(
                "🫂 Follow on Nostr",
                tips_data["nostr_pubkey"],
                "Follow for updates and zaps",
            )

            if not output:
                console.print(table)

            if output:
                # Convert table to text for file output
                content = (
                    "Support Nostress Development\n"
                    "=" * 50 + "\n\n"
                    f"Lightning Zaps: {tips_data['lightning_address']}\n"
                    f"Follow on Nostr: {tips_data['nostr_pubkey']}\n"
                )
            else:
                return  # Already displayed

        else:  # text format
            content = (
                f"Nostress - Support Development\n"
                f"{'=' * 30}\n\n"
                f"Lightning: {tips_data['lightning_address']}\n"
                f"Nostr: {tips_data['nostr_pubkey']}\n"
            )

            if not output:
                console.print(content)

        # Write to file if output specified
        if output and "content" in locals():
            write_output(content, output_path)
            echo_success(f"Support information saved to {output_path}")
        elif not output:
            echo_success("Support information displayed")

    except typer.Exit:
        raise
    except Exception as e:
        echo_error(f"Error displaying tips: {e}")
        if verbose:
            console_err.print_exception()
        raise typer.Exit(1) from None


@app.command()
def lightning(
    format: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format: text or json",
        metavar="FORMAT",
    ),
) -> None:
    """Display Lightning Network address for zaps.

    Shows just the Lightning Network address for quick copying or sharing.
    Perfect for adding to documentation or sharing in Nostr posts.

    Examples:
        nostress tips lightning
        nostress tips lightning --format json
    """
    try:
        # Get verbose mode
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        lightning_address = "hberaud@nostrcheck.me"

        if format == "json":
            data = {"lightning_address": lightning_address}
            console.print_json(data=data)
        else:
            console.print(f"⚡ {lightning_address}")

        if verbose:
            echo_info("Lightning address displayed")

    except Exception as e:
        echo_error(f"Error displaying lightning address: {e}")
        raise typer.Exit(1) from None


@app.command()
def nostr(
    format: str = typer.Option(
        "text",
        "--format",
        "-f",
        help="Output format: text or json",
        metavar="FORMAT",
    ),
) -> None:
    """Display Nostr public key for following.

    Shows the developer's Nostr public key for following and zapping.

    Examples:
        nostress tips nostr
        nostress tips nostr --format json
    """
    try:
        # Get verbose mode
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        # pragma: allowlist secret
        nostr_pubkey = "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"

        if format == "json":
            data = {"nostr_pubkey": nostr_pubkey}
            console.print_json(data=data)
        else:
            console.print(f"🫂 {nostr_pubkey}")

        if verbose:
            echo_info("Nostr public key displayed")

    except Exception as e:
        echo_error(f"Error displaying nostr public key: {e}")
        raise typer.Exit(1) from None


@app.command()
def logo(
    plain: bool = typer.Option(
        False,
        "--plain",
        "-p",
        help="Display plain text without colors",
    ),
    output: str | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Save logo to file instead of displaying",
        metavar="FILE",
    ),
) -> None:
    """Display the Nostress ASCII art logo.

    Shows the beautiful ASCII art logo with lightning-themed colors.
    Perfect for documentation, presentations, or just admiring the artwork!

    Examples:
        nostress tips logo
        nostress tips logo --plain
        nostress tips logo --output logo.txt
    """
    try:
        # Get verbose mode
        import os

        verbose = os.environ.get("NOSTRESS_VERBOSE", "").strip() == "1"

        # The ASCII art logo
        logo_art = """

                                      +*:
                                      @::@ -:
                                    :@:::@:@:@+
                            +:::::#@:-==+@@::@::
                       :*@@:::::-========---+#@:#
                    =%@:-==================----@:
                 :-=@:========================:@:
               =@:===@=======================--:*=
               =:=======+====+======++=========-=:@#
               :@:+*============+%%-::::@%=====---:%
:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:
:@@..@%.#@@@@@@@@@@@@@@..@@. @@@@@@@@@@@@@+=======@==@@@@:
:::@@.:@-.@@@@@@@@@@@%@%=@@..@@..@@@@@@@@@@:*======-#:  :@@@-
  :++*#=**==@@@@@@@@#::-=****==**+%@@@@@@**:+=======:*
    :@%.*@..@@@@@@@@::----=@@..@@.#@@@@@@-:@=======@:@
      -@@@@@@@@@@.:---+**@---@@@@@@@@@@#:-@=========:@:
       :@@%:::::---------------=*@@#*@%+============::@+
      :@:-+-------------------=++++++--=@============-:
       @=++=++++++++++++#@@#+-------+++--@========+-#::
         ::@#++++=-=%@%#++++++++--=+@@@@+=======+++-@:%
            %:::=    :@-+***++*@@%@*+=========++++:#-
                       :@-++++**+==+=====+==+++++-@:
                         +:@#-+++++++++*#*+++++%-:@
                             --@@=++++++++++++++-%:
                               *-*******++++++++-@#
                               :@+*****++++++++-=:
                               #@+++*++++++++++-@-
                               -@++*++====++++---
                               :@++=======++++-@-
                               =-+========+++--#
                              =@==========+++-@:
                              --==========+++-@
                             -@:=========+++++:


"""

        if plain or output:
            # Plain text version
            content = logo_art
        else:
            # Colorized version with Rich
            if verbose:
                echo_info("Displaying colorized Nostress logo...")

            # Create colorized version - use yellow/orange for lightning effect
            colorized_lines = []
            for line in logo_art.split("\n"):
                if any(char in line for char in ["*", "+", "=", "-", "@", ":"]):
                    # Lightning/energy parts in yellow/orange
                    colored_line = line
                    # Color the main symbols
                    colored_line = colored_line.replace(
                        "*", "[bold yellow]*[/bold yellow]"
                    )
                    colored_line = colored_line.replace("+", "[yellow]+[/yellow]")
                    colored_line = colored_line.replace("=", "[orange3]=[/orange3]")
                    colored_line = colored_line.replace("-", "[red]-[/red]")
                    colored_line = colored_line.replace("@", "[bold cyan]@[/bold cyan]")
                    colored_line = colored_line.replace(":", "[blue]:[/blue]")
                    colored_line = colored_line.replace("#", "[magenta]#[/magenta]")
                    colored_line = colored_line.replace("%", "[green]%[/green]")
                    colorized_lines.append(colored_line)
                else:
                    colorized_lines.append(line)

            if not output:
                console.print("\n".join(colorized_lines))
                if verbose:
                    echo_info("⚡ Nostress - Lightning-fast Nostr CLI")
                return
            else:
                content = logo_art  # Save plain version to file

        # Handle file output
        if output:
            try:
                output_path = validate_output_path(output)
                write_output(content, output_path)
                echo_success(f"Logo saved to {output_path}")
            except typer.BadParameter as e:
                echo_error(str(e))
                raise typer.Exit(1) from None
        else:
            # Plain text display
            console.print(content)

        if verbose and not output:
            echo_info("ASCII art logo displayed")

    except typer.Exit:
        raise
    except Exception as e:
        echo_error(f"Error displaying logo: {e}")
        if verbose:
            console_err.print_exception()
        raise typer.Exit(1) from None


# Allow running module directly for testing
if __name__ == "__main__":
    app()
