"""Configuration management."""

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from ..exceptions import ConfigurationError


@dataclass
class NostressConfig:
    """Configuration for nostress CLI."""

    # Default key format
    default_key_format: str = "hex"

    # Output preferences
    verbose: bool = False
    color_output: bool = True

    # Security settings
    require_password_confirmation: bool = True
    min_password_length: int = 8

    # File paths
    default_output_dir: str | None = None

    @classmethod
    def default(cls) -> "NostressConfig":
        """Create default configuration.

        Returns:
            NostressConfig: Default configuration
        """
        return cls()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary.

        Returns:
            dict: Configuration as dictionary
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NostressConfig":
        """Create from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            NostressConfig: Configuration instance
        """
        # Filter only valid fields
        valid_fields = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


def get_config_dir() -> Path:
    """Get configuration directory path.

    Returns:
        Path: Configuration directory
    """
    # Use XDG_CONFIG_HOME if available, otherwise ~/.config
    config_home = os.environ.get("XDG_CONFIG_HOME")
    if config_home:
        return Path(config_home) / "nostress"
    else:
        return Path.home() / ".config" / "nostress"


def get_config_file_path() -> Path:
    """Get configuration file path.

    Returns:
        Path: Configuration file path
    """
    return get_config_dir() / "config.json"


def load_config() -> NostressConfig:
    """Load configuration from file.

    Returns:
        NostressConfig: Loaded configuration or default if file doesn't exist

    Raises:
        ConfigurationError: If configuration file is invalid
    """
    config_file = get_config_file_path()

    if not config_file.exists():
        return NostressConfig.default()

    try:
        with config_file.open("r") as f:
            data = json.load(f)

        return NostressConfig.from_dict(data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        raise ConfigurationError(f"Invalid configuration file: {e}") from e
    except OSError as e:
        raise ConfigurationError(f"Failed to read configuration file: {e}") from e


def save_config(config: NostressConfig) -> None:
    """Save configuration to file.

    Args:
        config: Configuration to save

    Raises:
        ConfigurationError: If saving fails
    """
    config_file = get_config_file_path()

    try:
        # Create directory if it doesn't exist
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Write configuration
        with config_file.open("w") as f:
            json.dump(config.to_dict(), f, indent=2)

    except OSError as e:
        raise ConfigurationError(f"Failed to save configuration: {e}") from e


def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific configuration setting.

    Args:
        key: Setting key
        default: Default value if setting not found

    Returns:
        Any: Setting value or default
    """
    try:
        config = load_config()
        return getattr(config, key, default)
    except ConfigurationError:
        return default


def set_setting(key: str, value: Any) -> None:
    """Set a specific configuration setting.

    Args:
        key: Setting key
        value: Setting value

    Raises:
        ConfigurationError: If setting cannot be saved
    """
    try:
        config = load_config()
        setattr(config, key, value)
        save_config(config)
    except AttributeError as e:
        raise ConfigurationError(f"Invalid configuration key: {key}") from e
