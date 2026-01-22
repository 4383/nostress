"""Integration tests for CLI tips commands."""

import json
import re

from typer.testing import CliRunner

from nostress.main import app


def strip_ansi(text):
    """Remove ANSI escape sequences from text."""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


class TestTipsShow:
    """Test the tips show command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_show_default_rich_format(self):
        """Test tips show with default rich format."""
        result = self.runner.invoke(app, ["tips", "show"])

        assert result.exit_code == 0
        assert "🚀 Support Nostr Development" in result.stdout
        assert "nostress - Modern Python CLI for Nostr" in result.stdout
        assert (
            "Support Nostr ecosystem development through Lightning zaps"
            in result.stdout
        )
        assert "⚡ Lightning Address:" in result.stdout
        assert "hberaud@nostrcheck.me" in result.stdout
        assert "🫂 Follow on Nostr:" in result.stdout
        assert (
            "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )

    def test_show_table_format(self):
        """Test tips show with table format."""
        result = self.runner.invoke(app, ["tips", "show", "--format", "table"])

        assert result.exit_code == 0
        assert "Support Nostress Development" in result.stdout
        assert "Method" in result.stdout
        assert "Address/Link" in result.stdout
        assert "Description" in result.stdout
        assert "⚡ Lightning Zaps" in result.stdout
        assert "hberaud@nostrcheck.me" in result.stdout
        assert "🫂 Follow on Nostr" in result.stdout
        assert "npub1azaaxhlx3v8lex2gnyxz" in result.stdout  # Truncated in table format

    def test_show_json_format(self):
        """Test tips show with JSON format."""
        result = self.runner.invoke(app, ["tips", "show", "--format", "json"])

        assert result.exit_code == 0

        # Parse JSON output - extract JSON part, ignore success message
        lines = result.stdout.strip().split("\n")
        # Find JSON content (everything before the success message)
        json_lines = []
        for line in lines:
            if line.startswith("✓"):
                break
            json_lines.append(line)
        json_str = "\n".join(json_lines).strip()
        json_data = json.loads(json_str)

        assert json_data["project"] == "nostress - Modern Python CLI for Nostr"
        assert json_data["developer"] == "hberaud"
        assert json_data["lightning_address"] == "hberaud@nostrcheck.me"
        assert (
            json_data["nostr_pubkey"]
            == "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
        )
        assert json_data["github_repo"] == "https://github.com/4383/nostress"
        assert "description" in json_data
        assert "support_methods" in json_data
        assert isinstance(json_data["support_methods"], list)

    def test_show_text_format(self):
        """Test tips show with text format."""
        result = self.runner.invoke(app, ["tips", "show", "--format", "text"])

        assert result.exit_code == 0
        assert "Nostress - Support Development" in result.stdout
        assert "Lightning: hberaud@nostrcheck.me" in result.stdout
        assert (
            "Nostr: npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )
        assert "✓ Support information displayed" in result.stdout

    def test_show_with_qr_flag_rich_format(self):
        """Test tips show with QR flag (should show placeholder message)."""
        result = self.runner.invoke(app, ["tips", "show", "--qr"])

        assert result.exit_code == 0
        assert "QR code generation requires 'qrcode' package" in result.stdout

    def test_show_with_qr_flag_non_rich_format_error(self):
        """Test tips show with QR flag and non-rich format should error."""
        result = self.runner.invoke(app, ["tips", "show", "--format", "json", "--qr"])

        assert result.exit_code != 0
        assert "QR codes can only be displayed in rich terminal format" in result.stdout

    def test_show_invalid_format(self):
        """Test tips show with invalid format errors."""
        result = self.runner.invoke(app, ["tips", "show", "--format", "invalid"])

        # Invalid format should error
        assert result.exit_code == 1
        # Error messages go to stderr
        output = result.stdout + (result.stderr or "")
        assert "Invalid format 'invalid'" in output
        assert "Valid options: rich, table, json, text" in output

    def test_show_output_to_file(self, temp_output_file):
        """Test tips show output to file."""
        result = self.runner.invoke(
            app, ["tips", "show", "--format", "text", "--output", str(temp_output_file)]
        )

        assert result.exit_code == 0
        assert temp_output_file.exists()

        content = temp_output_file.read_text()
        assert "Nostress - Support Development" in content
        assert "Lightning: hberaud@nostrcheck.me" in content
        assert (
            "Nostr: npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in content
        )

    def test_show_output_to_existing_file_no_overwrite(self, temp_output_file):
        """Test tips show refuses to overwrite existing file without confirmation."""
        # Create existing file
        temp_output_file.write_text("existing content")

        result = self.runner.invoke(
            app,
            ["tips", "show", "--format", "text", "--output", str(temp_output_file)],
            input="n\n",  # Answer "no" to overwrite prompt
        )

        # Should exit with code 0 but not overwrite file
        assert result.exit_code == 0
        # Original content should be preserved
        assert temp_output_file.read_text() == "existing content"


class TestTipsLightning:
    """Test the tips lightning command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_lightning_default_text_format(self):
        """Test tips lightning with default text format."""
        result = self.runner.invoke(app, ["tips", "lightning"])

        assert result.exit_code == 0
        assert "hberaud@nostrcheck.me" in result.stdout

    def test_lightning_text_format_explicit(self):
        """Test tips lightning with explicit text format."""
        result = self.runner.invoke(app, ["tips", "lightning", "--format", "text"])

        assert result.exit_code == 0
        assert "hberaud@nostrcheck.me" in result.stdout

    def test_lightning_json_format(self):
        """Test tips lightning with JSON format."""
        result = self.runner.invoke(app, ["tips", "lightning", "--format", "json"])

        assert result.exit_code == 0

        json_data = json.loads(result.stdout.strip())
        assert json_data["lightning_address"] == "hberaud@nostrcheck.me"

    def test_lightning_invalid_format(self):
        """Test tips lightning with invalid format defaults to text."""
        result = self.runner.invoke(app, ["tips", "lightning", "--format", "invalid"])

        # Lightning command accepts invalid format and defaults to text
        assert result.exit_code == 0
        assert "hberaud@nostrcheck.me" in result.stdout


class TestTipsNostr:
    """Test the tips nostr command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_nostr_default_text_format(self):
        """Test tips nostr with default text format."""
        result = self.runner.invoke(app, ["tips", "nostr"])

        assert result.exit_code == 0
        assert (
            "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )

    def test_nostr_text_format_explicit(self):
        """Test tips nostr with explicit text format."""
        result = self.runner.invoke(app, ["tips", "nostr", "--format", "text"])

        assert result.exit_code == 0
        assert (
            "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )

    def test_nostr_json_format(self):
        """Test tips nostr with JSON format."""
        result = self.runner.invoke(app, ["tips", "nostr", "--format", "json"])

        assert result.exit_code == 0

        json_data = json.loads(result.stdout.strip())
        assert (
            json_data["nostr_pubkey"]
            == "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
        )

    def test_nostr_invalid_format(self):
        """Test tips nostr with invalid format defaults to text."""
        result = self.runner.invoke(app, ["tips", "nostr", "--format", "invalid"])

        # Nostr command accepts invalid format and defaults to text
        assert result.exit_code == 0
        assert (
            "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )


class TestTipsLogo:
    """Test the tips logo command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_logo_default_colored(self):
        """Test tips logo with default colored output."""
        result = self.runner.invoke(app, ["tips", "logo"])

        assert result.exit_code == 0
        # Check for ASCII art patterns (should contain typical ASCII characters)
        assert any(
            char in result.stdout for char in ["*", "#", "@", "+", "-", "|", "/"]
        )

    def test_logo_plain_output(self):
        """Test tips logo with plain (no color) output."""
        result = self.runner.invoke(app, ["tips", "logo", "--plain"])

        assert result.exit_code == 0
        # Should contain ASCII art but without ANSI color codes
        assert any(
            char in result.stdout for char in ["*", "#", "@", "+", "-", "|", "/"]
        )
        # Check that there are no ANSI escape sequences (basic check)
        assert "\x1b[" not in result.stdout

    def test_logo_output_to_file(self, temp_output_file):
        """Test tips logo output to file."""
        result = self.runner.invoke(
            app, ["tips", "logo", "--output", str(temp_output_file)]
        )

        assert result.exit_code == 0
        assert temp_output_file.exists()

        content = temp_output_file.read_text()
        # File output should contain ASCII art
        assert any(char in content for char in ["*", "#", "@", "+", "-", "|", "/"])

    def test_logo_plain_output_to_file(self, temp_output_file):
        """Test tips logo plain output to file."""
        result = self.runner.invoke(
            app, ["tips", "logo", "--plain", "--output", str(temp_output_file)]
        )

        assert result.exit_code == 0
        assert temp_output_file.exists()

        content = temp_output_file.read_text()
        # Should contain ASCII art without color codes
        assert any(char in content for char in ["*", "#", "@", "+", "-", "|", "/"])
        assert "\x1b[" not in content

    def test_logo_output_to_existing_file_no_overwrite(self, temp_output_file):
        """Test tips logo refuses to overwrite existing file without confirmation."""
        # Create existing file
        temp_output_file.write_text("existing content")

        result = self.runner.invoke(
            app,
            ["tips", "logo", "--output", str(temp_output_file)],
            input="n\n",  # Answer "no" to overwrite prompt
        )

        # Should exit with code 0 but not overwrite file
        assert result.exit_code == 0
        # Original content should be preserved
        assert temp_output_file.read_text() == "existing content"


class TestTipsCommandHelp:
    """Test tips command help and general functionality."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_tips_main_help(self):
        """Test main tips command help."""
        result = self.runner.invoke(app, ["tips", "--help"])

        assert result.exit_code == 0
        assert "Tips and sponsorship information" in result.stdout
        assert "show" in result.stdout
        assert "lightning" in result.stdout
        assert "nostr" in result.stdout
        assert "logo" in result.stdout

    def test_tips_show_help(self):
        """Test tips show command help."""
        result = self.runner.invoke(app, ["tips", "show", "--help"])

        assert result.exit_code == 0
        clean_output = strip_ansi(result.stdout)
        assert "--format" in clean_output
        assert "--output" in clean_output
        assert "--qr" in clean_output

    def test_tips_lightning_help(self):
        """Test tips lightning command help."""
        result = self.runner.invoke(app, ["tips", "lightning", "--help"])

        assert result.exit_code == 0
        clean_output = strip_ansi(result.stdout)
        assert "--format" in clean_output

    def test_tips_nostr_help(self):
        """Test tips nostr command help."""
        result = self.runner.invoke(app, ["tips", "nostr", "--help"])

        assert result.exit_code == 0
        clean_output = strip_ansi(result.stdout)
        assert "--format" in clean_output

    def test_tips_logo_help(self):
        """Test tips logo command help."""
        result = self.runner.invoke(app, ["tips", "logo", "--help"])

        assert result.exit_code == 0
        clean_output = strip_ansi(result.stdout)
        assert "--plain" in clean_output
        assert "--output" in clean_output

    def test_tips_no_subcommand(self):
        """Test tips command without subcommand shows error."""
        result = self.runner.invoke(app, ["tips"])

        assert result.exit_code == 2  # Missing command error
        # Check both stdout and stderr for the error message
        output = result.stdout + (result.stderr or "")
        clean_output = strip_ansi(output)
        assert "Missing command" in clean_output
        assert "nostress tips [OPTIONS] COMMAND [ARGS]" in clean_output
        assert "nostress tips -h" in clean_output


class TestTipsVerboseMode:
    """Test tips commands with verbose mode."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_tips_show_verbose_mode(self):
        """Test tips show with verbose mode."""
        result = self.runner.invoke(
            app, ["--verbose", "tips", "show", "--format", "text"]
        )

        assert result.exit_code == 0
        # Verbose mode should still work correctly
        assert "Verbose mode enabled" in result.stdout
        assert "Lightning: hberaud@nostrcheck.me" in result.stdout
        assert (
            "Nostr: npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )

    def test_tips_lightning_verbose_mode(self):
        """Test tips lightning with verbose mode."""
        result = self.runner.invoke(app, ["--verbose", "tips", "lightning"])

        assert result.exit_code == 0
        assert "hberaud@nostrcheck.me" in result.stdout

    def test_tips_nostr_verbose_mode(self):
        """Test tips nostr with verbose mode."""
        result = self.runner.invoke(app, ["--verbose", "tips", "nostr"])

        assert result.exit_code == 0
        assert (
            "npub1azaaxhlx3v8lex2gnyxzq8ws9nxsh8ga30d64jeaqxw4e75vxufqm434ty"
            in result.stdout
        )

    def test_tips_logo_verbose_mode(self):
        """Test tips logo with verbose mode."""
        result = self.runner.invoke(app, ["--verbose", "tips", "logo", "--plain"])

        assert result.exit_code == 0
        # Should still output logo
        assert any(
            char in result.stdout for char in ["*", "#", "@", "+", "-", "|", "/"]
        )
