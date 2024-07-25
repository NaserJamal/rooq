import click
import os
from .main import run_rooq
from .config import ensure_api_key, update_api_key

@click.group(invoke_without_command=True)
@click.pass_context
@click.argument('directory', default='.', required=False)
def cli(ctx, directory):
    """Rooq: A tool to automatically fix Flake8 issues using GPT."""
    if ctx.invoked_subcommand is None:
        if not os.path.isdir(directory):
            click.echo(f"Error: {directory} is not a valid directory.")
            return
        
        ensure_api_key()
        run_rooq(directory)

@cli.command()
def key():
    """Update the OpenAI API key."""
    update_api_key()
    click.echo("API key updated successfully.")

def main():
    cli()

if __name__ == '__main__':
    main()