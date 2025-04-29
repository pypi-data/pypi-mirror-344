import os
import shutil
import click
import lamini
from importlib import resources
import pathlib

base_dir = os.path.dirname(lamini.__file__)


@click.group()
def cli():
    """CLI tool for scaffolding projects."""
    pass


@cli.command()
@click.argument("project_type")
@click.argument("project_name")
def create(project_type, project_name):
    """
    Create a new project based on the specified template.
    PROJECT_TYPE: Type of project (e.g., 'Q&A')
    PROJECT_NAME: Name of the new project
    """
    try:
        # Access template files from package data
        with resources.path('lamini.project_templates', project_type) as template_path:
            template_dir = pathlib.Path(template_path)
            if not template_dir.exists():
                click.echo(f"Template for project type '{project_type}' does not exist.")
                return

            target_dir = os.path.join(os.getcwd(), project_name)
            if os.path.exists(target_dir):
                click.echo(f"Project '{project_name}' already exists.")
                return

            shutil.copytree(template_dir, target_dir)
            click.echo(
                f"Project '{project_name}' created successfully using the '{project_type}' template."
            )
    except ModuleNotFoundError:
        click.echo(f"Template for project type '{project_type}' does not exist.")
        return


if __name__ == "__main__":
    cli()
