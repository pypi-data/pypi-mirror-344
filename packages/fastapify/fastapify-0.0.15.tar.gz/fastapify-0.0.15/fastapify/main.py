import click
from fastapify import __version__
from fastapify.module_functionality.commands import ProjectStructure

command = ProjectStructure()


@click.group()
@click.version_option(version=__version__, prog_name="Fastapify")
def cli():
    pass


@cli.command()
def startproject():
    """
    Create a new Project and app with a specific structure.
    """
    command.startproject()


@cli.command()
@click.argument('app_name')
def startapp(app_name):
    """
    Create a new Project app with a specific structure.
    :param app_name:
    :return:
    """
    command.startapp(app_name)
