import os
from importlib.metadata import version

import click

from ditidy.checks.checks import checks
from ditidy.config import parse


@click.command()
@click.version_option(version("ditidy"), message="%(version)s")
@click.option("--config-file", required=True, type=str, help="Path of the config file")
def cli(config_file):
    config_file_dir = os.path.dirname(config_file)
    if os.path.isabs(config_file):
        root_dir = config_file_dir
    else:
        root_dir = os.path.join(os.getcwd(), config_file_dir)

    config = parse(config_file)
    checks(root_dir, config)


if __name__ == "__main__":
    cli()
