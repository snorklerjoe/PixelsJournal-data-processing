"""This module is the entry point for the Pixels Processor application.
"""

import os
import toml
import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.command()
@click.option('--config', default='config.toml', help='Path to configuration file')
def main(config):
    if not os.path.exists(config):
        console.print(f'[red]Configuration file not found at {config}[/red]')
        return

    # Load configuration from TOML file
    with open(config, 'r') as f:
        config_data = toml.load(f)

    # Print configuration to console
    table = Table(title='Configuration')
    for key, value in config_data.items():
        table.add_column(key)
        table.add_row(str(value))
    console.print(table)

if __name__ == '__main__':
    main()
