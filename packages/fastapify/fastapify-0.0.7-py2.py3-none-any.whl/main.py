import click

from app.module_functionality.commands import current_path, create_src, ProjectStructure

command = ProjectStructure()


@click.group()
def cli():
    pass


@cli.command()
@click.option('-n', '--name', type=str, help='Name to greet', default='World')
def hello(name):
    click.echo(f'Hello {name}')


@cli.command()
def path():
    current_path()


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
