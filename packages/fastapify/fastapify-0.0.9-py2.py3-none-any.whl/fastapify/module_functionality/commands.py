import os
import click
from pathlib import Path


class ProjectStructure:

    def __init__(self):
        self.project_name = None
        self.required_files = [
            '__init__.py',
            'admin.py',
            'models.py',
            'router.py',
            'schema.py',
            'service.py',

        ]
        self.source_folder = 'src'
        self.config_folder = 'core'
        self.env_folder = '.envs'
        self.compose_folder = 'compose'

    def create_env(self):
        """
        Create a new Project and app with a specific structure.
        """
        base_dir = Path.cwd() / self.env_folder
        os.makedirs(base_dir, exist_ok=True)

        os.makedirs(base_dir / '.local', exist_ok=True)
        os.makedirs(base_dir / '.prod', exist_ok=True)

        click.echo(f"Environment folder successfully created at {base_dir}")

    def create_compose(self):
        """
        Create a new Project and app with a specific structure.
        """
        base_dir = Path.cwd()
        compose_folder = base_dir / self.compose_folder
        os.makedirs(compose_folder, exist_ok=True)

        os.makedirs(compose_folder / 'local' / 'django', exist_ok=True)
        os.makedirs(compose_folder / 'prod' / 'django', exist_ok=True)

        if not (base_dir / 'local.yml').exists():
            with open(base_dir / 'local.yml', 'w') as f:
                pass

        if not (base_dir / 'prod.yml').exists():
            with open(base_dir / 'prod.yml', 'w') as f:
                pass

        click.echo(f"Compose folder successfully created at {base_dir}")

    def create_config(self):
        """
        Create a new Project and app with a specific structure.
        :return:
        """
        base_dir = Path.cwd()
        config_folder = base_dir / self.config_folder
        os.makedirs(config_folder, exist_ok=True)
        with open(config_folder / 'config.py', 'w') as f:
            template_path = Path(__file__).parent / 'templates/config.txt'
            output_path = config_folder / 'config.py'
            self.render_to_string(template_path, output_path)

        with open(config_folder / 'database.py', 'w') as f:
            template_path = Path(__file__).parent / 'templates/database.txt'
            output_path = config_folder / 'database.py'
            self.render_to_string(template_path, output_path)

        with open(config_folder / 'middlewares.py', 'w') as f:
            pass

    def create_src(self):
        """
        create src folder in the app folder
        :return:
        """
        base_dir = Path.cwd()
        source_folder = base_dir / self.source_folder
        os.makedirs(source_folder, exist_ok=True)
        if not (source_folder / '__init__.py').exists():
            with open(source_folder / '__init__.py', 'w') as f:
                pass

        template_path = Path(__file__).parent / 'templates/api.txt'
        output_path = source_folder / 'api.py'
        self.render_to_string(template_path, output_path)

        template_path = Path(__file__).parent / 'templates/main.txt'
        output_path = base_dir / 'main.py'
        self.render_to_string(template_path, output_path)

    def render_to_string(self, template_path, output_path, placeholders=None):

        # Ensure the template file exists
        template_file = Path(template_path)
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found at {template_file}")

        # Read the template file
        with open(template_file, 'r') as file:
            content = file.read()

        # Replace placeholders if provided
        if placeholders:
            for placeholder, value in placeholders.items():
                content = content.replace(f"{{{{ {placeholder} }}}}", value)  # Replace {{ placeholder }}

        # Write the processed content to the output file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        with open(output_file, 'w') as file:
            file.write(content)

        click.echo(f"File '{output_file}' created successfully.")

    def startproject(self):
        """
        Create a new Project and app with a specific structure.
        """
        # Define the folder structure

        # Create the base directory for the project
        base_dir = Path.cwd()
        os.makedirs(base_dir, exist_ok=True)

        # Create the folder structure
        self.create_env()
        self.create_compose()
        self.create_config()
        self.create_src()

        click.echo(f"Project successfully created at {base_dir}")

    def startapp(self, app_name):
        """
        Create a new Project app with a specific structure.
        :param app_name:
        :return:
        """
        # firstly search 'src' folder in the current path and create it if not exists
        # than create app folder in the src folder
        src_path = Path.cwd() / 'src'
        if not src_path.exists():
            os.makedirs(src_path, exist_ok=True)
            click.echo(f"src folder created at {src_path}")

        app_path = src_path / app_name
        os.makedirs(app_path, exist_ok=True)

        # Create the file structure
        for file in self.required_files:
            file_path = app_path / file
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    pass
        click.echo(f"App '{app_name}' created successfully at {app_path}")


def current_path():
    """
    print current path
    :return:
    """
    c_path = os.getcwd()
    click.echo(f"Current path: {c_path}")
    return c_path


def create_src():
    """
    create src folder in the app folder
    :return:
    """
    os.makedirs('src', exist_ok=True)

    click.echo("src folder created successfully.")
