import click
import os
from .main import run_rooq

@click.command()
@click.argument('directory', default='.')
def main(directory):
    """Run Rooq on the specified directory."""
    if not os.path.isdir(directory):
        click.echo(f"Error: {directory} is not a valid directory.")
        return
    
    run_rooq(directory)

if __name__ == '__main__':
    main()