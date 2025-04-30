"""Commands for configuration management.

This module provides CLI commands for managing and viewing configuration settings
for the CodeMie Plugins CLI. It allows users to view, set, and retrieve configuration
values that affect the behavior of the CLI tool.
"""
import os
from typing import Any, Dict, List

import click
from rich.console import Console
from rich.table import Table

from cli.utils import get_config_value, load_config, set_config_value

# Constants for configuration keys
CONFIG_KEY_PLUGIN_KEY = "PLUGIN_KEY"
CONFIG_KEY_PLUGIN_ENGINE_URI = "PLUGIN_ENGINE_URI"
CONFIG_KEY_COMMAND_LINE_TOOL_TIMEOUT = "COMMAND_LINE_TOOL_TIMEOUT"
CONFIG_KEY_CODEMIE_PLUGINS_ROOT = "CODEMIE_PLUGINS_ROOT"

# Constants for UI elements
TABLE_TITLE = "CodeMie Plugins Configuration"
COLUMN_KEY = "Key"
COLUMN_VALUE = "Value"
COLUMN_SOURCE = "Source"
SOURCE_ENVIRONMENT = "Environment"
SOURCE_CONFIG_FILE = "Config File"
NOT_SET_TEXT = "[dim]Not set[/]"

# Console styling
STYLE_KEY = "cyan"
STYLE_VALUE = "green"
STYLE_SOURCE = "yellow"
STYLE_SUCCESS = "green"
STYLE_WARNING = "yellow"
STYLE_ERROR = "bold red"

# Global console instance
console = Console()


@click.group(name="config")
@click.pass_context
def config_cmd(ctx: click.Context) -> None:
    """Manage CLI configuration settings."""
    pass


@config_cmd.command(name="list")
@click.option(
    '--all', 'show_all', is_flag=True, 
    help="List all configuration including environment variables"
)
@click.pass_context
def config_show(ctx: click.Context, show_all: bool) -> None:
    """Show current configuration settings.
    
    Displays a table of configuration values from both environment variables
    and the configuration file. Use the --all flag to show all settings
    including those that aren't set.
    """
    config = load_config()
    
    table = _create_config_table()
    
    # Common config keys to check
    keys = _get_default_config_keys()
    
    if show_all:
        # Add all keys from the config file
        keys.extend([k for k in config.keys() if k not in keys])
    
    _populate_config_table(table, keys, config)
    
    console.print(table)


@config_cmd.command(name="set")
@click.argument("key")
@click.argument("value")
@click.pass_context
def config_set(ctx: click.Context, key: str, value: str) -> None:
    """Set a configuration value.
    
    Args:
        key: The configuration key to set
        value: The value to assign to the key
    """
    try:
        set_config_value(key, value)
        console.print(f"[{STYLE_SUCCESS}]Configuration updated:[/] {key} = {value}")
    except Exception as e:
        console.print(f"[{STYLE_ERROR}]Error setting configuration:[/] {str(e)}")


@config_cmd.command(name="get")
@click.argument("key")
@click.pass_context
def config_get(ctx: click.Context, key: str) -> None:
    """Get a specific configuration value.
    
    Args:
        key: The configuration key to retrieve
    """
    value = get_config_value(key)
    if value is not None:
        console.print(f"{key} = {value}")
    else:
        console.print(f"[{STYLE_WARNING}]Configuration key '{key}' is not set[/]")


def _get_default_config_keys() -> List[str]:
    """Get the list of default configuration keys to display.
    
    Returns:
        A list of the most common configuration keys
    """
    return [
        CONFIG_KEY_PLUGIN_KEY,
        CONFIG_KEY_PLUGIN_ENGINE_URI,
        CONFIG_KEY_COMMAND_LINE_TOOL_TIMEOUT,
        CONFIG_KEY_CODEMIE_PLUGINS_ROOT
    ]


def _create_config_table() -> Table:
    """Create and configure a table for displaying configuration.
    
    Returns:
        A styled Rich Table object ready for configuration data
    """
    table = Table(title=TABLE_TITLE)
    table.add_column(COLUMN_KEY, style=STYLE_KEY)
    table.add_column(COLUMN_VALUE, style=STYLE_VALUE)
    table.add_column(COLUMN_SOURCE, style=STYLE_SOURCE)
    return table


def _populate_config_table(table: Table, keys: List[str], config: Dict[str, Any]) -> None:
    """Fill the table with configuration data.
    
    Args:
        table: The Rich Table to populate
        keys: List of configuration keys to check
        config: The loaded configuration dictionary
    """
    for key in keys:
        # Check environment first
        env_value = os.environ.get(key)
        file_value = config.get(key)
        
        if env_value is not None:
            table.add_row(key, env_value, SOURCE_ENVIRONMENT)
        elif file_value is not None:
            table.add_row(key, str(file_value), SOURCE_CONFIG_FILE)
        else:
            table.add_row(key, NOT_SET_TEXT, "")
