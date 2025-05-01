import click
from .cmd import init

@click.group()
def cli():
    pass

@click.group()
def config():
    pass

config.add_command(init)

cli.add_command(config)