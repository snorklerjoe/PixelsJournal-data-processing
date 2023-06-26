"""This module is the entry point for the Pixels Processor application.
"""

import os
import toml
import click
from rich.console import Console
from rich.table import Table

from pixelsprocessor.data.pixeldb import PixelDb, PixelDbQuery

console = Console()

@click.command()
@click.option('--config', default='config.toml', help='Path to configuration file')
def main(config):
    # Print title screen
    console.print("[bold magenta]Pixels Processor[/bold magenta]")
    console.print("  A data processing tool for Pixels Journal app data\n")

    if not os.path.exists(config):
        console.print(f'[red]Configuration file not found at {config}[/red]')
        return

    # Load configuration from TOML file
    with open(config, 'r') as f:
        config_data = toml.load(f)
    console.print(f"[green]Configuration file loaded from [italic]{config}[/italic][/green]\n")

    # Load data from JSON file
    datafile = config_data['data']['source']['file']
    if not os.path.exists(datafile):
        console.print(f'[red]Data file not found at {datafile}[/red]')
        return
    with open(datafile, 'r') as f:
        db = PixelDb.from_json_str(f.read())
    console.print(f"[green]Data file loaded from [italic]{datafile}[/italic][/green]")
    console.print(f"  [bold]Pixel count:[/bold] {len(db.pixels)}")
    console.print(f"  [bold]Categories:[/bold] {(db.categories)}")

    # Execute initial filter query
    query_string = config_data['data']['filtering']['query']
    if query_string:
        console.print(f"\n[bold]Initial query:[/bold] {query_string}")
        query = PixelDbQuery()
        query.parse(query_string)
        filtered_pixels = query.execute(db)
        console.print(f"  [bold]Filtered pixel count:[/bold] {len(filtered_pixels)}")
        datadb = PixelDb(filtered_pixels, db.categories)
    else:
        datadb = db
    
    # Execute data processing steps
    

if __name__ == '__main__':
    main()
