"""Main CLI entry point for CodeMie Plugins.

This module provides the main command line interface for CodeMie Plugins,
allowing users to interact with the plugin system through various commands.
It handles configuration, sets up signal handlers for graceful shutdown,
and registers commands for the CLI.
"""
import atexit
import builtins
import logging
import os
import signal
import sys
from pathlib import Path
from typing import Any, List, Optional

import click
from rich.console import Console
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.table import Table

from cli.commands.config_cmd import config_cmd
from cli.commands.development_cmd import development_cmd
from cli.commands.list_cmd import list_cmd
from cli.commands.mcp_cmd import mcp_cmd
from cli.utils import get_config_value, get_version, print_banner

# Constants
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
SHUTDOWN_MESSAGE = "\n[yellow]Keyboard interrupt received, shutting down gracefully...[/]"

# Configuration keys
KEY_DEBUG = "DEBUG"
KEY_CONFIG = "CONFIG"
KEY_PLUGIN_KEY = "PLUGIN_KEY"
KEY_PLUGIN_ENGINE_URI = "PLUGIN_ENGINE_URI"

# Default values
DEFAULT_PLUGIN_ENGINE_URI = "nats://nats-codemie.epmd-edp-anthos.eu.gcp.cloudapp.epam.com:443"

# CLI options
OPT_PLUGIN_KEY = "--plugin-key"
OPT_PLUGIN_ENGINE_URI = "--plugin-engine-uri"
OPT_DEBUG = "--debug/--no-debug"

# CLI option descriptions
DESC_PLUGIN_KEY = "Authentication key for the plugin engine for runtime authentication during CLI execution"
DESC_PLUGIN_ENGINE_URI = f"URI for the plugin engine (typically a NATS server, defaults to {DEFAULT_PLUGIN_ENGINE_URI})"
DESC_DEBUG = "Enable debug mode"

# CLI info
CLI_NAME = "CodeMie Plugins CLI"

# Global objects
console = Console()

# Global registry of running processes to terminate on exit
# A process is any object with terminate(), cancel(), or close() method
RUNNING_PROCESSES: List[Any] = []


class CustomGroup(click.Group):
    """Custom Click Group that shows the banner and formatted help."""
    
    def get_help(self, ctx: click.Context) -> str:
        """Override get_help to show banner and formatted help text."""
        # Print the banner first
        print_banner()
        
        # Format and display help in a pretty way using Rich
        self._format_help_with_rich(ctx)
        
        # Return empty string since we've already printed the help
        return ""
    
    def _format_help_with_rich(self, ctx: click.Context) -> None:
        """Format and display help using Rich tables."""
        # Print description panel
        self._print_description_panel(ctx)
        
        # Print commands table if this is a group
        if isinstance(ctx.command, click.Group):
            self._print_commands_table(ctx)
        
        # Print usage panel with examples
        self._print_usage_panel(ctx)

        # Print options table
        self._print_options_table(ctx)
    
    def _print_description_panel(self, ctx: click.Context) -> None:
        """Print a panel containing the command description."""
        description = ctx.command.help or "No description available."
        desc_panel = Panel(
            Text(description, style="cyan"),
            border_style="blue",
            title="Description",
            expand=False
        )
        console.print(desc_panel)
    
    def _print_options_table(self, ctx: click.Context) -> None:
        """Print a table containing the command options."""
        options_table = Table(title="Options", box=box.ROUNDED, border_style="blue", expand=False)
        options_table.add_column("Option", style="green")
        options_table.add_column("Description", style="white")
        options_table.add_column("Default", style="yellow")
        
        for param in ctx.command.params:
            if param.hidden:
                continue
            
            option_name = self._format_option_name(param)
            help_text = param.help or ""
            default = self._format_default_value(param)
            
            options_table.add_row(option_name, help_text, default)
        
        console.print(options_table)
    
    def _format_option_name(self, param) -> str:
        """Format the option name from parameter opts and secondary_opts."""
        names = []
        names.extend(param.opts)
        names.extend(param.secondary_opts)
        return ", ".join(names)
    
    def _format_default_value(self, param) -> str:
        """Format the default value for a parameter."""
        if param.default is not None and param.default != "" and not param.is_flag:
            return str(param.default)
        elif param.is_flag and param.default:
            return "Enabled"
        elif param.is_flag:
            return "Disabled"
        return ""
    
    def _print_commands_table(self, ctx: click.Context) -> None:
        """Print a table containing the available commands."""
        commands_table = Table(title="Commands", box=box.ROUNDED, border_style="blue", expand=False)
        commands_table.add_column("Command", style="green")
        commands_table.add_column("Description", style="white")
        
        commands = getattr(ctx.command, "commands", {})
        if not commands:
            return
            
        # Sort commands by name
        command_list = sorted(commands.items(), key=lambda x: x[0])
        
        # Add each command to the table
        for cmd_name, cmd in command_list:
            cmd_help = cmd.get_short_help_str() or "No description available."
            commands_table.add_row(cmd_name, cmd_help)
        
        console.print(commands_table)
    
    def _print_usage_panel(self, ctx: click.Context) -> None:
        """Print a panel containing usage information and examples."""
        usage_text = self.get_usage(ctx)
        examples = self._get_command_examples(ctx)
        
        usage_panel = Panel(
            Text.assemble(
                Text(usage_text + "\n\n", style="white"),
                Text("Examples:\n", style="bold yellow"),
                Text(examples, style="green")
            ),
            border_style="blue",
            title="Usage",
            expand=False
        )
        console.print(usage_panel)
        
    def _get_command_examples(self, ctx: click.Context) -> str:
        """Get command-specific examples for the help text."""
        # Base examples for the main CLI
        if ctx.command.name == "cli" and not ctx.parent:
            return (
                "# Show CLI version\n"
                "codemie-plugins --version\n\n"
                "# Configure your plugin key\n"
                "codemie-plugins config set PLUGIN_KEY your-plugin-key\n\n"
                "# List available MCP servers\n"
                "codemie-plugins mcp list\n\n"
                "# Run MCP with JetBrains IDE servers\n"
                "codemie-plugins mcp run -s jetbrains\n\n"
                "# Run MCP with filesystem and CLI servers\n"
                "codemie-plugins mcp run -s filesystem,cli-mcp-server\n\n"
                "# Run development toolkit on a repository\n"
                "codemie-plugins development run --repo-path /path/to/repo\n\n"
                "# Enable debug mode for any command\n"
                "codemie-plugins --debug mcp run -s filesystem"
            )
        
        # Command-specific examples
        command_name = ctx.command.name
        
        if command_name == "config":
            return (
                "# Show current configuration\n"
                "codemie-plugins config show\n\n"
                "# Show all configuration including environment variables\n"
                "codemie-plugins config show --all\n\n"
                "# Set your plugin key\n"
                "codemie-plugins config set PLUGIN_KEY your-plugin-key\n\n"
                "# Get a specific configuration value\n"
                "codemie-plugins config get PLUGIN_KEY"
            )
        
        elif command_name == "mcp":
            return (
                "# List available MCP servers\n"
                "codemie-plugins mcp list\n\n"
                "# Run a single server\n"
                "codemie-plugins mcp run -s filesystem\n\n"
                "# Run multiple servers\n"
                "codemie-plugins mcp run -s filesystem,cli-mcp-server\n\n"
                "# Run with environment variables\n"
                "codemie-plugins mcp run -s filesystem -e filesystem=FILE_PATHS\n\n"
                "# Run with custom timeout\n"
                "codemie-plugins mcp run -s filesystem -t 120"
            )
        
        elif command_name == "development":
            return (
                "# Run development toolkit on current directory\n"
                "codemie-plugins development run\n\n"
                "# Run development toolkit on a specific repository\n"
                "codemie-plugins development run --repo-path /path/to/repo\n\n"
                "# Run with a custom timeout\n"
                "codemie-plugins development run --timeout 600"
            )
        
        elif command_name == "list":
            return (
                "# List available commands\n"
                "codemie-plugins list\n\n"
                "# List commands with detailed information\n"
                "codemie-plugins list -v"
            )
        
        # Default examples if no specific ones are available
        return (
            "# Get help for this command\n"
            f"codemie-plugins {command_name} --help"
        )


def print_version(ctx, param, value):
    """Custom version callback that shows the banner before printing version."""
    if not value or ctx.resilient_parsing:
        return
    
    # Print the banner first
    version = print_banner()
    
    # Then print version info in Click's format and exit
    click.echo(f"{CLI_NAME}, version {version}")
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS, cls=CustomGroup)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help='Show version and exit')
@click.option(
    OPT_PLUGIN_KEY,
    envvar=KEY_PLUGIN_KEY,
    help=DESC_PLUGIN_KEY,
)
@click.option(
    OPT_PLUGIN_ENGINE_URI,
    envvar=KEY_PLUGIN_ENGINE_URI,
    help=DESC_PLUGIN_ENGINE_URI,
)
@click.option(OPT_DEBUG, default=False, help=DESC_DEBUG)
@click.pass_context
def cli(
    ctx: click.Context,
    plugin_key: Optional[str],
    plugin_engine_uri: Optional[str],
    debug: bool,
) -> None:
    """CodeMie Plugins CLI - Run CodeMie toolkits without requiring devbox."""
    # Ensure the context object exists and is a dictionary
    ctx.ensure_object(dict)

    # Add project root to PYTHONPATH to ensure imports work correctly
    _add_project_root_to_path()

    # Banner is now printed by the CustomGroup.get_help method when no subcommand is provided
    # For subcommands, we still want to print the banner here
    if ctx.invoked_subcommand is not None:
        print_banner()

    # Store configuration in context
    ctx.obj[KEY_DEBUG] = debug
    ctx.obj[KEY_CONFIG] = {
        KEY_PLUGIN_KEY: plugin_key,
        KEY_PLUGIN_ENGINE_URI: plugin_engine_uri,
    }

    # Resolve configuration values from multiple sources
    resolved_plugin_key = plugin_key or os.getenv(KEY_PLUGIN_KEY) or get_config_value(KEY_PLUGIN_KEY)
    resolved_plugin_engine_uri = (
        plugin_engine_uri
        or os.getenv(KEY_PLUGIN_ENGINE_URI)
        or get_config_value(KEY_PLUGIN_ENGINE_URI)
        or DEFAULT_PLUGIN_ENGINE_URI
    )

    # Set environment variables for nested commands
    if resolved_plugin_key:
        os.environ[KEY_PLUGIN_KEY] = resolved_plugin_key
    # Always set the plugin engine URI (using default if not provided)
    os.environ[KEY_PLUGIN_ENGINE_URI] = resolved_plugin_engine_uri

    # Set up logging if debug is enabled
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    # Setup signal handlers for graceful shutdown
    _setup_graceful_shutdown()


def _add_project_root_to_path() -> None:
    """Add the project root directory to Python path for imports."""
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def _setup_graceful_shutdown() -> None:
    """Configure signal handlers to ensure graceful shutdown."""
    # Register cleanup function to be called at exit
    atexit.register(_cleanup_processes)

    # Register signal handlers
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)


def _cleanup_processes():
    """Clean up all registered processes on exit."""
    for process in RUNNING_PROCESSES:
        try:
            if hasattr(process, "terminate") and callable(process.terminate):
                process.terminate()
            elif hasattr(process, "cancel") and callable(process.cancel):
                process.cancel()
            elif hasattr(process, "close") and callable(process.close):
                process.close()
        except Exception:
            # We don't want cleanup exceptions to interrupt the shutdown process
            pass


def _signal_handler(sig: int, frame: Any) -> None:
    """Handle termination signals by cleaning up and exiting.
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    console.print(SHUTDOWN_MESSAGE, highlight=False)
    _cleanup_processes()
    sys.exit(0)


def register_process(process: Any) -> None:
    """Register a process to be terminated on exit.
    
    Args:
        process: Any process-like object with terminate(), cancel(), or close() method
    """
    RUNNING_PROCESSES.append(process)


# Global function name used by other modules
REGISTER_PROCESS_NAME = "register_codemie_process"

# Make the register_process function available to all modules
setattr(builtins, REGISTER_PROCESS_NAME, register_process)


# Add commands to the CLI group
cli.add_command(list_cmd)
cli.add_command(config_cmd)
cli.add_command(mcp_cmd)
cli.add_command(development_cmd)


if __name__ == "__main__":
    cli(obj={})
