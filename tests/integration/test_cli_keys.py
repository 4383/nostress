"""Integration tests for CLI key commands."""

import json
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from nostress.main import app


class TestKeysGenerate:
    """Test the keys generate command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_generate_default_hex(self):
        """Test default key generation (hex format)."""
        result = self.runner.invoke(app, ["keys", "generate"])

        assert result.exit_code == 0
        assert "Private Key:" in result.stdout
        assert "Public Key:" in result.stdout

        # Extract keys from output
        lines = result.stdout.strip().split("\n")
        private_line = next(line for line in lines if line.startswith("Private Key:"))
        public_line = next(line for line in lines if line.startswith("Public Key:"))

        private_key = private_line.split(": ")[1].strip()
        public_key = public_line.split(": ")[1].strip()

        # Validate hex format
        assert len(private_key) == 64
        assert len(public_key) == 64
        assert all(c in "0123456789abcdef" for c in private_key.lower())
        assert all(c in "0123456789abcdef" for c in public_key.lower())

    def test_generate_bech32_format(self):
        """Test key generation in bech32 format."""
        result = self.runner.invoke(app, ["keys", "generate", "--format", "bech32"])

        assert result.exit_code == 0
        assert "Private Key:" in result.stdout
        assert "Public Key:" in result.stdout
        assert "nsec" in result.stdout
        assert "npub" in result.stdout

    def test_generate_both_formats(self):
        """Test key generation with both formats."""
        result = self.runner.invoke(app, ["keys", "generate", "--format", "both"])

        assert result.exit_code == 0
        assert "Private Key:" in result.stdout
        assert "Public Key:" in result.stdout
        # Should contain both hex and bech32
        assert "nsec" in result.stdout
        assert "npub" in result.stdout

    def test_generate_json_output(self):
        """Test key generation with JSON output."""
        result = self.runner.invoke(app, ["keys", "generate", "--json"])

        assert result.exit_code == 0

        # Parse JSON output
        data = json.loads(result.stdout)
        assert "private_key" in data
        assert "public_key" in data
        assert "format" in data
        assert data["format"] == "hex"
        assert len(data["private_key"]) == 64
        assert len(data["public_key"]) == 64

    def test_generate_json_both_formats(self):
        """Test key generation with JSON output for both formats."""
        result = self.runner.invoke(
            app, ["keys", "generate", "--format", "both", "--json"]
        )

        assert result.exit_code == 0

        # Parse JSON output
        data = json.loads(result.stdout)
        assert "hex" in data
        assert "bech32" in data
        assert "format" in data
        assert data["format"] == "both"

        # Check hex format
        hex_data = data["hex"]
        assert len(hex_data["private_key"]) == 64
        assert len(hex_data["public_key"]) == 64

        # Check bech32 format
        bech32_data = data["bech32"]
        assert bech32_data["private_key"].startswith("nsec")
        assert bech32_data["public_key"].startswith("npub")

    def test_generate_to_file(self):
        """Test key generation with file output."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "test_output.txt"

            result = self.runner.invoke(
                app, ["keys", "generate", "--output", str(tmp_path)]
            )

            assert result.exit_code == 0

            # Read the file
            output_content = tmp_path.read_text()
            assert "Private Key:" in output_content
            assert "Public Key:" in output_content

    def test_generate_encrypt_without_output_fails(self):
        """Test that --encrypt requires --output."""
        result = self.runner.invoke(app, ["keys", "generate", "--encrypt"])

        assert result.exit_code == 1
        assert "--encrypt requires --output option" in result.stderr

    def test_generate_invalid_format(self):
        """Test key generation with invalid format."""
        result = self.runner.invoke(app, ["keys", "generate", "--format", "invalid"])

        assert result.exit_code == 1
        assert "Invalid format:" in result.stderr


class TestKeysValidate:
    """Test the keys validate command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_validate_hex_key(self):
        """Test validation of hex key."""
        # Generate a key first to get a valid one
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        private_key = data["private_key"]

        # Validate the generated key
        result = self.runner.invoke(app, ["keys", "validate", private_key])

        assert result.exit_code == 0
        assert "Valid hex key" in result.stdout

    def test_validate_bech32_nsec_key(self):
        """Test validation of bech32 nsec key."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        private_key = data["private_key"]

        # Validate the generated key
        result = self.runner.invoke(app, ["keys", "validate", private_key])

        assert result.exit_code == 0
        assert "Valid nsec key" in result.stdout

    def test_validate_bech32_npub_key(self):
        """Test validation of bech32 npub key."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        public_key = data["public_key"]

        # Validate the generated key
        result = self.runner.invoke(app, ["keys", "validate", public_key])

        assert result.exit_code == 0
        assert "Valid npub key" in result.stdout

    def test_validate_invalid_key(self):
        """Test validation of invalid key."""
        result = self.runner.invoke(app, ["keys", "validate", "invalid_key"])

        assert result.exit_code == 1
        assert "Could not detect key type" in result.stderr

    def test_validate_with_type_check(self):
        """Test validation with specific type check."""
        # Generate a key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        private_key = data["private_key"]  # nsec key

        # Validate with correct type
        result = self.runner.invoke(
            app, ["keys", "validate", private_key, "--type", "nsec"]
        )
        assert result.exit_code == 0

        # Validate with wrong type should fail
        result = self.runner.invoke(
            app, ["keys", "validate", private_key, "--type", "npub"]
        )
        assert result.exit_code == 1

    def test_validate_short_hex_key(self):
        """Test validation of too-short hex key."""
        result = self.runner.invoke(app, ["keys", "validate", "abc123"])

        assert result.exit_code == 1
        assert "Could not detect key type" in result.stderr

    def test_validate_invalid_hex_characters(self):
        """Test validation of hex key with invalid characters."""
        invalid_hex = "g" * 64  # 'g' is not a valid hex character
        result = self.runner.invoke(app, ["keys", "validate", invalid_hex])

        assert result.exit_code == 1
        assert "Could not detect key type" in result.stderr


class TestKeysConvert:
    """Test the keys convert command."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_convert_bech32_private_to_hex(self):
        """Test converting bech32 private key to hex."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        bech32_private = data["private_key"]

        # Convert to hex
        result = self.runner.invoke(
            app, ["keys", "convert", bech32_private, "--to", "hex"]
        )

        assert result.exit_code == 0
        assert "Converted bech32 private key to hex format" in result.stdout
        assert "Result:" in result.stdout

        # Extract the converted key
        lines = result.stdout.strip().split("\n")
        result_line = next(line for line in lines if line.strip().startswith("Result:"))
        hex_key = result_line.split(": ")[1].strip()

        # Verify hex format
        assert len(hex_key) == 64
        assert all(c in "0123456789abcdef" for c in hex_key.lower())

    def test_convert_bech32_public_to_hex(self):
        """Test converting bech32 public key to hex."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        bech32_public = data["public_key"]

        # Convert to hex
        result = self.runner.invoke(
            app, ["keys", "convert", bech32_public, "--to", "hex"]
        )

        assert result.exit_code == 0
        assert "Converted bech32 public key to hex format" in result.stdout
        assert "Result:" in result.stdout

    def test_convert_hex_private_to_bech32(self):
        """Test converting hex private key to bech32."""
        # Generate a hex key first
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        hex_private = data["private_key"]

        # Convert to bech32 with type specification
        result = self.runner.invoke(
            app, ["keys", "convert", hex_private, "--to", "bech32", "--type", "private"]
        )

        assert result.exit_code == 0
        assert "Converted hex private key to bech32 format" in result.stdout
        assert "Result:" in result.stdout

        # Extract the converted key
        lines = result.stdout.strip().split("\n")
        result_line = next(line for line in lines if line.strip().startswith("Result:"))
        bech32_key = result_line.split(": ")[1].strip()

        # Verify bech32 format
        assert bech32_key.startswith("nsec")

    def test_convert_hex_public_to_bech32(self):
        """Test converting hex public key to bech32."""
        # Generate a hex key first
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        hex_public = data["public_key"]

        # Convert to bech32 with type specification
        result = self.runner.invoke(
            app, ["keys", "convert", hex_public, "--to", "bech32", "--type", "public"]
        )

        assert result.exit_code == 0
        assert "Converted hex public key to bech32 format" in result.stdout

        # Extract the converted key
        lines = result.stdout.strip().split("\n")
        result_line = next(line for line in lines if line.strip().startswith("Result:"))
        bech32_key = result_line.split(": ")[1].strip()

        # Verify bech32 format
        assert bech32_key.startswith("npub")

    def test_convert_hex_without_type_fails(self):
        """Test that hex keys require --type flag."""
        # Generate a hex key first
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        hex_private = data["private_key"]

        # Try to convert without --type flag
        result = self.runner.invoke(
            app, ["keys", "convert", hex_private, "--to", "bech32"]
        )

        assert result.exit_code == 1
        assert "Hex keys require --type flag" in result.stderr
        assert "Examples:" in result.stdout

    def test_convert_invalid_key_type(self):
        """Test conversion with invalid key type."""
        result = self.runner.invoke(
            app, ["keys", "convert", "1" * 64, "--to", "bech32", "--type", "invalid"]
        )

        assert result.exit_code == 1
        assert "Invalid key type: invalid" in result.stderr
        assert "Valid types: private, public" in result.stdout

    def test_convert_invalid_target_format(self):
        """Test conversion with invalid target format."""
        result = self.runner.invoke(
            app, ["keys", "convert", "nsecabc123", "--to", "invalid"]
        )

        assert result.exit_code == 1
        assert "Invalid target format: invalid" in result.stderr
        assert "Valid formats: hex, bech32" in result.stdout

    def test_convert_invalid_key(self):
        """Test conversion with invalid key."""
        result = self.runner.invoke(
            app, ["keys", "convert", "invalid_key", "--to", "hex"]
        )

        assert result.exit_code == 1
        assert "Could not detect key type" in result.stderr

    def test_convert_invalid_bech32_key(self):
        """Test conversion with invalid bech32 key."""
        result = self.runner.invoke(
            app, ["keys", "convert", "nsec_invalid", "--to", "hex"]
        )

        assert result.exit_code == 1
        assert "Invalid nsec key" in result.stderr

    def test_convert_invalid_hex_key(self):
        """Test conversion with invalid hex key."""
        invalid_hex = "g" * 64  # 'g' is not a valid hex character
        result = self.runner.invoke(
            app, ["keys", "convert", invalid_hex, "--to", "bech32", "--type", "private"]
        )

        assert result.exit_code == 1
        assert "Could not detect key type" in result.stderr

    def test_convert_same_format_warning(self):
        """Test converting key to same format shows warning."""
        # Generate a hex key
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        hex_private = data["private_key"]

        # Convert hex to hex (same format)
        result = self.runner.invoke(
            app, ["keys", "convert", hex_private, "--to", "hex", "--type", "private"]
        )

        assert result.exit_code == 0
        assert "Key is already in hex format" in result.stderr
        assert "Result:" in result.stdout

    def test_convert_json_output(self):
        """Test conversion with JSON output."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        bech32_private = data["private_key"]

        # Convert to hex with JSON output
        result = self.runner.invoke(
            app, ["keys", "convert", bech32_private, "--to", "hex", "--json"]
        )

        assert result.exit_code == 0

        # Parse JSON output
        output_data = json.loads(result.stdout)
        assert "original_key" in output_data
        assert "original_format" in output_data
        assert "original_type" in output_data
        assert "converted_key" in output_data
        assert "target_format" in output_data

        assert output_data["original_key"] == bech32_private
        assert output_data["original_format"] == "bech32"
        assert output_data["original_type"] == "private"
        assert output_data["target_format"] == "hex"
        assert len(output_data["converted_key"]) == 64

    def test_convert_file_output(self):
        """Test conversion with file output."""
        # Generate a bech32 key first
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        bech32_private = data["private_key"]

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir) / "converted_key.txt"

            # Convert to hex with file output
            result = self.runner.invoke(
                app,
                [
                    "keys",
                    "convert",
                    bech32_private,
                    "--to",
                    "hex",
                    "--output",
                    str(tmp_path),
                ],
            )

            assert result.exit_code == 0
            assert "Converted key written to" in result.stdout

            # Read the file
            output_content = tmp_path.read_text().strip()
            assert len(output_content) == 64
            assert all(c in "0123456789abcdef" for c in output_content.lower())

    def test_convert_roundtrip_private(self):
        """Test roundtrip conversion private key: hex->bech32->hex."""
        # Generate original hex key
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        original_hex = data["private_key"]

        # Convert hex to bech32
        result1 = self.runner.invoke(
            app,
            [
                "keys",
                "convert",
                original_hex,
                "--to",
                "bech32",
                "--type",
                "private",
                "--json",
            ],
        )
        assert result1.exit_code == 0
        data1 = json.loads(result1.stdout)
        bech32_key = data1["converted_key"]

        # Convert bech32 back to hex
        result2 = self.runner.invoke(
            app, ["keys", "convert", bech32_key, "--to", "hex", "--json"]
        )
        assert result2.exit_code == 0
        data2 = json.loads(result2.stdout)
        final_hex = data2["converted_key"]

        # Should match original
        assert final_hex == original_hex

    def test_convert_roundtrip_public(self):
        """Test roundtrip conversion public key: hex->bech32->hex."""
        # Generate original hex key
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        original_hex = data["public_key"]

        # Convert hex to bech32
        result1 = self.runner.invoke(
            app,
            [
                "keys",
                "convert",
                original_hex,
                "--to",
                "bech32",
                "--type",
                "public",
                "--json",
            ],
        )
        assert result1.exit_code == 0
        data1 = json.loads(result1.stdout)
        bech32_key = data1["converted_key"]

        # Convert bech32 back to hex
        result2 = self.runner.invoke(
            app, ["keys", "convert", bech32_key, "--to", "hex", "--json"]
        )
        assert result2.exit_code == 0
        data2 = json.loads(result2.stdout)
        final_hex = data2["converted_key"]

        # Should match original
        assert final_hex == original_hex

    def test_convert_verbose_mode(self, monkeypatch):
        """Test convert command in verbose mode."""
        # Set verbose environment variable
        monkeypatch.setenv("NOSTRESS_VERBOSE", "1")

        # Generate a bech32 key first (avoiding verbose mode for generation)
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        # Parse the JSON to get the keys (verbose mode still outputs JSON correctly)
        # Extract JSON from the verbose output
        lines = gen_result.stdout.strip().split("\n")
        json_start = None
        for i, line in enumerate(lines):
            if line.strip().startswith("{"):
                json_start = i
                break

        json_lines = lines[json_start:]
        json_content = "\n".join(json_lines)
        data = json.loads(json_content)
        bech32_private = data["private_key"]

        # Convert with verbose mode
        result = self.runner.invoke(
            app, ["keys", "convert", bech32_private, "--to", "hex"]
        )

        assert result.exit_code == 0
        # In verbose mode, we expect additional information
        assert "Detecting key type" in result.stdout
        assert "Detected nsec (private) bech32 key" in result.stdout
        assert "Converting from bech32 to hex" in result.stdout


class TestIntegration:
    """Integration tests combining multiple commands."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_generate_then_validate_hex(self):
        """Test generating a key then validating it."""
        # Generate key
        gen_result = self.runner.invoke(app, ["keys", "generate", "--json"])
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        private_key = data["private_key"]
        public_key = data["public_key"]

        # Validate private key
        val_result = self.runner.invoke(app, ["keys", "validate", private_key])
        assert val_result.exit_code == 0

        # Validate public key
        val_result = self.runner.invoke(app, ["keys", "validate", public_key])
        assert val_result.exit_code == 0

    def test_generate_then_validate_bech32(self):
        """Test generating bech32 keys then validating them."""
        # Generate bech32 keys
        gen_result = self.runner.invoke(
            app, ["keys", "generate", "--format", "bech32", "--json"]
        )
        assert gen_result.exit_code == 0

        data = json.loads(gen_result.stdout)
        private_key = data["private_key"]
        public_key = data["public_key"]

        # Validate private key (nsec)
        val_result = self.runner.invoke(
            app, ["keys", "validate", private_key, "--type", "nsec"]
        )
        assert val_result.exit_code == 0

        # Validate public key (npub)
        val_result = self.runner.invoke(
            app, ["keys", "validate", public_key, "--type", "npub"]
        )
        assert val_result.exit_code == 0

    def test_verbose_mode(self, monkeypatch):
        """Test that verbose mode works."""
        # Set verbose environment variable
        monkeypatch.setenv("NOSTRESS_VERBOSE", "1")

        # Generate key in verbose mode
        result = self.runner.invoke(app, ["keys", "generate"])

        assert result.exit_code == 0
        # In verbose mode, we expect additional information
        # (exact output depends on rich formatting)
