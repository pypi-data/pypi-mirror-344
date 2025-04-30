import os
from importlib.metadata import version
from pathlib import Path

import click

from ditidy.checks.checks import checks
from ditidy.config import parse
from ditidy.error import on_error


@click.command()
@click.version_option(version("ditidy"), message="%(version)s")
@click.option("--config-file", type=str, help="Path of the config file")
def cli(config_file):
    # pick default config file
    if config_file is None:
        p = Path.cwd()/"ditidy.yaml"
        if p.exists():
            config_file = str(p)
        else:
            on_error("config file could not found")

    config_file_dir = os.path.dirname(config_file)
    if os.path.isabs(config_file):
        root_dir = config_file_dir
    else:
        root_dir = os.path.join(os.getcwd(), config_file_dir)

    config = parse(config_file)
    checks(root_dir, config)


if __name__ == "__main__":
    cli()
