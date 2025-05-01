from pathlib import Path
import click
import yaml
from cryptography.fernet import Fernet

@click.command()
@click.option("--name", required = True, help='The Project Name')
def init(name):
    """
    Help to create config svd yml

    :param name: project name
    :return: None
    """
    file_path = Path.cwd() / ".config_svd.yml"
    if file_path.exists():
        click.echo("Already config file present")
    else:
        default_config = {"project":
                              {"name": name},
                          "storage":
                              {"name": name,
                               "path": "Default"
                               },
                          "encrypt":
                              {
                                  "key": Fernet.generate_key().decode()
                              }

                          }
        click.echo("creating config file")
        with open(file_path, "w") as fp:
            yaml.safe_dump(default_config, fp)
        click.echo(f"config file created: {file_path}")
